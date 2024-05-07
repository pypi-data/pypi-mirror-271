from decimal import Decimal
from src.pragmatic_business_rules.condition import assert_single_conditional, evaluate_condition, evaluate_conditional
import pytest


class TestAssertSingleConditional:

	def test_single_conditional(self):
		with pytest.raises(
			Exception,
			match="'all' and 'any' properties can't be specified for the same conditional"
		):
			assert_single_conditional({"all": [], "any": []})

	def test_valid_conditional(self):
		with pytest.raises(
			Exception,
			match="'all' or 'any' properties were not found in the conditional"
		):
			assert_single_conditional({})


class TestEvaluateCondition:

	def test_constant_exists(self):
		constant = "xyz"
		with pytest.raises(Exception, match=f"Constant '{constant}' not defined"):
			evaluate_condition(
				{
					"constant": constant,
					"operator": "equal_to",
					"value": "something"
				},
				{},
				{},
			)

	def test_variable_exists(self):
		variable = "xyz"
		with pytest.raises(Exception, match=f"Variable '{variable}' not defined"):
			evaluate_condition(
				{
					"variable": variable,
					"operator": "equal_to",
					"value": "something"
				},
				{},
				{},
			)

	def test_constant_matches_type(self):
		constant_name = "abc"
		constant_value = 1
		condition_value = "a string"
		with pytest.raises(
			Exception,
			match='\\("{}", "{}", {}\\) and \\("{}", {}\\)'.format(
				constant_name,
				constant_value,
				type(constant_value).__name__,
				condition_value,
				type(condition_value).__name__,
			),
		):
			evaluate_condition(
				{
					"constant": constant_name,
					"operator": "equal_to",
					"value": condition_value,
				},
				{
					constant_name: constant_value,
				},
				{},
			)

	def test_variable_matches_type(self):
		variable_name = "abc"
		variable_value = 1
		condition_value = "a string"
		with pytest.raises(
			Exception,
			match='\\("{}", "{}", {}\\) and \\("{}", {}\\)'.format(
				variable_name,
				variable_value,
				type(variable_value).__name__,
				condition_value,
				type(condition_value).__name__,
			),
		):
			evaluate_condition(
				{
					"variable": variable_name,
					"operator": "equal_to",
					"value": condition_value,
				},
				{},
				{
					variable_name: variable_value,
				},
			)

	def test_compares_between_number_types(self):
		constant_name = "abc"
		constant_value = 1
		condition_value = 1.5
		assert not evaluate_condition(
			{
				"constant": constant_name,
				"operator": "equal_to",
				"value": condition_value,
			},
			{
				constant_name: constant_value,
			},
			{},
		)

		variable_name = "abc"
		variable_value = 1.5
		condition_value = 1
		assert not evaluate_condition(
			{
				"variable": variable_name,
				"operator": "equal_to",
				"value": condition_value,
			},
			{},
			{
				variable_name: variable_value,
			},
		)

		variable_name = "abc"
		variable_value = 5
		condition_value = 5.0
		assert evaluate_condition(
			{
				"variable": variable_name,
				"operator": "equal_to",
				"value": condition_value,
			},
			{},
			{
				variable_name: variable_value,
			},
		)

		constant_name = "some"
		constant_value = Decimal(5)
		condition_value = 5
		assert evaluate_condition(
			{
				"constant": constant_name,
				"operator": "equal_to",
				"value": condition_value,
			},
			{
				constant_name: constant_value,
			},
			{},
		)

	def test_invalid_type(self):
		variable = "123"
		value = {}
		with pytest.raises(
			Exception,
			match="The value '{}' has a type '{}' which is not valid for a condition value"
			.format(
				value,
				type(value).__name__,
			)
		):
			evaluate_condition(
				{
					"variable": variable,
					"operator": "equal_to",
					"value": value,
				},
				{},
				{
					variable: {},
				},
			)

	def test_string_comparable_to_none(self):
		variable = "variable name"

		assert not evaluate_condition(
			{
				"variable": variable,
				"operator": "equal_to",
				"value": None,
			},
			{},
			{
				variable: "some value",
			},
		)

	def test_none_comparable_to_none(self):
		variable = "not a variable name"

		assert evaluate_condition(
			{
				"variable": variable,
				"operator": "equal_to",
				"value": None,
			},
			{},
			{
				variable: None,
			},
		)

	def test_string_equal_to(self):
		variable = "some variable"
		value = "some value"

		assert evaluate_condition(
			{
				"variable": variable,
				"operator": "equal_to",
				"value": value,
			},
			{},
			{
				variable: value,
			},
		)

		assert not evaluate_condition(
			{
				"variable": variable,
				"operator": "equal_to",
				"value": value,
			},
			{},
			{
				variable: value + " other",
			},
		)

	def test_invalid_string_operator(self):
		variable = "123"
		operator = "invalid operator"
		with pytest.raises(
			Exception,
			match=f"The operator '{operator}' is not valid for string operations"
		):
			evaluate_condition(
				{
					"variable": variable,
					"operator": operator,
					"value": "123",
				},
				{},
				{
					variable: "asd",
				},
			)

	def test_number_equal_to(self):
		variable = "some variable"
		value = 15

		assert evaluate_condition(
			{
				"variable": variable,
				"operator": "equal_to",
				"value": value,
			},
			{},
			{
				variable: value,
			},
		)

		assert not evaluate_condition(
			{
				"variable": variable,
				"operator": "equal_to",
				"value": value,
			},
			{},
			{
				variable: value + 10,
			},
		)

	def test_number_greater_than_or_equal_to(self):
		variable = "some variable"
		value = 450.54

		assert evaluate_condition(
			{
				"variable": variable,
				"operator": "greater_than_or_equal_to",
				"value": value,
			},
			{},
			{
				variable: value,
			},
		)

		assert evaluate_condition(
			{
				"variable": variable,
				"operator": "greater_than_or_equal_to",
				"value": value - 1,
			},
			{},
			{
				variable: value,
			},
		)

		assert not evaluate_condition(
			{
				"variable": variable,
				"operator": "greater_than_or_equal_to",
				"value": value + 1,
			},
			{},
			{
				variable: value,
			},
		)

	def test_number_greater_than(self):
		variable = "some variable"
		value = 125

		assert evaluate_condition(
			{
				"variable": variable,
				"operator": "greater_than",
				"value": value - 1,
			},
			{},
			{
				variable: value,
			},
		)

		assert not evaluate_condition(
			{
				"variable": variable,
				"operator": "greater_than",
				"value": value,
			},
			{},
			{
				variable: value,
			},
		)

		assert not evaluate_condition(
			{
				"variable": variable,
				"operator": "greater_than",
				"value": value + 1,
			},
			{},
			{
				variable: value,
			},
		)

	def test_number_less_than_or_equal_to(self):
		variable = "some variable"
		value = 521350.879821

		assert evaluate_condition(
			{
				"variable": variable,
				"operator": "less_than_or_equal_to",
				"value": value + 1,
			},
			{},
			{
				variable: value,
			},
		)

		assert evaluate_condition(
			{
				"variable": variable,
				"operator": "less_than_or_equal_to",
				"value": value,
			},
			{},
			{
				variable: value,
			},
		)

		assert not evaluate_condition(
			{
				"variable": variable,
				"operator": "less_than_or_equal_to",
				"value": value - 1,
			},
			{},
			{
				variable: value,
			},
		)

	def test_number_less_than(self):
		variable = "some variable"
		value = 48.5316541

		assert evaluate_condition(
			{
				"variable": variable,
				"operator": "less_than",
				"value": value + 1,
			},
			{},
			{
				variable: value,
			},
		)

		assert not evaluate_condition(
			{
				"variable": variable,
				"operator": "less_than",
				"value": value,
			},
			{},
			{
				variable: value,
			},
		)

		assert not evaluate_condition(
			{
				"variable": variable,
				"operator": "less_than",
				"value": value - 1,
			},
			{},
			{
				variable: value,
			},
		)

	def test_invalid_number_operator(self):
		variable = "number variable"
		operator = "invalid operator"
		with pytest.raises(
			Exception,
			match=f"The operator '{operator}' is not valid for number operations"
		):
			evaluate_condition(
				{
					"variable": variable,
					"operator": operator,
					"value": 0,
				},
				{},
				{
					variable: 1,
				},
			)


