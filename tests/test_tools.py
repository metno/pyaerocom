import pytest

from pyaerocom.exceptions import DataSearchError
from pyaerocom.tools import browse_database


def test_browse_database():
    with pytest.raises(DataSearchError):
        browse_database("blaaa")
