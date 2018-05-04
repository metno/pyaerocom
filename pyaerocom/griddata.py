#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pyaerocom GridData class
"""
from os.path import exists
from copy import deepcopy
from collections import OrderedDict as od
from iris import Constraint, load, load_cube
from iris.cube import Cube, CubeList
from iris.analysis.cartography import area_weights
from iris.analysis import MEAN
from pandas import Timestamp
from warnings import warn
from numpy import nan

from pyaerocom import const
from pyaerocom.exceptions import DataExtractionError
from pyaerocom.helpers import (get_time_constraint, 
                               cftime_to_datetime64,
                               str_to_iris)

from pyaerocom.region import Region

class GridData(object):
    """Base class representing model data
    
    This class is largely based on the :class:`iris.Cube` object. However, this
    object comes with an expanded functionality for convenience, for instance, 
    netCDF files can directly be loaded in the :class:`GridData` object,
    whereas :class:`iris.cube.Cube` instances are typically created using
    helper methods such as
    
    1. :func:`iris.load` (returns 
    :class:`iris.cube.CubeList`, i.e. a list-like iterable object that contains 
    instances of :class:`Cube` objects, one for each variable) or 
    
    2. :func:`iris.load_cube` which directly returns a :class:`iris.cube.Cube` 
    instance and typically requires specification of a variable constraint.
    
    The :class:`GridData` object represents one variable in space and time, as
    well as corresponding meta information. Since it is based on the 
    :class:`iris.cube.Cube` it is optimised for netCDF files that follow the
    CF conventions and may not work for files that do not follow this standard.
       
    Parameters
    ----------
    input : :obj:`str:` or :obj:`Cube`
        data input. Can be a single .nc file or a preloaded iris Cube.
    var_name : :obj:`str`, optional
        variable name that is extracted if `input` is a file path . Irrelevant
        if `input` is preloaded Cube

    Example
    -------
    >>> from pyaerocom.io.testfiles import get
    >>> files = get()
    >>> data = GridData(files['models']['aatsr_su_v4.3'], var_name="od550aer",
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
    2008-01-01T00:00:00.000000 2008-12-31T00:00:00.000000
    >>> data_cropped = data.crop(lat_range=(-60, 60), lon_range=(160, 180),
    ...                          time_range=("2008-02-01", "2008-02-15"))
    >>> print(data_cropped.shape)
    (15, 120, 20)
    
    Attributes
    ----------
    grid
        underlying data type (hopefully :class:`iris.cube.Cube` in most cases)
    suppl_info : dict
        dictionary containing supplementary information about this data
        object (these may be attributes that are not already stored within
        the metadata representation of the underlying data object)
        
    """
    _grid = None
    _ON_LOAD = const.ON_LOAD
    def __init__(self, input=None, var_name=None, verbose=const.VERBOSE, 
                 **suppl_info):
        #super(GridData, self).__init__(input, var_name, verbose, **suppl_info)
        self.verbose = verbose
        self.suppl_info = od(from_files     = [],
                             model_id       = "Unknown",
                             ts_type        = "Unknown",
                             region         = None)
        #attribute used to store area weights (if applicable, see method
        #area_weights)
        self._area_weights = None
        if input:
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
        if not isinstance(value, Cube):
            raise TypeError("Grid data format %s is not supported, need Cube" 
                            %type(value))
        self._grid = value
    
    @property
    def var_name(self):
        """Name of variable in grid"""
        if not self.is_cube:
            raise NotImplementedError("Attribute var_name is not available")
        return self.grid.var_name
    
    @property
    def plot_settings(self):
        """:class:`Variable` instance that contains plot settings
        
        The settings can be specified in the variables.ini file based on the
        unique var_name, see e.g. `here <http://aerocom.met.no/pyaerocom/
        config_files.html#variables>`__
        
        If no default settings can be found for this variable, all parameters
        will be initiated with ``None``, in which case the Aerocom plot method
        uses
        """
        from pyaerocom import Variable
        return Variable(self.var_name)
            
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
    
    @property
    def area_weights(self):
        if self._area_weights is None:
            self.calc_area_weights()
        return self._area_weights
    
    @area_weights.setter
    def area_weights(self, val):
        raise AttributeError("Area weights cannot be set manually yet...")
        
    @property
    def start_time(self):
        """Start time of dataset as datetime64 object"""
        if not self.is_cube:
            if self.verbose:
                print("Start time could not be accessed in "
                                 "GridData class")
            return nan
        return cftime_to_datetime64(self.time[0])[0]
    
    @property
    def stop_time(self):
        """Start time of dataset as datetime64 object"""
        if not self.is_cube:
            if self.verbose:
                print("Stop time could not be accessed in "
                                 "GridData class")
            return nan
        return cftime_to_datetime64(self.time[-1])[0]
        
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
        try:
            if self._ON_LOAD["DEL_TIME_BOUNDS"]:
                self.grid.coord("time").bounds = None
        except:
            if self.verbose:
                print("Failed to access time coordinate in GridData class")
        if self._ON_LOAD["SHIFT_LONS"]:
            self.check_and_regrid_lons()
            
    def time_stamps(self):
        """Convert time stamps into list of numpy datetime64 objects
        
        The conversion is done using method :func:`cfunit_to_datetime64`
        
        Returns
        -------
        list 
            list containing all time stamps as datetime64 objects 
        """
        if self.is_cube:    
            return cftime_to_datetime64(self.time)
    
    def calc_area_weights(self):
        """Calculate area weights for grid"""
        self._check_lonlat_bounds()
        self._area_weights = area_weights(self.grid)
        return self.area_weights
        
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
             time_range=None, region=None):
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
        region : :obj:`str` or :obj:`Region`, optional
            string ID of pyaerocom default region or directly an instance of 
            the :class:`Region` object. May be used instead of 
            ``lon_range`` and ``lat_range``, if these are unspecified.
            
        Returns
        -------
        GridData
            new data object containing cropped grid
        """
        if not self.is_cube:
            raise NotImplementedError("This feature is only available if the"
                                      "underlying data is of type iris.Cube")
        suppl = deepcopy(self.suppl_info)
        if region is not None:
            if isinstance(region, str):
                try:
                    region = Region(region)
                except Exception as e:
                    if self.verbose:
                        print("Failed to access longitude / latitude range "
                              "using region ID {}. Error msg: {}".format(region, 
                                               repr(e)))
            if not isinstance(region, Region):
                raise ValueError("Invalid input for region")
            suppl["region"] = region
            lon_range, lat_range = region.lon_range, region.lat_range
        if lon_range is not None and lat_range is not None:
            data = self.grid.intersection(longitude=lon_range, 
                                          latitude=lat_range)
        elif lon_range is not None and lat_range is None:
            data = self.grid.intersection(longitude=lon_range)
        elif lon_range is None and lat_range is not None:
            data = self.grid.intersection(latitude=lat_range)
        else:
            data = self.grid
        if not data:
            raise DataExtractionError("Failed to apply spatial cropping...")
        if time_range is None:
            return GridData(data, **suppl)
        else:
            if all(isinstance(x, str) for x in time_range):
                time_range = (Timestamp(time_range[0]),
                              Timestamp(time_range[1]))
            if all(isinstance(x, Timestamp) for x in time_range):
                if self.verbose:
                    print("Cropping along time axis based on Timestamps")
                time_constraint = get_time_constraint(*time_range)
                data = data.extract(time_constraint)
            elif all(isinstance(x, int) for x in time_range):
                if self.verbose:
                    print("Cropping along time axis based on indices")
                data = data[time_range[0]:time_range[1]]
            if not data:
                raise DataExtractionError("Failed to apply temporal cropping")
        return GridData(data, **suppl)
        
    def area_weighted_mean(self):
        """Get area weighted mean"""
        ws = self.area_weights
        return self.collapsed(coords=["longitude", "latitude"], 
                              aggregator=MEAN, 
                              weights=ws).grid.data
        
    # redefined methods from iris.Cube class. This includes all Cube 
    # processing methods that exist in the Cube class and that work on the 
    # Cube and return a Cube instance. These may be expanded (e.g. for 
    # instance what they accept as input
    
    def interpolate(self, sample_points, scheme="nearest", 
                    collapse_scalar=True):
        """Interpolate cube at certain discrete points
        
        Reimplementation of method :func:`iris.cube.Cube.interpolate`, for 
        details `see here <http://scitools.org.uk/iris/docs/v1.10.0/iris/iris/
        cube.html#iris.cube.Cube.interpolate>`__
        
        Parameters
        ----------
        sample_points : list
            sequence of coordinate pairs over which to interpolate
        scheme : str or iris interpolator object
            interpolation scheme, pyaerocom default is Nearest. If input is 
            string, it is converted into the corresponding iris Interpolator 
            object, see :func:`str_to_iris` for valid strings
        collapse_scalar : bool
            Whether to collapse the dimension of scalar sample points in the
            resulting cube. Default is True.
        
        Returns
        -------
        GridData
            collapsed data object
            
        Examples
        --------
        
            >>> from pyaerocom import GridData
            >>> data = GridData()
            >>> data._init_testdata_default()
            >>> itp = data.interpolate([("longitude", (10)),
            ...                         ("latitude" , (35))])
            >>> print(itp.shape)
            (365, 1, 1)
        """
        if isinstance(scheme, str):
            scheme = str_to_iris(scheme)
        itp_cube = self.grid.interpolate(sample_points, scheme, 
                                         collapse_scalar)
        return GridData(itp_cube, **self.suppl_info)
    
    def collapsed(self, coords, aggregator, **kwargs):
        """Collapse cube
        
        Reimplementation of method :func:`iris.cube.Cube.collapsed`, for 
        details `see here <http://scitools.org.uk/iris/docs/latest/iris/iris/
        cube.html#iris.cube.Cube.collapsed>`__
        
        Parameters
        ----------
        coords : str or list
            string IDs of coordinate(s) that are to be collapsed (e.g. 
            ``["longitude", "latitude"]``)
        aggregator : str or Aggregator or WeightedAggretor
            the aggregator used. If input is string, it is converted into the
            corresponding iris Aggregator object, see 
            :func:`str_to_iris` for valid strings
        **kwargs 
            additional keyword args (e.g. ``weights``)
        
        Returns
        -------
        GridData
            collapsed data object
        """
        if isinstance(aggregator, str):
            aggregator = str_to_iris(aggregator)
        collapsed = self.grid.collapsed(coords, aggregator, **kwargs)
        return GridData(collapsed, **self.suppl_info)
    
# =============================================================================
#     def extract(self, constraint):
#         """Extract subset
#         
#         Parameters
#         ----------
#         constraint : iris.Constraint
#             constraint that is to be applied
#             
#         Returns
#         -------
#         GridData
#             new data object containing cropped data
#         """
#         if not self.is_cube:
#             raise NotImplementedError("This feature is only available if the"
#                                       "underlying data is of type iris.Cube")
#         data_crop = self.grid.extract(constraint)
#         if not data_crop:
#             raise DataExtractionError("Failed to extract subset")
#         
#         return GridData(data_crop, **self.suppl_info)
# =============================================================================
    
    def intersection(self, *args, **kwargs):
        """Ectract subset using :func:`iris.cube.Cube.intersection` 
        
        See `here for details <http://scitools.org.uk/iris/docs/v1.9.0/html/
        iris/iris/cube.html#iris.cube.Cube.intersection>`__
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
        GridData
            new data object containing cropped data
        """
        if not self.is_cube:
            raise NotImplementedError("This feature is only available if the"
                                      "underlying data is of type iris.Cube")
        data_crop = self.grid.intersection(*args, **kwargs)
        
        return GridData(data_crop, **self.suppl_info)
    
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
    
    def short_str(self):
        """Short string representation"""
        head = "Pyaerocom {}".format(type(self).__name__)
        s = ("\n{}\n{}\n"
             "Variable: {}\n"
             "Temporal resolution: {}\n"
             "Start / Stop: {} - {}".format(head,
                                            len(head)*"-",
                                            self.var_name, 
                                            self.suppl_info["ts_type"],
                                            self.start_time,
                                            self.stop_time))
        return s
    
    def _check_lonlat_bounds(self):
        """Check if longitude and latitude bounds are set and if not, guess"""
        if self.longitude.bounds is None:
            self.longitude.guess_bounds()
        if self.latitude.bounds is None:
            self.latitude.guess_bounds()
            
    def _init_testdata_default(self):
        """Helper method that loads ECMWF_OSUITE test data"""
        from pyaerocom.io.testfiles import get
        self.load_input(get()["models"]["ecmwf_osuite"], var_name="od550aer")
        return self
    
    def __getitem__(self, indices):
        """x.__getitem__(y) <==> x[y]"""
        sub = self.grid.__getitem__(indices)
        return GridData(sub, **self.suppl_info)
        
    def __str__(self):
        """For now, use string representation of underlying data"""
        return ("pyaerocom.GridData: %s\nGrid data: %s"
                %(self.model_id, self.grid.__str__()))
    
    def __repr__(self):
        """For now, use representation of underlying data"""
        return "pyaerocom.GridData\nGrid data: %s" %self.grid.__repr__()
    
if __name__=='__main__':
    RUN_OLD_STUFF = False
    
    data = GridData()
    data._init_testdata_default()
# =============================================================================
#     itp = data.interpolate([("longitude", (10)),
#                             ("latitude" , (35))])
#     
# =============================================================================

    start = Timestamp("2018-1-22")
    stop = Timestamp("2018-2-5")
    
    cropped = data.crop(time_range=(start, stop))
    if RUN_OLD_STUFF:
        from pyaerocom.io.testfiles import get
        from matplotlib.pyplot import close, figure
        import numpy as np
        close("all")
        files = get()
        data = GridData(files['models']['aatsr_su_v4.3'], var_name="od550aer",
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
        
        other = GridData(files["models"]["ecmwf_osuite"],
                          var_name="od550aer", model_id="ECMWF_OSUITE")
        other.quickplot_map()
        #crop randomly
        ocropped = other.crop(lon_range=(100, 170), lat_range=(-60, 60))
        ocropped.quickplot_map()
        # some plot options
        ocropped.quickplot_map(fix_aspect=2, vmin=.4, vmax=1.)
        ocropped.quickplot_map(vmin=0, vmax=1., c_over="r")
        
        # crop india
        cropped_india = other.crop(region="INDIA")[:60]
        cropped_india.quickplot_map(time_idx=0)
        
        if np.any(np.isnan(cropped_india.grid.data)):
            raise Exception
        
        mean = cropped_india.area_weighted_mean()
        
        from pandas import Series
        
        s = Series(data=mean, index=cropped_india.time_stamps())
        
        fig = figure()
        s.plot()
        fig.tight_layout()
        try:
            GridData(files["models"]["ecmwf_osuite"])
        except ValueError as e:
            warn(repr(e))
        
# =============================================================================
#     import doctest
#     doctest.testmod()
# 
# =============================================================================
