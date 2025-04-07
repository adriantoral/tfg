# Manual Técnico de Uso del Sistema de Catalogación Automática

## Despliegue e Instalación del Sistema

### 1. Hardware probado

- Sistema: Windows 11 (64 bits)
- Memoria RAM: 32GB
- Espacio en disco suficiente para dependencias y base de datos `.mdb`
- Necesario: Microsoft Access (nativo en Windows) y sus drivers ODBC

### 2. Instalación de Python y Dependencias

- Python 3.11 debe estar instalado (`python --version`)
- Instalar pip (usualmente viene incluido)

#### Dependencias del Proyecto

```bash
pip install pyodbc==5.2.0
```

- `pyodbc`: Para conexión con Access

### 3. Driver ODBC para Access

Para verificar que se tienen los drivers necesarios se debe usar una función que se encuentra en `/lib/odbc/checkers`
llamada `check_microsoft_access_drivers` la cual verifica si se tienen los drivers necesarios para la conexión con
Access.

Si no se tienen los drivers necesarios, se debe instalar el driver de Microsoft Access desde la página oficial de
Microsoft.

```python
from lib.odbc.checkers import check_microsoft_access_drivers

check_microsoft_access_drivers( )
```

### 4. Archivo de Base de Datos ETNOCAM

Para usar la aplicacion se debe tener en fichero de base de datos de ETNOCAM, el cual se suele llamar `INPHIS.mdb`. Para
comprobar que el fichero es correcto se puede usar la función que se encuentra en `/lib/odbc/checkers` llamada
`check_microsoft_access_mdb_file` la cual verifica si el fichero es correcto.

```python
from lib.odbc.checkers import check_microsoft_access_mdb_file

FILE = "C:/MiRuta/A/INPHIS.mdb"
check_microsoft_access_mdb_file( FILE )
```

El paso 3 y 4 se pueden unificar usando la función que se encuentra en `/lib/odbc/checkers` llamada `odbc_checkers` la
cual verifica si se tienen los drivers necesarios y si el fichero de base de datos es correcto.

```python
from lib.odbc.checkers import odbc_checkers

FILE = "C:/MiRuta/A/INPHIS.mdb"
odbc_checkers( FILE )
```

### 5. Código Fuente del Sistema

Esta es la estructura de carpetas usada en el proyecto:

```plaintext
lib/
├── inphis/           # Lógica de entidades patrimoniales
├── interfaces/       # Interfaces abstractas
├── odbc/             # Conexión con Access
└── orm/              # ORM genérico
```

---

## Guía de uso

### 1. Conectar con la Base de Datos

```python
from lib.odbc.connection import PyODBCConnection

PyODBCConnection( "C:/MiRuta/A/INPHIS.mdb" )
```

Errores comunes:

- Drivers no encontrados → Ver sección instalación
- Ruta incorrecta → Verificar `.mdb`

Para solucionar estos errores se recomienda usar siempre esta pieza de codigo para crear la conexion:

```python
import os

from lib.odbc.checkers import odbc_checkers
from lib.odbc.connection import PyODBCConnection
from lib.orm.tables.table_index import IGNORE_TABLES, TableIndex

# Ruta a la base de datos de Microsoft Access
DB_PATH = "C:/MiRuta/A/INPHIS.mdb"

# Comprueba si la base de datos de Microsoft Access es accesible y si están los drivers necesarios
odbc_checkers( DB_PATH )

# Conecta a la base de datos de Microsoft Access y obtiene los nombres de las tablas
odbc_connection = PyODBCConnection( DB_PATH )
microsoft_access_tables = [
	table_info.table_name
	for table_info in odbc_connection.cursor.tables( tableType='TABLE' )
	if table_info.table_name not in IGNORE_TABLES
]

# Crea un indice de las tablas de la base de datos
tables = TableIndex( microsoft_access_tables )

# Genera un indice de las tablas de la base de datos y lo guarda en un archivo JSON si no existe
if not os.path.isfile( './dumps/index.json' ):
	tables.generate_index( save_to='./dumps/index.json' )

# Genera un snapshot incial de las tablas de la base de datos y lo guarda en un archivo JSON si no existe
if not os.path.isfile( './dumps/snapshot.json' ):
	tables.generate_snapshot( save_to='./dumps/snapshot.json' )
```

### 2. Importar Datos desde CSV

Para importar datos desde un archivo CSV se debe tener en cuenta que la primera fila contiene los nombres de las
columnas de la tabla en la que se van a guardar.

