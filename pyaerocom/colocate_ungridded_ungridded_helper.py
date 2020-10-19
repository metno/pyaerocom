
import numpy as np

from pyaerocom import const
from pyaerocom._lowlevel_helpers import invalid_input_err_str
from pyaerocom.geodesy import find_coord_indices_within_distance
from pyaerocom.stationdata import StationData
from pyaerocom.helpers import sort_ts_types
from pyaerocom.colocation import _colocate_site_data_helper
import os

def combine_vardata_ungridded(data1, var1, data2=None, var2=None,
                              match_stats_how='closest',
                              match_stats_tol_km=1,
                              merge_how='combine',
                              merge_eval_fun=None,
                              var_name_out=None,
                              resample_how='mean',
                              apply_time_resampling_constraints=False,
                              min_num_obs=None):
    """
    Combine and colocate different variables from UngriddedData

    Parameters
    ----------
    data1 : UngriddedData
        input data object containing data of first input variable (`var1`)
    var1 : str
        name of first input variable
    data2 : UngriddedData, optional
        input data object containing data of second input variable (`var2`).
        The default is None, in which case `data1` is used to access `var2`.
    var2 : str, optional
        name of second input variable. The default is None.
    match_stats_how : str, optional
        String specifying how site locations are supposed to be matched.
        The default is 'closest'. Supported are 'closest' and 'station_name'.
    match_stats_tol_km : float, optional
        radius tolerance in km for matching site locations when using 'closest'
        for site location matching. The default is 1.
    merge_how : str, optional
        String specifying how to merge variable data at site locations.
        The default is 'combine'. If both input variables are the same and
        `combine` is used, then the first input variable will be preferred over
        the other. Supported are 'combine', 'mean' and 'eval', for the latter,
        `merge_eval_fun` needs to be specified explicitly.
    merge_eval_fun : str, optional
        String specifying how `var1` and `var2` data should be evaluated (only
        relevant if `merge_how='eval'` is used) . The default is None.
    var_name_out : str, optional
        Name of output variable (only relevant if `merge_how='eval'` is used).
        Default is None.
    resample_how : str, optional
        String specifying how temporal resampling should be done. The default
        is 'mean'.
    apply_time_resampling_constraints : bool, optional
        Boolean specifying whether constraints should be applied for temporal
        resampling (e.g. at least X daily values to get a monthly mean).
        The default is False.
    min_num_obs : int or dict, optional
        Minimum number of observations for temporal resampling.
        The default is None in which case pyaerocom default is used, which
        is available via pyaerocom.const.OBS_MIN_NUM_RESAMPLE.

    Raises
    ------
    ValueError
        If input for `merge_how` or `match_stats_how` is invalid.
    NotImplementedError
        If one of the input UngriddedData objects contains more than one
        dataset.

    Returns
    -------
    merged_stats : list
        list of `StationData` objects containing the colocated and combined
        variable data.

    """
    if data2 is None:
        data2 = data
    if var2 is None:
        var2 = var1
    if data2 is data1 and var2 == var1:
        raise ValueError('nothing to combine...')

    if len(data1.contains_datasets) > 1:
        raise NotImplementedError
    elif len(data2.contains_datasets) > 1:
        raise NotImplementedError

    dataset1 = data1.contains_datasets[0]
    dataset2 = data2.contains_datasets[0]

    id1='{};{}'.format(dataset1, var1)
    id2='{};{}'.format(dataset2, var2)

    data1_stats = data1.to_station_data_all(var1)#, start=start, stop=stop)
    data1_stats['var_name'] = var1
    data1_stats['id'] = id1

    data2_stats = data2.to_station_data_all(var2)#, start=start, stop=stop)
    data2_stats['var_name'] = var2
    data2_stats['id'] = id2


    if len(data1_stats['latitude']) <= len(data2_stats['latitude']): #
        short = data1_stats
        long = data2_stats
    else:
        short = data2_stats
        long = data1_stats

    match_stats_opts = ['station_name', 'closest']


    if not match_stats_how in match_stats_opts:
        raise ValueError('Invalid input for match_stats_how {}, choose from {}'
                         .format(match_stats_how, match_stats_opts))

    merge_how_opts = ['combine', 'mean', 'eval']

    # if e.g. merge_how is combine and var==var2, then the preferred
    # dataset & variable can be provided via this instance
    prefer = id1

    if not merge_how in merge_how_opts:
        raise ValueError(invalid_input_err_str(
            'merge_how', merge_how, merge_how_opts))

    elif merge_how == 'eval':
        if merge_eval_fun is None:
            raise ValueError('Please specify evaluation function for mode eval')
        elif not all([x in merge_eval_fun for x in [id1, id2]]):
            raise ValueError('merge_eval_fun needs to include both input '
                             'datasets;variables (e.g. {} + {}'
                             .format(id1, id2))
        if '=' in merge_eval_fun:
            spl = merge_eval_fun.split('=')
            if len(spl) > 2:
                raise ValueError('merge_eval_fun contains more than 1 equality '
                                 'symbol...')
            var_name_out = spl[0].strip()
            merge_eval_fun = spl[1].strip()

        elif var_name_out is None:
            var_name_out = merge_eval_fun
            var_name_out = var_name_out.replace('{};'.format(dataset1), '')
            var_name_out = var_name_out.replace('{};'.format(dataset2), '')

    merge_info_vars = {'merge_how' : merge_how}
    if merge_how == 'combine' and var1==var2:
        merge_info_vars['prefer'] = prefer
    elif merge_how == 'eval':
        merge_info_vars['merge_eval_fun'] = merge_eval_fun

    long_coords = list(zip(long['latitude'], long['longitude']))

    merged_stats = []
    _index_used = []
    var, var_other = short['var_name'], long['var_name']
    for i, stat in enumerate(short['stats']):
        statname = stat.station_name
        lat0, lon0 = short['latitude'][i], short['longitude'][i]

        if match_stats_how == 'station_name':
            index_matches = np.where(np.asarray(long['station_name'])==statname)[0]
        else:
            index_matches = find_coord_indices_within_distance(
                latref=lat0,
                lonref=lon0,
                latlons=long_coords,
                radius=match_stats_tol_km)

        if len(index_matches) == 0:
            continue
        elif len(index_matches) > 1 and not match_stats_how=='closest':
            raise NotImplementedError()

        idx_other = index_matches[0]

        # make sure to assign each site only once
        if idx_other in _index_used:
            continue

        _index_used.append(idx_other)

        stat_other = long['stats'][idx_other]

        # prepare output StationData object (will contain colocated timeseries
        # of both input variables as well as, additionally retrieved variable,
        # if applicable)
        new = StationData()

        meta_merged = stat.merge_meta_same_station(stat_other,
                                                   inplace=False)

        for key in new.STANDARD_META_KEYS:
            new[key] = meta_merged[key]

        tt = stat.get_var_ts_type(var)
        tto = stat.get_var_ts_type(var_other)

        to_ts_type = sort_ts_types([tt, tto])[-1]

        df = _colocate_site_data_helper(
            stat, stat_other,
            var, var_other,
            to_ts_type,
            resample_how=resample_how,
            apply_time_resampling_constraints=apply_time_resampling_constraints,
            min_num_obs=min_num_obs,
            use_climatology_ref=False)

        df.dropna(axis=0, how='all', inplace=True)

        # NOTE: the dataframe returned by _colocate_site_data_helper has ref as first
        # column and the first input data as 2nd!
        stat_order = [stat_other, stat]
        col_order = [long['id'], short['id']]
        col_vars = [long['var_name'], short['var_name']]
        col_names = list(df.columns.values)

        # in case input variables are different, keep both of them in the
        # output colocated StationData, in addition to potentially computed
        # additional variables below
        if var != var2:
            for j, colname in enumerate(col_names):
                _var = col_vars[j]
                _stat = stat_order[j]
                ts = df[colname]
                new[_var] = ts
                vi = _stat['var_info'][_var]
                vi['ts_type'] = to_ts_type
                new['var_info'][_var] = vi

        add_ts = None
        # Merge timeseries if variables are the same and are supposed to be
        # combined
        if merge_how=='combine' and var==var2:
            prefer_col = col_names[col_order.index(prefer)]
            dont_prefer = col_names[int(not (col_names.index(prefer_col)))]
            add_ts = df[prefer_col].combine_first(df[dont_prefer])
            var_name_out = var

        elif merge_how == 'mean':
            add_ts = df.mean(axis=1)

        elif merge_how == 'eval':
            func = merge_eval_fun.replace(col_order[0], col_names[0])
            func = func.replace(col_order[1], col_names[1])

            add_ts = df.eval(func)

        if add_ts is not None:

            var_info = {'ts_type' : to_ts_type}
            var_info.update(merge_info_vars)

            new['var_info'][var_name_out] = var_info
            new[var_name_out] = add_ts

        merged_stats.append(new)

    return merged_stats

