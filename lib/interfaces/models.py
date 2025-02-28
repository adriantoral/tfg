from abc import abstractmethod
from typing import Type

from lib.tables.table import Table
from lib.utils.build_query import build_query_colums


class IModels:
	"""
	Interface for models.
	"""

	@staticmethod
	@abstractmethod
	def create ( *args, **kwargs ):
		"""
		Abstract method to create a new instance of the model.
		"""

		pass

	@staticmethod
	@abstractmethod
	def read ( *args, **kwargs ):
		"""
		Abstract method to read existing instances of the model.
		"""

		pass

	def _save (
			self,
			where,
			read_value,
			model: Type['IModels'],
			table: Table,
			ignore: list[str],
			is_update: bool = False
	):
		"""
		Method to save the current model.

		:param where: WHERE clause for the update.
		:type where: str
		:param read_value: Value to read the model after insertion.
		:type read_value: Any
		:param model: The model class.
		:type model: Type[IModels]
		:param table: The database table.
		:type table: Table
		:param ignore: List of columns to ignore.
		:type ignore: list[str]
		:param is_update: Whether it is an update instead of an insertion.
		:type is_update: bool
		"""

		data = build_query_colums( self.__dict__, ignore )

		if is_update:
			table.update( **data, where=where )
			return

		table.insert( **data )
		self.__dict__.update( model.read( read_value ).pop( ).__dict__ )

	@abstractmethod
	def save ( self ):
		"""
		Abstract method to save the current model.
		"""

		pass

	@abstractmethod
	def delete ( self ):
		"""
		Abstract method to delete the current model instance.
		"""

		pass
