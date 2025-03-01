from typing import Literal, get_args


class OrderByConditions:
	"""
	Class to define order by conditions.

	Attributes
	----------
	CRITERIA_ORDER : Literal
		A literal type that can be either 'ASC' or 'DESC'.
	"""

	CRITERIA_ORDER = Literal['ASC', 'DESC']
	CRITERIA_ORDER_VALUES = get_args( CRITERIA_ORDER )