class TestEvaluateConditional:

	def test_invalid_type(self):
		type = "something else"
		with pytest.raises(
			Exception,
			match=f"The evaluation type '{type}' is not a valid conditional type"
		):
			evaluate_conditional(
				[],
				{},
				{},
				type,
			)

	def test_empty_conditional_yields_false(self):
		assert not evaluate_conditional([], {}, {}, "all")
		assert not evaluate_conditional([], {}, {}, "any")

	def test_all_conditions(self):
		variable_1 = "some variable"
		value_1 = 123
		variable_2 = "some other variable"
		value_2 = "xyz"

		assert evaluate_conditional(
			[
				{
					"variable": variable_1,
					"operator": "equal_to",
					"value": value_1,
				},
				{
					"variable": variable_2,
					"operator": "equal_to",
					"value": value_2,
				},
			],
			{},
			{
				variable_1: value_1,
				variable_2: value_2,
			},
			"all",
		)

		assert evaluate_conditional(
			[
				{
					"variable": variable_1,
					"operator": "equal_to",
					"value": value_1,
				},
			],
			{},
			{
				variable_1: value_1,
			},
			"all",
		)

		assert not evaluate_conditional(
			[
				{
					"variable": variable_1,
					"operator": "equal_to",
					"value": value_1,
				},
				{
					"variable": variable_2,
					"operator": "equal_to",
					"value": value_2 + "123",
				},
			],
			{},
			{
				variable_1: value_1,
				variable_2: value_2,
			},
			"all",
		)

		assert not evaluate_conditional(
			[
				{
					"variable": variable_1,
					"operator": "equal_to",
					"value": value_1 + 15,
				},
			],
			{},
			{
				variable_1: value_1,
			},
			"all",
		)

	def test_all_conditions_nested(self):
		variable_1 = "some variable"
		value_1 = 6487
		variable_2 = "some other variable"
		value_2 = "asdjn"
		variable_3 = "some other other variable"
		value_3 = 4580.1

		assert evaluate_conditional(
			[
				{
					"all": [
						{
							"variable": variable_1,
							"operator": "equal_to",
							"value": value_1,
						},
						{
							"variable": variable_2,
							"operator": "equal_to",
							"value": value_2,
						},
					],
				},
				{
					"all": [{
						"variable": variable_3,
						"operator": "equal_to",
						"value": value_3,
					}],
				},
			],
			{},
			{
				variable_1: value_1,
				variable_2: value_2,
				variable_3: value_3,
			},
			"all",
		)

		assert evaluate_conditional(
			[
				{
					"all": [
						{
							"variable": variable_1,
							"operator": "equal_to",
							"value": value_1,
						},
						{
							"variable": variable_2,
							"operator": "equal_to",
							"value": value_2,
						},
					],
				},
			],
			{},
			{
				variable_1: value_1,
				variable_2: value_2,
			},
			"all",
		)

		assert not evaluate_conditional(
			[
				{
					"all": [
						{
							"variable": variable_1,
							"operator": "equal_to",
							"value": value_1,
						},
						{
							"variable": variable_2,
							"operator": "equal_to",
							"value": value_2 + "something",
						},
					],
				},
				{
					"all": [{
						"variable": variable_3,
						"operator": "equal_to",
						"value": value_3,
					}],
				},
			],
			{},
			{
				variable_1: value_1,
				variable_2: value_2,
				variable_3: value_3,
			},
			"all",
		)

		assert not evaluate_conditional(
			[
				{
					"all": [
						{
							"variable": variable_1,
							"operator": "equal_to",
							"value": value_1,
						},
						{
							"variable": variable_2,
							"operator": "equal_to",
							"value": value_2 + "something",
						},
					],
				},
				{
					"all": [{
						"variable": variable_3,
						"operator": "equal_to",
						"value": value_3 + 17,
					}],
				},
			],
			{},
			{
				variable_1: value_1,
				variable_2: value_2,
				variable_3: value_3,
			},
			"all",
		)

	def test_any_conditions(self):
		variable_1 = "some variable"
		value_1 = 47.5
		variable_2 = "some other variable"
		value_2 = "A1"

		assert evaluate_conditional(
			[
				{
					"variable": variable_1,
					"operator": "equal_to",
					"value": value_1,
				},
				{
					"variable": variable_2,
					"operator": "equal_to",
					"value": value_2,
				},
			],
			{},
			{
				variable_1: value_1,
				variable_2: value_2,
			},
			"any",
		)

		assert evaluate_conditional(
			[
				{
					"variable": variable_1,
					"operator": "equal_to",
					"value": value_1,
				},
				{
					"variable": variable_2,
					"operator": "equal_to",
					"value": value_2 + "asd",
				},
			],
			{},
			{
				variable_1: value_1,
				variable_2: value_2,
			},
			"any",
		)

		assert not evaluate_conditional(
			[
				{
					"variable": variable_1,
					"operator": "equal_to",
					"value": value_1 + 10,
				},
				{
					"variable": variable_2,
					"operator": "equal_to",
					"value": value_2 + "123",
				},
			],
			{},
			{
				variable_1: value_1,
				variable_2: value_2,
			},
			"any",
		)

	def test_any_conditions_nested(self):
		variable_1 = "some variable"
		value_1 = 19
		variable_2 = "some other variable"
		value_2 = "keeping"
		variable_3 = "some other other variable"
		value_3 = 5123.45

		assert evaluate_conditional(
			[
				{
					"any": [
						{
							"variable": variable_1,
							"operator": "equal_to",
							"value": value_1,
						},
						{
							"variable": variable_2,
							"operator": "equal_to",
							"value": value_2,
						},
					],
				},
				{
					"any": [{
						"variable": variable_3,
						"operator": "equal_to",
						"value": value_3,
					},],
				},
			],
			{},
			{
				variable_1: value_1,
				variable_2: value_2,
				variable_3: value_3,
			},
			"any",
		)

		assert evaluate_conditional(
			[
				{
					"any": [
						{
							"variable": variable_1,
							"operator": "equal_to",
							"value": value_1,
						},
						{
							"variable": variable_2,
							"operator": "equal_to",
							"value": value_2 + "something",
						},
					],
				},
				{
					"any": [{
						"variable": variable_3,
						"operator": "equal_to",
						"value": value_3,
					}],
				},
			],
			{},
			{
				variable_1: value_1,
				variable_2: value_2,
				variable_3: value_3,
			},
			"any",
		)

		assert evaluate_conditional(
			[
				{
					"any": [
						{
							"variable": variable_1,
							"operator": "equal_to",
							"value": value_1,
						},
						{
							"variable": variable_2,
							"operator": "equal_to",
							"value": value_2 + "something",
						},
					],
				},
				{
					"any": [{
						"variable": variable_3,
						"operator": "equal_to",
						"value": value_3 + 15156416,
					}],
				},
			],
			{},
			{
				variable_1: value_1,
				variable_2: value_2,
				variable_3: value_3,
			},
			"any",
		)

		assert not evaluate_conditional(
			[
				{
					"any": [
						{
							"variable": variable_1,
							"operator": "equal_to",
							"value": value_1 + 54164,
						},
						{
							"variable": variable_2,
							"operator": "equal_to",
							"value": value_2 + "something",
						},
					],
				},
				{
					"any": [{
						"variable": variable_3,
						"operator": "equal_to",
						"value": value_3 + 17,
					}],
				},
			],
			{},
			{
				variable_1: value_1,
				variable_2: value_2,
				variable_3: value_3,
			},
			"any",
		)

	def test_mixed_conditions_nested(self):
		variable_1 = "some variable"
		value_1 = 41684
		variable_2 = "some other variable"
		value_2 = "clancy"
		variable_3 = "some other other variable"
		value_3 = 178.45

		assert evaluate_conditional(
			[
				{
					"any": [
						{
							"variable": variable_1,
							"operator": "equal_to",
							"value": value_1,
						},
						{
							"variable": variable_2,
							"operator": "equal_to",
							"value": value_2 + "asd",
						},
					],
				},
				{
					"all": [{
						"variable": variable_3,
						"operator": "equal_to",
						"value": value_3,
					}],
				},
			],
			{},
			{
				variable_1: value_1,
				variable_2: value_2,
				variable_3: value_3,
			},
			"any",
		)

		assert not evaluate_conditional(
			[
				{
					"all": [
						{
							"variable": variable_1,
							"operator": "equal_to",
							"value": value_1,
						},
						{
							"variable": variable_2,
							"operator": "equal_to",
							"value": value_2 + "something",
						},
					],
				},
			],
			{},
			{
				variable_1: value_1,
				variable_2: value_2,
				variable_3: value_3,
			},
			"any",
		)

		assert evaluate_conditional(
			[
				{
					"all": [
						{
							"variable": variable_1,
							"operator": "equal_to",
							"value": value_1,
						},
						{
							"any": [
								{
									"variable": variable_2,
									"operator": "equal_to",
									"value": value_2 + "something",
								},
								{
									"variable": variable_3,
									"operator": "equal_to",
									"value": value_3,
								},
							]
						},
					],
				},
			],
			{},
			{
				variable_1: value_1,
				variable_2: value_2,
				variable_3: value_3,
			},
			"all",
		)

		assert not evaluate_conditional(
			[
				{
					"all": [
						{
							"variable": variable_1,
							"operator": "equal_to",
							"value": value_1,
						},
						{
							"any": [
								{
									"variable": variable_2,
									"operator": "equal_to",
									"value": value_2 + "something",
								},
								{
									"all": [
										{
											"variable": variable_1,
											"operator": "equal_to",
											"value": value_1,
										},
										{
											"variable": variable_3,
											"operator": "equal_to",
											"value": value_3 + 245152,
										},
									]
								},
							]
						},
					],
				},
			],
			{},
			{
				variable_1: value_1,
				variable_2: value_2,
				variable_3: value_3,
			},
			"any",
		)

class TestConditionalInputs:
	def test_invalid_categories(self):
		with pytest.raises(
			Exception,
			match='No values were found',
		):
			evaluate_condition(
				{
					"operator": "equal_to",
				},
				{},
				{},
			)

		with pytest.raises(
			Exception,
			match='"value" found',
		):
			evaluate_condition(
				{
					"value": "some value",
					"operator": "equal_to",
				},
				{},
				{},
			)

		with pytest.raises(
			Exception,
			match='"constant, value, variable" found',
		):
			evaluate_condition(
				{
					"value": "some value",
					"variable": "some variable",
					"constant": "some constant",
					"operator": "equal_to",
				},
				{},
				{},
			)