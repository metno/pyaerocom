from pathlib import Path

import pytest

from pyaerocom import const
from pyaerocom.access_testdata import AccessTestData


@pytest.fixture(scope="module")
def td() -> AccessTestData:
    return AccessTestData()


def test_TestDataAccess(td: AccessTestData):
    assert td._basedir is None
    assert str(td.basedir) == const.OUTPUTDIR
    assert td.testdatadir.name == "testdata-minimal"
    with pytest.raises(AttributeError):
        td.testdatadir = "/home"  # type:ignore[misc]


def test_TestDataAccess_add_paths(td: AccessTestData):
    assert td.testdatadir.exists()
    paths = [td.testdatadir / path for path in td.ADD_PATHS.values()]
    assert all(path.exists() for path in paths)


def test_TestDataAccess_check_access(td: AccessTestData):
    assert td.check_access()
    assert not td.check_access(dict(bla="/blub"))


def test_TestDataAccess_init(td: AccessTestData):
    assert td.init()
