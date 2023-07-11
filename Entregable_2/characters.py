from config import AWS
import redshift_connector as r
import pandas as pd

def listado_character():
    
    col_character = 'id'

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

    # Query, posterior ejecucion e impresion de resgistros por consola para verificacion de carga de datos en bd Redshift
    query = f'''
        SELECT distinct id_character FROM {schema}.marvelCharacters
    '''

    valores = cursor.execute(query).fetchall()

    df = pd.DataFrame(valores, columns=[f'{col_character}'])

    cursor.close()

    lista = df[f'{col_character}'].to_list()

    return lista