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
from pyaerocom.web.const import HEATMAP_FILENAME_EVAL_IFACE
from pyaerocom.colocateddata import ColocatedData
from pyaerocom.mathutils import calc_statistics
from pyaerocom.exceptions import DataDimensionError
from pyaerocom.region import (get_all_default_region_ids,
                              find_closest_region_coord,
                              get_all_default_regions, Region)

from pyaerocom import __version__ as pyaerocom_version

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

def make_regions_json(regions_file):
    """Creates file regions.ini for web interface"""
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
    save_dict_json(regs, regions_file)
    return regs
    
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
    filename = get_stationfile_name(ts_data['station_name'], 
                                    ts_data['obs_name'],
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
        

       
def compute_json_files_from_colocateddata(coldata, obs_name, 
                                          model_name, use_weights,
                                          colocation_settings,
                                          vert_code, out_dirs,
                                          regions_by_country=False):
    
    """Creates all json files for one ColocatedData object
    
    ToDo
    ----
    Complete docstring
    """
    if regions_by_country:
        raise NotImplementedError('Region by country filter is coming soon...')
        
    if not isinstance(coldata, ColocatedData):
        raise ValueError('Need ColocatedData object, got {}'
                         .format(type(coldata)))
    stats_dummy = {}
    
    for k in calc_statistics([1], [1]):
        stats_dummy[k] = np.nan
    
    stacked = False
    if 'altitude' in coldata.data.dims:
        raise NotImplementedError('Cannot yet handle profile data')
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
        stacked = True
     
    assert coldata.data.dims == ('data_source', 'time', 'station_name')
    
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
    
    obs_var = coldata.meta['var_name'][0]
    model_var = coldata.meta['var_name'][1]
    
    ts_objs = []
    
    map_data = []
    scat_data = {}
    hm_data = {}
    
    # data used for heatmap display in interface
    if stacked:    
        hmd = ColocatedData(data_arrs[ts_type].unstack('station_name'))
    else:
        hmd = ColocatedData(data_arrs[ts_type])

    for reg in get_all_default_region_ids():
        filtered = hmd.filter_region(region_id=reg)
        stats = filtered.calc_statistics(use_area_weights=use_weights)
        for k, v in stats.items():
            if not k=='NOTE':
                v = np.float64(v)
            stats[k] = v
        
        hm_data[reg] = stats
    
    hm_file = os.path.join(out_dirs['hm'], HEATMAP_FILENAME_EVAL_IFACE)
    
    add_entry_heatmap_json(hm_file, hm_data, obs_name, obs_var, vert_code, 
                           model_name, model_var)
    
    if vert_code == 'ModelLevel':
        raise NotImplementedError('Coming soon...')
    const.print_log.info('Computing json files for {} vs. {}'
                         .format(model_name, obs_name))
    
    default_regs = get_all_default_regions(use_all_in_ini=False)
    
    meta = coldata.meta
    
    # create metadata dictionary that is shared among all timeseries files
    meta_glob = {}
    meta_glob['pyaerocom_version'] = pyaerocom_version
    meta_glob['obs_name'] = obs_name
    meta_glob['model_name'] = model_name
    meta_glob['obs_var'] = meta['var_name'][0]
    meta_glob['obs_unit'] = meta['var_units'][0]
    meta_glob['vert_code'] = vert_code
    meta_glob['obs_freq_src'] = meta['ts_type_src'][0]
    meta_glob['obs_revision'] = meta['revision_ref']
    
    meta_glob['mod_var'] = meta['var_name'][1]
    meta_glob['mod_unit'] = meta['var_units'][1]
    meta_glob['mod_freq_src'] = meta['ts_type_src'][1]
    
    lats = coldata.data.latitude.values.astype(np.float64)
    lons = coldata.data.longitude.values.astype(np.float64)
    if 'altitude' in coldata.data.coords:
        alts = coldata.data.altitude.values.astype(np.float64)
    else:
        alts = [np.nan]*len(lats)
        
    for i, stat_name in enumerate(coldata.data.station_name.values):
        has_data = False
        ts_data = {}
        ts_data['station_name'] = stat_name
        ts_data.update(meta_glob)
        
        stat_lat = lats[i]
        stat_lon = lons[i]
        stat_alt = alts[i]
        
        region = find_closest_region_coord(stat_lat, stat_lon,
                                           default_regs=default_regs)
        
        # station information for map view
        map_stat = {'site'      : stat_name, 
                    'lat'       : stat_lat, 
                    'lon'       : stat_lon,
                    'alt'       : stat_alt,
                    'region'    : region}
        
        for tres, arr in data_arrs.items():
            map_stat['{}_statistics'.format(tres)] = {}
            if arr is None:
                ts_data['{}_date'.format(tres)] = []
                ts_data['{}_obs'.format(tres)] = []
                ts_data['{}_mod'.format(tres)] = []
                map_stat['{}_statistics'.format(tres)].update(stats_dummy)
                continue
    
            obs_vals = arr.data[0, :, i]
            if all(np.isnan(obs_vals)):
                ts_data['{}_date'.format(tres)] = []
                ts_data['{}_obs'.format(tres)] = []
                ts_data['{}_mod'.format(tres)] = []
                map_stat['{}_statistics'.format(tres)].update(stats_dummy)
                continue
            has_data = True
            mod_vals = arr.data[1, :, i]
            
            if not len(jsdate[tres]) == len(obs_vals):
                raise Exception('Please debug...')
            
            ts_data['{}_date'.format(tres)] = jsdate[tres]
            ts_data['{}_obs'.format(tres)] = obs_vals.tolist()
            ts_data['{}_mod'.format(tres)] = mod_vals.tolist()
            
            station_statistics = calc_statistics(mod_vals, obs_vals)
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
        
    dirs = out_dirs

    map_name = get_json_mapname(obs_name, obs_var, model_name, 
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
        
if __name__ == '__main__':
    import pyaerocom as pya
    stp = pya.web.AerocomEvaluation('test', 'test')
    
    colfile = '/home/jonasg/github/aerocom_evaluation/coldata/PIII-optics2019-P/AEROCOM-MEDIAN_AP3-CTRL/od550aer_REF-AeronetSun_MOD-AEROCOM-MEDIAN_20100101_20101231_monthly_WORLD-noMOUNTAINS.nc'
    colfile = '/home/jonasg/github/aerocom_evaluation/coldata/PIII-optics2019-P/AEROCOM-MEDIAN_AP3-CTRL/od550aer_REF-AATSR4.3-SU_MOD-AEROCOM-MEDIAN_20100101_20101231_monthly_WORLD-noMOUNTAINS.nc'
    
    coldata = ColocatedData(colfile)
    out_dirs = stp.out_dirs
    obs_name, model_name = coldata.meta['data_source']
    
    compute_json_files_from_colocateddata(coldata, obs_name, 
                                          model_name, 
                                          use_weights=False,
                                          colocation_settings=stp.colocation_settings,
                                          vert_code='Column', 
                                          out_dirs=out_dirs)