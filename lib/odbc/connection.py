import pyodbc

PYODBC_IGNORE_CONNECTION = 'IGNORE'


class PyODBCConnection:
	"""
	Singleton class to manage a PyODBC connection to a Microsoft Access database.

	:ivar connection: The PyODBC connection object.
	:ivar cursor: The cursor object for executing SQL queries.
	"""

	_instance = None
	_initialized = False

	def __new__ ( cls, *args, **kwargs ):
		"""
		Create a new instance of the PyODBCConnection class if it does not already exist.

		:param args: Additional arguments.
		:param kwargs: Additional keyword arguments.
		:return: The singleton instance of the PyODBCConnection class.
		"""

		if not cls._instance: cls._instance = super( PyODBCConnection, cls ).__new__( cls )
		return cls._instance

	def __init__ ( self, db_path: str ):
		"""
		Initialize the PyODBC connection to the specified Microsoft Access database.

		:param db_path: Path to the Microsoft Access database file.
		:type db_path: str
		"""

		if PyODBCConnection._initialized: return

		self.connection = pyodbc.connect( f'Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};' )
		self.cursor = self.connection.cursor( )

		PyODBCConnection._initialized = True
