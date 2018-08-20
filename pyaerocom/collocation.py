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
                               TS_TYPE_TO_NUMPY_FREQ)
from pyaerocom.filter import Filter
from pyaerocom.collocateddata import CollocatedData

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
    freq_np = TS_TYPE_TO_NUMPY_FREQ[ts_type]
    
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
    np_conv = 'datetime64[{}]'.format(freq_np)

    for i, obs_data in enumerate(obs_stat_data):
        if obs_data is not None:
            # get model data corresponding to station
            grid_tseries = grid_stat_data[i][var]
            if sum(grid_tseries.isnull()) > 0:
                raise Exception('DEVELOPER: PLEASE DEBUG AND FIND SOLUTION')
                
            # make sure, time index is defined in the right way (i.e.
            # according to TIME_INDEX, e.g. if ts_type='monthly', it should
            # not be the mid or end of month)
            grid_tseries.index = grid_tseries.index.values.astype(np_conv)
            
            # get observations (Note: the index of the observation time series
            # is already in the specified frequency format, and thus, does not
            # need to be updated, for details (or if errors occur), cf. 
            # UngriddedData.to_station_data, where the conversion happens)
            obs_tseries = obs_data[var]
            
            # the following command takes care of filling up with NaNs where
            # data is missing
            df = pd.DataFrame({'ungridded' : obs_tseries, 
                               'gridded'   : grid_tseries}, index=TIME_IDX)
            grid_vals_temp = df['gridded'].values
            # TODO: remove this later, or include solution in case this exception
            # is raised (i.e. if model data is incomplete on the defined time
            # grid). 
            if sum(np.isnan(grid_vals_temp)) > 0:
                raise Exception
            obs_vals.append(df['ungridded'].values)
            grid_vals.append(grid_vals_temp)
            
            lons.append(obs_data.longitude)
            lats.append(obs_data.latitude)
            alts.append(obs_data.altitude)
            station_names.append(obs_data.station_name)
    
    if len(obs_vals) == 0:
        raise CollocationError('No observations could be found that match '
                               'the collocation constraints')
        
    meta = {'dataset_name'  :   ungridded_data.contains_datasets[0],
            'grid_data_name':   gridded_data.name,
            'var_name'      :   var,
            'ts_type'       :   ts_type,
            'start'         :   start,
            'stop'          :   stop,
            'filter_name'   :   filter_name}

    
    meta.update(regfilter.to_dict())
    
    grid_vals = np.asarray(grid_vals)
    obs_vals = np.asarray(obs_vals)
    
    stat_dim, time_dim = grid_vals.shape
    arr = np.array((obs_vals, grid_vals))
    arr = np.swapaxes(arr, 1, 2)
    #.reshape((2, time_dim, stat_dim))
    
    # create coordinates of DataArray
    coords = {'data_source' : [meta['dataset_name'], 
                               meta['grid_data_name']],
              'time'        : TIME_IDX,
              'station_name': station_names,
              'longitude'   : ('station_name', lons),
              'latitude'    : ('station_name', lats),
              'altitude'    : ('station_name', alts)
              }
    dims = ['data_source', 'time', 'station_name']
    data = CollocatedData(data=arr, coords=coords, dims=dims, name=var,
                          attrs=meta)
    
    return data