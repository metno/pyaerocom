#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 14:00:44 2019
"""
import os
import numpy as np
import simplejson
import xarray as xr
from pyaerocom import const
from pyaerocom.io.helpers import save_dict_json
from pyaerocom.web.helpers import read_json, write_json
from pyaerocom.colocateddata import ColocatedData
from pyaerocom.mathutils import calc_statistics
from pyaerocom.tstype import TsType
from pyaerocom.exceptions import (AeroValConfigError,
                                  DataCoverageError)
from pyaerocom.region_defs import OLD_AEROCOM_REGIONS, HTAP_REGIONS_DEFAULT
from pyaerocom.region import (get_all_default_region_ids,
                              find_closest_region_coord,
                              Region)

SEASONS = ['all', 'DJF', 'MAM', 'JJA', 'SON']

def get_heatmap_filename(ts_type):
    return f'glob_stats_{ts_type}.json'

def get_stationfile_name(station_name, obs_name, obs_var, vert_code):
    """Get name of station timeseries file"""
    return ('{}_OBS-{}:{}_{}.json'
            .format(station_name, obs_name, obs_var, vert_code))

def get_json_mapname(obs_name, obs_var, model_name, model_var,
                     vert_code):
    """Get name base name of json file"""
    return ('OBS-{}:{}_{}_MOD-{}:{}.json'
            .format(obs_name, obs_var, vert_code, model_name, model_var))

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
                                    ts_data['web_iface_name'],
                                    ts_data['obs_var'],
                                    ts_data['vert_code'])

    fp = os.path.join(out_dir, filename)
    if os.path.exists(fp):
        with open(fp, 'r') as f:
            current = simplejson.load(f)
    else:
        current = {}
    current[ts_data['model_name']] = ts_data
    with open(fp, 'w') as f:
        simplejson.dump(current, f, ignore_nan=True)

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
                                    ts_data['web_iface_name'],
                                    ts_data['obs_var'],
                                    ts_data['vert_code'])

    fp = os.path.join(out_dirs['ts'],'dw', filename)
    if os.path.exists(fp):
        try:
            with open(fp, 'r') as f:
                current = simplejson.load(f)
        except Exception as e:
            raise Exception('Fatal: could not open existing json file: {}. '
                            'Reason: {}'.format(fp, repr(e)))
    else:
        current = {}
    current[ts_data['model_name']] = ts_data
    with open(fp, 'w') as f:
        simplejson.dump(current, f, ignore_nan=True)

def _add_entry_heatmap_json(heatmap_file, result, obs_name, obs_var, vert_code,
                            model_name, model_var):
    fp = heatmap_file
    if os.path.exists(fp):
        with open(fp, 'r') as f:
            current = simplejson.load(f)
    else:
        current = {}
    if not obs_var in current:
        current[obs_var] = {}
    ov = current[obs_var]
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
    with open(fp, 'w') as f:
        simplejson.dump(current, f, ignore_nan=True)

def _init_stats_dummy():
    # dummy for statistics dictionary for locations without data
    stats_dummy = {}
    for k in calc_statistics([1], [1]):
        stats_dummy[k] = np.nan
    return stats_dummy

def _check_flatten_latlon_dims(coldata):
    if not 'station_name' in coldata.data.coords:
        coldata.data = coldata.data.stack(station_name=('latitude',
                                                        'longitude'))
    return coldata

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
    save_dict_json(current, regions_json)
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
    meta_glob.update(kwargs)
    return meta_glob

def _init_ts_data():
    return dict(
        daily_date = [],
        daily_obs = [],
        daily_mod = [],
        monthly_date = [],
        monthly_obs = [],
        monthly_mod = [],
        yearly_date = [],
        yearly_obs = [],
        yearly_mod = []
        )

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

    if isinstance(coldata, ColocatedData):
        _check_flatten_latlon_dims(coldata)
        assert coldata.dims == ('data_source', 'time', 'station_name')

    repw_res = {'seasonal':_create_diurnal_weekly_data_object(coldata, 'seasonal')['rep_week'],
                'yearly':_create_diurnal_weekly_data_object(coldata, 'yearly')['rep_week'].expand_dims('period',axis=0),}

    ts_objs = _process_weekly_object_to_station_time_series(repw_res,meta_glob)
    ts_objs_reg = _process_weekly_object_to_country_time_series(repw_res,
                                                                meta_glob,
                                                                regions_how,
                                                                region_ids)

    return (ts_objs,ts_objs_reg)

def _process_sites(data, jsdate, regions, regions_how, meta_glob):
    #----------------------------------------------------------------------
    # MAP files: ADD stats for whole period, individual years, and seasons,
    #----------------------------------------------------------------------
    ts_objs = []

    map_data = []
    scat_data = {}

    for freq, cd in data.items():
        if isinstance(cd, ColocatedData):
            _check_flatten_latlon_dims(cd)
            assert cd.dims == ('data_source', 'time', 'station_name')

    mon = data['monthly']

    stats_dummy = _init_stats_dummy()

    lats = mon.data.latitude.values.astype(np.float64)
    lons = mon.data.longitude.values.astype(np.float64)

    if 'altitude' in mon.data.coords:
        alts = mon.data.altitude.values.astype(np.float64)
    else:
        alts = [np.nan]*len(lats)

    if regions_how == 'country':
        countries = mon.data.country.values
    dc = 0
    for i, stat_name in enumerate(mon.data.station_name.values):
        has_data = False
        ts_data = _init_ts_data()
        ts_data['station_name'] = stat_name
        ts_data.update(meta_glob)

        stat_lat = lats[i]
        stat_lon = lons[i]
        stat_alt = alts[i]

        if regions_how in ('default', 'htap'):
            region = find_closest_region_coord(stat_lat, stat_lon,
                                               regions=regions)
        elif regions_how == 'country':
            region = countries[i]
        else:
            raise ValueError(
                f'Fatal: invalid value {regions_how} for regions_how'
                )

        # station information for map view
        map_stat = {'site'      : stat_name,
                    'lat'       : stat_lat,
                    'lon'       : stat_lon,
                    'alt'       : stat_alt,
                    'region'    : region}

        for tres, coldata in data.items():

            map_stat['{}_statistics'.format(tres)] = {}
            if coldata is None:
                map_stat['{}_statistics'.format(tres)].update(stats_dummy)
                continue
            arr = coldata.data
            obs_vals = arr.data[0, :, i]
            if all(np.isnan(obs_vals)):
                map_stat['{}_statistics'.format(tres)].update(stats_dummy)
                continue
            has_data = True
            mod_vals = arr.data[1, :, i]
            ts_data['{}_date'.format(tres)] = jsdate[tres]
            ts_data['{}_obs'.format(tres)] = obs_vals.tolist()
            ts_data['{}_mod'.format(tres)] = mod_vals.tolist()

            station_statistics = calc_statistics(mod_vals, obs_vals,
                                                 min_num_valid=1)

            for k, v in station_statistics.items():
                station_statistics[k] = np.float64(v)
            map_stat['{}_statistics'.format(tres)] = station_statistics

        if has_data:
            ts_objs.append(ts_data)
            map_data.append(map_stat)
            scat_data[str(stat_name)] = sc = {}
            sc['obs'] = ts_data['monthly_obs']
            sc['mod'] = ts_data['monthly_mod']
            sc['region'] = region
            dc += 1
    return (map_data, scat_data, ts_objs)

def _process_regional_timeseries(data, jsdate, region_ids,
                                 regions_how, meta_glob):
    ts_objs = []
    check_countries = True if regions_how=='country' else False
    for regid, regname in region_ids.items():
        ts_data = _init_ts_data()
        ts_data['station_name'] = regname
        ts_data.update(meta_glob)

        for freq, cd in data.items():
            jsfreq = jsdate[freq]
            if not isinstance(cd, ColocatedData):
                continue
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
        elif tst == 'yearly':
            output[tst] = yearly
        else:
            output[tst] = _apply_annual_constraint_helper(cd, yearly)
    return output

def _get_stats_region(data, regid, use_weights, use_country):
    filtered = data.filter_region(region_id=regid,
                                  check_country_meta=use_country)

    # if all model and obsdata is NaN, use dummy stats (this can
    # e.g., be the case if colocate_time=True and all obs is NaN,
    # or if model domain is not covered by the region)
    if np.isnan(filtered.data.data).all():
        # use stats_dummy
        raise DataCoverageError(f'All data is NaN in {regid}')

    stats = filtered.calc_statistics(use_area_weights=use_weights)

    (stats['R_spatial_mean'],
     stats['R_spatial_median']) = _calc_spatial_corr(filtered, use_weights)

    (stats['R_temporal_mean'],
     stats['R_temporal_median']) = _calc_temporal_corr(filtered)


    for k, v in stats.items():
        try:
            stats[k] = np.float64(v) # for json encoder...
        except Exception:
            # value is str (e.g. for weighted stats)
            # 'NOTE': 'Weights were not applied to FGE and kendall and spearman corr (not implemented)'
            stats[k] = v
    return stats

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
    arr = coldata.data
    # Use only sites that contain at least 3 valid data points (otherwise
    # correlation will be 1).
    obs_ok = arr[0].count(dim='time') > 2
    arr = arr.where(obs_ok, drop=True)
    corr_time = xr.corr(arr[1], arr[0], dim='time')
    return (np.nanmean(corr_time.data), np.nanmedian(corr_time.data))

def _period_to_timeslice(period):
    spl = period.split('-')
    if len(spl) == 1:
        return slice(spl[0],spl[0])
    elif len(spl) == 2:
        return slice(*spl)
    raise ValueError(period)

def _select_period_season_coldata(coldata, period, season):
    tslice = _period_to_timeslice(period)
    arr = coldata.data.sel(time=tslice)
    if len(arr.time) == 0:
        raise DataCoverageError(f'No data available in period {period}')
    if season != 'all':
        if not season in arr.season:
            raise DataCoverageError(f'No data available in {season} in '
                                    f'period {period}')
        mask = arr['season'] == season
        arr = arr.sel(time=arr['time'][mask])

    return ColocatedData(arr)

def _process_heatmap_data(data, region_ids, use_weights, use_country,
                          meta_glob, statistics_periods):

    hm_all = {}
    stats_dummy = _init_stats_dummy()
    for freq, coldata in data.items():
        hm_all[freq] = hm_freq = {}
        use_dummy = True if coldata is None else False
        for regid, regname in region_ids.items():
            hm_freq[regname] = {}
            for per in statistics_periods:
                if use_dummy:
                    stats = stats_dummy
                else:
                    for season in SEASONS:
                        try:
                            subset = _select_period_season_coldata(coldata,
                                                                   per,
                                                                   season)

                            stats = _get_stats_region(subset, regid,
                                                      use_weights, use_country)
                        except DataCoverageError:
                            stats = stats_dummy

                        hm_freq[regname][f'{per}-{season}'] = stats
    return hm_all

def _get_jsdate(coldata):
    js = (coldata.data.time.values.astype('datetime64[s]') -
          np.datetime64('1970', '[s]')).astype(int) * 1000
    return js.tolist()

def _resample_time_coldata(coldata, freq, colstp):
    return coldata.resample_time(freq,
                apply_constraints=colstp['apply_time_resampling_constraints'],
                min_num_obs=colstp['min_num_obs'],
                how=colstp['resample_how'],
                colocate_time=colstp['colocate_time'],
                inplace=False)

def _init_data_default_frequencies(coldata, colocation_settings, to_ts_types):
    """
    Compute one colocated data object for each desired statistics frequency

    Parameters
    ----------
    coldata : ColocatedData
        Initial colocated data in a certain frequency
    colocation_settings : dict or similar
        colocation settings containing information about temporal resampling
        that is to be applied for downsampling.
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
    jsdate = dict.fromkeys(to_ts_types)

    from_tst = TsType(coldata.ts_type)

    for to in to_ts_types:
        to_tst = TsType(to)
        if from_tst < to_tst:
            continue
        elif from_tst == to_tst:
            cd = coldata.copy()
        else:
            cd = _resample_time_coldata(coldata, to,
                                        colocation_settings)
        # add season coordinate for later filtering
        cd.data['season'] = cd.data.time.dt.season
        data_arrs[to] = cd
        jsdate[to] = _get_jsdate(cd)

    return (data_arrs, jsdate)

