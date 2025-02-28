from dataclasses import dataclass
from typing import Optional

from lib.interfaces.models import IModels
from lib.tables.table import SELECT_ALL, Table
from lib.types.integer import TInteger
from lib.types.string import TString

TABLE_NAME = 'CULT_BIENES_PICKLIST'
IGNORE = [
	'objectid'
]


@dataclass
class CultBienesPicklistModel( IModels ):
	"""
	Model to represent a cult_bien picklist item.
	"""

	objectid: Optional[int] = None
	cd_codigo: Optional[str] = None
	cd_tipo: Optional[str] = None
	nm_orden: Optional[int] = None
	ds_valor: Optional[str] = None

	@staticmethod
	def create ( cd_codigo: str, cd_tipo: str, ds_valor: str ):
		"""
		Create a new instance of CultBienesPicklistModel.

		:param cd_codigo: The code of the cult_bien.
		:type cd_codigo: str
		:param cd_tipo: The type of picklist.
		:type cd_tipo: str
		:param ds_valor: The value of the picklist item.
		:type ds_valor: str
		:returns: An instance of CultBienesPicklistModel.
		:rtype: CultBienesPicklistModel
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
		Read picklist items of an existing cult_bien.

		:param cd_codigo: The code of the cult_bien.
		:type cd_codigo: str
		:returns: A list of instances of CultBienesPicklistModel.
		:rtype: list[CultBienesPicklistModel]
		"""

		data = Table( TABLE_NAME ).select(
			SELECT_ALL,
			where=f'''CD_CODIGO={TString( cd_codigo )}'''
		)

		if not len( data ): raise ValueError( f'{cd_codigo} not found in {TABLE_NAME}' )
		return [CultBienesPicklistModel( *row ) for row in data]

	def save ( self ):
		"""
		Save the current picklist item.
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
		Delete the current picklist item.

		:raises ValueError: If OBJECTID is not set.
		"""

		if not self.objectid: raise ValueError( 'OBJECTID is required to delete' )
		return Table( TABLE_NAME ).delete( f'OBJECTID={TInteger( self.objectid )}' )
