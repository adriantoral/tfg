from lib.odbc.connection import PYODBC_IGNORE_CONNECTION, PyODBCConnection
from lib.types.null import TNull
from lib.utils.build_query import build_query
from lib.utils.save_to import save_to_file

SELECT_ALL = '*'
NO_COLUMNS_SELECTED = 'No columns selected'


class Table:
	_cursor = None

	@staticmethod
	def initialize_cursor ( cursor ) -> None:
		"""
		Initialize the cursor for the Table class if it is not already initialized.

		:param cursor: The cursor to be initialized.
		"""

		if not Table._cursor: Table._cursor = cursor

	def __init__ ( self, table_name: str ):
		"""
		Initialize a Table instance.

		:param table_name: The name of the table.
		"""

		Table.initialize_cursor( PyODBCConnection( PYODBC_IGNORE_CONNECTION ).cursor )

		self._table_name = table_name
		self._columns = None
		self._columns_bytes_size = None
		self._columns_types = None

		self.get_info( )

	def __select (
			self,
			*columns: str,
			where: str = None,
			order_by: str = None
	) -> list[tuple]:
		"""
		Private method to execute a SELECT query on the table.

		:param columns: Columns to select.
		:param where: Optional WHERE clause.
		:param order_by: Optional ORDER BY clause.
		:return: List of tuples containing the query results.
		:raises ValueError: If no columns are selected.
		"""

		if not len( columns ): raise ValueError( NO_COLUMNS_SELECTED )

		query = [
			f'''SELECT {build_query( list( columns ), ',' )}''',
			f'''FROM {self._table_name}''',
			f'''WHERE {where}''' if where else False,
			f'''ORDER BY {order_by}''' if order_by else False
		]

		Table._cursor.execute( build_query( query ) )
		return Table._cursor.fetchall( )

	def select (
			self,
			*columns: str,
			where: str = None,
			order_by: str = None
	) -> list[tuple]:
		"""
		Execute a SELECT query on the table.

		:param columns: Columns to select.
		:param where: Optional WHERE clause.
		:param order_by: Optional ORDER BY clause.
		:return: List of tuples containing the query results.
		:raises ValueError: If any of the selected columns do not exist in the table.
		"""

		missing_columns = [column for column in columns if column not in self._columns and column != SELECT_ALL]
		if missing_columns: raise ValueError( f'Columns {missing_columns} do not exist in {self._table_name}' )

		return self.__select( *columns, where=where, order_by=order_by )

	def __insert (
			self,
			columns: list[str],
			values: list
	) -> None:
		"""
		Private method to execute an INSERT query on the table.

		:param columns: Columns to insert values into.
		:param values: Values to insert.
		:raises ValueError: If no columns or values are provided.
		"""

		if not len( columns ) or not len( values ): raise ValueError( NO_COLUMNS_SELECTED )

		query = [
			'INSERT',
			f'''INTO {self._table_name}''',
			f'''({build_query( columns, ',' )})''',
			'VALUES',
			f'''({build_query( [repr( value if value else TNull( ) ) for value in values], ',' )})'''
		]

		Table._cursor.execute( build_query( query ) )
		Table._cursor.commit( )

	def insert (
			self,
			**columns_values
	) -> None:
		"""
		Execute an INSERT query on the table.

		:param columns_values: Dictionary of columns and their corresponding values to insert.
		:raises ValueError: If no columns are provided or if any of the columns do not exist in the table.
		"""

		if not len( columns_values ): raise ValueError( NO_COLUMNS_SELECTED )
		columns, values = zip( *columns_values.items( ) )

		missing_columns = [column for column in columns if column not in self._columns]
		if missing_columns: raise ValueError( f'Columns {missing_columns} do not exist in {self._table_name}' )

		return self.__insert( columns, values )

	def __update (
			self,
			columns: list[str],
			values: list,
			where: str,
	) -> int:
		"""
		Private method to execute an UPDATE query on the table.

		:param columns: Columns to update.
		:param values: Values to update.
		:param where: WHERE clause is to specify which rows to update.
		:return: Number of rows affected.
		:raises ValueError: If no columns or values are provided.
		"""

		if not len( columns ) or not len( values ): raise ValueError( NO_COLUMNS_SELECTED )

		query = [
			f'''UPDATE {self._table_name}''',
			f'''SET {build_query( [f'{column}={repr( value if value else TNull( ) )}' for column, value in zip( columns, values )], ',' )}''',
			f'''WHERE {where}'''
		]

		Table._cursor.execute( build_query( query ) )
		Table._cursor.commit( )

		return Table._cursor.rowcount

	def update (
			self,
			where: str,
			**columns_values,
	) -> int:
		"""
		Execute an UPDATE query on the table.

		:param where: WHERE clause is to specify which rows to update.
		:param columns_values: Dictionary of columns and their corresponding values to update.
		:return: Number of rows affected.
		:raises ValueError: If no columns are provided or if any of the columns do not exist in the table.
		"""

		if not len( columns_values ): raise ValueError( NO_COLUMNS_SELECTED )
		columns, values = zip( *columns_values.items( ) )

		missing_columns = [column for column in columns if column not in self._columns]
		if missing_columns: raise ValueError( f'Columns {missing_columns} do not exist in {self._table_name}' )

		return self.__update( columns, values, where )

	def __delete (
			self,
			where: str,
	) -> int:
		"""
		Private method to execute a DELETE query on the table.

		:param where: WHERE clause to specify which rows to delete.
		:return: Number of rows affected.
		"""

		query = [
			'DELETE',
			f'''FROM {self._table_name}''',
			f'''WHERE {where}'''
		]

		Table._cursor.execute( build_query( query ) )
		Table._cursor.commit( )

		return Table._cursor.rowcount

	def delete (
			self,
			where: str
	) -> int:
		"""
		Execute a DELETE query on the table.

		:param where: WHERE clause to specify which rows to delete.
		:return: Number of rows affected.
		"""

		return self.__delete( where )

	def get_info ( self ) -> tuple[list[str], list[int], list[type]]:
		"""
		Retrieve information about the table's columns, their byte sizes, and their types.

		:return: Tuple containing lists of column names, column byte sizes, and column types.
		"""

		if not self._columns or not self._columns_bytes_size or not self._columns_types:
			self.__select( SELECT_ALL )
			self._columns = [column[0] for column in Table._cursor.description]
			self._columns_bytes_size = [column[3] for column in Table._cursor.description]
			self._columns_types = [column[1] for column in Table._cursor.description]

		return self._columns, self._columns_bytes_size, self._columns_types

	def generate_snapshot ( self, save_to: str = None ) -> object:
		"""
		Generate a snapshot of the table's data and optionally save it to a file.

		:param save_to: Optional file path to save the snapshot.
		:return: Snapshot of the table's data.
		"""

		try:
			snapshot = [list( row ) for row in self.__select( SELECT_ALL, order_by='OBJECTID ASC' )]
		except ValueError:
			snapshot = [list( row ) for row in self.__select( SELECT_ALL )]

		if save_to: save_to_file( snapshot, save_to )
		return snapshot
