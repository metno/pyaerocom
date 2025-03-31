import numpy as np
import pandas as pd
import pytest
import xarray as xr

from pyaerocom import StationData, helpers
from pyaerocom.exceptions import DataCoverageError, TemporalResolutionError
from pyaerocom.units import UnitConversionError


def test_get_standarad_name():
    assert (
        helpers.get_standard_name("od550aer")
        == "atmosphere_optical_thickness_due_to_ambient_aerosol_particles"
    )


@pytest.mark.parametrize("val", [3, 3.3455, complex(1, 2)])
def test_isnumeric(val):
    assert helpers.isnumeric(val)


@pytest.mark.parametrize(
    "val,result",
    [
        ((0, 1), True),
        ([10, 20], True),
        ([10, 20, 30], False),
    ],
)
def test_isrange(val, result):
    assert helpers.isrange(val) == result


@pytest.mark.parametrize(
    "use,var_name,pref_attr,sort_by_largest,fill_missing_nan,add_meta_keys,num,tst,mean",
    [
        ("concpm10", "concpm10", None, True, True, None, 730, "daily", 17.93),
        ("concpm10", "concpm10", "awesomeness", True, True, None, 730, "daily", 17.93),
        ("concpm10", "concpm10", "awesomeness", False, True, None, 730, "daily", 15),
        ("od550aer", "od550aer", None, True, True, None, 67, "60daily", 0.51),
        ("od550aer", "od550aer", "awesomeness", True, True, None, 67, "60daily", 0.59),
        ("od550aer", "od550aer", "awesomeness", False, True, None, 67, "60daily", 0.51),
    ],
)
def test_merge_station_data(
    statlist,
    use,
    var_name,
    pref_attr,
    sort_by_largest,
    fill_missing_nan,
    add_meta_keys,
    num,
    tst,
    mean,
):
    stats = [x.copy() for x in statlist[use]]
    stat = helpers.merge_station_data(
        stats, var_name, pref_attr, sort_by_largest, fill_missing_nan, add_meta_keys
    )
    assert isinstance(stat, StationData)
    vardata = stat[var_name]
    assert len(vardata) == num
    assert stat.get_var_ts_type(var_name) == tst
    assert np.mean(vardata) == pytest.approx(mean, rel=1e-2)


@pytest.mark.parametrize(
    "use,exception,error",
    [
        ("concpm10_X2", UnitConversionError, "failed to convert unit from mole mole-1 to ug m-3"),
        ("concpm10_X", TemporalResolutionError, "Invalid input for ts_type daily"),
        ("od550aer", DataCoverageError, "All input stations must contain concpm10 data"),
    ],
)
def test_merge_station_data_error(statlist, use, exception, error):
    stats = [x.copy() for x in statlist[use]]
    with pytest.raises(exception) as e:
        helpers.merge_station_data(stats, "concpm10")
    assert str(e.value).startswith(error)


def test__get_pandas_freq_and_offset():
    val = helpers._get_pandas_freq_and_offset("monthly")
    assert val == ("MS", pd.Timedelta(14, "d"))


@pytest.fixture(scope="module")
def fake_hourly_ts():
    time = pd.date_range("2018-01-10T00:00:00", "2018-01-17T23:59:00", freq="h")
    xrange_modulation = np.linspace(0, np.pi * 40, len(time))
    signal = np.sin(xrange_modulation)
    return pd.Series(signal, time)


