from lib.orm.utils.convert_to_type import convert_to_type


def build_query ( query: list[str], delimeter: str = ' ' ):
	"""
	Build a query string by joining elements of a list with a delimiter.

	:param query: List of strings to be joined.
	:type query: list[str]
	:param delimeter: Delimiter to join the strings, defaults to a space.
	:type delimeter: str, optional
	:return: Joined query string.
	:rtype: str
	"""

	return delimeter.join( filter( None, query ) )


def build_query_colums ( columns_value: dict[str, str], ignore: list[str] ):
	"""
	Build a dictionary of column names and their converted values, ignoring specified columns.

	:param columns_value: Dictionary of column names and their values.
	:type columns_value: dict[str, str]
	:param ignore: List of column names to ignore.
	:type ignore: list[str]
	:return: Dictionary with column names in uppercase and their converted values.
	:rtype: dict
	"""

	return {
		column.upper( ): convert_to_type( value )
		for column, value in columns_value.items( )
		if column not in ignore and value
	}
