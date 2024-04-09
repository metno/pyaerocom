from pathlib import Path

import numpy as np
import pytest

from pyaerocom.io.read_aeronet_sunv3 import ReadAeronetSunV3
from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData
from tests.conftest import lustre_unavail


@pytest.fixture(scope="module")
def reader():
    return ReadAeronetSunV3("AeronetSunV3L2Subset.daily")


def test_get_file_list(reader):
    assert len(reader.get_file_list()) == 22


def test_read_file(reader):
    reader.get_file_list()
    file = reader.files[-3]
    assert Path(file).name == "Thessaloniki.lev30"
    data = reader.read_file(file)
    assert isinstance(data, StationData)
    assert data.latitude[0] == 40.63
    assert data.longitude[0] == 22.96
    assert data.station_name[0] == "Thessaloniki"
    assert "od550aer" in data
    assert data["od550aer"][:10].mean() == pytest.approx(0.287, rel=1e-3)
    assert "ang4487aer" in data
    assert data["ang4487aer"][:10].mean() == pytest.approx(1.787, rel=1e-3)


def test_read(reader):
    reader.get_file_list()
    files = reader.files[2:4]
    assert [Path(file).name for file in files] == ["Agoufou.lev30", "Alta_Floresta.lev30"]
    # proxyzdust is essentially od550aer
    data = reader.read(
        files=files, vars_to_retrieve=["od550aer", "ang4487aer", "proxyod550oa", "proxyzdust"]
    )
    assert isinstance(data, UngriddedData)
    assert data.unique_station_names == ["Agoufou", "Alta_Floresta"]
    assert data.contains_vars == ["od550aer", "ang4487aer", "proxyod550oa", "proxyzdust"]
    assert data.contains_instruments == ["sun_photometer"]
    assert data.shape == (23980, 12)
    assert np.nanmean(data._data[:, data._DATAINDEX]) == pytest.approx(0.527, rel=1e-3)


def test_read_add_common_meta(reader):
    files = reader.files[2:4]
    data = reader.read("od550aer", files=files, common_meta={"bla": 42})
    assert all("bla" in x for x in data.metadata.values())


@lustre_unavail
def test_get_od550lt1ang(reader):
    reader.get_file_list()
    file = reader.files[-3]
    data = reader.read_file(file, vars_to_retrieve="od550lt1ang")
    assert "od550lt1ang" in data
    test_data = reader.read_file(file)
    test_data = np.where(test_data["ang4487aer"] < 1.0, test_data["od550aer"], np.nan)
    assert np.nanmean(data["od550lt1ang"]) == pytest.approx(np.nanmean(test_data), rel=1e-3)
