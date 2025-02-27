from datetime import datetime

from lib.types.t_date import TDate
from lib.types.t_integer import TInteger
from lib.types.t_null import TNull
from lib.types.t_string import TString

TYPES_MAP = {
    str: TString,
    int: TInteger,
    float: TInteger,
    None: TNull,
    datetime: TDate,
}


def convert_to_type(value):
    return TYPES_MAP[type_value](value) if (type_value := type(value)) in TYPES_MAP else TNull()
