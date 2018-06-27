import pytest
from pycalc import Calc

calc = Calc('calc_test')


@pytest.fixture(scope="session", autouse=True)
def calc_session(request):
    """ We can put here a lot of different preparing
        stuff for our extended unit tests

    """

    calc.log('info', '#############################')
    calc.log('info', 'pycalc unit testing. START')
    calc.log('info', '#############################')

    def end_session():
        """teardown fixture to finish tests"""

        calc.log('info', '#############################')
        calc.log('info', 'pycalc unit testing. STOP')
        calc.log('info', '#############################')

    request.addfinalizer(end_session)