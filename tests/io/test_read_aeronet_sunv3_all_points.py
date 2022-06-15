from pathlib import Path

import pytest

from pyaerocom.exceptions import AeronetReadError
from pyaerocom.io.read_aeronet_sunv3 import ReadAeronetSunV3


@pytest.fixture(scope="module")
def reader():
    return ReadAeronetSunV3("AeronetSunV3L2Subset.AP")


def test_get_file_list(reader):
    assert len(reader.get_file_list()) >= 2


def test_read_file(reader):
    from pyaerocom.stationdata import StationData

    reader.get_file_list()
    file = reader.files[0]
    assert Path(file).name == "19930101_20211120_Karlsruhe.lev20.gz"
    data = reader.read_file(file)
    assert isinstance(data, StationData)
    assert data.latitude[0] == pytest.approx(49.09, 0.01)
    assert data.longitude[0] == pytest.approx(8.42, 0.01)
    assert data.station_name[0] == "Karlsruhe"
    assert all(x in data for x in ["od550aer", "ang4487aer"])


def test_read_add_common_meta(reader):
    reader.get_file_list()
    files = reader.files[0]

    data = reader.read("od550aer", files=files, common_meta={"bla": 42})
    assert all("bla" in x for x in data.metadata.values())


def test_exception_aeronet_read_error(reader):
    reader.get_file_list()
    files = sorted(reader.files)[-1]
    with pytest.raises(AeronetReadError) as e:
        data = reader.read_file(files[-1])
        assert data
    assert str(e.value).startswith("gzip error in file")
