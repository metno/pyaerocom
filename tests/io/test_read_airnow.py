from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from numpy.testing import assert_allclose

from pyaerocom.exceptions import DataRetrievalError
from pyaerocom.io.read_airnow import ReadAirNow
from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData


@pytest.fixture(scope="module")
def reader() -> ReadAirNow:
    return ReadAirNow("AirNowSubset")


def test__FILETYPE(reader: ReadAirNow):
    assert reader._FILETYPE == ".dat"


def test__FILEMASK(reader: ReadAirNow):
    assert reader._FILEMASK == "/**/*.dat"


def test__version__(reader: ReadAirNow):
    assert reader.__version__ == "0.07"


def test_FILE_COL_DELIM(reader: ReadAirNow):
    assert reader.FILE_COL_DELIM == "|"


def test_FILE_COL_NAMES(reader: ReadAirNow):
    COLUMNS_IN_DATA_FILES = [
        "date",
        "time",
        "station_id",
        "station_name",
        "time_zone",
        "variable",
        "unit",
        "value",
        "institute",
    ]
    assert sorted(reader.FILE_COL_NAMES) == sorted(COLUMNS_IN_DATA_FILES)


def test_STATION_META_MAP(reader: ReadAirNow):
    # mapping of columns in station metadata file to pyaerocom standard
    METADATA_COLUMNS = dict(
        aqsid="station_id",
        name="station_name",
        lat="latitude",
        lon="longitude",
        elevation="altitude",
        city="city",
        address="address",
        timezone="timezone",
        environment="area_classification",
        populationclass="station_classification",
        modificationdate="modificationdate",
        comment="comment",
    )
    assert reader.STATION_META_MAP == METADATA_COLUMNS


def test_STATION_META_DTYPES(reader: ReadAirNow):
    METADATA_TYPES = dict(
        station_id=str,
        station_name=str,
        latitude=float,
        longitude=float,
        altitude=float,
        city=str,
        address=str,
        timezone=str,
        area_classification=str,
        modificationdate=str,
        station_classification=str,
        comment=str,
    )
    assert reader.STATION_META_DTYPES == METADATA_TYPES


def test_REPLACE_STATNAME(reader: ReadAirNow):
    REPLACE_STATNAME = {"&": "and", "/": " ", ":": " ", ".": " ", "'": ""}
    assert reader.REPLACE_STATNAME == REPLACE_STATNAME


def test_BASEYEAR(reader: ReadAirNow):
    # Years in timestamps in the files are are 2-digit (e.g. 20 for 2020)
    assert reader.BASEYEAR == 2000


def test_DATA_ID(reader: ReadAirNow):
    assert reader.DATA_ID == "AirNow"


def test_SUPPORTED_DATASETS(reader: ReadAirNow):
    assert reader.SUPPORTED_DATASETS == ["AirNow", "AirNowSubset"]


def test_UNIT_MAP(reader: ReadAirNow):
    # units found in file
    UNITS = {
        "C": "celcius",
        "M/S": "m s-1",
        "MILLIBAR": "mbar",
        "MM": "mm",
        "PERCENT": "%",
        "PPB": "ppb",
        "PPM": "ppm",
        "UG/M3": "ug m-3",
        "WATTS/M2": "W m-2",
    }
    assert reader.UNIT_MAP == UNITS


def test_variables(reader: ReadAirNow):
    VARIABLES = dict(
        concbc="BC",
        concpm10="PM10",
        concpm25="PM2.5",
        vmrco="CO",
        vmrnh3="NH3",
        vmrno="NO",
        vmrno2="NO2",
        vmrnox="NOX",
        vmrnoy="NOY",
        vmro3="OZONE",
        vmrso2="SO2",
    )
    assert reader.VAR_MAP == VARIABLES
    assert reader.DEFAULT_VARS == reader.PROVIDES_VARIABLES == list(VARIABLES)


def test_TSTYPE(reader: ReadAirNow):
    assert reader.TS_TYPE == "hourly"


def test_STAT_META_FILENAME(reader: ReadAirNow):
    assert reader.STAT_METADATA_FILENAME == "allStations_20191224.csv"


