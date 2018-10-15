#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Methods and / or classes to perform colocation
"""
import pandas as pd
import numpy as np

from pyaerocom.exceptions import (VarNotAvailableError, TimeMatchError,
                                  ColocationError, DataDimensionError,
                                  DataUnitError)
from pyaerocom.helpers import (to_pandas_timestamp, 
                               TS_TYPE_TO_PANDAS_FREQ,
                               TS_TYPE_TO_NUMPY_FREQ,
                               to_datestring_YYYYMMDD)
from pyaerocom.filter import Filter
from pyaerocom import GriddedData, UngriddedData, print_log
from pyaerocom.colocateddata import ColocatedData


class Colocator(object):
    """Helper / factory class for performing colocation of data"""
    SUPPORTED = (GriddedData, UngriddedData)
    
    def __init__(self, data_ref):
        raise NotImplementedError('Coming soon...')
        if not isinstance(data_ref, self.SUPPORTED):
            raise ValueError('Cannot instantiate colocation class. Need '
                             'either of the supported data types {} as '
                             'reference dataset'.format(self.SUPPORTED))
        self.data_ref = data_ref
        
    def run(self, data, ts_type=None, start=None, stop=None, filter_name=None,
            **add_args):
        if not isinstance(data, self.SUPPORTED):
            raise ValueError('Cannot instantiate colocation class. Need '
                             'either of the supported data types {} as '
                             'reference dataset'.format(self.SUPPORTED))
        if isinstance(self.data_ref, UngriddedData):
            if isinstance(data, GriddedData):
                return colocate_gridded_ungridded_2D(data, self.data_ref,
                                                      ts_type=ts_type,
                                                      start=start,
                                                      stop=stop,
                                                      filter_name=filter_name,
                                                      **add_args)
        elif isinstance(self.data_ref, GriddedData):
            if isinstance(data, GriddedData):
                pass
        raise NotImplementedError
        
def colocate_gridded_gridded(gridded_data, gridded_data_ref, ts_type=None,
                              start=None, stop=None, filter_name=None, 
                              regrid_scheme='areaweighted',
                              vert_scheme=None, **kwargs):
    """Colocate 2 gridded data objects
    
    Todo
    ----
    - Complete docstring
    - think about vertical dimension (vert_scheme input not used at the moment)
    """
    if ts_type is None:
        ts_type = 'yearly'
    if filter_name is None:
        filter_name = 'WORLD-wMOUNTAINS'
    if gridded_data.var_info.has_unit:
        if not gridded_data.unit == gridded_data_ref.unit:
            try:
                gridded_data_ref.convert_unit(gridded_data.unit)
            except:
                raise DataUnitError('Failed to merge data unit of reference '
                                    'gridded data object ({}) to data unit '
                                    'of gridded data object ({})'
                                    .format(gridded_data.unit, 
                                            gridded_data_ref.unit))
    # get start / stop of gridded data as pandas.Timestamp
    grid_start = to_pandas_timestamp(gridded_data.start)
    grid_stop = to_pandas_timestamp(gridded_data.stop)
    
    
    
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
    gridded_data = gridded_data.regrid(gridded_data_ref, 
                                       scheme=regrid_scheme)
    
    # perform region extraction (if applicable)
    regfilter = Filter(name=filter_name)
    gridded_data = regfilter(gridded_data)
    gridded_data_ref = regfilter(gridded_data_ref)
    
    if not gridded_data.shape == gridded_data_ref.shape:
        raise ColocationError('Shape mismatch between two colocated data '
                               'arrays, please debug')
    
    meta = {'data_source'       :   [gridded_data_ref.name,
                                    gridded_data.name],
            'var_name'          :   [gridded_data.var_name,
                                     gridded_data_ref.var_name],
            'ts_type'           :   ts_type,
            'filter_name'       :   filter_name,
            'ts_type_src'       :   grid_ts_type,
            'ts_type_src_ref'   :   gridded_data_ref.ts_type,
            'start_str'         :   to_datestring_YYYYMMDD(start),
            'stop_str'          :   to_datestring_YYYYMMDD(stop),
            'unit'              :   str(gridded_data.unit),
            'data_level'        :   'colocated',
            'revision_ref'      :   gridded_data_ref.data_revision}

    
    meta.update(regfilter.to_dict())
    data_ref = gridded_data_ref.grid.data
    if isinstance(data_ref, np.ma.core.MaskedArray):
        data_ref = data_ref.filled(np.nan)

    arr = np.asarray((data_ref,
                      gridded_data.grid.data))
    time = gridded_data.time_stamps().astype('datetime64[ns]')
    # create coordinates of DataArray
    coords = {'data_source' : meta['data_source'],
              'var_name'    : ('data_source', meta['var_name']),
              'time'        : time,
              'longitude'   : gridded_data.longitude.points,
              'latitude'    : gridded_data.latitude.points
              }
    dims = ['data_source', 'time', 'latitude', 'longitude']

    return ColocatedData(data=arr, coords=coords, dims=dims,
                          name=gridded_data.var_name, attrs=meta)

def colocate_gridded_ungridded(gridded_data, ungridded_data, 
                                  ts_type='daily', start=None, stop=None, 
                                  filter_name='WORLD-wMOUNTAINS',
                                  var_ref=None, vert_scheme=None,
                                  **kwargs):
    """Colocate gridded with ungridded data of 2D data
    
    2D means, that the vertical direction is only sampled at one altitude or
    the variable is of integrated nature (or averaged) so that the dimensionality
    of the grid data is (or can be -> cf. input parameter `vert_scheme`) 
    reduced to dimensionality time, lat, lon.
    
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
        variable to be colocated
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
        details). Default is 'WORLD-wMOUNTAINS', which corresponds to no 
        filtering (world with mountains). Use WORLD-noMOUNTAINS to exclude
        stations at altitudes exceeding 1000 m.
    var_ref : :obj:`str`, optional
        variable against which data in :attr:`gridded_data` is supposed to be
        compared. If None, then the same variable is used 
        (i.e. `gridded_data.var_name`).
    vert_scheme : str
        string specifying scheme used to reduce the dimensionality in case 
        input grid data contains vertical dimension. Example schemes are 
        `mean, surface, altitude`, for details see 
        :func:`GriddedData.to_time_series`.
    **kwargs
        additional keyword args (not used here, but included such that factory 
        class can handle different methods with different inputs)
        
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
    var = gridded_data.var_info.var_name
    if var_ref is None:
        var_ref = var
    
    if gridded_data.var_info.has_unit:
        if not gridded_data.unit == ungridded_data.unit[var_ref]:
            try:
                gridded_data.convert_unit(ungridded_data.unit[var_ref])
            except:
                raise DataUnitError('Failed to merge data unit of '
                                    'gridded data object ({}) to data unit '
                                    'of ungridded data object ({})'
                                    .format(gridded_data.unit, 
                                            ungridded_data.unit[var_ref]))
                
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
    
    # get start / stop of gridded data as pandas.Timestamp
    grid_start = to_pandas_timestamp(gridded_data.start)
    grid_stop = to_pandas_timestamp(gridded_data.stop)
    
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
                                              latitude=ungridded_lats,
                                              vert_scheme=vert_scheme)

    # pandas frequency string for TS type
    freq_pd = TS_TYPE_TO_PANDAS_FREQ[ts_type]
    freq_np = TS_TYPE_TO_NUMPY_FREQ[ts_type]
    
    start = pd.Timestamp(start.to_datetime64().astype('datetime64[{}]'.format(freq_np)))
    #stop = pd.Timestamp(stop.to_datetime64().astype('datetime64[{}]'.format(freq_np)))
    
    obs_stat_data = ungridded_data.to_station_data_all(vars_to_convert=var_ref, 
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

    ts_type_src_ref = None
    for i, obs_data in enumerate(obs_stat_data):
        if obs_data is not None:
            if ts_type_src_ref is None:
                ts_type_src_ref = obs_data['ts_type_src']
            elif not obs_data['ts_type_src'] == ts_type_src_ref:
                raise ValueError('Cannot perform colocation. Ungridded data '
                                 'object contains different source frequencies')
            # get observations (Note: the index of the observation time series
            # is already in the specified frequency format, and thus, does not
            # need to be updated, for details (or if errors occur), cf. 
            # UngriddedData.to_station_data, where the conversion happens)
            obs_tseries = obs_data[var_ref]
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
        raise ColocationError('No observations could be found that match '
                               'the colocation constraints')
    try:
        revision = ungridded_data.data_revision[dataset_ref]
    except: 
        revision = 'n/a'
    meta = {'data_source'       :   [dataset_ref,
                                     gridded_data.name],
            'var_name'          :   [var, var_ref],
            'ts_type'           :   ts_type,
            'filter_name'       :   filter_name,
            'ts_type_src'       :   grid_ts_type,
            'ts_type_src_ref'   :   ts_type_src_ref,
            'start_str'         :   to_datestring_YYYYMMDD(start),
            'stop_str'          :   to_datestring_YYYYMMDD(stop),
            'unit'              :   str(gridded_data.unit),
            'data_level'        :   'colocated',
            'revision_ref'      :   revision}

    
    meta.update(regfilter.to_dict())
    
    grid_vals = np.asarray(grid_vals)
    obs_vals = np.asarray(obs_vals)
    
    stat_dim, time_dim = grid_vals.shape
    arr = np.array((obs_vals, grid_vals))
    arr = np.swapaxes(arr, 1, 2)
    #.reshape((2, time_dim, stat_dim))
    
    # create coordinates of DataArray
    coords = {'data_source' : meta['data_source'],
              'var_name'    : ('data_source', meta['var_name']),
              'time'        : TIME_IDX,
              'station_name': station_names,
              'latitude'    : ('station_name', lats),
              'longitude'   : ('station_name', lons),
              'altitude'    : ('station_name', alts)
              }
    dims = ['data_source', 'time', 'station_name']
    data = ColocatedData(data=arr, coords=coords, dims=dims, name=var,
                          attrs=meta)
    
    return data

def colocate_gridded_ungridded_2D(*args, **kwargs):
    print(DeprecationWarning('Old name of function colocate_gridded_ungridded'
                             '(still works)'))
    return colocate_gridded_ungridded(*args, **kwargs)

if __name__=='__main__':
    import pyaerocom as pya
    
    reader = pya.io.ReadGridded('ECMWF_OSUITE')
    model_data = reader.read_var(var_name='od550aer', start=2010)
    
    obs_reader = pya.io.ReadUngridded('AeronetSunV3Lev2.daily')
    obs_data = obs_reader.read(vars_to_retrieve='od550aer')
    
    colocated_data = pya.colocation.colocate_gridded_ungridded_2D(model_data, obs_data)
    
    
    r = pya.io.ReadGridded('ECMWF_CAMS_REAN')
    model = r.read_var('od550aer', start=2010)
    
    obs_r1 = pya.io.ReadGridded('MODIS6.terra')
    obs1 = obs_r1.read_var('od550aer', start=2010)
    
    obs_r2 = pya.io.ReadUngridded('AeronetSunV3Lev2.daily')
    obs2 = obs_r2.read(vars_to_retrieve='od550aer')
    
    coll_data1 = colocate_gridded_gridded(model, obs1, ts_type='monthly')
    
    coll_data1.plot_scatter()
    
    coll_data2 = colocate_gridded_ungridded_2D(model, obs2, ts_type='monthly')
    coll_data2.plot_scatter()
    
    print(model)
    print(obs1)
    print(obs2)
    print(coll_data1)
    print(coll_data2)