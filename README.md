# CoderHouse
## Data Engineering
### Repositorio de ejercicios de CoderHouse 

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

#### Entregable 1:
+ A. Se debe conectar a una Api publica para extraer datos
+ B. Crear tablas en Redshift.
+ C. Insertar datos en Redshift.

Se toman datos de la api de marvel https://developer.marvel.com/.

Para este caso las credenciales no se suben y quedan de manera local en un archivo ".py" tambien se genero uno igual como ".env", pero para el caso
se uso los del ".py"
En estos archivos se encuentran.
Las claves publicas y privadas, el hash generado, y los datos de conexion hacia aws.

#### Entregable 2:

+ A. Se debe conectar a una Api publica para extraer datos
+ B. Crear tablas en Redshift.
+ C. Verificar si hay duplicados con Pandas.
+ C. Insertar datos desde un data frame en Redshift.

Se toman datos de la api de marvel https://developer.marvel.com/.

Para este caso las credenciales no se suben y quedan de manera local en un archivo ".py" tambien se genero uno igual como ".env", pero para el caso
se uso los del ".py"
En estos archivos se encuentran.
Las claves publicas y privadas, el hash generado, y los datos de conexion hacia aws.

#### Entregable 3:

Utilizando AirFlow

+ A. Se debe conectar a una Api publica para extraer datos
+ B. Crear tablas en Redshift.
+ C. Verificar si hay duplicados con Pandas.
+ C. Insertar datos desde un data frame en Redshift.

Se toman datos de la api de marvel https://developer.marvel.com/.
Para este caso se usa AirFlow:
Usando DAGS, Operadores, Tareas y XCOMs.
Apache Airflow se levanta con un docker-compose.
Las credenciales a la api y las variables de conexion a AWS se encuentran en la configuracion de AirFlow para mantenerlas de manera secreta y encriptadas.


## Comenzando 🚀
<!-- 
_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._

Mira **Deployment** para conocer como desplegar el proyecto.
 -->

### Pre-requisitos 📋
<!-- 
_Que cosas necesitas para instalar el software y como instalarlas_

```
Da un ejemplo
``` -->

### Instalación 🔧

<!-- _Una serie de ejemplos paso a paso que te dice lo que debes ejecutar para tener un entorno de desarrollo ejecutandose_

_Dí cómo será ese paso_

```
Da un ejemplo
```

_Y repite_

```
hasta finalizar
```

_Finaliza con un ejemplo de cómo obtener datos del sistema o como usarlos para una pequeña demo_ -->

## Ejecutando las pruebas ⚙️

<!-- _Explica como ejecutar las pruebas automatizadas para este sistema_ -->
```
En Desarrollo
```


### Analice las pruebas end-to-end 🔩

<!-- _Explica que verifican estas pruebas y por qué_ -->

```
En Desarrollo
```

### Y las pruebas de estilo de codificación ⌨️
<!-- 
_Explica que verifican estas pruebas y por qué_ -->

```
En Desarrollo
```

## Despliegue 📦 -->

<!-- ```
Agrega notas adicionales sobre como hacer deploy_
``` -->

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

## Versionado 📌

Para todas las versiones disponibles, mira los [tags en este repositorio](https://github.com/11Feldman/DataEngineering/tags).

## Autores ✒️

* **Ariel Feldman** - [feldmanam](https://github.com/feldman11)

## Licencia 📄

[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Naereen/badges/)
