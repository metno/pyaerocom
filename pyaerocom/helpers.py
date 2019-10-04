#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General helper methods for the pyaerocom library.
"""
from cf_units import Unit
from datetime import MINYEAR, datetime, date
import iris
import numpy as np
import pandas as pd
import xarray as xray

from pyaerocom.exceptions import (LongitudeConstraintError, 
                                  DataCoverageError, MetaDataError,
                                  DataDimensionError)
from pyaerocom import logger, const
from pyaerocom.time_config import (GREGORIAN_BASE, TS_TYPE_SECS,
                                   TS_TYPE_TO_PANDAS_FREQ,
                                   PANDAS_RESAMPLE_OFFSETS,
                                   TS_TYPE_DATETIME_CONV,
                                   microsec_units, millisec_units,
                                   sec_units, min_units, hr_units,
                                   day_units)

NUM_KEYS_META = ['longitude', 'latitude', 'altitude']

STR_TO_IRIS = dict(count       = iris.analysis.COUNT,
                   gmean       = iris.analysis.GMEAN,
                   hmean       = iris.analysis.HMEAN,
                   max         = iris.analysis.MAX,
                   mean        = iris.analysis.MEAN,
                   median      = iris.analysis.MEDIAN,
                   sum         = iris.analysis.SUM,
                   nearest     = iris.analysis.Nearest,
                   linear      = iris.analysis.Linear,
                   areaweighted= iris.analysis.AreaWeighted)

def delete_all_coords_cube(cube, inplace=True):
    """Delete all coordinates of an iris cube
    
    Parameters
    ----------
    cube : iris.cube.Cube
        input cube that is supposed to be cleared of coordinates
    inplace : bool
        if True, then the coordinates are deleted in the input object, else in
        a copy of it
        
    Returns
    -------
    iris.cube.Cube
        input cube without coordinates 
    """
    if not inplace:
        cube = cube.copy()
        
    for aux_fac in cube.aux_factories:
        cube.remove_aux_factory(aux_fac)

    for coord in cube.coords():
        cube.remove_coord(coord)
    return cube

def copy_coords_cube(to_cube, from_cube, inplace=True):
    """Copy all coordinates from one cube to another
    
    Requires the underlying data to be the same shape. 
    
    Warning
    --------
    This operation will delete all existing coordinates and auxiliary 
    coordinates and will then copy the ones from the input data object.
    No checks of any kind will be performed
    
    Parameters
    ----------
    to_cube
    other : GriddedData or Cube
        other data object (needs to be same shape as this object)
    
    Returns
    -------
    GriddedData
        data object containing coordinates from other object
    """
    if not all([isinstance(x, iris.cube.Cube) for x in [to_cube, from_cube]]):
        raise ValueError('Invalid input. Need instances of iris.cube.Cube class...')
        
    if not from_cube.shape == to_cube.shape:
        raise DataDimensionError('Cannot copy coordinates: shape mismatch')
    
    to_cube = delete_all_coords_cube(to_cube, inplace)
    
    for i, dim_coord in enumerate(from_cube.dim_coords):
        to_cube.add_dim_coord(dim_coord, i)
    
    for aux_coord, dim in from_cube._aux_coords_and_dims:
        to_cube.add_aux_coord(aux_coord, dim)
        
    for aux_fac in from_cube.aux_factories:
        to_cube.add_aux_factory(aux_fac)
    return to_cube

def infer_time_resolution(time_stamps):
    """Infer time resolution based on input time-stamps
    
    Uses the minimum time difference found in input array between consecutive
    time stamps and based on that finds the corresponding AeroCom resolution
    
    Parameters
    ----------
    time_stamps : pandas.DatetimeIndex
        time stamps 
    
    Ret    
    """
    import pandas as pd
    if not isinstance(time_stamps, pd.DatetimeIndex):
        try:
            time_stamps = pd.DatetimeIndex(time_stamps)
        except:
            raise ValueError('Could not infer time resolution: failed to '
                             'convert input to pandas.DatetimeIndex')
    vals = time_stamps.values
    highest_secs = abs(vals[1:] - vals[:-1]).min().astype('timedelta64[s]').astype(int)
    
    for tp in const.GRID_IO.TS_TYPES:
        if highest_secs <= TS_TYPE_SECS[tp]:
            return tp
    raise ValueError('Could not infer time resolution')

def get_tot_number_of_seconds(ts_type, dtime = None):
    from pyaerocom.tstype import TsType

    ts_tpe = TsType(ts_type)

    if ts_tpe >= TsType('monthly'):
        if dtime is None:
            raise AttributeError('For frequncies larger than or eq. monthly you' +
                                 ' need to provide dtime in order to compute the number of second.')
        else:
            # find seconds from dtime
            # TODO generalize this
            days_in_month = dtime.dt.daysinmonth
            if ts_type == 'monthly':
                monthly_to_sec = days_in_month*24*60*60
            return monthly_to_sec
    else:
        return TS_TYPE_SECS[ts_type]

def get_standard_name(var_name):
    """Converts AeroCom variable name to CF standard name
    
    Also handles alias names for variables, etc. or strings corresponding to
    older conventions (e.g. names containing 3D).
    
    Parameters
    ----------
    var_name : str
        AeroCom variable name
        
    Returns
    -------
    str
        corresponding standard name
    """
    return const.VARS[var_name].standard_name

def get_standard_unit(var_name):
    """Gets standard unit of AeroCom variable
    
    Also handles alias names for variables, etc. or strings corresponding to
    older conventions (e.g. names containing 3D).
    
    Parameters
    ----------
    var_name : str
        AeroCom variable name
        
    Returns
    -------
    str
        corresponding standard unit
    """
    return const.VARS[var_name].unit

def get_lowest_resolution(ts_type, *ts_types):
    """Get the lowest resolution from several ts_type codes
    
    Parameters
    ----------
    ts_type : str
        first ts_type
    *ts_types
        one or more additional ts_type codes
    
    Returns
    -------
    str
        the ts_type that corresponds to the lowest resolution
        
    Raises
    ------
    ValueError
        if one of the input ts_type codes is not supported
    """
    #all_ts_types = const.GRID_IO.TS_TYPES
    from pyaerocom.tstype import TsType
    lowest = TsType(ts_type)
    for freq in ts_types:
# =============================================================================
#         if not freq in all_ts_types:
#             raise ValueError('Invalid input, only valid ts_type codes are '
#                              'supported: {}'.format(all_ts_types))
# =============================================================================
        _temp = TsType(freq)
        if _temp < lowest:
            lowest = _temp
    return lowest.val

def get_highest_resolution(ts_type, *ts_types):
    """Get the highest resolution from several ts_type codes
    
    Parameters
    ----------
    ts_type : str
        first ts_type
    *ts_types
        one or more additional ts_type codes
    
    Returns
    -------
    str
        the ts_type that corresponds to the highest resolution
        
    Raises
    ------
    ValueError
        if one of the input ts_type codes is not supported
    """
    all_ts_types = const.GRID_IO.TS_TYPES
    highest = ts_type
    for freq in ts_types:
        if not freq in all_ts_types:
            raise ValueError('Invalid input, only valid ts_type codes are '
                             'supported: {}'.format(all_ts_types))
        elif all_ts_types.index(highest) > all_ts_types.index(freq):
            highest = freq
    return highest

def isnumeric(val):
    """Check if input value is numeric
    
    Parameters
    ----------
    val
        input value to be checked
    
    Returns
    -------
    bool 
        True, if input value corresponds to a range, else False.
    """
    from numbers import Number
    if isinstance(val, Number):
        return True
    return False
    
def isrange(val):
    """Check if input value corresponds to a range
    
    Checks if input is list, or array or tuple with 2 entries, or alternatively
    a slice that has defined start and stop and has set step to None.

    Note
    ----
    No check is performed, whether first entry is smaller than second entry if
    all requirements for a range are fulfilled.
    
    Parameters
    ----------
    val
        input value to be checked
    
    Returns
    -------
    bool 
        True, if input value corresponds to a range, else False.
    """
    if isinstance(val, (list, np.ndarray, tuple)):
        if len(val) == 2:
            return True
        return False
    elif isinstance(val, slice):
        if val.step is not None or val.start is None or val.stop is None:
            return False
        return True
    return False
       
def merge_station_data(stats, var_name, pref_attr=None, 
                       sort_by_largest=True, fill_missing_nan=True, 
                       **add_meta_keys):
    """Merge multiple StationData objects (from one station) into one instance
    
    Note
    ----
    - all input :class:`StationData` objects need to have same attributes\
       ``station_name``, ``latitude``, ``longitude`` and ``altitude``
    
    Parameters
    ----------
    stats : list
        list containing :class:`StationData` objects (note: all of these 
        objects must contain variable data for the specified input variable)
    var_name : str
        data variable name that is to be merged
    pref_attr 
        optional argument that may be used to specify a metadata attribute
        that is available in all input :class:`StationData` objects and that
        is used to order the input stations by relevance. The associated values
        of this attribute need to be sortable (e.g. revision_date). This is 
        only relevant in case overlaps occur. If unspecified the relevance of 
        the stations is sorted based on the length of the associated data 
        arrays.
    sort_by_largest : bool
        if True, the result from the sorting is inverted. E.g. if 
        ``pref_attr`` is unspecified, then the stations will be sorted based on
        the length of the data vectors, starting with the shortest, ending with
        the longest. This sorting result will then be inverted, if 
        ``sort_by_largest=True``, so that the longest time series get's highest
        importance. If, e.g. ``pref_attr='revision_date'``, then the stations 
        are sorted by the associated revision date value, starting with the 
        earliest, ending with the latest (which will also be inverted if 
        this argument is set to True)
    fill_missing_nan : bool
        if True, the resulting time series is filled with NaNs. NOTE: this 
        requires that information about the temporal resolution (ts_type) of
        the data is available in each of the StationData objects.
    """    
    if isinstance(var_name, list):
        if len(var_name) > 1:
            raise NotImplementedError('Merging of multivar data not yet possible')
        var_name = var_name[0]
        
    # make sure the data is provided as pandas.Series object
    is_3d, has_errs = False, False
    for stat in stats:
        if not var_name in stat:
            raise DataCoverageError('All input station must contain {} data'
                                    .format(var_name))
        elif pref_attr is not None and not pref_attr in stat:
            raise MetaDataError('Cannot sort station relevance by attribute {}. '
                                'At least one of the input stations does not '
                                'contain this attribute'.format(pref_attr))
        elif not isinstance(stat[var_name], pd.Series):
            try:
                stat._to_ts_helper(var_name)
            except Exception as e:
                raise ValueError('Data needs to be provided as pandas Series in '
                                 'individual station data objects. Attempted to'
                                 'convert but failed with the following '
                                 'exception: {}'.format(repr(e)))
        elif fill_missing_nan:
            try:
                stat.get_var_ts_type(var_name)
            except MetaDataError:
                raise MetaDataError('Cannot merge StationData objects: one or '
                                    'more of the provided objects does not '
                                    'provide information about the ts_type of '
                                    'the {} data, which is required when input '
                                    'arg. fill_missing_nan is True.'.format(var_name))
        if stat.check_if_3d(var_name):
            is_3d = True
        elif is_3d:
            raise ValueError('Merge error: some of the input stations contain '
                             'altitude info (suggesting profile data), others '
                             'not.')
        if var_name in stat.data_err:
            has_errs = True
            
    if not is_3d:
        if pref_attr is not None:
            stats.sort(key=lambda s: s[pref_attr])
        else:
            stats.sort(key=lambda s: len(s[var_name].dropna()))
        
        if sort_by_largest:
            stats = stats[::-1]

        # remove first station from the list
        merged = stats.pop(0)
            
        for i, stat in enumerate(stats): 
            merged.merge_other(stat, var_name, **add_meta_keys)
    else:
        from xarray import DataArray
        dtime = []
        for stat in stats:
            _t = stat[var_name].index.unique()
            if not len(_t) == 1:
                raise NotImplementedError('So far, merging of profile data '
                                          'requires that profile values are '
                                          'sampled at the same time')
            dtime.append(_t[0])
        tidx = pd.DatetimeIndex(dtime)
        
        # AeroCom default vertical grid
        vert_grid = const.make_default_vert_grid()
        _data = np.ones((len(vert_grid), len(tidx))) * np.nan
        if has_errs:
            _data_err = np.ones((len(vert_grid), len(tidx))) * np.nan
        
        for i, stat in enumerate(stats):
            #print(stat[var_name].values)
            if i == 0:
                merged = stat
            else:
                merged.merge_meta_same_station(stat, **add_meta_keys)

            _data[:, i] = np.interp(vert_grid, stat['altitude'], 
                                    stat[var_name].values)
            
            if has_errs:
                try:
                    _data_err[:, i] = np.interp(vert_grid, 
                                                stat['altitude'], 
                                                stat.data_err[var_name])
                except:
                    pass
        _coords = {'time'     : tidx,
                   'altitude' : vert_grid}
        
        d = DataArray(data=_data, coords=_coords, 
                      dims=['altitude', 'time'], name=var_name)
        d = d.sortby('time')
        merged[var_name] = d
        merged.dtime = d.time
        merged.altitude = d.altitude
    
    if fill_missing_nan:
        try:
            merged.insert_nans_timeseries(var_name)
        except Exception as e:
            const.print_log.warning('Could not insert NaNs into timeseries of '
                                    'variable {} after merging stations. '
                                    'Reason: {}'.format(var_name, repr(e)))
            
    merged['stat_merge_pref_attr'] = pref_attr
    return merged

def _get_pandas_freq_and_loffset(freq):
    """Helper to convert resampling info"""
    if freq in TS_TYPE_TO_PANDAS_FREQ:
        freq = TS_TYPE_TO_PANDAS_FREQ[freq]
    loffset = None
    if freq in PANDAS_RESAMPLE_OFFSETS:
        loffset = PANDAS_RESAMPLE_OFFSETS[freq]
    return (freq, loffset)

def resample_timeseries(s, freq, how='mean', min_num_obs=None):
    """Resample a timeseries (pandas.Series)
    
    Parameters
    ----------
    s : Series
        time series instance
    freq : str
        new temporal resolution (can be pandas freq. string, or pyaerocom
        ts_type)
    how : str
        choose from mean or median
    min_num_obs : :obj:`int`, optional
        minimum number of observations required per period (when downsampling).
        E.g. if input is in daily resolution and freq is monthly and 
        min_num_obs is 10, then all months that have less than 10 days of data
        are set to nan.
    
    Returns
    -------
    Series
        resampled time series object
    """
    freq, loffset = _get_pandas_freq_and_loffset(freq)    
    resampler = s.resample(freq, loffset=loffset)
    if min_num_obs is None:
        data = resampler.agg(how)
    else:
        df = resampler.agg([how, 'count'])
        const.logger.info(freq, min_num_obs)
        const.logger.info('before mean', df[how].mean())
        invalid = df['count'] < min_num_obs
        const.logger.info(len(invalid), invalid.sum())
        df[how][invalid] = np.nan
        const.logger.info('after mean', df[how].mean())
        data = df[how]

    return data.loc[s.index[0]:s.index[-1]]

def resample_time_dataarray(arr, freq, how='mean', min_num_obs=None):
    """Resample the time dimension of a :class:`xarray.DataArray`
    
    Note
    ----
    The dataarray must have a dimension coordinate named "time"
    
    Parameters
    ----------
    arr : DataArray
        data array to be resampled
    freq : str
        new temporal resolution (can be pandas freq. string, or pyaerocom
        ts_type)
    how : str
        choose from mean or median
    min_num_obs : :obj:`int`, optional
        minimum number of observations required per period (when downsampling).
        E.g. if input is in daily resolution and freq is monthly and 
        min_num_obs is 10, then all months that have less than 10 days of data
        are set to nan.
    
    Returns
    -------
    DataArray
        resampled data array object
    
    Raises
    ------
    IOError
        if data input `arr` is not an instance of :class:`DataArray`
    DataDimensionError
        if time dimension is not available in dataset
    """
    
    if not isinstance(arr, xray.DataArray):
        raise IOError('Invalid input for arr: need DataArray, got {}'.format(type(arr)))
    elif not 'time' in arr.dims:
        raise DataDimensionError('Cannot resample time: input DataArray has '
                                 'no time dimension')

    from pyaerocom.tstype import TsType
    from pyaerocom.time_config import XARR_TIME_GROUPERS
    to = TsType(freq)
    pd_freq=to.to_pandas()
    invalid = None
    if min_num_obs is not None:
        if not pd_freq in XARR_TIME_GROUPERS:
            raise ValueError('Cannot infer xarray grouper for ts_type {}'
                             .format(to.val))
        gr = XARR_TIME_GROUPERS[pd_freq]
        # 2D mask with shape of resampled data array
        invalid = arr.groupby('time.{}'.format(gr)).count(dim='time') < min_num_obs

    freq, loffset = _get_pandas_freq_and_loffset(freq)    
    arr = arr.resample(time=pd_freq, loffset=loffset).mean(dim='time')
    if invalid is not None:
        arr.data[invalid.data] = np.nan
    return arr
    
def same_meta_dict(meta1, meta2, ignore_keys=['PI'], 
                   num_keys=NUM_KEYS_META, num_rtol=1e-2):
    """Compare meta dictionaries
    
    Parameters
    ----------
    meta1 : dict
        meta dictionary that is to be compared with ``meta2``
    meta2 : dict
        meta dictionary that is to be compared with ``meta1``
    ignore_keys : list
        list containing meta keys that are supposed to be ignored
    num_keys : keys that contain numerical values
    num_rtol : float
        relative tolerance level for comparison of numerical values
        
    Returns
    -------
    bool 
        True, if dictionaries are the same, else False
    """
    if not meta1.keys() == meta2.keys():
        return False
    for k, v in meta1.items():
        if k in ignore_keys:
            continue
        elif k in num_keys:
            if not np.isclose(v, meta2[k], rtol=num_rtol):
                return False
        elif isinstance(v, dict):
            if not same_meta_dict(v, meta2[k]):
                return False
        else:
            if not v == meta2[k]:
                return False
    return True
            
def str_to_iris(key, **kwargs):
    """Mapping function that converts strings into iris analysis objects
    
    Please see dictionary ``STR_TO_IRIS`` in this module for valid definitions
    
    Parameters
    ----------
    key : str
        key of :attr:`STR_TO_IRIS` dictionary
        
    Returns
    -------
    obj
        corresponding iris analysis object (e.g. Aggregator, method)
    """
    key = key.lower()
    if not key in STR_TO_IRIS:
        raise KeyError("No iris.analysis object available for key %s, please "
                       "choose from %s" %(key, STR_TO_IRIS.keys()))
    val = STR_TO_IRIS[key]
    if callable(val):
        return val(**kwargs)
    return val

def to_pandas_timestamp(value):
    """Convert input to instance of :class:`pandas.Timestamp`"""
    if isinstance(value, pd.Timestamp):
        return value
    elif isinstance(value, (str, np.datetime64, datetime, date)):
        return pd.Timestamp(value)
    else:
        try:
            numval = int(value)
            if not 0 <= numval <= 10000:
                raise ValueError('Could not infer valid year from numerical '
                                 'time input')
            return pd.Timestamp(str(numval))
        except Exception as e:
            raise ValueError('Failed to convert {} to Timestamp: {}'
                             .format(value, repr(e)))    
    
def to_datetime64(value):
    """Convert input value to numpy.datetime64 
    
    Parameters
    ----------
    value
        input value that is supposed to be converted, needs to be either str, 
        datetime.datetime, pandas.Timestamp or an integer specifying the 
        desired year.
        
    Returns
    -------
    datetime64
        input timestamp converted to datetime64
    """
    if isinstance(value, np.datetime64):
        return value
    else:
        try:
            return to_pandas_timestamp(value).to_datetime64()
        except Exception as e:
            raise ValueError('Failed to convert {} to datetime64 object'
                             'Error: {}'.format(value, repr(e)))
  
def is_year(val):
    """Check if input is / may be year
    
    Parameters
    ----------
    val
        input that is supposed to be checked    
    
    Returns
    -------
    bool
        True if input is a number between -2000 and 10000, else False
    """
    try:
        if -2000 < int(val) < 10000:
            return True
        raise Exception
    except:
        return False
  
def _check_climatology_timestamp(t):
    if isnumeric(t) and t == 9999:
        return pd.Timestamp('1-1-2222')
    elif isinstance(t, np.datetime64):
        tstr = str(t)
        if tstr.startswith('9999'):
            return pd.Timestamp(tstr.replace('9999', '2222'))
    elif isinstance(t, str) and '9999' in t:
        return pd.Timestamp(t.replace('9999', '2222'))
    elif isinstance(t, datetime) and t.year == 9999:
        return pd.Timestamp(t.replace(year=2222))
    raise ValueError('Failed to identify {} as climatological timestamp...'
                     .format(t))
    
def start_stop(start, stop=None):
    """Create pandas timestamps from input start / stop values
    
    Note
    ----
    If input suggests climatological data in AeroCom format (i.e. year=9999) 
    then the year is converted to 2222 instead since pandas cannot handle 
    year 9999.
    
    Parameters
    -----------
    start
        start time (any format that can be converted to pandas.Timestamp)
    stop
        stop time (any format that can be converted to pandas.Timestamp)
    
    Returns
    -------
    pandas.Timestamp
        start timestamp
    pandas.Timestamp
        stop timestamp
    
    Raises
    ------
    ValueError
        if input cannot be converted to pandas timestamps
    """
    isclim = False
    try:
        start = to_pandas_timestamp(start)
    except pd.errors.OutOfBoundsDatetime: # probably climatology
        start = _check_climatology_timestamp(start)
        isclim = True
        
    if stop is None:
        if isclim:
            yr = 2222
        else:
            yr = start.year
        stop = to_pandas_timestamp('{}-12-31 23:59:59'.format(yr))
    else:
        try:
            stop = to_pandas_timestamp(stop)
        except pd.errors.OutOfBoundsDatetime:
            stop = _check_climatology_timestamp(stop)
    return (start, stop)

def datetime2str(time, ts_type=None):
    conv = TS_TYPE_DATETIME_CONV[ts_type]
    if is_year(time):
        return str(time)
    try:
        time = to_pandas_timestamp(time).strftime(conv)
    except pd.errors.OutOfBoundsDatetime:
        const.print_log.warning('Failed to convert time {} to string'.format(time))
        pass
    return time

def start_stop_str(start, stop=None, ts_type=None):
    
    conv = TS_TYPE_DATETIME_CONV[ts_type]
    if is_year(start) and stop is None:
        return str(start)
    start, stop = start_stop(start, stop)
    start_str = start.strftime(conv)
    stop_str = stop.strftime(conv)
    if stop_str != start_str:
        return '{}-{}'.format(start_str, stop_str)
    return start_str

def start_stop_from_year(year):
    """Create start / stop timestamp from year
    
    Parameters
    ----------
    year : int
        the year for which start / stop is to be instantiated
        
    Returns
    -------
    tuple
        2-element tuple containing
        
        - :obj:`pandas.Timestamp`: start timestamp
        - :obj:`pandas.Timestamp`: end timestamp
    """
    start = to_pandas_timestamp(year)
    stop = to_pandas_timestamp('{}-12-31 23:59:59'.format(year))
    return (start, stop)
            
def to_datestring_YYYYMMDD(value):
    """Convert input time to string with format YYYYMMDD
    
    Parameters
    ----------
    value
        input time, may be string, datetime, numpy.datetime64 or 
        pandas.Timestamp
        
    Returns
    -------
    str
        input formatted to string YYYYMMDD
        
    Raises
    ------
    ValueError
        if input is not supported
    """
    if isinstance(value, str) and len(value, 8):
        logger.info('Input is already string containing 8 chars. Assuming it '
                    'is in the right format and returning unchanged')
        return value
    try:
        return to_pandas_timestamp(value).strftime('%Y%m%d')
    except Exception as e:
        raise ValueError('Invalid input, need str, datetime, numpy.datetime64 '
                         'or pandas.Timestamp. Error: {}'.format(repr(e)))
    
def cftime_to_datetime64(times, cfunit=None, calendar=None):
    """Convert numerical timestamps with epoch to numpy datetime64
    
    This method was designed to enhance the performance of datetime conversions
    and is based on the corresponding information provided in the cftime 
    package (`see here <https://github.com/Unidata/cftime/blob/master/cftime/
    _cftime.pyx>`__). Particularly, this object does, what the :func:`num2date` 
    therein does, but faster, in case the time stamps are not defined on a non
    standard calendar.
    
    Parameters
    ----------
    times : :obj:`list` or :obj:`ndarray` or :obj:`iris.coords.DimCoord`
        array containing numerical time stamps (relative to basedate of 
        ``cfunit``). Can also be a single number.
    cfunit : :obj:`str` or :obj:`Unit`, optional
        CF unit string (e.g. day since 2018-01-01 00:00:00.00000000 UTC) or
        unit. Required if `times` is not an instance of 
        :class:`iris.coords.DimCoord`
    calendar : :obj:`str`, optional
        string specifying calendar (only required if ``cfunit`` is of type
        ``str``).
        
    Returns
    -------
    ndarray
        numpy array containing timestamps as datetime64 objects
        
    Raises
    ------
    ValueError
        if cfunit is ``str`` and calendar is not provided or invalid, or if 
        the cfunit string is invalid
        
    Example
    -------
    
    >>> cfunit_str = 'day since 2018-01-01 00:00:00.00000000 UTC'
    >>> cftime_to_datetime64(10, cfunit_str, "gregorian")
    array(['2018-01-11T00:00:00.000000'], dtype='datetime64[us]')
    """
    if isinstance(times, iris.coords.DimCoord): #special case
        times, cfunit = times.points, times.units
    try:
        len(times)
    except:
        times = [times]
    if isinstance(cfunit, str):
        if calendar is None:
            raise ValueError("Require specification of calendar for "
                             "conversion into datetime64 objects")
        cfunit = Unit(cfunit, calendar) #raises Error if calendar is invalid
    if not isinstance(cfunit, Unit):
        raise ValueError("Please provide cfunit either as instance of class "
                         "cf_units.Unit or as a string")
    calendar = cfunit.calendar
    basedate = cfunit.num2date(0)
    if ((calendar == 'proleptic_gregorian' and basedate.year >= MINYEAR) or 
        (calendar in ['gregorian','standard'] and basedate > GREGORIAN_BASE)):
        # NOTE: changed on 9 July 2018 by jgliss due to error (kernel died)
        # after update of dependencies (cf_units). Attribute name does not
        # work anymore...
        cfu_str = cfunit.origin #cfunit.name
        
        res = cfu_str.split()[0].lower()
        if res in microsec_units:
            tstr = "us"
        elif res in millisec_units:
            tstr = "ms"
        elif res in sec_units:
            tstr = "s"
        elif res in min_units:
            tstr = "m"
        elif res in hr_units:
            tstr = "h"
        elif res in day_units:
            tstr = "D"
        else:
            raise ValueError('unsupported time units')
        
        basedate = np.datetime64(basedate)
        dt = np.asarray(np.asarray(times), dtype="timedelta64[%s]" %tstr)
        return basedate + dt
    else:
        return np.asarray([np.datetime64(t) for t in cfunit.num2date(times)])

def get_constraint(lon_range=None, lat_range=None, 
                   time_range=None, meridian_centre=True):
    """Function that creates an :class:`iris.Constraint` based on input
    
    Note
    ----
    Please be aware of the definition of the longitudes in your data when 
    cropping within the longitude dimension. The longitudes in your data may be 
    defined either from **-180 <= lon <= 180** (pyaerocom standard) or from 
    **0 <= lon <= 360**. In the former case (-180 -> 180) you can leave the 
    additional input parameter ``meridian_centre=True`` (default). 
    
    Parameters
    ----------
    lon_range : :obj:`tuple`, optional
        2-element tuple containing longitude range for cropping
        Example input to crop around meridian: `lon_range=(-30, 30)`
    lat_range : :obj:`tuple`, optional
        2-element tuple containing latitude range for cropping. 
    time_range : :obj:`tuple`, optional
        2-element tuple containing time range for cropping. Allowed data
        types for specifying the times are 
        
            1. a combination of 2 :class:`pandas.Timestamp` instances or 
            2. a combination of two strings that can be directly converted\
            into :class:`pandas.Timestamp` instances (e.g.\
            `time_range=("2010-1-1", "2012-1-1")`) or
            3. directly a combination of indices (:obj:`int`). 
    meridian_centre : bool
        specifies the coordinate definition range of longitude array. If True, 
        then -180 -> 180 is assumed, else 0 -> 360
        
    Returns
    -------
    iris.Constraint
        the combined constraint from all valid input parameters
    
    Examples
    --------
    The following example shows how to crop over the meridian
    
    >>> from pyaerocom.helpers import get_constraint
    >>> from pyaerocom.io.fileconventions import FileConventionRead
    >>> from iris import load
    >>> from pyaerocom.io.testfiles import get
    >>> files = get()
    >>> fname = files['models']['aatsr_su_v4.3']
    >>> convention = FileConventionRead().from_file(fname)
    >>> meta_info = convention.get_info_from_file(fname)
    >>> for k, v in meta_info.items(): print(k, v)
    year 2008
    var_name od550aer
    ts_type daily
    >>> cubes = load(fname)
    >>> lons = cubes[0].coord("longitude").points
    >>> meridian_centre = True if lons.max() > 180 else False
    >>> year = meta_info["year"]
    >>> c = get_constraint(lon_range=(50, 150), 
    ...                    lat_range=(20, 60), 
    ...                    time_range=("%s-02-05" %year, "%s-02-25" %year))
    >>> cube_crop = cubes.extract(c)[0]
    >>> cube_crop.shape
    (21, 40, 100)
    """
    constraints = []
    if lon_range is not None:
        constraints.append(get_lon_rng_constraint(lon_range, meridian_centre))
    if lat_range is not None:
        constraints.append(get_lat_rng_constraint(lat_range))
    if time_range is not None:
        constraints.append(get_time_rng_constraint(*time_range))
    if len(constraints) > 0:
        c = constraints[0]
        for cadd in constraints[1:]:
            c = c & cadd
    return c
    
def get_lat_rng_constraint(lat_range):
    """Create latitude constraint based on input range
    
    Parameters
    ----------
    lat_range : tuple
        2-element tuple specifying latitude range
    
    Returns
    -------
    iris.Constraint
        the corresponding iris.Constraint instance
        
    """
    return iris.Constraint(latitude=lambda v: lat_range[0] <= v <= lat_range[1])
    
def get_lon_rng_constraint(lon_range, meridian_centre=True):
    """Create longitude constraint based on input range

    Parameters
    ----------
    lon_range : tuple
        2-element tuple containing from left -> right end of range
    meridian_centre : bool
        specifies the coordinate definition range of longitude array of the 
        data to be cropped. If True, then -180 -> 180 is assumed, else 0 -> 360
    
    Returns
    -------
    iris.Constraint
        the corresponding iris.Constraint instance 
    
    Raises
    ------
    ValueError
        if first coordinate in lon_range equals or exceeds second
    LongitudeConstraintError
        if the input implies cropping over border of longitude array
        (e.g. 160 -> - 160 if -180 <= lon <= 180).

    Example
    -------
    >>> from pyaerocom.io.testfiles import get
    >>> from pyaerocom import GriddedData
    >>> files = get()
    >>> data = GriddedData(files['models']['aatsr_su_v4.3'], var_name="od550aer")
    >>> c = get_lon_rng_constraint(lon_range=(170, -160), meridian_centre=True)
    Traceback (most recent call last):
     ...
    ValueError: Left coordinate must exceed right coordinate
    >>> c = get_lon_rng_constraint(lon_range=(-30, 30), meridian_centre=True)
    >>> data_crop = data.extract(c)
    >>> assert data_crop.grid.shape == (366, 180, 60)
    """
    left, right = lon_range
    if left == right:
        raise ValueError("the specified values are equal")
    elif left > right:
        raise ValueError("Left coordinate must exceed right coordinate")
    if meridian_centre:
        left, right = (left+180)%360-180, (right+180)%360-180
    else:
        left, right = left%360, right%360
    if left > right:
        msg = ("Cannot crop over right border of longitude range")
        raise LongitudeConstraintError(msg)
    return iris.Constraint(longitude=lambda v: left <= v <= right)

def get_time_rng_constraint(start, stop):
    """Create iris.Constraint for data extraction along time axis
    
    Parameters
    ----------
    start : :obj:`Timestamp` or :obj:` str`
        start time of desired subset. If string, it must be convertible 
        into :class:`pandas.Timestamp` (e.g. "2012-1-1")
    stop : :obj:`Timestamp` or :obj:` str`
        start time of desired subset. If string, it must be convertible 
        into :class:`pandas.Timestamp` (e.g. "2012-1-1")
    
    Returns
    -------
    iris.Constraint
        iris Constraint instance that can, e.g., be used as input for
        :func:`pyaerocom.griddeddata.GriddedData.extract`
    """
    if not isinstance(start, pd.Timestamp):
        start = pd.Timestamp(start)
    if not isinstance(stop, pd.Timestamp):
        stop = pd.Timestamp(stop)
        
    t_lower = iris.time.PartialDateTime(year=start.year,
                                        month=start.month,
                                        day=start.day)
    t_upper = iris.time.PartialDateTime(year=stop.year,
                                        month=stop.month,
                                        day=stop.day)
    
    return iris.Constraint(time=lambda cell: t_lower <= cell <= t_upper)

if __name__=="__main__":
    print(get_lowest_resolution('yearly', 'daily', 'monthly'))
    print(get_highest_resolution('yearly', 'daily', 'monthly'))
    
    print(infer_time_resolution([np.datetime64('2010-01-01'),
                                 np.datetime64('2010-01-02'),
                                 np.datetime64('2010-01-05'),
                                 np.datetime64('2010-10-15')]))