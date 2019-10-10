#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Methods and / or classes to perform colocation
"""
import numpy as np
import os
import pandas as pd
from pyaerocom import logger
from pyaerocom.exceptions import (ColocationError, 
                                  DataUnitError,
                                  DimensionOrderError,
                                  MetaDataError,
                                  TimeMatchError,
                                  VarNotAvailableError)

from pyaerocom.time_config import TS_TYPE_TO_PANDAS_FREQ
from pyaerocom.helpers import (to_pandas_timestamp, 
                               to_datestring_YYYYMMDD)

from pyaerocom.filter import Filter
from pyaerocom.colocateddata import ColocatedData
        
def colocate_gridded_gridded(gridded_data, gridded_data_ref, ts_type=None,
                             start=None, stop=None, filter_name=None, 
                             regrid_res_deg=None, remove_outliers=True,
                             vert_scheme=None, harmonise_units=True,
                             regrid_scheme='areaweighted', 
                             var_outlier_ranges=None,
                             var_ref_outlier_ranges=None,
                             update_baseyear_gridded=None,
                             apply_time_resampling_constraints=None,
                             min_num_obs=None,
                             colocate_time=False,
                             var_keep_outliers=True,
                             var_ref_keep_outliers=False, 
                             **kwargs):
    """Colocate 2 gridded data objects
    
    Todo
    ----
    - think about vertical dimension (vert_scheme input not used at the moment)
    
    Parameters
    ----------
    gridded_data : GriddedData
        gridded data (e.g. model results)
    gridded_data_ref : GriddedData
        reference dataset that is used to evaluate 
        :attr:`gridded_data` (e.g. gridded observation data)
    ts_type : str
        desired temporal resolution of colocated data (must be valid AeroCom
        ts_type str such as daily, monthly, yearly..)
    start : :obj:`str` or :obj:`datetime64` or similar, optional
        start time for colocation, if None, the start time of the input
        :class:`GriddedData` object is used
    stop : :obj:`str` or :obj:`datetime64` or similar, optional
        stop time for colocation, if None, the stop time of the input
        :class:`GriddedData` object is used
    filter_name : str
        string specifying filter used (cf. :class:`pyaerocom.filter.Filter` for
        details). If None, then it is set to 'WORLD-wMOUNTAINS', which 
        corresponds to no filtering (world with mountains). 
        Use WORLD-noMOUNTAINS to exclude mountain sites.
    regrid_res_deg : :obj:`int`, optional
        regrid resolution in degrees. If specified, the input gridded data 
        objects will be regridded in lon / lat dimension to the input 
        resolution. (BETA feature)
    remove_outliers : bool
        if True, outliers are removed from model and obs data before colocation, 
        else not.
    vert_scheme : str
        string specifying scheme used to reduce the dimensionality in case 
        input grid data contains vertical dimension. Example schemes are 
        `mean, surface, altitude`, for details see 
        :func:`GriddedData.to_time_series`.
    harmonise_units : bool
        if True, units are attempted to be harmonised (note: raises Exception
        if True and units cannot be harmonised).
    regrid_scheme : str
        iris scheme used for regridding (defaults to area weighted regridding)
    var_outlier_ranges : :obj:`dict`, optional
        dictionary specifying outlier ranges for dataset to be analysed
        (e.g. dict(od550aer = [-0.05, 10], ang4487aer=[0,4])). If None, then
        the pyaerocom default outlier ranges are used for the input variable.
        Defaults to None.
    var_ref_outlier_ranges : dict, optional
        like `var_outlier_ranges` but for reference dataset.
    update_baseyear_gridded : int, optional
        optional input that can be set in order to redefine the time dimension
        in the gridded data object to be analysed. E.g., if the data object 
        is a climatology (one year of data) that has set the base year of the
        time dimension to a value other than the specified input start / stop 
        time this may be used to update the time in order to make colocation 
        possible.
    apply_time_resampling_constraints : bool, optional
        if True, then time resampling constraints are applied as provided via 
        :attr:`min_num_obs` or if that one is unspecified, as defined in
        :attr:`pyaerocom.const.OBS_MIN_NUM_RESAMPLE`. If None, than 
        :attr:`pyaerocom.const.OBS_APPLY_TIME_RESAMPLE_CONSTRAINTS` is used
        (which defaults to True !!).
    min_num_obs : int or dict, optional
        minimum number of observations for resampling of time
    colocate_time : bool
        if True and if original time resolution of data is higher than desired
        time resolution (`ts_type`), then both datasets are colocated in time 
        *before* resampling to lower resolution. 
    var_keep_outliers : bool
        if True, then no outliers will be removed from dataset to be analysed, 
        even if `remove_outliers` is True. That is because for model evaluation
        often only outliers are supposed to be removed in the observations but
        not in the model.
    var_ref_keep_outliers : bool
        if True, then no outliers will be removed from the reference dataset, 
        even if `remove_outliers` is True.
    **kwargs
        additional keyword args (not used here, but included such that factory 
        class can handle different methods with different inputs)
    
    Returns
    -------
    ColocatedData
        instance of colocated data
        
    """
    if vert_scheme is not None:
        raise NotImplementedError('Input vert_scheme cannot yet be handled '
                                  'for gridded / gridded colocation...')
    if ts_type is None:
        ts_type = 'monthly'
    
    if var_outlier_ranges is None:
        var_outlier_ranges = {}
    if var_ref_outlier_ranges is None:
        var_ref_outlier_ranges = {}
    if filter_name is None:
        filter_name = 'WORLD-wMOUNTAINS'
    if gridded_data.var_info.has_unit:
        if harmonise_units and not gridded_data.units == gridded_data_ref.units:
            try:
                gridded_data_ref.convert_unit(gridded_data.units)
            except:
                raise DataUnitError('Failed to merge data unit of reference '
                                    'gridded data object ({}) to data unit '
                                    'of gridded data object ({})'
                                    .format(gridded_data.units, 
                                            gridded_data_ref.units))
    var, var_ref = gridded_data.var_name, gridded_data_ref.var_name
    if remove_outliers:
        low, high, low_ref, high_ref = None, None, None, None    
        if var in var_outlier_ranges:
            low, high = var_outlier_ranges[var]
        if var_ref in var_ref_outlier_ranges:
            low_ref, high_ref = var_ref_outlier_ranges[var_ref]
    
    if update_baseyear_gridded is not None:
        # update time dimension in gridded data
        gridded_data.base_year = update_baseyear_gridded
        
    # get start / stop of gridded data as pandas.Timestamp
    grid_start = to_pandas_timestamp(gridded_data.start)
    grid_stop = to_pandas_timestamp(gridded_data.stop)
    
    grid_start_ref = to_pandas_timestamp(gridded_data_ref.start)
    grid_stop_ref = to_pandas_timestamp(gridded_data_ref.stop)
    
    grid_ts_type = gridded_data.ts_type
    
    if start is None:
        start = grid_start
    else:
        start = to_pandas_timestamp(start)    
    if stop is None:
        stop = grid_stop
    else:
        stop = to_pandas_timestamp(stop)
    
    if grid_start_ref > start:
        start = grid_start_ref
    if grid_stop_ref < stop:
        stop = grid_stop_ref
    # check overlap
    if stop < grid_start or start > grid_stop:
        raise TimeMatchError('Input time range {}-{} does not '
                             'overlap with data range: {}-{}'
                             .format(start, stop, grid_start, grid_stop))
    gridded_data = gridded_data.crop(time_range=(start, stop))
    gridded_data_ref = gridded_data_ref.crop(time_range=(start, stop))
    
    if regrid_res_deg is not None:
        
        lons = gridded_data_ref.longitude.points
        lats = gridded_data_ref.latitude.points
        
        lons_new = np.arange(lons.min(), lons.max(), regrid_res_deg)
        lats_new = np.arange(lats.min(), lats.max(), regrid_res_deg) 
        
        gridded_data_ref = gridded_data_ref.interpolate(latitude=lats_new, 
                                                        longitude=lons_new)
        
    
        
    # get both objects in same time resolution
    if not colocate_time:
        gridded_data = gridded_data.resample_time(ts_type)
        gridded_data_ref = gridded_data_ref.resample_time(ts_type)
    
    # guess bounds (for area weighted regridding, which is the default)
    gridded_data._check_lonlat_bounds()
    gridded_data_ref._check_lonlat_bounds()
    
    # perform regridding
    gridded_data = gridded_data.regrid(gridded_data_ref, 
                                       scheme=regrid_scheme)
    
    # perform region extraction (if applicable)
    regfilter = Filter(name=filter_name)
    gridded_data = regfilter(gridded_data)
    gridded_data_ref = regfilter(gridded_data_ref)
    
    if not gridded_data.shape == gridded_data_ref.shape:
        raise ColocationError('Shape mismatch between two colocated data '
                               'arrays, please debug')
    files_ref = [os.path.basename(x) for x in gridded_data_ref.from_files]
    files = [os.path.basename(x) for x in gridded_data.from_files]
    
    
    meta = {'data_source'       :   [gridded_data_ref.data_id,
                                     gridded_data.data_id],
            'var_name'          :   [var_ref, var],
            'ts_type'           :   ts_type,
            'filter_name'       :   filter_name,
            'ts_type_src'       :   [gridded_data_ref.ts_type, grid_ts_type],
            'start_str'         :   to_datestring_YYYYMMDD(start),
            'stop_str'          :   to_datestring_YYYYMMDD(stop),
            'var_units'         :   [str(gridded_data_ref.units),
                                     str(gridded_data.units)],
            'vert_scheme'       :   vert_scheme,
            'data_level'        :   3,
            'revision_ref'      :   gridded_data_ref.data_revision,
            'from_files'        :   files,
            'from_files_ref'    :   files_ref,
            'colocate_time'     :   colocate_time,
            'apply_constraints' :   apply_time_resampling_constraints,
            'min_num_obs'       :   min_num_obs}
    
    meta.update(regfilter.to_dict())
    if remove_outliers:
        if not var_keep_outliers:
            gridded_data.remove_outliers(low, high)
        if not var_ref_keep_outliers:
            gridded_data_ref.remove_outliers(low_ref, high_ref)
            
    data = gridded_data.grid.data
    if isinstance(data, np.ma.core.MaskedArray):
        data = data.filled(np.nan)
    data_ref = gridded_data_ref.grid.data
    if isinstance(data_ref, np.ma.core.MaskedArray):
        data_ref = data_ref.filled(np.nan)
    arr = np.asarray((data_ref,
                      data))
    time = gridded_data.time_stamps().astype('datetime64[ns]')
    lats = gridded_data.latitude.points
    lons = gridded_data.longitude.points
    
    
    # create coordinates of DataArray
    coords = {'data_source' : meta['data_source'],
              'var_name'    : ('data_source', meta['var_name']),
              'var_units'   : ('data_source', meta['var_units']),
              'ts_type_src' : ('data_source', meta['ts_type_src']),
              'time'        : time,
              'latitude'    : lats,
              'longitude'   : lons}
    
    dims = ['data_source', 'time', 'latitude', 'longitude']
    
    data = ColocatedData(data=arr, coords=coords, dims=dims,
                         name=gridded_data.var_name, attrs=meta)
    
    if colocate_time and grid_ts_type != ts_type:
        data = data.resample_time(to_ts_type=ts_type, 
                                  colocate_time=True,
                                  apply_constraints=apply_time_resampling_constraints,
                                  min_num_obs=min_num_obs,
                                  **kwargs)
    return data

def colocate_gridded_ungridded(gridded_data, ungridded_data, ts_type=None, 
                               start=None, stop=None, filter_name=None,
                               regrid_res_deg=None, remove_outliers=True,
                               vert_scheme=None, harmonise_units=True, 
                               var_ref=None, 
                               var_outlier_ranges=None, 
                               var_ref_outlier_ranges=None,
                               update_baseyear_gridded=None,
                               ignore_station_names=None,
                               apply_time_resampling_constraints=None,
                               min_num_obs=None,
                               colocate_time=False,
                               var_keep_outliers=True,
                               var_ref_keep_outliers=False, 
                               **kwargs):
    """Colocate gridded with ungridded data 
    
    Note
    ----
    Uses the variable that is contained in input :class:`GriddedData` object 
    (since these objects only contain a single variable)
    
    Parameters
    ----------
    gridded_data : GriddedData
        gridded data (e.g. model results)
    ungridded_data : UngriddedData
        ungridded data (e.g. observations)
    ts_type : str
        desired temporal resolution of colocated data (must be valid AeroCom
        ts_type str such as daily, monthly, yearly.). The colocation itself is
        done in the highest available resolution and resampling to `ts_type` is
        done afterwards. You may change this behaviour by setting input param
        `resample_first=True` (default is False).
    start : :obj:`str` or :obj:`datetime64` or similar, optional
        start time for colocation, if None, the start time of the input
        :class:`GriddedData` object is used
    stop : :obj:`str` or :obj:`datetime64` or similar, optional
        stop time for colocation, if None, the stop time of the input
        :class:`GriddedData` object is used
    filter_name : str
        string specifying filter used (cf. :class:`pyaerocom.filter.Filter` for
        details). If None, then it is set to 'WORLD-wMOUNTAINS', which 
        corresponds to no filtering (world with mountains). 
        Use WORLD-noMOUNTAINS to exclude mountain sites.
    regrid_res_deg : :obj:`int`, optional
        regrid resolution in degrees. If specified, the input gridded data 
        object will be regridded in lon / lat dimension to the input 
        resolution. (BETA feature)
    remove_outliers : bool
        if True, outliers are removed from model and obs data before colocation, 
        else not.
    vert_scheme : str
        string specifying scheme used to reduce the dimensionality in case 
        input grid data contains vertical dimension. Example schemes are 
        `mean, surface, altitude`, for details see 
        :func:`GriddedData.to_time_series`.
    harmonise_units : bool
        if True, units are attempted to be harmonised (note: raises Exception
        if True and units cannot be harmonised).
    var_ref : :obj:`str`, optional
        variable against which data in :attr:`gridded_data` is supposed to be
        compared. If None, then the same variable is used 
        (i.e. `gridded_data.var_name`).
    var_outlier_ranges : dict, optional
        dictionary specifying outlier ranges for dataset to be analysed
        (e.g. dict(od550aer = [-0.05, 10], ang4487aer=[0,4])). If None, then
        the pyaerocom default outlier ranges are used for the input variable.
        Defaults to None.
    var_ref_outlier_ranges : dict, optional
        like `var_outlier_ranges` but for reference dataset.
    update_baseyear_gridded : int, optional
        optional input that can be set in order to re-define the time dimension
        in the gridded data object to be analysed. E.g., if the data object 
        is a climatology (one year of data) that has set the base year of the
        time dimension to a value other than the specified input start / stop 
        time this may be used to update the time in order to make colocation 
        possible.
    ignore_station_names : str or list, optional
        station name or pattern or list of station names or patterns that should
        be ignored
    apply_time_resampling_constraints : bool, optional
        if True, then time resampling constraints are applied as provided via 
        :attr:`min_num_obs` or if that one is unspecified, as defined in
        :attr:`pyaerocom.const.OBS_MIN_NUM_RESAMPLE`. If None, than 
        :attr:`pyaerocom.const.OBS_APPLY_TIME_RESAMPLE_CONSTRAINTS` is used
        (which defaults to True !!).
    min_num_obs : int or dict, optional
        minimum number of observations for resampling of time
    colocate_time : bool
        if True and if original time resolution of data is higher than desired
        time resolution (`ts_type`), then both datasets are colocated in time 
        *before* resampling to lower resolution. 
    var_keep_outliers : bool
        if True, then no outliers will be removed from dataset to be analysed, 
        even if `remove_outliers` is True. That is because for model evaluation
        often only outliers are supposed to be removed in the observations but
        not in the model.
    var_ref_keep_outliers : bool
        if True, then no outliers will be removed from the reference dataset, 
        even if `remove_outliers` is True.
    **kwargs
        additional keyword args (passed to 
        :func:`UngriddedData.to_station_data_all`)
        
    Returns
    -------
    ColocatedData
        instance of colocated data
        
    Raises
    ------
    VarNotAvailableError
        if grid data variable is not available in ungridded data object
    AttributeError
        if instance of input :class:`UngriddedData` object contains more than
        one dataset
    TimeMatchError
        if gridded data time range does not overlap with input time range
    ColocationError
        if none of the data points in input :class:`UngriddedData` matches 
        the input colocation constraints
    """
    if var_outlier_ranges is None:
        var_outlier_ranges = {}
    if var_ref_outlier_ranges is None:
        var_ref_outlier_ranges = {}
        
    if filter_name is None:
        filter_name = 'WORLD-wMOUNTAINS'
    
    var = gridded_data.var_name
    aerocom_var = gridded_data.var_name_aerocom
    if var_ref is None:
        var_ref = aerocom_var
        
    if remove_outliers:
        low, high, low_ref, high_ref = None, None, None, None    
        if var in var_outlier_ranges:
            low, high = var_outlier_ranges[var]
        if var_ref in var_ref_outlier_ranges:
            low_ref, high_ref = var_ref_outlier_ranges[var_ref]
            
    if not var_ref in ungridded_data.contains_vars:
        raise VarNotAvailableError('Variable {} is not available in ungridded '
                                   'data (which contains {})'
                                   .format(var_ref,
                                           ungridded_data.contains_vars))
    elif len(ungridded_data.contains_datasets) > 1:
        raise AttributeError('Colocation can only be performed with '
                             'ungridded data objects that only contain a '
                             'single dataset. Use method `extract_dataset` of '
                             'UngriddedData object to extract single datasets')
    
    dataset_ref = ungridded_data.contains_datasets[0]
    
    if update_baseyear_gridded is not None:
        # update time dimension in gridded data
        gridded_data.base_year = update_baseyear_gridded
    # get start / stop of gridded data as pandas.Timestamp
    grid_start = to_pandas_timestamp(gridded_data.start)
    grid_stop = to_pandas_timestamp(gridded_data.stop)
    
    grid_ts_type = gridded_data.ts_type
    
    if ts_type is None:
        ts_type = grid_ts_type
    if start is None:
        start = grid_start
    else:
        start = to_pandas_timestamp(start)    
    if stop is None:
        stop = grid_stop
    else:
        stop = to_pandas_timestamp(stop)
    
    if start < grid_start:
        start = grid_start
    if stop > grid_stop:
        stop = grid_stop
    # check overlap
    if stop < grid_start or start > grid_stop:
        raise TimeMatchError('Input time range {}-{} does not '
                             'overlap with data range: {}-{}'
                             .format(start, stop, grid_start, grid_stop))  
    # create instance of Filter class (may, in the future, also include all
    # filter options, e.g. start, stop, variables, only land, only oceans, and
    # may also be linked with other data object, e.g. if data is only supposed
    # to be used if other data object exceeds a certain threshold... but for 
    # now, only region and altitude range)
    regfilter = Filter(name=filter_name)
    
    # apply filter to data
    ungridded_data = regfilter(ungridded_data)

    #crop time
    gridded_data = gridded_data.crop(time_range=(start, stop))
    
    if regrid_res_deg is not None:
        
        lons = gridded_data.longitude.points
        lats = gridded_data.latitude.points
        
        lons_new = np.arange(lons.min(), lons.max(), regrid_res_deg)
        lats_new = np.arange(lats.min(), lats.max(), regrid_res_deg) 
        
        gridded_data = gridded_data.interpolate(latitude=lats_new, 
                                                longitude=lons_new)
    
    ungridded_freq = None # that keeps ungridded data in original resolution
    
    if not colocate_time:
        gridded_data = gridded_data.resample_time(to_ts_type=ts_type)
        ungridded_freq = ts_type # converts ungridded data directly to desired resolution
        
    # ts_type that is used for colocation
    col_ts_type = gridded_data.ts_type
    
    # pandas frequency string that corresponds to col_ts_type
    col_freq = TS_TYPE_TO_PANDAS_FREQ[col_ts_type]
    
    if remove_outliers and not var_ref_keep_outliers:
        ungridded_data.remove_outliers(var_ref, inplace=True,
                                       low=low_ref, 
                                       high=high_ref)
    
    all_stats = ungridded_data.to_station_data_all(
            
            vars_to_convert=var_ref, 
            start=start, 
            stop=stop, 
            freq=ungridded_freq,
            by_station_name=True,
            ignore_index=ignore_station_names,
            apply_constraints=apply_time_resampling_constraints,
            min_num_obs=min_num_obs,
            **kwargs)
    
    obs_stat_data = all_stats['stats']
    ungridded_lons = all_stats['longitude']
    ungridded_lats = all_stats['latitude']
    
    # resampling constraints may have been altered in case input was None, 
    # thus overwrite
    vi = obs_stat_data[0]['var_info'][var_ref]
    if 'apply_constraints' in vi:
        apply_time_resampling_constraints = vi['apply_constraints']
        min_num_obs = vi['min_num_obs']
    
    if len(obs_stat_data) == 0:
        raise VarNotAvailableError('Variable {} is not available in specified '
                                   'time interval ({}-{})'
                                   .format(var_ref, start, stop))
    # make sure the gridded data is in the right dimension
    try:
        gridded_data.check_dimcoords_tseries()
    except DimensionOrderError:
        gridded_data.reorder_dimensions_tseries()
    
    if gridded_data.ndim > 3:
        if vert_scheme is None:
            vert_scheme = 'mean'
        if not vert_scheme in gridded_data.SUPPORTED_VERT_SCHEMES:
            raise ValueError('Vertical scheme {} is not supported'.format(vert_scheme))
            
    grid_stat_data = gridded_data.to_time_series(longitude=ungridded_lons,
                                                 latitude=ungridded_lats,
                                                 vert_scheme=vert_scheme)
    
    # Generate time index of ColocatedData object
    time_idx = pd.DatetimeIndex(start=start, end=stop, freq=col_freq)
    #periods = time_idx.to_period(col_freq)
# =============================================================================
#     if col_freq in PANDAS_RESAMPLE_OFFSETS:
#         offs = np.timedelta64(1, '[{}]'.format(PANDAS_RESAMPLE_OFFSETS[col_freq]))
#         time_idx = time_idx + offs
# =============================================================================
    
    coldata = np.empty((2, len(time_idx), len(obs_stat_data)))
    
    lons = []
    lats = []
    alts = []
    station_names = []
                
    ungridded_unit = None
    ts_type_src_ref = None
    if not harmonise_units:
        gridded_unit = str(gridded_data.units)
    else:
        gridded_unit = None
    
    # loop over all stations and append to colocated data object
    for i, obs_stat in enumerate(obs_stat_data):
        
        if ts_type_src_ref is None:
            ts_type_src_ref = obs_stat['ts_type_src']
        elif obs_stat['ts_type_src'] != ts_type_src_ref:
            spl = ts_type_src_ref.split(';')
            if not obs_stat['ts_type_src'] in spl:
                spl.append(obs_stat['ts_type_src'])
            ts_type_src_ref = ';'.join(spl)
            
        if ungridded_unit is None:
            try:
                ungridded_unit = obs_stat['var_info'][var_ref]['units']
            except KeyError as e: #variable information or unit is not defined
                logger.exception(repr(e))
        try:
            unit = obs_stat['var_info'][var_ref]['units']
        except:
            unit = None
        if not unit == ungridded_unit:
            raise ValueError('Cannot perform colocation. Ungridded data '
                             'object contains different units ({})'.format(var_ref))
        # get observations (Note: the index of the observation time series
        # is already in the specified frequency format, and thus, does not
        # need to be updated, for details (or if errors occur), cf. 
        # UngriddedData.to_station_data, where the conversion happens)
        
        # get model data corresponding to station
        grid_stat = grid_stat_data[i]
        if harmonise_units:
            grid_unit = grid_stat.get_unit(var)
            obs_unit = obs_stat.get_unit(var_ref)
            if not grid_unit == obs_unit:
                grid_stat.convert_unit(var, obs_unit)
            if gridded_unit is None:
                gridded_unit = obs_unit
        
        if remove_outliers and not var_keep_outliers:
            # don't check if harmonise_units is active, because the 
            # remove_outliers method checks units based on AeroCom default 
            # variables, and a variable mapping might be active, i.e. 
            # sometimes models use abs550aer for absorption coefficients 
            # with units [m-1] and not for AAOD (which is the AeroCom default
            # and unitless. Hence, unit check in remove_outliers works only
            # if the variable name (and unit) corresonds to AeroCom default)
            #chk_unit = not harmonise_units 
            grid_stat.remove_outliers(var, low=low, high=high,
                                      check_unit=True)
        
        # get grid and obs timeseries data (that may be sampled in arbitrary
        # time resolution, particularly the obs data)
        grid_ts = grid_stat[var]
        obs_ts = obs_stat[var_ref]
        
        # resample to the colocation frequency
        obs_ts1 = obs_ts.resample(col_freq).mean()
        grid_ts1 = grid_ts.resample(col_freq).mean()
        
        # fill up missing time stamps
        _df = pd.concat([obs_ts1, grid_ts1], axis=1, keys=['o', 'm'])
        
        # assign the unified timeseries data to the colocated data array
        coldata[0, :, i] = _df['o'].values
        coldata[1, :, i] = _df['m'].values
        
        lons.append(obs_stat.longitude)
        lats.append(obs_stat.latitude)
        alts.append(obs_stat.altitude)
        station_names.append(obs_stat.station_name)
    
    try:
        revision = ungridded_data.data_revision[dataset_ref]
    except: 
        try:
            revision = ungridded_data._get_data_revision_helper(dataset_ref)
        except MetaDataError:
            revision = 'MULTIPLE'
        except:
            revision = 'n/a'
            
    files = [os.path.basename(x) for x in gridded_data.from_files]
    
    meta = {'data_source'       :   [dataset_ref,
                                     gridded_data.name],
            'var_name'          :   [var_ref, var],
            'ts_type'           :   col_ts_type,
            'filter_name'       :   filter_name,
            'ts_type_src'       :   [ts_type_src_ref, grid_ts_type],
            'start_str'         :   to_datestring_YYYYMMDD(start),
            'stop_str'          :   to_datestring_YYYYMMDD(stop),
            'var_units'         :   [ungridded_unit,
                                     gridded_unit],
            'vert_scheme'       :   vert_scheme,
            'data_level'        :   3,
            'revision_ref'      :   revision,
            'from_files'        :   files,
            'from_files_ref'    :   None,
            'stations_ignored'  :   ignore_station_names,
            'colocate_time'     :   colocate_time,
            'apply_constraints' :   apply_time_resampling_constraints,
            'min_num_obs'       :   min_num_obs,
            'outliers_removed'  :   remove_outliers}

    
    meta.update(regfilter.to_dict())
    
    # create coordinates of DataArray
    coords = {'data_source' : meta['data_source'],
              'var_name'    : ('data_source', meta['var_name']),
              'var_units'   : ('data_source', meta['var_units']),
              'ts_type_src' : ('data_source', meta['ts_type_src']),
              'time'        : time_idx,
              'station_name': station_names,
              'latitude'    : ('station_name', lats),
              'longitude'   : ('station_name', lons),
              'altitude'    : ('station_name', alts)
              }
    
    dims = ['data_source', 'time', 'station_name']
    data = ColocatedData(data=coldata, coords=coords, dims=dims, name=var,
                         attrs=meta)
    
    if colocate_time and grid_ts_type != ts_type:
        data = data.resample_time(to_ts_type=ts_type, 
                                  colocate_time=True,
                                  apply_constraints=apply_time_resampling_constraints,
                                  min_num_obs=min_num_obs,
                                  **kwargs)
    return data

if __name__=='__main__':
    import pyaerocom as pya
    import matplotlib.pyplot as plt
    plt.close('all')
    
    obsdata = pya.io.ReadGridded('MODIS6.aqua').read_var('od550aer', 
                                start=2010)
    
    
    modeldata = pya.io.ReadGridded('ECMWF_CAMS_REAN').read_var('od550aer')
    coldata = pya.colocation.colocate_gridded_gridded(modeldata, obsdata, 
                                                      ts_type='monthly',
                                                      regrid_res_deg=5,
                                                      remove_outliers=True,
                                                      colocate_time=False)
    
    stats = coldata.calc_statistics()
    
    coldata_alt = pya.colocation.colocate_gridded_gridded(modeldata, obsdata, 
                                                      ts_type='monthly',
                                                      regrid_res_deg=5,
                                                      remove_outliers=True,
                                                      colocate_time=True)
    
    stats_alt = coldata_alt.calc_statistics()