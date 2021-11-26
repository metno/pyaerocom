# ToDo: merge with test_coldatatojson_helpers.py
from __future__ import annotations

from typing import Type

import numpy as np
import pytest

import pyaerocom.aeroval.coldatatojson_helpers as mod
import pyaerocom.exceptions as exceptions
from pyaerocom import ColocatedData, TsType


def test_get_heatmap_filename():
    assert mod.get_heatmap_filename("daily") == "glob_stats_daily.json"


def test_get_stationfile_name():

    val = mod.get_stationfile_name("stat1", "obs1", "var1", "Column")
    assert val == "stat1_obs1-var1_Column.json"


def test_get_json_mapname():
    """Get name base name of json file"""
    val = mod.get_json_mapname("obs1", "var1", "mod1", "var1", "Column")
    assert val == "obs1-var1_Column_mod1-var1.json"


@pytest.mark.parametrize(
    "which,to_ts_types",
    [
        ("tm5_aeronet", ["daily", "monthly"]),
        ("tm5_aeronet", ["3yearly"]),
    ],
)
def test__init_data_default_frequencies(coldata, which, to_ts_types):
    data = coldata[which]
    result = mod._init_data_default_frequencies(data, to_ts_types)
    tst = TsType(data.ts_type)
    assert len(result) == len(to_ts_types)
    for freq, val in result.items():
        if TsType(freq) > tst:
            assert val is None
        else:
            assert isinstance(val, ColocatedData)
            assert val.ts_type == freq


@pytest.fixture(scope="module")
def example_coldata(coldata):
    return mod._init_data_default_frequencies(
        coldata["tm5_aeronet"], ["daily", "monthly", "yearly"]
    )


def test_get_jsdate(example_coldata):
    vals = mod._get_jsdate(example_coldata["monthly"].data.time.values)
    assert len(vals) == 12


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
    result = mod._process_statistics_timeseries(
        example_coldata, freq, region_ids, False, False, data_freq
    )
    assert len(result) == len(region_ids)
    biases = [np.nan]
    for data in result.values():
        for stats in data.values():
            biases.append(stats["nmb"])
    mean_bias = np.nanmean(biases)
    if np.isnan(nmb_avg):
        assert np.isnan(mean_bias)
    else:
        np.testing.assert_allclose(mean_bias, nmb_avg, atol=0.001)


@pytest.mark.parametrize(
    "freq,region_ids,data_freq,exception,error",
    [
        pytest.param(
            "monthly",
            {"bla": "blub"},
            None,
            exceptions.UnknownRegion,
            "no such region defined bla",
            id="unknown region",
        ),
        pytest.param(
            "daily",
            {},
            "daily",
            exceptions.TemporalResolutionError,
            "failed to compute statistics timeseries, no co-located data available in specified base resolution daily",
            id="no daily data",
        ),
        pytest.param(
            "daily",
            {},
            "monthly",
            exceptions.TemporalResolutionError,
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
    exception: Type[Exception],
    error: str,
):
    with pytest.raises(exception) as e:
        mod._process_statistics_timeseries(
            example_coldata, freq, region_ids, False, False, data_freq
        )
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
def test__make_trends(
    coldata, freq: str, season: str, start: int, stop: int, min_yrs: int, station: int
):
    trend_1d = coldata["fake_3d_trends"]
    obs_val = trend_1d.data.data[0, :, station]
    mod_val = trend_1d.data.data[1, :, station]
    time = trend_1d.data.time

    obs_trend, mod_trend = mod._make_trends(
        obs_val, mod_val, time, freq, season, start, stop, min_yrs
    )

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
            exceptions.AeroValTrendsError,
            "min_yrs (7) larger than time between start and stop",
            id="wrong min_yrs",
        ),
    ],
)
def test__make_trends_error(
    coldata, freq: str, season: str, min_yrs: int, exception: Type[Exception], error: str
):
    trend_1d = coldata["fake_3d_trends"]
    obs_val = trend_1d.data.data[0, :, 0]
    mod_val = trend_1d.data.data[1, :, 0]
    time = trend_1d.data.time
    with pytest.raises(exception) as e:
        mod._make_trends(obs_val, mod_val, time, freq, season, 2010, 2015, min_yrs)
    assert str(e.value) == error
