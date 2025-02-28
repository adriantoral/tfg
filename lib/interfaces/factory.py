from abc import abstractmethod


class IFactory:
	"""
	Interface for factory operations.
	"""

	@staticmethod
	@abstractmethod
	def import_from_csv (
			csv_path: str,
			cult_var_municipios_separator: str = '-',
			bien_separator: str = ';',
			save_on_import: bool = True
	):
		"""
		Abstract method to import data from a CSV file.

		:param csv_path: Path to the CSV file.
		:type csv_path: str
		:param cult_var_municipios_separator: Separator for `cult_var_municipios` field, defaults to '-'.
		:type cult_var_municipios_separator: str, optional
		:param bien_separator: Separator for `bien` field, defaults to ';'.
		:type bien_separator: str, optional
		:param save_on_import: Whether to save the data on import, defaults to True.
		:type save_on_import: bool, optional
		"""

		pass
