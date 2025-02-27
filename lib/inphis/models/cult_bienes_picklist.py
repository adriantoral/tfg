from dataclasses import dataclass

from lib.interfaces.models import IModels
from lib.tables.table import Table, SELECT_ALL
from lib.types.t_integer import TInteger
from lib.types.t_string import TString

TABLE_NAME = 'CULT_BIENES_PICKLIST'
IGNORE = [
    'objectid'
]


@dataclass
class CultBienesPicklistModel(IModels):
    objectid: int = None
    cd_codigo: str = None
    cd_tipo: str = None
    nm_orden: int = None
    ds_valor: str = None

    @staticmethod
    def create(cd_codigo: str, cd_tipo: str, ds_valor: str):
        data = Table(TABLE_NAME).select(
            'NM_ORDEN',
            where=f'''CD_CODIGO={TString(cd_codigo)} and CD_TIPO={TString(cd_tipo)}''',
            order_by='OBJECTID DESC'
        )

        last_nm_orden = data[0][0] if len(data) else 0

        return CultBienesPicklistModel(
            cd_codigo=cd_codigo,
            cd_tipo=cd_tipo,
            nm_orden=last_nm_orden + 1,
            ds_valor=ds_valor
        )

    @staticmethod
    def read(cd_codigo: str):
        data = Table(TABLE_NAME).select(
            SELECT_ALL,
            where=f'''CD_CODIGO={TString(cd_codigo)}'''
        )

        if not len(data):
            raise ValueError(f'{cd_codigo} not found in {TABLE_NAME}')

        return [CultBienesPicklistModel(*row) for row in data]

    def save(self):
        return self._save(
            f'OBJECTID={TInteger(self.objectid)}',
            self.cd_codigo,
            CultBienesPicklistModel,
            Table(TABLE_NAME),
            IGNORE,
            is_update=bool(self.objectid)
        )

    def delete(self):
        if not self.objectid:
            raise ValueError('OBJECTID is required to delete')

        return Table(TABLE_NAME).delete(f'OBJECTID={TInteger(self.objectid)}')
