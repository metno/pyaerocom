# ToDo: merge with test_coldatatojson_helpers.py
from __future__ import annotations

import numpy as np
import pytest
import xarray

from pyaerocom import ColocatedData, TsType
from pyaerocom.aeroval.coldatatojson_helpers import (
    _create_diurnal_weekly_data_object,
    _get_jsdate,
    _get_period_keys,
    _init_data_default_frequencies,
    _init_meta_glob,
    _make_trends,
    _map_indices,
    _process_statistics_timeseries,
    get_heatmap_filename,
    get_json_mapname,
    get_profile_filename,
    get_stationfile_name,
    get_timeseries_file_name,
)
from pyaerocom.exceptions import AeroValTrendsError, TemporalResolutionError, UnknownRegion
from tests.fixtures.collocated_data import COLDATA


def test_get_heatmap_filename():
    assert get_heatmap_filename("daily") == "glob_stats_daily.json"


def test_get_timeseries_filename():
    assert get_timeseries_file_name("reg1", "obs1", "var1", "vert1") == "reg1-obs1-var1-vert1.json"


def test_get_stationfile_name():
    json = get_stationfile_name("stat1", "obs1", "var1", "Column")
    assert json == "stat1_obs1-var1_Column.json"


def test_get_json_mapname():
    json = get_json_mapname("obs1", "var1", "mod1", "var1", "Column", "period")
    assert json == "obs1-var1_Column_mod1-var1_period.json"


def get_profile_filename():
    json = get_profile_filename("reg1", "obs1", "var1")
    assert json == "reg1_obs1_var1.json"


@pytest.mark.parametrize(
    "to_ts_types",
    [
        ["daily", "monthly"],
        ["3yearly"],
    ],
)
@pytest.mark.parametrize("coldataset", ["tm5_aeronet"])
def test__init_data_default_frequencies(coldata: ColocatedData, to_ts_types: str):
    result = _init_data_default_frequencies(coldata, to_ts_types)
    assert len(result) == len(to_ts_types)

    tst = TsType(coldata.ts_type)
    for freq, val in result.items():
        if TsType(freq) > tst:
            assert val is None
        else:
            assert isinstance(val, ColocatedData)
            assert val.ts_type == freq


@pytest.fixture(scope="module")
def example_coldata():
    """dictionary of colocated data statistics"""
    return _init_data_default_frequencies(COLDATA["tm5_aeronet"](), ["daily", "monthly", "yearly"])


def test_get_jsdate(example_coldata):
    time = _get_jsdate(example_coldata["monthly"].data.time.values)
    assert len(time) == 12


@pytest.mark.parametrize(
    "freq,region_ids,data_freq,nmb_avg",
    [
        ("yearly", {"EUROPE": "Europe"}, "monthly", 0.168),
        ("yearly", {"EUROPE": "Europe"}, None, 0.122),
        ("monthly", {"EUROPE": "Europe"}, None, 0.181),
        ("monthly", {"EUR": "Europe(HTAP)"}, None, 0.181),
        ("monthly", {"SEA": "SE Asia(HTAP)"}, None, np.nan),
        ("monthly", {"SEA": "SE Asia(HTAP)", "EUR": "Europe(HTAP)"}, None, 0.181),
        ("monthly", {}, None, np.nan),
    ],
)
@pytest.mark.filterwarnings("ignore:Mean of empty slice:RuntimeWarning")
def test__process_statistics_timeseries(
    example_coldata, freq: str, region_ids: dict[str, str], data_freq: str, nmb_avg
):
    result = _process_statistics_timeseries(
        example_coldata, freq, region_ids, False, False, data_freq
    )
    assert len(result) == len(region_ids)
    biases = [np.nan]
    for data in result.values():
        for stats in data.values():
            biases.append(stats["nmb"])
    mean_bias = np.nanmean(biases)
    assert mean_bias == pytest.approx(nmb_avg, abs=0.001, nan_ok=True)


@pytest.mark.parametrize(
    "freq,region_ids,data_freq,exception,error",
    [
        pytest.param(
            "monthly",
            {"bla": "blub"},
            None,
            UnknownRegion,
            "no such region defined bla",
            id="unknown region",
        ),
        pytest.param(
            "daily",
            {},
            "daily",
            TemporalResolutionError,
            "failed to compute statistics timeseries, no co-located data available in specified base resolution daily",
            id="no daily data",
        ),
        pytest.param(
            "daily",
            {},
            "monthly",
            TemporalResolutionError,
            "Desired input frequency monthly is lower than desired output frequency daily",
            id="wrong data_freq",
        ),
    ],
)
def test__process_statistics_timeseries_error(
    example_coldata,
    freq: str,
    region_ids: dict[str, str],
    data_freq: str,
    exception: type[Exception],
    error: str,
):
    with pytest.raises(exception) as e:
        _process_statistics_timeseries(example_coldata, freq, region_ids, False, False, data_freq)
    assert str(e.value) == error


