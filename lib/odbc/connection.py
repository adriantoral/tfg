import pyodbc

PYODBC_IGNORE_CONNECTION = 'IGNORE'


class PyODBCConnection:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PyODBCConnection, cls).__new__(cls)

        return cls._instance

    def __init__(self, db_path: str):
        if PyODBCConnection._initialized: return

        self.connection = pyodbc.connect(f'Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};')
        self.cursor = self.connection.cursor()

        PyODBCConnection._initialized = True