En el caso de importar a la tabla `CULT_BIENES`se debe tener en cuenta que la columna `CD_CODIGO` se genera en tiempo de
ejecucion, por lo que se debe seguir un formato específico, el cual es separar por guiones los ids de las regiones a las
que pertenece.
Esto se debe a como se usan estos ids para generar el `CD_CODIGO` de la entidad en la base de datos.

Ejemplo de archivo CSV:

```csv
cd_codigo;tl_nombre;tl_dircalle;nm_dirnum
001-002-003-004;Casa de la Cultura;Av. 9 de Octubre;505
001-002-003-004;Calle 1;Av. 9 de Octubre;508
```

```python
from lib.inphis.factory.cult_bienes import CultBienesFactory

nuevos_bienes = CultBienesFactory.import_from_csv(
	csv_path="C:/MiRuta/A/bienes.csv"
)

for bien in nuevos_bienes:
	print( bien.cd_codigo, "-", bien.tl_nombre )
```

### 3. Añadir un Registro Manualmente

Para agregar un registro manualmente se puede usar la factoría correspondiente, en este caso `CultBienesFactory` la cual
contiene una función llamada `create_bien` que permite crear un nuevo bien recibiendo el nombre y una lista con
los ids de las regiones a las que pertenece como parametros, esta función devuelve un objeto de tipo `CultBienesModel`.

Este modelo tiene las columnas de la tabla como campos modificables, permite alterar sus valores de una
forma sencilla, cuando se desee guardar los cambios se debe llamar al método `save`.

Ejemplo de creación de un nuevo bien:

```python
from lib.inphis.factory.cult_bienes import CultBienesFactory

mi_nuevo_bien = CultBienesFactory.create_bien(
	'Mi nuevo bien',
	[  # Los valores de cult_var_municipios_cd_values se pueden ver en el snapshot en la tabla CULT_VAR_MUNICIPIOS
		'001',
		'002',
	]
)

# Cambio algunos valores del modelo
mi_nuevo_bien.tl_dircalle = 'Calle de mi nuevo bien'
mi_nuevo_bien.tl_dirnum = '1'

# Guardo el modelo en la base de datos
mi_nuevo_bien.save( )
```

> No se recomienda usar directamente el modelo para crear un nuevo bien porque esta tabla tiene relaciones con otras
> tablas, la factoría se encarga de crear el bien y de generar las relaciones necesarias.

### 4. Consultar Registros

Para obtener registros de la base de datos existen varias formas, la primera y recomenda es usar los modelos de las
tablas, estos convierten automaticamente los datos a objetos de modelo, lo cual permite hacer un CRUD de forma directa.

La función `read` deberia de devolver un único objeto, sin embargo, como en la base de datos no se valida que
`CD_CODIGO` sea único, esto puede dar el caso de que varios registros tengan el mismo `CD_CODIGO`, por lo que la función
`read` devolvera una lista con los objetos que tengan el `CD_CODIGO`, por lo que devuleve una lista de objetos. Para
usar el primero que encuentre simplemente se accede a su posición de la lista.

También se permite usar la clase `Table` para hacer consultas SQL directas, esto es ciertamente inseguro porque los
datos no se convierten a objetos, sino que se devuelven crudos.

Ejemplo de consulta de registros:

```python
from lib.inphis.models.cult_bienes import CultBienesModel
from lib.orm.tables.table import SELECT_ALL, Table

# Consulta con Modelo
bienes = CultBienesModel.read( 'CM/001/001' )  # ID único de un bien
print( bienes )
print( bienes[0] )

# Consulta con Table
Table( 'CULT_BIENES' )\
    .select( SELECT_ALL )\
    .where( CD_CODIGO=(None, '=', 'CM/001/001') )\
    .execute( )
```

### 5. Actualizar un Registro

Al igual que en la creación de un nuevo bien, se puede usar el modelo para actualizar los valores de un registro y luego
llamar el método `save` para guardar los cambios.
La función se encarga automaticamente de actualizar o crear el registro en caso de que no exista.

```python
from lib.inphis.models.cult_bienes import CultBienesModel
from lib.orm.tables.table import Table

# Consulta con Modelo
bien = CultBienesModel.read( 'CM/001/001' )[0]

bien.tl_nombre = 'Mi nuevo nombre'
bien.tl_dircalle = 'Calle de mi nuevo bien'

bien.save( )

# Consulta con Table
Table( 'CULT_BIENES' )\
    .update( TL_NOMBRE='Mi nuevo nombre', TL_DIRCALLE='Calle de mi nuevo bien' )\
    .where( CD_CODIGO=(None, '=', 'CM/001/001') )\
    .execute( )
```

