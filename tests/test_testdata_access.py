import os

import pytest

from pyaerocom import const
from pyaerocom.access_testdata import AccessTestData


@pytest.fixture(scope="module")
def td():
    return AccessTestData()


def test_TestDataAccess(td):
    assert td._basedir is None
    assert str(td.basedir) == const.OUTPUTDIR
    assert os.path.basename(td.testdatadir) == "testdata-minimal"
    with pytest.raises(AttributeError):
        td.testdatadir = "/home"


def test_TestDataAccess_add_paths(td):
    assert os.path.exists(td.testdatadir)
    for name, relpath in td.ADD_PATHS.items():
        assert td.testdatadir.joinpath(relpath).exists()


def test_TestDataAccess_check_access(td):
    assert td.check_access()
    assert not td.check_access(dict(bla="/blub"))


def test_TestDataAccess_init(td):
    assert td.init()
