
import os
import numpy as np
import xarray as xr
import pandas as pd
from datetime import datetime
from pyaerocom import const
from pyaerocom.helpers import start_stop
from pyaerocom.trends_helpers import _get_season_from_months
from pyaerocom.aeroval.helpers import (_period_str_to_timeslice,
                                       _get_min_max_year_periods, read_json,
                                       write_json)
from pyaerocom.colocateddata import ColocatedData
from pyaerocom.mathutils import calc_statistics
from pyaerocom.tstype import TsType
from pyaerocom.exceptions import (AeroValConfigError,
                                  DataCoverageError,
                                  TemporalResolutionError,
                                  AeroValTrendsError)
from pyaerocom.region_defs import OLD_AEROCOM_REGIONS, HTAP_REGIONS_DEFAULT
from pyaerocom.region import (get_all_default_region_ids,
                              find_closest_region_coord,
                              Region)

from pyaerocom.aeroval._processing_base import ProcessingEngine
from pyaerocom.trends_engine import TrendsEngine

from time import time

def get_heatmap_filename(ts_type):
    return f'glob_stats_{ts_type}.json'

def get_stationfile_name(station_name, obs_name, var_name_web, vert_code):
    """Get name of station timeseries file"""
    return ('{}_{}-{}_{}.json'
            .format(station_name, obs_name, var_name_web, vert_code))

def get_json_mapname(obs_name, var_name_web, model_name, model_var,
                     vert_code):
    """Get name base name of json file"""
    return ('{}-{}_{}_{}-{}.json'
            .format(obs_name, var_name_web, vert_code, model_name, model_var))

def _write_stationdata_json(ts_data, out_dir):
    """
    This method writes time series data given in a dictionary to .json files

    Parameters
    ----------
    ts_data : dict
        A dictionary containing all processed time series data.
    out_dir : str or similar
        output directory

    Returns
    -------
    None.

    """
    filename = get_stationfile_name(ts_data['station_name'],
                                    ts_data['obs_name'],
                                    ts_data['var_name_web'],
                                    ts_data['vert_code'])

    fp = os.path.join(out_dir, filename)
    if os.path.exists(fp):
        current = read_json(fp)
    else:
        current = {}
    current[ts_data['model_name']] = ts_data
    write_json(current, fp, ignore_nan=True)

def _write_site_data(ts_objs, dirloc):
    """Write list of station timeseries files to json"""
    for ts_data in ts_objs:
        #writes json file
        _write_stationdata_json(ts_data, dirloc)

def _write_diurnal_week_stationdata_json(ts_data, out_dirs):
    """
    Minor modification of method _write_stationdata_json to allow a further
    level of sub-directories

    Parameters
    ----------
    ts_data : dict
        A dictionary containing all processed time series data.
    out_dirs : list
        list of file paths for writing data to

    Raises
    ------
    Exception
        Raised if opening json file fails

    Returns
    -------
    None.

    """
    filename = get_stationfile_name(ts_data['station_name'],
                                    ts_data['obs_name'],
                                    ts_data['var_name_web'],
                                    ts_data['vert_code'])

    fp = os.path.join(out_dirs['ts/diurnal'], filename)
    if os.path.exists(fp):
        current = read_json(fp)
    else:
        current = {}
    current[ts_data['model_name']] = ts_data
    write_json(current, fp, ignore_nan=True)

def _add_entry_json(heatmap_file, result, obs_name, var_name_web, vert_code,
                            model_name, model_var):
    if os.path.exists(heatmap_file):
        current = read_json(heatmap_file)
    else:
        current = {}
    if not var_name_web in current:
        current[var_name_web] = {}
    ov = current[var_name_web]
    if not obs_name in ov:
        ov[obs_name] = {}
    on = ov[obs_name]
    if not vert_code in on:
        on[vert_code] = {}
    ovc = on[vert_code]
    if not model_name in ovc:
        ovc[model_name] = {}
    mn = ovc[model_name]
    mn[model_var] = result
    write_json(current, heatmap_file, ignore_nan=True)

