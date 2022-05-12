import numpy as np
import pandas as pd
import pytest
import xarray as xr
from iris.cube import Cube

from pyaerocom import GriddedData, TsType
from pyaerocom.helpers import resample_time_dataarray, resample_timeseries
from pyaerocom.time_resampler import TimeResampler

# get default resampling "min_num_obs"
min_num_obs_default = {
    "yearly": {"monthly": 3},
    "monthly": {"daily": 7},
    "daily": {"hourly": 6},
    "hourly": {"minutely": 15},
}

# get stricter constraints (from Hans issue)
min_num_obs_custom = {
    "yearly": {"monthly": 9},
    "monthly": {"weekly": 3},
    "weekly": {"daily": 5},
    "daily": {"hourly": 18},
    "hourly": {"minutely": 45},
}


@pytest.fixture(scope="module")
def fakedata_hourly():
    idx = pd.date_range(start="1-1-2010 00:00:00", end="1-13-2010 23:59:59", freq="h")

    data = np.sin(range(len(idx)))
    data[44:65] = np.nan
    return pd.Series(data, idx)


@pytest.mark.parametrize(
    "data",
    [
        pytest.param(np.asarray([1]), id="np.array"),
        pytest.param(GriddedData(), id="GriddedData"),
        pytest.param(Cube([]), id="Cube"),
    ],
)
def test_TimeResampler_invalid_input_data(data):
    tr = TimeResampler()
    with pytest.raises(ValueError) as e:
        tr.input_data = data
    assert str(e.value) == "Invalid input: need Series or DataArray"


@pytest.mark.parametrize(
    "data,resampler_function",
    [
        pytest.param(pd.Series(dtype=np.float64), resample_timeseries, id="pd.Series"),
        pytest.param(xr.DataArray(), resample_time_dataarray, id="xr.DataArray"),
    ],
)
def test_TimeResampler_fun(data, resampler_function):
    tr = TimeResampler()
    tr.input_data = data
    assert tr.fun == resampler_function


@pytest.mark.parametrize(
    "kwargs,index",
    [
        pytest.param(
            dict(
                from_ts_type=TsType("3hourly"),
                to_ts_type=TsType("monthly"),
                min_num_obs=min_num_obs_default,
                how=dict(monthly={"daily": "max"}),
            ),
            [("daily", 2, "mean"), ("monthly", 7, "max")],
            id="3hourly to monthly",
        ),
        pytest.param(
            dict(
                from_ts_type=TsType("84hourly"),
                to_ts_type=TsType("6daily"),
                min_num_obs={"daily": {"minutely": 12}},
                how="median",
            ),
            [("6daily", 0, "median")],
            id="84hourly to 6daily",
        ),
        pytest.param(
            dict(
                from_ts_type=TsType("84hourly"),
                to_ts_type=TsType("6daily"),
                min_num_obs={"daily": {"hourly": 12}},
                how="median",
            ),
            [("6daily", 1, "median")],
            id="84hourly to 6daily",
        ),
        pytest.param(
            dict(
                from_ts_type=TsType("hourly"),
                to_ts_type=TsType("daily"),
                min_num_obs=3,
                how="median",
            ),
            [("daily", 3, "median")],
            id="hourly to daily",
        ),
        pytest.param(
            dict(
                from_ts_type=TsType("3hourly"),
                to_ts_type=TsType("monthly"),
                min_num_obs=3,
                how="mean",
            ),
            [("monthly", 3, "mean")],
            id="3hourly to monthly",
        ),
        pytest.param(
            dict(
                from_ts_type=TsType("3hourly"),
                to_ts_type=TsType("monthly"),
                min_num_obs=min_num_obs_default,
                how="mean",
            ),
            [("daily", 2, "mean"), ("monthly", 7, "mean")],
            id="3hourly to monthly",
        ),
        pytest.param(
            dict(
                from_ts_type=TsType("2daily"),
                to_ts_type=TsType("weekly"),
                min_num_obs=min_num_obs_custom,
                how="max",
            ),
            [("weekly", 2, "max")],
            id="2daily to weekly",
        ),
    ],
)
def test_TimeResampler__gen_index(kwargs, index):
    tr = TimeResampler()
    assert tr._gen_idx(**kwargs) == index


@pytest.mark.parametrize(
    "kwargs,output_len,output_numnotnan,lup",
    [
        pytest.param(
            dict(to_ts_type="monthly", from_ts_type="hourly"),
            1,
            1,
            True,
            id="monthly from hourly",
        ),
        pytest.param(
            dict(
                to_ts_type="monthly",
                from_ts_type="hourly",
                how="median",
                min_num_obs=min_num_obs_default,
            ),
            1,
            1,
            True,
            id="monthly from hourly, median",
        ),
        pytest.param(
            dict(
                to_ts_type="monthly",
                from_ts_type="hourly",
                how="median",
                min_num_obs=min_num_obs_custom,
            ),
            1,
            0,
            True,
            id="monthly from hourly, median",
        ),
        pytest.param(
            dict(to_ts_type="monthly", from_ts_type="hourly", how="median"),
            1,
            1,
            True,
            id="monthly from hourly, median",
        ),
        pytest.param(
            dict(
                to_ts_type="monthly",
                from_ts_type="hourly",
                how=dict(daily=dict(hourly="sum")),
                min_num_obs=min_num_obs_custom,
            ),
            1,
            0,
            False,
            id="monthly from hourly, hourly sum",
        ),
        pytest.param(
            dict(
                to_ts_type="monthly",
                from_ts_type="hourly",
                how=dict(monthly=dict(daily="sum"), daily=dict(hourly="max")),
                min_num_obs=dict(monthly=dict(daily=15), daily=dict(hourly=1)),
            ),
            1,
            0,
            False,
            id="monthly from hourly, hourly max",
        ),
        pytest.param(
            dict(to_ts_type="daily", from_ts_type="hourly", how="median"),
            13,
            13,
            True,
            id="daily from hourly, median",
        ),
        pytest.param(
            dict(
                to_ts_type="daily",
                from_ts_type="hourly",
                how="median",
                min_num_obs=min_num_obs_default,
            ),
            13,
            13,
            True,
            id="daily from hourly, median",
        ),
        pytest.param(
            dict(
                to_ts_type="daily",
                from_ts_type="hourly",
                how="median",
                min_num_obs=min_num_obs_custom,
            ),
            13,
            12,
            True,
            id="daily from hourly, median",
        ),
    ],
)
def test_TimeResampler_resample(fakedata_hourly, kwargs, output_len, output_numnotnan, lup):
    tr = TimeResampler(input_data=fakedata_hourly)
    ts = tr.resample(**kwargs)
    assert len(ts) == output_len
    notnan = ~np.isnan(ts)
    assert notnan.sum() == output_numnotnan
    assert tr.last_units_preserved == lup
