#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 14:00:44 2019
"""
import os, glob, shutil
import numpy as np
import simplejson
from pyaerocom import const
from pyaerocom._lowlevel_helpers import sort_dict_by_name
from pyaerocom.io.helpers import save_dict_json
from pyaerocom.web.helpers import read_json, write_json
from pyaerocom.web.const import (HEATMAP_FILENAME_EVAL_IFACE_MONTHLY,
                                 HEATMAP_FILENAME_EVAL_IFACE_DAILY)
from pyaerocom.colocateddata import ColocatedData
from pyaerocom.mathutils import calc_statistics
from pyaerocom.tstype import TsType
from pyaerocom.exceptions import DataDimensionError, TemporalResolutionError
from pyaerocom.region import (get_all_default_region_ids,
                              find_closest_region_coord,
                              get_all_default_regions, Region)

#from pyaerocom import __version__ as PYA_VERSION

def delete_experiment_data_evaluation_iface(base_dir, proj_id, exp_id):
    """Delete all data associated with a certain experiment

    Parameters
    ----------
    base_dir : str, optional
        basic output direcory (containg subdirs of all projects)
    proj_name : str, optional
        name of project, if None, then this project is used
    exp_name : str, optional
        name experiment, if None, then this project is used
    """

    p = os.path.join(base_dir, proj_id, exp_id)
    if not os.path.exists(p):
        raise NameError('No such data directory found: {}'.format(p))

    shutil.rmtree(p)

def get_all_config_files_evaluation_iface(config_dir):
    """

    Note
    ----
    This code only checks json configuration files, not .py module files
    containing configuration.

    Parameters
    ----------
    config_dir : str
        directory containing config json files for AerocomEvaluation interface

    Returns
    -------
    dict
        nested dictionary containing file paths of all config files that were
        detected, where first level of dict id `proj_id` and second level
        is `exp_id`.
    """

    results = {}

    for file in glob.glob('{}/*.json'.format(config_dir)):
        spl = os.path.basename(file).split('_')
        if not len(spl) == 3 or not spl[0] =='cfg':
            raise NameError('Invalid config file name ', file)
        proj, exp = spl[1], spl[2].split('.')[0]
        if not proj in results:
            results[proj] = {}
        results[proj][exp] = file
    return results

def reorder_experiments_menu_evaluation_iface(menu_file, exp_order=None):
    """Reorder experiment order in evaluation interface

    Parameters
    ----------
    menu_file : str
        file path of menu.json file
    exp_order : str or list, optional
        desired experiment order (must not contain all available experiments
        in menu)
    """
    current = read_json(menu_file)
    if exp_order is None:
        # keep the way it is
        exp_order = list(current.keys())
    elif isinstance(exp_order, str):
        exp_order = [exp_order]
    if not isinstance(exp_order, list):
        raise ValueError('Invalid input for exp_order, need None, str or list')

    new = sort_dict_by_name(current, pref_list=exp_order)
    write_json(new, menu_file, indent=4)

def update_menu_evaluation_iface(config, ignore_experiments=None):
    """Update menu for Aerocom Evaluation interface

    The menu.json file is created based on the available json map files in the
    map directory of an experiment.

    Parameters
    ----------
    config : AerocomEvaluation
        instance of config class that has all relevant paths specified
    ignore_experiments : list, optional
        list containing experiment IDs that may be in the current menu.json
        file and that are supposed to be removed from it.
    """
    def var_dummy():
        """Helper that creates empty dict for variable info"""
        return {'type'      :   '',
                'cat'       :   '',
                'name'      :   '',
                'longname'  :   '',
                'obs'       :   {}}

    new = {}
    exp_id = config.exp_id
    if ignore_experiments is None:
        ignore_experiments = []
    try:
        tab = config.get_web_overview_table()
    except FileNotFoundError:
        import pandas as pd
        tab = pd.DataFrame()

    for index, info in tab.iterrows():
        obs_var, obs_name, vert_code, mod_name, mod_var = info
        if not obs_var in new:
            const.print_log.info('Adding new observation variable: {}'
                                 .format(obs_var))
            new[obs_var] = d = var_dummy()
            name, tp, cat = config.get_obsvar_name_and_type(obs_var)

            d['name'] = name
            d['type'] = tp
            d['cat']  =cat
            d['longname'] = const.VARS[obs_var].description
        else:
            d = new[obs_var]

        if not obs_name in d['obs']:
            d['obs'][obs_name] = dobs = {}
        else:
            dobs = d['obs'][obs_name]

        if not vert_code in dobs:
            dobs[vert_code] = dobs_vert = {}
        else:
            dobs_vert = dobs[vert_code]
        if mod_name in dobs_vert:
            const.print_log.warning('Overwriting old entry for {}: {}'
                                    .format(mod_name, dobs_vert[mod_name]))
        dobs_vert[mod_name] = {'dir' : mod_name,
                               'id'  : config.model_config[mod_name]['model_id'],
                               'var' : mod_var}

    if len(new)  > 0:
        _new = {}
        for var in config.var_order_menu:
            try:
                _new[var] = new[var]
            except Exception:
                const.print_log.info('No variable {} found'.format(var))
        for var, info in new.items():
            if not var in _new:
                _new[var] = info
        new = _new

    new_sorted = {}
    for var, info in new.items():
        new_sorted[var] = info
        sorted_obs = sort_dict_by_name(info['obs'])
        new_sorted[var]['obs'] = sorted_obs
        for obs_name, vert_codes in sorted_obs.items():
            vert_codes_sorted = sort_dict_by_name(vert_codes)
            new_sorted[var]['obs'][obs_name] = vert_codes_sorted
            for vert_code, models in vert_codes_sorted.items():
                models_sorted = sort_dict_by_name(models)
                new_sorted[var]['obs'][obs_name][vert_code] = models_sorted
    new_menu = {}
    basedir = os.path.dirname(config.menu_file)
    available_exps = os.listdir(basedir)
    if os.path.exists(config.menu_file):
        current = read_json(config.menu_file)
        for exp, submenu in current.items():
            if exp in ignore_experiments or len(submenu) == 0:
                continue
            elif not exp in available_exps:
                const.print_log.info('Removing outdated experiment {} from '
                                     'menu.json'.format(exp))
                continue
            new_menu[exp] = submenu

    if config.exp_id in new_menu:
        const.print_log.warning('Sub menu for experiment {} already exists in '
                                'menu.json and will be overwritten'
                                .format(config.exp_id))
    if len(new_sorted) > 0:
        new_menu[exp_id] = new_sorted

    with open(config.menu_file, 'w+') as f:
        f.write(simplejson.dumps(new_menu, indent=4))

def make_info_table_evaluation_iface(config):
    from pyaerocom import ColocatedData
    import glob
    menu = config.menu_file

    SKIP_META = ['data_source', 'var_name', 'lon_range',
                 'lat_range', 'alt_range']
    with open(menu, 'r') as f:
        menu = simplejson.load(f)
    if not config.exp_id in menu:
        raise KeyError('No menu entry available for experiment {}'
                       .format(config.exp_id))
    table = {}
    exp = menu[config.exp_id]
    for obs_var, info in exp.items():
        for obs_name, vert_types in info['obs'].items():
            for vert_type, models in vert_types.items():
                for mname, minfo in models.items():
                    if not mname in table:
                        table[mname] = mi = {}
                        mi['id'] = model_id = minfo['id']
                    else:
                        mi = table[mname]
                        model_id = mi['id']
                        if minfo['id'] != mi['id']:
                            raise KeyError('Unexpected error: conflict in model ID and name')

                    try:
                        mo = mi['obs']
                    except Exception:
                        mi['obs'] = mo = {}
                    if 'var' in minfo:
                        mvar = minfo['var']
                    else:
                        mvar = obs_var
                    if not obs_var in mo:
                        mo[obs_var] = oi = {}
                    else:
                        oi = mo[obs_var]
                    if obs_name in oi:
                        raise Exception
                    oi[obs_name] = motab = {}
                    motab['model_var'] = mvar
                    motab['obs_id'] = config.get_obs_id(obs_name)
                    files = glob.glob('{}/{}/{}*REF-{}*.nc'
                                      .format(config.coldata_dir,
                                              model_id, mvar, obs_name))

                    if not len(files) == 1:
                        if len(files) > 1:
                            motab['MULTIFILES'] = len(files)
                        else:
                            motab['NOFILES'] = True
                        continue

                    coldata = ColocatedData(files[0])
                    for k, v in coldata.meta.items():
                        if not k in SKIP_META:
                            if isinstance(v, (list, tuple)):
                                if len(v) == 2:
                                    motab['{}_obs'.format(k)] = str(v[0])
                                    motab['{}_mod'.format(k)] = str(v[1])
                                else:
                                    motab[k] = ';'.join([str(x) for x in v])
                            else:
                                motab[k] = str(v)
    return table

def get_stationfile_name(station_name, obs_name, obs_var, vert_code):
    """Get name of station timeseries file"""
    return ('{}_OBS-{}:{}_{}.json'
            .format(station_name, obs_name, obs_var, vert_code))

def get_json_mapname(obs_name, obs_var, model_name, model_var,
                     vert_code):
    """Get name base name of json file"""
    return ('OBS-{}:{}_{}_MOD-{}:{}.json'
            .format(obs_name, obs_var, vert_code, model_name, model_var))

def _write_stationdata_json(ts_data, out_dirs):
    """
    This method writes time series data given in a dictionary to .json files

    Parameters
    ----------
    ts_data : dict
        A dictionary containing all processed time series data.
    out_dirs : list?
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

    fp = os.path.join(out_dirs['ts'], filename)
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

