""" Configuration file for 'Pytest'.
    Main tests for calculator

    The list of func for test coverage

    def clean_up_str(self, _string):
    def parse_string(self, input_string):
    def sort_values_stack(self, parsed_string):
    def calc(self, notation):

"""

from pycalc import Calc


def test_clean_up_str(calc_session):
    """checking clanup"""

    calculator = Calc('calc')
    result = calculator.calc([2, 2, '+'])
    expectation = 4
    calculator.log('info', '---------------------------')
    calculator.log('info', 'compare {expect} with {actual}'.format(expect=expectation, actual=result))
    calculator.log('info', '---------------------------')

    assert result == expectation
