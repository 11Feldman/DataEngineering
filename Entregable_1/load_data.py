from config import AWS
import redshift_connector as r
import pandas as pd
from extract_api import extract_data
from datetime import datetime as dt

# Obtencion de datos.
registros = extract_data()

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

for i in registros:

    id_character =int(i['id_character'])
    nombre =i['nombre']
    descripcion =str(i['descripcion'][0:254]).replace("'","")
    cantidad_de_comics = i['cantidad_de_comics']
    cantidad_de_series = i['cantidad_de_series']
    cantidad_de_historias = i['cantidad_de_historias']
    fecha_modificacion = i['fecha_modificacion'][0:10]
    fecha_insercion_bd = dt.date(dt.now())


    insert = f'INSERT INTO {schema}.marvelcharacters (id_character,nombre, descripcion, cantidad_de_comics, cantidad_de_series, cantidad_de_historias,fecha_modificacion, fecha_insercion_bd)'
    values = f"VALUES({id_character},'{nombre}','{descripcion}', {cantidad_de_comics}, {cantidad_de_series}, {cantidad_de_historias}, '{fecha_modificacion}', '{fecha_insercion_bd}')"
    
    cursor.execute(insert+values)


# Query, posterior ejecucion e impresion de resgistros por consola para verificacion de carga de datos en bd Redshift
query = f'''
    SELECT * FROM {schema}.marvelCharacters
'''

valores = cursor.execute(query).fetchall()

print(valores)