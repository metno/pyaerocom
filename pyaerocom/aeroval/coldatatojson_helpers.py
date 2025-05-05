"""
Helpers for conversion of ColocatedData to JSON files for web interface.
"""

import logging
from collections.abc import Callable
from copy import deepcopy
from datetime import datetime, timezone
from typing import Literal

import numpy as np
import pandas as pd
import xarray as xr

from pyaerocom import ColocatedData
from pyaerocom._warnings import ignore_warnings
from pyaerocom.aeroval.exceptions import ConfigError, TrendsError
from pyaerocom.aeroval.fairmode_stats import fairmode_stats
from pyaerocom.aeroval.helpers import (
    _get_min_max_year_periods,
    _period_str_to_timeslice,
)
from pyaerocom.config import ALL_REGION_NAME
from pyaerocom.exceptions import DataCoverageError, TemporalResolutionError
from pyaerocom.region import (
    Region,
    find_closest_region_coord,
    get_all_default_region_ids,
)
from pyaerocom.region_defs import HTAP_REGIONS_DEFAULT, OLD_AEROCOM_REGIONS
from pyaerocom.stats.stats import _init_stats_dummy, calculate_statistics
from pyaerocom.trends_engine import TrendsEngine
from pyaerocom.trends_helpers import (
    _get_season_from_months,
    _get_unique_seasons,
    _get_yearly,
    _init_trends_result_dict,
)
from pyaerocom.units.datetime import TsType

# from pyaerocom.aeroval.fairmode_statistics import FairmodeStatistics

logger = logging.getLogger(__name__)


def _prepare_regions_json_helper(region_ids):
    regborders, regs = {}, {}
    for regid in region_ids:
        reg = Region(regid)
        name = reg.name
        regs[name] = reg
        regborders[name] = rinfo = {}

        latr = reg.lat_range
        lonr = reg.lon_range
        if any(x is None for x in (latr, lonr)):
            raise ValueError(f"Lat / lon range missing for region {regid}")
        rinfo["minLat"] = latr[0]
        rinfo["maxLat"] = latr[1]
        rinfo["minLon"] = lonr[0]
        rinfo["maxLon"] = lonr[1]

    return (regborders, regs)


def _prepare_default_regions_json():
    return _prepare_regions_json_helper(get_all_default_region_ids())


def _prepare_aerocom_regions_json():
    return _prepare_regions_json_helper(OLD_AEROCOM_REGIONS)


def _prepare_htap_regions_json():
    return _prepare_regions_json_helper(HTAP_REGIONS_DEFAULT)


def _prepare_country_regions(region_ids):
    regs = {}
    for regid in region_ids:
        reg = Region(regid)
        name = reg.name
        regs[name] = reg
    return regs


def init_regions_web(coldata, regions_how):
    regborders, regs = {}, {}
    regborders_default, regs_default = _prepare_default_regions_json()
    if regions_how == "default":
        regborders, regs = regborders_default, regs_default
    elif regions_how == "aerocom":
        regborders, regs = _prepare_aerocom_regions_json()
    elif regions_how == "htap":
        regborders[ALL_REGION_NAME] = regborders_default[ALL_REGION_NAME]
        regs[ALL_REGION_NAME] = regs_default[ALL_REGION_NAME]
        add_borders, add_regs = _prepare_htap_regions_json()
        regborders.update(add_borders)
        regs.update(add_regs)
    elif regions_how == "country":
        regborders[ALL_REGION_NAME] = regborders_default[ALL_REGION_NAME]
        regs[ALL_REGION_NAME] = regs_default[ALL_REGION_NAME]
        coldata.check_set_countries(True)
        regborders.update(coldata.get_country_codes())
        add_regs = _prepare_country_regions(coldata.get_country_codes().keys())
        regs.update(add_regs)
    else:
        raise ValueError("Invalid input for regions_how", regions_how)

    regnames = {}
    for regname, reg in regs.items():
        regnames[reg.region_id] = regname
    return (regborders, regs, regnames)


