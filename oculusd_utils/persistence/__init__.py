# Copyright (c) 2018. All rights reserved. OculusD.com, Inc. 
# This software is licensed under the LGPL license version 3 of 2007. A copy of
# the license should be included with this software, usually in a file called
# LICENSE.txt. If this is not the case, you can view the license online at
# https://www.gnu.org/licenses/lgpl-3.0.txt

from oculusd_utils import OculusDLogger, get_utc_timestamp
from oculusd_utils.security.validation import DataValidator, StringDataValidator, NumberDataValidator
import pathlib
import os
import json
from decimal import Decimal


L = OculusDLogger()


HOME = '{}{}'.format(str(pathlib.Path.home()), os.sep)
L.debug('HOME={}'.format(HOME))


class GenericDataContainer:
    """A data container for storing some common Python types with some basic validation capabilities
    """

    def __init__(self, result_set_name: str='anonymous', data_type: object=str, data_validator: DataValidator=None, logger=L):
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
        self.data_validator = None
        if data_validator is not None:
            if isinstance(data_validator, DataValidator):
                self.data_validator = data_validator
                logger.info('Using DataValidator implementation of "{}"'.format(self.data_validator.__class__.__name__))
            else:
                raise Exception('Invalid data validator type. Expected an implementation of DataValidator')
        else:
            logger.warning('No data validator set')
        logger.info('GenericDataContainer "{}" ready'.format(result_set_name))
        self.logger = logger
        self.result_set_name = result_set_name

    def _store_dict(self, data: object, key: object, **kwarg)->int:
        if key is None:
            raise Exception('Expected a key value but found None (data_type was set to dict)')
        if key in self.data:
            self.logger.warning('Key "{}" already exists in dict - old value was replaced with new value'.format(key))
        if self.data_validator is not None:
            if isinstance(self.data_validator, DataValidator):
                if not self.data_validator.validate(data=data, **kwarg):
                    raise Exception('Dictionary validation failed')
                self.logger.info('Validation for value passed. key="{}"'.format(key))
            else:
                # FIXME: The code below should be unreachable. Further scenarios in testing should be explored.
                self.logger.warning('No DataValidator set - Dictionary value for key "{}" stored without validation! [2]'.format(key)) # pragma: no cover
        else:
            self.logger.warning('No DataValidator set - Dictionary value for key "{}" stored without validation! [1]'.format(key))
        self.data[key] = data
        return len(self.data)

    def _store_str(self, data: object, key: object=None, **kwarg)->int:
        validated = False
        if self.data_validator is not None:
            if isinstance(self.data_validator, StringDataValidator):
                validated = True
                if not self.data_validator.validate(data=data, **kwarg):
                    raise Exception('String validation failed')
                self.data = data
        if not validated:
            if data is None:
                self.data = None
                return 0
            else:
                self.data = '{}'.format(data)
        return len(self.data)

    def _store_list(self, data: object, key: object=None, **kwarg)->int:
        if self.data_validator is not None:
            if isinstance(self.data_validator, DataValidator):
                if not self.data_validator.validate(data=data, **kwarg):
                    raise Exception('List item validation failed')
                self.logger.debug('Validation for value passed. New list size: {}'.format(len(self.data)+1))
        else:
            self.logger.warning('No DataValidator set - List value stored without validation! [2]. New list size: {}'.format(len(self.data)+1))
        self.data.append(data)
        return len(self.data)

    def _store_tuple(self, data: object, key: object=None, **kwarg)->int:
        if data is None:
            raise Exception('Input data cannot be None - expecting a list or tuple')
        if type(data).__name__ not in ('list', 'tuple'):
            raise Exception('Expecting a list or tuple but got "{}"'.format(type(data)))
        if self.data_validator is not None:
            item_index = 0
            for item in data:
                if not self.data_validator.validate(data=item, **kwarg):
                    raise Exception('List item validation failed on item number {}'.format(item_index))
                item_index = item_index + 1
            self.logger.info('Validation for value passed. New list size: {}'.format(len(self.data)+1))
        if len(self.data) == 0 and type(self.data).__name__ == 'list':
            if type(data).__name__ == 'list':
                self.data = data
                self.data = tuple(self.data)
            elif type(data).__name__ == 'tuple':
                self.data = data
        else:
            raise Exception('Tuple already set. You have to create another GenericDataContainer instance to store another tuple')
        return len(self.data)

    def _store_int(self, data: object, key: object=None, **kwarg)->int:
        if type(data).__name__ not in ('int', 'float', 'str'):
            raise Exception('Expecting a int, float or str but got "{}"'.format(type(data).__name__))
        tmp_value = None
        if isinstance(data, str):
            tmp_value = int(float(data))
        elif isinstance(data, float):
            tmp_value = int(data)
        elif isinstance(data, int):
            tmp_value = data
        self.data = tmp_value
        if self.data_validator is not None:
            if isinstance(self.data_validator, NumberDataValidator):
                if self.data_validator.validate(data=self.data, **kwarg) is False:
                    raise Exception('Input validation failed')
            else:
                raise Exception('Expected a NumberDataValidator')
        return 1

    def _store_float(self, data: object, key: object=None, **kwarg)->int:
        if isinstance(data, str):
            self.data = float(data)
        elif isinstance(data, int):
            self.data = float(data)
        elif isinstance(data, float):
            self.data = data
        else:
            raise Exception('Could not convert input data to float')
        if self.data_validator is not None:
            if isinstance(self.data_validator, NumberDataValidator):
                if self.data_validator.validate(data=self.data, **kwarg) is False:
                    raise Exception('Input validation failed') 
            else:
                raise Exception('Expected a NumberDataValidator')
        return 1

    def _store_decimal(self, data: object, key: object=None, **kwarg)->int:
        if isinstance(data, str) or isinstance(data, int) or isinstance(data, float):
            self.data = Decimal(data)
        elif isinstance(data, Decimal):
            self.data = data
        else:
            raise Exception('Could not convert input data to Decimal')
        if self.data_validator is not None:
            if isinstance(self.data_validator, NumberDataValidator):
                if self.data_validator.validate(data=self.data, **kwarg) is False:
                    raise Exception('Input validation failed')
            else:
                raise Exception('Expected a NumberDataValidator')
        return 1

    def store(self, data: object, key: object=None, **kwarg)->int:
        if self.data_type.__name__ == 'dict':
            return self._store_dict(data=data, key=key, **kwarg)
        elif self.data_type.__name__ == 'str':
            return self._store_str(data=data, key=key, **kwarg)
        elif self.data_type.__name__ == 'list':
            return self._store_list(data=data, key=key, **kwarg)
        elif self.data_type.__name__ == 'tuple':
            return self._store_tuple(data=data, key=key, **kwarg)
        elif self.data_type.__name__ == 'int':
            return self._store_int(data=data, key=key, **kwarg)
        elif self.data_type.__name__ == 'float':
            return self._store_float(data=data, key=key, **kwarg)
        elif self.data_type.__name__ == 'Decimal':
            return self._store_decimal(data=data, key=key, **kwarg)
        else:
            raise Exception('Data was not a supported type. Type="{}"'.format(type(data)))


