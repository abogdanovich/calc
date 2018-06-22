"""calc.py script to parse and calculate values from input string.

Python Programming Language Foundation Hometask
You are proposed to implement pure-python command-line calculator
using **python 3.6**.


By Aliaksandr Bahdanovich

Last updates: 6/20/18 (08:00)

Required parameters:
    -m  --module include module into func (optional)
    -f  --file with parsed strings (optional)
    -l  --log file to show the overall progress (optional)
"""

import argparse
import logging
from os import path
from time import strftime, sleep
import importlib


# state for important module
is_imported = False
imported_module = None


################################################
# Console parser
################################################


def console_parser():
    parser = argparse.ArgumentParser('Calc string values script')

    # input string param
    parser.add_argument('string', type=str, help="display a square of a given number")

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
    '+': (1, lambda x, y: x+y), '-': (1, lambda x, y: x-y),
    '*': (2, lambda x, y: x*y), '/': (2, lambda x, y: x/y),
    '^': (2, lambda x, y: x**y), '**': (2, lambda x, y: x**y),
    '//': (2, lambda x, y: x//y), '%': (2, lambda x, y: x % y),
})
FUNCTIONS = (
    'abs', 'pow', 'round',
    'sin', 'log', 'pi', 'cos',
)
BRACKETS = ('(', ')', )

################################################
# Main functions to parse and calculate values from string
################################################


def clean_up_str(str):
    """Remove all spaces """

    return str.replace(' ', '')


def parse_string(input_string):
    """Parse clean string and find all signs, funcs and numbers with operators"""

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
    for token in parsed_string:
        # если элемент - оператор, то отправляем дальше все операторы из стека,
        # чей приоритет больше или равен пришедшему,
        # до открывающей скобки или опустошения стека.
        # здесь мы пользуемся тем, что все операторы право-ассоциативны
        if token in OPERATORS:
            while stack and stack[-1] != "(" and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
                yield stack.pop()
            stack.append(token)
        elif token == ')':
            # если элемент - закрывающая скобка, выдаём все элементы из стека, до открывающей скобки,
            # а открывающую скобку выкидываем из стека.
            while stack:
                x = stack.pop()
                if x == '(':
                    break
                yield x
        elif token == "(":
            # если элемент - открывающая скобка, просто положим её в стек
            stack.append(token)
        else:
            # если элемент - число, отправим его сразу на выход
            yield token
    while stack:
        yield stack.pop()


def calc(notation):
    """Main calculation using reverse polish notation"""

    stack = []
    for token in notation:
        if token in OPERATORS:
            y, x = stack.pop(), stack.pop()

            # TODO: check funcs separately! do not through OPERATORS and do not apply lambda for funcs

            # calculate two values using lambda trick from OPERATORS
            stack.append(OPERATORS[token][1](float(x), float(y)))
        else:
            stack.append(token)
    print(stack[0])
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

        logger.info('Starting calc with string {parse_str}'.format(parse_str=console_args))

        # check and dynamically import external module
        if console_args.module:
            try:
                imported_module = importlib.import_module(console_args.module)
                is_imported = True
                print(imported_module.sin(9))
                logger.info('Module {module} is imported successfully'.format(module=console_args.module))
                logger.info('Possible func list for {module} are: {module_funcs}'.format(module=console_args.module, module_funcs=dir(imported_module)))
            except ImportError as err:
                logger.error('I can not import your interesting "{module}" module. Error: {err}'.format(module=console_args.module, err=err))

        # running parser
        list_values = parse_string(testing_strings)
        print(list_values)
        print("polish")
        calc_values = sort_values_stack(list_values)
        print("calc")
        calc(calc_values)
        # operators[s][1](x,y) - lambda fun to quickly calc numbers and get the result
    finally:
        logger.info('close application')


if __name__ == '__main__':
    main()
