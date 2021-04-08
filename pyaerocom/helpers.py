#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General helper methods for the pyaerocom library.
"""
from cf_units import Unit
from collections import Counter
from datetime import MINYEAR, datetime, date
import iris
import math as ma
import numpy as np
import pandas as pd
import xarray as xray

from pyaerocom.exceptions import (LongitudeConstraintError,
                                  DataCoverageError, MetaDataError,
                                  DataDimensionError,
                                  VariableDefinitionError,
                                  ResamplingError,
                                  TemporalResolutionError)
from pyaerocom import logger, const
from pyaerocom.time_config import (GREGORIAN_BASE, TS_TYPE_SECS,
                                   TS_TYPE_TO_PANDAS_FREQ,
                                   PANDAS_RESAMPLE_OFFSETS,
                                   TS_TYPE_DATETIME_CONV,
                                   microsec_units, millisec_units,
                                   sec_units, min_units, hr_units,
                                   day_units)
from pyaerocom.tstype import TsType

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

def varlist_aerocom(varlist):

    if isinstance(varlist, str):
        varlist = [varlist]
    elif not isinstance(varlist, list):
        raise ValueError('Need string or list')
    output = []
    for var in varlist:
        try:
            _var = const.VARS[var].var_name_aerocom
            if not _var in output:
                output.append(_var)
        except VariableDefinitionError as e:
            const.print_log.warning(repr(e))
    if len(output) == 0:
        raise ValueError('None of the input variables appears to be valid')
    return output

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

def extract_latlon_dataarray(arr, lat, lon, lat_dimname=None,
                             lon_dimname=None, method='nearest',
                             new_index_name=None, check_domain=True):
    """Extract individual lat / lon coordinates from `DataArray`

    Parameters
    ----------
    arr : DataArray
        data (must contain lat and lon dimensions)
    lat : array or similar
        1D array containing latitude coordinates
    lon : array or similar
        1D array containing longitude coordinates
    lat_dimname : str, optional
        name of latitude dimension in input data (if None, it assumes standard
        name)
    lon_dimname : str, optional
        name of longitude dimension in input data (if None, it assumes standard
        name)
    method : str
        how to interpolate to input coordinates (defaults to nearest neighbour)
    new_index_name : str, optional
        name of flattend latlon dimension (defaults to latlon)
    check_domain : bool
        if True, lat/lon domain of datarray is checked and all input coordinates
        that are outside of the domain are ignored.

    Returns
    -------
    DataArray
        data at input coordinates
    """
    if lat_dimname is None:
        lat_dimname = 'lat'
    if lon_dimname is None:
        lon_dimname = 'lon'
    if not lat_dimname in arr.dims and lat_dimname == 'lat':
        for alias in const.COORDINFO['lat'].aliases:
            if alias in arr.dims:
                lat_dimname = alias
                break
    if not lon_dimname in arr.dims and lon_dimname == 'lon':
        for alias in const.COORDINFO['lon'].aliases:
            if alias in arr.dims:
                lon_dimname = alias
                break
    if isinstance(lat, str):
        lat = [lat]
    if isinstance(lon, str):
        lon = [lon]
    if check_domain:
        arr_lat = arr[lat_dimname].data
        arr_lon = arr[lon_dimname].data
        lat0, lat1 = arr_lat.min(), arr_lat.max()
        lon0, lon1 = arr_lon.min(), arr_lon.max()
        new_lat = []
        new_lon = []
        for x, y in zip(lat, lon):
            if (lat0 <= x <= lat1) and (lon0 <= y <= lon1):
                new_lat.append(x)
                new_lon.append(y)
        if len(new_lat) == 0 and len(new_lon) == 0:
            raise DataCoverageError('Coordinates not found in dataarray')
        lat, lon = new_lat, new_lon
    if new_index_name is None:
        new_index_name = 'latlon'
    where = {lat_dimname : xray.DataArray(lat, dims=new_index_name),
             lon_dimname : xray.DataArray(lon, dims=new_index_name)}
    subset = arr.sel(where, method=method)
    subset.attrs['lat_dimname'] = lat_dimname
    subset.attrs['lon_dimname'] = lon_dimname
    return subset

def lists_to_tuple_list(*lists):
    """Convert input lists (of same length) into list of tuples

    e.g. input 2 lists of latitude and longitude coords, output one list
    with tuple coordinates at each index
    """
    return list(zip(*lists))

def tuple_list_to_lists(tuple_list):
    """Convert list with tuples (e.g. (lat, lon)) into multiple lists"""
    return list(map(list, zip(tuple_list)))

def make_dummy_cube_latlon(lat_res_deg=2, lon_res_deg=3, lat_range=None,
                           lon_range=None):
    """Make an empty Cube with given latitude and longitude resolution

    Dimensions will be lat, lon

    Parameters
    ----------
    lat_res_deg : float or int
        latitude resolution of grid
    lon_res_deg : float or int
        longitude resolution of grid
    lat_range : tuple or list
        2-element list containing latitude range. If `None`, then `(-90, 90)`
        is used.
    lon_range : tuple or list
        2-element list containing longitude range. If `None`, then `(-180, 180)`
        is used.

    Returns
    -------
    Cube
        dummy cube in input resolution
    """
    if lat_range is None:
        lat_range = (-90, 90)
    if lon_range is None:
        lon_range = (-180, 180)

    lons = np.arange(lon_range[0]+lon_res_deg/2, lon_range[1]+lon_res_deg/2,
                     lon_res_deg)
    lats = np.arange(lat_range[0]+lat_res_deg/2, lat_range[1]+lat_res_deg/2,
                     lat_res_deg)

    lon_circ = check_coord_circular(lons, modulus=360)
    latdim = iris.coords.DimCoord(lats, var_name='lat',
                                  standard_name='latitude',
                                  circular=False,
                                  units=Unit('degrees'))

    londim = iris.coords.DimCoord(lons, var_name='lon',
                                  standard_name='longitude',
                                  circular=lon_circ,
                                  units=Unit('degrees'))

    latdim.guess_bounds()
    londim.guess_bounds()
    dummy = iris.cube.Cube(np.ones((len(lats), len(lons))))

    dummy.add_dim_coord(latdim, 0)
    dummy.add_dim_coord(londim, 1)
    dummy.var_name = 'dummy_grid'

    return dummy

def check_coord_circular(coord_vals, modulus, rtol=1e-5):
    """Check circularity of coordinate

    Parameters
    ----------
    coord_vals : list or ndarray
        values of coordinate to be tested
    modulus : float or int
        modulus of coordinate (e.g. 360 for longitude)
    rtol : float
        relative tolerance

    Returns
    -------
    bool
        True if circularity is given, else False

    Raises
    ------
    ValueError
        if circularity is given and results in overlap (right end of input
        array is mapped to a value larger than the first one at the left end
        of the array)

    """
    from pyaerocom import const
    if len(coord_vals) < 2:
        const.print_log.warning('Checking coordinate values for circularity '
                                'failed since coord array has less than 2 values')
        return False
    step = coord_vals[-1] - coord_vals[-2]
    tol = step*rtol
    diff = coord_vals[-1] - coord_vals[0] + step
    if diff - tol > modulus:
        raise ValueError('Circularity is given but results in overlap (right '
                         'end of input array is mapped to a value larger than '
                         'the first one at the left end of the array).')
    if abs(modulus - diff) > tol:
        return False
    return True

def numpy_to_cube(data, dims=None, var_name=None, units=None, **attrs):
    """Make a cube from a numpy array

    Parameters
    ----------
    data : ndarray
        input data
    dims : list, optional
        list of :class:`iris.coord.DimCoord` instances in order of dimensions
        of input data array (length of list and shapes of each of the
        coordinates must match dimensions of input data)
    var_name : str, optional
        name of variable
    units : str
        unit of variable
    **attrs
        additional attributes to be added to metadata

    Returns
    -------
    iris.cube.Cube

    Raises
    ------
    DataDimensionError
        if input `dims` is specified and results in conflict
    """
    if not isinstance(data, np.ndarray):
        raise ValueError('Invalid input, need numpy array')
    cube = iris.cube.Cube(data)

    cube.var_name=var_name
    cube.units = units

    sh = data.shape
    if dims is not None:
        if not len(dims) == data.ndim:

            raise DataDimensionError('Input number of dimensios must match array '
                                     'dimension number')
        for i, dim in enumerate(dims):
            if not isinstance(dim, iris.coords.DimCoord):
                raise ValueError('Need iris.DimCoord...')
            elif not len(dim.points) == sh[i]:
                raise DataDimensionError('Length mismatch between {} dim ({}) and '
                                         'array dimension {} ({})'
                                         .format(dim.var_name, len(dim.points),
                                                 i, sh[i]))
            cube.add_dim_coord(dim, i)

    cube.attributes.update(attrs)
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

def infer_time_resolution(time_stamps, dt_tol_percent=5,
                          minfrac_most_common=0.8):
    """Infer time resolution based on input time-stamps

    Calculates time difference *dt* between consecutive timestamps provided via
    input array or list. Then it counts the most common *dt* (e.g. 86400 s for
    daily). Before inferring the frequency it then checks all other *dts*
    occurring in the input array to see if they are within a certain interval
    around the most common one (e.g. +/- 5% as default, via arg
    `dt_tol_percent`), that is, 86390 would be included if most common dt is
    86400 s but not 80000s. Then it checks if the number of *dts* that
    are within that tolerance level around the most common *dt* exceed a
    certain fraction (arg `minfrac_most_common`) of the total number of *dts*
    that occur in the input array (default is 80%). If that is the case, the
    most common frequency is attempted to be derived using
    :func:`TsType.from_total_seconds` based on the most common *dt* (in this
    example that would be *daily*).


    Parameters
    ----------
    time_stamps : pandas.DatetimeIndex, or similar
        list of time stamps
    dt_tol_percent : int
        tolerance in percent of accepted range of time diffs with respect to
        most common time difference.
    minfrac_most_common : float
        minimum required fraction of time diffs that have to be equal to, or
        within tolerance range, the most common time difference.


    Raises
    ------
    TemporalResolutionError
        if frequency cannot be derived.

    Returns
    -------
    str
        inferred frequency
    """
    from pyaerocom import TsType

    if not isinstance(time_stamps, pd.DatetimeIndex):
        time_stamps = pd.DatetimeIndex(time_stamps)
    vals = time_stamps.values

    dts = (vals[1:] - vals[:-1]).astype('timedelta64[s]').astype(int)

    if np.min(dts) < 0:
        raise TemporalResolutionError(
            'Nasa Ames file contains neg. meas periods...')

    counts = Counter(dts).most_common()
    most_common_dt, most_common_num = counts[0]
    num_within_tol = most_common_num
    lower = most_common_dt * (100 - dt_tol_percent)/100
    upper = most_common_dt * (100 + dt_tol_percent)/100
    for dt, num in counts[1:]:
        if lower <= dt <= upper:
            num_within_tol += num
    frac_ok = num_within_tol / len(dts)
    if not frac_ok > minfrac_most_common:
        raise TemporalResolutionError('Failed to infer ts_type')
    tst = TsType.from_total_seconds(most_common_dt)
    return str(tst)

def seconds_in_periods(timestamps, ts_type):
    """
    Calculates the number of seconds for each period in timestamps.

    Parameters
    ----------
    timestamps : numpy.datetime64 or numpy.ndarray
        Either a single datetime or an array of datetimes.
    ts_type : str
        Frequency of timestamps.

    Returns
    -------
    np.array :
        Array with same length as timestamps containing number of seconds for
        each period.
    """

    ts_type = TsType(ts_type)
    if isinstance(timestamps, np.datetime64):
        timestamps = np.array([timestamps])
    if isinstance(timestamps, np.ndarray):
        timestamps = [to_pandas_timestamp(timestamp) for timestamp in timestamps]
    # From here on timestamps should be a numpy array containing pandas Timestamps

    seconds_in_day = 86400
    if ts_type >= TsType('monthly'):
        if ts_type == TsType('monthly'):
            days_in_months = np.array([ timestamp.days_in_month for timestamp in timestamps])
            seconds = days_in_months * seconds_in_day
            return seconds
        if ts_type == TsType('daily'):
            return seconds_in_day * np.ones_like(timestamps)
        raise NotImplementedError('Only yearly, monthly and daily frequencies implemented.')
    elif ts_type == TsType('yearly'):
        days_in_year = []
        for ts in timestamps:
            if ts.year % 4 == 0:
                days_in_year.append(366) #  Leap year
            else:
                days_in_year.append(365)
        seconds = np.array(days_in_year) * seconds_in_day
        return seconds
    raise TemporalResolutionError('Unknown TsType: {}'.format(ts_type))

def get_tot_number_of_seconds(ts_type, dtime=None):
    """Get total no. of seconds for a given frequency

    ToDo
    ----
    This method needs revision and can be solved simpler probably

    Parameters
    ----------
    ts_type : str or TsType
        frequency for which number of seconds is supposed to be retrieved
    dtime : TYPE, optional
        DESCRIPTION. The default is None.

    Raises
    ------
    AttributeError
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """

    ts_tpe = TsType(ts_type)

    if ts_tpe >= TsType('monthly'):
        if dtime is None:
            raise AttributeError('For frequncies larger than or eq. monthly you' +
                                 ' need to provide dtime in order to compute the number of second.')
        if not ts_type == 'monthly':
            raise NotImplementedError('Can only handle monthly so far...')

        # find seconds from dtime
        # TODO generalize this
        days_in_month = dtime.dt.daysinmonth

        return days_in_month*24*60*60
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
    from pyaerocom import const
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
    from pyaerocom import const
    return const.VARS[var_name].units

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
        _temp = TsType(freq)
        if _temp < lowest:
            lowest = _temp
    return lowest.val

def sort_ts_types(ts_types):
    """Sort a list of ts_types

    Parameters
    ----------
    ts_types : list
        list of strings (or instance of :class:`TsType`) to be sorted

    Returns
    -------
    list
        list of strings with sorted frequencies

    Raises
    ------
    TemporalResolutionError
        if one of the input ts_types is not supported
    """
    freqs_sorted = []
    for ts_type in ts_types:
        if isinstance(ts_type, str):
            ts_type = TsType(ts_type)
        if len(freqs_sorted) == 0:
            freqs_sorted.append(ts_type)
        else:
            insert = False
            for i, tt in enumerate(freqs_sorted):
                if tt < ts_type:
                    insert=True
                    break
            if insert:
                freqs_sorted.insert(i, ts_type)
            else:
                freqs_sorted.append(ts_type)
    return [str(tt) for tt in freqs_sorted]

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
    lst = [ts_type]
    lst.extend(ts_types)
    return sort_ts_types(lst)[0]

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

def _check_stats_merge(statlist, var_name, pref_attr, fill_missing_nan):
    has_errs = False
    is_3d = []
    stats = []
    for stat in statlist:
        if not var_name in stat:
            raise DataCoverageError('All input stations must contain {} data'
                                    .format(var_name))
        elif pref_attr is not None and not pref_attr in stat:
            raise MetaDataError('Cannot sort station relevance by attribute {}. '
                                'At least one of the input stations does not '
                                'contain this attribute'.format(pref_attr))
        elif not isinstance(stat[var_name], pd.Series):
            stat._to_ts_helper(var_name)
        # this will raise MetaDataError or TemporalResolutionError if there is
        # an unresolvable issue with sampling frequency
        stat.get_var_ts_type(var_name)

        is_3d.append(stat.check_if_3d(var_name))

        if var_name in stat.data_err:
            has_errs = True

        stats.append(stat)
    if np.any(is_3d):
        if not np.all(is_3d):
            raise ValueError('Merge error: some of the input stations contain '
                             'altitude info (suggesting profile data), others '
                             'not.')
        is_3d = True
    else:
        is_3d = False
    return (stats, is_3d, has_errs)

def merge_station_data(stats, var_name, pref_attr=None,
                       sort_by_largest=True, fill_missing_nan=True,
                       add_meta_keys=None):
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
    add_meta_keys : str or list, optional
        additional non-standard metadata keys that are supposed to be
        considered for merging.
    """
    if isinstance(var_name, list):
        if len(var_name) > 1:
            raise NotImplementedError('Merging of multivar data not yet possible')
        var_name = var_name[0]

    stats, is_3d, has_errs = _check_stats_merge(stats,var_name,pref_attr,fill_missing_nan)
    # ToDo: data_err is not handled at the moment for 2D data, needs r
    # revision and should be done in StationData.merge, also 3D vs 2D
    # should be handled by StationData directly...
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
            merged.merge_other(stat, var_name, add_meta_keys=add_meta_keys)
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
            if i == 0:
                merged = stat
            else:
                merged.merge_meta_same_station(stat,
                                               add_meta_keys=add_meta_keys)

            _data[:, i] = np.interp(vert_grid, stat['altitude'],
                                    stat[var_name].values)

            if has_errs:
                try:
                    _data_err[:, i] = np.interp(vert_grid,
                                                stat['altitude'],
                                                stat.data_err[var_name])
                except Exception:
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

