# Copyright (c) 2018. All rights reserved. OculusD.com, Inc. 
# This software is licensed under the LGPL license version 3 of 2007. A copy of
# the license should be included with this software, usually in a file called
# LICENSE.txt. If this is not the case, you can view the license online at
# https://www.gnu.org/licenses/lgpl-3.0.txt

from oculusd_utils import OculusDLogger, get_utc_timestamp
import pathlib
import os
from decimal import Decimal


L = OculusDLogger()


HOME = '{}{}'.format(str(pathlib.Path.home()), os.sep)
L.debug('HOME={}'.format(HOME))


class GenericIOProcessor:

    def process(self, data):
        raise Exception('Not yet implemented')


class GenericDataContainer:

    def __init__(self, result_set_name: str='anonymous', data_type: object=str):
        self.data = None
        self.data_type = data_type
        if data_type.__name__ == 'str':
            self.data = ''
        elif data_type.__name__ == 'list' or data_type.__name__ == 'tuple':
            self.data = list()
        elif data_type.__name__ == 'int':
            self.data = 0
        elif data_type.__name__ == 'float':
            self.data = 0.0
        elif data_type.__name__ == 'Decimal':
            self.data = Decimal('0.0')
        elif data_type.__name__ == 'dict':
            self.data = dict()
        else:
            raise Exception(
                'Data type "{}" was not found in the current supported types: {}'.format(
                    data_type.__name__,
                    ('str', 'list', 'tuple', 'int', 'float', 'Decimal', 'dict')
                )
            )

    def store(self, data: object, key: object=None)->int:
        if self.data_type.__name__ == 'dict':
            if key is None:
                raise Exception('Expected a key value but found None (data_type was set to dict)')
            if key in self.data:
                L.warning('Key "{}" already exists in dict - old value was replaced with new value'.format(key))
            self.data[key] = data
        elif self.data_type.__name__ == 'str':
            if data is None:
                self.data = None
            else:
                self.data = '{}'.format(data)
        elif self.data_type.__name__ == 'list':
            self.data.append(data)
        elif self.data_type.__name__ == 'tuple':
            if len(self.data) == 0 and type(self.data).__name__ == 'list':
                if type(data).__name__ == 'list':
                    self.data = data
                else:
                    self.data.append(data)
                self.data = tuple(self.data)
            else:
                L.error('Tuple already set. You have to create another GenericDataContainer instance to store another tuple')
        elif self.data_type.__name__ == 'int':
            if isinstance(data, str):
                self.data = int(float(data))
            elif isinstance(data, float):
                self.data = int(data)
            elif isinstance(data, int):
                self.data = data
            else:
                raise Exception('Could not convert input data to int')
        elif self.data_type.__name__ == 'float':
            if isinstance(data, str):
                self.data = float(data)
            elif isinstance(data, int):
                self.data = float(data)
            elif isinstance(data, float):
                self.data = data
            else:
                raise Exception('Could not convert input data to float')
        elif self.data_type.__name__ == 'Decimal':
            if isinstance(data, str) or isinstance(data, int) or isinstance(data, float):
                self.data = Decimal(data)
            elif isinstance(data, Decimal):
                self.data = data
            else:
                raise Exception('Could not convert input data to Decimal')


class GenericIO:

    def __init__(self, uri: str):
        self.uri = uri

    def read(self, read_processor: GenericIOProcessor=None, **kwarg)->GenericDataContainer:
        raise Exception('Not yet implemented')

    def write(self, data: GenericDataContainer, **kwarg):
        raise Exception('Not yet implemented')


class TextFileIO(GenericIO):

    def __init__(self, file_folder_path: str, file_name: str, cache_max_age: int=900, enable_cache: bool=False):
        # TODO: check that folder exists...
        self.cached_data = None
        self.cached_data_timestamp = 0
        self.cache_max_age = cache_max_age
        self.enable_cache = enable_cache
        super().__init__(
            uri='{}{}{}'.format(
                file_folder_path,
                os.sep,
                file_name
            )
        )

    def read(self, read_processor: GenericIOProcessor=None, **kwarg)->GenericDataContainer:
        """Read text data from a file

        :param read_processor: GenericIOProcessor that is not used in this function - whatever is supplied here will be ignored (for now)
        :param force: bool which is an optional argument. If the keyword is present, any cached data will be ignored

        :returns: GenericDataContainer
        """
        if self.enable_cache is True:
            now = get_utc_timestamp()
            if 'force' not in kwarg:
                if self.cached_data is not None and (now - self.cached_data_timestamp) < self.cache_max_age:
                    return self.cached_data
            self.cached_data = None
            self.cached_data_timestamp = 0
        data = GenericDataContainer(result_set_name=self.uri, data_type=str)
        data_str = ''
        with open(self.uri, 'r') as f:
            for line in f.readlines():
                if len(data_str) > 0:
                    data_str = '{}\n{}'.format(
                        data_str,
                        line.rstrip()
                    )
                else:
                    data_str = line
        data.store(data=data_str)
        if self.enable_cache is True:
            self.cached_data = data
            self.cached_data_timestamp = get_utc_timestamp()
        return data

    def write(self, data: GenericDataContainer, **kwarg):
        raise Exception('Not yet implemented')

# EOF
