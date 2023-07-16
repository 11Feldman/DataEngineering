# CoderHouse
## Data Engineering
### Repositorio de ejercicios de CoderHouse 

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

:point_right: + A. Se debe conectar a una Api publica para extraer datos
:point_right: + B. Crear tablas en Redshift.
:point_right: + C. Verificar si hay duplicados con Pandas.
:point_right: + D. Insertar datos desde un data frame en Redshift.

Se toman datos de la api de marvel https://developer.marvel.com/.

Para este caso se usa AirFlow:

Usando DAGS, Operadores, Tareas y XCOMs.

Apache Airflow se levanta con un docker-compose.

Las credenciales a la api y las variables de conexion a AWS se encuentran en la configuracion de AirFlow para mantenerlas de manera secreta y encriptadas.


