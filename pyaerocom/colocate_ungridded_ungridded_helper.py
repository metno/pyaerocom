
import numpy as np

from pyaerocom import const
from pyaerocom._lowlevel_helpers import invalid_input_err_str
from pyaerocom.geodesy import find_coord_indices_within_distance
from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.helpers import sort_ts_types
from pyaerocom.colocation import _colocate_site_data_helper
import os

from pyaerocom.conftest import TEST_PATHS

def combine_vardata_ungridded(data, var, data_ref=None, var_ref=None,
                              match_stats_how='closest',
                              match_stats_tol_km=1,
                              merge_how='eval',
                              merge_eval_fun=None,
                              var_name_out=None,
                              resample_how='mean',
                              apply_time_resampling_constraints=False,
                              min_num_obs=None):
    if data_ref is None:
        data_ref = data
    if var_ref is None:
        var_ref = var
    if data_ref is data and var_ref==var:
        raise ValueError('nothing to combine...')

    if len(data.contains_datasets) > 1:
        raise NotImplementedError
    elif len(data_ref.contains_datasets) > 1:
        raise NotImplementedError

    dataset = data.contains_datasets[0]
    dataset_ref = data_ref.contains_datasets[0]

    idobs='{};{}'.format(dataset, var)
    idref='{};{}'.format(dataset_ref, var_ref)

    data_stats = data.to_station_data_all(var)#, start=start, stop=stop)
    data_stats['var_name'] = var
    data_stats['id'] = idobs
    data_ref_stats = data_ref.to_station_data_all(var_ref)#, start=start, stop=stop)
    data_ref_stats['var_name'] = var_ref
    data_ref_stats['id'] = idref


    if len(data_stats['latitude']) <= len(data_ref_stats['latitude']): #
        short = data_stats
        long = data_ref_stats
    else:
        short = data_ref_stats
        long = data_stats

    match_stats_opts = ['station_name', 'closest']


    if not match_stats_how in match_stats_opts:
        raise ValueError('Invalid input for match_stats_how {}, choose from {}'
                         .format(match_stats_how, match_stats_opts))

    merge_how_opts = ['combine', 'mean', 'eval']

    # if e.g. merge_how is combine and var==var_ref, then the preferred
    # dataset & variable can be provided via this instance
    prefer = idobs

    if not merge_how in merge_how_opts:
        raise ValueError(invalid_input_err_str(
            'merge_how', merge_how, merge_how_opts))

    elif merge_how == 'eval':
        if merge_eval_fun is None:
            raise ValueError('Please specify evaluation function for mode eval')
        elif not all([x in merge_eval_fun for x in [idobs, idref]]):
            raise ValueError('merge_eval_fun needs to include both input '
                             'datasets;variables (e.g. {} + {}'
                             .format(idobs, idref))
        if '=' in merge_eval_fun:
            spl = merge_eval_fun.split('=')
            if len(spl) > 2:
                raise ValueError('merge_eval_fun contains more than 1 equality '
                                 'symbol...')
            var_name_out = spl[0].strip()
            merge_eval_fun = spl[1].strip()

        elif var_name_out is None:
            var_name_out = merge_eval_fun
            var_name_out = var_name_out.replace('{};'.format(dataset), '')
            var_name_out = var_name_out.replace('{};'.format(dataset_ref), '')

    merge_info_vars = {'merge_how' : merge_how}
    if merge_how == 'combine' and var==var_ref:
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
        if var != var_ref:
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
        if merge_how=='combine' and var==var_ref:
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

    data = UngriddedData.from_station_data(merged_stats)
    return data

if __name__=='__main__':
    import pyaerocom as pya
    from numpy import testing as npt
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
    data = combine_vardata_ungridded(data=sun_aod, var='od550aer',
                                     data_ref=sun_ang, var_ref='ang4487aer',
                                     match_stats_how='closest',
                                     merge_how='combine')

    assert len(data.unique_station_names) == 18
    for meta in data.metadata.values():
        assert 'od550aer' in meta['var_info']
        assert 'ang4487aer' in meta['var_info']

    # TEST 2 (use "combine with 2 different variables") using station names
    # for matching site locations
    data = combine_vardata_ungridded(data=sun_aod, var='od550aer',
                                     data_ref=sun_ang, var_ref='ang4487aer',
                                     match_stats_how='station_name',
                                     merge_how='combine')

    assert len(data.unique_station_names) == 18
    for meta in data.metadata.values():
        assert 'od550aer' in meta['var_info']
        assert 'ang4487aer' in meta['var_info']

    # TEST 3 (use "combine with the same variables") using station names
    # for matching site locations
    data = combine_vardata_ungridded(data=sun_aod, var='od550aer',
                                     data_ref=sda_aods, var_ref='od550aer',
                                     match_stats_how='station_name',
                                     merge_how='combine')

    stats_common = np.intersect1d(sun_aod.unique_station_names,
                                  sda_aods.unique_station_names)

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
    data = combine_vardata_ungridded(data=sun_aod, var='od550aer',
                                     data_ref=sun_ang, var_ref='ang4487aer',
                                     match_stats_how='closest',
                                     merge_how='eval',
                                     merge_eval_fun=func)

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



