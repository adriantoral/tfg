from lib.odbc.connection import PyODBCConnection, PYODBC_IGNORE_CONNECTION
from lib.types.t_null import TNull
from lib.utils.build_query import build_query
from lib.utils.save_to import save_to_file

SELECT_ALL = '*'


class Table:
    _cursor = None

    @staticmethod
    def initialize_cursor(cursor) -> None:
        if not Table._cursor:
            Table._cursor = cursor

    def __init__(self, table_name: str):
        Table.initialize_cursor(PyODBCConnection(PYODBC_IGNORE_CONNECTION).cursor)

        self._table_name = table_name
        self._columns = None
        self._columns_bytes_size = None
        self._columns_types = None

        self.get_info()

    def __select(
            self,
            *columns,
            where: str = None,
            order_by: str = None
    ) -> list[tuple]:
        if not len(columns): raise Exception('No columns selected')

        query = [
            f'''SELECT {','.join(columns)}''',
            f'''FROM {self._table_name}''',
            f'''WHERE {where}''' if where else False,
            f'''ORDER BY {order_by}''' if order_by else False
        ]

        Table._cursor.execute(build_query(query))
        return Table._cursor.fetchall()

    def select(
            self,
            *columns,
            where: str = None,
            order_by: str = None
    ) -> list[tuple]:
        missing_columns = [column for column in columns if column not in self._columns and column != SELECT_ALL]
        if missing_columns: raise Exception(f'Columns {missing_columns} do not exist in {self._table_name}')

        return self.__select(*columns, where=where, order_by=order_by)

    def __insert(
            self,
            columns,
            values
    ) -> None:
        if not len(columns) or not len(values): raise Exception('No columns selected')

        query = [
            f'''INSERT''',
            f'''INTO {self._table_name}''',
            f'''({",".join(columns)})''',
            f'''VALUES''',
            f'''({','.join([repr(value if value else TNull()) for value in values])})'''
        ]

        Table._cursor.execute(build_query(query))
        Table._cursor.commit()

    def insert(
            self,
            **columns_values
    ) -> None:
        if not len(columns_values): raise Exception('No columns selected')
        columns, values = zip(*columns_values.items())

        missing_columns = [column for column in columns if column not in self._columns]
        if missing_columns: raise Exception(f'Columns {missing_columns} do not exist in {self._table_name}')

        return self.__insert(columns, values)

    def __update(
            self,
            columns,
            values,
            where: str,
    ) -> int:
        if not len(columns) or not len(values): raise Exception('No columns selected')

        query = [
            f'''UPDATE {self._table_name}''',
            f'''SET {','.join([f'{column}={repr(value if value else TNull())}' for column, value in zip(columns, values)])}''',
            f'''WHERE {where}'''
        ]

        Table._cursor.execute(build_query(query))
        Table._cursor.commit()

        return Table._cursor.rowcount

    def update(
            self,
            where: str,
            **columns_values,
    ) -> int:
        if not len(columns_values): raise Exception('No columns selected')
        columns, values = zip(*columns_values.items())

        missing_columns = [column for column in columns if column not in self._columns]
        if missing_columns: raise Exception(f'Columns {missing_columns} do not exist in {self._table_name}')

        return self.__update(columns, values, where)

    def __delete(
            self,
            where: str,
    ) -> int:
        query = [
            f'''DELETE''',
            f'''FROM {self._table_name}''',
            f'''WHERE {where}'''
        ]

        Table._cursor.execute(build_query(query))
        Table._cursor.commit()

        return Table._cursor.rowcount

    def delete(
            self,
            where: str
    ) -> int:
        return self.__delete(where)

    def get_info(self) -> tuple[list[str], list[int], list[type]]:
        if not self._columns or not self._columns_bytes_size or not self._columns_types:
            self.__select(SELECT_ALL)
            self._columns = [column[0] for column in Table._cursor.description]
            self._columns_bytes_size = [column[3] for column in Table._cursor.description]
            self._columns_types = [column[1] for column in Table._cursor.description]

        return self._columns, self._columns_bytes_size, self._columns_types

    def generate_snapshot(self, save_to: str = None) -> object:
        try:
            snapshot = [list(row) for row in self.__select(SELECT_ALL, order_by='OBJECTID ASC')]
        except:
            snapshot = [list(row) for row in self.__select(SELECT_ALL)]

        if save_to: save_to_file(snapshot, save_to)
        return snapshot
