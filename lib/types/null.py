from lib.interfaces.types import ITypes


class TNull( ITypes ):
	"""
	Represent a null type.

	:param value: The null value to be represented, defaults to None.
	:type value: None, optional
	"""

	def __init__ ( self, value=None ):
		"""
		Initialize the TNull with a value.

		:param value: The null value to be represented, defaults to None.
		:type value: None, optional
		"""

		self.value = value

	def __repr__ ( self ):
		"""
		Return a string representation of the TNull.

		:return: String representation of the null value.
		:rtype: str
		"""

		return 'NULL'
