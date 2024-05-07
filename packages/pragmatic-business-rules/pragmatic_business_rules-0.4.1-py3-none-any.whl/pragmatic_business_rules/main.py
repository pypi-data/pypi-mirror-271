from .action import apply_actions_to_variables
from .asserts import assert_single_conditional
from .condition import evaluate_conditional
from .types import Conditional, number, Rule
from .validators import constant_schema, CustomValidationError, variable_schema, rule_schema, validate_schema_with_custom_errors
from jsonschema.exceptions import ValidationError
from typing import Literal, Union
import jsonschema


def assert_valid_rules(rules: list[Rule]):
	"""
	This function runs a validation over the rules passed and raises a detailed message with any
	inconsistencies found
	"""
	validate_schema_with_custom_errors(rules, rule_schema)


def process_rules(
	rules: list[Rule],
	constants: dict[str, Union[number, str]] = {},
	variables: dict[str, Union[number, str]] = {},
) -> dict[str, Union[number, str]]:
	"""
	Process the rules and execute the result of the actions over the passed variables argument

	This function does not mutate the original variables object passed to it
	"""
	try:
		assert_valid_rules(rules)
	except CustomValidationError as validation_error:
		raise Exception(
			f"Invalid input for 'rules': {str(validation_error)}"
		) from validation_error
	except ValidationError as validation_error:
		raise Exception(
			f"Invalid input for 'rules': {str(validation_error)}"
		) from validation_error

	try:
		jsonschema.validate(constants, constant_schema)
	except ValidationError as validation_error:
		raise Exception(
			f"Invalid input for 'constants': {validation_error.message}"
		) from validation_error

	try:
		jsonschema.validate(variables, variable_schema)
	except ValidationError as validation_error:
		raise Exception(
			f"Invalid input for 'variables': {validation_error.message}"
		) from validation_error
	
	result = variables.copy()
	for rule in rules:
		actions = rule["actions"]
		conditions: Conditional = rule["conditions"]

		# Make sure the condition has one single conditional defined
		assert_single_conditional(conditions)

		all = conditions.get("all")
		any = conditions.get("any")

		conditional = all if all is not None else any if any is not None else []
		type: Literal["all", "any"] = "all" if all is not None else "any"

		if evaluate_conditional(conditional, constants, result, type):
			apply_actions_to_variables(actions, result)

	return result