def _init_meta_glob(coldata, **kwargs):
    meta = coldata.metadata

    # create metadata dictionary that is shared among all timeseries files
    meta_glob = {}
    NDSTR = "UNDEFINED"
    try:
        meta_glob["pyaerocom_version"] = meta["pyaerocom"]
    except KeyError:
        meta_glob["pyaerocom_version"] = NDSTR
    try:
        meta_glob["obs_var"] = meta["var_name"][0]
        meta_glob["mod_var"] = meta["var_name"][1]
    except KeyError:
        meta_glob["obs_var"] = NDSTR
        meta_glob["mod_var"] = NDSTR
    try:
        meta_glob["obs_unit"] = meta["var_units"][0]
        meta_glob["mod_unit"] = meta["var_units"][1]
    except KeyError:
        meta_glob["obs_unit"] = NDSTR
        meta_glob["mod_unit"] = NDSTR
    try:
        meta_glob["obs_freq_src"] = meta["ts_type_src"][0]
        meta_glob["mod_freq_src"] = meta["ts_type_src"][1]
    except KeyError:
        meta_glob["obs_freq_src"] = NDSTR
        meta_glob["mod_freq_src"] = NDSTR
    try:
        meta_glob["obs_revision"] = meta["revision_ref"]
    except KeyError:
        meta_glob["obs_revision"] = NDSTR
    meta_glob["processed_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    meta_glob.update(kwargs)
    return meta_glob


def _init_ts_data(freqs):
    data = {}
    for freq in freqs:
        data[f"{freq}_date"] = []
        data[f"{freq}_obs"] = []
        data[f"{freq}_mod"] = []
    return data


def _create_diurnal_weekly_data_object(coldata, resolution):
    """
    Private helper functions that creates the data set containing all the
    weekly time series at the specified resolution. Called by
    _process_sites_weekly_ts. The returned xarray.Dataset contains a dummy time
    variable (currently not used) and the weekly time series as xarray.DataArray
    objects.

    Parameters
    ----------
    coldata : ColocatedData
        ColocatedData object colocated on hourly resolution.
    resolution : string
        String specifying the averaging window used to generate representative
        weekly time series with hourly resolution. Valid values are 'yearly'
        and  'seasonal'.

    Raises
    ------
    ValueError
        If an invalid resolution is given raise ValueError and print what
        was given.

    Returns
    -------
    rep_week_full_period : xarray.Dataset
        Contains the weekly time series as the variable 'rep_week'


    """
    import xarray as xr

    data_allyears = coldata.data

    yearkeys = list(data_allyears.groupby("time.year").groups)

    if resolution == "seasonal":
        seasons = ["DJF", "MAM", "JJA", "SON"]
    elif resolution == "yearly":
        seasons = ["year"]
    else:
        raise ValueError(f"Invalid resolution. Got {resolution}.")

    first = True
    for yr in yearkeys:
        data = data_allyears.where(data_allyears["time.year"] == yr, drop=True)
        for seas in seasons:
            rep_week_ds = xr.Dataset()
            if resolution == "seasonal":
                mon_slice = data.where(data["time.season"] == seas, drop=True)
            elif resolution == "yearly":
                mon_slice = data

            month_stamp = f"{seas}"

            for day in range(7):
                day_slice = mon_slice.where(mon_slice["time.dayofweek"] == day, drop=True)
                rep_day = day_slice.groupby("time.hour").mean(dim="time")
                rep_day["hour"] = rep_day.hour / 24 + day + 1
                if day == 0:
                    rep_week = rep_day
                else:
                    rep_week = xr.concat([rep_week, rep_day], dim="hour")

            rep_week = rep_week.rename({"hour": "dummy_time"})
            month_stamps = np.zeros(rep_week.dummy_time.shape, dtype="<U5")
            month_stamps[:] = month_stamp
            rep_week_ds["rep_week"] = rep_week
            rep_week_ds["month_stamp"] = (("dummy_time"), month_stamps)

            if seas in ["DJF", "year"]:
                rep_week_full_period = rep_week_ds
            else:
                rep_week_full_period = xr.concat([rep_week_full_period, rep_week_ds], dim="period")

        if first:
            output_array = rep_week_full_period
            # output_array = output_array.expand_dims({'year':[0]},0)
            first = False
        else:
            output_array = xr.concat([output_array, rep_week_full_period], dim="year")

    try:
        output_array.year
    except AttributeError:
        output_array = output_array.expand_dims({"year": [0]}, 0)

    output_array = output_array.assign(dict(year=np.array(yearkeys)))
    # output_array.year[:] = np.array(yearkeys)

    return output_array


def _get_period_keys(resolution: Literal["seasonal", "yearly"]):
    period_keys = dict(
        seasonal=["DJF", "MAM", "JJA", "SON"],
        yearly=["All"],
    )

    if resolution not in period_keys:
        raise ValueError(f"Unknown {resolution=}")

    return period_keys[resolution]


def _process_one_station_weekly(stat_name, i, repw_res, meta_glob, time):
    """
    Processes one station data set for all supported averaging windows into a
    dict of station time series data and metadata.

    Parameters
    ----------
    stat_name : string
        Name of station to process
    i : int
        Index of the station to process in the xarray.Datasets.
    repw_res : dict
        Dictionary of xarray.Datasets for each supported averaging window for
        the weekly time series
    meta_glob : TYPE
        Dictionary containing global metadata.
    time : list
        Time index.

    Returns
    -------
    ts_data : dict
        Dictionary of time series data and metadata for one station. Contains all
        resolutions/averaging windows.
    has_data : bool
        Set to false if all data is missing for a station.

    """
    has_data = False

    years = list(repw_res["seasonal"].year.values)
    yeardict = {}
    for year in years:
        yeardict[f"{year}"] = {}

    ts_data = {
        "time": time,
        "seasonal": {"obs": deepcopy(yeardict), "mod": deepcopy(yeardict)},
        "yearly": {"obs": deepcopy(yeardict), "mod": deepcopy(yeardict)},
    }
    ts_data["station_name"] = stat_name
    ts_data.update(meta_glob)

    for y, year in enumerate(years):
        for res, repw in repw_res.items():
            repw = repw.transpose("year", "period", "data_source", "dummy_time", "station_name")
            obs_vals = repw[y, :, 0, :, i]
            if (np.isnan(obs_vals)).all().values:
                continue
            has_data = True
            mod_vals = repw[y, :, 1, :, i]

            period_keys = _get_period_keys(res)
            for period_num, pk in enumerate(period_keys):
                ts_data[res]["obs"][f"{year}"][pk] = obs_vals.sel(
                    period=period_num
                ).values.tolist()
                ts_data[res]["mod"][f"{year}"][pk] = mod_vals.sel(
                    period=period_num
                ).values.tolist()
    return ts_data, has_data


def _process_weekly_object_to_station_time_series(repw_res, meta_glob):
    """
    Process the xarray.Datasets objects returned by _create_diurnal_weekly_data_object
    into a dictionary containing station time series data and metadata.

    Parameters
    ----------
    repw_res : dict
        Dictionary of xarray.Datasets for each supported averaging window for
        the weekly time series
    meta_glob : dict
        Dictionary containing global metadata.

    Returns
    -------
    ts_objs : list
        List of dicts containing station time series data and metadata.

    """
    ts_objs = []
    dc = 0
    time = (np.arange(168) / 24 + 1).round(4).tolist()
    for i, stat_name in enumerate(repw_res["seasonal"].station_name.values):
        ts_data, has_data = _process_one_station_weekly(stat_name, i, repw_res, meta_glob, time)

        if has_data:
            ts_objs.append(ts_data)
            dc += 1
    return ts_objs


def _process_weekly_object_to_country_time_series(repw_res, meta_glob, regions_how, region_ids):
    """
    Process the xarray.Dataset objects returned by _create_diurnal_weekly_data_object
    into a dictionary containing country average time series data and metadata.

    ToDo
    ----
    Implement regions_how for other values than country based

    Parameters
    ----------
    repw_res : dict
        Dictionary of xarray.Datasets for each supported averaging window for
        the weekly time series
    meta_glob : dict
        Dictionary containing global metadata.
    regions_how : string
        String describing how regions are to be processed. Regional time series
        are only calculated if regions_how = country.
    region_ids : dict
        Dict containing mapping of region IDs and names.

    Returns
    -------
    ts_objs_reg : list
        List of dicts containing station time series data and metadata.

    """
    ts_objs_reg = []
    time = (np.arange(168) / 24 + 1).round(4).tolist()

    years = list(repw_res["seasonal"].year.values)
    yeardict = {}
    for year in years:
        yeardict[f"{year}"] = {}

    if regions_how != "country":
        print("Regional diurnal cycles are only implemented for country regions, skipping...")
        ts_objs_reg = None
    else:
        for regid, regname in region_ids.items():
            ts_data = {
                "time": time,
                "seasonal": {"obs": deepcopy(yeardict), "mod": deepcopy(yeardict)},
                "yearly": {"obs": deepcopy(yeardict), "mod": deepcopy(yeardict)},
            }
            ts_data["station_name"] = regname
            ts_data.update(meta_glob)

            for y, year in enumerate(years):
                for res, repw in repw_res.items():
                    repw = repw.transpose(
                        "year", "period", "data_source", "dummy_time", "station_name"
                    )
                    if regid == ALL_REGION_NAME:
                        subset = repw
                    else:
                        subset = repw.where(repw.country == regid)

                    avg = subset.mean(dim="station_name")
                    obs_vals = avg[y, :, 0, :]
                    mod_vals = avg[y, :, 1, :]

                    period_keys = _get_period_keys(res)
                    for period_num, pk in enumerate(period_keys):
                        ts_data[res]["obs"][f"{year}"][pk] = obs_vals.sel(
                            period=period_num
                        ).values.tolist()
                        ts_data[res]["mod"][f"{year}"][pk] = mod_vals.sel(
                            period=period_num
                        ).values.tolist()

            ts_objs_reg.append(deepcopy(ts_data))
    return ts_objs_reg


def _process_sites_weekly_ts(coldata, regions_how, region_ids, meta_glob):
    """
    Private helper function to process ColocatedData objects into dictionaries
    containing representative weekly time series with hourly resolution.

    Processing the coloceted data object into a collection of representative
    weekly time series is done in the private function _create_diurnal_weekly_data_object.
    This object (an xarray.Dataset) is then further processed into two dictionaries
    containing station and regional time series respectively.

    Parameters
    ----------
    coldata : ColocatedData
        The colocated data to process.
    regions_how : string
        String describing how regions are to be processed. Regional time series
        are only calculated if regions_how = country.
    region_ids : dict
        Dict containing mapping of region IDs and names.
    meta_glob : dict
        Dictionary containing global metadata.

    Returns
    -------
    ts_objs : list
        List of dicts containing station time series data and metadata.
    ts_objs_reg : list
        List of dicts containing country time series data and metadata.

    """
    assert coldata.dims == ("data_source", "time", "station_name")

    repw_res = {
        "seasonal": _create_diurnal_weekly_data_object(coldata, "seasonal")["rep_week"],
        "yearly": _create_diurnal_weekly_data_object(coldata, "yearly")["rep_week"].expand_dims(
            "period", axis=0
        ),
    }

    ts_objs = _process_weekly_object_to_station_time_series(repw_res, meta_glob)
    ts_objs_reg = _process_weekly_object_to_country_time_series(
        repw_res, meta_glob, regions_how, region_ids
    )

    return (ts_objs, ts_objs_reg)


def _init_site_coord_arrays(data):
    found = False
    jsdates = {}
    for freq, cd in data.items():
        if cd is None:
            continue
        elif not found:
            sites = cd.data.station_name.values
            if "station_type" in cd.data.coords:
                sites_types = cd.data.station_type.values
            else:
                sites_types = [""] * len(sites)
            lats = cd.data.latitude.values.astype(np.float64)
            lons = cd.data.longitude.values.astype(np.float64)
            if "altitude" in cd.data.coords:
                alts = cd.data.altitude.values.astype(np.float64)
            else:
                alts = [np.nan] * len(lats)
            if "country" in cd.data.coords:
                countries = cd.data.country.values
            else:
                countries = ["UNAVAIL"] * len(lats)

            found = True
        else:
            assert all(cd.data.station_name.values == sites)
        jsdates[freq] = cd.data.jsdate.values.tolist()
    return (sites, sites_types, lats, lons, alts, countries, jsdates)


def _get_stat_regions(lats, lons, regions, **kwargs):
    regs = []
    regions_how = kwargs.get("regions_how", None)
    for lat, lon in zip(lats, lons):
        reg = find_closest_region_coord(lat, lon, regions=regions, regions_how=regions_how)
        regs.append(reg)
    return regs


def _process_sites(data, regions, regions_how, meta_glob):
    freqs = list(data)
    (sites, site_types, lats, lons, alts, countries, jsdates) = _init_site_coord_arrays(data)
    if regions_how == "country":
        regs = countries
    elif regions_how == "htap":
        regs = _get_stat_regions(lats, lons, regions, regions_how=regions_how)
    else:
        regs = _get_stat_regions(lats, lons, regions)

    ts_objs = []
    site_indices = []
    map_meta = []

    for i, site in enumerate(sites):
        # init empty timeseries data object
        site_meta = {
            "station_name": str(site),
            "station_type": site_types[i],
            "latitude": lats[i],
            "longitude": lons[i],
            "altitude": alts[i],
        }
        if regions_how == "country":
            site_meta["region"] = [regs[i]]
        else:
            site_meta["region"] = regs[i]
        ts_data = _init_ts_data(freqs)
        ts_data.update(meta_glob)
        ts_data.update(site_meta)
        has_data = False
        for freq, cd in data.items():
            if cd is not None:
                assert cd.dims == ("data_source", "time", "station_name")
                sitedata = cd.data.data[:, :, i]
                if np.all(np.isnan(sitedata)):
                    # skip this site, all is NaN
                    continue
                ts_data[f"{freq}_date"] = jsdates[freq]
                ts_data[f"{freq}_obs"] = sitedata[0].tolist()
                ts_data[f"{freq}_mod"] = sitedata[1].tolist()
                has_data = True
        if has_data:  # site is valid
            # register ts_data
            ts_objs.append(ts_data)
            # remember site indices in data for faster processing of statistics
            # below.
            site_indices.append(i)
            # init map data for each valid site
            map_meta.append({**site_meta})

    return (ts_objs, map_meta, site_indices)


def _get_statistics(obs_vals, mod_vals, min_num, drop_stats):
    stats = calculate_statistics(mod_vals, obs_vals, min_num_valid=min_num, drop_stats=drop_stats)
    return _prep_stats_json(stats)


"""
TODO: Make the regional trends by finding all the stations with the correct
amount of data for a certain period and season -> Calculate trends for the average
of those stations

Almost the same as the _remove_less_covered function, but check for each season and period
"""


def _make_regional_trends(
    data: ColocatedData,
    trends_min_yrs: int,
    per: str,
    freq: str,
    season: str,
    regid: str,
    use_country: bool = True,
    median: bool = False,
) -> tuple[dict, dict, bool]:
    (start, stop) = _get_min_max_year_periods([per])
    (start, stop) = (start.year, stop.year)
    data = data.copy()

    station_mod_trends = []
    station_obs_trends = []

    trends_successful = True

    subset_time_series = data.get_regional_timeseries(
        regid,
        check_country_meta=use_country,
    )

    data = data.filter_region(
        regid,
        inplace=False,
        check_country_meta=use_country,
    )
    nb_stations = len(data.data.data[0, 0, :])

    for i in range(nb_stations):
        if stop - start >= trends_min_yrs:
            try:
                obs_vals = data.data.data[0, :, i]
                mod_vals = data.data.data[1, :, i]

                time = data.data.time.values
                (obs_trend, mod_trend) = _make_trends(
                    obs_vals,
                    mod_vals,
                    time,
                    freq,
                    season,
                    start,
                    stop,
                    trends_min_yrs,
                )
                if None not in obs_trend.values() and None not in mod_trend.values():
                    station_mod_trends.append(mod_trend)
                    station_obs_trends.append(obs_trend)
            except TrendsError as e:
                msg = f"Failed to calculate trends, and will skip. This was due to {e}"
                logger.info(msg)

    if len(station_obs_trends) == 0 or len(station_mod_trends) == 0:
        trends_successful = False
        obs_trend = {}
        mod_trend = {}
    else:
        obs_trend = _combine_regional_trends(
            station_obs_trends,
            start,
            stop,
            subset_time_series["obs"],
            median=median,
        )
        mod_trend = _combine_regional_trends(
            station_mod_trends,
            start,
            stop,
            subset_time_series["mod"],
            median=median,
        )

        obs_trend["data"] = obs_trend["data"].to_json()
        mod_trend["data"] = mod_trend["data"].to_json()

        obs_trend["map_var"] = f"slp_{start}"
        mod_trend["map_var"] = f"slp_{start}"

    return obs_trend, mod_trend, trends_successful


def _combine_regional_trends(
    trends: list[dict],
    start_yr: int | float,
    stop_yr: int | float,
    time_series: pd.Series,
    median: bool = False,
) -> dict:
    result = _init_trends_result_dict(start_yr)

    if median:
        avg_func = np.nanmedian
    else:
        avg_func = np.nanmean

    default_trend = trends[0]

    result["period"] = default_trend["period"]
    result["season"] = default_trend["season"]

    result["data"] = _get_yearly(time_series, default_trend["season"], start_yr).loc[
        str(start_yr) : str(stop_yr)
    ]

    result["n"] = _combine_statistic(trends, "n", np.nanmax)
    result["y_mean"] = _combine_statistic(trends, "y_mean", avg_func)
    result["y_min"] = _combine_statistic(trends, "y_min", np.nanmin)
    result["y_max"] = _combine_statistic(trends, "y_max", np.nanmax)

    # result["pval"] = _fishers_pval(trends)
    result["pval"] = _harmonic_mean_pval(trends)

    result["m"] = _combine_statistic(trends, "m", avg_func)
    result["m_err"] = _get_trend_error(trends, "m")
    result["yoffs"] = _combine_statistic(trends, "yoffs", avg_func)

    result["slp"] = _combine_statistic(trends, "slp", avg_func)
    result["slp_err"] = _get_trend_error(trends, "slp")
    result["reg0"] = _combine_statistic(trends, "reg0", avg_func)

    result[f"slp_{start_yr}"] = _combine_statistic(trends, f"slp_{start_yr}", avg_func)
    result[f"slp_{start_yr}_err"] = _get_trend_error(trends, f"slp_{start_yr}")
    result[f"reg0_{start_yr}"] = _combine_statistic(trends, f"reg0_{start_yr}", avg_func)

    return result


def _combine_statistic(data: list, key: str, func: Callable) -> float:
    cleaned = np.array([i[key] for i in data])
    return float(func(cleaned))


def _get_trend_error(trends: list, key: str) -> float:
    cleaned = np.array([i[key] for i in trends])
    return float(np.nanstd(cleaned))


def _fishers_pval(trends: list) -> float:
    """
    Quick implementation of Fisher's method for combining p values
    Is most probably wrong
    """
    pvals = np.array([i["pval"] for i in trends])
    x = -2.0 * np.nansum(np.log(pvals))
    return float(1 - x)


def _harmonic_mean_pval(trends: list, weights: np.ndarray | None = None) -> float:
    """
    Alternative way of combining pvals
    """
    pvals = np.array([i["pval"] for i in trends])
    L = len(pvals)
    if weights is not None and len(weights) != L:
        raise ValueError(
            f"Weights must be the same length as the number of pvals: {len(weights)} != {L}"
        )

    if weights is None:
        weights = np.array([1.0 / L for i in range(L)])

    har_mean = np.sum(weights) / np.sum(weights / pvals)

    return har_mean


def process_trends(
    subset: ColocatedData,
    trends_min_yrs: int,
    season: str,
    per: str,
    avg_over_trends: bool,
    regid: str,
    use_country: bool,
    freq: str,
    use_weights: bool,
) -> dict:
    # subset = _select_period_season_coldata(coldata, per, season, use_meteorological_seasons)
    stats = {}
    trends_successful = False
    mean_trends_successful = False
    median_trends_successful = False

    if avg_over_trends:
        (
            mean_obs_trend,
            mean_mod_trend,
            mean_trends_successful,
        ) = _make_regional_trends(
            subset,
            trends_min_yrs,
            per,
            freq,
            season,
            regid,
            use_country,
        )

        (
            median_obs_trend,
            median_mod_trend,
            median_trends_successful,
        ) = _make_regional_trends(
            subset,
            trends_min_yrs,
            per,
            freq,
            season,
            regid,
            use_country,
            median=True,
        )

    # Calculates the start and stop years. min_yrs have a test value of 7 years. Should be set in cfg
    (start, stop) = _get_min_max_year_periods([per])
    (start, stop) = (start.year, stop.year)

    if stop - start >= trends_min_yrs:
        try:
            subset_time_series = subset.get_regional_timeseries(
                regid, check_country_meta=use_country
            )

            (obs_trend, mod_trend) = _make_trends_from_timeseries(
                subset_time_series["obs"],
                subset_time_series["mod"],
                freq,
                season,
                start,
                stop,
                trends_min_yrs,
            )

            trends_successful = True
        except TrendsError as e:
            msg = f"Failed to calculate trends, and will skip. This was due to {e}"
            logger.info(msg)

    if trends_successful:
        # The whole trends dicts are placed in the stats dict
        stats["obs_trend"] = obs_trend
        stats["mod_trend"] = mod_trend

    if mean_trends_successful and avg_over_trends:
        # The whole trends dicts are placed in the stats dict
        stats["obs_mean_trend"] = mean_obs_trend
        stats["mod_mean_trend"] = mean_mod_trend

    if median_trends_successful and avg_over_trends:
        # The whole trends dicts are placed in the stats dict
        stats["obs_median_trend"] = median_obs_trend
        stats["mod_median_trend"] = median_mod_trend

    return stats


def _make_trends_from_timeseries(obs, mod, freq, season, start, stop, min_yrs):
    """
    Function for generating trends from timeseries

    Includes formatting in a way
    that can be serialized to json. A key, map_var, is added
    for use in the web interface.

    Parameters
    ----------
    obs     : pd.Series
        Time series of the obs
    mod     : pd.Series
        Time series of the mod
    freq    : str
        Frequency for the trends, either monthly or yearly
    season  : str
        Seasons used for the trends
    start   : int
        Start year
    stop    : int
        Stop year
    min_yrs : int
        Minimal number of years for the calculation of the trends

    Raises
    ------
    TrendsError
        If stop - start is smaller than min_yrs

    AeroValError
        If the trend engine returns None

    Returns
    ------
    (dict, dict)
        Dicts consisting of the trends data for the obs and mod
    """

    if stop - start < min_yrs:
        raise TrendsError(f"min_yrs ({min_yrs}) larger than time between start and stop")

    te = TrendsEngine

    # The model and observation data are made to pandas times series
    obs_trend_series = obs
    mod_trend_series = mod

    # Translate season to names used in trends_helpers.py. Should be handled there instead!
    season = _get_season_from_months(season)

    # Trends are calculated
    obs_trend = te.compute_trend(obs_trend_series, freq, start, stop, min_yrs, season)
    mod_trend = te.compute_trend(mod_trend_series, freq, start, stop, min_yrs, season)

    # Makes pd.Series serializable
    if obs_trend["data"] is None or mod_trend["data"] is None:
        raise TrendsError("Trends came back as None", obs_trend["data"], mod_trend["data"])

    obs_trend["data"] = obs_trend["data"].to_json()
    mod_trend["data"] = mod_trend["data"].to_json()

    obs_trend["map_var"] = f"slp_{start}"
    mod_trend["map_var"] = f"slp_{start}"

    return obs_trend, mod_trend


def _make_trends(obs_vals, mod_vals, time, freq, season, start, stop, min_yrs):
    """
    Function for generating trends from lists of observations

    This will calculate pandas time series
    from the lists and use that to calculate trends

    Parameters
    ----------
    obs     : list
        Time series of the obs
    mod     : list
        Time series of the mod
    freq    : str
        Frequency for the trends, either monthly or yearly
    season  : str
        Seasons used for the trends
    start   : int
        Start year
    stop    : int
        Stop year
    min_yrs : int
        Minimal number of years for the calculation of the trends

    Raises
    ------
    TrendsError
        If stop - start is smaller than min_yrs

    AeroValError
        If the trend engine returns None

    Returns
    ------
    (dict, dict)
        Dicts consisting of the trends data for the obs and mod
    """

    # The model and observation data are made to pandas times series
    obs_trend_series = pd.Series(obs_vals, time)
    mod_trend_series = pd.Series(mod_vals, time)

    (obs_trend, mod_trend) = _make_trends_from_timeseries(
        obs_trend_series, mod_trend_series, freq, season, start, stop, min_yrs
    )

    return obs_trend, mod_trend


def _process_map_and_scat(
    data,
    map_data,
    site_indices,
    periods,
    scatter_freq,
    min_num,
    seasons,
    add_trends,
    trends_min_yrs,
    avg_over_trends,
    use_fairmode,
    obs_var,
    drop_stats,
    use_meteorological_seasons,
):
    stats_dummy = _init_stats_dummy(drop_stats=drop_stats)
    scat_data = {}
    scat_dummy = [np.nan]
    for freq, cd in data.items():
        for per in periods:
            for season in seasons:
                use_dummy = cd is None
                if not use_dummy:
                    try:
                        subset = _select_period_season_coldata(
                            cd, per, season, use_meteorological_seasons
                        )
                        jsdate = subset.data.jsdate.values.tolist()
                    except (DataCoverageError, TemporalResolutionError):
                        use_dummy = True
                for i, map_stat in zip(site_indices, map_data):
                    if freq not in map_stat:
                        map_stat[freq] = {}

                    if use_dummy:
                        stats = stats_dummy
                    else:
                        obs_vals = subset.data.data[0, :, i]
                        mod_vals = subset.data.data[1, :, i]
                        stats = _get_statistics(
                            obs_vals, mod_vals, min_num=min_num, drop_stats=drop_stats
                        )

                        if use_fairmode and freq != "yearly" and not np.isnan(obs_vals).all():
                            stats["mb"] = np.nanmean(mod_vals - obs_vals)

                            stats["fairmode"] = fairmode_stats(obs_var, stats, freq)

                        #  Code for the calculation of trends
                        if add_trends and freq != "daily":
                            (start, stop) = _get_min_max_year_periods([per])
                            (start, stop) = (start.year, stop.year)

                            if stop - start >= trends_min_yrs:
                                try:
                                    time = subset.data.time.values
                                    (obs_trend, mod_trend) = _make_trends(
                                        obs_vals,
                                        mod_vals,
                                        time,
                                        freq,
                                        season,
                                        start,
                                        stop,
                                        trends_min_yrs,
                                    )

                                    # The whole trends dicts are placed in the stats dict
                                    stats["obs_trend"] = obs_trend
                                    stats["mod_trend"] = mod_trend

                                    if avg_over_trends:
                                        stats["obs_mean_trend"] = obs_trend
                                        stats["mod_mean_trend"] = mod_trend

                                        stats["obs_median_trend"] = obs_trend
                                        stats["mod_median_trend"] = mod_trend

                                except TrendsError as e:
                                    msg = f"Failed to calculate trends, and will skip. This was due to {e}"
                                    logger.info(msg)

                    perstr = f"{per}-{season}"
                    map_stat[freq][perstr] = stats
                    if freq == scatter_freq:
                        # add only sites to scatter data that have data available
                        # in the lowest of the input resolutions (e.g. yearly)
                        site = map_stat["station_name"]
                        if site not in scat_data:
                            scat_data[site] = {}
                            scat_data[site]["latitude"] = map_stat["latitude"]
                            scat_data[site]["longitude"] = map_stat["longitude"]
                            scat_data[site]["altitude"] = map_stat["altitude"]
                            scat_data[site]["region"] = map_stat["region"]
                        if use_dummy:
                            obs = mod = jsdate = scat_dummy
                        else:
                            obs, mod = obs_vals.tolist(), mod_vals.tolist()
                        scat_data[site][perstr] = {
                            "obs": obs,
                            "mod": mod,
                            "date": jsdate,
                        }

    return (map_data, scat_data)


def _process_regional_timeseries(data, region_ids, regions_how, meta_glob):
    ts_objs = []
    freqs = list(data)
    check_countries = True if regions_how == "country" else False
    for regid, regname in region_ids.items():
        ts_data = _init_ts_data(freqs)
        ts_data["station_name"] = regname
        ts_data.update(meta_glob)

        for freq, cd in data.items():
            if cd is None:
                continue
            jsfreq = cd.data.jsdate.values.tolist()
            try:
                subset = cd.filter_region(regid, inplace=False, check_country_meta=check_countries)
            except DataCoverageError:
                logger.info(f"no data in {regid} ({freq}) to compute regional timeseries")
                ts_data[f"{freq}_date"] = jsfreq
                ts_data[f"{freq}_obs"] = [np.nan] * len(jsfreq)
                ts_data[f"{freq}_mod"] = [np.nan] * len(jsfreq)
                continue

            if subset.has_latlon_dims:
                avg = subset.data.mean(dim=("latitude", "longitude"))
            else:
                avg = subset.data.mean(dim="station_name")
            obs_vals = avg[0].data.tolist()
            mod_vals = avg[1].data.tolist()
            ts_data[f"{freq}_date"] = jsfreq
            ts_data[f"{freq}_obs"] = obs_vals
            ts_data[f"{freq}_mod"] = mod_vals

        ts_objs.append(ts_data)
    return ts_objs


def _apply_annual_constraint_helper(coldata, yearly):
    arr_yr = yearly.data
    yrs_cd = coldata.data.time.dt.year
    yrs_avail = arr_yr.time.dt.year
    obs_allyrs = arr_yr[0]
    for i, yr in enumerate(yrs_avail):
        obs_yr = obs_allyrs[i]
        nan_sites_yr = obs_yr.isnull()
        if not nan_sites_yr.any():
            continue
        scond = nan_sites_yr.data
        tcond = (yrs_cd == yr).data
        # workaround since numpy sometimes throws IndexError if tcond and
        # scond are attempted to be applied directly via
        # coldata.data.data[:,tcond, scond] = np.nan
        tsel = coldata.data.data[:, tcond]
        tsel[:, :, scond] = np.nan
        coldata.data.data[:, tcond] = tsel

    return coldata


def _apply_annual_constraint(data):
    """
    Apply annual filter to data

    Parameters
    ----------
    data : dict
        keys are frequencies, values are corresponding
        instances of `ColocatedData` in that resolution, or None, if colocated
        data is not available in that resolution (see also
        :func:`_init_data_default_frequencies`).

    Raises
    ------
    ConfigError
        If colocated data in yearly resolution is not available in input data

    Returns
    -------
    output : dict
        like input `data` but with annual constrained applied.

    """
    output = {}
    if "yearly" not in data or data["yearly"] is None:
        raise ConfigError(
            "Cannot apply annual_stats_constrained option. "
            'Please add "yearly" in your setup (see attribute '
            '"statistics_json" in AerocomEvaluation class)'
        )
    yearly = data["yearly"]
    for tst, cd in data.items():
        if cd is None:
            output[tst] = None
        else:
            output[tst] = _apply_annual_constraint_helper(cd, yearly)
    return output


def _prep_stats_json(stats):
    for k, v in stats.items():
        try:
            stats[k] = np.float64(v)  # for json encoder...
        except Exception:
            # value is str (e.g. for weighted stats)
            # 'NOTE': 'Weights were not applied to FGE and kendall and spearman corr (not implemented)'
            stats[k] = v
    return stats


def _get_extended_stats(coldata, use_weights, drop_stats):
    stats = coldata.calc_statistics(use_area_weights=use_weights, drop_stats=drop_stats)

    # Removes the spatial median and temporal mean (see mails between Hilde, Jonas, Augustin and Daniel from 27.09.21)
    # (stats['R_spatial_mean'],
    #  stats['R_spatial_median']) = _calc_spatial_corr(coldata, use_weights)

    # (stats['R_temporal_mean'],
    #  stats['R_temporal_median']) = _calc_temporal_corr(coldata)

    (stats["R_spatial_mean"], _) = _calc_spatial_corr(coldata, use_weights)

    (_, stats["R_temporal_median"]) = _calc_temporal_corr(coldata)

    return _prep_stats_json(stats)


def _calc_spatial_corr(coldata, use_weights):
    """
    Compute spatial correlation both for median and mean aggregation

    Parameters
    ----------
    coldata : ColocatedData
        Input data.
    use_weights : bool
        Apply area weights or not.

    Returns
    -------
    float
        mean spatial correlation
    float
        median spatial correlation

    """
    return (
        coldata.calc_spatial_statistics(aggr="mean", use_area_weights=use_weights)["R"],
        coldata.calc_spatial_statistics(aggr="median", use_area_weights=use_weights)["R"],
    )


def _calc_temporal_corr(coldata):
    """
    Compute temporal correlation both for median and mean aggregation

    Parameters
    ----------
    coldata : ColocatedData
        Input data.

    Returns
    -------
    float
        mean temporal correlation
    float
        median temporal correlation

    """
    if len(coldata.time) < 3:
        return np.nan, np.nan
    elif coldata.has_latlon_dims:
        coldata = coldata.flatten_latlondim_station_name()

    # Use only sites that contain at least 3 valid data points (otherwise
    # correlation will be 1).
    obs_ok = coldata.data[0].count(dim="time") > 2
    arr = []
    arr.append(coldata.data[0].where(obs_ok, drop=True))
    arr.append(coldata.data[1].where(obs_ok, drop=True))

    if np.prod(arr[0].shape) == 0 or np.prod(arr[1].shape) == 0:
        return np.nan, np.nan
    corr_time = xr.corr(arr[1], arr[0], dim="time")
    with ignore_warnings(RuntimeWarning, "Mean of empty slice", "All-NaN slice encountered"):
        return (np.nanmean(corr_time.data), np.nanmedian(corr_time.data))


def _select_period_season_coldata(coldata, period, season, use_meteorological_seasons):
    tslice = _period_str_to_timeslice(period)
    if use_meteorological_seasons and len(period) == 4 and season == "DJF":
        # relevant only for single years and DJF
        # for period = '2022' tslice needs to be slice('2021-12','2022-11')
        yeardt = datetime.strptime(period, "%Y")
        tslice = slice(f"{yeardt.year - 1}-12", f"{yeardt.year}-11")
        logger.debug(f"Using meteorological year slicing for {period}: {tslice}")
    # expensive, try use solution with numpy indexing directly...
    # also, keep an eye on: https://github.com/pydata/xarray/issues/2799
    arr = coldata.data.sel(time=tslice)
    if len(arr.time) == 0:
        raise DataCoverageError(f"No data available in period {period}")
    if season != "all":
        if season not in arr.season:
            raise DataCoverageError(f"No data available in {season} in period {period}")
        elif TsType(coldata.ts_type) < "monthly":
            raise TemporalResolutionError(
                "Season selection is only available for monthly or higher resolution data"
            )
        mask = arr["season"] == season
        arr = arr.sel(time=arr["time"][mask])

    return ColocatedData(data=arr)


def _process_heatmap_data(
    data,
    region_ids,
    use_weights,
    drop_stats,
    use_country,
    meta_glob,
    periods,
    seasons,
    add_trends,
    trends_min_yrs,
    avg_over_trends,
    use_meteorological_seasons,
):
    output = {}
    stats_dummy = _init_stats_dummy(drop_stats=drop_stats)
    for freq, coldata in data.items():
        output[freq] = hm_freq = {}
        for regid, regname in region_ids.items():
            hm_freq[regname] = {}
            for per in periods:
                for season in seasons:
                    use_dummy = coldata is None
                    perstr = f"{per}-{season}"
                    if use_dummy:
                        stats = stats_dummy
                    else:
                        try:
                            subset = _select_period_season_coldata(
                                coldata, per, season, use_meteorological_seasons
                            )

                            if add_trends and freq != "daily":
                                trend_stats = process_trends(
                                    subset,
                                    trends_min_yrs,
                                    season,
                                    per,
                                    avg_over_trends,
                                    regid,
                                    use_country,
                                    freq,
                                    use_weights,
                                )

                            subset = subset.filter_region(
                                region_id=regid, check_country_meta=use_country
                            )

                            stats = _get_extended_stats(subset, use_weights, drop_stats)

                            if add_trends and freq != "daily":
                                stats.update(**trend_stats)

                        except (DataCoverageError, TemporalResolutionError):
                            stats = stats_dummy

                    hm_freq[regname][perstr] = stats

    return output


def _map_indices(outer_idx, inner_idx):
    """
    Find index positions of inner array contained in outer array

    Note
    ----
    Both outer and inner index arrays must be strictly monotonous

    Parameters
    ----------
    outer_idx : np.ndarray
        numerical value array (e.g. numerical timestamps in yearly resolution
        from 2010-2020). Must be strictly monotonous.
    inner_idx : np.ndarray
        inner value array, must be contained in outer array, e.g.
        numerical timestamps in yearly resolution from 2012-2014, all values
        in this array must be contained

    Returns
    -------
    mappingg : np.ndarray
        same shape as `outer_idx` with values -1 where no matches are found
        and else, corresponding indices of `inner_idx`

    Example
    -------
    `outer_idx`: [2010, 2011, 2012, 2013, 2014, 2015]
    `inner_idx`: [2011, 2012]
    `mapping`  : [-1, 0, 1, -1, -1, -1]

    """
    inner_start, inner_stop = inner_idx[0], inner_idx[-1]
    mapping = np.ones_like(outer_idx) * -1
    count = 0
    indata = False
    for i, idx in enumerate(outer_idx):
        if inner_start == idx:
            indata = True
        elif inner_stop < idx:
            break
        if indata:
            mapping[i] = count
            # sanity checking, will fail, e.g. if input data is not monotonuos
            assert inner_idx[count] == idx
            count += 1
    return mapping.astype(int)


def _process_statistics_timeseries(
    data, freq, region_ids, use_weights, drop_stats, use_country, data_freq
):
    """
    Compute statistics timeseries for input data

    Parameters
    ----------
    data : dict
        dictionary containing colocated data object (values) in different
        temporal resolutions (keys).
    freq : str
        Output frequency (temporal resolution in which statistics timeseries
        if computed, AeroVal default is monthly)
    region_ids : dict
        Region IDs (keys) and corresponding names (values)
    use_weights : bool
        calculate statistics using area weights or not (only relevant for 4D
        colocated data with lat and lon dimension, e.g. from gridded / gridded
        co-location)
    use_country : bool
        Use countries for regional filtering.
    data_freq : str, optional
        Base frequency for computation of statistics (if None, `freq` is used).
        For details see https://github.com/metno/pyaerocom/pull/416.

    Raises
    ------
    TemporalResolutionError
        If `data_freq` is lower resolution than `freq`.

    Returns
    -------
    output : dict
        Dictionary with results.

    """
    if data_freq is None:
        data_freq = freq

    # input frequency is lower resolution than output frequency
    if TsType(data_freq) < TsType(freq):
        raise TemporalResolutionError(
            f"Desired input frequency {data_freq} is lower than desired output frequency {freq}"
        )

    output = {}
    if data_freq not in data or data[data_freq] is None:
        raise TemporalResolutionError(
            f"failed to compute statistics timeseries, no co-located data "
            f"available in specified base resolution {data_freq}"
        )

    coldata = data[data_freq]

    # get time index of output frequency
    to_idx = data[freq].data.time.values
    tstr = TsType(freq).to_numpy_freq()
    # list of strings of output timestamps (used below to select the
    # individual periods)
    to_idx_str = [str(x) for x in to_idx.astype(f"datetime64[{tstr}]")]
    jsdate = _get_jsdate(to_idx)

    for regid, regname in region_ids.items():
        output[regname] = {}
        try:
            subset = coldata.filter_region(region_id=regid, check_country_meta=use_country)
        except DataCoverageError:
            continue
        for i, js in enumerate(jsdate):
            per = to_idx_str[i]
            try:
                arr = ColocatedData(data=subset.data.sel(time=per))
                stats = arr.calc_statistics(use_area_weights=use_weights, drop_stats=drop_stats)
                output[regname][str(js)] = _prep_stats_json(stats)
            except DataCoverageError:
                pass

    return output


def _get_jsdate(nparr: np.ndarray):
    dt = nparr.astype("datetime64[s]")
    offs = np.datetime64("1970", "s")
    return (dt - offs).astype(int) * 1000


def _init_data_default_frequencies(coldata, to_ts_types):
    """
    Compute one colocated data object for each desired statistics frequency

    Parameters
    ----------
    coldata : ColocatedData
        Initial colocated data in a certain frequency
    to_ts_types : list
        list of desired frequencies for which statistical parameters are being
        computed.

    Returns
    -------
    dict
        keys are elements of `to_ts_types`, values are corresponding
        instances of `ColocatedData` in that resolution, or None, if resolution
        is higher than original resolution of input `coldata`.
    dict
        like `data_arrs` but values are jsdate instances.

    """

    data_arrs = dict.fromkeys(to_ts_types)

    from_tst = TsType(coldata.ts_type)

    for to in to_ts_types:
        to_tst = TsType(to)
        if from_tst < to_tst:
            continue
        elif from_tst == to_tst:
            cd = coldata.copy()
        else:
            cd = coldata.resample_time(to, settings_from_meta=True, inplace=False)
        # add season coordinate for later filtering
        arr = cd.data
        arr["season"] = arr.time.dt.season
        jsdates = _get_jsdate(arr.time.values)
        arr = arr.assign_coords(jsdate=("time", jsdates))
        cd.data = arr
        data_arrs[to] = cd

    return data_arrs


def process_profile_data_for_regions(
    data: ColocatedData,
    region_id: str,
    use_country: bool,
    periods: list[str],
    seasons: list[str],
    use_meteorological_seasons: bool,
) -> dict:  # pragma: no cover
    """
    This method populates the json files in data/profiles which are use for visualization.
    Analogous to _process_map_and_scat for profile data.
    Each json file corresponds to a region or station, obs network, and variable.
    Inside the json, it is broken up by model.
    Each model has a key for "z" (the vertical dimension), "obs", and "mod"
    Each "obs" and "mod" is broken up by period.


    Args:
        data (ColocatedData): ColocatedData object for this layer
        region_id (str): Spatial subset to compute the mean profiles over
        station_name (str): Station to compute mean profiles over for period
        use_country (boolean): Passed to filter_region().
        periods (str): Year part of the temporal range to average over
        seasons (str): Sesonal part of the temporal range to average over

    Returns:
        output (dict): Dictionary to write to json
    """
    output = {"obs": {}, "mod": {}}

    for freq, coldata in data.items():
        if freq not in output["obs"]:
            output["obs"][freq] = {}
        if freq not in output["mod"]:
            output["mod"][freq] = {}

        for per in periods:
            for season in seasons:
                use_dummy = coldata is None
                perstr = f"{per}-{season}"
                if use_dummy:
                    output["obs"][freq][perstr] = np.nan
                    output["mod"][freq][perstr] = np.nan
                else:
                    try:
                        per_season_subset = _select_period_season_coldata(
                            coldata, per, season, use_meteorological_seasons
                        )

                        subset = per_season_subset.filter_region(
                            region_id=region_id, check_country_meta=use_country
                        )
                        with ignore_warnings(
                            RuntimeWarning,
                            "Mean of empty slice",
                            "All-NaN slice encountered",
                        ):
                            output["obs"][freq][perstr] = np.nanmean(subset.data[0, :, :])
                            output["mod"][freq][perstr] = np.nanmean(subset.data[1, :, :])

                    except (DataCoverageError, TemporalResolutionError) as e:
                        msg = f"Failed to access subset timeseries, and will skip. Reason was: {e}"
                        logger.info(msg)

                        output["obs"][freq][perstr] = np.nan
                        output["mod"][freq][perstr] = np.nan

    return output


def process_profile_data_for_stations(
    data: ColocatedData,
    station_name: str,
    use_country: bool,
    periods: list[str],
    seasons: list[str],
    use_meteorological_seasons: bool,
) -> dict:  # pragma: no cover
    """
    This method populates the json files in data/profiles which are use for visualization.
    Analogous to _process_map_and_scat for profile data.
    Each json file corresponds to a region, obs network, and variable.
    Inside the json, it is broken up by model.
    Each model has a key for "z" (the vertical dimension), "obs", and "mod"
    Each "obs" and "mod" is broken up by period.


    Args:
        data (ColocatedData): ColocatedData object for this layer
        region_id (str): Spatial subset to compute the mean profiles over
        station_name (str): Station to compute mean profiles over for period
        use_country (boolean): Passed to filter_region().
        periods (str): Year part of the temporal range to average over
        seasons (str): Sesonal part of the temporal range to average over

    Returns:
        output (dict): Dictionary to write to json
    """
    output = {"obs": {}, "mod": {}}

    for freq, coldata in data.items():
        if freq not in output["obs"]:
            output["obs"][freq] = {}
        if freq not in output["mod"]:
            output["mod"][freq] = {}

        for per in periods:
            for season in seasons:
                use_dummy = coldata is None
                perstr = f"{per}-{season}"
                if use_dummy:
                    output["obs"][freq][perstr] = np.nan
                    output["mod"][freq][perstr] = np.nan
                else:
                    try:
                        per_season_subset = _select_period_season_coldata(
                            coldata, per, season, use_meteorological_seasons
                        )

                        subset = per_season_subset.data[
                            :,
                            :,
                            per_season_subset.data.station_name.values
                            == station_name,  # in this case a station
                        ]  # Assumes ordering of station name matches

                        with ignore_warnings(
                            RuntimeWarning,
                            "Mean of empty slice",
                            "All-NaN slice encountered",
                        ):
                            output["obs"][freq][perstr] = np.nanmean(subset.data[0, :, :])
                            output["mod"][freq][perstr] = np.nanmean(subset.data[1, :, :])

                    except (DataCoverageError, TemporalResolutionError) as e:
                        msg = f"Failed to access subset timeseries, and will skip. Reason was: {e}"
                        logger.info(msg)

                        output["obs"][freq][perstr] = np.nan
                        output["mod"][freq][perstr] = np.nan

    return output


def _remove_less_covered(
    data: ColocatedData,
    min_yrs: int,
    sequential_yrs: bool = False,
) -> ColocatedData:
    stations = data.data.station_name.data
    data = data.copy()
    for i, s in enumerate(stations):
        years = _get_yeares(data, s)
        if sequential_yrs:
            max_yrs = _find_longest_seq_yrs(years)
        else:
            max_yrs = _find_n_yrs(years)

        if min_yrs > max_yrs:
            logger.info(f"Dropping {s}; It has only {max_yrs}")
            data.data = data.data.drop_sel(station_name=s)

    new_stations = data.data.station_name.data

    logger.info(f"Removed {len(stations) - len(new_stations)} stations")
    if len(new_stations) == 0:
        logger.warning(
            f"No stations left after removing stations with fewer than {min_yrs} years!"
        )

    return data


def _get_yeares(coldata: ColocatedData, site: str, start_yr: int = 2000) -> np.ndarray:
    found_yrs = []
    data = coldata.data.sel(station_name=site).isel(data_source=0).to_series()

    yrs = np.unique(data.index.year)
    for yr in yrs:
        if yr < start_yr:  # winter
            continue

        subset = data.loc[str(yr)]

        if len(subset) == 0:
            continue
        elif np.isnan(subset.values).all():
            continue

        d = subset.index
        valid_mask = ~np.isnan(subset.values)
        seasons = _get_unique_seasons(d[valid_mask])

        if len(seasons) == 4:
            found_yrs.append(yr)

    return np.array(found_yrs)


def _find_n_yrs(years: np.ndarray) -> int:
    return len(years)


def _find_longest_seq_yrs(years: np.ndarray) -> int:
    years = np.sort(years)
    max_yrs = 1
    yrs = 1
    for i in range(1, len(years)):
        if years[i] == years[i - 1] + 1:
            yrs += 1
        else:
            yrs = 1

        max_yrs = max(yrs, max_yrs)

    return max_yrs


def _get_yrs_from_season_yrs(season_yrs: dict) -> np.ndarray:
    yrs = []
    for y in season_yrs.keys():
        s = season_yrs[y]
        if len(list(set(s))) == 4:
            yrs.append(y)

    return np.array(yrs)


def _process_statistics_timeseries_single_region(
    reg: str,
    regnames: dict,
    data: dict[str, ColocatedData],
    main_freq: str,
    use_weights: bool,
    drop_stats: tuple,
    use_country: bool,
    input_freq: str,
    obs_name: str,
    var_name_web: str,
    vert_code: str,
    model_name: str,
    model_var: str,
):
    try:
        stats_ts = _process_statistics_timeseries(
            data=data,
            freq=main_freq,
            region_ids={reg: regnames[reg]},
            use_weights=use_weights,
            drop_stats=drop_stats,
            use_country=use_country,
            data_freq=input_freq,
        )
    except TemporalResolutionError:
        stats_ts = {}

    region = regnames[reg]
    return (stats_ts, region, obs_name, var_name_web, vert_code, model_name, model_var)


def _calculate_fairmode(
    coldata: ColocatedData,
    fairmode_statistics,  #: FairmodeStatistics,
    map_meta: list[dict],
    obs_var: str = None,
    periods: tuple[str, ...] | None = None,
    seasons: tuple[str, ...] | None = None,
    use_meteorological_seasons: bool = False,
):
    results = {"ALL": {}}
    for per in periods:
        for season in seasons:
            try:
                subset = _select_period_season_coldata(
                    coldata, per, season, use_meteorological_seasons
                )
                # jsdate = subset.data.jsdate.values.tolist()
            except (DataCoverageError, TemporalResolutionError) as e:
                logger.info(f"Failed to access subset coldata: {e}")
                return results

            perstr = f"{per}-{season}"
            fm_stats = fairmode_statistics.fairmode_statistics(subset, obs_var)
            for i, station in enumerate(map_meta):
                station_name = station["station_name"]
                region = station["region"][0]
                if region not in results:
                    results[region] = {}

                if perstr not in results[region]:
                    results[region][perstr] = {}
                if perstr not in results["ALL"]:
                    results["ALL"][perstr] = {}

                results[region][perstr][station_name] = fm_stats[station_name]
                results["ALL"][perstr][station_name] = fm_stats[station_name]
    return results
