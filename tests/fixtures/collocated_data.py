import numpy as np
import pandas as pd
import pytest

from pyaerocom import ColocatedData, Filter
from pyaerocom.config import ALL_REGION_NAME

from .data_access import DataForTests

CHECK_PATHS = f"coldata/od550aer_REF-AeronetSunV3L2Subset.daily_MOD-TM5_AP3-CTRL2016_20100101_20101231_monthly_{ALL_REGION_NAME}-noMOUNTAINS.nc"
EXAMPLE_FILE = DataForTests(CHECK_PATHS).path


def _create_fake_coldata_3d():
    var = "concpm10"
    filter_name = f"{ALL_REGION_NAME}-wMOUNTAINS"
    regfilter = Filter(name=filter_name)

    dtime = pd.date_range("2000-01-01", "2019-12-31", freq="MS") + np.timedelta64(14, "D")

    lats = [-80, 0, 70, 0.1]
    lons = [-150, 0, 100, 0.1]
    alts = [0, 100, 2000, 10]

    timenum = len(dtime)
    statnum = len(lats)
    c = 1
    statnames = []
    for lat in lats:
        statnames.append(f"FakeStation{c}")
        c += 1
    data = np.ones((2, timenum, statnum))
    xrange_modulation = np.linspace(0, np.pi * 40, timenum)
    data[1] += 0.1  # +10% model bias

    # 1. SITE: modify first site (sin , cos waves)
    data[0, :, 0] += np.sin(xrange_modulation)
    data[1, :, 0] += np.cos(xrange_modulation)  # phase shifted to obs

    years = dtime.year.values
    # 2. SITE: modify second site (yearly stepwise increase, double as
    # pronounced in obs than in model)
    c = 0
    for year in np.unique(years):
        mask = years == year
        data[0, mask, 1] += c * 0.4
        data[1, mask, 1] += c * 0.2

    # set the first and last 10 months of obs to NaN to violate 25% coverage
    # constraint of first and last year to test option annual_stats_constrained
    # in json conversion routines
    data[0, :10, 1] = np.nan
    data[0, -10:, 1] = np.nan

    # 3 SITE: add noise to model and obs
    data[0, :, 2] += np.random.rand(timenum)
    data[1, :, 2] += np.random.rand(timenum)

    meta = {
        "data_source": ["fakeobs", "fakemod"],
        "var_name": [var, var],
        "ts_type": "monthly",  # will be updated below if resampling
        "filter_name": filter_name,
        "ts_type_src": ["monthly", "daily"],
        "start_str": dtime[0].strftime("%Y%m%d"),
        "stop_str": dtime[-1].strftime("%Y%m%d"),
        "var_units": ["ug m-3", "ug m-3"],
        "vert_scheme": "surface",
        "data_level": 3,
        "revision_ref": "20210409",
        "from_files": [],
        "from_files_ref": None,
        "stations_ignored": None,
        "colocate_time": False,
        "obs_is_clim": False,
        "pyaerocom": "0.11.0",
        "min_num_obs": dict(monthly=dict(daily=15), daily=dict(hourly=12)),
        "resample_how": dict(monthly=dict(daily="sum"), daily=dict(hourly="max")),
    }

    meta.update(regfilter.to_dict())

    # create coordinates of DataArray
    coords = {
        "data_source": meta["data_source"],
        "time": dtime,
        "station_name": statnames,
        "latitude": ("station_name", lats),
        "longitude": ("station_name", lons),
        "altitude": ("station_name", alts),
    }

    dims = ["data_source", "time", "station_name"]
    cd = ColocatedData(data=data, coords=coords, dims=dims, name=var, attrs=meta)

    return cd


