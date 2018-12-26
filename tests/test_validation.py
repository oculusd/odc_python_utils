# Copyright (c) 2018. All rights reserved. OculusD.com, Inc. 
# This software is licensed under the LGPL license version 3 of 2007. A copy of
# the license should be included with this software, usually in a file called
# LICENSE.txt. If this is not the case, you can view the license online at
# https://www.gnu.org/licenses/lgpl-3.0.txt

"""
Usage with coverage:

::

    $ coverage run --omit="oculusd_utils/__init__.py,oculusd_utils/security/__init__.py"  -m tests.test_validation
    $ coverage report -m
"""

import unittest
from oculusd_utils.security.validation import is_valid_email, validate_string


class TestEmailValidation(unittest.TestCase):

    def setUp(self):
        self.valid_email_address = 'user1@example.tld'
        self.invalid_email_address_1 = 'user2'
        self.invalid_email_address_2 = 'user2@example'
        self.invalid_email_address_3 = 'user2@example .tld'

    def test_validation_valid_email_address(self):
        result = is_valid_email(email=self.valid_email_address)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)

    def test_validation_invalid_email_address_1(self):
        result = is_valid_email(email=self.invalid_email_address_1)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)

    def test_validation_invalid_email_address_2(self):
        result = is_valid_email(email=self.invalid_email_address_2)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)

    def test_validation_invalid_email_address_3(self):
        result = is_valid_email(email=self.invalid_email_address_3)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)


class TestStringValidation(unittest.TestCase):

    def setUp(self):
        self.short_str = 'abc'
    
    def test_validate_string_short_str_defaults(self):
        result = validate_string(input_str=self.short_str)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)

    def test_validate_string_can_be_none_and_is_none(self):
        result = validate_string(input_str=None, can_be_none=True)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)

    def test_validate_string_can_not_be_none_and_is_none(self):
        result = validate_string(input_str=None)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)

    def test_validate_string_not_a_string_instance(self):
        result = validate_string(input_str=[1, 2])
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)

    def test_validate_string_less_than_minimum_len(self):
        result = validate_string(input_str=self.short_str, min_length=len(self.short_str) + 1)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)

    def test_validate_string_greater_than_maximum_len(self):
        result = validate_string(input_str=self.short_str, max_length=len(self.short_str) - 1)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)

    def test_validate_string_does_not_start_with_alpha_but_with_space(self):
        result = validate_string(input_str=' {}'.format(self.short_str), start_with_alpha=True)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)

    def test_validate_string_fail_to_contain_at_least_one_space(self):
        result = validate_string(input_str=self.short_str, contain_at_least_one_space=True)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)

    def test_validate_string_contains_at_least_one_space(self):
        result = validate_string(input_str=' {}'.format(self.short_str), contain_at_least_one_space=True, start_with_alpha=False)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()

# EOF
