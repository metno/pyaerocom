import os

import numpy as np
import pytest
from numpy.testing import assert_allclose

from pyaerocom.io.read_aeronet_sunv3 import ReadAeronetSunV3

from ..conftest import data_unavail


@data_unavail
@pytest.fixture(scope="module")
def reader():
    return ReadAeronetSunV3("AeronetSunV3L2Subset.daily")


@data_unavail
def test_get_file_list(reader):
    assert len(reader.get_file_list()) == 22


@data_unavail
def test_read_file(reader):
    from pyaerocom.stationdata import StationData

    reader.get_file_list()
    file = reader.files[-3]
    assert os.path.basename(file) == "Thessaloniki.lev30"
    data = reader.read_file(file)
    assert isinstance(data, StationData)
    assert data.latitude[0] == 40.63
    assert data.longitude[0] == 22.96
    assert data.station_name[0] == "Thessaloniki"
    assert all(x in data for x in ["od550aer", "ang4487aer"])

    actual = [data["od550aer"][:10].mean(), data["ang4487aer"][:10].mean()]
    desired = [0.287, 1.787]
    assert_allclose(actual, desired, rtol=1e-3)


@data_unavail
def test_read(reader):
    from pyaerocom.ungriddeddata import UngriddedData

    files = reader.files[2:4]
    assert all(os.path.basename(x) in ("Agoufou.lev30", "Alta_Floresta.lev30") for x in files)
    data = reader.read(files=files)
    assert isinstance(data, UngriddedData)
    assert data.unique_station_names == ["Agoufou", "Alta_Floresta"]
    assert data.contains_vars == ["od550aer", "ang4487aer"]
    assert data.contains_instruments == ["sun_photometer"]
    assert data.shape == (11990, 12)
    assert_allclose(np.nanmean(data._data[:, data._DATAINDEX]), 0.676, rtol=1e-3)


@data_unavail
def test_read_add_common_meta(reader):
    files = reader.files[2:4]
    data = reader.read("od550aer", files=files, common_meta={"bla": 42})
    assert all("bla" in x for x in data.metadata.values())


@data_unavail
def test_get_od550lt1ang(reader):
    reader.get_file_list()
    file = reader.files[-3]
    data = reader.read_file(file, vars_to_retrieve="od550lt1ang")
    assert "od550lt1ang" in data
    test_data = reader.read_file(file)
    test_data = np.where(test_data["ang4487aer"] < 1.0, test_data["od550aer"], np.nan)
    assert_allclose(np.nanmean(data["od550lt1ang"]), np.nanmean(test_data), rtol=1e-3)
