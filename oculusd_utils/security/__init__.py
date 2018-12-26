# Copyright (c) 2018. All rights reserved. OculusD.com, Inc. 
# This software is licensed under the LGPL license version 3 of 2007. A copy of
# the license should be included with this software, usually in a file called
# LICENSE.txt. If this is not the case, you can view the license online at
# https://www.gnu.org/licenses/lgpl-3.0.txt

from oculusd_utils import OculusDLogger


L = OculusDLogger()


def mask_sensitive_string(
    input_str: str,
    mask_flag: bool=True,
    use_fixed_mask_length: bool=True,
    mask_length=8,
    mask_char: str='*',
    logger_impl: OculusDLogger=L
)->str:
    result = ''
    if input_str is not None:
        if not isinstance(input_str, str):
            input_str = '{}'.format(input_str)
        if len(input_str) > 0:
            if use_fixed_mask_length is True and mask_flag is True:
                result = '{}'.format(mask_char) * mask_length
            elif use_fixed_mask_length is False and mask_flag is True:
                result = '{}'.format(mask_char) * len(input_str)
            elif mask_flag is False:
                result = input_str
    else:
        logger_impl.error('input_str was None - returning empty string (trying to fail gracefully)')
        return ''
    logger_impl.debug('masking return string length: {}'.format(len(result)))
    return result

# EOF
