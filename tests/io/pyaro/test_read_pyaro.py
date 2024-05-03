from __future__ import annotations

import pandas as pd

from pyaerocom import UngriddedData
from pyaerocom.io import ReadPyaro


def test_testfile(pyaro_test_data_file):
    assert pyaro_test_data_file.exists()


def test_readpyaro(pyaro_testdata):
    rp = pyaro_testdata

    assert isinstance(rp, ReadPyaro)


def test_variables(pyaro_testdata):
    rp = pyaro_testdata
    variables = ["NOx", "concso4"]

    assert rp.PROVIDES_VARIABLES == variables
    assert rp.DEFAULT_VARS == variables


####################################################
#   Tests for the helper class PyaroToUngriddedData
####################################################


def test_pyarotoungriddeddata_reading(pyaro_testdata):
    obj = pyaro_testdata.converter
    data = obj.read()
    assert isinstance(data, UngriddedData)

    # Checks is data is empty
    assert not data.is_empty
    assert len(data.unique_station_names) == 2

    # Tests the found stations
    all_stations = data.to_station_data_all("concso4")

    assert all_stations["stats"][0]["ts_type"] == "daily"
    assert all_stations["stats"][0]["country"] == "NO"

    # Tests the dates
    start = pd.to_datetime("01.01.2015", dayfirst=True)
    end = pd.to_datetime("31.12.2015", dayfirst=True)
    dates = pd.date_range(start, end, freq="D")
    assert (all_stations["stats"][0].dtime == dates).all()


def test_pyarotoungriddeddata_reading_kwargs(pyaro_testdata_kwargs):
    obj = pyaro_testdata_kwargs.converter
    data = obj.read()
    assert isinstance(data, UngriddedData)

    # Checks if stations have correct countries
    all_stations = data.to_station_data_all("concso4")
    countries = ["NO", "GB"]
    assert all_stations["stats"][1]["country"].strip() == countries[0]
    assert all_stations["stats"][0]["country"].strip() == countries[1]


def test_pyarotoungriddeddata_stations(pyaro_testdata):
    obj = pyaro_testdata.converter

    assert len(obj.get_stations()) == 2


def test_pyarotoungriddeddata_variables(pyaro_testdata):
    obj = pyaro_testdata.converter

    assert obj.get_variables() == pyaro_testdata.PROVIDES_VARIABLES
