
import numpy as np

from pyaerocom.obs_io import ObsVarCombi
from pyaerocom._lowlevel_helpers import invalid_input_err_str
from pyaerocom.geodesy import find_coord_indices_within_distance
from pyaerocom.stationdata import StationData
from pyaerocom.helpers import sort_ts_types
from pyaerocom.colocation import _colocate_site_data_helper
import os

def _check_input_data_ids_and_vars(data_ids_and_vars):
    if not isinstance(data_ids_and_vars, (list, tuple)):
        raise ValueError('Input data_ids_and_vars must be tuple or list')
    elif len(data_ids_and_vars) != 2:
        raise NotImplementedError('Currently, only (and exactly) 2 datasets '
                                  'can be combined...')
    for item in data_ids_and_vars:
        if not isinstance(item, (list, tuple)):
            raise ValueError('Each entry in data_ids_and_vars must be tuple or list')
        elif len(item) != 3:
            raise ValueError(
                'Each entry in data_ids_and_vars needs to contain exactly 3 '
                'items.')
        if not isinstance(item[1], str) or not isinstance(item[2], str):
            raise ValueError('2nd and 3rd entries (data_id, var_name) in item '
                             'need to be str')

def _map_same_stations(stats_short, stats_long, match_stats_how,
                       match_stats_tol_km):

    long_coords = list(zip(stats_long['latitude'], stats_long['longitude']))

    # index matches and corresponding station name matches
    _index_short = []
    _index_long = []
    _statnames_short = []
    _statnames_long = []

    long_sitenames = np.asarray(stats_long['station_name'])

    for i, stat in enumerate(stats_short['stats']):
        statname = stat.station_name
        lat0, lon0 = stats_short['latitude'][i], stats_short['longitude'][i]

        if match_stats_how == 'station_name':
            # np.where returns tuple, first index contains array with index
            # matches
            index_matches = np.where(long_sitenames==statname)[0]
        else:
            index_matches = find_coord_indices_within_distance(
                latref=lat0,
                lonref=lon0,
                latlons=long_coords,
                radius=match_stats_tol_km)

        # init which default index to use
        use_index = 0
        if len(index_matches) == 0:
            continue
        elif len(index_matches) > 1:
            if match_stats_how=='station_name':
                raise Exception('Unexpected error: each station_name should '
                                'only occur once... (perhaps due to unforeseen '
                                'API change sometime in the future)')
            else:
                # more than one site was found in the surroundings of the
                # current coordinate. Check and prefer same site name if
                # possible, else, use closest
                for j, idx_match in enumerate(index_matches):
                    if statname == stats_long['station_name'][idx_match]:
                        use_index = j
                        break

        idx_long = index_matches[use_index]

        # make sure to colocate each site only once
        if idx_long in _index_long:
            statname_long = stats_long['station_name'][idx_long]
            if statname == statname_long:
                # rare case: the index match in long has already been assigned
                # to another site in short which does not occur in long
                # (e.g. AAOT site and Venise site in AERONET). In this case
                # we want to use the one that matches the site name, so we
                # have to remove the already registered index from the record
                rm_idx = _statnames_long.index(statname_long)
                _index_short.pop(rm_idx)
                _index_long.pop(rm_idx)
                _statnames_long.pop(rm_idx)
                _statnames_short.pop(rm_idx)
            else:
                continue

        _index_short.append(i)
        _index_long.append(idx_long)
        _statnames_short.append(statname)
        _statnames_long.append(stats_long['station_name'][idx_long])

    return (_index_short, _index_long, _statnames_short, _statnames_long)