class GenericIOProcessor:
    """A processing Abstract Base Class that can be used to process data post reading/writing
    """

    def __init__(self, logger=L):
        """Initialize the processor

        :param logger: OculusDLogger defining the logger to use (default=OculusDLogger())
        """
        self.logger = logger

    def process(self, data: GenericDataContainer, **kwarg):
        """Each GenericIO implementation have the option to implement post read/write processing. When this is done, 
        this method will be called.

        The method will not return any data. If you need to get data from this processing function, a possible solution
        is to define an in-memory SQLite database, and pass the DB handler and key as keyword parameters to your
        processor. The caller can then retrieve the result from memory using the key. Example:

        ::
            import sqlite3

            conn = sqlite3.connect(':memory:')
            c = conn.cursor()
            c.execute('''CREATE TABLE store (key TEXT PRIMARY KEY, value TEXT)'''
            conn.commit()

            class MyIOProcessor(GenericIOProcessor):
                def __init__(self, logger=L):
                    super().__init__(logger=logger)
                def process(self, data: GenericDataContainer, **kwarg):
                       .
                       .
                       .
                    # if 'memory_db_handler' key is present in kwarg, use it to store the result, using the uri of the GenericDataContainer as the in-memory DB key
                    if 'memory_db_handler' in kwarg:
                        if kwarg['memory_db_handler'] is not None:
                            if isinstance(kwarg['memory_db_handler'], sqlite3.Connection):
                                key = data.uri
                                c = kwarg['memory_db_handler'].cursor()
                                c.execute('''INSERT INTO store ( key, value ) VALUES ( ?, ? )''', (data.uri, '{}'.format(True),))
                                kwarg['memory_db_handler'].commit()
                        .
                        .
                        .

            # Do a test:
            test_data = GenericDataContainer(result_set_name='test1')
            processor = MyIOProcessor()
            processor.process(
                data = GenericDataContainer(),
                memory_db_handler=conn
            )
               .
               .
               .
            # Later...
            c.execute('''SELECT value FROM store WHERE key = ?''', (test_data.uri, ))
            print('value={}'.format(c.fetchone()))

        :param data: GenericDataContainer containing the data to process
        :param **kwarg: All additional arguments passed to the GenericIO implementation class will be forwarded to this method
        """
        raise Exception('Not yet implemented')


