# Copyright (c) 2018. All rights reserved. OculusD.com, Inc. 
# This software is licensed under the LGPL license version 3 of 2007. A copy of
# the license should be included with this software, usually in a file called
# LICENSE.txt. If this is not the case, you can view the license online at
# https://www.gnu.org/licenses/lgpl-3.0.txt

"""Testing all domain aggregates

Depends on the Python package "coverage"

Usage

::

    $ coverage run  --omit="*tests*","oculusd_utils/__init__.py" -m tests.test_all
    $ coverage report -m
"""

import unittest
from tests.test_logging import TestOculusDLogger
from tests.test_security import TestInitFunctions
from tests.test_validation import TestEmailValidation, TestStringValidation, TestDataValidator, TestStringDataValidator, TestNumberDataValidator
from tests.test_persistence import TestGenericDataContainer, TestGenericIOProcessor, TestGenericIO, TestTextFileIO


def suite():
    suite = unittest.TestSuite()

    suite.addTest(TestOculusDLogger('test_init'))
    suite.addTest(TestOculusDLogger('test_init_force_debug'))
    suite.addTest(TestOculusDLogger('test_verify_content_no_debug'))
    suite.addTest(TestOculusDLogger('test_verify_content_including_debug'))
    suite.addTest(TestOculusDLogger('test_empty_message_logging'))
    suite.addTest(TestOculusDLogger('test_warning_message_logging'))
    suite.addTest(TestOculusDLogger('test_error_message_logging'))

    suite.addTest(TestInitFunctions('test_mask_str1_defaults'))
    suite.addTest(TestInitFunctions('test_mask_none_string_defaults'))
    suite.addTest(TestInitFunctions('test_mask_str1_toggle_use_fixed_mask_length'))
    suite.addTest(TestInitFunctions('test_mask_str2_toggle_use_fixed_mask_length'))
    suite.addTest(TestInitFunctions('test_mask_str1_toggle_mask_flag'))
    suite.addTest(TestInitFunctions('test_mask_none_str'))

    suite.addTest(TestEmailValidation('test_validation_valid_email_address'))
    suite.addTest(TestEmailValidation('test_validation_invalid_email_address_1'))
    suite.addTest(TestEmailValidation('test_validation_invalid_email_address_2'))
    suite.addTest(TestEmailValidation('test_validation_invalid_email_address_3'))

    suite.addTest(TestStringValidation('test_validate_string_short_str_defaults'))
    suite.addTest(TestStringValidation('test_validate_string_can_be_none_and_is_none'))
    suite.addTest(TestStringValidation('test_validate_string_can_not_be_none_and_is_none'))
    suite.addTest(TestStringValidation('test_validate_string_not_a_string_instance'))
    suite.addTest(TestStringValidation('test_validate_string_less_than_minimum_len'))
    suite.addTest(TestStringValidation('test_validate_string_greater_than_maximum_len'))
    suite.addTest(TestStringValidation('test_validate_string_does_not_start_with_alpha_but_with_space'))
    suite.addTest(TestStringValidation('test_validate_string_fail_to_contain_at_least_one_space'))
    suite.addTest(TestStringValidation('test_validate_string_contains_at_least_one_space'))

    suite.addTest(TestDataValidator('test_init_data_validator'))
    suite.addTest(TestDataValidator('test_validation_fails'))

    suite.addTest(TestStringDataValidator('test_init_string_data_validator'))
    suite.addTest(TestStringDataValidator('test_string_data_validator_short_string_all_defaults'))
    suite.addTest(TestStringDataValidator('test_string_data_validator_data_container_all_defaults'))
    suite.addTest(TestStringDataValidator('test_string_data_validator_short_string_with_min_and_max_lengths'))
    suite.addTest(TestStringDataValidator('test_string_data_validator_short_string_with_min_and_max_lengths_fail_string_to_short'))
    suite.addTest(TestStringDataValidator('test_string_data_validator_short_string_with_min_and_max_lengths_fail_string_to_long'))
    suite.addTest(TestStringDataValidator('test_string_data_validator_short_string_with_start_with_alpha'))
    suite.addTest(TestStringDataValidator('test_string_data_validator_short_string_with_start_with_alpha_but_start_with_space'))
    suite.addTest(TestStringDataValidator('test_string_data_validator_short_string_with_start_with_alpha_but_start_with_numeric'))
    suite.addTest(TestStringDataValidator('test_string_data_validator_short_string_with_can_be_none_is_true'))
    suite.addTest(TestStringDataValidator('test_string_data_validator_none_value_with_can_be_none_is_true'))
    suite.addTest(TestStringDataValidator('test_string_data_validator_short_string_with_contain_at_least_one_space'))
    suite.addTest(TestStringDataValidator('test_string_data_validator_none_value_with_contain_at_least_one_space_but_doesnt'))
    suite.addTest(TestStringDataValidator('test_string_data_validator_short_string_with_start_with_alpha_and_start_with_space'))

    suite.addTest(TestGenericDataContainer('test_init_generic_data_container'))
    suite.addTest(TestGenericDataContainer('test_init_generic_data_container_list'))
    suite.addTest(TestGenericDataContainer('test_init_generic_data_container_tuple'))
    suite.addTest(TestGenericDataContainer('test_init_generic_data_container_int'))
    suite.addTest(TestGenericDataContainer('test_init_generic_data_container_float'))
    suite.addTest(TestGenericDataContainer('test_init_generic_data_container_decimal'))
    suite.addTest(TestGenericDataContainer('test_init_generic_data_container_dict'))
    suite.addTest(TestGenericDataContainer('test_init_generic_data_container_unsupported_type'))
    suite.addTest(TestGenericDataContainer('test_init_generic_data_container_invalid_validator'))
    suite.addTest(TestGenericDataContainer('test_generic_data_container_dict_test01'))
    suite.addTest(TestGenericDataContainer('test_generic_data_container_dict_omit_key_expect_exception'))
    suite.addTest(TestGenericDataContainer('test_generic_data_container_dict_override_key_with_new_value'))
    suite.addTest(TestGenericDataContainer('test_generic_data_container_dict_with_custom_dict_data_validator'))
    suite.addTest(TestGenericDataContainer('test_generic_data_container_dict_with_custom_dict_data_validator_force_validation_exception'))
    suite.addTest(TestGenericDataContainer('test_generic_data_container_dict_with_dict_validator_not_of_the_expected_type_must_raise_exception'))
    suite.addTest(TestGenericDataContainer('test_generic_data_container_string_with_string_validator_and_invalid_string_must_raise_exception'))
    suite.addTest(TestGenericDataContainer('test_generic_data_container_string_with_no_validator_and_valid_string'))
    suite.addTest(TestGenericDataContainer('test_generic_data_container_string_with_no_validator_and_valid_none_store'))
    suite.addTest(TestGenericDataContainer('test_generic_data_container_list_with_string_validator_and_valid_strings'))
    suite.addTest(TestGenericDataContainer('test_generic_data_container_list_with_string_validator_and_one_invalid_object_must_raise_exception'))
    suite.addTest(TestGenericDataContainer('test_generic_data_container_list_no_validator_list_contains_various_types'))
    suite.addTest(TestGenericDataContainer('test_generic_data_container_tuple_with_string_validator_and_valid_strings'))
    suite.addTest(TestGenericDataContainer('test_generic_data_container_tuple_with_string_validator_and_null_data_expecting_exception'))
    suite.addTest(TestGenericDataContainer('test_generic_data_container_tuple_with_string_validator_and_unsupported_data_expecting_exception'))
    suite.addTest(TestGenericDataContainer('test_generic_data_container_tuple_with_string_validator_and_data_validation_fail_expecting_exception'))
    suite.addTest(TestGenericDataContainer('test_generic_data_container_tuple_with_no_validator_and_valid_list'))
    suite.addTest(TestGenericDataContainer('test_generic_data_container_tuple_with_no_validator_and_valid_list_add_another_item_expecting_exception'))
    suite.addTest(TestGenericDataContainer('test_generic_data_container_int_with_no_validator_and_valid_int'))

    suite.addTest(TestGenericIOProcessor('test_init_generic_io_processor'))

    suite.addTest(TestGenericIO('test_init_generic_io'))

    suite.addTest(TestTextFileIO('test_init_text_file_io'))

    suite.addTest(TestNumberDataValidator('test_init_number_data_validator'))
    suite.addTest(TestNumberDataValidator('test_number_data_validator_int_input_no_validator_params'))
    suite.addTest(TestNumberDataValidator('test_number_data_validator_int_input_with_validator_params_expect_pass'))
    suite.addTest(TestNumberDataValidator('test_number_data_validator_float_input_no_validator_params'))
    suite.addTest(TestNumberDataValidator('test_number_data_validator_float_input_with_validator_params_expect_pass'))
    suite.addTest(TestNumberDataValidator('test_number_data_validator_str_input_no_validator_params'))
    suite.addTest(TestNumberDataValidator('test_number_data_validator_str_input_with_validator_params_expect_pass'))
    suite.addTest(TestNumberDataValidator('test_number_data_validator_decimal_input_no_validator_params'))
    suite.addTest(TestNumberDataValidator('test_number_data_validator_decimal_input_with_validator_params_expect_pass'))
    suite.addTest(TestNumberDataValidator('test_number_data_validator_decimal_input_with_invalid_validator_params_expect_fail'))
    suite.addTest(TestNumberDataValidator('test_number_data_validator_decimal_input_with_validator_params_expect_fail_input_less_than_min_value'))
    suite.addTest(TestNumberDataValidator('test_number_data_validator_decimal_input_with_validator_params_expect_fail_input_greater_than_max_value'))
    suite.addTest(TestNumberDataValidator('test_number_data_validator_int_input_with_validator_params_expect_fail_input_less_than_min_value'))
    suite.addTest(TestNumberDataValidator('test_number_data_validator_int_input_with_validator_params_expect_fail_input_greater_than_max_value'))
    suite.addTest(TestNumberDataValidator('test_number_data_validator_invalid_number_expect_fail'))

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

# EOF