@pytest.mark.parametrize(
    "freq,season,start,stop,min_yrs,station",
    [
        ("yearly", "all", 2000, 2015, 7, 1),
        ("yearly", "JJA", 2010, 2015, 4, 2),
        ("yearly", "SON", 2000, 2015, 7, 3),
        ("monthly", "all", 2000, 2015, 7, 2),
        ("monthly", "all", 2010, 2015, 4, 0),
    ],
)
@pytest.mark.parametrize("coldataset", ["fake_3d_trends"])
def test__make_trends(
    coldata: ColocatedData,
    freq: str,
    season: str,
    start: int,
    stop: int,
    min_yrs: int,
    station: int,
):
    obs_val = coldata.data.data[0, :, station]
    mod_val = coldata.data.data[1, :, station]
    time = coldata.data.time

    obs_trend, mod_trend = _make_trends(obs_val, mod_val, time, freq, season, start, stop, min_yrs)

    assert obs_trend["period"] == f"{start}-{stop}"
    assert mod_trend["period"] == f"{start}-{stop}"

    assert obs_trend["season"] == mod_trend["season"]

    trend_slops = [1, 2, 50, -3]

    eps = 0.1
    assert abs((obs_trend["m"] - trend_slops[station]) / obs_trend["m"]) < eps
    assert abs((mod_trend["m"] - trend_slops[station]) / mod_trend["m"]) < eps

    assert int(obs_trend["map_var"].split("_")[1]) == start
    assert int(mod_trend["map_var"].split("_")[1]) == start


@pytest.mark.parametrize(
    "freq,season,min_yrs,exception,error",
    [
        pytest.param(
            "daily",
            "JJA",
            4,
            ValueError,
            "daily",
            id="wrong freq",
        ),
        pytest.param(
            "yearly",
            "all",
            7,
            AeroValTrendsError,
            "min_yrs (7) larger than time between start and stop",
            id="wrong min_yrs",
        ),
    ],
)
@pytest.mark.parametrize("coldataset", ["fake_3d_trends"])
def test__make_trends_error(
    coldata: ColocatedData,
    freq: str,
    season: str,
    min_yrs: int,
    exception: type[Exception],
    error: str,
):
    obs_val = coldata.data.data[0, :, 0]
    mod_val = coldata.data.data[1, :, 0]
    time = coldata.data.time
    with pytest.raises(exception) as e:
        _make_trends(obs_val, mod_val, time, freq, season, 2010, 2015, min_yrs)
    assert str(e.value) == error


@pytest.mark.parametrize("coldataset", ["fake_3d_trends"])
def test__init_meta_glob(coldata: ColocatedData):
    # test the functionality of __init_meta_glob when there are KeyErrors. Other cases already covered
    no_meta_coldata = coldata.copy()
    no_meta_coldata.data.attrs = {}
    res = _init_meta_glob(no_meta_coldata)
    res.pop("processed_utc")
    assert np.all(value == "UNDEFINED" for value in res.values())


@pytest.mark.parametrize(
    "resolution",
    [
        ("yearly"),
        ("seasonal"),
        ("cat"),
    ],
)
@pytest.mark.parametrize("coldataset", ["fake_3d_trends"])
def test__create_diurnal_weekly_data_object(coldata: ColocatedData, resolution: str):
    try:
        obj = _create_diurnal_weekly_data_object(coldata, resolution)
        assert isinstance(obj, xarray.Dataset)
    except:
        with pytest.raises(ValueError) as e:
            _create_diurnal_weekly_data_object(coldata, resolution)
        assert e.type is ValueError


@pytest.mark.parametrize(
    "resolution",
    [
        ("seasonal"),
        ("yearly"),
    ],
)
def test__get_period_keys(resolution: str):
    res = _get_period_keys(resolution)
    assert np.all(isinstance(item, str) for item in res)


def test__map_indices():
    outer_idx = [2010, 2011, 2012, 2013, 2014, 2015]
    inner_idx = [2011, 2012]
    out = _map_indices(outer_idx, inner_idx)
    assert isinstance(out, np.ndarray)
    assert len(out) == len(outer_idx)