class GenericIO:

    def __init__(self, uri: str, logger=L):
        self.uri = uri
        self.logger = logger

    def read(self, read_processor: GenericIOProcessor=None, **kwarg)->GenericDataContainer:
        raise Exception('Not yet implemented')

    def write(self, data: GenericDataContainer, write_processor: GenericIOProcessor=None, **kwarg):
        raise Exception('Not yet implemented')


class TextFileIO(GenericIO):

    def __init__(
        self,
        file_folder_path: str,
        file_name: str,
        cache_max_age: int=900,
        enable_cache: bool=False,
        logger=L
    ):
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
            ),
            logger=logger
        )

    def read(self, read_processor: GenericIOProcessor=None, **kwarg)->GenericDataContainer:
        """Read text data from a file

        :param read_processor: GenericIOProcessor that is not used in this function - whatever is supplied here will be ignored (for now)
        :param force: bool which is an optional argument. If the keyword is present, any cached data will be ignored (cache will be cleared as well)

        :returns: GenericDataContainer
        """
        if self.enable_cache is True:
            now = get_utc_timestamp()
            if 'force' not in kwarg:
                if self.cached_data is not None and (now - self.cached_data_timestamp) < self.cache_max_age:
                    self.logger.info('Returning cached value')
                    return self.cached_data
            else:
                self.logger.info('Cache reset forced.')
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
        self.logger.info('{} bytes read.'.format(len(data_str)))
        if self.enable_cache is True:
            self.cached_data = data
            self.cached_data_timestamp = get_utc_timestamp()
            self.logger.info('Cache updated')
        if read_processor is not None:
            if isinstance(read_processor, GenericIOProcessor):
                self.logger.info('Running read processor')
                self.logger.debug('kwarg={}'.format(kwarg))
                read_processor.process(data=data, **kwarg)
            else:
                self.logger.error('Skipping read processor - wrong type. Expected a GenericIOProcessor')
        return data

    def write(self, data: GenericDataContainer, write_processor: GenericIOProcessor=None, **kwarg):
        data_to_write = data.data
        if data.data_type.__name__ != 'str':
            if data.data_type.__name__ == 'dict':
                data_to_write = json.dumps(data_to_write)
            else:
                data_to_write = '{}'.format(data_to_write)
        with open(self.uri, 'w') as f:
            f.write(data.data)
            if self.enable_cache is True:
                self.cached_data = data
                self.cached_data_timestamp = get_utc_timestamp()
        if write_processor is not None:
            if isinstance(write_processor, GenericIOProcessor):
                self.logger.info('Running write processor')
                self.logger.debug('kwarg={}'.format(kwarg))
                write_processor.process(data=data, **kwarg)
            else:
                self.logger.error('Skipping write processor - wrong type. Expected a GenericIOProcessor')

# EOF
