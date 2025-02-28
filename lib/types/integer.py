from lib.interfaces.types import ITypes


class TInteger( ITypes ):
	"""
	Class to represent an integer type.

	:param value: The integer value to be represented.
	:type value: str
	"""

	def __init__ ( self, value: int ):
		"""
		Initialize the TInteger with a value.

		:param value: The integer value to be represented.
		:type value: int
		"""

		self.value = str( value )

	def __repr__ ( self ):
		"""
		Return a string representation of the TInteger.

		:return: String representation of the integer value.
		:rtype: str
		"""

		return self.value
