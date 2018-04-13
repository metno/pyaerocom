#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General helper methods for the pyaerocom library.
"""
from iris import Constraint
from iris.time import PartialDateTime
from pandas import Timestamp
from pyaerocom.exceptions import LongitudeConstraintError

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
    Constraint
        the combined constraint from all valid input parameters
    
    Examples
    --------
    The following example shows how to crop over the meridian
    
    >>> from pyaerocom.helpers import get_constraint
    >>> from pyaerocom.io.utils import FileConventionRead
    >>> from iris import load
    >>> from pyaerocom.test_files import get
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
        constraints.append(Constraint(cube_func=cond))
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
    Constraint
        the corresponding iris.Constraint instance
        
    """
    return Constraint(latitude=lambda v: lat_range[0] <= v <= lat_range[1])

def get_lon_constraint_buggy(lon_range, meridian_centre=True):        
    """Create longitude constraint based on input range
    
    Note
    ----
    In this definition, the constraint is combined in case the border of the
    longitude array is crossed. Apparently, that does not work properly and 
    it is therefore recommended to use :func:`iris.cube.Cube.intersection` 
    instead (which is also reimplemented in :class:`pyaerocom.ModelData`). 
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
    Constraint
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
        return Constraint(longitude=lambda v: left < v < right)
    else:
        cleft = Constraint(longitude=lambda v: left <= v <= r_end)
        cright = Constraint(longitude=lambda v: l_end <= v <= right)
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
    Constraint
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
    >>> from pyaerocom.test_files import get
    >>> from pyaerocom import ModelData
    >>> files = get()
    >>> data = ModelData(files['models']['aatsr_su_v4.3'], var_name="od550aer")
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
    return Constraint(longitude=lambda v: left <= v <= right)

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
    Constraint
        iris Constraint instance that can, e.g., be used as input for
        :func:`pyaerocom.modeldata.ModelData.extract` 
    """
    if not isinstance(start_time, Timestamp):
        start_time = Timestamp(start_time)
    if not isinstance(stop_time, Timestamp):
        stop_time = Timestamp(stop_time)
        
    t_lower = PartialDateTime(year=start_time.year,
                              month=start_time.month,
                              day=start_time.day)
    t_upper = PartialDateTime(year=stop_time.year,
                              month=stop_time.month,
                              day=stop_time.day)
    
    return Constraint(time=lambda cell: t_lower <= cell <= t_upper)

if __name__=="__main__":
    import doctest
    doctest.testmod()
    from pyaerocom.test_files import get
    from pyaerocom import ModelData
    files = get()
    data = ModelData(files['models']['aatsr_su_v4.3'], var_name="od550aer")
    lons = data.grid.coord("longitude")
    try:
        get_lon_constraint(lon_range=(170, -160), meridian_centre=True)
    except ValueError:
        print("Expected beahviour")
    
    from iris import load
    from pyaerocom.test_files import get
    cubes = load(files['models']['aatsr_su_v4.3'])
    lons = cubes[0].coord("longitude").points
    meridian_centre = True if lons.max() > 180 else False
    c = get_constraint(var_names="od550aer", 
                       lon_range=(50, 150), 
                       lat_range=(20, 60), 
                       time_range=("2010-02-01", "2012-02-01"))
    cube_crop = cubes.extract(c)[0]
    cube_crop.shape
                           


