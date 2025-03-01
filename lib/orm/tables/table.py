from typing import Any

from lib.odbc.connection import PYODBC_IGNORE_CONNECTION, PyODBCConnection
from lib.orm.queries.query import Query
from lib.orm.utils.save_to import save_to_file

SELECT_ALL = '*'
NO_COLUMNS_SELECTED = 'No columns selected'


class Table( Query ):
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

		super( ).__init__( table_name )

		self._table_name = table_name
		self._columns = None
		self._columns_bytes_size = None
		self._columns_types = None

		self.get_info( )

	def get_info ( self ) -> tuple[list[str], list[int], list[type]]:
		"""
		Retrieve information about the table's columns, their byte sizes, and their types.

		:return: Tuple containing lists of column names, column byte sizes, and column types.
		"""

		if not self._columns or not self._columns_bytes_size or not self._columns_types:
			self.execute(
				Query( self._table ) \
					.select( SELECT_ALL ) \
					.build( ),
				True
			)

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

		snapshot = [
			list( row )
			for row in self \
				.select( SELECT_ALL ) \
				.execute( )
		]

		if save_to: save_to_file( snapshot, save_to )
		return snapshot

	def select ( self, *args: str ):
		"""
        Execute a SELECT query on the table.

        :param args: Columns to select.
        :type args: str
        :raises ValueError: If any of the selected columns do not exist in the table.
        :return: The Table instance.
        :rtype: Table
        """

		missing_columns = [column for column in args if column not in self._columns and column != SELECT_ALL]
		if missing_columns: raise ValueError( f'Columns {missing_columns} do not exist in {self._table_name}' )

		super( ).select( *args )
		return self

	def insert ( self, **kwargs: Any ):
		"""
		Execute an INSERT query on the table.

		:param kwargs: Dictionary of columns and their corresponding values to insert.
		:type kwargs: dict
		:raises ValueError: If no columns are provided or if any of the columns do not exist in the table.
		:return: The Table instance.
		:rtype: Table
		"""

		if not len( kwargs ): raise ValueError( NO_COLUMNS_SELECTED )

		columns, _ = zip( *kwargs.items( ) )
		missing_columns = [column for column in columns if column not in self._columns]
		if missing_columns: raise ValueError( f'Columns {missing_columns} do not exist in {self._table_name}' )

		super( ).insert( **kwargs )
		return self

	def update ( self, **kwargs: Any ):
		"""
		Execute an UPDATE query on the table.

		:param kwargs: Dictionary of columns and their corresponding values to update.
		:type kwargs: dict
		:raises ValueError: If no columns are provided or if any of the columns do not exist in the table.
		:return: The Table instance.
		:rtype: Table
		"""

		if not len( kwargs ): raise ValueError( NO_COLUMNS_SELECTED )

		columns, _ = zip( *kwargs.items( ) )
		missing_columns = [column for column in columns if column not in self._columns]
		if missing_columns: raise ValueError( f'Columns {missing_columns} do not exist in {self._table_name}' )

		super( ).update( **kwargs )
		return self

	def execute ( self, query: str = None, is_select: bool = False ):
		"""
		Execute a query on the table.

		:param query: The query to execute.
		:type query: str, optional
		:param is_select: Flag to indicate if the query is a SELECT query.
		:type is_select: bool, optional
		:return: The result of the query execution.
		:rtype: Any
		"""

		Table._cursor.execute( query or self.build( ) )

		if self._select or is_select:
			_return = Table._cursor.fetchall( )

		else:
			Table._cursor.commit( )
			_return = Table._cursor.rowcount

		self.reset_query( )
		return _return
