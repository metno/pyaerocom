# ToDo: merge with test_coldatatojson_helpers.py
from __future__ import annotations

import numpy as np
import pytest
import xarray

from pyaerocom import ColocatedData, TsType
from pyaerocom.aeroval.coldatatojson_helpers import (
    _calculate_fairmode,
    _create_diurnal_weekly_data_object,
    _get_jsdate,
    _get_period_keys,
    _init_data_default_frequencies,
    _init_meta_glob,
    _make_trends,
    _map_indices,
    _process_sites,
    _process_statistics_timeseries,
    _remove_less_covered,
    _select_period_season_coldata,
)
from pyaerocom.aeroval.exceptions import TrendsError
from pyaerocom.aeroval.fairmode_statistics import SPECIES, FairmodeStatistics
from pyaerocom.exceptions import TemporalResolutionError, UnknownRegion
from tests.fixtures.collocated_data import COLDATA


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
        data=example_coldata,
        freq=freq,
        region_ids=region_ids,
        use_weights=False,
        drop_stats=(),
        use_country=False,
        data_freq=data_freq,
    )
    assert len(result) == len(region_ids)
    biases = [np.nan]
    for data in result.values():
        for stats in data.values():
            biases.append(stats["nmb"])
    mean_bias = np.nanmean(biases)
    assert mean_bias == pytest.approx(nmb_avg, abs=0.001, nan_ok=True)


