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
