# -*- coding: utf-8 -*-

import pytest
from pyaerocom.io import ebas_file_index as mod
from pyaerocom.conftest import does_not_raise_exception

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
        idx = mod.EbasSQLRequest()
        _val = idx._var2sql(var)
        assert _val == output

@pytest.mark.parametrize('kwargs,output,raises', [
    ({}, 'select distinct filename from variable join station on station.station_code=variable.station_code;',
     does_not_raise_exception()),
    ({'distinct': False}, 'select filename from variable join station on station.station_code=variable.station_code;',
     does_not_raise_exception())
    ])
def test_EbasSQLRequest_make_file_query_str(kwargs,output,raises):
    with raises:
        idx = mod.EbasSQLRequest()
        _val = idx.make_file_query_str(**kwargs)
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
        idx = mod.EbasSQLRequest()
        _val = idx.make_query_str(**kwargs)
        assert _val == output

@pytest.mark.parametrize('args,kwargs,raises', [
    ([],{}, does_not_raise_exception())
    ])
def test_EbasFileIndex___init__(args, kwargs, raises):
    with raises:
        mod.EbasFileIndex(*args, **kwargs)
if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