def add_entry_heatmap_json(heatmap_file, result, obs_name, obs_var, vert_code,
                           model_name, model_var):
    fp = heatmap_file
    if os.path.exists(fp):
        try:
            with open(fp, 'r') as f:
                current = simplejson.load(f)
        except Exception as e:
            raise Exception('Fatal: could not open existing json file: {}. '
                            'Reason: {}'.format(fp, repr(e)))
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
    if model_var in mn:
        const.print_log.info('Overwriting existing heatmap statistics for '
                             'model {}/{} ({}, {}, {}) in glob_stats.json'
                             .format(model_name, model_var, obs_var, obs_name,
                                     vert_code))
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
        if not coldata.data.ndim == 4:
            raise DataDimensionError('Invalid number of dimensions. '
                                     'Need 4, got: {}'
                                     .format(coldata.data.dims))
        elif not 'latitude' in coldata.data.dims and 'longitude' in coldata.data.dims:
            raise DataDimensionError('Need latitude and longitude '
                                     'dimension. Got {}'
                                     .format(coldata.data.dims))
        coldata.data = coldata.data.stack(station_name=('latitude',
                                                        'longitude'))
    return coldata

def _prepare_default_regions_json():
    regs = {}
    for regname in get_all_default_region_ids():
        reg = Region(regname)
        regs[regname] = r = {}
        latr = reg.lat_range
        r['minLat'] = latr[0]
        r['maxLat'] = latr[1]
        lonr = reg.lon_range
        r['minLon'] = lonr[0]
        r['maxLon'] = lonr[1]
    return regs

