from abc import abstractmethod
from typing import Type

from lib.tables.table import Table
from lib.utils.build_query import build_query_colums


class IModels:
	"""
	Interfaz para modelos.
	"""

	@staticmethod
	@abstractmethod
	def create ( *args, **kwargs ):
		"""
		Método abstracto para crear una nueva instancia del modelo.
		"""

		pass

	@staticmethod
	@abstractmethod
	def read ( *args, **kwargs ):
		"""
		Método abstracto para leer instancias existentes del modelo.
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
		Método para guardar el modelo actual.

		:param where: Cláusula WHERE para la actualización.
		:param read_value: Valor para leer el modelo después de la inserción.
		:param model: La clase del modelo.
		:param table: La tabla de la base de datos.
		:param ignore: Lista de columnas para ignorar.
		:param is_update: Si es una actualización en lugar de una inserción.
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
		Método abstracto para guardar el modelo actual.
		"""

		pass

	@abstractmethod
	def delete ( self ):
		"""
		Método abstracto para eliminar la instancia actual del modelo.
		"""

		pass
