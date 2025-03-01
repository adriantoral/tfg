from typing import Any, Tuple

from lib.orm.queries.order_by_conditions import OrderByConditions
from lib.orm.queries.where_conditions import QueryWhereConditions
from lib.orm.utils.build_query import build_query
from lib.orm.utils.convert_to_type import convert_to_type


class Query:
	"""
	A class to represent an MS Access query.

	:param table: The name of the table to query.
	:type table: str

	Attributes
	----------
	_table : str
		The name of the table to query.
	_select : str or None
		The SELECT part of the query.
	_insert : str or None
		The INSERT part of the query.
	_insert_keys : str or None
		The keys for the INSERT part of the query.
	_update : str or None
		The UPDATE part of the query.
	_delete : bool or None
		The DELETE part of the query.
	_where : str or None
		The WHERE part of the query.
	_order_by : str or None
		The ORDER BY part of the query.
	"""

	_select: str | None
	_insert: str | None
	_insert_keys: str | None
	_update: str | None
	_delete: bool | None
	_where: str | None
	_order_by: str | None

	def __init__ ( self, table: str = '' ):
		"""
		Initialize the Query object.

		:param table: The name of the table to query.
		:type table: str
		"""

		self._table = table
		self.reset_query( )

	def __repr__ ( self ):
		"""
		Returns the string representation of the query.

		:return: The SQL query as a string.
		:rtype: str
		"""

		return self.build( )

	def reset_query ( self ):
		"""
		Resets the query object.

		:return: The current query object.
		:rtype: Query
		"""

		self._select = None
		self._insert = None
		self._insert_keys = None
		self._update = None
		self._delete = None
		self._where = None
		self._order_by = None

		return self

	def select ( self, *args: str ):
		"""
		Sets the SELECT part of the query.

		:param args: The columns to select.
		:type args: str
		:return: The current query object.
		:rtype: Query
		"""

		self._select = build_query( list( args ), ',' )
		return self

	def insert ( self, **kwargs: Any ):
		"""
		Sets the INSERT part of the query.

		:param kwargs: The columns and values to insert.
		:type kwargs: Any
		:return: The current query object.
		:rtype: Query
		"""

		self._insert = build_query(
			[f'{convert_to_type( value )}' for value in kwargs.values( )], ','
		)
		self._insert_keys = build_query( [key for key in kwargs.keys( )], ',' )
		return self

	def update ( self, **kwargs: Any ):
		"""
		Sets the UPDATE part of the query.

		:param kwargs: The columns and values to update.
		:type kwargs: Any
		:return: The current query object.
		:rtype: Query
		"""

		self._update = build_query(
			[
				f'{key}={convert_to_type( value )}'
				for key, value in kwargs.items( )
			], ','
		)
		return self

	def delete ( self ):
		"""
		Sets the DELETE part of the query.

		:return: The current query object.
		:rtype: Query
		"""

		self._delete = True
		return self

	def from_table ( self, table: str ):
		"""
		Sets the table for the query.

		:param table: The name of the table.
		:type table: str
		:return: The current query object.
		:rtype: Query
		"""

		return self._set_table( table )

	def into_table ( self, table: str ):
		"""
		Sets the table for the query.

		:param table: The name of the table.
		:type table: str
		:return: The current query object.
		:rtype: Query
		"""

		return self._set_table( table )

	def _set_table ( self, table: str ):
		"""
		Sets the table for the query.

		:param table: The name of the table.
		:type table: str
		:return: The current query object.
		:rtype: Query
		"""

		self._table = table
		return self

	def where (
			self,
			**kwargs: Tuple[
				QueryWhereConditions.CRITERIA_JOIN_CONDITIONS, QueryWhereConditions.CRITERIA_CONDITIONS, Any
			]
	):
		"""
		Sets the WHERE part of the query.

		:param kwargs: The conditions for the WHERE clause.
		:type kwargs: Tuple[QueryWhereConditions.CRITERIA_JOIN_CONDITIONS, QueryWhereConditions.CRITERIA_CONDITIONS, Any]
		:return: The current query object.
		:rtype: Query
		"""

		self._where = build_query(
			[
				f'{join_op} {key} {operator} {convert_to_type( value )}'
				if index else
				f'{key} {operator} {convert_to_type( value )}'
				for index, (key, (join_op, operator, value)) in enumerate( kwargs.items( ) )
			]
		)
		return self

	def order_by ( self, *args: str, **kwargs: OrderByConditions.CRITERIA_ORDER ):
		"""
		Sets the ORDER BY part of the query.

		:param args: The columns to order by.
		:type args: str
		:param kwargs: The columns and their order (ASC or DESC).
		:type kwargs: OrderByConditions.CRITERIA_ORDER
		:return: The current query object.
		:rtype: Query
		"""

		basic_orderby = build_query( list( args ), ',' )
		advanced_orderby = build_query(
			[
				f"{key} {crit if (crit := criteria.upper( )) in OrderByConditions.CRITERIA_ORDER_VALUES else 'DESC'}"
				for key, criteria in kwargs.items( )
			], ','
		) if kwargs else None

		self._order_by = build_query( [basic_orderby, advanced_orderby], ',' )
		return self

	def build ( self ):
		"""
		Builds the SQL query.

		:return: The SQL query as a string.
		:rtype: str
		:raises ValueError: If no query type is selected or multiple query types are selected.
		"""

		self.__validate_build( )

		if self._insert:
			q = self.__build_insert( )
		elif self._select:
			q = self.__build_select( )
		elif self._update:
			q = self.__build_update( )
		elif self._delete:
			q = self.__build_delete( )
		else:
			raise ValueError( 'No query type selected' )

		return build_query( q )

	def __validate_build ( self ):
		"""
		Validates the query before building it.

		:raises ValueError: If no query type is selected or multiple query types are selected.
		:raises ValueError: If no table is specified.
		"""

		queries = [self._select, self._insert, self._update, self._delete]

		if not any( queries ):
			raise ValueError( 'No query type selected' )

		if sum( bool( q ) for q in queries ) > 1:
			raise ValueError( 'Only one query type can be selected' )

		if not self._table:
			raise ValueError( 'No table specified' )

	def __build_select ( self ):
		"""
		Builds the SELECT part of the query.

		:return: The SELECT query as a list of strings.
		:rtype: list
		"""

		return [
			f'SELECT {self._select}' if self._select else None,
			f'FROM {self._table}' if self._table else None,
			f'WHERE {self._where}' if self._where else None,
			f'ORDER BY {self._order_by}' if self._order_by else None,
		]

	def __build_insert ( self ):
		"""
		Builds the INSERT part of the query.

		:return: The INSERT query as a list of strings.
		:rtype: list
		"""

		return [
			f'INSERT INTO {self._table} ({self._insert_keys})' if self._table and self._insert_keys else None,
			f'VALUES ({self._insert})' if self._insert else None,
		]

	def __build_update ( self ):
		"""
		Builds the UPDATE part of the query.

		:return: The UPDATE query as a list of strings.
		:rtype: list
		"""

		return [
			f'UPDATE {self._table}' if self._table else None,
			f'SET {self._update}' if self._update else None,
			f'WHERE {self._where}' if self._where else None,
		]

	def __build_delete ( self ):
		"""
		Builds the DELETE part of the query.

		:return: The DELETE query as a list of strings.
		:rtype: list
		"""

		return [
			f'DELETE FROM {self._table}' if self._table else None,
			f'WHERE {self._where}' if self._where else None,
		]