def test__date_time_str_to_datetime64(reader: ReadAirNow):
    dt = reader._date_time_str_to_datetime64("10/23/20", "13:55")

    assert isinstance(dt, np.datetime64)
    assert dt.dtype == "datetime64[s]"
    assert str(dt) == "2020-10-23T13:55:00"


@pytest.mark.parametrize(
    "filename,timestamp",
    [
        ("2020010101.dat", "2020-01-01T01:00:00"),
        ("2020010102.dat", "2020-01-01T02:00:00"),
        ("2020010107.dat", "2020-01-01T07:00:00"),
    ],
)
def test__datetime64_from_filename(reader: ReadAirNow, filename: str, timestamp: str):
    dt = reader._datetime64_from_filename(filename)
    assert isinstance(dt, np.datetime64)
    assert dt.dtype == "datetime64[s]"
    assert str(dt) == timestamp


def test__read_metadata_file(reader: ReadAirNow):
    COLUMNS = [
        "aqsid",
        "name",
        "lat",
        "lon",
        "elevation",
        "city",
        "address",
        "position",
        "timezone",
        "environment",
        "modificationdate",
        "populationclass",
        "comment",
    ]

    cfg = reader._read_metadata_file()
    assert isinstance(cfg, pd.DataFrame)
    assert list(cfg.columns) == COLUMNS
    assert cfg.values.shape == (2588, 13)


def test__correct_station_name(reader: ReadAirNow):
    station_name = "Bla/blub.bla'blub:blaa & blub"
    correct_name = "Bla blub blablub blaa and blub"
    assert reader._correct_station_name(station_name) == correct_name


def test__init_station_metadata(reader: ReadAirNow):
    stations = reader._init_station_metadata()
    assert len(stations) == 2588
    assert all(isinstance(x, dict) for x in stations.values())

    ids = list(stations)
    assert ids[0] == "000010101"
    assert ids[1000] == "160550006"

    station = stations["000010101"]
    assert station["station_name"] == "Duckworth and Ordinance"
    assert station["station_id"] == "000010101"
    assert_allclose(station["latitude"], 47.568, rtol=1e-3)
    assert_allclose(station["longitude"], -52.702, rtol=1e-3)
    assert station["altitude"] == 7

    station = stations["160550006"]
    assert station["station_name"] == "Coeur D Alene - Teom"
    assert station["station_id"] == "160550006"
    assert_allclose(station["latitude"], 47.682, rtol=1e-3)
    assert_allclose(station["longitude"], -116.766, rtol=1e-3)
    assert station["altitude"] == 665


def test_data_dir_exists(reader: ReadAirNow):
    assert Path(reader.data_dir).exists()


def test_get_file_list(reader: ReadAirNow):
    files = reader.get_file_list()
    assert len(files) == 3

    FILE_NAMES = ["2020010101.dat", "2020010102.dat", "2020010107.dat"]
    assert [Path(f).name for f in files] == FILE_NAMES


def test__read_file(reader: ReadAirNow):
    file = reader.get_file_list()[0]
    data = reader._read_file(file)
    assert isinstance(data, pd.DataFrame)
    assert list(data.columns) == reader.FILE_COL_NAMES
    assert data.values.shape == (14979, 9)


