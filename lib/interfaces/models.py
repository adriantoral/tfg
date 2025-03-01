from abc import abstractmethod
from typing import Any, Type

from lib.orm.tables.table import Table
from lib.orm.utils.build_query import build_query_colums


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
			table_name: str,
			model_cls: Type['IModels'],
			is_update: bool,
			update_key_value: tuple[str, Any],
			read_value: str,
			ignore: list[str]
	):
		"""
		Save the current model instance to the database.

		:param table_name: The name of the table where the model instance will be saved.
		:type table_name: str
		:param model_cls: The class of the model being saved.
		:type model_cls: Type['IModels']
		:param is_update: Flag indicating whether the operation is an update.
		:type is_update: bool
		:param update_key_value: A tuple containing the key and value for the update condition.
		:type update_key_value: tuple[str, Any]
		:param read_value: The value used to read the model instance after saving.
		:type read_value: str
		:param ignore: A list of fields to ignore during the save operation.
		:type ignore: list[str]
		"""

		data = build_query_colums( self.__dict__, ignore )

		if is_update:
			Table( table_name ) \
				.update( **data ) \
				.where( **{ update_key_value[0]: (None, '=', update_key_value[1]) } ) \
				.execute( )
		else:
			Table( table_name ) \
				.insert( **data ) \
				.execute( )

		self.__dict__.update( model_cls.read( read_value ).pop( ).__dict__ )

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
