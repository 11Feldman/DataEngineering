from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
import json
import requests
import os
import pandas as pd
import redshift_connector as r

marvel_var= Variable.get('api_marvel',deserialize_json=True)
aws_var = Variable.get('aws_redshift',deserialize_json=True)

def guardar_archivo(ruta_archivo,data):
    
    # Verifico si existe el archivo, si existe imprimo eso, si no existe lo genero.
    if os.path.exists(ruta_archivo):
        print('ya existe el archivo')
    else:
        print('No existe el archivo')
        with open(ruta_archivo,'w') as file:
            json.dump(data,file,indent=4)
        
        if os.path.exists(ruta_archivo):
            print('Archivo cargado')
        else:            
            print('No se guardo el archivo ... ')
    
def extract_data ():

    ruta_archivo_json = '/opt/airflow/data/compania1/data_character.json'

    response = requests.get(marvel_var['SECRET_URL_API_MARVEL'])
    lista = {}
    a = 1

    if response.status_code == 200:
        response_json = json.loads(response.text)
        results = response_json['data']['results']
                
        for i in results:
            id_character = i['id']
            nombre = i['name']
            descripcion = i['description']
            comic_disponibles = i['comics']['available']
            series_disponibles = i['series']['available']
            historias_disponibles = i['stories']['available']
            modificacion = i['modified']

            if descripcion == '':
                descripcion = 'Sin descripcion'
            
            dic = {
                'id_character':id_character,
                'nombre': nombre,
                'descripcion': descripcion,
                'cantidad_de_comics': comic_disponibles,
                'cantidad_de_series':series_disponibles,
                'cantidad_de_historias': historias_disponibles,
                'fecha_modificacion': modificacion
            }

            lista[f'{a}'] = dic
            a = a + 1

    guardar_archivo(
        ruta_archivo=ruta_archivo_json,
        data=lista
    )

    transform(registros=lista)
    # return lista

def transform(registros):

    ruta = '/opt/airflow/data/compania1/'
    nombre_archivo = 'data.csv'

    #fecha para insercion en base de datos
    fecha_insercion_bd = str(datetime.date(datetime.now()))
    
    # Tomamos los datos extraidos como diccionario y generamos un data frame
    df = pd.DataFrame.from_dict(registros,orient='index')

    # Eliminamos los duplicados
    df_not_duplicates = df.drop_duplicates()

    df_not_duplicates['fecha_insercion_bd'] = fecha_insercion_bd

    print(df.columns)
    print(df.shape)
    
    if os.path.exists(ruta+nombre_archivo):
        print('Ya existe el csv: ', ruta)
    else:
        df_not_duplicates.to_csv(
            path_or_buf=ruta+nombre_archivo,
            sep='|',
            index=False
        )
        print('archivo guardado')

    # llamo a la funcion para que se inserten los datos.
    load_data(df_not_duplicates)

    # return df_not_duplicates

def load_data(dataframe):

    # Conexion a la bd de redshift
    conn = r.connect(
        user=aws_var['USER'],
        password=aws_var['PASS'],
        database=aws_var['DATABASE'],
        host=aws_var['HOST'],
        port=int(aws_var['PORT'])
    )

    schema = aws_var['SCHEMA']

    conn.rollback()
    conn.autocommit = True

    #creacion de cursor
    cursor = conn.cursor()

    #Query creacion de tabla con clausula if not exits y posterior ejecucion.

    create_table = f'''
        CREATE TABLE IF NOT EXISTS {schema}.marvelCharacters(
            id_character int not null,
            nombre varchar(50) not null,
            descripcion varchar(255) null,
            cantidad_de_comics integer,
            cantidad_de_series integer,
            cantidad_de_historias integer,
            fecha_modificacion date,
            fecha_insercion_bd date
        )
        distkey(id_character)
        sortkey(id_character,fecha_insercion_bd);
    '''

    cursor.execute(create_table)

    # insercion de datos mediante registros (extraccion de datos)

    # Hago una comprension de listas para obtener las columnas para el 'insert'
    nombres_columnas = '","'.join([str(i) for i in dataframe.columns.tolist()])

    for i,row in dataframe.iterrows():

        id_character =int(row['id_character'])
        nombre =row['nombre']
        descripcion =str(row['descripcion'][0:254]).replace("'","")
        cantidad_de_comics = int(row['cantidad_de_comics'])
        cantidad_de_series = int(row['cantidad_de_series'])
        cantidad_de_historias = int(row['cantidad_de_historias'])
        fecha_modificacion = row['fecha_modificacion'][0:10]
        fecha_insercion_bd = row['fecha_insercion_bd']

        # Armo la estructura de Insert y Values para luego ejecutar.
        insert = f'INSERT INTO {schema}.marvelcharacters ("' +nombres_columnas + '") '
        values = f"VALUES({id_character},'{nombre}','{descripcion}', {cantidad_de_comics}, {cantidad_de_series}, {cantidad_de_historias}, '{fecha_modificacion}', '{fecha_insercion_bd}')"
        
        cursor.execute(insert+values)
    
    # Cierro la conexion
    cursor.close()

# Establecer argumentos por default
default_args={
    'owner':'Ariel Feldman',
    'depend_on_past':False,
    'retries':10, 
    'retry_delay':timedelta(minutes=2),
    'email':['arielmfeldman.af@gmail.com'], #
    'email_on_retry':['arielmfeldman.af@gmail.com'], #
    'email_on_failure':['arielmfeldman.af@gmail.com'], #
}

# Creacion del dag
with DAG(
    dag_id='etl_api_marvel_hacia_aws_redshift',
    description='etl de api marvel a aws redshift',
    default_args=default_args,
    start_date=datetime(
        year=datetime.now().year,
        month=datetime.now().month,
        day=datetime.now().day,
        hour=datetime.now().hour,
        minute=datetime.now().minute,
    ),
    tags=['conexion_con_aws_redshift'],
    schedule_interval='@daily'
) as dag:
    
    # Tareas
    task1=PythonOperator(
        task_id='etl',
        python_callable=extract_data
    )

    # Ejecucion de tareas
    task1