def _combine_2_sites(stat, var, stat_other, var_other,
                     merge_how, merge_eval_fun,
                     match_stats_tol_km, var_name_out,
                     data_id_out, var_unit_out,
                     resample_how,
                     apply_time_resampling_constraints,
                     min_num_obs, prefer, merge_info_vars,
                     add_meta_keys):
    """Combine two StationData objects for a given merge strategy

    Private for now...  details should follow. Until then see
    :func:`combine_vardata_ungridded` for details on input args

    Returns
    -------
    StationData
        merged StationData instance
    """
    # unit of first variable
    var_unit_in = stat.get_unit(var)

    # check if output unit is defined explicitly and if not, use unit of
    # variable 1
    if var_unit_out is None:
        var_unit_out = var_unit_in
    # make sure both input data objects are in the correct unit (which is
    # var_unit_out)
    elif not var_unit_in == var_unit_out:
        stat.convert_unit(var, var_unit_out)

    if not stat_other.get_unit(var_other) == var_unit_out:
        stat_other.convert_unit(var_other, var_unit_out)

    new = StationData()
    # add default metadata to new data object
    meta_first = stat.get_meta(force_single_value=False,
                               quality_check=False,
                               add_meta_keys=add_meta_keys)
    new.update(meta_first)

    new.merge_meta_same_station(
        other=stat_other,
        check_coords=False, #has already been done
        inplace=True,
        raise_on_error=True,
        add_meta_keys=add_meta_keys)

    tstype = stat.get_var_ts_type(var)
    tstype_other = stat_other.get_var_ts_type(var_other)

    to_ts_type = sort_ts_types([tstype, tstype_other])[-1]

    df = _colocate_site_data_helper(
        stat, stat_other,
        var, var_other,
        to_ts_type,
        resample_how=resample_how,
        apply_time_resampling_constraints=apply_time_resampling_constraints,
        min_num_obs=min_num_obs,
        use_climatology_ref=False)

    # remove timestamps where both observations are NaN
    df.dropna(axis=0, how='all', inplace=True)

    # NOTE: the dataframe returned by _colocate_site_data_helper has ref as first
    # column and the first input data as 2nd!
    obsvar_id = str(ObsVarCombi(stat.data_id, var))
    obsvar_id_other = str(ObsVarCombi(stat_other.data_id, var_other))

    stat_order = [stat_other, stat]
    col_order = [obsvar_id_other, obsvar_id]
    col_vars = [var_other, var]
    col_names = list(df.columns.values)

    # In case input variables are different, keep both of them in the
    # output colocated StationData, in addition to potentially computed
    # additional variables below. This is equivalent with using
    # merge_how='combine' and var1 != var2
    if var != var_other:
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
    if merge_how=='combine' and var==var_other:
        prefer_col = col_names[col_order.index(prefer)]
        dont_prefer = col_names[int(not (col_names.index(prefer_col)))]
        add_ts = df[prefer_col].combine_first(df[dont_prefer])

        if var_name_out is None:
            var_name_out = var

    elif merge_how == 'mean':
        if var != var_other:
            raise NotImplementedError('Averaging of site data is only '
                                      'supported if input variables are the '
                                      'same...')
        # if it made it until here, then both sites have same variables and
        # units
        if var_name_out is None:
            var_name_out = var

        add_ts = df.mean(axis=1)

    elif merge_how == 'eval':

        func = merge_eval_fun.replace(col_order[0], col_names[0])
        func = func.replace(col_order[1], col_names[1])
        if '=' in merge_eval_fun:
            # make sure variable name is not in merge_eval_fun anymore, otherwise
            # the eval method will return a DataFrame instead of a Series
            func = func.split('=')[-1].strip()
        add_ts = df.eval(func)

        if var_name_out is None:
            var_name_out = merge_eval_fun
            var_name_out = var_name_out.replace('{};'.format(stat.data_id), '')
            var_name_out = var_name_out.replace('{};'.format(stat_other.data_id), '')

    if add_ts is not None:

        var_info = {'ts_type'   : to_ts_type,
                    'units'     : var_unit_out}

        var_info.update(merge_info_vars)

        new['var_info'][var_name_out] = var_info
        new[var_name_out] = add_ts

    if isinstance(data_id_out, str):
        new['data_id'] = data_id_out

    return new

