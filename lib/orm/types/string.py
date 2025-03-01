from lib.interfaces.types import ITypes


class TString( ITypes ):
	"""
	Represent a string type.

	:param value: The string value to be represented.
	:type value: str
	"""

	def __init__ ( self, value: str ):
		"""
		Initialize the TString with a value.

		:param value: The string value to be represented.
		:type value: str
		"""

		self._value = f"'{value}'"

	def __repr__ ( self ):
		"""
		Return a string representation of the TString.

		:return: String representation of the string value.
		:rtype: str
		"""

		return self._value
