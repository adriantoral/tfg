import json

from lib.orm.tables.table import Table
from lib.orm.utils.save_to import save_to_file

IGNORE_TABLES = [
	'CamposNoExportados',
	'CULT_BIENES_Shape_Index',
	'CULT_ENTORNO_Shape_Index',
	'CULT_BIENES_POLIGONO_GEOMETRY1_Index',
	'GDB_ColumnInfo',
	'GDB_GeomColumns',
	'GDB_ItemRelationships',
	'GDB_ItemRelationshipTypes',
	'GDB_Items',
	'GDB_Items_Shape_Index',
	'GDB_ItemTypes',
	'GDB_ReplicaLog',
	'GDB_SpatialRefs'
]


class TableIndex:
	"""
	Class to manage a collection of tables and perform operations on them.

	:param table_names: List of table names to manage.
	:type table_names: list[str]
	"""

	def __init__ ( self, table_names: list[str] ):
		"""
		Initialize the TableIndex with a list of table names.

		:param table_names: List of table names to manage.
		:type table_names: list[str]
		"""

		self._index = None
		self._table_names = table_names

		for table_name in table_names:
			self.create_table( table_name )

	def __str__ ( self ):
		"""
		Return a string representation of the TableIndex.

		:return: String representation of the TableIndex.
		:rtype: str
		"""

		return f'TableIndex({self._table_names})'

	def create_table ( self, table_name: str ):
		"""
		Create a Table object for the given table name.

		:param table_name: Name of the table to create.
		:type table_name: str
		:raises Exception: If the table already exists.
		"""

		if table_name in self.__dict__: raise KeyError( f'Table {table_name} already exists' )
		self.__dict__[table_name] = Table( table_name )

	def use ( self, table_name: str ) -> Table:
		"""
		Retrieve the Table object for the given table name.

		:param table_name: Name of the table to retrieve.
		:type table_name: str
		:return: Table object for the given table name.
		:rtype: Table
		:raises Exception: If the table does not exist.
		"""

		if table_name not in self.__dict__: raise KeyError( f'Table {table_name} does not exist' )
		return self.__dict__[table_name]

	def generate_index ( self, save_to: str = None ) -> dict:
		"""
		Generate an index of the table columns, their types, and byte sizes.

		:param save_to: Optional file path to save the index.
		:type save_to: str, optional
		:return: Dictionary containing the index of the table columns.
		:rtype: dict
		"""

		index = {
			table_name: {
				column_data[0]: {
					"type" : str( column_data[2] ),
					"bytes": column_data[1]
				}
				for column_data in zip( *self.use( table_name ).get_info( ) )
			}
			for table_name in self._table_names
		} if not self._index else self._index

		if not self._index:
			self._index = index

		if save_to: save_to_file( index, save_to )
		return index

	def generate_snapshot ( self, save_to: str = None ):
		"""
		Generate a snapshot of the table data and optionally save it to a file.

		:param save_to: Optional file path to save the snapshot.
		:type save_to: str, optional
		:return: Snapshot of the table data.
		:rtype: dict
		"""

		snapshot = {
			table_name: self.use( table_name ).generate_snapshot( )
			for table_name in self._table_names
		}

		if save_to: save_to_file( snapshot, save_to )
		return snapshot

	def import_from_snapshot ( self, snapshot_path: str, tables_to_import: list[str] ):
		"""
		Import table data from a snapshot file.

		:param snapshot_path: Path to the snapshot file.
		:type snapshot_path: str
		:param tables_to_import: List of table names to import.
		:type tables_to_import: list[str]
		"""

		with open( snapshot_path, 'r', encoding='utf-8' ) as snapshot_file:
			for table_name, table_snapshot in json.load( snapshot_file ).items( ):
				if table_name not in tables_to_import:
					continue

				table = self.use( table_name )
				for row in table_snapshot:
					try: table.insert(
						**{
							column: value
							for column, value in zip( table.get_info( )[0], row )
						}
					).execute( )
					except ValueError: continue
