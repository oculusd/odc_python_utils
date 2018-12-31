# Copyright (c) 2018. All rights reserved. OculusD.com, Inc. 
# This software is licensed under the LGPL license version 3 of 2007. A copy of
# the license should be included with this software, usually in a file called
# LICENSE.txt. If this is not the case, you can view the license online at
# https://www.gnu.org/licenses/lgpl-3.0.txt

"""
Usage with coverage:

::

    $ coverage run --omit="oculusd_utils/__init__.py","oculusd_utils/security/validation.py","oculusd_utils/security/__init__.py" -m tests.test_persistence
    $ coverage report -m
"""

import unittest
from oculusd_utils.persistence import GenericDataContainer, GenericIOProcessor, GenericIO, TextFileIO
from decimal import Decimal
from oculusd_utils.security.validation import DataValidator, L, StringDataValidator, NumberDataValidator


class DictValueNotNoneDataValidator(DataValidator):
    def __init__(self, logger=L):
        self.logger = logger

    def validate(self, data: object, **kwarg)->bool:
        if data is not None:
            return True
        self.logger.error('Data value must be set')
        return False


class TestGenericDataContainer(unittest.TestCase):

    def setUp(self):
        pass
        
    def test_init_generic_data_container(self):
        gdc = GenericDataContainer(result_set_name='Test')
        self.assertIsNotNone(gdc)
        self.assertIsInstance(gdc, GenericDataContainer)
        self.assertEqual('Test', gdc.result_set_name)
        self.assertIsInstance(gdc.data_type, type)
        self.assertEqual('str', gdc.data_type.__name__)
        self.assertIsNone(gdc.data_validator)

    def test_init_generic_data_container_list(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=list)
        self.assertEqual('list', gdc.data_type.__name__)

    def test_init_generic_data_container_tuple(self):
        # NOTE: Before a tuple is added (store() called), the data_type must be a list... Just roll with it!
        gdc = GenericDataContainer(result_set_name='Test', data_type=list)
        self.assertEqual('list', gdc.data_type.__name__)

    def test_init_generic_data_container_int(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=int)
        self.assertEqual('int', gdc.data_type.__name__)

    def test_init_generic_data_container_float(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=float)
        self.assertEqual('float', gdc.data_type.__name__)

    def test_init_generic_data_container_decimal(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=Decimal)
        self.assertEqual('Decimal', gdc.data_type.__name__)

    def test_init_generic_data_container_dict(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=dict)
        self.assertEqual('dict', gdc.data_type.__name__)

    def test_init_generic_data_container_unsupported_type(self):
        with self.assertRaises(Exception):
            gdc = GenericDataContainer(result_set_name='Test', data_type=self.__class__)

    def test_init_generic_data_container_invalid_validator(self):
        with self.assertRaises(Exception):
            gdc = GenericDataContainer(result_set_name='Test', data_validator='This must fail!')

    def test_generic_data_container_dict_test01(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=dict)
        self.assertEqual('dict', gdc.data_type.__name__)
        d = {
            'TestKey1': 1001,
            'TestKey2': 'Test Value',
            'TestKey3': Decimal('100'),
        }
        item_nr = 0
        for key, val in d.items():
            item_nr = item_nr + 1
            result = gdc.store(data=val, key=key)
            self.assertEqual(item_nr, result, 'Key "{}" failed to be added'.format(key))
            self.assertTrue(key in gdc.data, 'Key "{}" not found'.format(key))
        self.assertEqual(d['TestKey1'], gdc.data['TestKey1'])
        self.assertEqual(d['TestKey2'], gdc.data['TestKey2'])
        self.assertIsInstance(d['TestKey3'], Decimal)

    def test_generic_data_container_dict_omit_key_expect_exception(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=dict)
        with self.assertRaises(Exception):
            gdc.store(data='Unimportant Data')
    
    def test_generic_data_container_dict_override_key_with_new_value(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=dict)
        self.assertEqual('dict', gdc.data_type.__name__)
        d = {
            'TestKey1': 1001,
            'TestKey2': 'Test Value',
            'TestKey3': Decimal('100'),
        }
        for key, val in d.items():
            result = gdc.store(data=val, key=key)
        result = gdc.store(data='New Value', key='TestKey1')
        self.assertTrue(result == 3)
        self.assertEqual('New Value', gdc.data['TestKey1'])

    def test_generic_data_container_dict_with_custom_dict_data_validator(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=dict, data_validator=DictValueNotNoneDataValidator())
        self.assertEqual('dict', gdc.data_type.__name__)
        d = {
            'TestKey1': 1001,
            'TestKey2': 'Test Value',
            'TestKey3': Decimal('100'),
        }
        item_nr = 0
        for key, val in d.items():
            item_nr = item_nr + 1
            result = gdc.store(data=val, key=key)
            self.assertEqual(item_nr, result, 'Key "{}" failed to be added'.format(key))
            self.assertTrue(key in gdc.data, 'Key "{}" not found'.format(key))
        self.assertEqual(d['TestKey1'], gdc.data['TestKey1'])
        self.assertEqual(d['TestKey2'], gdc.data['TestKey2'])
        self.assertIsInstance(d['TestKey3'], Decimal)
    
    def test_generic_data_container_dict_with_custom_dict_data_validator_force_validation_exception(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=dict, data_validator=DictValueNotNoneDataValidator())
        self.assertEqual('dict', gdc.data_type.__name__)
        d = {
            'TestKey1': 1001,
            'TestKey2': 'Test Value',
            'TestKey3': Decimal('100'),
        }
        item_nr = 0
        for key, val in d.items():
            item_nr = item_nr + 1
            result = gdc.store(data=val, key=key)
        with self.assertRaises(Exception):
            gdc.store(data=None, key='TheInfamousAnyKey')

    def test_generic_data_container_dict_with_dict_validator_not_of_the_expected_type_must_raise_exception(self):
        with self.assertRaises(Exception):
            gdc = GenericDataContainer(result_set_name='Test', data_type=dict, data_validator='Definitely an invalid validator instance!')

    def test_generic_data_container_string_with_string_validator_and_invalid_string_must_raise_exception(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=str, data_validator=StringDataValidator())
        input_str = ' abc'
        with self.assertRaises(Exception):
            gdc.store(data=input_str, start_with_alpha=True)

    def test_generic_data_container_string_with_no_validator_and_valid_string(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=str)
        gdc.store(data='abc')
        self.assertIsNotNone(gdc.data)
        self.assertIsInstance(gdc.data, str)
        self.assertEqual('abc', gdc.data)

    def test_generic_data_container_string_with_no_validator_and_valid_none_store(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=str)
        gdc.store(data=None)
        self.assertIsNone(gdc.data)

    def test_generic_data_container_list_with_string_validator_and_valid_strings(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=list, data_validator=StringDataValidator())
        l = ['Item 1', 'Item 2']
        qty = 0
        for item in l:
            qty = qty + 1
            result = gdc.store(data=item, start_with_alpha=False)
            self.assertEqual(qty, result, 'Item "{}" failed to be stored'.format(qty))

    def test_generic_data_container_list_with_string_validator_and_one_invalid_object_must_raise_exception(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=list, data_validator=StringDataValidator())
        l = ['Item 1', 1, 'This item will be ignored']
        result = gdc.store(data=l[0], start_with_alpha=False)
        self.assertEqual(1, result)
        with self.assertRaises(Exception):
            result = gdc.store(data=l[1], start_with_alpha=False)

    def test_generic_data_container_list_no_validator_list_contains_various_types(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=list)
        l = ['Item 1', 1, Decimal('0.0')]
        qty = 0
        for item in l:
            qty = qty + 1
            result = gdc.store(data=item, start_with_alpha=False)
            self.assertEqual(qty, result, 'Item "{}" failed to be stored'.format(qty))

    def test_generic_data_container_tuple_with_string_validator_and_valid_strings(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=tuple, data_validator=StringDataValidator())
        l = ('Item 1', 'Item 2', )
        result = gdc.store(data=l, start_with_alpha=False)
        self.assertEqual(len(l), result, 'Item "{}" failed to be stored'.format(len(l)))

    def test_generic_data_container_tuple_with_string_validator_and_null_data_expecting_exception(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=tuple, data_validator=StringDataValidator())
        with self.assertRaises(Exception):
            gdc.store(data=None, start_with_alpha=False)

    def test_generic_data_container_tuple_with_string_validator_and_unsupported_data_expecting_exception(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=tuple, data_validator=StringDataValidator())
        with self.assertRaises(Exception):
            gdc.store(data='This must fail', start_with_alpha=False)

    def test_generic_data_container_tuple_with_string_validator_and_data_validation_fail_expecting_exception(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=tuple, data_validator=StringDataValidator())
        l = ('Item 1', 'Item 2', 3, )
        with self.assertRaises(Exception):
            gdc.store(data=l, start_with_alpha=False)

    def test_generic_data_container_tuple_with_no_validator_and_valid_list(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=tuple)
        l = ['Item 1', 'Item 2', ]
        result = gdc.store(data=l, start_with_alpha=False)
        self.assertEqual(len(l), result, 'Item "{}" failed to be stored'.format(len(l)))

    def test_generic_data_container_tuple_with_no_validator_and_valid_list_add_another_item_expecting_exception(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=tuple)
        l = ['Item 1', 'Item 2', ]
        l2 = ['Item 3', 'Item 4', ]
        result = gdc.store(data=l, start_with_alpha=False)
        with self.assertRaises(Exception):
            gdc.store(data=l2, start_with_alpha=False)

    def test_generic_data_container_int_with_no_validator_and_valid_int(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=int)
        l = 1001
        result = gdc.store(data=l)
        self.assertEqual(1, result)

    def test_generic_data_container_int_with_validator_and_invalid_int_value(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=int, data_validator=NumberDataValidator())
        l = 1001
        with self.assertRaises(Exception):
            gdc.store(data=l, min_value=2000, max_value=3000)

    def test_generic_data_container_int_with_no_validator_and_invalid_input_type(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=int, data_validator=NumberDataValidator())
        l = 1001
        with self.assertRaises(Exception):
            gdc.store(data=Decimal(l), min_value=2000, max_value=3000)

    def test_generic_data_container_int_with_no_validator_and_valid_int_as_str(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=int)
        l = '1001'
        result = gdc.store(data=l)
        self.assertEqual(1, result)

    def test_generic_data_container_int_with_no_validator_and_valid_int_as_float(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=int)
        l = 1001.0
        result = gdc.store(data=l)
        self.assertEqual(1, result)

    def test_generic_data_container_float_with_no_validator_and_valid_float(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=float)
        l = 1001.01
        result = gdc.store(data=l)
        self.assertEqual(1, result)

    def test_generic_data_container_float_with_no_validator_and_valid_float_as_str(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=float)
        l = '1001.01'
        result = gdc.store(data=l)
        self.assertEqual(1, result)

    def test_generic_data_container_float_with_no_validator_and_valid_float_as_int(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=float)
        l = 1001
        result = gdc.store(data=l)
        self.assertEqual(1, result)

    def test_generic_data_container_float_with_no_validator_and_invalid_input_type(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=float)
        l = Decimal(1001)
        with self.assertRaises(Exception):
            gdc.store(data=l)

    def test_generic_data_container_float_with_validator_and_valid_float(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=float, data_validator=NumberDataValidator())
        l = 1001.001
        result = gdc.store(data=l, min_value=0.0, max_value=9999.0)
        self.assertEqual(1, result)

    def test_generic_data_container_float_with_validator_and_invalid_float_expect_exception(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=float, data_validator=NumberDataValidator())
        l = 1001.001
        with self.assertRaises(Exception):
            gdc.store(data=l, min_value=5555.0, max_value=9999.0)

    def test_generic_data_container_int_with_invalid_validator_expect_exception(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=int, data_validator=StringDataValidator())
        l = 1001
        with self.assertRaises(Exception):
            gdc.store(data=l, min_value=0, max_value=3000)

    def test_generic_data_container_float_with_invalid_validator_expect_exception(self):
        gdc = GenericDataContainer(result_set_name='Test', data_type=float, data_validator=StringDataValidator())
        l = 1001.001
        with self.assertRaises(Exception):
            gdc.store(data=l, min_value=0.0, max_value=3000.0)


class TestGenericIOProcessor(unittest.TestCase):

    def test_init_generic_io_processor(self):
        self.fail('No test code implemented yet')


class TestGenericIO(unittest.TestCase):

    def test_init_generic_io(self):
        self.fail('No test code implemented yet')


class TestTextFileIO(unittest.TestCase):

    def test_init_text_file_io(self):
        self.fail('No test code implemented yet')


# EOF
