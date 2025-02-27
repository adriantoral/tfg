from dataclasses import dataclass
from typing import Optional

from lib.interfaces.models import IModels
from lib.tables.table import SELECT_ALL, Table
from lib.types.t_integer import TInteger
from lib.types.t_string import TString

TABLE_NAME = 'CULT_BIENES_PICKLIST'
IGNORE = [
	'objectid'
]


@dataclass
class CultBienesPicklistModel( IModels ):
	"""
	Modelo para representar un elemento de lista de selección de bien cultural.
	"""

	objectid: Optional[int] = None
	cd_codigo: Optional[str] = None
	cd_tipo: Optional[str] = None
	nm_orden: Optional[int] = None
	ds_valor: Optional[str] = None

	@staticmethod
	def create ( cd_codigo: str, cd_tipo: str, ds_valor: str ):
		"""
		Crea una nueva instancia de CultBienesPicklistModel.

		:param cd_codigo: El código del bien cultural.
		:param cd_tipo: El tipo de lista de selección.
		:param ds_valor: El valor del elemento de lista de selección.
		:return: Una instancia de CultBienesPicklistModel.
		"""

		data = Table( TABLE_NAME ).select(
			'NM_ORDEN',
			where=f'''CD_CODIGO={TString( cd_codigo )} and CD_TIPO={TString( cd_tipo )}''',
			order_by='OBJECTID DESC'
		)

		last_nm_orden = data[0][0] if len( data ) else 0

		return CultBienesPicklistModel(
			cd_codigo=cd_codigo,
			cd_tipo=cd_tipo,
			nm_orden=last_nm_orden + 1,
			ds_valor=ds_valor
		)

	@staticmethod
	def read ( cd_codigo: str ):
		"""
		Lee elementos de lista de selección de un bien cultural existente.

		:param cd_codigo: El código del bien cultural.
		:return: Una lista de instancias de CultBienesPicklistModel.
		"""

		data = Table( TABLE_NAME ).select(
			SELECT_ALL,
			where=f'''CD_CODIGO={TString( cd_codigo )}'''
		)

		if not len( data ): raise ValueError( f'{cd_codigo} not found in {TABLE_NAME}' )
		return [CultBienesPicklistModel( *row ) for row in data]

	def save ( self ):
		"""
		Guarda el elemento de lista de selección actual.
		"""

		return self._save(
			f'OBJECTID={TInteger( self.objectid )}',
			self.cd_codigo,
			CultBienesPicklistModel,
			Table( TABLE_NAME ),
			IGNORE,
			is_update=bool( self.objectid )
		)

	def delete ( self ):
		"""
		Elimina el elemento de lista de selección actual.
		"""

		if not self.objectid: raise ValueError( 'OBJECTID is required to delete' )
		return Table( TABLE_NAME ).delete( f'OBJECTID={TInteger( self.objectid )}' )
