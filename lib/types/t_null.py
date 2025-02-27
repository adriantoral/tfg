from lib.interfaces.types import ITypes


class TNull( ITypes ):
	"""
	Representa un tipo nulo.

	:param value: El valor nulo a ser representado.
	:type value: None
	"""

	def __init__ ( self, value=None ):
		"""
		Inicializa el TNull con un valor.

		:param value: El valor nulo a ser representado.
		:type value: None
		"""

		self.value = value

	def __repr__ ( self ):
		"""
		Retorna una representación en cadena del TNull.

		:return: Representación en cadena del valor nulo.
		:rtype: str
		"""

		return 'NULL'