@pytest.mark.parametrize(
    "freq,region_ids,data_freq,drop_stats",
    [
        ("yearly", {"EUROPE": "Europe"}, "monthly", ("mb", "mab")),
        ("yearly", {"EUROPE": "Europe"}, None, ("nmb",)),
    ],
)
@pytest.mark.filterwarnings("ignore:Mean of empty slice:RuntimeWarning")
def test__process_statistics_timeseries_drop_stats(
    example_coldata,
    freq: str,
    region_ids: dict[str, str],
    data_freq: str,
    drop_stats: tuple[str],
):
    result = _process_statistics_timeseries(
        data=example_coldata,
        freq=freq,
        region_ids=region_ids,
        use_weights=False,
        drop_stats=drop_stats,
        use_country=False,
        data_freq=data_freq,
    )
    assert result.keys().isdisjoint(drop_stats)


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
        _process_statistics_timeseries(
            data=example_coldata,
            freq=freq,
            region_ids=region_ids,
            use_weights=False,
            drop_stats=(),
            use_country=False,
            data_freq=data_freq,
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
            TrendsError,
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
    assert set(res.values()) == {"UNDEFINED"}


@pytest.mark.parametrize("resolution", ["yearly"])
@pytest.mark.parametrize("coldataset", ["fake_3d_trends"])
def test__create_diurnal_weekly_data_object(coldata: ColocatedData, resolution: str):
    obj = _create_diurnal_weekly_data_object(coldata, resolution)
    assert isinstance(obj, xarray.Dataset)


@pytest.mark.parametrize(
    "resolution,error_message",
    [
        ("seasonal", "hour must not be empty"),
        ("cat", "Invalid resolution"),
    ],
)
@pytest.mark.parametrize("coldataset", ["fake_3d_trends"])
def test__create_diurnal_weekly_data_object__error(
    coldata: ColocatedData, resolution: str, error_message: str
):
    with pytest.raises(ValueError, match=error_message):
        _create_diurnal_weekly_data_object(coldata, resolution)


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


@pytest.mark.parametrize(
    "min_yrs, station_nb, colocate_time",
    [
        (0, 5, False),
        (0, 5, True),
        (4, 2, True),
        (4, 2, False),
        (3, 3, True),
        (3, 3, False),
    ],
)
def test__remove_less_covered(
    # coldata: dict,
    min_yrs: int,
    station_nb: int,
    colocate_time: bool,
):
    cd = (
        COLDATA["fake_3d_partial_trends_coltime"]()
        if colocate_time
        else COLDATA["fake_3d_partial_trends"]()
    )
    old_stations = cd.data.station_name.data

    new_cd = _remove_less_covered(cd, min_yrs)

    new_stations = new_cd.data.station_name.data

    if min_yrs == 0:
        assert len(old_stations) == len(new_stations)

    assert len(new_stations) == station_nb


def test__remove_less_covered_all():
    cd = COLDATA["fake_3d_partial_trends_coltime"]()
    new_cd = _remove_less_covered(cd, 1000)
    assert new_cd.data.station_name.shape[0] == 0


@pytest.mark.parametrize(
    "period, use_meteorological_seasons, resultfirst, resultlast",
    [
        (
            "2004",
            True,
            np.datetime64("2003-12-01T00:00:00.000000000"),
            np.datetime64("2004-02-29T00:00:00.000000000"),
        ),
        (
            "2003-2004",
            True,
            np.datetime64("2003-01-01T00:00:00.000000000"),
            np.datetime64("2004-12-31T00:00:00.000000000"),
        ),
        (
            "2004",
            False,
            np.datetime64("2004-01-01T00:00:00.000000000"),
            np.datetime64("2004-12-31T00:00:00.000000000"),
        ),
    ],
)
@pytest.mark.parametrize("coldataset", ["fake_3d_partial_trends"])
def test__select_period_season_coldata(
    coldata: ColocatedData,
    period: str,
    use_meteorological_seasons: bool,
    resultfirst: np.datetime64,
    resultlast: np.datetime64,
):
    coldatamod = coldata.copy()
    coldatamod.data = coldatamod.data.assign_coords(
        season=("time", coldata.coords["time.season"].values)
    )
    cd = _select_period_season_coldata(coldatamod, period, "DJF", use_meteorological_seasons)
    assert cd.coords["time"].values[0] == resultfirst
    assert cd.coords["time"].values[-1] == resultlast


@pytest.mark.parametrize("cfg", ["cfgexp1"])
@pytest.mark.filterwarnings("ignore:invalid value encountered in .*divide:RuntimeWarning")
def test_calculate_fairmode(eval_config: dict, caplog):
    example_coldata = COLDATA["tm5_aeronet"]()

    # add fake station_type
    fake_type = "bla"
    fake_types = [fake_type] * example_coldata.coords["station_name"].shape[0]

    example_coldata.data = example_coldata.data.assign_coords(
        station_type=("station_name", fake_types)
    )

    meta_glob = _init_meta_glob(
        example_coldata,
    )

    data = _init_data_default_frequencies(example_coldata, ["monthly"])
    (ts_objs, map_meta, site_indices) = _process_sites(data, None, "default", meta_glob)

    fairmode_statistics = FairmodeStatistics()

    # fill nans
    np.nan_to_num(data["monthly"].data, copy=False, nan=1)

    period = "2010"
    season = "DJF"

    # we ignore here the fact that the data is monthly and for od550aer, the data is basically to be considered dummy
    # since we bypass the guards on frequency and variable, _calculate_fairmode will not question the data at this point
    # and treat it as if it's concno2 hourly
    results = _calculate_fairmode(
        data["monthly"],
        fairmode_statistics,
        map_meta,
        "concno2",
        [period],
        [season],
        use_meteorological_seasons=False,
    )

    assert results["ALL"][f"{period}-{season}"]["Agoufou"]["station_type"] == np.str_(fake_type)
    assert all(
        results["ALL"][f"{period}-{season}"]["Agoufou"][item] == SPECIES["concno2"][item]
        for item in ["freq", "alpha", "percentile", "RV", "UrRV"]
    )
    assert all(
        item in results["ALL"][f"{period}-{season}"]["Agoufou"]
        for item in ["RMSU", "sign", "beta_mqi", "Hperc", "crms", "bias", "rms"]
    )

    wrongperiod = "2025"
    # here we pass the wrong period to test the case when the coldata subset fails
    resultsempty = _calculate_fairmode(
        data["monthly"],
        fairmode_statistics,
        map_meta,
        "concno2",
        [wrongperiod],
        [season],
        use_meteorological_seasons=False,
    )

    assert resultsempty == {"ALL": {}}
    assert (
        f"Failed to access subset coldata: No data available in period {wrongperiod}"
        in caplog.text
    )