def _create_fake_trends_coldata_3d():
    var = "concpm10"
    filter_name = f"{ALL_REGION_NAME}-wMOUNTAINS"
    regfilter = Filter(name=filter_name)

    dtime = pd.date_range("2000-01-01", "2019-12-31", freq="MS") + np.timedelta64(14, "D")

    lats = [-80, 0, 70, 0.1]
    lons = [-150, 0, 100, 0.1]
    alts = [0, 100, 2000, 10]

    timenum = len(dtime)
    statnum = len(lats)

    statnames = [f"FakeStation{c}" for c in range(statnum)]

    data = np.ones((2, timenum, statnum))

    trend_slops = [1, 2, 50, -3]

    xs = np.linspace(0, 20, timenum)
    for i, s in enumerate(trend_slops):
        data[0, :, i] = s * xs
        data[1, :, i] = s * xs

    meta = {
        "data_source": ["fakeobs", "fakemod"],
        "var_name": [var, var],
        "ts_type": "monthly",  # will be updated below if resampling
        "filter_name": filter_name,
        "ts_type_src": ["monthly", "daily"],
        "start_str": dtime[0].strftime("%Y%m%d"),
        "stop_str": dtime[-1].strftime("%Y%m%d"),
        "var_units": ["ug m-3", "ug m-3"],
        "vert_scheme": "surface",
        "data_level": 3,
        "revision_ref": "20210409",
        "from_files": [],
        "from_files_ref": None,
        "stations_ignored": None,
        "colocate_time": False,
        "obs_is_clim": False,
        "pyaerocom": "0.11.0",
        "min_num_obs": dict(monthly=dict(daily=15), daily=dict(hourly=12)),
        "resample_how": dict(monthly=dict(daily="sum"), daily=dict(hourly="max")),
    }

    meta.update(regfilter.to_dict())

    # create coordinates of DataArray
    coords = {
        "data_source": meta["data_source"],
        "time": dtime,
        "station_name": statnames,
        "latitude": ("station_name", lats),
        "longitude": ("station_name", lons),
        "altitude": ("station_name", alts),
    }

    dims = ["data_source", "time", "station_name"]
    cd = ColocatedData(data=data, coords=coords, dims=dims, name=var, attrs=meta)

    return cd


def _create_fake_coldata_3d_hourly():
    var = "vmro3"
    filter_name = f"{ALL_REGION_NAME}-wMOUNTAINS"
    regfilter = Filter(name=filter_name)

    dtime = pd.date_range("2018-01-10T00:00:00", "2018-01-17T23:59:00", freq="h")

    lats = [-80]
    lons = [-150]
    alts = [10]

    timenum = len(dtime)
    statnum = len(lats)
    c = 1
    statnames = []
    for lat in lats:
        statnames.append(f"FakeStation{c}")
        c += 1
    data = np.ones((2, timenum, statnum))
    xrange_modulation = np.linspace(0, np.pi * 40, timenum)
    signal = np.sin(xrange_modulation)
    data[1] += 0.1  # +10% model bias

    # 1. SITE: modify first site (sin , cos waves)
    data[0, :, 0] += signal
    data[1, :, 0] += signal
    data[0, :36, 0] = np.nan  # invalidate first 1.5 days in obs

    meta = {
        "data_source": ["fakeobs", "fakemod"],
        "var_name": [var, var],
        "ts_type": "hourly",
        "filter_name": filter_name,
        "var_units": ["nmole mole-1", "nmole mole-1"],
        "min_num_obs": dict(hourly=dict(minutely=15), minutely=dict(secondly=15)),
    }

    meta.update(regfilter.to_dict())

    # create coordinates of DataArray
    coords = {
        "data_source": meta["data_source"],
        "time": dtime,
        "station_name": statnames,
        "latitude": ("station_name", lats),
        "longitude": ("station_name", lons),
        "altitude": ("station_name", alts),
    }

    dims = ["data_source", "time", "station_name"]
    cd = ColocatedData(data=data, coords=coords, dims=dims, name=var, attrs=meta)

    return cd


