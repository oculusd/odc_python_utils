# Copyright (c) 2018. All rights reserved. OculusD.com, Inc. 
# This software is licensed under the LGPL license version 3 of 2007. A copy of
# the license should be included with this software, usually in a file called
# LICENSE.txt. If this is not the case, you can view the license online at
# https://www.gnu.org/licenses/lgpl-3.0.txt

"""
Usage with coverage:

::

    $ coverage run --omit="oculusd_utils/__init__.py"  -m tests.test_security
    $ coverage report -m
"""

import unittest
from oculusd_utils.security import mask_sensitive_string


class TestInitFunctions(unittest.TestCase):

    def setUp(self):
        self.str1 = 'aaa'
        self.str2 = 'aaa  bbb ccc ddd eee fff ggg hhh'
        self.default_mask = '*' * 8

    def test_mask_str1_defaults(self):
        result = mask_sensitive_string(input_str=self.str1)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertEqual(result, self.default_mask)
        self.assertFalse(self.str1 in result)

    def test_mask_none_string_defaults(self):
        number = 12345
        result = mask_sensitive_string(input_str=number)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertEqual(result, self.default_mask)

    def test_mask_str1_toggle_use_fixed_mask_length(self):
        result = mask_sensitive_string(input_str=self.str1, use_fixed_mask_length=False)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), len(self.str1))
        self.assertFalse(self.str1 in result)

    def test_mask_str2_toggle_use_fixed_mask_length(self):
        result = mask_sensitive_string(input_str=self.str2, use_fixed_mask_length=False)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), len(self.str2))
        self.assertFalse(self.str2 in result)

    def test_mask_str1_toggle_mask_flag(self):
        result = mask_sensitive_string(input_str=self.str1, mask_flag=False)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), len(self.str1))
        self.assertTrue(self.str1 in result)

    def test_mask_none_str(self):
        result = mask_sensitive_string(input_str=None)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertEqual(0, len(result))


if __name__ == '__main__':
    unittest.main()

# EOF
