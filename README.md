# CoderHouse
## Data Engineering
### Repositorio de ejercicios de CoderHouse 

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

#### Proyecto:

Utilizando AirFlow

+ A. Se debe conectar a una Api publica para extraer datos
+ B. Crear tablas en Redshift.
+ C. Verificar si hay duplicados con Pandas.
+ D. Insertar datos desde un data frame en Redshift.
+ E. Todo debe realizarse mediante Apache Airflow.


Se toman datos de la api de marvel https://developer.marvel.com/.
Para este caso se usa AirFlow:
Usando DAGS, Operadores, Tareas, XCOMs Variables de entorno, Instancia de contexto.
Apache Airflow se levanta con un docker-compose up.
Las credenciales a la api y las variables de conexion a AWS se encuentran en la configuracion de AirFlow para mantenerlas de manera secreta y encriptadas.


## Comenzando 🚀

Para poder utilizar este proyecto debe copiar el siguiente codigo 

```
git clone 'https://github.com/11Feldman/DataEngineering.git'
```

### Pre-requisitos 📋

Debe tener instaladas estas herramientas.

* [Airflow](https://airflow.apache.org/)  
* [Python](https://www.python.org/)
* [Docker](https://www.docker.com/)
* [DBEAVER-CE](https://dbeaver.io/)

Luego de tener instaladas estas herramientas debe ir a su terminal y ejecutar.

```
pip install -r requirements.txt
```

Su estructura de carpetas debe estar de la siguiente manera.

![Estructura Carpeta](/EntregaFinal_ArielFeldman_DATENG_51935/images/estructura_carpetas.png)


si no lo esta debe verificar y crearlas 'config.py', 'smtplib_test.py' no los tenga en cuenta.

Luego, en la carpeta config, cree 3 archivos json que luego importara en las variables de apache airflow.

```
api_marvel.json
```

![api_marvel.json](/EntregaFinal_ArielFeldman_DATENG_51935/images/api_marvel_images.png)


```
aws_redshift.json
```

![aws_redshift.json](/EntregaFinal_ArielFeldman_DATENG_51935/images/aws_redshift_images.png)


```
smtp_env.json
```

![smtp_env.json](/EntregaFinal_ArielFeldman_DATENG_51935/images/smtp_image.png)


una vez creadas ejecutar en la terminal el siguiente codigo.

```
docker-compose up
```

Finalizado esto.

Ir a http://localhost:8080 ingresar en apache airflow 

user: airflow
pass: airflow

Luego ir a la imagen, buscar los json creados e importarlos.

![variables](/EntregaFinal_ArielFeldman_DATENG_51935/images/variables.png)

la variable de password la debe generar desde su cuenta de gmail en "contrasenia para aplicaciones"

## Ejecutando las pruebas ⚙️ 📦

Para ejecutar las pruebas levanto el docker compose.
<!-- _Explica como ejecutar las pruebas automatizadas para este sistema_ -->
```
docker-compose up
```
finalizado esto. 

Ingreso a airflow y vamos a ejecutar 2 Dag,



### DAG 1

```
Dag 1: --> etl_api_marvel

```
##### Ingreso correcto a la BD.

```
Como fue la corrida de las tareas ...
```
![variables](/EntregaFinal_ArielFeldman_DATENG_51935/images/corrida_correcta.png)

```
Como nos llega el mail de si cada tarea fue correcta.
```
![variables](/EntregaFinal_ArielFeldman_DATENG_51935/images/imagen_gmail_correcta.png)
```
Extract
```
![variables](/EntregaFinal_ArielFeldman_DATENG_51935/images/extract_correcta.png)

```
Transform
```
![variables](/EntregaFinal_ArielFeldman_DATENG_51935/images/transform_correcta.png)

```
Load
```
![variables](/EntregaFinal_ArielFeldman_DATENG_51935/images/load_correcta.png)

### DAG 2

```
Dag 2: --> etl_api_marvel_2

```

##### Buscamos el fallo para mostrar la funcionalidad

```
Como fue la corrida de las tareas ...
```
![variables](/EntregaFinal_ArielFeldman_DATENG_51935/images/corrida_falla.png)

```
Como nos llega el mail de si cada tarea fue correcta.
```
![variables](/EntregaFinal_ArielFeldman_DATENG_51935/images/imagen_gmail_falla.png)

```
Extract
```
![variables](/EntregaFinal_ArielFeldman_DATENG_51935/images/extract_falla.png)

```
Transform
```
![variables](/EntregaFinal_ArielFeldman_DATENG_51935/images/transform_falla.png)

```
Load
```
![variables](/EntregaFinal_ArielFeldman_DATENG_51935/images/load_falla.png)


## Construido con 🛠️

* [Airflow](https://airflow.apache.org/) - plataforma creada por la comunidad para crear, programar y monitorear flujos de trabajo mediante programación.
* [Python](https://www.python.org/) - Tecnologia utilizada para el proyecto
* [Docker](https://www.docker.com/) - Usado para generar el docker-compose
* [API MARVEL](https://developer.marvel.com/) - Se utiliza esta api para extraer informacion
* [AWS Redshift](https://aws.amazon.com/es/redshift/) - Base de datos utilizada para leer y cargar datos.
* [Pandas](https://pandas.pydata.org/) - Tecnologia utilizada para el proyecto
* [PySpark](https://spark.apache.org/docs/latest/api/python/) - Tecnologia utilizada para el proyecto
* [Jupyter Notebook](https://jupyter.org/) - Tecnologia utilizada para el proyecto
* [VSC](https://code.visualstudio.com/) - IDLE utilizado para el proyecto.
* [DBEAVER-CE](https://dbeaver.io/) - Universal Database Tool 

## Versionado 📌

Para todas las versiones disponibles, mira los [tags en este repositorio](https://github.com/11Feldman/DataEngineering/tags).

## Autores ✒️

* **Ariel Feldman** - [feldmanam](https://github.com/feldman11)

## Licencia 📄

[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Naereen/badges/)
