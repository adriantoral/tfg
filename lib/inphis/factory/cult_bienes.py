import csv

from lib.inphis.models.cult_bienes import CultBienesModel
from lib.inphis.models.cult_bienes_picklist import CultBienesPicklistModel


class CultBienesFactory:
    @staticmethod
    def create_bien(tl_nombre: str, cult_var_municipios_cd_values: list[str]):
        cult_bien = CultBienesModel.create(tl_nombre, cult_var_municipios_cd_values)
        cult_bien.save()

        for municipio in cult_var_municipios_cd_values:
            CultBienesPicklistModel.create(cult_bien.cd_codigo, 'MUNICIPIO', municipio).save()

        return cult_bien

    @staticmethod
    def import_from_csv(
            csv_path: str,
            cult_var_municipios_separator: str = '-',
            bien_separator: str = ';',
            save_on_import: bool = True
    ):
        imported = []

        with open(csv_path, 'r') as csv_file:
            for line in csv.DictReader(csv_file, delimiter=bien_separator):
                model = CultBienesModel(
                    **{
                        key: CultBienesModel.__annotations__[key](value)
                        for key, value in line.items()
                    }
                )

                cult_var_municipios = model.cd_codigo.split(cult_var_municipios_separator)
                model.cd_codigo = CultBienesModel.generate_cd_codigo(cult_var_municipios)

                if save_on_import:
                    model.save()

                    for municipio in cult_var_municipios:
                        CultBienesPicklistModel.create(model.cd_codigo, 'MUNICIPIO', municipio).save()

                imported.append(model)

        return imported
