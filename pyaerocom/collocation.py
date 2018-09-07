#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Methods and / or classes to perform collocation
"""
import pandas as pd
import numpy as np
from pyaerocom.exceptions import (VarNotAvailableError, TimeMatchError,
                                  CollocationError)
from pyaerocom.helpers import (to_pandas_timestamp, 
                               TS_TYPE_TO_PANDAS_FREQ,
                               to_datestring_YYYYMMDD)
from pyaerocom.filter import Filter
from pyaerocom.collocateddata import CollocatedData

def collocate_gridded_gridded(gridded_data, gridded_data_ref, ts_type='yearly',
                              start=None, stop=None, 
                              filter_name='WORLD-wMOUNTAINS', **regrid_opts):
    """Collocate 2 gridded data objects
    
    Todo
    ----
    Complete docstring
    """
    # get start / stop of gridded data as pandas.Timestamp
    grid_start = to_pandas_timestamp(gridded_data.start_time)
    grid_stop = to_pandas_timestamp(gridded_data.stop_time)
    
    grid_ts_type = gridded_data.ts_type
    
    if start is None:
        start = grid_start
    else:
        start = to_pandas_timestamp(start)    
    if stop is None:
        stop = grid_stop
    else:
        stop = to_pandas_timestamp(stop)
    
    # check overlap
    if stop < grid_start or start >  grid_stop:
        raise TimeMatchError('Input time range {}-{} does not '
                             'overlap with data range: {}-{}'
                             .format(start, stop, grid_start, grid_stop))
    gridded_data = gridded_data.crop(time_range=(start, stop))
    gridded_data_ref = gridded_data_ref.crop(time_range=(start, stop))
    
    # get both objects in same time resolution
    gridded_data = gridded_data.downscale_time(ts_type)
    gridded_data_ref = gridded_data_ref.downscale_time(ts_type)
    
    # guess bounds (for area weighted regridding, which is the default)
    gridded_data._check_lonlat_bounds()
    gridded_data_ref._check_lonlat_bounds()
    
    # perform regridding
    gridded_data = gridded_data.regrid(gridded_data_ref, **regrid_opts)
    
    # perform region extraction (if applicable)
    regfilter = Filter(name=filter_name)
    gridded_data = regfilter(gridded_data)
    gridded_data_ref = regfilter(gridded_data_ref)
    
    if not gridded_data.shape == gridded_data_ref.shape:
        raise CollocationError('Shape mismatch between two collocated data '
                               'arrays, please debug')
    
    meta = {'data_source'       :   [gridded_data_ref.name,
                                    gridded_data.name],
            'var_name'          :   gridded_data.var_name,
            'ts_type'           :   ts_type,
            'filter_name'       :   filter_name,
            'ts_type_src'       :   grid_ts_type,
            'start_str'         :   to_datestring_YYYYMMDD(start),
            'stop_str'          :   to_datestring_YYYYMMDD(stop),
            'data_level'        :   'collocated'}

    
    meta.update(regfilter.to_dict())
    data_ref = gridded_data_ref.grid.data
    if isinstance(data_ref, np.ma.core.MaskedArray):
        data_ref = data_ref.filled(np.nan)

    arr = np.asarray((data_ref,
                      gridded_data.grid.data))
    time = gridded_data.time_stamps().astype('datetime64[ns]')
    # create coordinates of DataArray
    coords = {'data_source' : meta['data_source'],
              'time'        : time,
              'longitude'   : gridded_data.longitude.points,
              'latitude'    : gridded_data.latitude.points
              }
    dims = ['data_source', 'time', 'latitude', 'longitude']
    try:
        return CollocatedData(data=arr, coords=coords, dims=dims, 
                          name=gridded_data.var_name, attrs=meta)
    except:
        return arr, coords, dims

def collocate_gridded_ungridded_2D(gridded_data, ungridded_data, ts_type='daily', 
                                   start=None, stop=None, 
                                   filter_name='WORLD-wMOUNTAINS'):
    """Collocate gridded with ungridded data of 2D data 
    
    2D means, that the vertical direction is only sampled at one altitude or
    the variable is of integrated nature (or averaged) so that the dimensionality
    of the data is reduced to lon lat and time
    
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
    var_name : str
        variable to be collocated
    ts_type : str
        desired temporal resolution of collocated data (must be valid AeroCom
        ts_type str such as daily, monthly, yearly..)
    start : :obj:`str` or :obj:`datetime64` or similar, optional
        start time for collocation, if None, the start time of the input 
        :class:`GriddedData` object is used
    stop : :obj:`str` or :obj:`datetime64` or similar, optional
        stop time for collocation, if None, the stop time of the input 
        :class:`GriddedData` object is used
    filter_name : str
        string specifying filter used (cf. :class:`pyaerocom.filter.Filter` for
        details). Default is 'WORLD-wMOUNTAINS', which corresponds to no 
        filtering (world with mountains). Use WORLD-noMOUNTAINS to exclude
        stations at altitudes exceeding 1000 m.
        
    Returns
    -------
    CollocatedData
        instance of collocated data
        
    Raises
    ------
    VarNotAvailableError
        if grid data variable is not available in ungridded data object
    AttributeError
        if instance of input :class:`UngriddedData` object contains more than
        one dataset
    TimeMatchError
        if gridded data time range does not overlap with input time range
    CollocationError
        if none of the data points in input :class:`UngriddedData` matches 
        the input collocation constraints
    """
    var = gridded_data.var_name
    if not var in ungridded_data.contains_vars:
        raise VarNotAvailableError('Variable {} is not '
            'available in ungridded data (which contains {})'.format(var,
                                         ungridded_data.contains_vars))
    elif len(ungridded_data.contains_datasets) > 1:
        raise AttributeError('Collocation can only be performed with '
                             'ungridded data objects that only contain a '
                             'single dataset. Use method `extract_dataset` of '
                             'UngriddedData object to extract single datasets')
        
    # get start / stop of gridded data as pandas.Timestamp
    grid_start = to_pandas_timestamp(gridded_data.start_time)
    grid_stop = to_pandas_timestamp(gridded_data.stop_time)
    
    grid_ts_type = gridded_data.ts_type
    
    if start is None:
        start = grid_start
    else:
        start = to_pandas_timestamp(start)    
    if stop is None:
        stop = grid_stop
    else:
        stop = to_pandas_timestamp(stop)
    
    # check overlap
    if stop < grid_start or start >  grid_stop:
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
    
    ungridded_lons = ungridded_data.longitude
    ungridded_lats = ungridded_data.latitude               

    #crop time
    gridded_data = gridded_data.crop(time_range=(start, stop))
    
    # downscale time (if applicable)
    grid_data = gridded_data.downscale_time(to_ts_type=ts_type)
    
    # conver
    grid_stat_data = grid_data.to_time_series(longitude=ungridded_lons,
                                              latitude=ungridded_lats)

    # pandas frequency string for TS type
    freq_pd = TS_TYPE_TO_PANDAS_FREQ[ts_type]
    
    obs_stat_data = ungridded_data.to_station_data_all(vars_to_convert=var, 
                                                       start=start, 
                                                       stop=stop, 
                                                       freq=freq_pd, 
                                                       interp_nans=False)
    
    obs_vals = []
    grid_vals = []
    lons = []
    lats = []
    alts = []
    station_names = []
    
    # TIME INDEX ARRAY FOR COLLOCATED DATA OBJECT
    TIME_IDX = pd.DatetimeIndex(freq=freq_pd, start=start, end=stop)

    for i, obs_data in enumerate(obs_stat_data):
        if obs_data is not None:
            # get observations (Note: the index of the observation time series
            # is already in the specified frequency format, and thus, does not
            # need to be updated, for details (or if errors occur), cf. 
            # UngriddedData.to_station_data, where the conversion happens)
            obs_tseries = obs_data[var]
            # get model data corresponding to station
            grid_tseries = grid_stat_data[i][var]
            if sum(grid_tseries.isnull()) > 0:
                raise Exception('DEVELOPER: PLEASE DEBUG AND FIND SOLUTION')
            elif not len(grid_tseries) == len(TIME_IDX):
                raise Exception('DEVELOPER: PLEASE DEBUG AND FIND SOLUTION')
            # make sure, time index is defined in the right way (i.e.
            # according to TIME_INDEX, e.g. if ts_type='monthly', it should
            # not be the mid or end of month)
            grid_tseries = pd.Series(grid_tseries.values, 
                                     index=TIME_IDX)
            
            # the following command takes care of filling up with NaNs where
            # data is missing
            df = pd.DataFrame({'ungridded' : obs_tseries, 
                               'gridded'   : grid_tseries}, 
                              index=TIME_IDX)
            
            grid_vals_temp = df['gridded'].values

            obs_vals.append(df['ungridded'].values)
            grid_vals.append(grid_vals_temp)
            
            lons.append(obs_data.longitude)
            lats.append(obs_data.latitude)
            alts.append(obs_data.altitude)
            station_names.append(obs_data.station_name)
    
    if len(obs_vals) == 0:
        raise CollocationError('No observations could be found that match '
                               'the collocation constraints')
        
    meta = {'data_source'  :   [ungridded_data.contains_datasets[0],
                                    gridded_data.name],
            'var_name'      :   var,
            'ts_type'       :   ts_type,
            'filter_name'   :   filter_name,
            'ts_type_src'   :   grid_ts_type,
            'start_str'     :   to_datestring_YYYYMMDD(start),
            'stop_str'      :   to_datestring_YYYYMMDD(stop),
            'data_level'    :   'collocated'}

    
    meta.update(regfilter.to_dict())
    
    grid_vals = np.asarray(grid_vals)
    obs_vals = np.asarray(obs_vals)
    
    stat_dim, time_dim = grid_vals.shape
    arr = np.array((obs_vals, grid_vals))
    arr = np.swapaxes(arr, 1, 2)
    #.reshape((2, time_dim, stat_dim))
    
    # create coordinates of DataArray
    coords = {'data_source' : meta['data_source'],
              'time'        : TIME_IDX,
              'station_name': station_names,
              'latitude'    : ('station_name', lats),
              'longitude'   : ('station_name', lons),
              'altitude'    : ('station_name', alts)
              }
    dims = ['data_source', 'time', 'station_name']
    data = CollocatedData(data=arr, coords=coords, dims=dims, name=var,
                          attrs=meta)
    
    return data