import requests as r
from config import URL
import json

def extract_data ():

    response = r.get(URL)
    lista = []
    
    if response.status_code == 200:
        response_json = json.loads(response.text)
        results = response_json['data']['results']
        #pprint(response_json['data']['results'][0])
                
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
            lista.append(dic)

    else:
        print('error')

    return lista

# registros = extract_data()