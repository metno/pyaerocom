import os

import numpy as np
import pandas as pd
import xarray as xr

from pyaerocom import ColocatedData, Filter, StationData


def _load_coldata_tm5_aeronet_from_scratch(file_path):
    from xarray import open_dataarray

    from pyaerocom import ColocatedData

    arr = open_dataarray(file_path)
    if "_min_num_obs" in arr.attrs:
        info = {}
        for val in arr.attrs["_min_num_obs"].split(";")[:-1]:
            to, fr, num = val.split(",")
            if not to in info:
                info[to] = {}
            if not fr in info[to]:
                info[to][fr] = {}
            info[to][fr] = int(num)
        arr.attrs["min_num_obs"] = info
    cd = ColocatedData()
    cd.data = arr
    return cd


def create_fake_station_data(addvars, varinfo, varvals, start, stop, freq, meta):
    if isinstance(addvars, str):
        addvars = [addvars]
    stat = StationData()
    stat.update(**meta)
    dtime = pd.date_range(start, stop, freq=freq).values
    stat["dtime"] = dtime
    for var in addvars:
        if var in varinfo:
            stat.var_info[var] = varinfo[var]
        if isinstance(varvals, dict):
            val = varvals[var]
        else:
            val = varvals
        stat[var] = np.ones(len(dtime)) * val
    return stat


def create_fake_stationdata_list():
    stats = [
        create_fake_station_data(
            "concpm10",
            {"concpm10": {"units": "ug m-3"}},
            10,
            "2010-01-01",
            "2010-12-31",
            "d",
            {
                "awesomeness": 10,
                "data_revision": 20120101,
                "ts_type": "daily",
                "latitude": 42.001,
                "longitude": 20,
                "altitude": 0.1,
                "station_name": "FakeSite",
            },
        ),
        # overlaps with first one
        create_fake_station_data(
            "concpm10",
            {"concpm10": {"units": "ug m-3"}},
            20,
            "2010-06-01",
            "2011-12-31",
            "d",
            {
                "awesomeness": 12,
                "data_revision": 20110101,
                "ts_type": "daily",
                "latitude": 42.001,
                "longitude": 20,
                "altitude": 0.1,
                "station_name": "FakeSite",
            },
        ),
        # monthly, but missing ts_type and wrong unit
        create_fake_station_data(
            "concpm10",
            {"concpm10": {"units": "mole mole-1"}},
            20,
            "2014-01-01",
            "2015-12-31",
            "3MS",
            {
                "awesomeness": 2,
                "data_revision": 20140101,
                "latitude": 42.001,
                "longitude": 20,
                "altitude": 0.1,
                "station_name": "FakeSite",
            },
        ),
        # invalid ts_type
        create_fake_station_data(
            "concpm10",
            {"concpm10": {"units": "ug m-3"}},
            20,
            "1850",
            "2020",
            "1000d",
            {
                "awesomeness": 15,
                "data_revision": 20130101,
                "ts_type": "1000daily",
                "latitude": 42.001,
                "longitude": 20,
                "altitude": 0.1,
                "station_name": "FakeSite",
            },
        ),
        # new variable and monthly
        create_fake_station_data(
            "od550aer",
            {"od550aer": {"units": "1"}},
            1,
            "2005",
            "2012",
            "MS",
            {
                "awesomeness": 42,
                "data_revision": 20200101,
                "ts_type": "monthly",
                "latitude": 22.001,
                "longitude": 10,
                "altitude": 99,
                "station_name": "FakeSite",
            },
        ),
        create_fake_station_data(
            "od550aer",
            {"od550aer": {"units": "1"}},
            0.1,
            "2008",
            "2009",
            "60d",
            {
                "awesomeness": 46,
                "data_revision": 20200101,
                "ts_type": "60daily",
                "latitude": 22.001,
                "longitude": 10,
                "altitude": 100,
                "station_name": "FakeSite2",
            },
        ),
    ]

    stat_werr = create_fake_station_data(
        "od550aer",
        {"od550aer": {"units": "1"}},
        0.2,
        "2010",
        "2016",
        "10d",
        {
            "awesomeness": 30,
            "data_revision": 20200101,
            "ts_type": "10daily",
            "latitude": 22.001,
            "longitude": 10,
            "altitude": 100,
            "station_name": "FakeSite2",
        },
    )
    stat_werr.data_err["od550aer"] = np.ones(len(stat_werr.dtime)) * 9999
    stats.append(stat_werr)
    return stats


