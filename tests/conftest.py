import pytest
from calc import Calc

calc = Calc('calc_test')


@pytest.fixture(scope="session", autouse=True)
def calc_session(request, func):
    calc.log('info', 'Starting test for func: {func}'.format(func=func))

    def end_session():
        calc.log('info', 'Stop testing session')

    request.addfinalizer(end_session)