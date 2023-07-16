import requests
from config import URL,AWS
import json
import redshift_connector as r
import pandas as pd
from datetime import datetime as dt

def extract_data ():

    response = requests.get(URL['characters'])
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

    # with open('texto.json','w') as file:
    #     json.dump(lista,file,indent=4)

    return lista

def transform(registros):

    #fecha para insercion en base de datos
    fecha_insercion_bd = str(dt.date(dt.now()))
    
    # Tomamos los datos extraidos como diccionario y generamos un data frame
    df = pd.DataFrame.from_dict(registros,orient='index')

    # Eliminamos los duplicados
    df_not_duplicates = df.drop_duplicates()

    df_not_duplicates['fecha_insercion_bd'] = fecha_insercion_bd

    return df_not_duplicates

def load_data(dataframe):

    # Conexion a la bd de redshift
    conn = r.connect(
        user=AWS['USR_AWS'],
        password=AWS['USR_PASS'],
        database=AWS['DATABASE'],
        host=AWS['HOST'],
        port=int(AWS['PORT'])
    )

    schema = AWS['SCHEMA']

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
    nombres_columnas = '","'.join([str(i) for i in df.columns.tolist()])

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
    

if __name__ == '__main__':
    
    data = extract_data()

    df = transform(data)

    load_data(df)
