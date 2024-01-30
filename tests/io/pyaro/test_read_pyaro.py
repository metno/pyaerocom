from __future__ import annotations

import pytest
from pathlib import Path

import pandas as pd

from tests.fixtures.pyaro import pyaro_test_data_file, pyaro_testdata
from pyaerocom.io import ReadPyaro, PyaroConfig
from pyaerocom.io.pyaro.read_pyaro import PyaroToUngriddedData
from pyaerocom import UngriddedData

def test_testfile(pyaro_test_data_file):
    assert pyaro_test_data_file.exists()

def test_readpyaro(pyaro_testdata):
    rp = pyaro_testdata

    assert isinstance(rp, ReadPyaro)

def test_variables(pyaro_testdata):
    rp = pyaro_testdata
    variables = ["NOx","oxidised_sulphur"]

    assert rp.PROVIDES_VARIABLES == variables
    assert rp.DEFAULT_VARS == variables

def test_getreaders(pyaro_testdata):
    readers = pyaro_testdata.get_pyaro_readers()

    assert pyaro_testdata.DATA_ID in readers



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
    all_stations = data.to_station_data_all("oxidised_sulphur")

    assert all_stations["stats"][0]["ts_type"] == "daily"
    assert all_stations["stats"][0]["country"] == "NO"


    # Tests the dates
    start = pd.to_datetime("01.01.2015", dayfirst=True)
    end = pd.to_datetime("31.12.2015", dayfirst=True)
    dates = pd.date_range(start, end, freq="D")
    assert (all_stations["stats"][0].dtime == dates).all()


def test_pyarotoungriddeddata_stations(pyaro_testdata):
    obj = pyaro_testdata.converter

    assert len(obj.get_stations()) == 2

def test_pyarotoungriddeddata_variables(pyaro_testdata):
    obj = pyaro_testdata.converter

    assert obj.get_variables() == pyaro_testdata.PROVIDES_VARIABLES

