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
    variables = ["NOx", "concso4", "od550aer", "SO2"]

    assert rp.PROVIDES_VARIABLES == variables
    assert rp.DEFAULT_VARS == variables


####################################################
#   Tests for the helper class PyaroToUngriddedData
####################################################


def test_pyarotoungriddeddata_reading(pyaro_testdata):
    from math import ceil

    obj = pyaro_testdata.converter
    data = obj.read()
    assert isinstance(data, UngriddedData)

    # Checks is data is empty
    assert not data.is_empty
    assert len(data.unique_station_names) == 2

    # Tests the found stations
    all_stations = data.to_station_data_all("concso4", ts_type_preferred="daily")

    assert all_stations["stats"][0]["ts_type"] in [
        "hourly",
        "3daily",
        "2hourly",
        "2daily",
    ]
    assert all_stations["stats"][0]["country"] == "NO"

    # Tests the dates
    start = pd.to_datetime("01.01.2010", dayfirst=True)
    end = pd.to_datetime("31.12.2010", dayfirst=True)
    dates = pd.date_range(start, end, freq="D")
    assert len(all_stations["stats"][0].dtime) == ceil(len(dates) / 2)


def test_pyarotoungriddeddata_reading_kwargs(pyaro_testdata_kwargs):
    obj = pyaro_testdata_kwargs.converter
    data = obj.read()
    assert isinstance(data, UngriddedData)

    # Checks if stations have correct countries
    all_stations = data.to_station_data_all("concso4")
    countries = ["NO", "GB"]
    assert all_stations["stats"][1]["country"].strip() == countries[0]
    assert all_stations["stats"][0]["country"].strip() == countries[1]


def test_pyarotoungriddeddata_reading_extra_metadata(pyaro_testdata_kwargs):
    obj = pyaro_testdata_kwargs.converter
    data = obj.read()
    assert isinstance(data, UngriddedData)

    # Checks if stations have correct countries
    all_stations = data.to_station_data_all("concso4", add_meta_keys=["area_classification"])
    area_type = ["Rural", "Urban"]
    assert all_stations["stats"][1]["area_classification"].strip() == area_type[0]
    assert all_stations["stats"][0]["area_classification"].strip() == area_type[1]


def test_pyarotoungriddeddata_stations(pyaro_testdata):
    obj = pyaro_testdata.converter

    assert len(obj.get_stations()) == 2


def test_pyarotoungriddeddata_variables(pyaro_testdata):
    obj = pyaro_testdata.converter

    assert obj.get_variables() == pyaro_testdata.PROVIDES_VARIABLES


def test_pyaro_unit_change(pyaro_testdata_units):
    # Atoms
    M_O = 15.999  # u
    M_S = 32.065  # u
    # Molecules
    M_SO2 = M_S + 2 * M_O
    conversion_factor = 1e-6 * M_SO2 / M_S

    obj = pyaro_testdata_units.converter
    data = obj.read()

    all_stations_so4 = data.to_station_data_all("concso4")
    all_stations_so2 = data.to_station_data_all("concso2")

    assert (
        abs(
            all_stations_so4["stats"][0]["concso4"].mean() * conversion_factor
            - all_stations_so2["stats"][0]["concso2"].mean()
        )
        < 1e-5
    )
