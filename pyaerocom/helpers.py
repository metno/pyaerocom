#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper methods for the pyaerocom library
"""
from iris import Constraint
from iris.time import PartialDateTime
from pandas import Timestamp
from warnings import warn

def get_constraint(var_names=None, lon_range=None, lat_range=None, 
                   time_range=None, meridian_centre=True):
    """Function that creates an :class:`iris.Constraint` based on input
    
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
    eridian_centre : bool
        specifies the coordinate definition range of longitude array. If True, 
        then -180 -> 180 is assumed, else 0 -> 360
        
    Returns
    -------
    Constraint
        the combined constraint from all valid input parameters
    
    Raises
    ------
    
    Example
    -------
    >>> from pyaerocom.helpers import get_constraint
    >>> c = get_constraint(var_names="od550aer", 
                           lon_range=(-20, 20), 
                           lat_range=(20, 60), 
                           time_range=("2010-02-01", "2012-02-01"),
                           lon_def=(-180, 180))
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
        constraints.append(get_time_constraint(time_range))
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

def get_lon_constraint(lon_range, meridian_centre=True):        
    """Create longitude constraint based on input range
    
    Note
    ----
    This approach does not work (see `this script <https://github.com/metno/
    pyaerocom/blob/master/test_dev/test_loncrop_cube.py>`__), even though 
    suggested `here <https://groups.google.com/
    forum/#!topic/scitools-iris/DP7w1dWH6hI>~__
    
    For now, the recommendation is to NOT use iris Constraints for cropping 
    longitude (only if you are really sure that you are not crossing a border)
    but rather use the Cube method `intersection`.
    
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
    warn("BUGGY! PLEASE DO NOT USE")
    left, right = lon_range
    print("l, r (input): %s, %s" %(left, right))
    if left == right:
        raise ValueError("the specified values are equal")
    if meridian_centre:
        left, right = (left+180)%360-180, (right+180)%360-180
        print("l, r (converted): %s, %s" %(left, right))
        if left < right:
            return Constraint(longitude=lambda v: left <= v <= right)
        print('Changing to 0 -> 360 notation due to border crossing')
        print("%s -> 180 and -180 -> %s" %(left, right))
        c = Constraint(longitude=lambda v: left < v < 180 or -180 < v < right)
        return c
    #meridian_centre is False
    left, right = left%360, right%360
    print("l, r (converted): %s, %s" %(left, right))
    if left < right:
        return Constraint(longitude=lambda v: left < v < right)
    print("%s -> 360 and 0 -> %s" %(left, right))
    cleft = Constraint(longitude=lambda v: left <= v <= 360)
    cright = Constraint(longitude=lambda v: 0 <= v <= right)
    return (cleft or cright)

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


