from .types import Conditional
from decimal import Decimal
from typing import Any, Optional

def assert_single_conditional(conditional: Conditional):
	all = conditional.get("all")
	any = conditional.get("any")

	if all is not None and any is not None:
		raise Exception(
			"'all' and 'any' properties can't be specified for the same conditional"
		)
	elif all is None and any is None:
		raise Exception(
			"'all' or 'any' properties were not found in the conditional"
		)


def assert_comparable_type(
	label_1: Optional[str],
	value_1: Any,
	label_2: Optional[str],
	value_2: Any,
):
	# None is comparable to string and None
	if (value_1 is None and value_2 is None) or (
		type(value_1) == str and value_2 is None
	) or (
		value_1 is None and type(value_2) == str
	):
		return

	# Decimal, ints and floats are comparable
	if type(value_1) in [Decimal, int, float] and type(value_2) in [Decimal, int, float]:
		return

	if type(value_1) != type(value_2):
		raise Exception(
			'Can\'t compare values ({}"{}", {}) and ({}"{}", {})'
			.format(
				f'"{label_1}", ' if label_1 is not None else "",
				value_1,
				type(value_1).__name__,
				f'"{label_2}", ' if label_2 is not None else "",
				value_2,
				type(value_2).__name__,
			)
		)
