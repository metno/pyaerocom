#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General helper methods for the pyaerocom library.
"""
import iris
from iris import coord_categorisation
import pandas as pd
import numpy as np
from pyaerocom.exceptions import LongitudeConstraintError
from cf_units import Unit
from datetime import MINYEAR, datetime, date

# The following import was removed and the information about available unit 
# strings was copied from the netCDF4 module directly here
# from netCDF4 import (microsec_units, millisec_units, sec_units, min_units,
#                     hr_units, day_units)
# from netCDF4._netCDF4 import _dateparse
microsec_units = ['microseconds', 'microsecond', 'microsec', 'microsecs']
millisec_units = ['milliseconds', 'millisecond', 'millisec', 'millisecs']
sec_units = ['second', 'seconds', 'sec', 'secs', 's']
min_units = ['minute', 'minutes', 'min', 'mins']
hr_units = ['hour', 'hours', 'hr', 'hrs', 'h']
day_units = ['day', 'days', 'd']

#
# Start of the gregorian calendar
# adapted from here: https://github.com/Unidata/cftime/blob/master/cftime/_cftime.pyx   
GREGORIAN_BASE = datetime(1582, 10, 15)

_STR_TO_IRIS = dict(count       = iris.analysis.COUNT,
                    gmean       = iris.analysis.GMEAN, 
                    hmean       = iris.analysis.HMEAN,
                    max         = iris.analysis.MAX, 
                    mean        = iris.analysis.MEAN,
                    median      = iris.analysis.MEDIAN,
                    nearest     = iris.analysis.Nearest)

IRIS_AGGREGATORS = {'hourly'    :   coord_categorisation.add_hour,
                    'daily'     :   coord_categorisation.add_day_of_year,
                    'monthly'   :   coord_categorisation.add_month_number,
                    'yearly'    :   coord_categorisation.add_year} 

# some helper dictionaries for conversion of temporal resolution
TS_TYPE_TO_PANDAS_FREQ = {'hourly'  :   'H',
                          '3hourly' :   '3H',
                          'daily'   :   'D',
                          'monthly' :   'MS', #Month start !
                          'yearly'  :   'Y'}

# frequency strings 
TS_TYPE_TO_NUMPY_FREQ =  {'hourly'  :   'h',
                          '3hourly' :   '3h',
                          'daily'   :   'D',
                          'monthly' :   'M', #Month start !
                          'yearly'  :   'Y'}
 
def str_to_iris(key):
    """Mapping function that converts strings into iris analysis objects
    
    Please see dictionary ``_STR_TO_IRIS`` in this module for valid definitions
    
    Parameters
    ----------
    key : str
        key of :attr:`_STR_TO_IRIS` dictionary
        
    Returns
    -------
    obj
        corresponding iris analysis object (e.g. Aggregator, method)
    """
    key = key.lower()
    if not key in _STR_TO_IRIS:
        raise KeyError("No iris.analysis object available for key %s, please "
                       "choose from %s" %(key, _STR_TO_IRIS.keys()))
    val = _STR_TO_IRIS[key]
    if callable(val):
        return val()
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
    if isinstance(value, str):
        if not len(value, 8):
            raise ValueError('Need string in format YYYYMMDD')
        return value
    elif isinstance(value, np.datetime64):
        value = value.astype(datetime)
    elif isinstance(value, pd.Timestamp):
        value = value.to_pydatetime()
    if isinstance(value, datetime):
        return datetime.strftime(value, "%Y%m%d")
    raise ValueError('Invalid input, need str, datetime, numpy.datetime64 or '
                     'pandas.Timestamp')
    
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
        return basedate + np.asarray(times, dtype="timedelta64[%s]" %tstr)
    else:
        return np.asarray([np.datetime64(t) for t in cfunit.num2date(times)])

def get_constraint(var_names=None, lon_range=None, lat_range=None, 
                   time_range=None, meridian_centre=True):
    """Function that creates an :class:`iris.Constraint` based on input
    
    Note
    ----
    Please be aware of the definition of the longitudes in your data when 
    cropping within the longitude dimension. The longitudes in your data may be 
    defined either from **-180 <= lon <= 180** (pyaerocom standard) or from 
    **0 <= lon <= 360**. In the former case (-180 _> 180) you can leave the 
    additional input parameter ``meridian_centre=True`` (default). In this
    case, if you want to crop over the border of the array (e.g. from Australia 
    to North America),
    
    Parameters
    ----------
    var_names : :obj:`str` or :obj:`list`, optional
        variable name or list of variable names. Note that if multiple
        variables are provided in a list
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
    >>> c = get_constraint(var_names=meta_info["var_name"], 
    ...                    lon_range=(50, 150), 
    ...                    lat_range=(20, 60), 
    ...                    time_range=("%s-02-05" %year, "%s-02-25" %year))
    >>> cube_crop = cubes.extract(c)[0]
    >>> cube_crop.shape
    (21, 40, 100)
    """
    constraints = []
    if var_names is not None:
        if isinstance(var_names, str):
            var_names = [var_names]
        cond = lambda c: c.var_name in var_names
        constraints.append(iris.Constraint(cube_func=cond))
    if lon_range is not None:
        constraints.append(get_lon_constraint(lon_range, meridian_centre))    
    if lat_range is not None:
        constraints.append(get_lat_constraint(lat_range))
    if time_range is not None:
        constraints.append(get_time_constraint(*time_range))
    if len(constraints) > 0:
        c = constraints[0]
        for cadd in constraints[1:]:
            c = c & cadd
    return c

def get_lat_constraint(lat_range):
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

def get_lon_constraint_buggy(lon_range, meridian_centre=True):        
    """Create longitude constraint based on input range
    
    Note
    ----
    In this definition, the constraint is combined in case the border of the
    longitude array is crossed. Apparently, that does not work properly and 
    it is therefore recommended to use :func:`iris.cube.Cube.intersection` 
    instead (which is also reimplemented in :class:`pyaerocom.GriddedData`).
    If you use :func:`get_lon_constraint` it will detect if there is a border 
    crossing, and if so, it will raise an error (that suggests to use the
    intersection method instead).
    
    Parameters
    ----------
    lon_range : tuple
        2-element tuple containing from left -> right end of range
    meridian_centre : bool
        specifies the coordinate definition range of longitude array. If True, 
        then -180 -> 180 is assumed, else 0 -> 360
    
    Returns
    -------
    iris.Constraint
        the corresponding iris.Constraint instance 
    """
    left, right = lon_range
    if left == right:
        raise ValueError("the specified values are equal")
    if meridian_centre:
        left, right = (left+180)%360-180, (right+180)%360-180
        r_end, l_end = 180, -180
    else:
        left, right = left%360, right%360
        r_end, l_end = 360, 0
    if left < right:
        return iris.Constraint(longitude=lambda v: left < v < right)
    else:
        cleft = iris.Constraint(longitude=lambda v: left <= v <= r_end)
        cright = iris.Constraint(longitude=lambda v: l_end <= v <= right)
        return (cleft or cright)
    
def get_lon_constraint(lon_range, meridian_centre=True):        
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
    >>> c = get_lon_constraint(lon_range=(170, -160), meridian_centre=True)
    Traceback (most recent call last):
     ...
    ValueError: Left coordinate must exceed right coordinate
    >>> c = get_lon_constraint(lon_range=(-30, 30), meridian_centre=True)
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

def get_time_constraint(start_time, stop_time):
    """Create iris.Constraint for data extraction along time axis
    
    Parameters
    ----------
    start_time : :obj:`Timestamp` or :obj:` str`
        start time of desired subset. If string, it must be convertible 
        into :class:`pandas.Timestamp` (e.g. "2012-1-1")
    stop_time : :obj:`Timestamp` or :obj:` str`
        start time of desired subset. If string, it must be convertible 
        into :class:`pandas.Timestamp` (e.g. "2012-1-1")
    
    Returns
    -------
    iris.Constraint
        iris Constraint instance that can, e.g., be used as input for
        :func:`pyaerocom.griddeddata.GriddedData.extract`
    """
    if not isinstance(start_time, pd.Timestamp):
        start_time = pd.Timestamp(start_time)
    if not isinstance(stop_time, pd.Timestamp):
        stop_time = pd.Timestamp(stop_time)
        
    t_lower = iris.time.PartialDateTime(year=start_time.year,
                                        month=start_time.month,
                                        day=start_time.day)
    t_upper = iris.time.PartialDateTime(year=stop_time.year,
                                        month=stop_time.month,
                                        day=stop_time.day)
    
    return iris.Constraint(time=lambda cell: t_lower <= cell <= t_upper)

def to_time_series_griesie(data, lats, lons, times, var_name=['zdust'],**kwargs):
    """small helper routine to convert data from the object
    pyaerocom.io.ReadGridded.interpolate to the obs data dictionary
    containing the pandas timeseries

    FOR TESTING ONLY!"""

    import pandas as pd

    result = []
    for i in range(len(lats)):
        _dict = {}
        _dict['latitude']=lats[i]
        _dict['longitude']=lons[i]
        for var in var_name:
            _dict[var] = pd.Series(data[:, i, i],index=times)
        result.append(_dict)
    return result

# TODO: Review and move into test-suite
def griesie_dataframe_testing(model_data, obs_data, startdate, enddate):
    """testing routine to create a scatterplot using a pandas data frame"""

    import pyaerocom.io as pio
    import pyaerocom as pa
    import matplotlib.pyplot as plt
    import pandas as pd

    obs_data_as_series = obs_data.to_timeseries(start_date=startdate, 
                                                end_date=enddate, 
                                                freq='D')
    obs_lats = obs_data.latitude
    obs_lons = obs_data.longitude
    obs_lats=[obs_data_as_series[i]['latitude'] for i in range(len(obs_data_as_series))]
    obs_lons=[obs_data_as_series[i]['longitude'] for i in range(len(obs_data_as_series))]
    obs_names=[obs_data_as_series[i]['station_name'] for i in range(len(obs_data_as_series))]
    model_station_data = model_data.interpolate([("latitude", obs_lats),("longitude", obs_lons)])
    times_as_dt64 = pa.helpers.cftime_to_datetime64(model_station_data.time)
    model_data_as_series = pa.helpers.to_time_series_griesie(model_station_data.grid.data, obs_lats, obs_lons, times_as_dt64)
    print(obs_lats)
    # # single station
    # df = pd.DataFrame(obs_data_as_series[1]['zdust'], columns=['obs'])
    # df['model'] = model_data_as_series[1]['zdust']
    # # remove points where any of the df is NaN
    # #df = df.dropna(axis=0, how='any')
    # correlation = df.corr(method='pearson')
    # plot = df.plot.scatter('obs','model')
    # df.show()

# TODO: review and move into test-suite
def griesie_xarray_to_timeseries(xarray_obj, obs_lats, obs_lons, vars_to_retrieve=['od550_aer'], debug_mode = False):
    """test routine to colocate xarray object"""

    import pandas as pd
    import numpy as np
    result=[]
    if not debug_mode:
        max_index = len(obs_lats)
    else:
        max_index = 20

    for index in range(max_index):
        print(index)
        xarray_col = xarray_obj.sel(latitude=obs_lats[index], longitude=obs_lons[index], method='nearest')
        _dict = {}
        # _dict['latitude'] = obs_lats[index]
        # _dict['longitude'] = obs_lons[index]
        _dict['latitude'] = np.float_(xarray_col['latitude'])
        _dict['longitude'] = np.float_(xarray_col['longitude'])

        #data_frame = xarray_col.to_dataframe()
        for var in vars_to_retrieve:
            # _dict[var] = pd.Series(data_frame[var])
            # _dict[var] = xarray_col[var].to_series()
            _dict[var] = pd.Series(xarray_col[var], index=xarray_col['time'], dtype=np.float_)

        result.append(_dict)
    return result


if __name__=="__main__":
    
    
    import doctest
    import warnings
    warnings.simplefilter("ignore")
    doctest.testmod()
    from pyaerocom.io.testfiles import get
    from pyaerocom import GriddedData
    files = get()
    data = GriddedData(files['models']['aatsr_su_v4.3'], var_name="od550aer")
    lons = data.grid.coord("longitude")
    try:
        get_lon_constraint(lon_range=(170, -160), meridian_centre=True)
    except ValueError:
        print("Expected behaviour")

    from iris import load
    cubes = load(files['models']['aatsr_su_v4.3'])
    lons = cubes[0].coord("longitude").points
    meridian_centre = True if lons.max() > 180 else False
    c = get_constraint(var_names="od550aer",
                       lon_range=(50, 150),
                       lat_range=(20, 60),
                       time_range=("2008-02-01", "2008-02-05"))

    cube_crop = cubes.extract(c)[0]

                           


