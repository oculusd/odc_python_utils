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

# EOF
