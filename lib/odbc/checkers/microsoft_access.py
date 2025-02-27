import os.path

import pyodbc


def check_microsoft_access_drivers ( ):
	"""
	Check if Microsoft Access drivers are available.

	:raises RuntimeError: If Microsoft Access drivers are not found.
	"""

	if not any( driver.startswith( 'Microsoft Access Driver' ) for driver in pyodbc.drivers( ) ):
		raise RuntimeError( 'Microsoft Access drivers not found' )


def check_microsoft_access_mdb_file ( file_path: str ):
	"""
	Check if the given file is a valid Microsoft Access database file.

	:param file_path: Path to the Microsoft Access database file.
	:type file_path: str
	:raises RuntimeError: If the file is not a Microsoft Access database or if the file is not found.
	:return: True if the file is valid.
	:rtype: bool
	"""

	if not file_path.endswith( '.mdb' ):
		raise RuntimeError( 'File is not a Microsoft Access database' )

	if not os.path.exists( file_path ):
		raise RuntimeError( 'File not found' )

	return True
