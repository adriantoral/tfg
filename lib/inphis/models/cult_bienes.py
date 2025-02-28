import datetime
from dataclasses import dataclass
from typing import Optional

from lib.interfaces.models import IModels
from lib.tables.table import SELECT_ALL, Table
from lib.types.integer import TInteger
from lib.types.string import TString

TABLE_NAME = 'CULT_BIENES'
IGNORE = [
	'objectid',
	'shape',
	'shape_length',
	'shape_area'
]


@dataclass
class CultBienesModel( IModels ):
	"""
	Model to represent a cult_bien.
	"""

	objectid: Optional[int] = None
	shape: Optional[bytearray] = None
	cd_codigo: Optional[str] = None
	tl_nombre: Optional[str] = None
	tl_dircalle: Optional[str] = None
	nm_dirnum: Optional[int] = None
	tl_localidad: Optional[str] = None
	tl_otros_nombres: Optional[str] = None
	cd_cod_ant: Optional[str] = None
	nm_utm_x: Optional[float] = None
	nm_utm_y: Optional[float] = None
	tl_geo_lon: Optional[str] = None
	tl_geo_lat: Optional[str] = None
	nm_altitud: Optional[int] = None
	nm_extension: Optional[int] = None
	cl_accesos: Optional[str] = None
	cl_des_general: Optional[str] = None
	nm_cronologia_inicio: Optional[int] = None
	nm_cronologia_fin: Optional[int] = None
	cl_just_atribucion: Optional[str] = None
	cl_des_bien: Optional[str] = None
	cl_des_muebles: Optional[str] = None
	cl_fuentes_escritas: Optional[str] = None
	cl_fuentes_carto: Optional[str] = None
	cl_fuentes_icono: Optional[str] = None
	cl_fuentes_orales: Optional[str] = None
	cl_uso_estado: Optional[str] = None
	tl_estado_porc_extraido: Optional[str] = None
	tl_figura2: Optional[str] = None
	tl_figura3: Optional[str] = None
	tl_figura4: Optional[str] = None
	tl_figura5: Optional[str] = None
	cl_observaciones: Optional[str] = None
	tl_autor: Optional[str] = None
	tl_supervisor: Optional[str] = None
	fc_autor_fecha_cumplimenta: Optional[datetime.datetime] = None
	fc_super_fecha_cumplimenta: Optional[datetime.datetime] = None
	geometry1_sk: Optional[str] = None
	tl_adjunto: Optional[str] = None
	id_referencia: Optional[int] = None
	tl_fecha_referencia: Optional[str] = None
	cd_yac_referencia: Optional[str] = None
	cd_catalogo_regional: Optional[str] = None
	cd_catalogo_urbanistico: Optional[str] = None
	fc_inscripcion_catalogo: Optional[datetime.datetime] = None
	tl_proteccion_arq_regional: Optional[str] = None
	tl_dir_postal: Optional[str] = None
	tl_dir_poligono: Optional[str] = None
	tl_referencia_catastral: Optional[str] = None
	cl_historia_bien: Optional[str] = None
	cl_obras_usos: Optional[str] = None
	tl_arca: Optional[str] = None
	cl_otros_codigos: Optional[str] = None
	fc_fecha_modificacion: Optional[datetime.datetime] = None
	shape_length: Optional[float] = None
	shape_area: Optional[float] = None
	geometry_bk: Optional[str] = None
	geometry_x_bk: Optional[float] = None
	geometry_y_bk: Optional[float] = None
	geometry_area_bk: Optional[float] = None

	@staticmethod
	def generate_cd_codigo ( cult_var_municipios_cd_values: list[str] ):
		"""
		Generate a code for a new cult_bien.

		:param cult_var_municipios_cd_values: A list of municipality codes.
		:return: A generated code for the cult_bien.
		:rtype: str
		"""

		cd_value = '000' if len( cult_var_municipios_cd_values ) > 1 else cult_var_municipios_cd_values[0]
		data = Table( TABLE_NAME ).select(
			'CD_CODIGO',
			where=f'''CD_CODIGO like {TString( f'CM/{cd_value}/%' )}''',
			order_by='CD_CODIGO DESC'
		)

		last_cd_codigo = data[0][0] if data else f'CM/{cd_value}/0000'
		prefijo, cd_value, id_contador = last_cd_codigo.split( '/' )

		return f'{prefijo}/{cd_value}/{str( int( id_contador ) + 1 ).zfill( 4 )}'

	@staticmethod
	def create ( tl_nombre: str, cult_var_municipios_cd_values: list[str] ):
		"""
		Create a new instance of CultBienesModel.

		:param tl_nombre: The name of the cult_bien.
		:param cult_var_municipios_cd_values: A list of municipality codes.
		:return: An instance of CultBienesModel.
		:rtype: CultBienesModel
		"""

		return CultBienesModel(
			cd_codigo=CultBienesModel.generate_cd_codigo( cult_var_municipios_cd_values ),
			tl_nombre=tl_nombre
		)

	@staticmethod
	def read ( cd_codigo: str ):
		"""
		Read an existing cult_bien.

		:param cd_codigo: The code of the cult_bien.
		:return: A list of instances of CultBienesModel.
		:rtype: list[CultBienesModel]
		"""

		data = Table( TABLE_NAME ).select(
			SELECT_ALL,
			where=f'''CD_CODIGO={TString( cd_codigo )}'''
		)

		if not len( data ): raise ValueError( f'{cd_codigo} not found in {TABLE_NAME}' )
		return [CultBienesModel( *row ) for row in data]

	def save ( self ):
		"""
		Save the current cult_bien.
		"""

		return self._save(
			f'OBJECTID={TInteger( self.objectid )}',
			self.cd_codigo,
			CultBienesModel,
			Table( TABLE_NAME ),
			IGNORE,
			is_update=bool( self.objectid )
		)

	def delete ( self ):
		"""
		Delete the current cult_bien.

		:raises ValueError: If OBJECTID is not set.
		"""

		if not self.objectid: raise ValueError( 'OBJECTID is required to delete' )
		return Table( TABLE_NAME ).delete( f'OBJECTID={TInteger( self.objectid )}' )
