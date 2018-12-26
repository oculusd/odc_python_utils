# Common Python Utilities for OculusD.com, Inc. Projects and Applications

The common libraries include common functions and classes that may be useful in other projects or applications. 

The intention is that these should be common enough to be used in almost any application - even those outside 
OculusD.com, Inc. Please feel free to use it in your own projects as required.

## Prerequisites

The following are assumed:

* Python 3.6 or later is installed
* A Python virtual environment is preferred, but not essential

## Installation

Follow these commands to install from the console:

    (venv) $ git clone https://github.com/oculusd/odc_python_utils.git
    (venv) $ cd odc_python_utils/
    (venv) $ python3 setup.py sdist
    (venv) $ pip3 install dist/oculusd_commons_utils-0.0.1.tar.gz 

## Testing

The simplest way to run all unit tests will be the following method, requiring te package `coverage` to be installed:

    (venv) $ coverage run  --omit="*tests*" -m tests.test_all
    CONTENT: ['2018-12-26 11:48:35,060 - INFO - TEST\n']
    .CONTENT: ['2018-12-26 11:48:35,063 - DEBUG - [test_logging.py:60:test_init_force_debug] You should see this...\n', '2018-12-26 11:48:35,065 - INFO - [test_logging.py:61:test_init_force_debug] TEST\n']
    .CONTENT: ['2018-12-26 11:48:35,068 - INFO - TEST\n']
    .CONTENT: ['2018-12-26 11:48:35,070 - INFO - [test_logging.py:85:test_verify_content_including_debug] TEST\n']
    .........2018-12-26 11:48:35,082 - ERROR - input_str was None - returning empty string (trying to fail gracefully)
    ..............
    ----------------------------------------------------------------------
    Ran 26 tests in 0.035s

    OK
    (venv) $ coverage report -m
    Name                                   Stmts   Miss  Cover   Missing
    --------------------------------------------------------------------
    oculusd_utils/__init__.py                 58      0   100%
    oculusd_utils/security/__init__.py        18      0   100%
    oculusd_utils/security/validation.py      30      0   100%
    --------------------------------------------------------------------
    TOTAL                                    106      0   100%

__Note__: As you jump between branches the coverage numbers may change. Our aim is to always achieve close to 100% coverage

## Common Utilities

The following utilities are included:

* Pre-configured logging helper class
* Function to mask sensitive strings (like passwords)
* Simple (regular expression based) email address validation function
* Simple string validation function, intended to validate input parameters where those parameters are strings

More in-dept documentation will follow soon. For now you can refer to the documentation included in the source.