def init_regions_web(coldata, regions_how):
    default_regs = _prepare_default_regions_json()
    if regions_how == 'default':
        return default_regs
        #region_ids = get_all_default_region_ids()
    elif regions_how == 'country':
        regs = {}
        regs['WORLD'] = default_regs['WORLD']
        coldata.check_set_countries(True)
        regs.update(coldata.get_country_codes())
        return regs
        #region_ids = coldata.countries_available
    elif regions_how == 'htap':
        raise NotImplementedError('Support for HTAP regions is coming soon')
    else:
        raise ValueError('Invalid input for regions_how', regions_how)

def update_regions_json(region_defs, regions_json):
    if os.path.exists(regions_json):
        current = read_json(regions_json)
    else:
        current = {}

    for region_id, region_info in region_defs.items():
        if not region_id in current:
            current[region_id] = region_info
    save_dict_json(current, regions_json)
    return current

def _init_data_default_frequenciesOLD(coldata, colocation_settings):
    ts_types_order = const.GRID_IO.TS_TYPES
    to_ts_types = ['daily', 'monthly', 'yearly']

    data_arrs = dict.fromkeys(to_ts_types)
    jsdate = dict.fromkeys(to_ts_types)

    ts_type = coldata.meta['ts_type']
    for freq in to_ts_types:
        if ts_types_order.index(freq) < ts_types_order.index(ts_type):
            data_arrs[freq] = None
        elif ts_types_order.index(freq) == ts_types_order.index(ts_type):
            data_arrs[freq] = coldata.data

            js = (coldata.data.time.values.astype('datetime64[s]') -
                  np.datetime64('1970', '[s]')).astype(int) * 1000
            jsdate[freq] = js.tolist()

        else:
            colstp = colocation_settings
            _a = coldata.resample_time(to_ts_type=freq,
                                 apply_constraints=colstp.apply_time_resampling_constraints,
                                 min_num_obs=colstp.min_num_obs,
                                 colocate_time=colstp.colocate_time,
                                 inplace=False).data
            data_arrs[freq] = _a #= resample_time_dataarray(arr, freq=freq)

            js = (_a.time.values.astype('datetime64[s]') -
                  np.datetime64('1970', '[s]')).astype(int) * 1000
            jsdate[freq] = js.tolist()
    return (data_arrs, jsdate)

