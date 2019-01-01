# Copyright (c) 2018. All rights reserved. OculusD.com, Inc. 
# This software is licensed under the LGPL license version 3 of 2007. A copy of
# the license should be included with this software, usually in a file called
# LICENSE.txt. If this is not the case, you can view the license online at
# https://www.gnu.org/licenses/lgpl-3.0.txt

"""
Usage with coverage:

::

    $ coverage run -m tests.test_logging
    $ coverage report -m
"""

import unittest
import logging
from oculusd_utils import OculusDLogger, DEBUG, formatter, get_utc_timestamp
from pathlib import Path
import os
import traceback


def remove_log_file(filename: str): 
    try:
        target_file = Path(filename)
        if target_file.is_file():
            os.remove(target_file)
    except: # pragma: no cover
        print('Skipped deleting of file "{}"'.format(filename))


class TestOculusDLogger(unittest.TestCase):

    def setUp(self):    
        self.logfile = 'logtest'
        remove_log_file(filename=self.logfile)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        ch = logging.FileHandler(filename=self.logfile)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def tearDown(self):
        remove_log_file(filename=self.logfile)  

    def test_init(self):
        test_logger = OculusDLogger(logger_impl=self.logger)
        test_logger.info('TEST')
        with open(self.logfile, 'r') as f:
            lines = f.readlines()
            print('CONTENT: {}'.format(lines))
            self.assertEqual(len(lines), 1)
        self.assertTrue(Path(self.logfile).is_file)

    def test_init_force_debug(self):
        test_logger = OculusDLogger(logger_impl=self.logger)
        test_logger.enable_debug()
        test_logger.debug('You should see this...')
        test_logger.info('TEST')
        with open(self.logfile, 'r') as f:
            lines = f.readlines()
            print('CONTENT: {}'.format(lines))
            self.assertEqual(len(lines), 2)
        self.assertTrue(Path(self.logfile).is_file)

    def test_verify_content_no_debug(self):
        test_logger = OculusDLogger(logger_impl=self.logger)
        test_logger.disable_debug()
        test_logger.debug('You should not see this...')
        test_logger.info('TEST')
        with open(self.logfile, 'r') as f:
            lines = f.readlines()
            print('CONTENT: {}'.format(lines))
            self.assertEqual(len(lines), 1)
            line1_elements = lines[0].split(' ')
            self.assertEqual(len(line1_elements), 6)
            self.assertFalse('test_verify_content_no_debug' in lines[0])
        self.assertTrue(Path(self.logfile).is_file)

    def test_verify_content_including_debug(self):
        test_logger = OculusDLogger(logger_impl=self.logger)
        test_logger.enable_debug()
        test_logger.info('TEST')
        with open(self.logfile, 'r') as f:
            lines = f.readlines()
            print('CONTENT: {}'.format(lines))
            self.assertEqual(len(lines), 1)
            line1_elements = lines[0].split(' ')
            self.assertEqual(len(line1_elements), 7)
            self.assertTrue('test_verify_content_including_debug' in lines[0])
        self.assertTrue(Path(self.logfile).is_file)

    def test_empty_message_logging(self):
        test_logger = OculusDLogger(logger_impl=self.logger)
        test_logger.info(message=None)
        last_line = ''
        with open(self.logfile, 'r') as f:
            lines = f.readlines()
            last_line = lines[-1]
        self.assertTrue('NO_INPUT_MESSAGE' in last_line)

    def test_warning_message_logging(self):
        test_logger = OculusDLogger(logger_impl=self.logger)
        test_logger.warning(message=None)
        last_line = ''
        with open(self.logfile, 'r') as f:
            lines = f.readlines()
            last_line = lines[-1]
        self.assertTrue('NO_INPUT_MESSAGE' in last_line)
        self.assertTrue('WARN' in last_line)

    def test_error_message_logging(self):
        test_logger = OculusDLogger(logger_impl=self.logger)
        test_logger.error(message=None)
        last_line = ''
        with open(self.logfile, 'r') as f:
            lines = f.readlines()
            last_line = lines[-1]
        self.assertTrue('NO_INPUT_MESSAGE' in last_line)
        self.assertTrue('ERR' in last_line)


class TestGetUtcTimestamp(unittest.TestCase):

    def test_get_utc_timestamp_without_decimal(self):
        ts = get_utc_timestamp()
        self.assertIsNotNone(ts)
        self.assertIsInstance(ts, int)
        self.assertTrue(ts>0)

    def test_get_utc_timestamp_with_decimal(self):
        ts = get_utc_timestamp(with_decimal=True)
        self.assertIsNotNone(ts)
        self.assertIsInstance(ts, float)
        self.assertTrue(ts>0.5)

if __name__ == '__main__':
    unittest.main()

# EOF
