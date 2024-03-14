from __future__ import annotations

import pytest

from pyaerocom.io.ebas_file_index import EbasFileIndex, EbasSQLRequest


def test_EbasSQLRequest___init__():
    EbasSQLRequest()


@pytest.mark.parametrize(
    "var,output",
    [
        ("bla", "('bla')"),
        (("bla", "blub"), "('bla', 'blub')"),
        (["bla", "blub"], "('bla', 'blub')"),
    ],
)
def test_EbasSQLRequest__var2sql(var: str | tuple[str] | list[str], output: str):
    req = EbasSQLRequest()
    assert req._var2sql(var) == output


def test_EbasSQLRequest__var2sql_error():
    with pytest.raises(ValueError) as e:
        EbasSQLRequest()._var2sql({})
    assert str(e.value) == "Invalid value..."


@pytest.mark.parametrize(
    "kwargs,output",
    [
        (
            {},
            "select distinct filename from variable join station on station.station_code=variable.station_code and not exists (select * from characteristic where var_id=variable.var_id and ct_type='Fraction');",
        ),
        (
            {"distinct": False},
            "select filename from variable join station on station.station_code=variable.station_code and not exists (select * from characteristic where var_id=variable.var_id and ct_type='Fraction');",
        ),
    ],
)
def test_EbasSQLRequest_make_file_query_str(kwargs: dict, output: str):
    req = EbasSQLRequest()
    assert req.make_file_query_str(**kwargs) == output


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
def test_EbasSQLRequest_make_query_str(kwargs: dict, output: str):
    req = EbasSQLRequest()
    assert req.make_query_str(**kwargs) == output


def test_EbasSQLRequest___str__():
    assert isinstance(str(EbasSQLRequest()), str)


def test_EbasFileIndex___init__():
    EbasFileIndex()


def test_EbasFileIndex_database_getter():
    with pytest.raises(AttributeError) as e:
        EbasFileIndex().database
    error = "EBAS SQLite database file could not be located but is needed in EbasFileIndex class"
    assert str(e.value) == error


def test_EbasFileIndex_ALL_STATION_NAMES(ebas: EbasFileIndex):
    assert isinstance(ebas.ALL_STATION_NAMES, list)


def test_EbasFileIndex_ALL_STATION_CODES(ebas: EbasFileIndex):
    assert isinstance(ebas.ALL_STATION_CODES, list)


def test_EbasFileIndex_ALL_STATISTICS_PARAMS(ebas: EbasFileIndex):
    assert isinstance(ebas.ALL_STATISTICS_PARAMS, list)


def test_EbasFileIndex_ALL_VARIABLES(ebas: EbasFileIndex):
    assert isinstance(ebas.ALL_VARIABLES, list)


def test_EbasFileIndex_ALL_MATRICES(ebas: EbasFileIndex):
    assert isinstance(ebas.ALL_MATRICES, list)


def test_EbasFileIndex_ALL_INSTRUMENTS(ebas: EbasFileIndex):
    assert isinstance(ebas.ALL_INSTRUMENTS, list)


def test_EbasFileIndex_get_table_names(ebas: EbasFileIndex):
    # assert ebas.get_table_names() == ["station", "variable"]
    assert ebas.get_table_names() == ["station", "variable", "characteristic"]


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
        "var_id",
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
        "vnum",
    ],
    characteristic=[
        "var_id",
        "ct_type",
        "datatype",
        "val_int",
        "val_dbl",
        "val_chr",
    ],
)


@pytest.mark.parametrize("table,column_names", table_comulns.items())
def test_EbasFileIndex_get_column_names(ebas: EbasFileIndex, table: str, column_names: list[str]):
    assert ebas.get_table_columns(table) == column_names
