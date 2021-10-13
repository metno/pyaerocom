import numpy as np
import numpy.testing as npt
import pandas as pd
import pytest
import xarray as xr

from pyaerocom import StationData, helpers
from pyaerocom.exceptions import DataCoverageError, TemporalResolutionError, UnitConversionError

from .conftest import does_not_raise_exception


def test_get_standarad_name():
    assert (helpers.get_standard_name('od550aer') ==
            'atmosphere_optical_thickness_due_to_ambient_aerosol_particles')

def test_get_standard_unit():
    assert helpers.get_standard_unit('ec550aer') == '1/Mm'

def test_get_lowest_resolution():
    assert helpers.get_lowest_resolution('3hourly',
                                         'hourly',
                                         'monthly',
                                         'yearly') == 'yearly'
@pytest.mark.parametrize('val', [3, 3.3455, complex(1,2)])
def test_isnumeric(val):
    assert helpers.isnumeric(val)

@pytest.mark.parametrize('val,result', [
    ((0, 1), True),
    ([10,20], True),
    ([10,20,30], False),
    ])
def test_isrange(val,result):
    assert helpers.isrange(val) == result

@pytest.mark.parametrize('use,var_name,pref_attr,sort_by_largest,fill_missing_nan,add_meta_keys,raises,num,tst,mean', [
    ('concpm10', 'concpm10',None,True,True,None,does_not_raise_exception(),730,'daily',17.93),
    ('concpm10', 'concpm10','awesomeness',True,True,None,does_not_raise_exception(),730,'daily',17.93),
    ('concpm10', 'concpm10','awesomeness',False,True,None,does_not_raise_exception(),730,'daily',15),
    ('concpm10_X2', 'concpm10',None,True,True,None,pytest.raises(UnitConversionError),None,None,None),
    ('all', 'concpm10',None,True,True,None,pytest.raises(TemporalResolutionError),None,None,None),
    ('concpm10_X', 'concpm10',None,True,True,None,pytest.raises(TemporalResolutionError),None,None,None),
    ('od550aer', 'od550aer',None,True,True,None,does_not_raise_exception(),67,'60daily',0.51),
    ('od550aer', 'od550aer','awesomeness',True,True,None,does_not_raise_exception(),67,'60daily',0.59),
    ('od550aer', 'od550aer','awesomeness',False,True,None,does_not_raise_exception(),67,'60daily',0.51),
    ('od550aer', 'concpm10',None,True,True,None,pytest.raises(DataCoverageError),None,None,None),

    ])
def test_merge_station_data(statlist,use,var_name,pref_attr,sort_by_largest,fill_missing_nan,add_meta_keys,raises,num,tst,mean):
    with raises:
        stats = [x.copy() for x in statlist[use]]
        stat = helpers.merge_station_data(stats,var_name,pref_attr,
                                   sort_by_largest,fill_missing_nan,
                                   add_meta_keys)
        assert isinstance(stat, StationData)
        vardata = stat[var_name]
        assert len(vardata) == num
        assert stat.get_var_ts_type(var_name) == tst
        avg = np.mean(vardata)
        npt.assert_allclose(avg, mean, rtol=1e-2)

def test__get_pandas_freq_and_loffset():
    val = helpers._get_pandas_freq_and_loffset('monthly')
    assert val == ('MS', '14D')

@pytest.fixture(scope='module')
def fake_hourly_ts():
    time = pd.date_range('2018-01-10T00:00:00', '2018-01-17T23:59:00', freq='h')
    xrange_modulation = np.linspace(0,np.pi*40, len(time))
    signal = np.sin(xrange_modulation)
    return pd.Series(signal, time)

@pytest.mark.parametrize('freq, how, min_num_obs, num, avg', [
    ('daily', 'mean', 10000, 8, np.nan),
    ('daily', '50percentile', 10000, 8, np.nan),
    ('daily', 'mean', 23, 8, 0),
    ('daily', '50percentile', 23, 8, 0),
    ('yearly', '50percentile', 23, 1, 0),
    ('yearly', '50percentile', 192, 1, 0),
    ('daily', '50percentile', None, 8, 0),
    ('yearly', '50percentile', 193, 1, np.nan),
    ('daily', 'median', None, 8, 0.0),
    ('monthly', 'mean', None, 1, 0),
    ('daily', 'mean', None, 8, 0),
    ('daily', '1percentile', None, 8, -1),
    ('daily', '25percentile', None, 8, -0.64),
    ('daily', '75percentile', None, 8, 0.64),
    ])
