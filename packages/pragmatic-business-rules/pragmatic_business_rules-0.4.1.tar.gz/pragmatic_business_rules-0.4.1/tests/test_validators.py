from decimal import Decimal
from jsonschema.exceptions import ValidationError
from src.pragmatic_business_rules.validators import rule_schema, variable_schema
import jsonschema
import pytest

def test_conditions():
	jsonschema.validate(
		[
			{
				"actions": {},
				"conditions": {
					"any": [
						{
							"variable": "some variable",
							"constant": "some constant",
							"operator": "equal_to",
							"value": "something"
						}
					]
				}
			}
		],
		rule_schema,
	)
	
	with pytest.raises(ValidationError) as variable_error:
		jsonschema.validate(
			[
				{
					"actions": {},
					"conditions": {
						"any": [
							{
								"variable": 1,
							}
						]
					}
				}
			],
			rule_schema,
		)

	assert variable_error.value.json_path == "$[0].conditions.any[0].variable"
	assert variable_error.value.validator == "type"

	with pytest.raises(ValidationError) as constant_error:
		jsonschema.validate(
			[
				{
					"actions": {},
					"conditions": {
						"any": [
							{
								"constant": 1,
							}
						]
					}
				}
			],
			rule_schema,
		)

	assert constant_error.value.json_path == "$[0].conditions.any[0].constant"
	assert constant_error.value.validator == "type"

	with pytest.raises(ValidationError) as operator_error:
		jsonschema.validate(
			[
				{
					"actions": {},
					"conditions": {
						"any": [
							{
								"variable": "asd",
							}
						]
					}
				}
			],
			rule_schema,
		)

	assert operator_error.value.json_path == "$[0].conditions.any[0]"
	assert operator_error.value.validator == "required"

def test_plain_dictionary_schema():
	jsonschema.validate({}, variable_schema)
	jsonschema.validate(
		{
			"string": "some string",
			"int": 1,
			"float": 2.5,
			"decimal": Decimal(12),
			"none": None,
		},
		variable_schema,
	)

	with pytest.raises(
		ValidationError,
		match="{} is not of type 'null', 'number', 'string'",
	):
		jsonschema.validate(
			{
				"an object": {},
			},
			variable_schema,
		)