def _create_fake_coldata_3d():
    var = "concpm10"
    filter_name = "WORLD-wMOUNTAINS"
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
    filter_name = "WORLD-wMOUNTAINS"
    regfilter = Filter(name=filter_name)

    dtime = pd.date_range("2000-01-01", "2019-12-31", freq="MS") + np.timedelta64(14, "D")

    lats = [-80, 0, 70, 0.1]
    lons = [-150, 0, 100, 0.1]
    alts = [0, 100, 2000, 10]

    timenum = len(dtime)
    statnum = len(lats)

    statnames = [f"FakeStation{c}" for c in range(statnum)]

    data = np.ones((2, timenum, statnum))
    xrange_modulation = np.linspace(0, np.pi * 40, timenum)
    # data[1] += 0.1 #+10% model bias

    # Sets seed to always get same trends
    # np.random.seed(13)

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
    filter_name = "WORLD-wMOUNTAINS"
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


def _create_fake_coldata_5d():
    _lats_fake = [10, 20]
    _lons_fake = [42, 43]
    _time_fake = pd.date_range("2010-01", "2010-03", freq="MS")
    _wvl_fake = [100, 200, 300]
    _data_fake = np.ones((2, len(_time_fake), len(_lats_fake), len(_lons_fake), len(_wvl_fake)))

    coords = {
        "data_source": ["fakeobs", "fakemod"],
        "time": _time_fake,
        "latitude": _lats_fake,
        "longitude": _lons_fake,
        "wvl": _wvl_fake,
    }

    dims = ["data_source", "time", "latitude", "longitude", "wvl"]
    # set all NaN in one obs coordinate
    arr = xr.DataArray(data=_data_fake, coords=coords, dims=dims)
    cd = ColocatedData(np.ones((2, 2, 2)))
    cd.data = arr
    return cd


def _create_fake_MSCWCtm_data(numval=1, tst=None):
    if tst is None:
        tst = "monthly"
    from pyaerocom import TsType

    tbase = TsType(tst).cf_base_unit

    _lats_fake = np.linspace(30, 82, 10)
    _lons_fake = np.linspace(-25, 90, 15)
    # _time_fake = pd.date_range('2019-01','2019-06', freq=pd_freq)
    _time_fake = np.arange(10)
    timeattrs = {"units": f"{tbase} since 2000-01-01", "calendar": "gregorian"}
    sh = (len(_time_fake), len(_lats_fake), len(_lons_fake))
    _data_fake = numval * np.ones(sh)

    coords = {"time": ("time", _time_fake, timeattrs), "lat": _lats_fake, "lon": _lons_fake}

    dims = ["time", "lat", "lon"]

    arr = xr.DataArray(data=_data_fake, coords=coords, dims=dims)

    return arr


import iris
from cf_units import Unit


def make_dummy_cube_3D_daily(
    year=2010, daynum=365, lat_range=None, lon_range=None, value=1, dtype=float
):
    if lat_range is None:
        lat_range = (-30, 30)
    if lon_range is None:
        lon_range = (-10, 10)
    lat_res_deg = lon_res_deg = 5
    times = np.arange(daynum)
    startstr = f"days since {year}-01-01 00:00"
    time_unit = Unit(startstr, calendar="gregorian")

    lons = np.arange(lon_range[0] + lon_res_deg / 2, lon_range[1] + lon_res_deg / 2, lon_res_deg)
    lats = np.arange(lat_range[0] + lat_res_deg / 2, lat_range[1] + lat_res_deg / 2, lat_res_deg)

    latdim = iris.coords.DimCoord(
        lats, var_name="lat", standard_name="latitude", circular=False, units=Unit("degrees")
    )

    londim = iris.coords.DimCoord(
        lons, var_name="lon", standard_name="longitude", circular=False, units=Unit("degrees")
    )

    timedim = iris.coords.DimCoord(times, var_name="time", standard_name="time", units=time_unit)

    latdim.guess_bounds()
    londim.guess_bounds()
    vals = np.ones((len(times), len(lats), len(lons))) * value
    dummy = iris.cube.Cube(vals, units="1")

    dummy.add_dim_coord(latdim, 1)
    dummy.add_dim_coord(londim, 2)
    dummy.add_dim_coord(timedim, 0)
    dummy.var_name = "dummy_grid"

    dummy.data = dummy.data.astype(dtype)
    dummy.attributes["ts_type"] = "daily"
    for coord in dummy.coords():
        coord.points = coord.points.astype(dtype)
    return dummy


def make_griddeddata(var_name, units, ts_type, vert_code, name, **kwargs):
    cube = make_dummy_cube_3D_daily(**kwargs)
    cube.var_name = var_name
    cube.units = units
    from pyaerocom import GriddedData

    data = GriddedData(cube)
    data.metadata["data_id"] = name
    data.metadata["vert_code"] = vert_code
    if ts_type != "daily":
        data = data.resample_time(ts_type)
    return data


def add_dummy_model_data(var_name, units, ts_type, vert_code, tmpdir, name=None, **kwargs):
    if name is None:
        name = "DUMMY-MODEL"
    outdir = os.path.join(tmpdir, name, "renamed")
    os.makedirs(outdir, exist_ok=True)
    data = make_griddeddata(var_name, units, ts_type, vert_code, name=name, **kwargs)
    data.to_netcdf(out_dir=outdir)
    return outdir
