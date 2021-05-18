# -*- coding: utf-8 -*-

import pytest
from pyaerocom.io import ebas_file_index as mod
from pyaerocom.conftest import does_not_raise_exception, EBAS_SQLite_DB

@pytest.mark.parametrize('args,kwargs,raises', [
    ([],{}, does_not_raise_exception())
    ])
def test_EbasSQLRequest___init__(args, kwargs, raises):
    with raises:
        mod.EbasSQLRequest(*args, **kwargs)


@pytest.mark.parametrize('var,output,raises', [
    ('bla', "('bla')", does_not_raise_exception()),
    ({}, None, pytest.raises(ValueError)),
    (('bla', 'blub'), "('bla', 'blub')", does_not_raise_exception()),
    (['bla', 'blub'], "('bla', 'blub')", does_not_raise_exception()),

    ])
def test_EbasSQLRequest__var2sql(var,output, raises):
    with raises:
        req = mod.EbasSQLRequest()
        _val = req._var2sql(var)
        assert _val == output

@pytest.mark.parametrize('kwargs,output,raises', [
    ({}, 'select distinct filename from variable join station on station.station_code=variable.station_code;',
     does_not_raise_exception()),
    ({'distinct': False}, 'select filename from variable join station on station.station_code=variable.station_code;',
     does_not_raise_exception())
    ])
def test_EbasSQLRequest_make_file_query_str(kwargs,output,raises):
    with raises:
        req = mod.EbasSQLRequest()
        _val = req.make_file_query_str(**kwargs)
        assert _val == output

@pytest.mark.parametrize('kwargs,output,raises', [
    ({'altitude_range' : [10,21],
      'lon_range' : [10, 20],
      'lat_range' : [10, 20],
      'start_date': '2010-01-21',
      'stop_date' : '2010-01-24',
      'statistics': ['arithmetic_mean', 'median'],
      'datalevel' : 2
      }, ("select distinct filename from variable join station on "
          "station.station_code=variable.station_code where "
          "station_altitude>10 and station_altitude<21 and "
          "station_longitude>10 and station_longitude<20 and "
          "station_latitude>10 and station_latitude<20 and "
          "first_end < '2010-01-24' and last_start > '2010-01-21' and "
          "statistics in ('arithmetic_mean', 'median') and datalevel=2;"),
     does_not_raise_exception()),
    ({}, 'select distinct filename from variable join station on station.station_code=variable.station_code;',
     does_not_raise_exception()),
    ({'distinct': False}, 'select filename from variable join station on station.station_code=variable.station_code;',
     does_not_raise_exception()),
    ({'what' : ('filename', 'station_code', 'bla')}, 'select distinct filename,station_code,bla from variable join station on station.station_code=variable.station_code;',
     does_not_raise_exception()),
    ])
def test_EbasSQLRequest_make_query_str(kwargs,output,raises):
    with raises:
        req = mod.EbasSQLRequest()
        _val = req.make_query_str(**kwargs)
        assert _val == output

def test_EbasSQLRequest___str__():
    assert isinstance(str(mod.EbasSQLRequest()), str)

@pytest.mark.parametrize('args,kwargs,raises', [
    ([],{}, does_not_raise_exception())
    ])
def test_EbasFileIndex___init__(args, kwargs, raises):
    with raises:
        mod.EbasFileIndex(*args, **kwargs)

@pytest.mark.parametrize('dbfile,raises', [
    (None, pytest.raises(AttributeError))
    ])
def test_EbasFileIndex_database_getter(dbfile,raises):
    with raises:
        idx = mod.EbasFileIndex(dbfile)
        assert idx.database == idx._database

def test_EbasFileIndex_ALL_STATION_NAMES():
    val = mod.EbasFileIndex(EBAS_SQLite_DB).ALL_STATION_NAMES
    assert isinstance(val, list)

def test_EbasFileIndex_ALL_STATION_CODES():
    val = mod.EbasFileIndex(EBAS_SQLite_DB).ALL_STATION_CODES
    assert isinstance(val, list)

def test_EbasFileIndex_ALL_STATISTICS_PARAMS():
    val = mod.EbasFileIndex(EBAS_SQLite_DB).ALL_STATISTICS_PARAMS
    assert isinstance(val, list)

def test_EbasFileIndex_ALL_VARIABLES():
    val = mod.EbasFileIndex(EBAS_SQLite_DB).ALL_VARIABLES
    assert isinstance(val, list)

def test_EbasFileIndex_ALL_MATRICES():
    val = mod.EbasFileIndex(EBAS_SQLite_DB).ALL_MATRICES
    assert isinstance(val, list)

def test_EbasFileIndex_ALL_INSTRUMENTS():
    val = mod.EbasFileIndex(EBAS_SQLite_DB).ALL_INSTRUMENTS
    assert isinstance(val, list)

def test_EbasFileIndex_get_table_names():
    val = mod.EbasFileIndex(EBAS_SQLite_DB).get_table_names()
    assert val == ['station', 'variable']

@pytest.mark.parametrize('table,names', [
    ('station', ['station_code', 'platform_code', 'station_name',
                 'station_wdca_id', 'station_gaw_name', 'station_gaw_id',
                 'station_airs_id', 'station_other_ids', 'station_state_code',
                 'station_landuse', 'station_setting', 'station_gaw_type',
                 'station_wmo_region', 'station_latitude',
                 'station_longitude', 'station_altitude']),
    ('variable', ['station_code', 'matrix', 'comp_name', 'statistics',
                  'instr_type', 'instr_ref', 'method', 'first_start',
                  'first_end', 'last_start', 'last_end', 'revdate',
                  'period', 'resolution', 'datalevel', 'filename'])

    ])
def test_EbasFileIndex_get_column_names(table,names):
    val = mod.EbasFileIndex(EBAS_SQLite_DB).get_table_columns(table)
    assert val == names

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
