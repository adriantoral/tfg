from typing import Any, Literal, Tuple


class QueryWhereConditions:
	"""
	Class to define conditions for SQL WHERE clauses.

	Attributes
	----------
	CRITERIA_CONDITIONS : Literal
		Literal types for SQL comparison operators.
	CRITERIA_JOIN_CONDITIONS : Literal
		Literal types for SQL logical operators.
	"""

	CRITERIA_CONDITIONS = Literal['=', '!=', '>', '<', '>=', '<=', 'LIKE', 'IN', 'NOT IN']
	CRITERIA_JOIN_CONDITIONS = Literal['AND', 'OR']

	@staticmethod
	def condition ( join_type: CRITERIA_JOIN_CONDITIONS, criteria_condition: CRITERIA_CONDITIONS, criteria: Any ) -> \
			Tuple[CRITERIA_JOIN_CONDITIONS, CRITERIA_CONDITIONS, Any]:
		"""
		Defines a condition for a SQL WHERE clause.

		:param join_type: The logical operator to join conditions (e.g., AND, OR).
		:type join_type: CRITERIA_JOIN_CONDITIONS
		:param criteria_condition: The comparison operator for the condition (e.g., =, !=, >).
		:type criteria_condition: CRITERIA_CONDITIONS
		:param criteria: The value to compare against.
		:type criteria: Any
		:return: A tuple representing the condition.
		:rtype: Tuple[CRITERIA_JOIN_CONDITIONS, CRITERIA_CONDITIONS, Any]
		"""

		return join_type, criteria_condition, criteria

	@staticmethod
	def OR ( criteria_condition: CRITERIA_CONDITIONS, criteria: Any ) -> \
			Tuple[CRITERIA_JOIN_CONDITIONS, CRITERIA_CONDITIONS, Any]:
		"""
		Defines an OR condition for a SQL WHERE clause.

		:param criteria_condition: The comparison operator for the condition (e.g., =, !=, >).
		:type criteria_condition: CRITERIA_CONDITIONS
		:param criteria: The value to compare against.
		:type criteria: Any
		:return: A tuple representing the OR condition.
		:rtype: Tuple[CRITERIA_JOIN_CONDITIONS, CRITERIA_CONDITIONS, Any]
		"""

		return QueryWhereConditions.condition( 'OR', criteria_condition, criteria )

	@staticmethod
	def AND ( criteria_condition: CRITERIA_CONDITIONS, criteria: Any ) -> \
			Tuple[CRITERIA_JOIN_CONDITIONS, CRITERIA_CONDITIONS, Any]:
		"""
		Defines an AND condition for a SQL WHERE clause.

		:param criteria_condition: The comparison operator for the condition (e.g., =, !=, >).
		:type criteria_condition: CRITERIA_CONDITIONS
		:param criteria: The value to compare against.
		:type criteria: Any
		:return: A tuple representing the AND condition.
		:rtype: Tuple[CRITERIA_JOIN_CONDITIONS, CRITERIA_CONDITIONS, Any]
		"""

		return QueryWhereConditions.condition( 'AND', criteria_condition, criteria )
