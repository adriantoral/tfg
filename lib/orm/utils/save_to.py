from json import dump


def save_to_file ( serializable: object, path: str ) -> None:
	"""
	Save a serializable object to a file.

	:param serializable: The object to be serialized and saved.
	:type serializable: object
	:param path: The file path where the object will be saved.
	:type path: str
	:return: None
	:rtype: None
	"""

	with open( path, 'w', encoding='utf-8' ) as file:
		dump( serializable, file, indent=4, ensure_ascii=False )
