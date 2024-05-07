from __future__ import annotations
from decimal import Decimal
from typing import Literal, Optional, TypedDict, Union

number = Union[Decimal, int, float]

class Action(TypedDict):
	set: Optional[Union[number, str]]


class Condition(TypedDict):
	constant: Optional[str]
	operator: Literal["equal_to", "greater_than_or_equal_to", "greater_than",
										"less_than_or_equal_to", "less_than"]
	value: Optional[Union[number, str]]
	variable: Optional[str]


class Conditional(TypedDict):
	all: Optional[list[Union[Conditional, Condition]]]
	any: Optional[list[Union[Conditional, Condition]]]


class Rule(TypedDict):
	actions: dict[str, Action]
	conditions: Conditional