def test_resample_timeseries(fake_hourly_ts, freq, how, min_num_obs, num, avg):

    s1 = helpers.resample_timeseries(fake_hourly_ts, freq=freq, how=how,
                                     min_num_obs=min_num_obs)
    _avg = np.nanmean(s1)
    npt.assert_allclose(_avg, avg, atol=1e-2)
    assert len(s1) == num

def test_same_meta_dict():
    d1 = dict(station_name='bla',
              station_id='blub',
              latitude=33,
              longitude=15,
              altitude=400,
              PI='pi1')
    d2 = dict(station_name='bla',
              station_id='blub1',
              latitude=33,
              longitude=15,
              altitude=401,
              PI='pi2')

    assert helpers.same_meta_dict(d1, d2) == False

def test_to_pandas_timestamp():
    pass

def test_to_datetime64():
    pass

def test_is_year():
    assert helpers.is_year(2010)

def test_start_stop():
    pass

def test_datetime2str():
    pass
def test_start_stop_str():
    pass

def test_start_stop_from_year():
    start, stop = helpers.start_stop_from_year(2000)
    assert start == pd.Timestamp('2000')
    assert stop == pd.Timestamp('2000-12-31 23:59:59')

@pytest.mark.parametrize(
    'input,expected', [
        ('20100101', '20100101'),
        (helpers.to_pandas_timestamp('20100101'), '20100101')
    ])
def test_to_datestring_YYYYMMDD(input, expected):
    assert helpers.to_datestring_YYYYMMDD(input) == expected

def test_cftime_to_datetime64():
    pass

def get_constraint():
    pass

def test_get_lat_rng_constraint():
    pass

def test_get_lon_rng_constraint():
    pass

def test_get_time_rng_constraint():
    pass

def test_extract_latlon_dataarray():
    cube = helpers.make_dummy_cube_latlon(lat_res_deg=1, lon_res_deg=1, lat_range=[10, 20], lon_range=[10, 20])
    data = xr.DataArray.from_iris(cube)
    # First coordinate does not exist in the dataarray.
    lat = [15, 15, 18]
    lon = [1, 15, 18]
    subset = helpers.extract_latlon_dataarray(data, lat, lon, check_domain=True)
    assert isinstance(subset, xr.DataArray)
    assert len(subset.lat) == len(lat) - 1 and len(subset.lon) == len(lon) -1

@pytest.mark.parametrize('lat,lon,expectation', [
    ([], [], pytest.raises(DataCoverageError)),
    ([1,2], [-1,2], pytest.raises(DataCoverageError)),
    ([15], [15], does_not_raise_exception())
    ])
def test_extract_latlon_dataarray_no_matches(lat, lon, expectation):
    cube = helpers.make_dummy_cube_latlon(lat_res_deg=1,
                                          lon_res_deg=1,
                                          lat_range=[10, 20],
                                          lon_range=[10, 20])
    data = xr.DataArray.from_iris(cube)
    with expectation:
        helpers.extract_latlon_dataarray(data, lat, lon, check_domain=True)

@pytest.mark.parametrize("date,ts_type,expected", [
    ("2000-02-18", "monthly", 29),  # February leap year
    ("2000-02-18", "yearly", 366),  # Leap year
    ("2001-02-18", "monthly", 28),  # February non leap year
    ("2001-02-18", "daily", 1),     # Daily
    ("2001-02-18", "yearly", 365)]) # Non leap year
def test_seconds_in_periods(date, ts_type, expected):
    seconds_in_day = 24*60*60
    ts = np.datetime64(date)
    seconds = helpers.seconds_in_periods(ts, ts_type)
    assert seconds == expected*seconds_in_day

if __name__ == "__main__":
    import sys
    pytest.main(sys.argv)