@pytest.mark.parametrize(
    "freq,how,min_num_obs,num,avg",
    [
        ("daily", "mean", 10000, 8, np.nan),
        ("daily", "50percentile", 10000, 8, np.nan),
        ("daily", "mean", 23, 8, 0),
        ("daily", "50percentile", 23, 8, 0),
        ("yearly", "50percentile", 23, 1, 0),
        ("yearly", "50percentile", 192, 1, 0),
        ("daily", "50percentile", None, 8, 0),
        ("yearly", "50percentile", 193, 1, np.nan),
        ("daily", "median", None, 8, 0.0),
        ("monthly", "mean", None, 1, 0),
        ("daily", "mean", None, 8, 0),
        ("daily", "1percentile", None, 8, -1),
        ("daily", "25percentile", None, 8, -0.64),
        ("daily", "75percentile", None, 8, 0.64),
    ],
)
@pytest.mark.filterwarnings("ignore:Mean of empty slice:RuntimeWarning")
def test_resample_timeseries(fake_hourly_ts, freq, how, min_num_obs, num, avg):
    s1 = helpers.resample_timeseries(fake_hourly_ts, freq=freq, how=how, min_num_obs=min_num_obs)
    assert len(s1) == num
    assert np.nanmean(s1) == pytest.approx(avg, abs=1e-2, nan_ok=True)


def test_same_meta_dict():
    d1 = dict(
        station_name="bla", station_id="blub", latitude=33, longitude=15, altitude=400, PI="pi1"
    )
    d2 = dict(
        station_name="bla", station_id="blub1", latitude=33, longitude=15, altitude=401, PI="pi2"
    )

    assert helpers.same_meta_dict(d1, d2) is False


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
    assert start == pd.Timestamp("2000")
    assert stop == pd.Timestamp("2000-12-31 23:59:59")


@pytest.mark.parametrize(
    "input,expected",
    [("20100101", "20100101"), (helpers.to_pandas_timestamp("20100101"), "20100101")],
)
def test_to_datestring_YYYYMMDD(input, expected):
    assert helpers.to_datestring_YYYYMMDD(input) == expected


def get_constraint():
    pass


def test_get_lat_rng_constraint():
    pass


def test_get_lon_rng_constraint():
    pass


def test_get_time_rng_constraint():
    pass


def test_extract_latlon_dataarray():
    cube = helpers.make_dummy_cube_latlon(
        lat_res_deg=1, lon_res_deg=1, lat_range=[10, 20], lon_range=[10, 20]
    )
    data = xr.DataArray.from_iris(cube)
    # First coordinate does not exist in the dataarray.
    lat = [15, 15, 18]
    lon = [1, 15, 18]
    subset = helpers.extract_latlon_dataarray(data, lat, lon, check_domain=True)
    assert isinstance(subset, xr.DataArray)
    assert len(subset.lat) == len(lat) - 1
    assert len(subset.lon) == len(lon) - 1


def test_extract_latlon_dataarray_no_matches():
    cube = helpers.make_dummy_cube_latlon(
        lat_res_deg=1, lon_res_deg=1, lat_range=[10, 20], lon_range=[10, 20]
    )
    data = xr.DataArray.from_iris(cube)
    helpers.extract_latlon_dataarray(data, [15], [15], check_domain=True)


@pytest.mark.parametrize(
    "lat,lon",
    [
        ([], []),
        ([1, 2], [-1, 2]),
    ],
)
def test_extract_latlon_dataarray_no_matches_error(lat, lon):
    cube = helpers.make_dummy_cube_latlon(
        lat_res_deg=1, lon_res_deg=1, lat_range=[10, 20], lon_range=[10, 20]
    )
    data = xr.DataArray.from_iris(cube)
    with pytest.raises(DataCoverageError) as e:
        helpers.extract_latlon_dataarray(data, lat, lon, check_domain=True)
    assert str(e.value) == "Coordinates not found in dataarray"


def test_make_dummy_cube():
    # make a dummy cube of an arbitrary variable name over one year
    cube = helpers.make_dummy_cube("concpm10", start_yr=2020, stop_yr=2021)
    data = xr.DataArray.from_iris(cube)
    # First coordinate does not exist in the dataarray.
    lat = [90, -67.5, 22.2]
    lon = [180, -135.0, 45.0]
    subset = helpers.extract_latlon_dataarray(data, lat, lon, check_domain=True)
    assert isinstance(subset, xr.DataArray)
    assert len(subset.lat) == len(lat) - 1
    assert len(subset.lon) == len(lon) - 1
