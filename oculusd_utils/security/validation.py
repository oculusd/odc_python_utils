# Copyright (c) 2018. All rights reserved. OculusD.com, Inc. 
# This software is licensed under the LGPL license version 3 of 2007. A copy of
# the license should be included with this software, usually in a file called
# LICENSE.txt. If this is not the case, you can view the license online at
# https://www.gnu.org/licenses/lgpl-3.0.txt

import re
import traceback
from oculusd_utils import OculusDLogger


L = OculusDLogger()


def is_valid_email(email):
    L.debug('email={}'.format(email))   # pragma: no cover
    if ' ' in email:
        return False
    if len(email) > 7:
        if re.match("[^@]+@[^@]+\.[^@]+", email) is not None:
            return True
    return False


def validate_string(
        input_str: str,
        min_length: int=1,
        max_length: int=255,
        start_with_alpha: bool=True,
        contain_at_least_one_space: bool=False,
        can_be_none: bool=False
) -> bool:
    if input_str is None:
        if can_be_none is True:
            return True
        return False
    if not isinstance(input_str, str):
        return False
    if len(input_str) < min_length:
        return False
    if len(input_str) > max_length:
        return False
    if start_with_alpha:
        if len(input_str) > 0:
            if not input_str[0].isalpha():
                return False
    if contain_at_least_one_space:
        if ' ' not in input_str:
            return False
    return True


class DataValidator:
    """The DataValidator base class must be extended with specific data type validation classes
    """

    def __init__(self, logger=L):
        """Initialise with an optional logger

        :param logger: OculusDLogger (default=OculusDLogger())
        """
        self.logger = logger

    def validate(self, data: object, **kwarg)->bool:
        """This method must be implemented/overridden by the class extending from this base class.

        :param data: object containing data to be validated
        
        :returns: bool with True mening validation passed and False meaning validation failed (do not trust the data!)
        """
        self.logger.error('You need to implement the logic for this method! Fail safely principle applied - returning False')
        return False


class StringDataValidator(DataValidator):

    def __init__(self, logger=L):
        super().__init__(logger=logger)

    def validate(self, data: object, **kwarg)->bool:
        """Checks against def validate_string()

        Optional keyword arguments with the default values:
            min_length: int=1,
            max_length: int=255,
            start_with_alpha: bool=True,
            contain_at_least_one_space: bool=False,
            can_be_none: bool=False
        """
        min_length = 1
        max_length = 255
        start_with_alpha = True
        contain_at_least_one_space = False
        can_be_none = False
        if 'min_length' in kwarg:
            min_length = kwarg['min_length']
            self.logger.debug('min_length set in kwarg - value: "{}"'.format(min_length))
        if 'max_length' in kwarg:
            max_length = kwarg['max_length']
            self.logger.debug('max_length set in kwarg - value: "{}"'.format(max_length))
        if 'start_with_alpha' in kwarg:
            start_with_alpha = kwarg['start_with_alpha']
            self.logger.debug('start_with_alpha set in kwarg - value: "{}"'.format(start_with_alpha))
        if 'contain_at_least_one_space' in kwarg:
            contain_at_least_one_space = kwarg['contain_at_least_one_space']
            self.logger.debug('contain_at_least_one_space set in kwarg - value: "{}"'.format(contain_at_least_one_space))
        if 'can_be_none' in kwarg:
            can_be_none = kwarg['can_be_none']
            self.logger.debug('can_be_none set in kwarg - value: "{}"'.format(can_be_none))
        return validate_string(
            input_str=data,
            min_length=min_length,
            max_length=max_length,
            start_with_alpha=start_with_alpha,
            contain_at_least_one_space=contain_at_least_one_space,
            can_be_none=can_be_none
        )


# EOF
