""" Configuration file for 'Pytest'.
    'Pytest' automatically search for it before test execution and specifies
    it's work according to a changes recorded inside of conftest.py.
    This file affects tests in current directory and it's subdirectories.
    More info about conftest.py:
    https://docs.pytest.org/en/2.7.3/plugins.html?highlight

    ---------------------------------------------------------------------------
    Conftest content
    ---------------------------------------------------------------------------

    Fixtures:
    TODO: textures description is here

"""

import pytest


@pytest.fixture(scope="session")
def initialization():
    """ Handler for --stand-config parameter """

    pass

