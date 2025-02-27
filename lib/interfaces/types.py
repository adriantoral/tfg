from abc import abstractmethod


class ITypes:
	"""
	Interfaz para tipos.
	"""

	@abstractmethod
	def __repr__ ( self ):
		"""
		Método abstracto para representar el tipo como una cadena.
		"""

		pass

	def __str__ ( self ):
		"""
		Representa el tipo como una cadena.
		"""

		return self.__repr__( )
