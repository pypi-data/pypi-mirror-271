from .asserts import assert_comparable_type, assert_single_conditional
from .types import Condition, Conditional, number
from decimal import Decimal
from typing import TypedDict, cast, Literal, Optional, Union

class ConditionValues(TypedDict):
	label_1: Optional[str]
	label_2: Optional[str]
	value_1: Union[None, number, str]
	value_2: Union[None, number, str]

def __get_condition_values(
	condition: Condition,
	constants: dict[str, Union[number, str]],
	variables: dict[str, Union[number, str]],
) -> ConditionValues:
	categories = list(filter(lambda k: k != "operator", condition.keys()))

	if len(categories) == 0:
		raise Exception("No values were found to execute the condition")
	elif len(categories) != 2:
		raise Exception(f'A condition must be composed by two categories of values, {"only " if len(categories) == 1 else ""}"{", ".join(sorted(categories))}" found')
	
	values: dict = {}
	i = 1
	for category in categories:
		label: Optional[str] = None
		value: Union[None, number, str]

		if category == "constant":
			constant_name = cast(str, condition.get(category))
			if constant_name not in constants:
				raise Exception(f"Constant '{constant_name}' not defined")

			label = constant_name
			value = constants[constant_name]
		elif category == "value":
			value = condition[cast(Literal["value"], category)]
		elif category == "variable":
			variable_name = cast(str, condition.get(category))
			if variable_name not in variables:
				raise Exception(f"Variable '{variable_name}' not defined")
			
			label = variable_name
			value = variables[variable_name]

		if i == 1:
			values["label_1"] = label
			values["value_1"] = value
		else:
			values["label_2"] = label
			values["value_2"] = value

		i += 1
	
	return cast(ConditionValues, values)

# By this point, the incoming conditions and variables have to have been already validated
# for correct value types
def evaluate_condition(
	condition: Condition,
	constants: dict[str, Union[number, str]],
	variables: dict[str, Union[number, str]],
) -> bool:
	condition_operator = condition["operator"]
	values = __get_condition_values(condition, constants, variables)
	value_1 = values["value_1"]
	value_2 = values["value_2"]

	assert_comparable_type(
		values["label_1"],
		value_1,
		values["label_2"],
		value_2,
	)

	# The only value comparable to None is string, so they can be grouped in the same category
	if type(value_1) == str or value_1 is None:
		if condition_operator == "equal_to":
			return value_1 == value_2
		else:
			raise Exception(
				f"The operator '{condition_operator}' is not valid for string operations"
			)
	elif type(value_1) == Decimal or type(value_1) == int or type(value_1) == float:
		if condition_operator == "equal_to":
			return value_1 == value_2
		elif condition_operator == "greater_than_or_equal_to":
			return value_1 >= value_2 # type: ignore[operator]
		elif condition_operator == "greater_than":
			return value_1 > value_2 # type: ignore[operator]
		elif condition_operator == "less_than_or_equal_to":
			return value_1 <= value_2 # type: ignore[operator]
		elif condition_operator == "less_than":
			return value_1 < value_2 # type: ignore[operator]
		else:
			raise Exception(
				f"The operator '{condition_operator}' is not valid for number operations"
			)
	else:
		raise Exception(
			"The value '{}' has a type '{}' which is not valid for a condition value"
			.format(
				value_1,
				type(value_1).__name__,
			)
		)


def evaluate_conditional(
	conditional: Optional[list[Union[Conditional, Condition]]],
	constants: dict[str, Union[str, number]],
	variables: dict[str, Union[str, number]],
	type: Literal["all", "any"],
) -> bool:
	"""
	This function will evaluate the conditionals and return the boolean result for the entire group

	The evaluation process is different depending on the type:
	- all: All conditionals must be true
	- any: At least one conditional must be true
	"""
	if type not in ["all", "any"]:
		raise Exception(
			f"The evaluation type '{type}' is not a valid conditional type"
		)

	if conditional is None:
		return False

	# Make sure that the conditional contains items that can be evaluated
	# If no items were evaluated, mark the conditional as false
	evaluated_items = 0
	# If the type is "all", the goal is to change the result to false, if it's "any"
	# we try to set it to true
	result = True if type == "all" else False
	for c in conditional:
		condition_result = None

		# If it contains a value, it's a simple condition
		if "operator" in c:
			condition_result = evaluate_condition(cast(Condition, c), constants, variables)
		else:
			assert_single_conditional(c)

			all = c.get("all")
			any = c.get("any")

			subconditional = all if all is not None else any
			subtype: Literal["all", "any"] = "all" if all is not None else "any"

			condition_result = evaluate_conditional(
				subconditional,
				constants,
				variables,
				subtype,
			)

		# Should never happen
		if condition_result is None:
			raise Exception("The evaluation of a condition failed")

		evaluated_items += 1

		# If one of the conditions returned false and the type is set to "all", stop evaluating and return
		# There is no need to change the value otherwise
		if type == "all" and condition_result == False:
			result = condition_result
			break
		# If one of the conditions returned true and the type is set to "any", stop evaluating and return
		elif type == "any" and condition_result == True:
			result = condition_result
			break

	return result if evaluated_items > 0 else False
