import pytest
from pyaerocom.io.read_etex1 import ReadETEX1
from pyaerocom.io.readungridded import ReadUngridded
from pyaerocom.ungriddeddata import UngriddedData

from ..conftest import lustre_unavail


@lustre_unavail
def test_read_etex1():
    data = ReadETEX1()
    assert isinstance(data, UngriddedData)


def test_read_ungridded():
    data = ReadUngridded().read("etex1", "concch")
    
