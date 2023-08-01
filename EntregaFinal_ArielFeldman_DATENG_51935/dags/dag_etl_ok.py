from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
import json
import requests
import pandas as pd
import redshift_connector as r
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

v_marvel= Variable.get('api_marvel',deserialize_json=True)
v_aws = Variable.get('aws_redshift',deserialize_json=True)
v_smtp = Variable.get('var_smtp', deserialize_json=True)
v_smtp_pass=Variable.get('SMTP_PASSWORD')


def send_email(context):

    state=context['task_instance'].state
    task_id=context['task_instance'].task_id
    dag_id=context['task_instance'].dag_id
    execution_date=context['task_instance'].execution_date
    next_execution_date = context.get('next_execution_date')
    start_date=context['task_instance'].start_date
    end_date=context['task_instance'].end_date
    duration=context['task_instance'].duration
    operator=context['task_instance'].operator
    priority_weight=context['task_instance'].priority_weight


    succes_message = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Ejecucion sin problemas</title>
        </head>
        <body>
            <b><h1> Estado : {state} </h1></b>
            <b><h1> DAG : {dag} </h1></b>
            <b><h1> TASK : {task} </h1></b>
            <p> Fecha de ejecucion: {execution}.</p>
            <p> Proxima ejecucion: {next_execution}.</p>
            <p> Comienzo: {start}.</p>
            <p> Fin: {end}.</p>            
            <p> Duracion: {duration}.</p>
            <p> Operador: {operator}.</p>
            <p> Prioridad: {priority}.</p>
            <p> Si necesitas ayuda, no dudes en contactarnos.</p>
        </body>
    </html>
    """.format(
        state=state,
        dag=dag_id,
        task=task_id,
        execution=execution_date,
        next_execution=next_execution_date,
        start=start_date,
        end=end_date,
        duration=duration,
        operator=operator,
        priority=priority_weight
    )

    x=smtplib.SMTP('smtp.gmail.com',int(v_smtp['PORT']))
    x.starttls()
    x.login(v_smtp['EMAIL'],v_smtp_pass)

    # Crear el objeto del mensaje y establecer los datos del encabezado
    message = MIMEMultipart('alternative')
    message['From'] = v_smtp['EMAIL']
    message['To'] = v_smtp['EMAIL']
    message['Subject'] = f'Status: "{state}" TASK "{task_id}" DAG "{dag_id}"'

    # Agregar el contenido del mensaje en formato HTML
    message.attach(MIMEText(succes_message, 'html'))

    x.sendmail(
        from_addr=v_smtp['EMAIL'],
        to_addrs='arielmfeldman.af@gmail.com',
        msg=message.as_string(),
    )

def extract_data (ti):

    response = requests.get(v_marvel['SECRET_URL_API_MARVEL'])
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

    ti.xcom_push(
        key='data_marvel', # Nombre de clave que se guardara para que lo llamen de otra tarea
        value=lista # valor que se guarda para enviar a otra tarea.
    )

    ti.xcom_push(
        key='count_data_marvel', # Nombre de clave que se guardara para que lo llamen de otra tarea
        value=len(lista) # valor que se guarda para enviar a otra tarea.
    )

def transform(ti):
    
    registros = ti.xcom_pull(
        key='data_marvel', # nombre que tiene la tarea anterior en su key de xcom_push
        task_ids='extract' # nombre de funcion anterior que nos envia el dato
    )

    # Tomamos los datos extraidos como diccionario y generamos un data frame
    df = pd.DataFrame.from_dict(registros,orient='index')

    # Eliminamos los duplicados
    df_not_duplicates = df.drop_duplicates()

    data_dict = df_not_duplicates.to_dict()

    ti.xcom_push(
        key='data_transformada',
        value=data_dict
    )

    ti.xcom_push(
        key='count_data_transformada',
        value=len(data_dict)
    )

def load_data(ti):

    #fecha para insercion en base de datos
    fecha_insercion_bd = str(datetime.date(datetime.now()))


    data = ti.xcom_pull( 
        key='data_transformada', 
        task_ids='transform'
    )
    
    df = pd.DataFrame.from_dict(data,orient='columns')

    df['fecha_insercion_bd'] = fecha_insercion_bd


    # Conexion a la bd de redshift
    conn = r.connect(
            user=v_aws['USER'],
            password=v_aws['PASS'],
            database=v_aws['DATABASE'],
            host=v_aws['HOST'],
            port=int(v_aws['PORT'])
    )

    schema = v_aws['SCHEMA']

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

    # Hago una comprension de listas para obtener las columnas para el 'insert'
    nombres_columnas = '","'.join([str(i) for i in df.columns.tolist()])

    for i,row in df.iterrows():

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
    'retries':1, 
    'retry_delay':timedelta(seconds=20),
    'email':['arielmfeldman.af@gmail.com'], #
    'email_on_retry':['arielmfeldman.af@gmail.com'], #
    'email_on_failure':['arielmfeldman.af@gmail.com'], #
}

# Creacion del dag
with DAG(
    dag_id='etl_api_marvel',
    description='etl api marvel characters',
    default_args=default_args,
    start_date=datetime(2023,7,31,22,57,20),
    tags=['etl_api_marvel_characters'],
    # Intervalo que queremos que se ejecute, para este caso dejamos @daily, 
    # con timedelta podriamos configurar por cualquier dimension de tiempo
    schedule_interval='@daily',
    catchup=False # Si ponemos True corre al momento de subir el dag
) as dag:
    
    # Tareas
    t_extract=PythonOperator(
        task_id='extract',
        python_callable=extract_data,
        on_failure_callback=send_email,
        on_success_callback=send_email,
        provide_context=True
    )
    
    t_transform=PythonOperator(
        task_id='transform',
        python_callable=transform,
        on_failure_callback=send_email,
        on_success_callback=send_email,
        provide_context=True
    )

    t_load=PythonOperator(
        task_id='load',
        python_callable=load_data,
        on_failure_callback=send_email,
        on_success_callback=send_email,
        provide_context=True
    )

    # Ejecucion de tareas
    t_extract >> t_transform >> t_load