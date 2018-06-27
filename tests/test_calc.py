""" Configuration file for 'Pytest'.
    Main tests for calculator

    The list of func for test coverage

    def clean_up_str(self, _string):
    def parse_string(self, input_string):
    def sort_values_stack(self, parsed_string):
    def calc(self, notation):

"""

from pycalc import Calc


def test_calc():
    """checking base cleanup and replacement **"""

    calculator = Calc('calc')
    result = calculator.clean_up_str(' 2+2-4 ** (-5-4) ')
    expectation = '2+2-4^(-5-4)'
    calculator.log('info', '---------------------------')
    calculator.log('info', 'compare {expect} with {actual}'.format(expect=expectation, actual=result))
    calculator.log('info', '---------------------------')

    assert result == expectation
