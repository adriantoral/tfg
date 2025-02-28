from datetime import datetime

from lib.types.date import TDate
from lib.types.integer import TInteger
from lib.types.null import TNull
from lib.types.string import TString

TYPES_MAP = {
	str     : TString,
	int     : TInteger,
	float   : TInteger,
	None    : TNull,
	datetime: TDate,
}


def convert_to_type ( value ):
	"""
	Convert a value to its corresponding type.

	:param value: The value to be converted.
	:type value: Any
	:return: The converted value.
	:rtype: ITypes
	"""

	return TYPES_MAP[type_value]( value ) if (type_value := type( value )) in TYPES_MAP else TNull( )
