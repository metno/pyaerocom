#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Methods and / or classes to perform colocation
"""
import pandas as pd
import numpy as np

from pyaerocom.exceptions import (VarNotAvailableError, TimeMatchError,
                                  ColocationError, 
                                  DataUnitError,
                                  DimensionOrderError)
from pyaerocom.helpers import (to_pandas_timestamp, 
                               TS_TYPE_TO_PANDAS_FREQ,
                               TS_TYPE_TO_NUMPY_FREQ,
                               PANDAS_RESAMPLE_OFFSETS,
                               to_datestring_YYYYMMDD)

from pyaerocom.filter import Filter
from pyaerocom.colocateddata import ColocatedData
        
def colocate_gridded_gridded(gridded_data, gridded_data_ref, ts_type=None,
                             start=None, stop=None, filter_name=None, 
                             regrid_scheme='areaweighted',
                             regrid_res_deg=None,
                             vert_scheme=None, **kwargs):
    """Colocate 2 gridded data objects
    
    Todo
    ----
    - Complete docstring
    - think about vertical dimension (vert_scheme input not used at the moment)
    """
    if ts_type is None:
        ts_type = 'monthly'
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
    
    if regrid_res_deg is not None:
        
        lons = gridded_data_ref.longitude.points
        lats = gridded_data_ref.latitude.points
        
        lons_new = np.arange(lons.min(), lons.max(), regrid_res_deg)
        lats_new = np.arange(lats.min(), lats.max(), regrid_res_deg) 
        
        gridded_data_ref = gridded_data_ref.interpolate(latitude=lats_new, 
                                                        longitude=lons_new)
        
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
    
    meta = {'data_source'       :   [gridded_data_ref.data_id,
                                     gridded_data.data_id],
            'var_name'          :   [gridded_data_ref.var_name,
                                     gridded_data.var_name],
            'ts_type'           :   ts_type,
            'filter_name'       :   filter_name,
            'ts_type_src'       :   [gridded_data_ref.ts_type, grid_ts_type],
            'start_str'         :   to_datestring_YYYYMMDD(start),
            'stop_str'          :   to_datestring_YYYYMMDD(stop),
            'unit'              :   [str(gridded_data_ref.unit),
                                     str(gridded_data.unit)],
            'data_level'        :   3,
            'revision_ref'      :   gridded_data_ref.data_revision}
    
    meta.update(regfilter.to_dict())
    data_ref = gridded_data_ref.grid.data
    if isinstance(data_ref, np.ma.core.MaskedArray):
        data_ref = data_ref.filled(np.nan)

    arr = np.asarray((data_ref,
                      gridded_data.grid.data))
    time = gridded_data.time_stamps().astype('datetime64[ns]')
    lats = gridded_data.latitude.points
    lons = gridded_data.longitude.points
    
    
    # create coordinates of DataArray
    coords = {'data_source' : meta['data_source'],
              'var_name'    : ('data_source', meta['var_name']),
              'unit'        : ('data_source', meta['unit']),
              'ts_type_src' : ('data_source', meta['ts_type_src']),
              'time'        : time,
              'latitude'    : lats,
              'longitude'   : lons,
              }
    
    dims = ['data_source', 'time', 'latitude', 'longitude']

    return ColocatedData(data=arr, coords=coords, dims=dims,
                          name=gridded_data.var_name, attrs=meta)

def colocate_gridded_ungridded(gridded_data, ungridded_data, 
                               ts_type=None, start=None, stop=None, 
                               filter_name='WORLD-wMOUNTAINS',
                               var_ref=None, vert_scheme=None,
                               harmonise_units=True,
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
    
    #Commented out on 6/2/19 due to new colocation strategy 
# =============================================================================
#     ungridded_lons = ungridded_data.longitude
#     ungridded_lats = ungridded_data.latitude               
# =============================================================================

    #crop time
    gridded_data = gridded_data.crop(time_range=(start, stop))
    
    # downscale time (if applicable)
    grid_data = gridded_data.downscale_time(to_ts_type=ts_type)

    # pandas frequency string for TS type
    freq_pd = TS_TYPE_TO_PANDAS_FREQ[ts_type]
    freq_np = TS_TYPE_TO_NUMPY_FREQ[ts_type]
    
    start = pd.Timestamp(start.to_datetime64().astype('datetime64[{}]'.format(freq_np)))
    
    all_stats = ungridded_data.to_station_data_all(vars_to_convert=var_ref, 
                                                   start=start, 
                                                   stop=stop, 
                                                   freq=freq_pd, 
                                                   by_station_name=True,
                                                   interp_nans=False)
    
    obs_stat_data = all_stats['stats']
    ungridded_lons = all_stats['longitude']
    ungridded_lats = all_stats['latitude']
    if len(obs_stat_data) == 0:
        raise VarNotAvailableError('Variable {} is not available in specified '
                                   'time interval ({}-{})'
                                   .format(var_ref, start, stop))
    # make sure the gridded data is in the right dimension
    try:
        grid_data.check_dimcoords_tseries()
    except DimensionOrderError:
        grid_data.reorder_dimensions_tseries()
    
    if grid_data.ndim > 3:
        if vert_scheme is None:
            vert_scheme = 'mean'
        if not vert_scheme in grid_data.SUPPORTED_VERT_SCHEMES:
            raise ValueError('Vertical scheme {} is not supported'.format(vert_scheme))
            
    grid_stat_data = grid_data.to_time_series(longitude=ungridded_lons,
                                              latitude=ungridded_lats,
                                              vert_scheme=vert_scheme)
    
    
    obs_vals = []
    grid_vals = []
    lons = []
    lats = []
    alts = []
    station_names = []
    
    # TIME INDEX ARRAY FOR COLLOCATED DATA OBJECT
    time_idx = pd.DatetimeIndex(freq=freq_pd, start=start, end=stop)
    if freq_pd in PANDAS_RESAMPLE_OFFSETS:
        offs = np.timedelta64(1, '[{}]'.format(PANDAS_RESAMPLE_OFFSETS[freq_pd]))
        time_idx = time_idx + offs
        
    ungridded_unit = None
    ts_type_src_ref = None
    if not harmonise_units:
        gridded_unit = str(gridded_data.unit)
    else:
        gridded_unit = None
    for i, obs_data in enumerate(obs_stat_data):
        if obs_data is not None:
            if ts_type_src_ref is None:
                ts_type_src_ref = obs_data['ts_type_src']
            elif not obs_data['ts_type_src'] == ts_type_src_ref:
                raise ValueError('Cannot perform colocation. Ungridded data '
                                 'object contains different source frequencies')
            if ungridded_unit is None:
                try:
                    ungridded_unit = obs_data['var_info'][var_ref]['unit']
                except KeyError as e: #variable information or unit is not defined
                    from pyaerocom import logger
                    logger.exception(repr(e))
            try:
                unit = obs_data['var_info'][var_ref]['unit']
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
                obs_unit = obs_data.get_unit(var_ref)
                if not grid_unit == obs_unit:
                    grid_stat.convert_unit(var, obs_unit)
                if gridded_unit is None:
                    gridded_unit = obs_unit
            grid_tseries = grid_stat[var]  
            obs_tseries = obs_data[var_ref]
            
            if sum(grid_tseries.isnull()) > 0:
                raise Exception('DEVELOPER: PLEASE DEBUG AND FIND SOLUTION')
            elif not len(grid_tseries) == len(time_idx):
                raise Exception('DEVELOPER: PLEASE DEBUG AND FIND SOLUTION')
            # make sure, time index is defined in the right way (i.e.
            # according to TIME_INDEX, e.g. if ts_type='monthly', it should
            # not be the mid or end of month)
            
            grid_tseries = pd.Series(grid_tseries.values, 
                                     index=time_idx)
            
            # the following command takes care of filling up with NaNs where
            # data is missing
            df = pd.DataFrame({'ungridded' : obs_tseries, 
                               'gridded'   : grid_tseries}, 
                              index=time_idx)
            
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
            'var_name'          :   [var_ref, var],
            'ts_type'           :   ts_type,
            'filter_name'       :   filter_name,
            'ts_type_src'       :   [ts_type_src_ref, grid_ts_type],
            'start_str'         :   to_datestring_YYYYMMDD(start),
            'stop_str'          :   to_datestring_YYYYMMDD(stop),
            'unit'              :   [ungridded_unit,
                                     gridded_unit],
            'vert_scheme'       :   vert_scheme,
            'data_level'        :   3,
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
              'unit'        : ('data_source', meta['unit']),
              'ts_type_src' : ('data_source', meta['ts_type_src']),
              'time'        : time_idx,
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

# =============================================================================
# class Colocator(object):
#     """Helper / factory class for performing colocation of data
#     
#     Note
#     ----
#     
#     This class is not functional yet
#     
#     """
#     SUPPORTED = (GriddedData, UngriddedData)
#     
#     def __init__(self, data_ref):
#         raise NotImplementedError('Coming soon...')
#         if not isinstance(data_ref, self.SUPPORTED):
#             raise ValueError('Cannot instantiate colocation class. Need '
#                              'either of the supported data types {} as '
#                              'reference dataset'.format(self.SUPPORTED))
#         self.data_ref = data_ref
#         
#     def run(self, data, ts_type=None, start=None, stop=None, filter_name=None,
#             **add_args):
#         if not isinstance(data, self.SUPPORTED):
#             raise ValueError('Cannot instantiate colocation class. Need '
#                              'either of the supported data types {} as '
#                              'reference dataset'.format(self.SUPPORTED))
#         if isinstance(self.data_ref, UngriddedData):
#             if isinstance(data, GriddedData):
#                 return colocate_gridded_ungridded_2D(data, self.data_ref,
#                                                       ts_type=ts_type,
#                                                       start=start,
#                                                       stop=stop,
#                                                       filter_name=filter_name,
#                                                       **add_args)
#         elif isinstance(self.data_ref, GriddedData):
#             if isinstance(data, GriddedData):
#                 pass
#         raise NotImplementedError
# =============================================================================
    
