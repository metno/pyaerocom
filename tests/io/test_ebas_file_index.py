from contextlib import nullcontext as does_not_raise_exception

import pytest

from pyaerocom.io import ebas_file_index as mod

from ..conftest import EBAS_SQLite_DB


def test_EbasSQLRequest___init__():
    mod.EbasSQLRequest()


@pytest.mark.parametrize(
    "var,output,raises",
    [
        ("bla", "('bla')", does_not_raise_exception()),
        ({}, None, pytest.raises(ValueError)),
        (("bla", "blub"), "('bla', 'blub')", does_not_raise_exception()),
        (["bla", "blub"], "('bla', 'blub')", does_not_raise_exception()),
    ],
)
def test_EbasSQLRequest__var2sql(var, output, raises):
    with raises:
        req = mod.EbasSQLRequest()
        _val = req._var2sql(var)
        assert _val == output


@pytest.mark.parametrize(
    "kwargs,output",
    [
        (
            {},
            "select distinct filename from variable join station on station.station_code=variable.station_code;",
        ),
        (
            {"distinct": False},
            "select filename from variable join station on station.station_code=variable.station_code;",
        ),
    ],
)
def test_EbasSQLRequest_make_file_query_str(kwargs, output):
    req = mod.EbasSQLRequest()
    _val = req.make_file_query_str(**kwargs)
    assert _val == output


@pytest.mark.parametrize(
    "kwargs,output",
    [
        (
            {
                "altitude_range": [10, 21],
                "lon_range": [10, 20],
                "lat_range": [10, 20],
                "start_date": "2010-01-21",
                "stop_date": "2010-01-24",
                "statistics": ["arithmetic_mean", "median"],
                "datalevel": 2,
            },
            (
                "select distinct filename from variable join station on "
                "station.station_code=variable.station_code where "
                "station_altitude>10 and station_altitude<21 and "
                "station_longitude>10 and station_longitude<20 and "
                "station_latitude>10 and station_latitude<20 and "
                "first_end < '2010-01-24' and last_start > '2010-01-21' and "
                "statistics in ('arithmetic_mean', 'median') and datalevel=2;"
            ),
        ),
        (
            {},
            "select distinct filename from variable join station on station.station_code=variable.station_code;",
        ),
        (
            {"distinct": False},
            "select filename from variable join station on station.station_code=variable.station_code;",
        ),
        (
            {"what": ("filename", "station_code", "bla")},
            "select distinct filename,station_code,bla from variable join station on station.station_code=variable.station_code;",
        ),
    ],
)
def test_EbasSQLRequest_make_query_str(kwargs, output):
    req = mod.EbasSQLRequest()
    _val = req.make_query_str(**kwargs)
    assert _val == output


def test_EbasSQLRequest___str__():
    assert isinstance(str(mod.EbasSQLRequest()), str)


def test_EbasFileIndex___init__():
    mod.EbasFileIndex()


def test_EbasFileIndex_database_getter():
    ebas = mod.EbasFileIndex()
    with pytest.raises(AttributeError):
        assert ebas.database == ebas._database


def test_EbasFileIndex_ALL_STATION_NAMES():
    ebas = mod.EbasFileIndex(EBAS_SQLite_DB)
    assert isinstance(ebas.ALL_STATION_NAMES, list)


def test_EbasFileIndex_ALL_STATION_CODES():
    ebas = mod.EbasFileIndex(EBAS_SQLite_DB)
    assert isinstance(ebas.ALL_STATION_CODES, list)


def test_EbasFileIndex_ALL_STATISTICS_PARAMS():
    ebas = mod.EbasFileIndex(EBAS_SQLite_DB)
    assert isinstance(ebas.ALL_STATISTICS_PARAMS, list)


def test_EbasFileIndex_ALL_VARIABLES():
    ebas = mod.EbasFileIndex(EBAS_SQLite_DB)
    assert isinstance(ebas.ALL_VARIABLES, list)


def test_EbasFileIndex_ALL_MATRICES():
    ebas = mod.EbasFileIndex(EBAS_SQLite_DB)
    assert isinstance(ebas.ALL_MATRICES, list)


def test_EbasFileIndex_ALL_INSTRUMENTS():
    ebas = mod.EbasFileIndex(EBAS_SQLite_DB)
    assert isinstance(ebas.ALL_INSTRUMENTS, list)


def test_EbasFileIndex_get_table_names():
    ebas = mod.EbasFileIndex(EBAS_SQLite_DB)
    assert ebas.get_table_names() == ["station", "variable"]


table_comulns = dict(
    station=[
        "station_code",
        "platform_code",
        "station_name",
        "station_wdca_id",
        "station_gaw_name",
        "station_gaw_id",
        "station_airs_id",
        "station_other_ids",
        "station_state_code",
        "station_landuse",
        "station_setting",
        "station_gaw_type",
        "station_wmo_region",
        "station_latitude",
        "station_longitude",
        "station_altitude",
    ],
    variable=[
        "station_code",
        "matrix",
        "comp_name",
        "statistics",
        "instr_type",
        "instr_ref",
        "method",
        "first_start",
        "first_end",
        "last_start",
        "last_end",
        "revdate",
        "period",
        "resolution",
        "datalevel",
        "filename",
    ],
)


@pytest.mark.parametrize("table,column_names", table_comulns.items())
def test_EbasFileIndex_get_column_names(table, column_names):
    ebas = mod.EbasFileIndex(EBAS_SQLite_DB)
    assert ebas.get_table_columns(table) == column_names