def _init_stats_dummy():
    # dummy for statistics dictionary for locations without data
    stats_dummy = {}
    for k in calc_statistics([1], [1]):
        stats_dummy[k] = np.nan
    return stats_dummy

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
            raise ValueError(f'Lat / lon range missing for region {regid}')
        rinfo['minLat'] = latr[0]
        rinfo['maxLat'] = latr[1]
        rinfo['minLon'] = lonr[0]
        rinfo['maxLon'] = lonr[1]

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
    if regions_how == 'default':
        regborders, regs = regborders_default, regs_default
    elif regions_how == 'aerocom':
        regborders, regs = _prepare_aerocom_regions_json()
    elif regions_how == 'htap':
        regborders['WORLD'] = regborders_default['WORLD']
        regs['WORLD'] = regs_default['WORLD']
        add_borders, add_regs = _prepare_htap_regions_json()
        regborders.update(add_borders)
        regs.update(add_regs)
    elif regions_how == 'country':
        regborders['WORLD'] = regborders_default['WORLD']
        regs['WORLD'] = regs_default['WORLD']
        coldata.check_set_countries(True)
        regborders.update(coldata.get_country_codes())
        add_regs = _prepare_country_regions(coldata.get_country_codes().keys())
        regs.update(add_regs)
    else:
        raise ValueError('Invalid input for regions_how', regions_how)

    regnames = {}
    for regname, reg in regs.items():
        regnames[reg.region_id] = regname
    return (regborders, regs, regnames)

def update_regions_json(region_defs, regions_json):
    """Check current regions.json for experiment and update if needed

    Parameters
    ----------
    region_defs : dict
        keys are names of region (not IDs!) values define rectangular borders
    regions_json : str
        regions.json file (if it does not exist it will be created).

    Returns
    -------
    dict
        current content of updated regions.json
    """
    if os.path.exists(regions_json):
        current = read_json(regions_json)
    else:
        current = {}

    for region_name, region_info in region_defs.items():
        if not region_name in current:
            current[region_name] = region_info
    write_json(current, regions_json)
    return current