# This should test all variables available and reads the first 3 data files
# so for each variable, the StationData objects should contain 3 timestamps
@pytest.mark.parametrize(
    "var_name,statnum,first_dtime,first_vals,unit",
    [
        pytest.param(
            "concbc",
            8,
            ["2019-12-31T17:00:00", "2019-12-31T18:00:00", "2019-12-31T23:00:00"],
            [0.92, 1.53, 3.37],
            "ug m-3",
            id="concbc",
        ),
        pytest.param(
            "concpm10",
            196,
            ["2019-12-31T19:00:00", "2019-12-31T20:00:00", "2020-01-01T01:00:00"],
            [0.0, 0.0, -1.0],
            "ug m-3",
            id="concpm10",
        ),
        pytest.param(
            "concpm25",
            679,
            ["2019-12-31T21:00:00", "2019-12-31T22:00:00", "2020-01-01T03:00:00"],
            [11.0, 12.0, 5.0],
            "ug m-3",
            id="concpm25",
        ),
        pytest.param(
            "vmrco",
            115,
            ["2019-12-31T18:00:00", "2019-12-31T19:00:00", "2020-01-01T00:00:00"],
            [0.7, 0.8, 0.6],
            "ppm",
            id="vmrco",
        ),
        pytest.param(
            "vmrno",
            129,
            ["2019-12-31T21:00:00", "2019-12-31T22:00:00", "2020-01-01T03:00:00"],
            [0.0, 0.0, 0.0],
            "ppb",
            id="vmrno",
        ),
        pytest.param(
            "vmrno2",
            187,
            ["2019-12-31T21:00:00", "2019-12-31T22:00:00", "2020-01-01T03:00:00"],
            [0.0, 0.0, 0.0],
            "ppb",
            id="vmrno2",
        ),
        pytest.param(
            "vmrnox",
            103,
            ["2019-12-31T17:00:00", "2019-12-31T18:00:00", "2019-12-31T23:00:00"],
            [22.7, 30.9, 31.5],
            "ppb",
            id="vmrnox",
        ),
        pytest.param(
            "vmrnoy",
            33,
            ["2019-12-31T18:00:00", "2019-12-31T19:00:00", "2020-01-01T00:00:00"],
            [21.6, 28.8, 84.5],
            "ppb",
            id="vmrnoy",
        ),
        pytest.param(
            "vmro3",
            747,
            ["2019-12-31T21:00:00", "2019-12-31T22:00:00", "2020-01-01T03:00:00"],
            [30.0, 25.0, 29.0],
            "ppb",
            id="vmro3",
        ),
        pytest.param(
            "vmrso2",
            181,
            ["2019-12-31T21:00:00", "2019-12-31T22:00:00", "2020-01-01T03:00:00"],
            [0.0, 0.0, 0.0],
            "ppb",
            id="vmrso2",
        ),
    ],
)
def test__read_files_single_var(
    reader: ReadAirNow,
    var_name: str,
    statnum: int,
    first_dtime: list[str],
    first_vals: list[float],
    unit: str,
):

    files = reader.get_file_list()
    data = reader._read_files(files, [var_name])
    assert isinstance(data, list)
    assert len(data) == statnum

    for stat in data:
        assert isinstance(stat, StationData)
        assert var_name in stat

    first_stat = data[0]

    # timeseries metadata
    assert var_name in first_stat["var_info"]
    assert "units" in first_stat["var_info"][var_name]
    assert first_stat["var_info"][var_name]["units"] == unit

    dtimelist = [str(x) for x in first_stat.dtime]
    assert dtimelist == first_dtime

    assert isinstance(first_stat[var_name], np.ndarray)
    assert list(first_stat[var_name]) == first_vals


def test__read_files_single_var_error(reader: ReadAirNow):

    files = reader.get_file_list()
    # NH3 not available in selected 3 test files
    with pytest.raises(DataRetrievalError) as e:
        reader._read_files(files, ["vmrnh3"])
    assert str(e.value) == "None of the input variables could be found in input list"


def test_read_file(reader):
    with pytest.raises(NotImplementedError):
        reader.read_file()


@pytest.mark.parametrize(
    "vars_to_retrieve, num_meta_blocks,num_stats",
    [
        ("concpm10", 196, 196),
        (
            [
                "concbc",
                "concpm10",
                "concpm25",
                "vmrco",
                "vmrno",
                "vmrno2",
                "vmrnox",
                "vmrnoy",
                "vmro3",
                "vmrso2",
            ],
            2378,
            1139,
        ),
    ],
)
def test_read(
    reader: ReadAirNow, vars_to_retrieve: str | list[str], num_meta_blocks: int, num_stats: int
):
    data = reader.read(vars_to_retrieve)
    if isinstance(vars_to_retrieve, str):
        vars_to_retrieve = [vars_to_retrieve]
    assert isinstance(data, UngriddedData)
    assert len(data.metadata) == num_meta_blocks
    assert len(data.unique_station_names) == num_stats
    assert sorted(data.contains_vars) == sorted(vars_to_retrieve)
