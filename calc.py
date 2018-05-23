"""
TODO: our steps how to parse and calc our string
1. get string and remove any spaces > clean_up_str(string)
2. parse clean string and find all signs, funcs and numbers
using perfect_parse_string(clean_string)
"""


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
testing_strings = {
    '(2 +55 +(4-6/  2)*(34-2 )+( 1-1*(2/2)))',
}


def clean_up_str(str):
    """ remove all spaces """

    return str.replace(' ', '')


def perfect_parse_string(input_string):
    """ parse clean string and find all signs, funcs and numbers """

    for _str in input_string:
        clean_str = clean_up_str(_str)
        parsed_list = ()
        last_element = ''
        print(clean_str)
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
        print(parsed_list)
    return parsed_list


def find_and_calc_branckets(list=[]):
    """ find and calculate all elements in brackets () firstly"""

    # while '(' or ')' not in list:
    is_value_in_brackets = False
    for position, element in enumerate(list):
        if element == '(':
            is_value_in_brackets = True
            values_in_branckets = ()
            values_in_branckets += (element, )
            continue
        elif element == ')':
            # if we found ) bracket we may propose
            # that we have the full (...) construction
            is_value_in_brackets = False
            values_in_branckets += (element, )
            if len(values_in_branckets) >= 2:
                # show the tuple if the len > 2
                # (not only ( or ) symbols)
                # TODO remove this easy and stupid method
                # need to check corectly
                print(values_in_branckets)
            values_in_branckets = ()
            continue
        if is_value_in_brackets:
            # show the tuple if it exists
            values_in_branckets += (element, )
    pass

# run parser
list_with_values = perfect_parse_string(testing_strings)
find_and_calc_branckets(list_with_values)
# operators[s][1](x,y) - lambda fun to quickly calc numbers and get the result
