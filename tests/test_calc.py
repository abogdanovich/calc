""" Configuration file for 'Pytest'.
    Main tests for calculator

    The list of func for test coverage

    def clean_up_str(self, _string):
    def parse_string(self, input_string):
    def sort_values_stack(self, parsed_string):
    def calc(self, notation):


"""

from calc import Calc
import pytest


def test_calc(calc_session):
    """checking base calculation"""

    Calc.calc([2, 2, '+'])
    assert result == 4


