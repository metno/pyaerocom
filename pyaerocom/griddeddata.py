#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pyaerocom GriddedData class
"""
from os.path import exists
from copy import deepcopy
from collections import OrderedDict as od
from iris import Constraint, load, load_cube
from iris.cube import Cube, CubeList
from iris.analysis.cartography import area_weights
from iris.analysis import MEAN
from pandas import Timestamp, Series
from warnings import warn
from numpy import nan, where
from numpy.ma import MaskedArray

from pyaerocom import const, logger
from pyaerocom.exceptions import (DataExtractionError,
                                  TemporalResolutionError)
from pyaerocom.helpers import (get_time_constraint, 
                               cftime_to_datetime64,
                               str_to_iris,
                               IRIS_AGGREGATORS)

from pyaerocom.region import Region


class GriddedData(object):
    """Base class representing model data
    
    Todo
    ----
    Add support for    
    This class is largely based on the :class:`iris.Cube` object. However, this
    object comes with an expanded functionality for convenience, for instance, 
    netCDF files can directly be loaded in the :class:`GriddedData` object,
    whereas :class:`iris.cube.Cube` instances are typically created using
    helper methods such as
    
    1. :func:`iris.load` (returns 
    :class:`iris.cube.CubeList`, i.e. a list-like iterable object that contains 
    instances of :class:`Cube` objects, one for each variable) or 
    
    2. :func:`iris.load_cube` which directly returns a :class:`iris.cube.Cube` 
    instance and typically requires specification of a variable constraint.
    
    The :class:`GriddedData` object represents one variable in space and time, as
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
    >>> data = GriddedData(files['models']['aatsr_su_v4.3'], 
    ...                    var_name="od550aer")
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
    _GRID_IO = const.GRID_IO
    
    def __init__(self, input=None, var_name=None, **suppl_info):
        self.suppl_info = od(from_files     = [],
                             name           = "Unknown",
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
    def ts_type(self):
        """Temporal resolution"""
        return self.suppl_info['ts_type']
    
    @property
    def TS_TYPES(self):
        """List with valid filename encryptions specifying temporal resolution
        """
        return self.io_opts.GRID_IO.TS_TYPES
    
    def to_daily(self):
        """Convert this object to daily resolution"""
        raise NotImplementedError
        
    @property
    def is_masked(self):
        """Flag specifying whether data is masked or not
        
        Note
        ----
        This method only works if the data is loaded.
        """
        if self.grid.has_lazy_data():
            raise AttributeError("Information cannot be accessed. Data is not "
                                 "available in memory (lazy loading)")
        return isinstance(self.grid.data, MaskedArray)
    
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
    def name(self):
        """ID of model to which data belongs"""
        return self.suppl_info["name"]
    
    @property
    def is_cube(self):
        """Checks if underlying data type is of type :class:`iris.cube.Cube`"""
        return True if isinstance(self.grid, Cube) else False
    
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
    def shape(self):
        if not self.has_data:
            raise NotImplementedError("No data available...")
        return self.grid.shape 
    
    @property
    def ndim(self):
        """Number of dimensions"""
        if not self.has_data:
            raise NotImplementedError("No data available...")
        return self.grid.ndim
    
    @property
    def coords_order(self):
        """Array containing the order of coordinates"""
        if not self.has_data:
            raise NotImplementedError("No data available...")
        return [x.name() for x in self.grid.coords()]
    
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
            logger.warning("Start time could not be accessed in GriddedData")
            return nan
        return cftime_to_datetime64(self.time[0])[0]
    
    @property
    def stop_time(self):
        """Start time of dataset as datetime64 object"""
        if not self.is_cube:
            logger.warning("Stop time could not be accessed in GriddedData")
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
            if self._GRID_IO["DEL_TIME_BOUNDS"]:
                self.grid.coord("time").bounds = None
        except:
            logger.warning("Failed to access time coordinate in GriddedData")
        if self._GRID_IO["SHIFT_LONS"]:
            self.check_and_regrid_lons()
        #if isinstance(sel)
            
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
    
    
    def lonlat_resolution(self):
        """Longitude / latitude resolution of grid
        
        Returns
        -------
        tuple
            2-element tuple containing
            
            - average longitude resolution in decimal degrees
            - average latitude resolution in decimal degrees
        """
        raise NotImplementedError
        
    def crop_around_coord(self, lon, lat, step_deg=2):
        """Crop cube around a single lon / lat coordinate
        
        Parameters
        -----------
        lon : float
            longitude of coordinate
        lat: float
            latitude of coordinate
        step_deg : :obj:`float` or :obj:`int`
            
        """
        raise NotImplementedError
        
    def to_timeseries_iter_coords(self, sample_points, scheme, collapse_scalar,
                                  **coords):
        """Extract time-series for provided input coordinates (lon, lat)
        
        Other than :func:`to_time_series`, this method extracts the time-series
        at all input coordinates by iterating over the coordinate locations, 
        cropping the grid around the coordinate and then interpolating it using
        the provided interpolation scheme.
        
        This method may be faster for a small number of coordinates (compared 
        to :func:`to_timeseries`). It may also be the better choice in case the
        number of coordinates is too large in which case :func:`to_time_series`
        may fail due to a MemoryError (i.e. the case where the final 
        interpolated object is too large to fit into memory).
        
        Parameters
        ----------
        sample_points : list
            coordinates (e.g. lon / lat) at which time series is supposed to be
            retrieved
        scheme : str or iris interpolator object
            interpolation scheme (for details, see :func:`interpolate`)
        collapse_scalar : bool
            see :func:`interpolate`
        **coords
            additional keyword args that may be used to provide the interpolation
            coordinates (for details, see :func:`interpolate`)

        Returns
        -------
        list
            list of result dictionaries for each coordinate. Dictionary keys
            are: ``longitude, latitude, var_name``
            
        """
        raise NotImplementedError
        
    def to_time_series(self, sample_points=None, scheme="nearest", 
                    collapse_scalar=True, **coords):

        """Extract time-series for provided input coordinates (lon, lat)

        Extract time series for each lon / lat coordinate in this cube or at
        predefined sample points (e.g. station data). If sample points are
        provided, the cube is interpolated first onto the sample points.

        Todo
        ----
        Add model ID 
        
        Parameters
        ----------
        sample_points : list
            coordinates (e.g. lon / lat) at which time series is supposed to be
            retrieved
        scheme : str or iris interpolator object
            interpolation scheme (for details, see :func:`interpolate`)
        collapse_scalar : bool
            see :func:`interpolate`
        **coords
            additional keyword args that may be used to provide the interpolation
            coordinates (for details, see :func:`interpolate`)

        Returns
        -------
        list
            list of result dictionaries for each coordinate. Dictionary keys
            are: ``longitude, latitude, var_name``
        """

        result = []
        if not sample_points:
            sample_points = []
        sample_points.extend(list(coords.items()))
        if not self.coords_order[:3] == ['time', 'latitude', 'longitude']:
            raise NotImplementedError("So far, time series can only be "
                                      "retrieved for 3-dimensional data "
                                      "with coordinate order "
                                      "[time, latitude, longitude].")
        lens = [len(x[1]) for x in sample_points]
        if not all([lens[0]==x for x in lens]):
            raise ValueError("Arrays for sample coordinates must have the "
                             "same lengths")
        try:
            data = self.interpolate(sample_points, scheme, collapse_scalar)
            var = self.var_name
            times = data.time_stamps()
            lats = [x[1] for x in sample_points if x[0] == "latitude"][0]
            lons = [x[1] for x in sample_points if x[0] == "longitude"][0]
            arr = data.grid.data
            grid_lons = data.longitude.points
            for i, lat in enumerate(lats):
                lon = lons[i]
                j = where(grid_lons == lon)[0][0]
                result.append({'latitude'   :   lat,
                               'longitude'  :   lon,
                               'name'       :   self.name, 
                               var          :   Series(arr[:, i, j], 
                                                       index=times)})
        except MemoryError:
            self._to_timeseries_slow(sample_points, scheme, collapse_scalar)
                
        return result
    
    # TODO: Test, confirm and remove beta flag in docstring
    def downscale_time(self, to_ts_type='monthly'):
        """Downscale in time to predefined resolution resolution
        
        Note
        ----
        Beta version
        
        Patameters
        ----------
        to_ts_type : str
            either of the supported temporal resolutions (cf. 
            :attr:`IRIS_AGGREGATORS` in :mod:`helpers`, e.g. "monthly")
        
        Returns
        -------
        GriddedData
            new data object containing downscaled data
            
        Raises
        ------
        TemporalResolutionError
            if input resolution is not provided, or if it is higher temporal 
            resolution than this object
        """
        ts_types_avail = const.GRID_IO.TS_TYPES
        idx_ts_type = ts_types_avail.index(to_ts_type)
        if self.ts_type == to_ts_type:
            logger.info('Data is already in {} resolution'.format(to_ts_type))
            return self
        if not to_ts_type in IRIS_AGGREGATORS:
            raise TemporalResolutionError('Resolution {} cannot '
                'converted'.format(to_ts_type))
        elif ts_types_avail.index(self.ts_type) >= idx_ts_type:
            raise TemporalResolutionError('Cannot increase '
                'temporal resolution from {} to {}'.format(self.ts_type,
                                          to_ts_type))
        cube = self.grid
        IRIS_AGGREGATORS[to_ts_type](cube, 'time', name=to_ts_type)
        aggregated = cube.aggregated_by(to_ts_type, MEAN)
        data = GriddedData(aggregated, **self.suppl_info)
        data.suppl_info['ts_type'] = to_ts_type
        return data     
    
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
            logger.info("Rolling longitudes to -180 -> 180 definition")
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
        GriddedData
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
                    logger.warning("Failed to access longitude / latitude range "
                                   "using region ID {}. Error msg: {}".format(
                                           region, repr(e)))
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
            return GriddedData(data, **suppl)
        else:
            if all(isinstance(x, str) for x in time_range):
                time_range = (Timestamp(time_range[0]),
                              Timestamp(time_range[1]))
            if all(isinstance(x, Timestamp) for x in time_range):
                logger.info("Cropping along time axis based on Timestamps")
                time_constraint = get_time_constraint(*time_range)
                data = data.extract(time_constraint)
            elif all(isinstance(x, int) for x in time_range):
                logger.info("Cropping along time axis based on indices")
                data = data[time_range[0]:time_range[1]]
            if not data:
                raise DataExtractionError("Failed to apply temporal cropping")
        return GriddedData(data, **suppl)
        
    
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
    
    def interpolate(self, sample_points=None, scheme="nearest", 
                    collapse_scalar=True, **coords):
        """Interpolate cube at certain discrete points
        
        Reimplementation of method :func:`iris.cube.Cube.interpolate`, for 
        details `see here <http://scitools.org.uk/iris/docs/v1.10.0/iris/iris/
        cube.html#iris.cube.Cube.interpolate>`__
        
        Note
        ----
        The input coordinates may also be provided using the input arg **coords
        which provides a more intuitive option (e.g. input
        ``(sample_points=[("longitude", [10, 20]), ("latitude", [1, 2])])`` 
        is the same as input
        ``(longitude=[10, 20], latitude=[1,2])``
        
        
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
        **coords
            additional keyword args that may be used to provide the interpolation
            coordinates in an easier way than using the ``Cube`` argument
            :arg:`sample_points``. May also be a combination of both.
         
        Returns
        -------
        GriddedData
            new data object containing interpolated data
            
        Examples
        --------
        
            >>> from pyaerocom import GriddedData
            >>> data = GriddedData()
            >>> data._init_testdata_default()
            >>> itp = data.interpolate([("longitude", (10)),
            ...                         ("latitude" , (35))])
            >>> print(itp.shape)
            (365, 1, 1)
        """
        if isinstance(scheme, str):
            scheme = str_to_iris(scheme)
        if not sample_points:
            sample_points = []
        sample_points.extend(list(coords.items()))
        try:
            itp_cube = self.grid.interpolate(sample_points, scheme, 
                                             collapse_scalar)
        except MemoryError:
            raise MemoryError("Interpolation failed since grid of interpolated "
                              "Cube is too large")
        return GriddedData(itp_cube, **self.suppl_info)
    
    def collocate(self, sample_points=None, scheme="nearest", 
                  collapse_scalar=True, **coords):
        """Collocate Cube to positions of input coordinates
        
        Note
        -----
        This method is under development and does not work yet
        
        Other than :func:`interpolate`, this method extracts the data values 
        for a given number of input coordinates (e.g. combination of lon / lat
        values that belong, e.g. to station coordinates). Thus, this results in
        a reduction of dimensionality, since the provided coordinate 
        combinations are not othorgonal anymore. 
        
        All other dimensions are preserved (e.g. time), thus, collocating a 3D
        grid of time / lon / lat dimension and shape ``(265, 360, 180)`` at 
        50 lon / lat coordinates will result in a 2D numpy array of shape 
        ``(365, 50)``
        
        Parameters
        ----------
        sample_points : list
            sequence of coordinate pairs over which to interpolate
        scheme : str or iris interpolator object
            interpolation scheme (for details, see :func:`interpolate`)
        collapse_scalar : bool
            see :func:`interpolate`
        **coords
            keyword args specifying coordinate name (key, e.g. longitude) and 
            list of corresponding sample point coordinates (value, 
            e.g. ``[1,2,3]``)
        
        Returns
        -------
        ndarray
            data values at provided input coordinates
            
        Raises
        ------
        ValueError
            if length of coordinate arrays are unequal or coord
        KeyError
            if one of the provided coordinates does not exist[('a', 1), ('b', 2), ('c', 3)]
        
        Example
        -------
        
            >>> from pyaerocom import GriddedData
            >>> data = GriddedData()
            >>> data._init_testdata_default()
            >>> lons = [10, 20, 30, 40]
            >>> lats = [5, 7, 9, 11]
            >>> pt_data = data.collocate(longitude=lons,
            ...                          latitude=lats)
            >>> print(pt_data.shape)
            (365, 4)
        
        """
        if not sample_points:
            sample_points = []
        sample_points.extend(list(coords.items()))
        if not sample_points:
            raise IOError("Please provide coordinate either using arg"
                          "sample_points or via **coords")
        coords_avail = [coord.name() for coord in self.grid.coords()]
        _indices = []
        if not sample_points:
            sample_points = []
        sample_points.extend(list(coords.items())) 
        # get length of sample points array of first coordinate
        ref_len = len(sample_points[0][1])
        
        for name, values in sample_points:
            if not name in coords_avail:
                raise KeyError("Coordinate {} does not exist in data, existing "
                               "coordinates are {}".format(name, coords_avail))
            elif not len(values) == ref_len:
                raise ValueError("Length of coordinate arrays must be the "
                                 "same...")
            _indices.append(coords_avail.index(name))
            
        ### interpolate grid to new coordinates
        sub = self.interpolate(sample_points, scheme, collapse_scalar)
        
        arr = sub.grid.data
        
        #total number of points in grid
        tot_num_grid = np.prod(arr.shape)
        
        #get the number of parameters spanned by the subspace
        sub_num_grid = ref_len**len(sample_points)
        
        #put reduced dimension into first index, so we can loop over it
        arr_dimred = arr.reshape(sub_num_grid, )
        
        #remove first item in sample_points (used to iterate over all points)
        first_coord, values = sample_points.pop(0)
        
        lats = [x[1] for x in sample_points if x[0] == "latitude"][0]
        lons = [x[1] for x in sample_points if x[0] == "longitude"][0]
        
        raise NotImplementedError("Under construction...")
        #for val in values:
# =============================================================================
#             
#         grid_lons = data.longitude.points
#         for i, lat in enumerate(lats):
#             lon = lons[i]
#             j = np.where(grid_lons == lon)[0][0]
#             result.append({'latitude'   :   lat,
#                            'longitude'  :   lon,
#                            var          :   Series(arr[:, i, j], 
#                                                    index=times)})
#         return ()
# =============================================================================
        
    
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
        GriddedData
            collapsed data object
        """
        if isinstance(aggregator, str):
            aggregator = str_to_iris(aggregator)
        collapsed = self.grid.collapsed(coords, aggregator, **kwargs)
        return GriddedData(collapsed, **self.suppl_info)
    
    def extract(self, constraint):
        """Extract subset
        
        Parameters
        ----------
        constraint : iris.Constraint
            constraint that is to be applied
            
        Returns
        -------
        GriddedData
            new data object containing cropped data
        """
        if not self.is_cube:
            raise NotImplementedError("This feature is only available if the"
                                      "underlying data is of type iris.Cube")
        data_crop = self.grid.extract(constraint)
        if not data_crop:
            raise DataExtractionError("Failed to extract subset")
        
        return GriddedData(data_crop, **self.suppl_info)
    
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
        GriddedData
            new data object containing cropped data
        """
        if not self.is_cube:
            raise NotImplementedError("This feature is only available if the"
                                      "underlying data is of type iris.Cube")
        data_crop = self.grid.intersection(*args, **kwargs)
        
        return GriddedData(data_crop, **self.suppl_info)
    
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
        fig = plot_map(self[time_idx], xlim, ylim, **kwargs)
        fig.axes[0].set_title("Model: %s, var=%s (%s)" 
                     %(self.name, self.var_name,
                       self.time.cell(time_idx)))
        return fig
    
    def min(self):
        """Minimum value"""
        #make sure data is in memory
        data = self.grid.data
        if self.is_masked:
            return data.data[~data.mask].min()
        return data.min()
        
    def max(self):
        """Maximum value"""
        #make sure data is in memory
        data = self.grid.data
        if self.is_masked:
            return data.data[~data.mask].max()
        return data.max()
    
    def mean(self):
        """Mean value of data array
        
        Note
        ----
        Corresponds to numerical mean of underlying N-dimensional numpy array.
        Does not consider area-weights or any other advanced averaging.
        """
        #make sure data is in memory
        data = self.grid.data
        if self.is_masked:
            return data.data[~data.mask].mean()
        return data.mean()
    
    def std(self):
        """Standard deviation of values"""
        #make sure data is in memory
        data = self.grid.data
        if self.is_masked:
            return data.data[~data.mask].std()
        return data.std()
    
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
        return GriddedData(sub, **self.suppl_info)
        
    def __str__(self):
        """For now, use string representation of underlying data"""
        return ("pyaerocom.GriddedData: %s\nGrid data: %s"
                %(self.name, self.grid.__str__()))
    
    def __repr__(self):
        """For now, use representation of underlying data"""
        return "pyaerocom.GriddedData\nGrid data: %s" %self.grid.__repr__()
    
if __name__=='__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    plt.close("all")
    RUN_OLD_STUFF = False
    
    data = GriddedData()
    data._init_testdata_default()
    
    start = Timestamp("2018-1-22")
    stop = Timestamp("2018-2-5")
    
    lons = np.linspace(-10, 30, 20)
    lats = np.linspace(40, 80, 20)
    cropped = data.crop(lon_range=(lons[0], lons[-1]), 
                        lat_range=(lats[0], lats[-1]), 
                        time_range=(start, stop))
    
    fig = cropped.quickplot_map()
    fig.suptitle("CROPPED")
    
    itp = cropped.interpolate(longitude=lons, 
                              latitude=lats)
    
    fig = itp.quickplot_map()
    fig.suptitle("INTERPOLATED")
    
# =============================================================================
#     collo = cropped.collocate(longitude=lons, 
#                               latitude=lats)
# =============================================================================
    
    s = cropped.to_time_series(sample_points=[('longitude', lons),
                                              ('latitude', lats)])
    
    
    if RUN_OLD_STUFF:
        from pyaerocom.io.testfiles import get
        from matplotlib.pyplot import close, figure
        import numpy as np
        files = get()
        data = GriddedData(files['models']['aatsr_su_v4.3'], var_name="od550aer",
                         name='aatsr_su_v4.3')
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
        
        other = GriddedData(files["models"]["ecmwf_osuite"],
                          var_name="od550aer", name="ECMWF_OSUITE")
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
            GriddedData(files["models"]["ecmwf_osuite"])
        except ValueError as e:
            warn(repr(e))
        
# =============================================================================
#     import doctest
#     doctest.testmod()
# 
# =============================================================================