### 6. Eliminar un Registro

```python
from lib.inphis.models.cult_bienes import CultBienesModel
from lib.orm.tables.table import Table

# Consulta con Modelo
bien = CultBienesModel.read( 'CM/001/001' )[0]
bien.delete( )

# Consulta con Table
Table( 'CULT_BIENES' )\
    .delete( )\
    .where( CD_CODIGO=(None, '=', 'CM/001/001') )\
    .execute( )
```

### 7. Snapshot de la Tabla

Se puede generar un snapshot de la tabla en formato JSON para respaldo o análisis.
Es simplemente un `dump` de todos los datos guardados en las tablas.

```python
from lib.orm.tables.table import Table

Table( "CULT_BIENES" ).generate_snapshot( save_to="respaldo_cult_bienes.json" )
Table( "CULT_BIENES_PICKLIST" ).generate_snapshot( save_to="respaldo_picklist.json" )
```

Tambien se puede generar un snapshot de toda la base de datos usando el indice de la misma.

```python
from lib.odbc.checkers import odbc_checkers
from lib.odbc.connection import PyODBCConnection
from lib.orm.tables.table_index import IGNORE_TABLES, TableIndex

DB_PATH = "C:/MiRuta/A/INPHIS.mdb"

# Comprueba si la base de datos de Microsoft Access es accesible y si están los drivers necesarios
odbc_checkers( DB_PATH )

# Conecta a la base de datos de Microsoft Access y obtiene los nombres de las tablas
odbc_connection = PyODBCConnection( DB_PATH )
microsoft_access_tables = [
	table_info.table_name
	for table_info in odbc_connection.cursor.tables( tableType='TABLE' )
	if table_info.table_name not in IGNORE_TABLES
]

# Crea un indice de las tablas de la base de datos
tables = TableIndex( microsoft_access_tables )

tables.generate_snapshot( save_to="C:/MiRuta/A/respaldo_inphis.json" )
```

---

## Guía Técnica para Desarrolladores

### 1. Arquitectura General

#### lib/orm/

Toda la implementacion del ORM como sistema de creacion de queries (`Query Builder`), las clases de la tabla e índice,
los tipos para las conversiones y utilidades del orm.

- `Table`: Clase principal para manejo de tablas
- `TableIndex`: Clase para manejo de multiples tablas
- `Query`: Clase para manejo de queries, se usa como alternativa a `SQL`
- `tipos`: Usados para conversiones en las queries (`type safety`)

#### lib/odbc/

- `PyODBCConnection`: Singleton, maneja conexión
- `check_microsoft_access_drivers`, `check_microsoft_access_mdb_file`

#### lib/interfaces/

- `IModels`, `IFactory`: interfaces para consistencia entre modelos y factorías

#### lib/inphis/

Contiene tanto los modelos como las factorías de las tablas de la base de datos.

Los modelos se usan para manejar los datos de las tablas de la base de datos, mientras que las factorías se usan para
gestionar como interactuar con los modelos.

En algunos casos las tablas están relacionadas, por lo que las factorías se
encargan de gestionar estas relaciones y abstraer al usuario de la complejidad de las relaciones.

- `models/`: Clases de modelos
- `factory/`: Clases de factorías

---

## Guia de uso de ChatGPT

Para poder usar el chat de INPHIS, es necesaria una cuenta de pago de ChatGPT. 
El chat es accesible públicamente a traves de este [enlace.](https://chatgpt.com/g/g-67cd7697ae388191a462f0011d23d7e4-inphis-tfg)

Una vez en el chat simplemente pidele datos sobre un bien patrimonial en concreto o por regiones.
El chat interara devolver siempre un .csv con todos los datos encontrados sobre los datos solicitados para que puedan ser importados a traves del ORM.

### Replicar modelo

Para poder replicar el modelo en caso de no tener ChatGPT premium o querer usar cualquier otro motor de Inteligencia Artificial,
todos los datos usados para entrenar el modelo están disponibles en la carpeta `chatgpt`.

En esta carpeta hay un `digest.txt`, `propmt.txt` y un `snapshot.json`. El `digest.txt` y `snapshot.json` continenen
datos para que el modelo pueda entender como funciona la estructura de la base de datos. Mientras que el `prompt.txt` contiene

Para poder replicar el modelo, simplemente pasale el `prompt.txt` y los dos ficheros `digest.txt` y `snapshot.json` a la IA
y sera capaz de entender como funciona la base de datos y como interactuar con ella.

> Nota: El modelo tiene que ser capaz de acceder a internet para poder buscar los datos de los bienes patrimoniales.