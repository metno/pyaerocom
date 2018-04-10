#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file could contain classes representing ModelData
"""

from collections import OrderedDict as od
from iris.time import PartialDateTime
from iris import Constraint
from iris.cube import Cube
from pandas import Timestamp
#from abc import ABCMeta, abstractmethod

from pyaerocom._glob import SUPPORTED_DATA_TYPES_MODEL

class ModelData:
    """Base class representing model data
    
    Attributes
    ----------
    data 
        underlying data type (hopefully :class:`iris.cube.Cube` in most cases)
    suppl_info : dict
        dictionary containing supplementary information about this data
        object (these may be attributes that are not already stored within
        the metadata representation of the underlying data object)
        
    .. todo::
        
        Ship relevant methods and attributes from underlying Cube 
        representation (e.g. `var_name, coords...`)
    """
    _grid = None
    def __init__(self, grid, verbose=True, **suppl_info):
        #super(ModelData, self).__init__(*args, **kwargs)
        self.grid = grid
        self.verbose = verbose
        self.suppl_info = od(from_files = [],
                             model_id = "")
        
        for k, v in suppl_info.items():
            if k in self.suppl_info:
                self.suppl_info[k] = v
                
    @property
    def grid(self):
        """Underlying grid data object"""
        return self._grid
    
    @grid.setter
    def grid(self, value):
        if not type(value) in SUPPORTED_DATA_TYPES_MODEL:
            raise TypeError("Grid data format %s is not supported" 
                            %type(value))
        self._grid = value
    
    @property
    def var_name(self):
        """Name of variable in grid"""
        if not self.is_cube:
            raise NotImplementedError("Attribute var_name is not available...")
        return self.grid.var_name
            
    @property 
    def model_id(self):
        """ID of model to which data belongs"""
        return self.suppl_info["model_id"]
        
    @property
    def is_cube(self):
        """Checks if underlying data type is of type :class:`iris.cube.Cube`"""
        return True if isinstance(self.grid, Cube) else False
    
    def crop(self, lon_range=None, lat_range=None, 
             time_range=None):
        """High level function that applies cropping along multiple axes
        
        Note
        ----
            1. For cropping of longitudes and latitudes, the method 
            :func:`iris.cube.Cube.intersection` is used since it automatically 
            accepts and understands longitude input based on definition 
            0 <= lon <= 360 as well as for -180 <= lon <= 180
            2. Time extraction may be provided directly as index or in form of
            :class:`pandas.Timestamp` objects. 
            
        Parameters
        ----------
        lon_range : :obj:`tuple`, optional
            2-element tuple containing longitude range for cropping. If None, 
            the longitude axis remains unchanged. 
            Example input to crop around meridian: `lon_range=(-30, 30)`
        lat_range : :obj:`tuple`, optional
            2-element tuple containing latitude range for cropping. If None, 
            the latitude axis remains unchanged
        time_range : :obj:`tuple`, optional
            2-element tuple containing time range for cropping. Allowed data
            types for specifying the times are 
            
                1. a combination of 2 :class:`pandas.Timestamp` instances or 
                2. a combination of two strings that can be directly converted\
                into :class:`pandas.Timestamp` instances (e.g.\
                `time_range=("2010-1-1", "2012-1-1")`) or
                3. directly a combination of indices (:obj:`int`). 
            
            If None, the time axis remains unchanged.
        
        Returns
        -------
        ModelData
            new data object containing cropped grid
        """
        if not self.is_cube:
            raise NotImplementedError("This feature is only available if the"
                                      "underlying data is of type iris.Cube")
        if lon_range is not None and lat_range is not None:
            data = self.grid.intersection(longitude=lon_range, 
                                          latitude=lat_range)
        elif lon_range is not None and lat_range is None:
            data = self.grid.intersection(longitude=lon_range)
        elif lon_range is None and lat_range is not None:
            data = self.grid.intersection(latitude=lat_range)
        else:
            data = self.grid
        if time_range is None:
            return ModelData(data, **self.suppl_info)
        else:
            if all(isinstance(x, str) for x in time_range):
                time_range = (Timestamp(time_range[0]),
                              Timestamp(time_range[1]))
            if all(isinstance(x, Timestamp) for x in time_range):
                if self.verbose:
                    print("Cropping along time axis based on Timestamps")
                data = data.extract(self.get_time_constraint(*time_range))
            elif all(isinstance(x, int) for x in time_range):
                if self.verbose:
                    print("Cropping along time axis based on indices")
                data = data[time_range[0]:time_range[1]]
        return ModelData(data, **self.suppl_info)
        
    def get_time_constraint(self, start_time, stop_time):
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
            :func:`extract`
        """
        t_lower = PartialDateTime(year=start_time.year,
                                  month=start_time.month,
                                  day=start_time.day)
        t_upper = PartialDateTime(year=stop_time.year,
                                  month=stop_time.month,
                                  day=stop_time.day)
        
        return Constraint(time=lambda cell: t_lower <= cell <= t_upper)
    
    #redifined methods from iris.Cube class
    
    def extract(self, constraint):
        """Extract subset
        
        Note
        ----
        Only works if underlying grid data type is :class:`iris.cube.Cube`
        
        Parameters
        ----------
        constraint : iris.Constraint
            constraint that is to be applied
            
        Returns
        -------
        ModelData
            new data object containing cropped data
        """
        if not self.is_cube:
            raise NotImplementedError("This feature is only available if the"
                                      "underlying data is of type iris.Cube")
        data_crop = self.grid.extract(constraint)
        
        return ModelData(data_crop, **self.suppl_info)
    
    def intersection(self, *args, **kwargs):
        """Ectract subset using :func:`iris.cube.Cube.intersection` 
        
        See `here for details <http://scitools.org.uk/iris/docs/v1.9.0/html/iris/iris/cube.html#iris.cube.Cube.intersection>`__
        related to method and input parameters.
        
        Note
        ----
        Only works if underlying grid data type is :class:`iris.cube.Cube`
        
        Parameters
        ----------
        *args
            non-keyword args
        **kwargs
            keyword args
        
        Returns
        -------
        ModelData
            new data object containing cropped data
        """
        if not self.is_cube:
            raise NotImplementedError("This feature is only available if the"
                                      "underlying data is of type iris.Cube")
        data_crop = self.grid.intersection(*args, **kwargs)
        
        return ModelData(data_crop, **self.suppl_info)
    
    def __str__(self):
        """For now, use string representation of underlying data"""
        return "pyaerocom.ModelData\nGrid data: %s" %self.grid.__str__()
    
    def __repr__(self):
        """For now, use representation of underlying data"""
        return "pyaerocom.ModelData\nGrid data: %s" %self.grid.__repr__()    