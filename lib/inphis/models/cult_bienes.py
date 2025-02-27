import datetime
from dataclasses import dataclass

from lib.interfaces.models import IModels
from lib.tables.table import Table, SELECT_ALL
from lib.types.t_integer import TInteger
from lib.types.t_string import TString

TABLE_NAME = 'CULT_BIENES'
IGNORE = [
    'objectid',
    'shape',
    'shape_length',
    'shape_area'
]


@dataclass
class CultBienesModel(IModels):
    objectid: int = None
    shape: bytearray = None
    cd_codigo: str = None
    tl_nombre: str = None
    tl_dircalle: str = None
    nm_dirnum: int = None
    tl_localidad: str = None
    tl_otros_nombres: str = None
    cd_cod_ant: str = None
    nm_utm_x: float = None
    nm_utm_y: float = None
    tl_geo_lon: str = None
    tl_geo_lat: str = None
    nm_altitud: int = None
    nm_extension: int = None
    cl_accesos: str = None
    cl_des_general: str = None
    nm_cronologia_inicio: int = None
    nm_cronologia_fin: int = None
    cl_just_atribucion: str = None
    cl_des_bien: str = None
    cl_des_muebles: str = None
    cl_fuentes_escritas: str = None
    cl_fuentes_carto: str = None
    cl_fuentes_icono: str = None
    cl_fuentes_orales: str = None
    cl_uso_estado: str = None
    tl_estado_porc_extraido: str = None
    tl_figura2: str = None
    tl_figura3: str = None
    tl_figura4: str = None
    tl_figura5: str = None
    cl_observaciones: str = None
    tl_autor: str = None
    tl_supervisor: str = None
    fc_autor_fecha_cumplimenta: datetime.datetime = None
    fc_super_fecha_cumplimenta: datetime.datetime = None
    geometry1_sk: str = None
    tl_adjunto: str = None
    id_referencia: int = None
    tl_fecha_referencia: str = None
    cd_yac_referencia: str = None
    cd_catalogo_regional: str = None
    cd_catalogo_urbanistico: str = None
    fc_inscripcion_catalogo: datetime.datetime = None
    tl_proteccion_arq_regional: str = None
    tl_dir_postal: str = None
    tl_dir_poligono: str = None
    tl_referencia_catastral: str = None
    cl_historia_bien: str = None
    cl_obras_usos: str = None
    tl_arca: str = None
    cl_otros_codigos: str = None
    fc_fecha_modificacion: datetime.datetime = None
    shape_length: float = None
    shape_area: float = None
    geometry_bk: str = None
    geometry_x_bk: float = None
    geometry_y_bk: float = None
    geometry_area_bk: float = None

    @staticmethod
    def generate_cd_codigo(cult_var_municipios_cd_values: list[str]):
        cd_value = '000' if len(cult_var_municipios_cd_values) > 1 else cult_var_municipios_cd_values[0]
        data = Table(TABLE_NAME).select(
            'CD_CODIGO',
            where=f'''CD_CODIGO like {TString(f'CM/{cd_value}/%')}''',
            order_by='CD_CODIGO DESC'
        )

        last_cd_codigo = data[0][0] if data else f'CM/{cd_value}/0000'
        prefijo, cd_value, id_contador = last_cd_codigo.split('/')

        return f'{prefijo}/{cd_value}/{str(int(id_contador) + 1).zfill(4)}'

    @staticmethod
    def create(tl_nombre: str, cult_var_municipios_cd_values: list[str]):
        return CultBienesModel(
            cd_codigo=CultBienesModel.generate_cd_codigo(cult_var_municipios_cd_values),
            tl_nombre=tl_nombre
        )

    @staticmethod
    def read(cd_codigo: str):
        data = Table(TABLE_NAME).select(
            SELECT_ALL,
            where=f'''CD_CODIGO={TString(cd_codigo)}'''
        )

        if not len(data):
            raise ValueError(f'{cd_codigo} not found in {TABLE_NAME}')

        return [CultBienesModel(*row) for row in data]

    def save(self):
        return self._save(
            f'OBJECTID={TInteger(self.objectid)}',
            self.cd_codigo,
            CultBienesModel,
            Table(TABLE_NAME),
            IGNORE,
            is_update=bool(self.objectid)
        )

    def delete(self):
        if not self.objectid:
            raise ValueError('OBJECTID is required to delete')

        return Table(TABLE_NAME).delete(f'OBJECTID={TInteger(self.objectid)}')