def _init_meta_glob(coldata, **kwargs):
    meta = coldata.metadata

    # create metadata dictionary that is shared among all timeseries files
    meta_glob = {}
    NDSTR = 'UNDEFINED'
    try:
        meta_glob['pyaerocom_version'] = meta['pyaerocom']
    except KeyError:
        meta_glob['pyaerocom_version'] = NDSTR
    try:
        meta_glob['obs_var'] = meta['var_name'][0]
        meta_glob['mod_var'] = meta['var_name'][1]
    except KeyError:
        meta_glob['obs_var'] = NDSTR
        meta_glob['mod_var'] = NDSTR
    try:
        meta_glob['obs_unit'] = meta['var_units'][0]
        meta_glob['mod_unit'] = meta['var_units'][1]
    except KeyError:
        meta_glob['obs_unit'] = NDSTR
        meta_glob['mod_unit'] = NDSTR
    try:
        meta_glob['obs_freq_src'] = meta['ts_type_src'][0]
        meta_glob['mod_freq_src'] = meta['ts_type_src'][1]
    except KeyError:
        meta_glob['obs_freq_src'] = NDSTR
        meta_glob['mod_freq_src'] = NDSTR
    try:
        meta_glob['obs_revision'] = meta['revision_ref']
    except KeyError:
        meta_glob['obs_revision'] = NDSTR
    meta_glob['processed_utc'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    meta_glob.update(kwargs)
    return meta_glob

def _init_ts_data(freqs):
    data = {}
    for freq in freqs:
        data[f'{freq}_date'] = []
        data[f'{freq}_obs'] = []
        data[f'{freq}_mod'] = []
    return data

def _create_diurnal_weekly_data_object(coldata,resolution):
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
    data = coldata.data
    if resolution == 'seasonal':
        seasons = ['DJF','MAM','JJA','SON']
    elif resolution == 'yearly':
        seasons = ['year']
    else:
        raise ValueError(f'Invalid resolution. Got {resolution}.')


    for seas in seasons:
        rep_week_ds = xr.Dataset()
        if resolution == 'seasonal':
            mon_slice = data.where(data['time.season']==seas,drop=True)
        elif resolution == 'yearly':
            mon_slice = data

        month_stamp = f'{seas}'

        for day in range(7):
            day_slice = mon_slice.where(mon_slice['time.dayofweek']==day,drop=True)
            rep_day = day_slice.groupby('time.hour').mean(dim='time')
            rep_day['hour'] = rep_day.hour/24+day+1
            if day == 0:
                rep_week = rep_day
            else:
                rep_week = xr.concat([rep_week,rep_day],dim='hour')

        rep_week=rep_week.rename({'hour':'dummy_time'})
        month_stamps = np.zeros(rep_week.dummy_time.shape,dtype='<U5')
        month_stamps[:] = month_stamp
        rep_week_ds['rep_week']=rep_week
        rep_week_ds['month_stamp'] = (('dummy_time'),month_stamps)

        if seas in ['DJF','year']:
            rep_week_full_period = rep_week_ds
        else:
            rep_week_full_period = xr.concat([rep_week_full_period,rep_week_ds],dim='period')
    return rep_week_full_period

def _get_period_keys(resolution):
    if resolution == 'seasonal':
        period_keys = ['DJF','MAM','JJA','SON']
    elif resolution == 'yearly':
        period_keys = ['Annual']
    return period_keys

def _process_one_station_weekly(stat_name, i,repw_res, meta_glob, time):
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
        Dictinary of time series data and metadata for one station. Contains all
        resolutions/averaging windows.
    has_data : bool
        Set to false if all data is missing for a station.

    """
    has_data = False
    ts_data = {'time' : time,'seasonal' : {'obs' : {},'mod' : {}},'yearly' : {'obs' : {},'mod' : {}} }
    ts_data['station_name'] = stat_name
    ts_data.update(meta_glob)


    for res,repw in repw_res.items():
        obs_vals = repw[:,0, :, i]
        if (np.isnan(obs_vals)).all().values:
            continue
        has_data = True
        mod_vals = repw[:,1, :, i]

        period_keys = _get_period_keys(res)
        for period_num,pk in enumerate(period_keys):
            ts_data[res]['obs'][pk] = obs_vals.sel(period=period_num).values.tolist()
            ts_data[res]['mod'][pk] = mod_vals.sel(period=period_num).values.tolist()
    return ts_data, has_data

def _process_weekly_object_to_station_time_series(repw_res,meta_glob):
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
    time = (np.arange(168)/24+1).round(4).tolist()
    for i, stat_name in enumerate(repw_res['seasonal'].station_name.values):
        ts_data, has_data = _process_one_station_weekly(stat_name, i, repw_res,
                                                        meta_glob, time)

        if has_data:
            ts_objs.append(ts_data)
            dc +=1
    return ts_objs

def _process_weekly_object_to_country_time_series(repw_res,meta_glob,
                                                  regions_how,region_ids):
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
    time = (np.arange(168)/24+1).round(4).tolist()

    if regions_how != 'country':
        print('Regional diurnal cycles are only implemented for country regions, skipping...')
        ts_objs_reg = None
    else:
        for regid, regname in region_ids.items():
            ts_data = {
                'time' : time,
                'seasonal' : {'obs' : {},'mod' : {}},
                'yearly' : {'obs' : {},'mod' : {}}
                }
            ts_data['station_name'] = regname
            ts_data.update(meta_glob)

            for res, repw in repw_res.items():
                if regid == 'WORLD':
                    subset = repw
                else:
                    subset = repw.where(repw.country == regid)

                avg = subset.mean(dim='station_name')
                obs_vals = avg[:,0,:]
                mod_vals = avg[:,1,:]

                period_keys = _get_period_keys(res)
                for period_num,pk in enumerate(period_keys):
                    ts_data[res]['obs'][pk] = obs_vals.sel(period=period_num).values.tolist()
                    ts_data[res]['mod'][pk] = mod_vals.sel(period=period_num).values.tolist()

            ts_objs_reg.append(ts_data)
    return ts_objs_reg

def _process_sites_weekly_ts(coldata,regions_how,region_ids,meta_glob):
    """
    Private helper function to process ColocatedData objects into dictionaries
    containing represenative weekly time series with hourly resolution.

    Processing the coloceted data object into a collection of representative
    weekly time series is done in the private function _create_diurnal_weekly_data_object.
    This object (an xarray.Dataset) is then further processed into two dictionaries
    containing station and regional time series respectively.

    Parameters
    ----------
    coldata : ColocatedData
        The colocated data to process.
    regions_how : string
        Srting describing how regions are to be processed. Regional time series
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
    assert coldata.dims == ('data_source', 'time', 'station_name')

    repw_res = {'seasonal':_create_diurnal_weekly_data_object(coldata, 'seasonal')['rep_week'],
                'yearly':_create_diurnal_weekly_data_object(coldata, 'yearly')['rep_week'].expand_dims('period',axis=0),}

    ts_objs = _process_weekly_object_to_station_time_series(repw_res,meta_glob)
    ts_objs_reg = _process_weekly_object_to_country_time_series(repw_res,
                                                                meta_glob,
                                                                regions_how,
                                                                region_ids)

    return (ts_objs,ts_objs_reg)

def _init_site_coord_arrays(data):
    found = False
    jsdates = {}
    for freq, cd in data.items():
        if cd is None:
            continue
        elif not found:
            sites = cd.data.station_name.values
            lats = cd.data.latitude.values.astype(np.float64)
            lons = cd.data.longitude.values.astype(np.float64)
            if 'altitude' in cd.data.coords:
                alts = cd.data.altitude.values.astype(np.float64)
            else:
                alts = [np.nan]*len(lats)
            if 'country' in cd.data.coords:
                countries = cd.data.country.values
            else:
                countries = ['UNAVAIL']*len(lats)

            found = True
        else:
            assert all(cd.data.station_name.values == sites)
        jsdates[freq] = cd.data.jsdate.values.tolist()
    return (sites, lats, lons, alts, countries, jsdates)

def _get_stat_regions(lats, lons, regions):
    regs = []
    for (lat, lon) in zip(lats, lons):
        reg = find_closest_region_coord(lat,lon,regions=regions)
        regs.append(reg)
    return regs


def _process_sites(data, regions, regions_how, meta_glob):

    freqs = list(data.keys())
    (sites, lats, lons, alts, countries, jsdates) = _init_site_coord_arrays(data)
    if regions_how == 'country':
        regs = countries
    else:
        regs = _get_stat_regions(lats, lons, regions)

    ts_objs = []
    site_indices = []
    map_meta = []

    for i, site in enumerate(sites):
        # init empty timeseries data object
        site_meta = {
            'station_name'  :   str(site),
            'latitude'      :   lats[i],
            'longitude'     :   lons[i],
            'altitude'      :   alts[i],
            'region'        :   regs[i]}
        ts_data = _init_ts_data(freqs)
        ts_data.update(meta_glob)
        ts_data.update(site_meta)
        has_data = False
        for freq, cd in data.items():
            if cd is not None:
                assert cd.dims == ('data_source', 'time', 'station_name')
                sitedata = cd.data.data[:, :, i]
                if np.all(np.isnan(sitedata)):
                    #skip this site, all is NaN
                    continue
                ts_data[f'{freq}_date'] = jsdates[freq]
                ts_data[f'{freq}_obs'] = sitedata[0].tolist()
                ts_data[f'{freq}_mod'] = sitedata[1].tolist()
                has_data = True
        if has_data: #site is valid
            # register ts_data
            ts_objs.append(ts_data)
            # remember site indices in data for faster processing of statistics
            # below.
            site_indices.append(i)
            # init map data for each valid site
            map_meta.append({**site_meta})

    return (ts_objs, map_meta, site_indices)

def _get_statistics(obs_vals, mod_vals, min_num):
    stats = calc_statistics(mod_vals, obs_vals,
                            min_num_valid=min_num)
    return _prep_stats_json(stats)

def _make_trends_from_timeseries(obs, mod, freq, season, start, stop, min_yrs):
    """
    Function for generating trends from timeseries
    
    Includes fomatting in a way
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
    AeroValTrendsError
        If stop - start is smaller than min_yrs
    
    AeroValError
        If the trend engine returns None

    Returns
    ------
    (dict, dict)
        Dicts consiting of the trends data for the obs and mod
    """


    if stop-start < min_yrs:
        raise AeroValTrendsError(f"min_yrs ({min_yrs}) larger than time between start and stop")

    te = TrendsEngine


    # The model and observation data are made to pandas times series
    obs_trend_series = obs
    mod_trend_series = mod

    # Translate season to names used in trends_helpers.py. Should be handled there instead!
    season = _get_season_from_months(season)

    # Trends are calculated
    obs_trend = te.compute_trend(obs_trend_series, freq, start, stop, 
                                                                min_yrs, season)
    mod_trend = te.compute_trend(mod_trend_series, freq, start, stop, 
                                                                min_yrs, season)

    # Makes pd.Series serializable
    if obs_trend["data"] is None or mod_trend["data"] is None:
        raise AeroValTrendsError("Trends came back as None",
                                     obs_trend["data"], mod_trend["data"])

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
    AeroValTrendsError
        If stop - start is smaller than min_yrs
    
    AeroValError
        If the trend engine returns None

    Returns
    ------
    (dict, dict)
        Dicts consiting of the trends data for the obs and mod
    """

    # The model and observation data are made to pandas times series
    obs_trend_series = pd.Series(obs_vals, time)
    mod_trend_series = pd.Series(mod_vals, time)

    (obs_trend, mod_trend) = _make_trends_from_timeseries(obs_trend_series, 
                                                    mod_trend_series, freq,
                                                    season, start, stop, min_yrs)

    return obs_trend, mod_trend
        



def _process_map_and_scat(data, map_data, site_indices, periods,
                          main_freq, min_num, seasons, 
                          add_trends, trends_min_yrs):


   
    stats_dummy = _init_stats_dummy()
    scat_data = {}
    scat_dummy = [np.nan]
    for freq, cd in data.items():
        use_dummy = True if cd is None else False
        for per in periods:
            for season in seasons:
                if not use_dummy:
                    try:
                        subset = _select_period_season_coldata(cd,
                                                               per,
                                                               season)
                        jsdate = subset.data.jsdate.values.tolist()
                    except (DataCoverageError, TemporalResolutionError):
                        use_dummy = True
                for i, map_stat in zip(site_indices, map_data):
                    if not freq in map_stat:
                        map_stat[freq] = {}

                    if use_dummy:
                        stats = stats_dummy
                    else:
                        obs_vals = subset.data.data[0, :, i]
                        mod_vals = subset.data.data[1, :, i]
                        stats = _get_statistics(obs_vals, mod_vals, min_num)


                        #  Code for the calculation of trends
                        if add_trends and freq != "daily":
    
                            (start, stop) = _get_min_max_year_periods([per])

                            if stop - start >= trends_min_yrs:
                                
                                try:
                                    time = subset.data.time.values
                                    (obs_trend, mod_trend) = _make_trends(obs_vals,
                                                            mod_vals, time, freq, 
                                                            season, start, stop, 
                                                            trends_min_yrs)


                                    # The whole trends dicts are placed in the stats dict
                                    stats["obs_trend"] = obs_trend
                                    stats["mod_trend"] = mod_trend

                                except AeroValTrendsError as e:
                                    msg = f"Failed to calculate trends, and will skip. This was due to {e}"
                                    const.logger.warning(msg)
                                    


                            

                          

                    

                    perstr = f'{per}-{season}'
                    map_stat[freq][perstr] = stats
                    if freq == main_freq:
                        # add only sites to scatter data that have data available
                        # in the lowest of the input resolutions (e.g. yearly)
                        site = map_stat['station_name']
                        if not site in scat_data:
                            scat_data[site] = {}
                            scat_data[site]['latitude'] = map_stat['latitude']
                            scat_data[site]['longitude'] = map_stat['longitude']
                            scat_data[site]['altitude'] = map_stat['altitude']
                            scat_data[site]['region'] = map_stat['region']
                        if use_dummy:
                            obs = mod = jsdate = scat_dummy
                        else:
                            obs, mod = obs_vals.tolist(), mod_vals.tolist()
                        scat_data[site][perstr] = {'obs':obs,'mod':mod,
                                                   'date':jsdate}


    return (map_data, scat_data)

def _process_regional_timeseries(data, region_ids, regions_how, meta_glob):
    ts_objs = []
    freqs = list(data.keys())
    check_countries = True if regions_how=='country' else False
    for regid, regname in region_ids.items():
        ts_data = _init_ts_data(freqs)
        ts_data['station_name'] = regname
        ts_data.update(meta_glob)

        for freq, cd in data.items():
            if cd is None:
                continue
            jsfreq = cd.data.jsdate.values.tolist()
            try:
                subset = cd.filter_region(regid,
                                          inplace=False,
                                          check_country_meta=check_countries)
            except DataCoverageError:
                const.print_log.info(
                    f'no data in {regid} ({freq}) to compute regional '
                    f'timeseries'
                    )
                ts_data[f'{freq}_date'] = jsfreq
                ts_data[f'{freq}_obs'] = [np.nan] * len(jsfreq)
                ts_data[f'{freq}_mod'] = [np.nan] * len(jsfreq)
                continue


            if subset.has_latlon_dims:
                avg = subset.data.mean(dim=('latitude', 'longitude'))
            else:
                avg = subset.data.mean(dim='station_name')
            obs_vals = avg[0].data.tolist()
            mod_vals = avg[1].data.tolist()
            ts_data[f'{freq}_date'] = jsfreq
            ts_data[f'{freq}_obs'] = obs_vals
            ts_data[f'{freq}_mod'] = mod_vals
         


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
        tsel = coldata.data.data[:,tcond]
        tsel[:,:,scond] = np.nan
        coldata.data.data[:,tcond] = tsel

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
    AeroValConfigError
        If colocated data in yearly resolution is not available in input data

    Returns
    -------
    output : dict
        like input `data` but with annual constrained applied.

    """
    output = {}
    if not 'yearly' in data or data['yearly'] is None:
        raise AeroValConfigError(
            'Cannot apply annual_stats_constrained option. '
            'Please add "yearly" in your setup (see attribute '
            '"statistics_json" in AerocomEvaluation class)')
    yearly = data['yearly']
    for tst, cd in data.items():
        if cd is None:
            output[tst] = None
        else:
            output[tst] = _apply_annual_constraint_helper(cd, yearly)
    return output

def _prep_stats_json(stats):
    for k, v in stats.items():
        try:
            stats[k] = np.float64(v) # for json encoder...
        except Exception:
            # value is str (e.g. for weighted stats)
            # 'NOTE': 'Weights were not applied to FGE and kendall and spearman corr (not implemented)'
            stats[k] = v
    return stats

def _get_extended_stats(coldata, use_weights):

    stats = coldata.calc_statistics(use_area_weights=use_weights)

    (stats['R_spatial_mean'],
     stats['R_spatial_median']) = _calc_spatial_corr(coldata, use_weights)

    (stats['R_temporal_mean'],
     stats['R_temporal_median']) = _calc_temporal_corr(coldata)

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
    return (coldata.calc_spatial_statistics(
                                aggr='mean',
                                use_area_weights=use_weights
                                )['R'],
            coldata.calc_spatial_statistics(
                                aggr='median',
                                use_area_weights=use_weights
                                )['R']
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
    arr = coldata.data
    # Use only sites that contain at least 3 valid data points (otherwise
    # correlation will be 1).
    obs_ok = arr[0].count(dim='time') > 2
    arr = arr.where(obs_ok, drop=True)
    if np.prod(arr.shape) == 0:
        return np.nan, np.nan
    corr_time = xr.corr(arr[1], arr[0], dim='time')
    return (np.nanmean(corr_time.data), np.nanmedian(corr_time.data))

def _select_period_season_coldata(coldata, period, season):
    tslice = _period_str_to_timeslice(period)
    # expensive, try use solution with numpy indexing directly...
    # also, keep an eye on: https://github.com/pydata/xarray/issues/2799
    arr = coldata.data.sel(time=tslice)
    if len(arr.time) == 0:
        raise DataCoverageError(f'No data available in period {period}')
    if season != 'all':
        if not season in arr.season:
            raise DataCoverageError(f'No data available in {season} in '
                                    f'period {period}')
        elif TsType(coldata.ts_type) < 'monthly':
            raise TemporalResolutionError(
                'Season selection is only available for monthly or higher  '
                'resolution data')
        mask = arr['season'] == season
        arr = arr.sel(time=arr['time'][mask])

    return ColocatedData(arr)

def _process_heatmap_data(data, region_ids, use_weights, use_country,
                          meta_glob, periods, seasons, 
                          add_trends, trends_min_yrs):

    output = {}
    stats_dummy = _init_stats_dummy()
    for freq, coldata in data.items():  
        output[freq] = hm_freq = {}
        use_dummy = True if coldata is None else False
        for regid, regname in region_ids.items():
            hm_freq[regname] = {}
            for per in periods:
                for season in seasons:
                    perstr = f'{per}-{season}'
                    if use_dummy:
                        stats = stats_dummy
                    else:
                        try:
                            subset = _select_period_season_coldata(coldata,
                                                                   per,
                                                                   season)
                            
                            trends_successful = False
                            if add_trends and freq != "daily":
                                # Calculates the start and stop years. min_yrs have a test value of 7 years. Should be set in cfg
                                (start, stop) = _get_min_max_year_periods([per])

                                if stop - start >= trends_min_yrs:
                                    try:
                                        subset_time_series = subset.get_regional_timeseries(regid)

                                        (obs_trend, mod_trend) = _make_trends_from_timeseries(  
                                                    subset_time_series["obs"],
                                                    subset_time_series["mod"],
                                                    freq,
                                                    season,
                                                    start,
                                                    stop,
                                                    trends_min_yrs
                                                    )

                                        trends_successful = True
                                    except AeroValTrendsError as e:
                                        msg = f"Failed to calculate trends, and will skip. This was due to {e}"
                                        const.logger.warning(msg)
                                

                            subset = subset.filter_region(region_id=regid,
                                                          check_country_meta=use_country)

                            stats = _get_extended_stats(subset, use_weights)

                            if add_trends and freq != "daily" and trends_successful:
                                # The whole trends dicts are placed in the stats dict
                                stats["obs_trend"] = obs_trend
                                stats["mod_trend"] = mod_trend


                        except (DataCoverageError, TemporalResolutionError) as e:
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
    mapping = np.ones_like(outer_idx)*-1
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
            count +=1
    return mapping.astype(int)

def _process_statistics_timeseries(data, freq, region_ids,
                                   use_weights, use_country,
                                   data_freq):
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
            f'Desired input frequency {data_freq} is lower than desired '
            f'output frequency {freq}')

    output = {}
    if not data_freq in data or data[data_freq] is None:
        raise TemporalResolutionError(
            f'failed to compute statistics timeseries, no co-located data '
            f'available in specified base resolution {data_freq}')

    coldata = data[data_freq]

    # get time index of output frequency
    to_idx = data[freq].data.time.values
    tstr = TsType(freq).to_numpy_freq()
    # list of strings of output timestamps (used below to select the
    # individual periods)
    to_idx_str = [str(x) for x in to_idx.astype(f'datetime64[{tstr}]')]
    jsdate = _get_jsdate(to_idx)

    for regid, regname in region_ids.items():
        output[regname] = {}
        try:
            subset = coldata.filter_region(region_id=regid,
                                        check_country_meta=use_country)
        except DataCoverageError:
            continue
        for i, js in enumerate(jsdate):
            per = to_idx_str[i]
            try:
                arr = ColocatedData(subset.data.sel(time=per))
                stats = arr.calc_statistics(use_area_weights=use_weights)
                output[regname][str(js)] = _prep_stats_json(stats)
            except DataCoverageError:
                pass

    return output

def _get_jsdate(nparr):
    dt = nparr.astype('datetime64[s]')
    offs = np.datetime64('1970', 's')
    return (dt-offs).astype(int)*1000

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
            cd = coldata.resample_time(to, settings_from_meta=True,
                                       inplace=False)
        # add season coordinate for later filtering
        arr = cd.data
        arr['season'] = arr.time.dt.season
        jsdates = _get_jsdate(arr.time.values)
        arr = arr.assign_coords(jsdate=('time', jsdates))
        cd.data = arr
        data_arrs[to] = cd

    return data_arrs

def _start_stop_from_periods(periods):
    start, stop = _get_min_max_year_periods(periods)
    return start_stop(start, stop+1)


class ColdataToJsonEngine(ProcessingEngine):

    def run(self, coldata : ColocatedData):
        """
        Creates all json files for one ColocatedData object

        Parameters
        ----------
        coldata : ColocatedData
            colocated data to be processed.
        cfg : EvalSetup
            setup of experiment.
        exp_output : ExperimentOutput
            DESCRIPTION.

        Raises
        ------
        NotImplementedError
            DESCRIPTION.
        ValueError
            DESCRIPTION.
        AeroValConfigError
            DESCRIPTION.

        Returns
        -------
        None.

        """
        t00 = time()
        use_weights = self.cfg.statistics_opts.weighted_stats
        freqs = self.cfg.time_cfg.freqs
        periods = self.cfg.time_cfg.periods
        main_freq = self.cfg.time_cfg.main_freq
        annual_stats_constrained = self.cfg.statistics_opts.annual_stats_constrained

        out_dirs = self.cfg.path_manager.get_json_output_dirs(True)
        regions_json = self.exp_output.regions_file
        regions_how = self.cfg.webdisp_opts.regions_how

        stats_min_num = self.cfg.statistics_opts.MIN_NUM
        seasons = self.cfg.time_cfg.SEASONS

        vert_code = coldata.get_meta_item('vert_code')
        diurnal_only = coldata.get_meta_item('diurnal_only')

        add_trends = self.cfg.statistics_opts.add_trends
        trends_min_yrs = self.cfg.statistics_opts.trends_min_yrs

        # ToDo: some of the checks below could be done automatically in
        # EvalSetup, and at an earlier stage
        if vert_code == 'ModelLevel':
            raise NotImplementedError('Coming (not so) soon...')

        # this will need to be figured out as soon as there is altitude
        elif 'altitude' in coldata.data.dims:
            raise NotImplementedError('Cannot yet handle profile data')

        elif not isinstance(coldata, ColocatedData):
            raise ValueError('Need ColocatedData object, got {}'
                             .format(type(coldata)))

        elif coldata.has_latlon_dims and regions_how=='country':
            raise NotImplementedError('Cannot yet apply country filtering for '
                                      '4D colocated data instances')
        elif not main_freq in freqs:
            raise AeroValConfigError(
                f'Scatter plot frequency {main_freq} is not in '
                f'experiment frequencies: {freqs}'
                )
        if self.cfg.statistics_opts.stats_tseries_base_freq is not None:
            if not self.cfg.statistics_opts.stats_tseries_base_freq in freqs:
                raise AeroValConfigError(
                    f'Base frequency for statistics timeseries needs to be '
                    f'specified in experiment frequencies: {freqs}')
        # init some stuff
        if 'var_name' in coldata.metadata:
            obs_var = coldata.metadata['var_name'][0]
            model_var = coldata.metadata['var_name'][1]
        else:
            obs_var = model_var = 'UNDEFINED'

        model_name = coldata.model_name
        obs_name = coldata.obs_name

        var_name_web = self.cfg.model_cfg.get_entry(model_name).get_varname_web(model_var,
                                                                           obs_var)

        const.print_log.info(
            f'Computing json files for {model_name} ({model_var}) vs. '
            f'{obs_name} ({obs_var})'
            )

        meta_glob = _init_meta_glob(coldata,
                                    vert_code=vert_code,
                                    obs_name=obs_name,
                                    model_name=model_name,
                                    var_name_web=var_name_web)

        # get region IDs
        (regborders, regs, regnames) = init_regions_web(coldata, regions_how)

        update_regions_json(regborders, regions_json)

        use_country = True if regions_how == 'country' else False

        data = _init_data_default_frequencies(coldata,
                                              freqs)
        if annual_stats_constrained:
            data = _apply_annual_constraint(data)

        if not diurnal_only:
            const.print_log.info('Processing statistics timeseries for all regions')
            input_freq = self.cfg.statistics_opts.stats_tseries_base_freq
            try:
                stats_ts = _process_statistics_timeseries(
                    data=data,
                    freq=main_freq,
                    region_ids=regnames,
                    use_weights=use_weights,
                    use_country=use_country,
                    data_freq=input_freq)
            except TemporalResolutionError:
                stats_ts = {}

            ts_file = os.path.join(out_dirs['hm/ts'], 'stats_ts.json')
            _add_entry_json(ts_file, stats_ts, obs_name, var_name_web,
                            vert_code, model_name, model_var)

            const.print_log.info('Processing heatmap data for all regions')
            hm_all = _process_heatmap_data(data, regnames, use_weights,
                                           use_country, meta_glob,
                                           periods,
                                           seasons,
                                           add_trends,
                                           trends_min_yrs,
                                           )

            for freq, hm_data in hm_all.items():
                fname = get_heatmap_filename(freq)

                hm_file = os.path.join(out_dirs['hm'], fname)

                _add_entry_json(hm_file, hm_data, obs_name, var_name_web,
                                vert_code, model_name, model_var)

            const.print_log.info('Processing regional timeseries for all regions')
            ts_objs_regional = _process_regional_timeseries(data,
                                                            regnames,
                                                            regions_how,
                                                            meta_glob)

            _write_site_data(ts_objs_regional, out_dirs['ts'])
            if coldata.has_latlon_dims:
                for cd in data.values():
                    if cd is not None:
                        cd.data = cd.flatten_latlondim_station_name().data

            const.print_log.info('Processing individual site timeseries data')
            (ts_objs,
             map_meta,
             site_indices) = _process_sites(data, regs, regions_how, meta_glob)

            _write_site_data(ts_objs, out_dirs['ts'])

            map_data, scat_data = _process_map_and_scat(data, map_meta,
                                                        site_indices,
                                                        periods,
                                                        main_freq,
                                                        stats_min_num,
                                                        seasons,
                                                        add_trends,
                                                        trends_min_yrs,
                                                        )

            map_name = get_json_mapname(obs_name, var_name_web, model_name,
                                        model_var, vert_code)

            outfile_map =  os.path.join(out_dirs['map'], map_name)
            write_json(map_data, outfile_map, ignore_nan=True)

            outfile_scat =  os.path.join(out_dirs['scat'], map_name)
            write_json(scat_data, outfile_scat, ignore_nan=True)

        if coldata.ts_type == 'hourly':
            const.print_log.info('Processing diurnal profiles')
            (ts_objs_weekly,
             ts_objs_weekly_reg) = _process_sites_weekly_ts(coldata, regions_how,
                                                            regnames, meta_glob)
            outdir = os.path.join(out_dirs['ts/diurnal'])
            for ts_data_weekly in ts_objs_weekly:
                #writes json file
                _write_stationdata_json(ts_data_weekly, outdir)
            if ts_objs_weekly_reg != None:
                for ts_data_weekly_reg in ts_objs_weekly_reg:
                    #writes json file
                    _write_stationdata_json(ts_data_weekly_reg, outdir)

        const.print_log.info(
            f'Finished computing json files for {model_name} ({model_var}) vs. '
            f'{obs_name} ({obs_var})'
            )

        dt = time() - t00
        const.print_log.info(f'Time expired (TOTAL): {dt:.2f} s')