if __name__=='__main__':
    import pyaerocom as pya
    from numpy import testing as npt
    from pyaerocom.conftest import TEST_PATHS

    testdatadir = (const._TESTDATADIR)
    obs_path = os.path.join(testdatadir, TEST_PATHS['AeronetSunV3L2Subset.daily'])
    obs_ref_path = os.path.join(testdatadir, TEST_PATHS['AeronetSDAV3L2Subset.daily'])

    pya.const.add_ungridded_obs('AeronetSunV3', obs_path, reader=pya.io.ReadAeronetSunV3)
    pya.const.add_ungridded_obs('AeronetSdaV3', obs_ref_path, reader=pya.io.ReadAeronetSdaV3)


    r = pya.io.ReadUngridded('AeronetSunV3')
    r_ref = pya.io.ReadUngridded('AeronetSdaV3')

    sun_aod = r.read(vars_to_retrieve=['od550aer'],
                     common_meta={'ts_type':'daily'})
    sun_ang = r.read(vars_to_retrieve=['ang4487aer'],
                     common_meta={'ts_type':'daily'})


    sda_aods = r_ref.read(vars_to_retrieve=['od550aer', 'od550lt1aer'],
                         common_meta={'ts_type':'daily'})

    # TEST 1 (use "combine with 2 different variables") using "closest" sites
    # for matching site locations
    data = pya.UngriddedData.from_station_data(combine_vardata_ungridded(
        data1=sun_aod, var1='od550aer',
        data2=sun_ang, var2='ang4487aer',
        match_stats_how='closest',
        merge_how='combine'))

    assert len(data.unique_station_names) == 18
    for meta in data.metadata.values():
        assert 'od550aer' in meta['var_info']
        assert 'ang4487aer' in meta['var_info']

    # TEST 2 (use "combine with 2 different variables") using station names
    # for matching site locations
    data = pya.UngriddedData.from_station_data(combine_vardata_ungridded(
        data1=sun_aod, var1='od550aer',
        data2=sun_ang, var2='ang4487aer',
        match_stats_how='station_name',
        merge_how='combine'))

    assert len(data.unique_station_names) == 18
    for meta in data.metadata.values():
        assert 'od550aer' in meta['var_info']
        assert 'ang4487aer' in meta['var_info']

    # TEST 3 (use "combine with the same variables") using station names
    # for matching site locations
    data = pya.UngriddedData.from_station_data(combine_vardata_ungridded(
        data1=sun_aod, var1='od550aer',
        data2=sda_aods, var2='od550aer',
        match_stats_how='station_name',
        merge_how='combine'))

    assert len(data.unique_station_names) == 13
    for meta in data.metadata.values():
        assert 'od550aer' in meta['var_info']
        vi =  meta['var_info']['od550aer']
        assert 'merge_how' in vi
        assert vi['merge_how'] == 'combine'
        assert 'prefer' in vi
        assert vi['prefer'] == 'AeronetSunV3;od550aer'


    # TEST 4 (use "eval to compute od500aer from od550aer and ang4487aer")
    # using "closest" sites for matching site locations
    func = 'od500aer=AeronetSunV3;od550aer*(500/550)**(-AeronetSunV3;ang4487aer)'
    data = pya.UngriddedData.from_station_data(combine_vardata_ungridded(
        data1=sun_aod, var1='od550aer',
        data2=sun_ang, var2='ang4487aer',
        match_stats_how='closest',
        merge_how='eval',
        merge_eval_fun=func))

    assert len(data.unique_station_names) == 18

    test_vals = []
    test_vals_computed = []
    for key, meta in data.metadata.items():
        assert 'od550aer' in meta['var_info']
        assert 'ang4487aer' in meta['var_info']
        assert 'od500aer' in meta['var_info']

        od550aer = data._data[data.meta_idx[key]['od550aer'][0], data._DATAINDEX]
        od500aer = data._data[data.meta_idx[key]['od500aer'][0], data._DATAINDEX]
        ang4487aer = data._data[data.meta_idx[key]['ang4487aer'][0], data._DATAINDEX]

        test_vals.append(od500aer)
        test_vals_computed.append(od550aer * (500/550)**(-ang4487aer))

    npt.assert_allclose(test_vals, test_vals_computed, atol=1e-12)