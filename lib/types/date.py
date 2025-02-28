from datetime import datetime

from lib.interfaces.types import ITypes


class TDate( ITypes ):
	"""
	A class to represent a date value.

	:param value: The date value, either as a string or a datetime object.
	:type value: str | datetime
	"""

	def __init__ ( self, value: str | datetime ):
		"""
		Initialize the TDate object.

		:param value: The date value, either as a string or a datetime object.
		:type value: str | datetime
		"""

		self._value = f"#{value if isinstance( value, str ) else value.now( ).strftime( '%Y-%m-%d %H:%M:%S' )}#"

	def __repr__ ( self ):
		"""
		Return a string representation of the TDate object.

		:return: String representation of the TDate object.
		:rtype: str
		"""

		return self._value
