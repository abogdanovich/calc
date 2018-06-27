"""pycalc.py script to parse and calculate values from input string.

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

# Predefined number, operators and funcs
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
    'acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil',
    'copysign', 'cos', 'cosh', 'degrees', 'e', 'erf', 'erfc', 'exp',
    'expm1', 'fabs', 'factorial', 'floor', 'fmod', 'frexp', 'fsum', 'gamma',
    'gcd', 'hypot', 'inf', 'isclose', 'isfinite', 'isinf', 'isnan', 'ldexp',
    'lgamma', 'log', 'log10', 'log1p', 'log2', 'modf', 'nan', 'pi', 'pow',
    'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'tau', 'trunc'
)
BRACKETS = ('(', ')', )


class Calc(object):
    """Main class with required funcs"""

    loging_level = 'INFO'
    time_format = '%Y-%m-%d_%H-%M-%S'

    # Unique log file name
    log_dir = './'

    # Init logger for common messages
    logger = logging.getLogger('Common')

    def __init__(self, log_name):
        """Init func with logging setup"""

        log_path = path.join(self.log_dir, '{name}_{time}.log'.format(
            name=log_name, time=strftime(self.time_format)
        )
                             )

        if self.loging_level.upper() == 'DEBUG':
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        # Add console handler to logger
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        self.logger.addHandler(stream_handler)

        # Add file handler to logger
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        self.logger.addHandler(file_handler)

        self.log('info', 'Logging is started {level}'.format(level=self.loging_level))

    def log(self, _level, _str):
        """Logging func to write logging"""

        if _level == 'info':
            self.logger.info(_str)
        else:
            self.logger.error(_str)

    def console_parser(self):
        """Console params parser"""

        parser = argparse.ArgumentParser('Calc string values script')

        # input string param as expression
        parser.add_argument('string', type=str,
                             help="input expression to calculate")

        # Arguments for calc operations
        parser.add_argument('-m', dest='module', action='store', type=str,
                            help='Additional modules to use in script')
        parser.add_argument('-f', dest='file', action='store', type=str,
                            help='File with testing expression lines')
        parser.add_argument('-log', dest='log', action='store', type=str,
                            help='Script log file name', default='./calc.log')

        return parser.parse_args()

    def clean_up_str(self, _string):
        """Remove all spaces and convert ** into ^(trick)"""

        _str = _string.replace(' ', '')

        return _str.replace('**', '^')

    def parse_string(self, input_string):
        """Parse string to find signs, funcs and numbers"""

        for _str in input_string:
            clean_str = self.clean_up_str(_str)
            parsed_list = ()
            last_element = ''
            for symbol in clean_str:
                # check each symbol
                if symbol in OPERATORS:
                    if last_element != '':
                        parsed_list += (last_element,)
                        last_element = ''
                    parsed_list += (symbol,)
                else:
                    # numbers and ()
                    if symbol in '()':
                        if last_element != '':
                            parsed_list += (last_element,)
                            last_element = ''
                        parsed_list += (symbol,)
                    else:
                        # the symbol is NUMBER
                        last_element += symbol
            if last_element != '':
                parsed_list += (last_element,)
        return parsed_list

    def sort_values_stack(self, parsed_string):
        """Trace values in accordance to sign priority and brackets"""

        stack = []
        sorted_elements = ()
        for element in parsed_string:
            # grab each element and compare priority with other stack elements
            if element in OPERATORS:
                while stack and stack[-1] != "(" \
                        and OPERATORS[element][0] <= OPERATORS[stack[-1]][0]:
                    sorted_elements += (stack.pop(),)
                    #yield stack.pop()
                stack.append(element)
            # check case when we're in (..)
            # and the next element is ) to get all bracket's elements
            elif element == ')':
                while stack:
                    bracket_item = stack.pop()
                    if bracket_item == '(':
                        break
                    sorted_elements += (bracket_item,)
                    #yield bracket_item
            elif element == "(":
                stack.append(element)
            else:
                # number of function is parsed here
                sorted_elements += (element,)
                #yield element
        while stack:
            sorted_elements += (stack.pop(),)
            #yield stack.pop()
        return sorted_elements

    def calc(self, notation):
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

    def calc_funcs(self, _tuple):
        """find and calculate all functions using external module"""

        # stupid solution to trace, find and calc all funcs
        stack = []
        for element in _tuple:
            if element in OPERATORS:
                y, x = stack.pop(), stack.pop()

                # calculate two values using lambda trick from OPERATORS
                stack.append(OPERATORS[element][1](float(x), float(y)))
            else:
                stack.append(element)
        return stack[0]


def main():
    """Main script method"""

    try:
        pycalc = Calc("calc")
        testing_strings = ''
        console_args = pycalc.console_parser()

        if not console_args.string:
           pycalc.log('error', 'No parsed input string')

        else:
            testing_strings = console_args.string
            pycalc.log('info', 'Starting with {parse_str}'.format(parse_str=console_args))

        # check and dynamically import external module
        if console_args.module:
            try:
                imported_module = importlib.import_module(console_args.module)
                # is_imported = True
                pycalc.log('info', 'Module {module} is imported successfully'.format(
                        module=console_args.module
                    )
                )
                pycalc.log('info', 'Func dir {module} is: {module_funcs}'.format(
                    module=console_args.module, module_funcs=dir(imported_module))
                )
            except ImportError as err:
                pycalc.log('error', 'Import {module} module {err}'.format(
                        module=console_args.module, err=err
                    )
                )

        # run parser
        list_values = pycalc.clean_up_str(testing_strings)
        calc_values = pycalc.sort_values_stack(list_values)
        print(pycalc.calc(calc_values))

    finally:
        pycalc.log('info', 'close application')


if __name__ == '__main__':
    main()