def make_datetime_index(start, stop, freq):
    """Make pandas.DatetimeIndex for input specs

    Note
    ----
    If input frequency is specified in `PANDAS_RESAMPLE_OFFSETS`, an offset
    will be added (e.g. 15 days for monthly data).

    Parameters
    ----------
    start
        start time
    stop
        stop time
    freq
        frequency

    Returns
    -------
    DatetimeIndex
    """
    if not isinstance(start, pd.Timestamp):
        start = to_pandas_timestamp(start)
    if not isinstance(stop, pd.Timestamp):
        stop = to_pandas_timestamp(stop)

    freq, loffset = _get_pandas_freq_and_loffset(freq)
    idx = pd.date_range(start=start, end=stop, freq=freq)
    if loffset is not None:
        idx = idx + pd.Timedelta(loffset)
    return idx

def calc_climatology(s, start, stop, min_count=None,
                     set_year=None, resample_how='mean'):
    """Compute climatological timeseries from pandas.Series

    Parameters
    ----------
    s : pandas.Series
        time series data
    start : numpy.datetime64 or similar
        start time of data used to compute climatology
    stop : numpy.datetime64 or similar
        start time of data used to compute climatology
    mincount_month : int, optional
        minimum number of observations required per aggregated month in
        climatological interval. Months not meeting this requirement will be
        set to NaN.
    set_year : int, optional
        if specified, the output data will be assigned the input year. Else
        the middle year of the climatological interval is used.
    resample_how : str
        string specifying how the climatological timeseries is to be
        aggregated

    Returns
    -------
    DataFrame
        dataframe containing climatological mean and median timeseries as
        well as columns std and count
    """
    if not isinstance(start, pd.Timestamp):
        start, stop = start_stop(start, stop)
    sc = s[start:stop]
    sc.dropna(inplace=True)

    if len(sc) == 0:
        raise ValueError('Cropping input time series in climatological '
                         'interval resulted in empty series')
    if set_year is None:
        set_year = int(start.year + (stop.year-start.year) / 2) + 1

    df = pd.DataFrame(sc)
    df['month'] = df.index.month

    clim = df.groupby('month').agg([resample_how, 'std','count'])

    #clim.columns = clim.columns.droplevel(0)
    clim.columns = ['data', 'std', 'numobs']
    idx = [np.datetime64('{}-{:02d}-15'.format(set_year, x)) for x in
           clim.index.values]
    clim.set_index(pd.DatetimeIndex(idx), inplace=True)
    if min_count is not None:
        mask = clim['numobs'] < min_count
        clim['data'][mask] = np.nan
        #mean[num < min_num_obs] = np.nan
    return clim

