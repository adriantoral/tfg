import os

from lib.inphis.models.cult_bienes import CultBienesModel
from lib.odbc.checkers import odbc_checkers
from lib.odbc.connection import PyODBCConnection
from lib.tables.table import SELECT_ALL
from lib.tables.table_index import TableIndex, IGNORE_TABLES


# Ruta a la base de datos de Microsoft Access
DB_PATH = "H:/tfg-adrian-toral-javier-algarra/inphisenblanco_2024-10-31_1320/INPHISenBlanco/INPHIS.mdb"


def main():
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

	# TODO: Hacer aqui todas las operaciones sobre los modelos para que el snapshot refleje los cambios
	# mi_nuevo_bien = CultBienesFactory.create_bien(
	# 	'Mi nuevo bien',
	# 	[  # Los valores de cult_var_municipios_cd_values se pueden ver en el snapshot en la tabla CULT_VAR_MUNICIPIOS
	# 		'001',
	# 		'002',
	# 	]
	# )
	#
	# # Cambio algunos valores del modelo
	# mi_nuevo_bien.tl_dircalle = 'Calle de mi nuevo bien'
	# mi_nuevo_bien.tl_dirnum = '1'
	#
	# # Guardo el modelo en la base de datos
	# mi_nuevo_bien.save()

	# [
	# 	print( x )
	# 	for x in CultBienesFactory.import_from_csv(
	# 	'H:/tfg-adrian-toral-javier-algarra/integracion-python/prueba.csv',
	# 	save_on_import=True
	# )]

	# Genera un snapshot después de las operaciones sobre los modelos y lo guarda en un archivo JSON
	tables.generate_snapshot( save_to='./dumps/snapshot_diff.json' )
	# tables.generate_snapshot( save_to='./dumps/snapshot_pre.json' )
	#
	# tables.import_from_snapshot(
	# 	'./dumps/snapshot_diff.json',
	# 	['CULT_BIENES', 'CULT_BIENES_BIBLIO', 'CULT_BIENES_CATALOGO', 'CULT_BIENES_PICKLIST']
	# )
	#
	# tables.generate_snapshot( save_to='./dumps/snapshot_post.json' )

	[print( row ) for row in tables.use( 'CULT_BIENES' ).select( SELECT_ALL )]


if __name__ == '__main__': main()
