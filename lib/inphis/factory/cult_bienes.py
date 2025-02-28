import csv

from lib.inphis.models.cult_bienes import CultBienesModel
from lib.inphis.models.cult_bienes_picklist import CultBienesPicklistModel
from lib.interfaces.factory import IFactory


class CultBienesFactory( IFactory ):
	@staticmethod
	def create_bien ( tl_nombre: str, cult_var_municipios_cd_values: list[str] ) -> CultBienesModel:
		"""
		Create a new instance of CultBienesModel and CultBienesPicklistModel.

		:param tl_nombre: The name of the cult_bien.
		:type tl_nombre: str
		:param cult_var_municipios_cd_values: A list of municipality codes.
		:type cult_var_municipios_cd_values: list[str]
		:return: An instance of CultBienesModel.
		:rtype: CultBienesModel
		"""

		cult_bien = CultBienesModel.create( tl_nombre, cult_var_municipios_cd_values )
		cult_bien.save( )

		for municipio in cult_var_municipios_cd_values:
			CultBienesPicklistModel.create( cult_bien.cd_codigo, 'MUNICIPIO', municipio ).save( )

		return cult_bien

	@staticmethod
	def import_from_csv (
			csv_path: str,
			cult_var_municipios_separator: str = '-',
			bien_separator: str = ';',
			save_on_import: bool = True
	) -> list[CultBienesModel]:
		"""
		Import cult_bien data from a CSV file.

		:param csv_path: The path to the CSV file.
		:type csv_path: str
		:param cult_var_municipios_separator: The separator for municipality codes.
		:type cult_var_municipios_separator: str
		:param bien_separator: The separator for cult_bien fields.
		:type bien_separator: str
		:param save_on_import: Whether to save each imported cult_bien.
		:type save_on_import: bool
		:return: A list of instances of CultBienesModel.
		:rtype: list[CultBienesModel]
		"""

		imported = []

		with open( csv_path, 'r' ) as csv_file:
			for line in csv.DictReader( csv_file, delimiter=bien_separator ):
				model = CultBienesModel(
					**{
						key: CultBienesModel.__annotations__[key]( value )
						for key, value in line.items( )
					}
				)

				cult_var_municipios = model.cd_codigo.split( cult_var_municipios_separator )
				model.cd_codigo = CultBienesModel.generate_cd_codigo( cult_var_municipios )

				if save_on_import:
					model.save( )

					for municipio in cult_var_municipios:
						CultBienesPicklistModel.create( model.cd_codigo, 'MUNICIPIO', municipio ).save( )

				imported.append( model )

		return imported