def resample_timeseries(ts, freq, how='mean', min_num_obs=None):
    """Resample a timeseries (pandas.Series)

    Parameters
    ----------
    ts : Series
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
    resampler = ts.resample(freq)#, loffset=loffset)
    if min_num_obs is None:
        data = resampler.agg(how)
    else:
        df = resampler.agg([how, 'count'])
        invalid = df['count'] < min_num_obs
        data = df[how]
        if np.any(invalid):
            data[invalid] = np.nan

    #print(freq, min_num_obs, how)
    if loffset is not None:
        data.index = data.index + pd.Timedelta(loffset)
    return data

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
    pd_freq=to.to_pandas_freq()
    invalid = None
    if min_num_obs is not None:
        if not pd_freq in XARR_TIME_GROUPERS:
            raise ValueError('Cannot infer xarray grouper for ts_type {}'
                             .format(to.val))
        #gr = XARR_TIME_GROUPERS[pd_freq]
        # 2D mask with shape of resampled data array
        #invalid = arr.groupby('time.{}'.format(gr)).count(dim='time') < min_num_obs
        invalid = arr.resample(time=pd_freq).count(dim='time') < min_num_obs

    freq, loffset = _get_pandas_freq_and_loffset(freq)
    resampler = arr.resample(time=pd_freq, loffset=loffset)
    try:
        aggfun = getattr(resampler, how)
    except AttributeError:
        raise ResamplingError('Invalid aggregator {} for temporal resampling '
                              'of DataArray...'.format(how))
    arr = aggfun(dim='time')

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
            if not ma.isclose(v, meta2[k], rel_tol=num_rtol):
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
    """Convert input to instance of :class:`pandas.Timestamp`

    Parameters
    ----------
    value
        input value that is supposed to be converted to time stamp

    Returns
    --------
    pandas.Timestamp
    """
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
    except Exception:
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
            subt_sec = False
            if isnumeric(stop):
                subt_sec = True
            stop = to_pandas_timestamp(stop)
            if subt_sec:
                stop = stop - pd.Timedelta(1, 's')
        except pd.errors.OutOfBoundsDatetime:
            stop = _check_climatology_timestamp(stop)
    return (start, stop)

def datetime2str(time, ts_type=None):
    from pyaerocom import const

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
    if isinstance(value, str) and len(value) == 8:
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
    except Exception:
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
        dt = np.asarray(np.asarray(times), dtype='timedelta64[{}]'.format(tstr))
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
        constraints.append(get_lon_rng_constraint(*lon_range, meridian_centre))
    if lat_range is not None:
        constraints.append(get_lat_rng_constraint(*lat_range))
    if time_range is not None:
        constraints.append(get_time_rng_constraint(*time_range))
    if len(constraints) > 0:
        c = constraints[0]
        for cadd in constraints[1:]:
            c = c & cadd
    return c

def get_lat_rng_constraint(low, high):
    """Create latitude constraint based on input range

    Parameters
    ----------
    low : float or int
        lower latitude coordinate
    high : float or int
        upper latitude coordinate

    Returns
    -------
    iris.Constraint
        the corresponding iris.Constraint instance

    """
    return iris.Constraint(latitude=lambda v: low <= v <= high)

def get_lon_rng_constraint(low, high, meridian_centre=True):
    """Create longitude constraint based on input range

    Parameters
    ----------
    low : float or int
        left longitude coordinate
    high : float or int
        right longitude coordinate
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
    """
    if low == high:
        raise ValueError("the specified values are equal")
    elif low > high:
        raise ValueError("Left coordinate must exceed right coordinate")
    if meridian_centre:
        low, high = (low+180)%360-180, (high+180)%360-180
    else:
        low, high = low%360, high%360
    if low > high:
        msg = ("Cannot crop over right border of longitude range")
        raise LongitudeConstraintError(msg)
    return iris.Constraint(longitude=lambda v: low <= v <= high)

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

    idx = make_datetime_index(2010, 2011, 'hourly')
    print(get_lowest_resolution('yearly', 'daily', 'monthly'))
    print(get_highest_resolution('yearly', 'daily', 'monthly'))

    print(infer_time_resolution([np.datetime64('2010-01-01'),
                                 np.datetime64('2010-01-02'),
                                 np.datetime64('2010-01-05'),
                                 np.datetime64('2010-10-15')]))

    print(varlist_aerocom(['od550aer', 'od550csaer']))

    rng = (30, 60)
    get_lon_rng_constraint(*rng, False)