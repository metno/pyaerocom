#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file could contain classes representing ModelData
"""
from cf_units import num2date
from os.path import exists
from collections import OrderedDict as od
from iris import Constraint, load, load_cube
from iris.cube import Cube, CubeList
from pandas import Timestamp
from numpy import datetime64
from warnings import warn

from pyaerocom.glob import SUPPORTED_DATA_TYPES_MODEL, VERBOSE, ON_LOAD
from pyaerocom.helpers import get_time_constraint
from pyaerocom.region import Region


class ModelData:
    """Base class representing model data
    
    This class is largely based on the :class:`iris.Cube` object. However, this
    object comes with an expanded functionality for convenience. Some examples
    are:
        
        1. Class instantiation:
            :class:`iris.cube.Cube` instances are typically created using
            helper methods such as:
                
                1. :func:`iris.load` (returns :class:`iris.cube.CubeList`, i.e. 
                a list-like iterable object that contains instance of 
                :class:`Cube` objects, one for each variable) or 
                2. :func:`iris.load_cube` (which directly returns a 
                :class:`iris.cube.Cube` instance, and may be called with a 
                spec)
                
        2. Subsetting and extraction
            The iris interface is based on :class:`Constraint` objects that 
            may be defined for variable, time and longitude / latitude range
            and that can be combined simply using the `&`
    
    Attributes
    ----------
    grid
        underlying data type (hopefully :class:`iris.cube.Cube` in most cases)
    suppl_info : dict
        dictionary containing supplementary information about this data
        object (these may be attributes that are not already stored within
        the metadata representation of the underlying data object)
       
    Parameters
    ----------
    input : :obj:`str:` or :obj:`Cube`
        data input. Can be a single .nc file or a preloaded iris Cube.
    var_name : :obj:`str`, optional
        variable name that is extracted if `input` is a file path . Irrelevant
        if `input` is preloaded Cube

    Example
    -------
    >>> from pyaerocom.test_files import get
    >>> files = get()
    >>> data = ModelData(files['models']['aatsr_su_v4.3'], var_name="od550aer",
    ...                  verbose=False)
    >>> print(data.var_name)
    od550aer
    >>> print(type(data.longitude))
    <class 'iris.coords.DimCoord'>
    >>> print(data.longitude.points.min(), data.longitude.points.max())
    -179.5 179.5
    >>> print(data.latitude.points.min(), data.latitude.points.max())
    -89.5 89.5
    >>> print(data.time.points.min(), data.time.points.max())
    0.0 365.0
    >>> tstamps = data.time_stamps()
    >>> print(tstamps[0], tstamps[-1])
    2008-01-01 00:00:00 2008-12-31 00:00:00
    >>> data_cropped = data.crop(lat_range=(-60, 60), lon_range=(160, 180),
    ...                          time_range=("2008-02-01", "2008-02-15"))
    >>> print(data_cropped.shape)
    (15, 120, 20)
    """
    _grid = None
    _ON_LOAD = ON_LOAD
    def __init__(self, input, var_name=None, verbose=VERBOSE, **suppl_info):
        self.verbose = verbose
        self.suppl_info = od(from_files = [],
                             model_id = "Unknown")
        
        self.load_input(input, var_name)
        for k, v in suppl_info.items():
            if k in self.suppl_info:
                self.suppl_info[k] = v
           
    @property
    def longitude(self):
        """Longitudes of data"""
        if self.is_cube:
            return self.grid.coord("longitude")
        
    @longitude.setter
    def longitude(self, value):
        raise AttributeError("Longitudes cannot be changed, please check "
                             "underlying data type stored in attribute grid")
    
    @property
    def latitude(self):
        """Latitudes of data"""
        if self.is_cube:
            return self.grid.coord("latitude")
        
    @latitude.setter
    def latitude(self, value):
        raise AttributeError("Latitudes cannot be changed, please check "
                             "underlying data type stored in attribute grid")
        
    @property
    def time(self):
        """Time dimension of data"""
        if self.is_cube:
            return self.grid.coord("time")
        
    @time.setter
    def time(self, value):
        raise AttributeError("Time array cannot be changed, please check "
                             "underlying data type stored in attribute grid")
            
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
    def has_data(self):
        """True if grid data is available (:attr:`grid` =! None)
        
        Note
        ----
        Since so far, the only supported type is :class:`iris.cube.Cube`, this
        method simply returns :attr:`is_cube`.
        """
        return self.is_cube
    
    @property
    def is_cube(self):
        """Checks if underlying data type is of type :class:`iris.cube.Cube`"""
        return True if isinstance(self.grid, Cube) else False
    
    @property
    def shape(self):
        if not self.is_cube:
            raise NotImplementedError("Attribute shape is not available...")
        return self.grid.shape 
    
    def load_input(self, input, var_name=None):
        """Interprete and load input
        
        Parameters
        ----------
        input : :obj:`str:` or :obj:`Cube`
            data input. Can be a single .nc file or a preloaded iris Cube.
        var_name : :obj:`str`, optional
            variable name that is extracted if `input` is a file path . Irrelevant
            if `input` is preloaded Cube
        """
        if isinstance(input, str) and exists(input):
            if not isinstance(var_name, str):
                _var_names = []
                try:
                    ctemp = load(input)
                    if isinstance(ctemp, CubeList):
                        _var_names = [x.var_name for x in ctemp]
                        _addstr = ("The following variable names exist in "
                                   "input file: %s" %_var_names)
                except:
                    _addstr = ""
                            
                raise ValueError("Loading data from input file %s requires "
                                 "specification of a variable name using "
                                 "input parameter var_name. %s" %(input, _addstr))
            func = lambda c: c.var_name == var_name
            constraint = Constraint(cube_func=func)
            self.grid = load_cube(input, constraint) #instance of CubeList
            self.suppl_info["from_files"].append(input)
        elif isinstance(input, Cube):
            self.grid = input #instance of Cube
        if self._ON_LOAD["DEL_TIME_BOUNDS"]:
            self.grid.coord("time").bounds = None
        if self._ON_LOAD["SHIFT_LONS"]:
            self.check_and_regrid_lons()
    
    def time_stamps(self):
        """Convert time stamps into list of numpy datetime64 objects
        
        Returns
        -------
        list 
            list containing all time stamps as datetime64 objects 
        """
        try:
            import cf_units
            ts = self.time
            return [datetime64(t) for t in cf_units.num2date(ts.points, 
                                                             ts.units.name, 
                                                             ts.units.calendar)]
        except Exception as e:
            warn("Failed to convert time stamps using cf_units.date2num "
                 "Trying slower method via cells() method of time dimension")
            return [datetime64(t.point) for t in ts.cells()]       
    
    def check_and_regrid_lons(self):
        """Checks and corrects for if longitudes of :attr:`grid` are 0 -> 360
        
        Note
        ----
        This method checks if the maximum of the current longitudes array
        exceeds 180. Thus, it is not recommended to use this function after
        subsetting a cube, rather, it should be checked directly when the 
        file is loaded (cf. :func:`load_input`)
        
        Returns
        -------
        bool
            True, if longitudes were on 0 -> 360 and have been rolled, else
            False
        """
        if self.grid.coord("longitude").points.max() > 180:
            if self.verbose:
                print("Rolling longitudes to -180 -> 180 definition")
            self.grid = self.grid.intersection(longitude=(-180, 180))
        
        
        
    def crop(self, lon_range=None, lat_range=None, 
             time_range=None, region_id=None):
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
        region_id : :obj:`str`, optional
            string ID of pyaerocom default region. May be used instead of 
            ``lon_range`` and ``lat_range``, if these are unspecified.
            
        
        Returns
        -------
        ModelData
            new data object containing cropped grid
        """
        if not self.is_cube:
            raise NotImplementedError("This feature is only available if the"
                                      "underlying data is of type iris.Cube")
        if region_id is not None:
            try:
                r = Region(region_id)
                lon_range, lat_range = r.lon_range, r.lat_range
            except Exception as e:
                warn("Failed to access longitude / latitude range using "
                     "region ID %s. Error msg: %s" %(region_id, repr(e)))
                
        if lon_range is not None and lat_range is not None:
            data = self.grid.intersection(longitude=lon_range, 
                                          latitude=lat_range)
        elif lon_range is not None and lat_range is None:
            data = self.grid.intersection(longitude=lon_range)
        elif lon_range is None and lat_range is not None:
            data = self.grid.intersection(latitude=lat_range)
        else:
            data = self.grid
        if data is None:
            raise Exception
        if time_range is None:
            return ModelData(data, **self.suppl_info)
        else:
            if all(isinstance(x, str) for x in time_range):
                time_range = (Timestamp(time_range[0]),
                              Timestamp(time_range[1]))
            if all(isinstance(x, Timestamp) for x in time_range):
                if self.verbose:
                    print("Cropping along time axis based on Timestamps")
                time_constraint = self.get_time_constraint(*time_range)
                data = data.extract(time_constraint)
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
        return get_time_constraint(start_time, stop_time)
    
    #redefined methods from iris.Cube class
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
    
    def quickplot_map(self, time_idx=0, xlim=(-180, 180), ylim=(-90, 90),
                      **kwargs):
        """Make a quick plot onto a map
        
        Parameters
        ----------
        time_idx : int
            index in time to be plotted
        xlim : tuple
            2-element tuple specifying plotted longitude range
        ylim : tuple
            2-element tuple specifying plotted latitude range
        **kwargs
            additional keyword arguments passed to 
            :func:`pyaerocom.quickplot.plot_map`
        
        Returns
        -------
        fig
            matplotlib figure instance containing plot
        """
        from pyaerocom.plot.mapping import plot_map
        fig = plot_map(self.grid[time_idx], xlim, ylim, **kwargs)
        fig.axes[0].set_title("Model: %s, var=%s (%s)" 
                     %(self.model_id, self.var_name, 
                       self.time.cell(time_idx)))
        return fig
    
    def __str__(self):
        """For now, use string representation of underlying data"""
        return ("pyaerocom.ModelData: %s\nGrid data: %s" 
                %(self.model_id, self.grid.__str__()))
    
    def __repr__(self):
        """For now, use representation of underlying data"""
        return "pyaerocom.ModelData\nGrid data: %s" %self.grid.__repr__() 
    
