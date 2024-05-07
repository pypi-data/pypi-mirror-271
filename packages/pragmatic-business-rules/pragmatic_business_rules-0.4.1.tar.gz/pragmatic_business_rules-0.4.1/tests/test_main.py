from src.pragmatic_business_rules import process_rules
import pytest


class TestProcessRules:

	def test_assert_rule_schema(self):
		with pytest.raises(
			Exception,
			match="Invalid input for 'rules': 'actions' is a required property",
		):
			process_rules(
				[
					{
						"conditions": {
							"all": [],
						},
					},
				],
			)

		with pytest.raises(
			Exception,
			match="Invalid input for 'rules': The provided type for the action is invalid",
		):
			process_rules(
				[
					{
						"actions": {
							"unknown rule": {
								"set": True,
							},
						},
						"conditions": {
							"all": [],
						},
					},
				],
			)

		with pytest.raises(
			Exception,
			match="Invalid input for 'rules': The provided operator for the condition is invalid",
		):
			process_rules(
				[
					{
						"actions": {},
						"conditions": {
							"all": [{
								"variable": "variable",
								"operator": "invalid operator",
								"value": 1,
							}],
						},
					},
				],
			)

	def test_assert_constant_schema(self):
		with pytest.raises(
			Exception,
			match="Invalid input for 'constants': {} is not of type 'null', 'number', 'string'",
		):
			process_rules(
				[],
				constants={
					"an object": {},
				},
			)

	def test_assert_variable_schema(self):
		with pytest.raises(
			Exception,
			match="Invalid input for 'variables': {} is not of type 'null', 'number', 'string'",
		):
			process_rules(
				[],
				variables={
					"an object": {},
				},
			)

	def test_assert_single_conditional(self):
		with pytest.raises(
			Exception,
			match="'all' and 'any' properties can't be specified for the same conditional"
		):
			process_rules(
				[
					{
						"actions": {},
						"conditions": {
							"all": [],
							"any": []
						},
					},
				],
			)

	def test_assert_valid_conditional(self):
		with pytest.raises(
			Exception,
			match="'all' or 'any' properties were not found in the conditional"
		):
			process_rules(
				[
					{
						"actions": {},
						"conditions": {},
					},
				],
			)

	def test_apply_no_action(self):
		item_name = "single key"
		current_item_value = 42.12
		expected_item_value = 99
		variable_name = "some variable"
		variable_value = "xyz"

		result = process_rules(
			[
				{
					"actions": {
						item_name: {
							"set": expected_item_value
						}
					},
					"conditions": {
						"any": [{
							"variable": variable_name,
							"operator": "equal_to",
							"value": variable_value + "abc",
						}],
					}
				},
			],
			variables={
				item_name: current_item_value,
				variable_name: variable_value,
			},
		)

		assert result.get(item_name) == current_item_value

	def test_apply_single_action(self):
		item_name = "single key"
		item_value = 1
		constant_name = "some variable"
		constant_value = 77

		result = process_rules(
			[
				{
					"actions": {
						item_name: {
							"set": item_value
						}
					},
					"conditions": {
						"any": [{
							"constant": constant_name,
							"operator": "equal_to",
							"value": constant_value,
						}],
					}
				},
			],
			constants={
				constant_name: constant_value,
			},
			variables={
				item_name: item_value - 1,
			},
		)

		assert result.get(item_name) == item_value

	def test_not_apply_invalid_condition(self):
		item_name = "single key"
		current_item_value = 0
		expected_item_value = 1
		variable_name = "some variable"
		variable_value = 77

		result = process_rules(
			[
				{
					"actions": {
						item_name: {
							"set": expected_item_value
						}
					},
					"conditions": {
						"any": [{
							"variable": variable_name,
							"operator": "less_than",
							"value": variable_value,
						}],
					}
				},
			],
			variables={
				item_name: expected_item_value - 1,
				variable_name: variable_value,
			},
		)

		assert result.get(item_name) == current_item_value

	def test_apply_multiple_actions(self):
		constant_1_name = "some variable"
		constant_1_value = 12
		constant_2_name = "other_variable"
		constant_2_value = 241.7
		variable_1_name = "some item name"
		variable_1_value = 1
		variable_2_name = "some other item name"
		variable_2_value = "asd"

		result = process_rules(
			[
				{
					"actions": {
						variable_1_name: {
							"set": variable_1_value
						}
					},
					"conditions": {
						"any": [{
							"constant": constant_1_name,
							"operator": "equal_to",
							"value": constant_1_value,
						}],
					}
				},
				{
					"actions": {
						variable_2_name: {
							"set": variable_2_value
						}
					},
					"conditions": {
						"all": [
							{
								"constant": constant_1_name,
								"operator": "equal_to",
								"value": constant_1_value,
							},
							{
								"constant": constant_2_name,
								"operator": "equal_to",
								"value": constant_2_value,
							},
						],
					}
				},
			],
			constants={
				constant_1_name: constant_1_value,
				constant_2_name: constant_2_value,
			},
			variables={
				variable_1_name: variable_1_value - 100,
				variable_2_name: variable_2_value + "123",
			},
		)

		assert result.get(variable_1_name) == variable_1_value
		assert result.get(variable_2_name) == variable_2_value

	# This checks that actions are applied to variables,
	# and those results are immediately available for the following evaluations
	def test_action_are_applied_to_variables_immediately(self):
		variable_1_name = "variable_1"
		variable_1_value = 1
		variable_2_name = "variable_2"
		variable_2_value = 0
		variable_3_name = "variable_3"
		variable_3_value = 0

		result = process_rules(
			[
				{
					"actions": {
						variable_2_name: {
							"set": 1
						}
					},
					"conditions": {
						"any": [{
							"variable": variable_1_name,
							"operator": "equal_to",
							"value": 1,
						}],
					}
				},
				{
					"actions": {
						variable_3_name: {
							"set": 1
						}
					},
					"conditions": {
						"any": [{
							"variable": variable_2_name,
							"operator": "equal_to",
							"value": 1,
						}],
					}
				},
			],
			variables={
				variable_1_name: variable_1_value,
				variable_2_name: variable_2_value,
				variable_3_name: variable_3_value,
			},
		)

		assert result.get(variable_3_name) == 1

	def test_actions_are_not_applied_to_constants(self):
		constant_1_name = "constant 1"
		constant_2_name = "constant 2"
		constant_2_value = 1

		with pytest.raises(
			Exception,
			match=f"The key '{constant_1_name}' is not defined in the variables object",
		):
			process_rules(
				[
					{
						"actions": {
							constant_1_name: {
								"set": 1
							}
						},
						"conditions": {
							"any": [{
								"constant": constant_2_name,
								"operator": "equal_to",
								"value": constant_2_value,
							}],
						}
					},
				],
				constants={
					constant_1_name: 0,
					constant_2_name: constant_2_value
				}
			)