def compute_json_files_from_colocateddata(coldata, obs_name,
                                          model_name, use_weights,
                                          colocation_settings,
                                          vert_code, out_dirs,
                                          regions_json,
                                          web_iface_name,
                                          diurnal_only,
                                          statistics_freqs,
                                          statistics_periods,
                                          regions_how=None,
                                          zeros_to_nan=False,
                                          annual_stats_constrained=False):

    """Creates all json files for one ColocatedData object

    ToDo
    ----
    Complete docstring
    """
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
    # init some stuff
    if 'var_name' in coldata.metadata:
        obs_var = coldata.metadata['var_name'][0]
        model_var = coldata.metadata['var_name'][1]
    else:
        obs_var = model_var = 'UNDEFINED'

    const.print_log.info(
        f'Computing json files for {model_name} ({model_var}) vs. '
        f'{obs_name} ({obs_var})'
        )

    meta_glob = _init_meta_glob(coldata,
                                vert_code=vert_code,
                                obs_name=obs_name,
                                model_name=model_name,
                                web_iface_name=web_iface_name)
    if regions_how is None:
        regions_how = 'default'

    # get region IDs
    (regborders, regs, regnames) = init_regions_web(coldata, regions_how)

    update_regions_json(regborders, regions_json)

    use_country = True if regions_how == 'country' else False

    if zeros_to_nan:
        coldata = coldata.set_zeros_nan()

    data, jsdate = _init_data_default_frequencies(coldata,
                                                  colocation_settings,
                                                  statistics_freqs)
    if annual_stats_constrained:
        data = _apply_annual_constraint(data)

    if not diurnal_only:
        # FIRST: process data for heatmap json file
        const.print_log.info('Processing heatmap data for all regions')
        hm_all = _process_heatmap_data(
            data, regnames, use_weights,
            use_country=use_country,
            meta_glob=meta_glob,
            statistics_periods=statistics_periods
            )

        for freq, hm_data in hm_all.items():
            fname = get_heatmap_filename(freq)

            hm_file = os.path.join(out_dirs['hm'], fname)

            _add_entry_heatmap_json(hm_file, hm_data, web_iface_name, obs_var,
                                    vert_code, model_name, model_var)

        const.print_log.info('Processing regional timeseries for all regions')
        ts_objs_regional = _process_regional_timeseries(data,
                                                        jsdate,
                                                        regnames,
                                                        regions_how,
                                                        meta_glob)

        for ts_data in ts_objs_regional:
            #writes json file
            _write_stationdata_json(ts_data, out_dirs['ts'])

        const.print_log.info('Processing individual site timeseries data')
        (map_data,
         scat_data,
         ts_objs) = _process_sites(data, jsdate,
                                   regs,
                                   regions_how,
                                   meta_glob=meta_glob)

        dirs = out_dirs

        map_name = get_json_mapname(web_iface_name, obs_var, model_name,
                                    model_var, vert_code)

        outfile_map =  os.path.join(dirs['map'], map_name)
        with open(outfile_map, 'w') as f:
            simplejson.dump(map_data, f, ignore_nan=True)

        outfile_scat =  os.path.join(dirs['scat'], map_name)
        with open(outfile_scat, 'w') as f:
            simplejson.dump(scat_data, f, ignore_nan=True)

        for ts_data in ts_objs:
            #writes json file
            _write_stationdata_json(ts_data, out_dirs['ts'])

    if coldata.ts_type == 'hourly':
        const.print_log.info('Processing diurnal profiles')
        (ts_objs_weekly,
         ts_objs_weekly_reg) = _process_sites_weekly_ts(coldata, regions_how,
                                                        regnames, meta_glob)
        outdir = os.path.join(out_dirs['ts'],'dw')
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

if __name__ == '__main__':
    import pyaerocom as pya
    stp = pya.web.AerocomEvaluation('test', 'test')

    colfile = '/home/jonasg/github/aerocom_evaluation/coldata/PIII-optics2019-P/AEROCOM-MEDIAN_AP3-CTRL/od550aer_REF-AeronetSun_MOD-AEROCOM-MEDIAN_20100101_20101231_monthly_WORLD-noMOUNTAINS.nc'
    #colfile = '/home/jonasg/github/aerocom_evaluation/coldata/PIII-optics2019-P/AEROCOM-MEDIAN_AP3-CTRL/od550aer_REF-AATSR4.3-SU_MOD-AEROCOM-MEDIAN_20100101_20101231_monthly_WORLD-noMOUNTAINS.nc'

    coldata = ColocatedData(colfile)
    out_dirs = stp.out_dirs
    obs, mod = coldata.metadata['data_source']

    rgf = stp.regions_file
    compute_json_files_from_colocateddata(coldata, obs,
                                          mod,
                                          use_weights=False,
                                          colocation_settings=stp.colocation_settings,
                                          vert_code='Column',
                                          out_dirs=out_dirs,
                                          regions_how='country',
                                          regions_json=rgf)
