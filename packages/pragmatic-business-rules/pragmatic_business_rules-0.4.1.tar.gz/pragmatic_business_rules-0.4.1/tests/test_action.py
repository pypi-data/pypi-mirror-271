from src.pragmatic_business_rules.action import apply_actions_to_variables, apply_action_to_item
import pytest


class TestApplyActionToValue:

	def test_assert_single_action(self):
		action = {"set": 1, "something_else": 2}

		with pytest.raises(
			Exception,
			match="Too many actions '{}' were specified".format(
				", ".join(action.keys())
			),
		):
			apply_action_to_item(action, "unknown key", 0)

	def test_assert_action_type(self):
		invalid_action = "unknown"

		with pytest.raises(
			Exception,
			match=f"Unexpected '{invalid_action}' action was specified",
		):
			apply_action_to_item({invalid_action: 1}, "unknown key", 0)

	def test_assert_comparable_item_type(self):
		invalid_item = "some item"
		original_value = 0
		new_value = "asd"

		with pytest.raises(
			Exception,
			match='\\("{}", "{}", {}\\) and \\("{}", {}\\)'.format(
				invalid_item,
				original_value,
				type(original_value).__name__,
				new_value,
				type(new_value).__name__,
			),
		):
			apply_action_to_item({"set": new_value}, invalid_item, original_value)


class TestApplyActionToVariables:

	def test_assert_item_defined_in_variables(self):
		item = "some key"

		with pytest.raises(
			Exception,
			match=f"The key '{item}' is not defined in the variables object"
		):
			apply_actions_to_variables(
				{
					item: {
						"set": 10
					},
				},
				{},
			)
