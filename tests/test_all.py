# Copyright (c) 2018. All rights reserved. OculusD.com, Inc. 
# This software is licensed under the LGPL license version 3 of 2007. A copy of
# the license should be included with this software, usually in a file called
# LICENSE.txt. If this is not the case, you can view the license online at
# https://www.gnu.org/licenses/lgpl-3.0.txt

"""Testing all domain aggregates

Depends on the Python package "coverage"

Usage

::

    $ coverage run  --omit="*tests*" -m tests.test_all
    $ coverage report -m
"""

import unittest
from tests.test_logging import TestOculusDLogger
from tests.test_security import TestInitFunctions
from tests.test_validation import TestEmailValidation, TestStringValidation


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

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

# EOF