def _create_fake_partial_trends_coldata_3d(colocate_time: bool = False):
    var = "concpm10"
    filter_name = "ALL-wMOUNTAINS"
    regfilter = Filter(name=filter_name)

    dtime1 = pd.date_range("2000", "2001", freq="D")
    dtime2 = pd.date_range("2003", "2006", freq="D")
    dtime3 = pd.date_range("2006", "2009", freq="D")
    dtime4 = pd.date_range("2011", "2013", freq="D")
    dtime_partial = dtime1.union(dtime2).union(dtime3).union(dtime4)

    dtimes = [dtime1, dtime2, dtime_partial, dtime4, dtime_partial]

    lats = [-80, 0, 70, 0.1, 0]
    lons = [-150, 0, 100, 0.1, 3]
    alts = [0, 100, 2000, 10, 0]

    timenum = len(dtime_partial)
    statnum = len(lats)

    statnames = [f"FakeStation{c}" for c in range(statnum)]

    data = np.ones((2, timenum, statnum))

    for i in range(len(statnames)):
        data[1, :, i] = 1
        for j, d in enumerate(dtime_partial):
            if d in dtimes[i]:
                data[0, j, i] = 1
            else:
                data[0, j, i] = np.nan

    meta = {
        "data_source": ["fakeobs", "fakemod"],
        "var_name": [var, var],
        "ts_type": "monthly",
        "filter_name": filter_name,
        "ts_type_src": ["monthly", "daily"],
        "start_str": dtime_partial[0].strftime("%Y%m%d"),
        "stop_str": dtime_partial[-1].strftime("%Y%m%d"),
        "var_units": ["ug m-3", "ug m-3"],
        "vert_scheme": "surface",
        # "data_level": 3,
        # "revision_ref": "20210409",
        "from_files": [],
        "from_files_ref": None,
        "stations_ignored": None,
        "colocate_time": colocate_time,
        "obs_is_clim": False,
        "pyaerocom": "0.21.0.dev0",
        "min_num_obs": dict(monthly=dict(daily=15), daily=dict(hourly=12)),
        "resample_how": dict(monthly=dict(daily="sum"), daily=dict(hourly="max")),
    }

    meta.update(regfilter.to_dict())

    # create coordinates of DataArray
    coords = {
        "data_source": meta["data_source"],
        "time": dtime_partial,
        "station_name": statnames,
        "latitude": ("station_name", lats),
        "longitude": ("station_name", lons),
        "altitude": ("station_name", alts),
    }

    dims = ["data_source", "time", "station_name"]
    cd = ColocatedData(data=data, coords=coords, dims=dims, name=var, attrs=meta)

    return cd


def _create_fake_partial_trends_coldata_3d_coltime():
    return _create_fake_partial_trends_coldata_3d(True)


def _create_fake_partial_trends_coldata_3d_no_coltime():
    return _create_fake_partial_trends_coldata_3d()


def _create_fake_timeseries_hourly():
    cd = _create_fake_coldata_3d_hourly()
    obs = cd.data.data[0, :, 0]
    return pd.Series(obs, index=cd.data.time.data)


def _create_fake_coldata_4d():
    _lats_fake = np.arange(30, 60, 10)
    _lons_fake = np.arange(10, 30, 10)
    _time_fake = pd.date_range("2010-01", "2010-03", freq="MS")
    _data_fake = np.ones((2, len(_time_fake), len(_lats_fake), len(_lons_fake)))

    coords = {
        "data_source": ["obs", "mod"],
        "time": _time_fake,
        "latitude": _lats_fake,
        "longitude": _lons_fake,
    }

    dims = ["data_source", "time", "latitude", "longitude"]
    # set some obs vals NaN
    _data_fake[0, :, 1, 1] = np.nan
    _data_fake[0, 0, 0, 0] = np.nan
    meta = {"ts_type": "monthly"}
    return ColocatedData(data=_data_fake, coords=coords, dims=dims, attrs=meta)


COLDATA = dict(
    tm5_aeronet=lambda: ColocatedData(data=str(EXAMPLE_FILE)),
    fake_nodims=lambda: ColocatedData(data=np.ones((2, 1, 1))),
    fake_3d=_create_fake_coldata_3d,
    fake_4d=_create_fake_coldata_4d,
    fake_3d_hr=_create_fake_coldata_3d_hourly,
    fake_3d_trends=_create_fake_trends_coldata_3d,
    fake_3d_partial_trends_coltime=_create_fake_partial_trends_coldata_3d_coltime,
    fake_3d_partial_trends=_create_fake_partial_trends_coldata_3d_no_coltime,
)


@pytest.fixture
def coldata(coldataset: str) -> ColocatedData:
    """dispatch ColocatedData depending on coldataset"""
    return COLDATA[coldataset]()