if __name__=='__main__':
    import pyaerocom as pya
    import matplotlib.pyplot as plt
    plt.close('all')
    
    reader = pya.io.ReadGridded('ECMWF_OSUITE')
    model_data = reader.read_var(var_name='od550aer', start=2010)
    
    obs_reader = pya.io.ReadUngridded('AeronetSunV3Lev2.daily')
    obs_data = obs_reader.read(vars_to_retrieve='od550aer')
    
    colocated_data = pya.colocation.colocate_gridded_ungridded(model_data, 
                                                               obs_data,
                                                               ts_type='monthly')
    
    colocated_data.plot_scatter()
# =============================================================================
#     r = pya.io.ReadGridded('ECMWF_CAMS_REAN')
#     model = r.read_var('od550aer', start=2010)
#     
#     obs_r1 = pya.io.ReadGridded('MODIS6.terra')
#     obs1 = obs_r1.read_var('od550aer', start=2010)
#     
#     obs_r2 = pya.io.ReadUngridded('AeronetSunV3Lev2.daily')
#     obs2 = obs_r2.read(vars_to_retrieve='od550aer')
#     
#     coll_data1 = colocate_gridded_gridded(model, obs1, ts_type='monthly')
#     
#     coll_data1.plot_scatter()
#     
#     coll_data2 = colocate_gridded_ungridded_2D(model, obs2, ts_type='monthly')
#     coll_data2.plot_scatter()
#     
#     print(model)
#     print(obs1)
#     print(obs2)
#     print(coll_data1)
#     print(coll_data2)
# =============================================================================