def combine_vardata_ungridded(data_ids_and_vars,
                              match_stats_how='closest',
                              match_stats_tol_km=1,
                              merge_how='combine',
                              merge_eval_fun=None,
                              var_name_out=None,
                              data_id_out=None,
                              var_unit_out=None,
                              resample_how='mean',
                              apply_time_resampling_constraints=False,
                              min_num_obs=None,
                              add_meta_keys=None):
    """
    Combine and colocate different variables from UngriddedData

    This method allows to combine different variable timeseries from different
    ungridded observation records in multiple ways. The source data may be all
    included in a single instance of `UngriddedData` or in multiple, for
    details see first input parameter :param:`data_ids_and_vars`. Merging can
    be done in flexible ways, e.g. by combining measurements of the same
    variable from 2 different datasets or by computing new variables based
    on 2 measured variables (e.g. concox=concno2+conco3). Doing this requires
    colocation of site locations and timestamps of both input observation
    records, which is done in this method.

    It comprises 2 major steps:

        1. Compute list of :class:`StationData` objects for both input \
            data combinations (data_id1 & var1; data_id2 & var2) and based \
            on these, find the coincident locations. Finding coincident \
            sites can either be done based on site location name or based on
            their lat/lon locations. The method to use can be specified via
            input arg :param:`match_stats_how`.
        2. For all coincident locations, a new instance of :class:`StationData` \
            is computed that has merged the 2 timeseries in the way
            that can be specified through input args :param:`merge_how` and
            :param:`merge_eval_fun`. If the 2 original timeseries from both
            sites come in different temporal resolutions, they will be
            resampled to the lower of both resolutions. Resampling constraints
            that are supposed to be applied in that case can be provided via
            the respective input args for temporal resampling. Default is
            pyaerocom default, which corresponds to ~25% coverage constraint
            (as of 22.10.2020) for major resolution steps, such as
            daily->monthly.

    Note
    ----
    Currently, only 2 variables can be combined to a new one (e.g.
    concox=conco3+concno2).

    Note
    ----
    Be aware of unit conversion issues that may arise if your input data is
    not in AeroCom default units. For details see below.

    Parameters
    ----------
    data_ids_and_vars : list
        list of 3 element tuples, each containing, in the following order
        1. instance of :class:`UngriddedData`; 2. dataset ID (remember that
        UngriddedData can contain more than one dataset); and 3. variable name.
        Note that currently only 2 of such tuples can be combined.
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
        relevant if `merge_how='eval'` is used) . The default is None. E.g. if
        one wants to retrieve the column aerosol fine mode fraction at 550nm
        (fmf550aer) through AERONET, this could be done through the SDA product
        by prodiding data_id1 and var1 are 'AeronetSDA' and 'od550aer' and
        second input data_id2 and var2 are 'AeronetSDA' and 'od550lt1aer' and
        merge_eval_fun could then be
        'fmf550aer=(AeronetSDA;od550lt1aer/AeronetSDA;od550aer)*100'. Note that
        the input variables will be converted to their AeroCom default units,
        so the specification of `merge_eval_fun` should take that into account
        in case the originally read obsdata is not in default units.
    var_name_out : str, optional
        Name of output variable. Default is None, in which case it is attempted
        to be inferred.
    data_id_out : str, optional
        `data_id` set in output `StationData` objects. Default is None, in
        which case it is inferred from input data_ids (e.g. in above example
        of merge_eval_fun, the output data_id would be 'AeronetSDA' since both
        input IDs are the same.
    var_unit_out : str
        unit of output variable.
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
    add_meta_keys : list, optional
        additional metadata keys to be added to output `StationData` objects
        from input data. If None, then only the pyaerocom default keys are
        added (see `StationData.STANDARD_META_KEYS`).

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
    if add_meta_keys is None:
        add_meta_keys=[]
    _check_input_data_ids_and_vars(data_ids_and_vars)
    data1, data_id1, var1 = data_ids_and_vars[0]
    data2, data_id2, var2 = data_ids_and_vars[1]

    if data2 is data1 and var2 == var1 and data_id1==data_id2:
        raise ValueError('nothing to combine...')

    if not data_id1 in data1.contains_datasets:
        raise ValueError('No such data ID {} in {}'.format(data_id1, data1))
    elif len(data1.contains_datasets) > 1:
        data1 = data1.extract_dataset(data_id1)

    if not data_id2 in data2.contains_datasets:
        raise ValueError('No such data ID {} in {}'.format(data_id2, data2))
    elif len(data2.contains_datasets) > 1:
        data2 = data2.extract_dataset(data_id2)

    id1 = str(ObsVarCombi(data_id1, var1))
    id2 = str(ObsVarCombi(data_id2, var2))

    data1_stats = data1.to_station_data_all(var1,
                                            add_meta_keys=add_meta_keys)
    data1_stats['var_name'] = var1
    data1_stats['id'] = id1

    data2_stats = data2.to_station_data_all(var2,
                                            add_meta_keys=add_meta_keys)
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
            var_name_out = var_name_out.replace('{};'.format(data_id1), '')
            var_name_out = var_name_out.replace('{};'.format(data_id2), '')

    merge_info_vars = {'merge_how' : merge_how}
    if merge_how == 'combine' and var1==var2:
        merge_info_vars['prefer'] = prefer
    elif merge_how == 'eval':
        merge_info_vars['merge_eval_fun'] = merge_eval_fun

    (_index_short,
     _index_long,
     _statnames_short,
     _statnames_long)=_map_same_stations(short, long, match_stats_how,
                                         match_stats_tol_km)


    merged_stats = []

    var_short, var_long = short['var_name'], long['var_name']
    for idx_short, idx_long in zip(_index_short, _index_long):

        stat_short = short['stats'][idx_short]
        stat_short.check_var_unit_aerocom(var_short)
        stat_long = long['stats'][idx_long]
        stat_long.check_var_unit_aerocom(var_long)

        # prepare output StationData object (will contain colocated timeseries
        # of both input variables as well as, additionally retrieved variable,
        # if applicable)
        new = _combine_2_sites(stat_short, var_short, stat_long, var_long,
                              merge_how, merge_eval_fun,
                              match_stats_tol_km, var_name_out,
                              data_id_out, var_unit_out, resample_how,
                              apply_time_resampling_constraints,
                              min_num_obs, prefer, merge_info_vars,
                              add_meta_keys)

        merged_stats.append(new)

    return merged_stats

if __name__=='__main__':
    import pyaerocom as pya

    OBS_LOCAL = '/home/jonasg/MyPyaerocom/data/obsdata/'

    GHOST_DIR = os.path.join(OBS_LOCAL, 'GHOST/data/EEA_AQ_eReporting/daily')

    filter_post = {'altitude' : [1500, 1700]}
    # Tests based on whole datasets
    vmro3 = pya.io.ReadUngridded('GHOST.EEA.daily',
                                 data_dir=GHOST_DIR).read(vars_to_retrieve='vmro3',
                                                          filter_post=filter_post)

                                                          # Tests based on whole datasets
    vmrno2 = pya.io.ReadUngridded('GHOST.EEA.daily',
                                  data_dir=GHOST_DIR).read(vars_to_retrieve='vmrno2',
                                                           filter_post=filter_post)



    input_data = [
        (vmro3, 'GHOST.EEA.daily', 'vmro3'),
        (vmrno2, 'GHOST.EEA.daily', 'vmrno2')
    ]

    meta_keys = list(vmro3.metadata[0].keys())
    fun = 'GHOST.EEA.daily;vmro3+GHOST.EEA.daily;vmrno2'
    stats_merged = combine_vardata_ungridded(input_data,
                                             merge_eval_fun=fun,
                                             var_unit_out='ppt',
                                             var_name_out='vmrox',
                                             merge_how='eval',
                                             add_meta_keys=meta_keys)
