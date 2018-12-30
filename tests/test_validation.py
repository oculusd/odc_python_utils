# Copyright (c) 2018. All rights reserved. OculusD.com, Inc. 
# This software is licensed under the LGPL license version 3 of 2007. A copy of
# the license should be included with this software, usually in a file called
# LICENSE.txt. If this is not the case, you can view the license online at
# https://www.gnu.org/licenses/lgpl-3.0.txt

"""
Usage with coverage:

::

    $ coverage run --omit="*tests*","oculusd_utils/__init__.py,oculusd_utils/persistence/__init__.py,oculusd_utils/security/__init__.py" -m tests.test_validation
    $ coverage report -m
"""

import unittest
from oculusd_utils.security.validation import is_valid_email, validate_string, DataValidator, StringDataValidator, NumberDataValidator
from oculusd_utils.persistence import GenericDataContainer
import random


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


class TestDataValidator(unittest.TestCase):

    def setUp(self):
        self.short_str = 'abc'

    def test_init_data_validator(self):
        dv = DataValidator()
        self.assertIsNotNone(dv)
        self.assertIsInstance(dv, DataValidator)

    def test_validation_fails(self):
        dv = DataValidator()
        result = dv.validate(data=self.short_str)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)


class TestStringDataValidator(unittest.TestCase):

    def setUp(self):
        self.short_str = 'abc'

    def test_init_string_data_validator(self):
        sdv = StringDataValidator()
        self.assertIsNotNone(sdv)
        self.assertIsInstance(sdv, DataValidator)
        self.assertIsInstance(sdv, StringDataValidator)

    def test_string_data_validator_short_string_all_defaults(self):
        sdv = StringDataValidator()
        result = sdv.validate(data=self.short_str)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)

    def test_string_data_validator_data_container_all_defaults(self):
        self.data_container = GenericDataContainer(result_set_name='Test', data_type=str, data_validator=StringDataValidator())
        result = self.data_container.store(data=self.short_str)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, int)
        self.assertEqual(len(self.short_str), result)

    def test_string_data_validator_short_string_with_min_and_max_lengths(self):
        sdv = StringDataValidator()
        result = sdv.validate(data=self.short_str, min_length=2, max_length=5)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)

    def test_string_data_validator_short_string_with_min_and_max_lengths_fail_string_to_short(self):
        sdv = StringDataValidator()
        result = sdv.validate(data=self.short_str, min_length=4, max_length=10)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)

    def test_string_data_validator_short_string_with_min_and_max_lengths_fail_string_to_long(self):
        sdv = StringDataValidator()
        result = sdv.validate(data=self.short_str, min_length=1, max_length=2)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)

    def test_string_data_validator_short_string_with_start_with_alpha(self):
        sdv = StringDataValidator()
        result = sdv.validate(data=self.short_str, min_length=2, max_length=5)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)

    def test_string_data_validator_short_string_with_start_with_alpha_but_start_with_space(self):
        sdv = StringDataValidator()
        result = sdv.validate(data=' {}'.format(self.short_str), start_with_alpha=True)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)

    def test_string_data_validator_short_string_with_start_with_alpha_and_start_with_space(self):
        sdv = StringDataValidator()
        result = sdv.validate(data=' {}'.format(self.short_str), start_with_alpha=False)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)

    def test_string_data_validator_short_string_with_start_with_alpha_but_start_with_numeric(self):
        sdv = StringDataValidator()
        result = sdv.validate(data='1{}'.format(self.short_str), start_with_alpha=True)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)

    def test_string_data_validator_short_string_with_can_be_none_is_true(self):
        sdv = StringDataValidator()
        result = sdv.validate(data=self.short_str, can_be_none=True)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)

    def test_string_data_validator_none_value_with_can_be_none_is_true(self):
        sdv = StringDataValidator()
        result = sdv.validate(data=None, can_be_none=True)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)

    def test_string_data_validator_short_string_with_contain_at_least_one_space(self):
        sdv = StringDataValidator()
        result = sdv.validate(data=' {}'.format(self.short_str), contain_at_least_one_space=True, start_with_alpha=False)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)

    def test_string_data_validator_none_value_with_contain_at_least_one_space_but_doesnt(self):
        sdv = StringDataValidator()
        result = sdv.validate(data=self.short_str, contain_at_least_one_space=True)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)


class TestNumberDataValidator(unittest.TestCase):

    def setUp(self):
        self.positive_float = random.uniform(0.0, 100.5)
        self.negative_float = random.uniform(-0.00001, -100.5)
        self.positive_int = random.randint(0, 1000)
        self.negative_int = random.randint(0, 1000) * -1
        self.float_as_str = '{}'.format(self.positive_float)

    def test_init_number_data_validator(self):
        v = NumberDataValidator()
        self.assertIsNotNone(v)
        self.assertIsInstance(v, NumberDataValidator)

    def test_number_data_validator_int_input_no_validator_params(self):
        v = NumberDataValidator()
        result_pos_number = v.validate(data=self.positive_int)
        self.assertIsNotNone(result_pos_number)
        self.assertIsInstance(result_pos_number, bool)
        self.assertTrue(result_pos_number)
        result_neg_number = v.validate(data=self.negative_int)
        self.assertIsNotNone(result_neg_number)
        self.assertIsInstance(result_neg_number, bool)
        self.assertTrue(result_neg_number)
        result_zero = v.validate(data=0)
        self.assertIsNotNone(result_zero)
        self.assertIsInstance(result_zero, bool)
        self.assertTrue(result_zero)

    def test_number_data_validator_int_input_with_validator_params_expect_pass(self):
        v = NumberDataValidator()
        result_pos_number = v.validate(data=self.positive_int, min_value=self.positive_int-1, max_value=self.positive_int+1)
        self.assertIsNotNone(result_pos_number)
        self.assertIsInstance(result_pos_number, bool)
        self.assertTrue(result_pos_number)

    def test_number_data_validator_float_input_no_validator_params(self):
        v = NumberDataValidator()
        result_pos_number = v.validate(data=self.positive_float)
        self.assertIsNotNone(result_pos_number)
        self.assertIsInstance(result_pos_number, bool)
        self.assertTrue(result_pos_number)
        result_neg_number = v.validate(data=self.positive_float)
        self.assertIsNotNone(result_neg_number)
        self.assertIsInstance(result_neg_number, bool)
        self.assertTrue(result_neg_number)
        result_zero = v.validate(data=0.0)
        self.assertIsNotNone(result_zero)
        self.assertIsInstance(result_zero, bool)
        self.assertTrue(result_zero)

    def test_number_data_validator_float_input_with_validator_params_expect_pass(self):
        v = NumberDataValidator()
        result_pos_number = v.validate(data=self.positive_float, min_value=self.positive_float-0.0001, max_value=self.positive_float+0.0001)
        self.assertIsNotNone(result_pos_number)
        self.assertIsInstance(result_pos_number, bool)
        self.assertTrue(result_pos_number)
        

if __name__ == '__main__':
    unittest.main()

# EOF