if __name__=='__main__':
    from pyaerocom.test_files import get
    from matplotlib.pyplot import close
    
    close("all")
    files = get()
    data = ModelData(files['models']['aatsr_su_v4.3'], var_name="od550aer",
                     model_id='aatsr_su_v4.3')
    print(data.var_name)
    print(type(data.longitude))
    print(data.longitude.points.min(), data.longitude.points.max())
    print(data.latitude.points.min(), data.latitude.points.max())
    print(data.time.points.min(), data.time.points.max())
    tstamps = data.time_stamps()
    print(tstamps[0], tstamps[-1])
    
    data.longitude.circular = True
    cropped = data.crop(lon_range=(100, 170), lat_range=(-60, 60))
    print(cropped.shape)
    cropped.quickplot_map()
    
    other = ModelData(files["models"]["ecmwf_osuite"], 
                      var_name="od550aer", model_id="ECMWF_OSUITE")
    other.quickplot_map()
    ocropped = other.crop(lon_range=(100, 170), lat_range=(-60, 60))
    ocropped.quickplot_map()
    
    ocropped.quickplot_map(fix_aspect=2, vmin=.4, vmax=1.)
    ocropped.quickplot_map(vmin=0, vmax=1., c_over="r")
    
    try:
        ModelData(files["models"]["ecmwf_osuite"])
    except ValueError as e:
        warn(repr(e))
        

    import doctest
    doctest.testmod()
