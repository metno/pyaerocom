#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper methods for the pyaerocom library
"""
from iris import Constraint
from iris.time import PartialDateTime

def get_constraint(var_names=None, lon_range=None, lat_range=None, 
                   time_range=None, lon_def=(-180, 180)):
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
    lon_def : tuple
        2-element tuple specifying over which range the longitudes are defined.
        Use (-180, 180) for -180 <= lon <= 180 
        and (0, 360) for 0 <= lon <= 360
        
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
    elif lon_range is not None:
        constraints.append(get_lon_constraint(lon_range, lon_def))    
    return 

def get_lon_constraint(lon_range, lon_def=(0, 360)):
    """Create iris.Constraint for data extraction along longitude axis
    
    Note
    ----
    Please provide input for lon_range in -180 <= lon <= 180 deg coordinate 
    system. We will take care of that, even if your data is defined on 
    (0, 360) coordinate system. 
    
    Parameters
    ----------
    lon_range : :obj:`tuple`, optional
        2-element tuple containing longitude range for cropping
        Example input to crop around meridian: `lon_range=(-30, 30)`
    """
    if not len(lon_range) == 2:
        raise ValueError("Please provide a 2-element tuple to specify "
                         "longitude range")
    if not all([-180 <= x <= 180 for x in lon_range]):
        raise ValueError("Please provide longitudes for definition range "
                         "-180 <= lon <= 180")
    if lon_def == (0, 360):
        raise NotImplementedError        
    
def get_time_constraint(start_time, stop_time):
    """Create iris.Constraint for data extraction along time axis
    
    Parameters
    ----------
    start_time : Timestamp
        start time of desired subset
    stop_time : Timestamp
        stop time of desired subset
    
    Returns
    -------
    Constraint
        iris Constraint instance that can, e.g., be used as input for
        :func:`pyaerocom.modeldata.ModelData.extract` 
    """
    t_lower = PartialDateTime(year=start_time.year,
                              month=start_time.month,
                              day=start_time.day)
    t_upper = PartialDateTime(year=stop_time.year,
                              month=stop_time.month,
                              day=stop_time.day)
    
    return Constraint(time=lambda cell: t_lower <= cell <= t_upper)

