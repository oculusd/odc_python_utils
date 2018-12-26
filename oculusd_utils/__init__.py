# Copyright (c) 2018. All rights reserved. OculusD.com, Inc. 
# This software is licensed under the LGPL license version 3 of 2007. A copy of
# the license should be included with this software, usually in a file called
# LICENSE.txt. If this is not the case, you can view the license online at
# https://www.gnu.org/licenses/lgpl-3.0.txt

import logging
import os
import traceback
import inspect


DEBUG = os.getenv('DEBUG', None)
if DEBUG is not None: # pragma: no cover
    DEBUG = True
else:
    DEBUG = False


def get_logging_level():
    if DEBUG is True:   # pragma: no cover
        return logging.DEBUG
    else:
        return logging.INFO


logger = logging.getLogger(__name__)
logger.setLevel(get_logging_level())

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(get_logging_level())

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


def id_caller()->list:
    result = list()
    try:
        caller_stack = inspect.stack()[2]
        result.append(caller_stack[1].split(os.sep)[-1]) # File name
        result.append(caller_stack[2]) # line number
        result.append(caller_stack[3]) # function name
    except: # pragma: no cover
        pass
    return result


class OculusDLogger:
    """
    A Python log wrapper class to make things a little easier
    """
    def __init__(self, logger_impl=logger):
        """
        General usage:

            >>> from oculusd_utils import OculusDLogger
               .
               .
            >>> app_logger = OculusDLogger()
            >>> app_logger.info('some message')

        Enabling DEBUG mode can be accomplished in two ways:

            Method 1: Environment Variable

                $ export DEBUG=1

            Method 2: Programmatically  

                >>> app_logger.enable_debug()

        When DEBUG mode is enabled via an environmental variable, you can programmatically disable it again:

            >>> app_logger.disable_debug()

        What does DEBUG mode do? Apart from enabling the Python logger DEBUG level mode, it will also add some 
        additional stack information to ALL log messages that include the calling file name, function and line number 
        details.

        Remember that no matter how you set-up your custom logger, when enabling DEBUG mode, the abbreviated stack 
        information will be added to ALL messages regardless, just infrom of the actual message enclosed in square 
        brackets.
        """
        self.logger = logger_impl
        self.debug_flag = DEBUG

    def _format_msg(self, stack_data: list, message: str)->str:
        if message is not None:
            message = '{}'.format(message)
            if len(stack_data) == 3:
                if self.debug_flag is True:
                    message = '[{}:{}:{}] {}'.format(
                        stack_data[0],
                        stack_data[1],
                        stack_data[2],
                        message
                    )
            return message
        return 'NO_INPUT_MESSAGE'

    def enable_debug(self):
        self.logger.setLevel(logging.DEBUG)
        for handler in self.logger.handlers:
            handler.setLevel(logging.DEBUG)
        self.debug_flag = True

    def disable_debug(self):
        self.logger.setLevel(logging.INFO)
        for handler in self.logger.handlers:
            handler.setLevel(logging.INFO)
        self.debug_flag = False

    def info(self, message: str):
        message = self._format_msg(stack_data=id_caller(), message=message)
        self.logger.info(message)

    def debug(self, message: str):
        if self.debug_flag is True:
            message = self._format_msg(stack_data=id_caller(), message=message)
            self.logger.debug(message)

    def warning(self, message: str):
        message = self._format_msg(stack_data=id_caller(), message=message)
        self.logger.warning(message)
    
    def error(self, message: str):
        message = self._format_msg(stack_data=id_caller(), message=message)
        self.logger.error(message)

# EOF
