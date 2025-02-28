from abc import abstractmethod


class ITypes:
	"""
	Interface for types.
	"""

	@abstractmethod
	def __repr__ ( self ):
		"""
		Abstract method to return the string representation of the object.
		"""

		pass

	def __str__ ( self ):
		"""
		Returns the string representation of the object.
		"""

		return self.__repr__( )
