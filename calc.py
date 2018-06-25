"""calc.py script to parse and calculate values from input string.

Python Programming Language Foundation Hometask
You are proposed to implement pure-python command-line calculator
using **python 3.6**.

Last updates: 6/20/18 (08:00)

Required parameters:
    -m  --module include module into func (optional)
    -f  --file with parsed strings (optional)
    -l  --log file to show the overall progress (optional)
"""

import argparse
import logging
from os import path
from time import strftime
import importlib


# state for important module
# is_imported = False
# imported_module = None


################################################
# Console parser
################################################


def console_parser():
    parser = argparse.ArgumentParser('Calc string values script')

    # input string param
    parser.add_argument('string', type=str,
                        help="display a square of a given number")

    # Arguments for calc operations
    parser.add_argument('-m', dest='module', action='store', type=str,
                        help='Additional modules to use in script')
    parser.add_argument('-f', dest='file', action='store', type=str,
                        help='File with testing expression lines')
    parser.add_argument('-log', dest='log', action='store', type=str,
                        help='Script log file name', default='./calc.log')

    return parser.parse_args()

################################################
# Logging
################################################


LOGGING_LEVEL = 'INFO'
INDENT = '==================================================='
TIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

# Unique log file name
LOG_DIR = './'
LOG_PATH = path.join(LOG_DIR, 'calc_{}.log'.format(strftime(TIME_FORMAT)))

# Init logger for common messages
logger = logging.getLogger('Common')

if LOGGING_LEVEL.upper() == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# Add console handler to logger

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
logger.addHandler(stream_handler)

# Add file handler to logger
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
logger.addHandler(file_handler)

################################################
# Pre-defined numbers \ functions \ functions
################################################


NUMBERS = (
    '0', '1', '2', '3', '4', '5',
    '6', '7', '8', '9', '.',
)
OPERATORS = ({
    '>': (1, lambda x, y: x+y), '<': (1, lambda x, y: x+y),
    '&': (2, lambda x, y: x+y),
    '+': (3, lambda x, y: x+y), '-': (3, lambda x, y: x-y),
    '*': (4, lambda x, y: x*y), '/': (4, lambda x, y: x/y),
    '//': (4, lambda x, y: x//y), '%': (4, lambda x, y: x % y),
    '^': (5, lambda x, y: x**y),

})
FUNCTIONS = (
    'abs', 'pow', 'round',
    'sin', 'log', 'pi', 'cos',
)
BRACKETS = ('(', ')', )

################################################
# Main functions to parse and calculate values from string
################################################


def clean_up_str(_string):
    """Remove all spaces and convert ** into ^(trick)"""

    _str = _string.replace(' ', '')

    return _str.replace('**', '^')


def parse_string(input_string):
    """Parse string to find signs, funcs and numbers"""

    for _str in input_string:
        clean_str = clean_up_str(_str)
        parsed_list = ()
        last_element = ''
        for symbol in clean_str:
            # check each symbol
            if symbol in OPERATORS:
                if last_element != '':
                    parsed_list += (last_element, )
                    last_element = ''
                parsed_list += (symbol, )
            else:
                # numbers and ()
                if symbol in '()':
                    if last_element != '':
                        parsed_list += (last_element, )
                        last_element = ''
                    parsed_list += (symbol, )
                else:
                    # the symbol is NUMBER
                    last_element += symbol
        if last_element != '':
            parsed_list += (last_element, )
    return parsed_list


def sort_values_stack(parsed_string):
    """Trace values in accordance to sign priority and brackets"""

    stack = []
    for element in parsed_string:
        # grab each element and compare priority with other stack elements
        if element in OPERATORS:
            while stack and stack[-1] != "(" \
                    and OPERATORS[element][0] <= OPERATORS[stack[-1]][0]:
                yield stack.pop()
            stack.append(element)
        # check case when we're in (..)
        # and the next element is ) to get all bracket's elements
        elif element == ')':
            while stack:
                x = stack.pop()
                if x == '(':
                    break
                yield x
        elif element == "(":
            stack.append(element)
        else:
            # number of function is parsed here
            yield element
    while stack:
        yield stack.pop()


def calc(notation):
    """Main calculation using reverse polish notation"""

    stack = []
    for element in notation:
        if element in OPERATORS:
            y, x = stack.pop(), stack.pop()
            # calculate two values using lambda trick from OPERATORS
            stack.append(OPERATORS[element][1](float(x), float(y)))
        else:
            stack.append(element)
    return stack[0]

################################################
# Main function
################################################


def main():
    """Main script method"""

    try:
        testing_strings = {}
        console_args = console_parser()

        if not console_args.string:
            logger.error('No parsed input string')

        else:
            testing_strings = {console_args.string}

        logger.info('Starting with {parse_str}'.format(parse_str=console_args))

        # check and dynamically import external module
        if console_args.module:
            try:
                imported_module = importlib.import_module(console_args.module)
                is_imported = True
                logger.info(
                    'Module {module} is imported successfully'.format(
                        module=console_args.module
                    )
                )
                logger.info('Func dir {module} is: {module_funcs}'.format(
                    module=console_args.module, module_funcs=dir(imported_module))
                )
            except ImportError as err:
                logger.error('Import {module} module {err}'.format(module=console_args.module, err=err))

        # run parser
        list_values = parse_string(testing_strings)
        calc_values = sort_values_stack(list_values)
        print(calc(calc_values))

    finally:
        logger.info('close application')


if __name__ == '__main__':
    main()