def _init_meta_glob(coldata, **kwargs):
    meta = coldata.meta

    # create metadata dictionary that is shared among all timeseries files
    meta_glob = {}
    meta_glob['pyaerocom_version'] = meta['pyaerocom']
    #meta_glob['obs_name'] = obs_name
    #meta_glob['model_name'] = model_name
    meta_glob['obs_var'] = meta['var_name'][0]
    meta_glob['obs_unit'] = meta['var_units'][0]
    #meta_glob['vert_code'] = vert_code
    meta_glob['obs_freq_src'] = meta['ts_type_src'][0]
    meta_glob['obs_revision'] = meta['revision_ref']

    meta_glob['mod_var'] = meta['var_name'][1]
    meta_glob['mod_unit'] = meta['var_units'][1]
    meta_glob['mod_freq_src'] = meta['ts_type_src'][1]
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

def _process_weekly_object_to_country_time_series(repw_res,meta_glob,regions_how,region_ids):
    """
    Process the xarray.Dataset objects returned by _create_diurnal_weekly_data_object
    into a dictionary containing country average time series data and metadata.

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
    region_ids : list?
        List of regional IDs

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
        for reg in region_ids:
            ts_data = {'time' : time,'seasonal' : {'obs' : {},'mod' : {}},'yearly' : {'obs' : {},'mod' : {}} }
            ts_data['station_name'] = reg
            ts_data.update(meta_glob)

            for res,repw in repw_res.items():
                if reg == 'WORLD':
                    subset = repw
                else:
                    subset = repw.where(repw.country == reg)

                # if cd.has_latlon_dims:
                #     avg = subset.data.mean(dim=('latitude', 'longitude'))
                # else:
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
    region_ids : list?
        List of regional IDs.
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

    default_regs = get_all_default_regions(use_all_in_ini=False)


    lats = repw_res['seasonal'].latitude.values.astype(np.float64)
    lons = repw_res['seasonal'].longitude.values.astype(np.float64)

    if 'altitude' in repw_res['seasonal'].coords:
        alts = repw_res['seasonal'].altitude.values.astype(np.float64)
    else:
        alts = [np.nan]*len(lats)

    if regions_how == 'country':
        countries = repw_res['seasonal'].country.values

    ts_objs = _process_weekly_object_to_station_time_series(repw_res,meta_glob)
    ts_objs_reg = _process_weekly_object_to_country_time_series(repw_res,
                                                                meta_glob,
                                                                regions_how,
                                                                region_ids)

    return ts_objs,ts_objs_reg

def _process_sites(data, jsdate, regions_how, meta_glob):
    ts_objs = []

    map_data = []
    scat_data = {}

    for freq, cd in data.items():
        if isinstance(cd, ColocatedData):
            _check_flatten_latlon_dims(cd)
            assert cd.dims == ('data_source', 'time', 'station_name')

    mon = data['monthly']

    stats_dummy = _init_stats_dummy()
    default_regs = get_all_default_regions(use_all_in_ini=False)

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

        if regions_how == 'default':
            region = find_closest_region_coord(stat_lat, stat_lon,
                                               default_regs=default_regs)
        elif regions_how == 'country':
            region = countries[i]

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
    for reg in region_ids:
        ts_data = _init_ts_data()
        ts_data['station_name'] = reg
        ts_data.update(meta_glob)

        for freq, cd in data.items():
            if not isinstance(cd, ColocatedData):
                continue
            subset = cd.filter_region(reg,
                                      inplace=False,
                                      check_country_meta=check_countries)
            if cd.has_latlon_dims:
                avg = subset.data.mean(dim=('latitude', 'longitude'))
            else:
                avg = subset.data.mean(dim='station_name')
            obs_vals = avg[0].data.tolist()
            mod_vals = avg[1].data.tolist()
            ts_data['{}_date'.format(freq)] = jsdate[freq]
            ts_data['{}_obs'.format(freq)] = obs_vals
            ts_data['{}_mod'.format(freq)] = mod_vals

        ts_objs.append(ts_data)
    return ts_objs

def _process_heatmap_data(data, region_ids, use_weights, use_country,
                          meta_glob):

    hm_all = dict(zip(('daily', 'monthly'), ({},{})))
    stats_dummy = _init_stats_dummy()
    for freq, hm_data in hm_all.items():
        for reg in region_ids:
            if not freq in data or data[freq] == None:
                hm_data[reg] = stats_dummy
            else:
                coldata = data[freq]

                filtered = coldata.filter_region(region_id=reg,
                                                 check_country_meta=use_country)

                stats = filtered.calc_statistics(use_area_weights=use_weights)
                for k, v in stats.items():
                    if not k=='NOTE':
                        v = np.float64(v)
                    stats[k] = v

                hm_data[reg] = stats
    return hm_all

def _get_jsdate(coldata):
    js = (coldata.data.time.values.astype('datetime64[s]') -
          np.datetime64('1970', '[s]')).astype(int) * 1000
    return js.tolist()

def _resample_time_coldata(coldata, freq, colstp):
    return coldata.resample_time(freq,
                apply_constraints=colstp.apply_time_resampling_constraints,
                min_num_obs=colstp.min_num_obs,
                colocate_time=colstp.colocate_time,
                inplace=False)

def _init_data_default_frequencies(coldata, colocation_settings):

    to_ts_types = ['daily',
                   'monthly',
                   'yearly']

    data_arrs = dict.fromkeys(to_ts_types)
    jsdate = dict.fromkeys(to_ts_types)

    tt = TsType(coldata.ts_type)

    if tt < TsType('monthly'):
        raise TemporalResolutionError('Temporal resolution ({}) is too low for '
                                      'web processing, need monthly or higher'
                                      .format(tt))
    elif tt > TsType('daily'):
        # resolution is higher than daily -> convert to daily
        coldata = _resample_time_coldata(coldata, 'daily', colocation_settings)
        tt = TsType('daily')

    for freq in to_ts_types:
        tt_freq = TsType(freq)
        if tt < tt_freq: # skip (coldata is in lower resolution)
            #data_arrs[freq] = None
            continue
        elif tt == tt_freq:
            data_arrs[freq] = coldata.copy()
            jsdate[freq] = _get_jsdate(coldata)

        else:
            cd = _resample_time_coldata(coldata, freq,
                                        colocation_settings)
            data_arrs[freq] = cd
            jsdate[freq] = _get_jsdate(cd)

    return (data_arrs, jsdate)

def compute_json_files_from_colocateddata(coldata, obs_name,
                                          model_name, use_weights,
                                          colocation_settings,
                                          vert_code, out_dirs,
                                          regions_json,
                                          web_iface_name,
                                          diurnal_only,
                                          regions_how=None,
                                          zeros_to_nan=True):

    """Creates all json files for one ColocatedData object

    ToDo
    ----
    Complete docstring
    """
    if vert_code == 'ModelLevel':
        raise NotImplementedError('Coming soon...')

    # this will need to be figured out as soon as there is altitude
    elif 'altitude' in coldata.data.dims:
        raise NotImplementedError('Cannot yet handle profile data')

    elif not isinstance(coldata, ColocatedData):
        raise ValueError('Need ColocatedData object, got {}'
                         .format(type(coldata)))

    elif coldata.has_latlon_dims and regions_how=='country':
        raise NotImplementedError('Cannot yet apply country filtering for '
                                  '4D colocated data instances')
    const.print_log.info('Computing json files for {} vs. {}'
                         .format(model_name, obs_name))

    if zeros_to_nan:
        coldata = coldata.set_zeros_nan()

    # init some stuff
    obs_var = coldata.meta['var_name'][0]
    model_var = coldata.meta['var_name'][1]
    meta_glob = _init_meta_glob(coldata,
                                vert_code=vert_code,
                                obs_name=obs_name,
                                model_name=model_name,
                                web_iface_name=web_iface_name)
    if regions_how is None:
        regions_how = 'default'

    # get region IDs
    regions = init_regions_web(coldata, regions_how)

    update_regions_json(regions, regions_json)

    region_ids = list(regions)

    use_country = True if regions_how == 'country' else False

    data, jsdate = _init_data_default_frequencies(coldata,
                                                  colocation_settings)

    if not diurnal_only:
        # FIRST: process data for heatmap json file
        hm_all = _process_heatmap_data(data, region_ids, use_weights,
                                        use_country=use_country,
                                        meta_glob=meta_glob)

        for freq, hm_data in hm_all.items():
            if freq == 'daily':
                fname = HEATMAP_FILENAME_EVAL_IFACE_DAILY
            else:
                fname = HEATMAP_FILENAME_EVAL_IFACE_MONTHLY

            hm_file = os.path.join(out_dirs['hm'], fname)

            add_entry_heatmap_json(hm_file, hm_data, web_iface_name, obs_var,
                                    vert_code, model_name, model_var)

        ts_objs_regional = _process_regional_timeseries(data,
                                                        jsdate,
                                                        region_ids,
                                                        regions_how,
                                                        meta_glob)

        for ts_data in ts_objs_regional:
            #writes json file
            _write_stationdata_json(ts_data, out_dirs)

        (map_data,
          scat_data,
          ts_objs) = _process_sites(data, jsdate,
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
            _write_stationdata_json(ts_data, out_dirs)

    if coldata.ts_type == 'hourly':
        ts_objs_weekly,ts_objs_weekly_reg = _process_sites_weekly_ts(coldata,regions_how, region_ids, meta_glob)
        for ts_data_weekly in ts_objs_weekly:
            #writes json file
            _write_diurnal_week_stationdata_json(ts_data_weekly, out_dirs)
        if ts_objs_weekly_reg != None:
            for ts_data_weekly_reg in ts_objs_weekly_reg:
                #writes json file
                _write_diurnal_week_stationdata_json(ts_data_weekly_reg, out_dirs)

if __name__ == '__main__':
    import pyaerocom as pya
    stp = pya.web.AerocomEvaluation('test', 'test')

    colfile = '/home/jonasg/github/aerocom_evaluation/coldata/PIII-optics2019-P/AEROCOM-MEDIAN_AP3-CTRL/od550aer_REF-AeronetSun_MOD-AEROCOM-MEDIAN_20100101_20101231_monthly_WORLD-noMOUNTAINS.nc'
    #colfile = '/home/jonasg/github/aerocom_evaluation/coldata/PIII-optics2019-P/AEROCOM-MEDIAN_AP3-CTRL/od550aer_REF-AATSR4.3-SU_MOD-AEROCOM-MEDIAN_20100101_20101231_monthly_WORLD-noMOUNTAINS.nc'

    coldata = ColocatedData(colfile)
    out_dirs = stp.out_dirs
    obs, mod = coldata.meta['data_source']

    rgf = stp.regions_file
    compute_json_files_from_colocateddata(coldata, obs,
                                          mod,
                                          use_weights=False,
                                          colocation_settings=stp.colocation_settings,
                                          vert_code='Column',
                                          out_dirs=out_dirs,
                                          regions_how='country',
                                          regions_json=rgf)
