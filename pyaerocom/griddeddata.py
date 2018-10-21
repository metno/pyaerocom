#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pyaerocom GriddedData class
"""

import os
from collections import OrderedDict as od
import iris
from iris.analysis.cartography import area_weights
from iris.analysis import MEAN
from pandas import Timestamp, Series
from warnings import warn
import numpy as np
import pandas as pd
from pyaerocom import const, logger, print_log

from pyaerocom.exceptions import (DataExtractionError,
                                  TemporalResolutionError,
                                  DimensionOrderError,
                                  NDimError, DataDimensionError,
                                  VariableDefinitionError)
from pyaerocom.helpers import (get_time_constraint, 
                               cftime_to_datetime64,
                               str_to_iris,
                               IRIS_AGGREGATORS,
                               to_pandas_timestamp,
                               TS_TYPE_TO_NUMPY_FREQ,
                               datetime2str)
from pyaerocom.mathutils import closest_index
from pyaerocom.stationdata import StationData
from pyaerocom.region import Region


class GriddedData(object):
    """Base class representing model data
    
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
    well as corresponding meta information. Since it is based on the https://github.com/SciTools/iris/issues/1977
    :class:`iris.cube.Cube` it is optimised for netCDF files that follow the
    CF conventions and may not work for files that do not follow this standard.
       
    Parameters
    ----------
    input : :obj:`str:` or :obj:`Cube`
        data input. Can be a single .nc file or a preloaded iris Cube.
    var_name : :obj:`str`, optional
        variable name that is extracted if `input` is a file path. Irrelevant
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
    #: Req. order of dimension coordinates for time-series computation
    COORDS_ORDER_TSERIES = ['time', 'latitude', 'longitude']
    _MAX_SIZE_GB = 6 #maximum file size for in-memory operations
    def __init__(self, input=None, var_name=None, convert_unit_on_init=True,
                 **suppl_info):
        self.suppl_info = od(from_files     = [],
                             name           = "Unknown",
                             ts_type        = "Unknown",
                             regridded      = False,
                             computed       = True,
                             region         = None)
        
        
        #attribute used to store area weights (if applicable, see method
        #area_weights)
        self._area_weights = None
        if input:
            self.load_input(input, var_name)
        for k, v in suppl_info.items():
            if k in self.suppl_info:
                self.suppl_info[k] = v
                
        if convert_unit_on_init:
            try:
                var = self.var_info
                if var.has_unit and var.unit != self.unit:
                    logger.info('Converting unit of data')
                    self.convert_unit(var.unit)
            except (VariableDefinitionError, MemoryError):
                pass
    
    @property
    def data_revision(self):
        """Revision string from file Revision.txt in the main data directory
        """
        if self.from_files:
            data_dir = os.path.dirname(self.from_files[0])
            revision_file = os.path.join(data_dir, const.REVISION_FILE)
            if os.path.isfile(revision_file):
                with open(revision_file, 'rt') as in_file:
                    revision = in_file.readline().strip()
                    in_file.close()
    
                return revision
        return 'n/a'
        
    @property
    def unit(self):
        """Unit of data"""
        return self.grid.units
    
    @property
    def var_info(self):
        """Print information about variable"""
        return const.VAR_PARAM[self.var_name]
    
    @property
    def ts_type(self):
        """Temporal resolution"""
        return self.suppl_info['ts_type']
    
    @property
    def TS_TYPES(self):
        """List with valid filename encryptions specifying temporal resolution
        """
        return self.io_opts.GRID_IO.TS_TYPES
      
    @property
    def from_files(self):
        """List of file paths from which this data object was created"""
        return self.suppl_info['from_files']
        
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
        return isinstance(self.grid.data, np.ma.core.MaskedArray)
    
    @property
    def start(self):
        """Start time of dataset as datetime64 object"""
        if not self.is_cube:
            logger.warning("Start time could not be accessed in GriddedData")
            return np.nan
        t = cftime_to_datetime64(self.time[0])[0]
        
        try:
            dtype_appr = 'datetime64[{}]'.format(TS_TYPE_TO_NUMPY_FREQ[self.ts_type])
            t=t.astype(dtype_appr)
        except:
            logger.exception('Failed to round start time {} to beginning of '
                             'frequency {}'.format(t, self.ts_type))
        return t.astype('datetime64[us]')

    
    @property
    def stop(self):
        """Start time of dataset as datetime64 object"""
        if not self.is_cube:
            logger.warning("Stop time could not be accessed in GriddedData")
            return np.nan
        t = cftime_to_datetime64(self.time[-1])[0]
        try:
            freq = TS_TYPE_TO_NUMPY_FREQ[self.ts_type]
            dtype_appr = 'datetime64[{}]'.format(freq)
            
            t = t.astype(dtype_appr) + np.timedelta64(1, unit=freq)
            t = t.astype('datetime64[us]') - np.timedelta64(1,unit='us')
            return t
        except:
            logger.exception('Failed to round start time {} to beggining of '
                             'frequency {}'.format(t, self.ts_type))
            return t.astype('datetime64[us]')
    
# =============================================================================
#     @property
#     def longitude(self):
#         """Longitudes of data"""
#         if self.is_cube:
#             return self.grid.coord("longitude")
#         
#     @longitude.setter
#     def longitude(self, value):
#         raise AttributeError("Longitudes cannot be changed, please check "
#                              "underlying data type stored in attribute grid")
#     
#     @property
#     def latitude(self):
#         """Latitudes of data"""
#         if self.is_cube:
#             return self.grid.coord("latitude")
#         
#     @latitude.setter
#     def latitude(self, value):
#         raise AttributeError("Latitudes cannot be changed, please check "
#                              "underlying data type stored in attribute grid")
# =============================================================================
        
# =============================================================================
#     @property
#     def time(self):
#         """Time dimension of data"""
#         if self.is_cube:
#             return self.grid.coord("time")
#         
#     @time.setter
#     def time(self, value):
#         raise AttributeError("Time array cannot be changed, please check "
#                              "underlying data type stored in attribute grid")
# =============================================================================
            
    @property
    def grid(self):
        """Underlying grid data object"""
        return self._grid
    
    @grid.setter
    def grid(self, value):
        if not isinstance(value, iris.cube.Cube):
            raise TypeError("Grid data format %s is not supported, need Cube" 
                            %type(value))
        self._grid = value
    
    @property
    def var_name(self):
        """Name of variable in grid"""
        if not self.is_cube:
            return 'n/a'
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
        return const.VAR_PARAM[self.var_name]
            
    @property 
    def name(self):
        """ID of model to which data belongs"""
        return self.suppl_info["name"]
    
    @property
    def is_cube(self):
        """Checks if underlying data type is of type :class:`iris.cube.Cube`"""
        return True if isinstance(self.grid, iris.cube.Cube) else False
    
    @property
    def is_climatology(self):
        try:
            year = to_pandas_timestamp(self.start).year
            if year == 9999:
                return True
            return False
        except pd.errors.OutOfBoundsDatetime:
            return True
    
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
    def lon_res(self):
        if not 'longitude' in self:
            raise AttributeError('Data does not contain longitude information')
        vals = np.diff(self.longitude.points)
        val = vals.mean()
        if vals.std() / val > 0.0001:
            raise ValueError('Check longitudes')
        return val
    
    @property
    def lat_res(self):
        if not 'latitude' in self:
            raise AttributeError('Data does not contain longitude information')
        vals = np.diff(self.latitude.points)
        val = vals.mean()
        if vals.std() / val > 0.0001:
            raise ValueError('Check latitudes')
        return val
    
    @property
    def ndim(self):
        """Number of dimensions"""
        if not self.has_data:
            raise NotImplementedError("No data available...")
        return self.grid.ndim
    
    @property
    def coords_order(self):
        """Array containing the order of coordinates"""
        return self.coord_names    
    
    @property
    def coord_names(self):
        """List containing coordinate names"""
        if not self.has_data:
            return []
        return [c.name() for c in self.grid.coords()]
    
    @property
    def dimcoord_names(self):
        """List containing coordinate names"""
        if not self.has_data:
            return []
        return [c.name() for c in self.grid.dim_coords]
    
    @property
    def area_weights(self):
        if self._area_weights is None:
            self.calc_area_weights()
        return self._area_weights
    
    @area_weights.setter
    def area_weights(self, val):
        raise AttributeError("Area weights cannot be set manually yet...")
      
    def check_dim_coords(self):
        """Check dimension coordinates of grid data"""
        raise NotImplementedError
        
    def load_input(self, input, var_name):
        """Import input as cube
        
        Parameters
        ----------
        input : :obj:`str:` or :obj:`Cube`
            data input. Can be a single .nc file or a preloaded iris Cube.
        var_name : :obj:`str`, optional
            variable name that is extracted if `input` is a file path . Irrelevant
            if `input` is preloaded Cube
            
        """
        if isinstance(input, iris.cube.Cube):
            self.grid = input #instance of Cube
        elif isinstance(input, str) and os.path.exists(input):
            from pyaerocom.io.iris_io import load_cube_custom
            from pyaerocom.io import FileConventionRead
            self.grid = load_cube_custom(input, var_name)
            
            try:
                f = FileConventionRead()
                f.from_file(input)
                self.suppl_info.update(**f.get_info_from_file(input))
            except:
                pass
            self.suppl_info["from_files"].append(input)
            
        else:
            raise IOError('Failed to load input: {}'.format(input))
        try:
            self.grid.var_name = self.var_info.var_name
        except:
            logger.warn('Failed to convert variable name {}'.format(self.var_name))
        
     
    def convert_unit(self, new_unit):
        """Convert unit of data to new unit"""
        if self._size_GB > self._MAX_SIZE_GB:
            raise MemoryError('Cannot convert unit in {} since data is too '
                              'large ({} GB)'.format(self.name, self._size_GB))
        self.grid.convert_units(new_unit)
        
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

    def check_coord_order(self):
        """Wrapper for :func:`check_dimcoords_tseries`"""
        logger.warn(DeprecationWarning('Method was renamed, please use '
                                       'check_dimcoords_tseries'))
        return self.check_dimcoords_tseries()
    
    def check_dimcoords_tseries(self):
        """Check order of dimension coordinates for time series retrieval
        
        For computation of time series at certain lon / lat coordinates, the 
        data dimensions have to be in a certain order specified by 
        :attr:`COORDS_ORDER_TSERIES`.
        
        This method checks the current order (and dimensionality) of data and
        raises appropriate errors.
        
        Raises
        ------
        NDimError
            if dimension of data is not supported (currently, 3D or 4D data
            is supported)
        DimensionOrderError
            if dimensions are not in the right order (in which case 
            :func:`reorder_dimensions_tseries` may be used to catch the 
            Exception)
        """
        order = self.COORDS_ORDER_TSERIES
        if not self.ndim in (3,4):
            raise NDimError('Time series extraction requires at least 3 '
                            'coordinates in cube')
        check = self.dimcoord_names
        if not len(check) >= 3:
            raise DataDimensionError('One of the data dimension coordinates '
                                     'may not be defined')
            
        for i, item in enumerate(check[:3]):
            if not item == order[i]:
                raise DimensionOrderError('Invalid order of grid '
                                          'dimension, need {}, got {}'
                                          .format(order,
                                                  check))
        
            
    def reorder_dimensions_tseries(self):
        """Reorders dimensions of data such that :func:`to_time_series` works
        """
        order = self.COORDS_ORDER_TSERIES
        new_order = []
        coord_names = [c.name() for c in self.grid.dim_coords]
        for coord_name in order:
            new_order.append(coord_names.index(coord_name))
        if not len(new_order) == self.ndim:
            for i in range(self.ndim):
                if not i in new_order:
                    new_order.append(i)
        self.transpose(new_order)
        self.check_dimcoords_tseries()
        
    def transpose(self, new_order):
        """Re-order data dimensions in object
        
        Wrapper for :func:`iris.cube.Cube.transpoe`
        
        Note
        ----
        Changes THIS object (i.e. no new instance of :class:`GriddedData` will 
        be created)
        
        Parameters
        ----------
        order : list
            new index order
        """
        self.grid.transpose(new_order)
        
    def _check_altitude_access(self):
        raise NotImplementedError
        coord_name = self.coord_names[-1]
        if coord_name == 'altitude':
            return True
        from pyaerocom.vert_coords import _VertCoordConverter as conv
        if not coord_name in conv.supported:
            return False
        arg_info = conv.VARS[coord_name]
        args_dict = {}
        name1
        for arg, possible_vals in arg_info.items():
            pass
            
        
        
    def get_altitude(self, coords):
        """Extract (or try to compute) altitude values at input coordinates"""
        raise NotImplementedError('Coming soon...')
        
    def to_time_series(self, sample_points=None, scheme="nearest", 
                       collapse_scalar=True, vert_scheme=None, **coords):

        """Extract time-series for provided input coordinates (lon, lat)

        Extract time series for each lon / lat coordinate in this cube or at
        predefined sample points (e.g. station data). If sample points are
        provided, the cube is interpolated first onto the sample points.

        Todo
        ----
        Check Memory error handle
        
        Parameters
        ----------
        sample_points : list
            coordinates (e.g. lon / lat) at which time series is supposed to be
            retrieved
        scheme : str or iris interpolator object
            interpolation scheme (for details, see :func:`interpolate`)
        collapse_scalar : bool
            see :func:`interpolate`
        vert_scheme : str
            string specifying how to treat vertical coordinates. This is only
            relevant for data that contains vertical levels. It will be ignored
            otherwise. Note that if the input coordinate specifications contain
            altitude information, this parameter will be set automatically to
            'altitude'. Allowed inputs are all data collapse schemes that 
            are supported by :func:`pyaerocom.helpers.str_to_iris` (e.g. `mean, 
            median, sum`). Further valid schemes are `altitude, surface, 
            profile`.
            If not other specified and if `altitude` coordinates are provided
            via sample_points (or **coords parameters) then, vert_scheme will 
            be set to `altitude`. Else, `profile` is used.
        **coords
            additional keyword args that may be used to provide the interpolation
            coordinates (for details, see :func:`interpolate`)

        Returns
        -------
        list
            list of result dictionaries for each coordinate. Dictionary keys
            are: ``longitude, latitude, var_name``
        """
        try:
            self.check_dimcoords_tseries()
        except DimensionOrderError:
            self.reorder_dimensions_tseries()
        # if the method makes it to this point, the it is 3 or 4 dimensional 
        # and the first 3 dimensions are time, latitude, longitude.
        
        # init input for sample points
        if not sample_points:
            sample_points = []
        sample_points.extend(list(coords.items()))
        lens = [len(x[1]) for x in sample_points]
        if not all([lens[0]==x for x in lens]):
            raise ValueError("Arrays for sample coordinates must have the "
                             "same lengths")
        if self.ndim == 3: #data does not contain vertical dimension
            return self._to_timeseries_2D(sample_points, scheme,
                                          collapse_scalar)
        
        return self._to_timeseries_3D(sample_points, scheme, 
                                      collapse_scalar, vert_scheme)
    
    def _to_timeseries_2D(self, sample_points, scheme, collapse_scalar):
        """Extract time-series for provided input coordinates (lon, lat)
        
        Todo
        ----
        Check Memory error handle
        
        Parameters
        ----------
        sample_points : list
            coordinates (e.g. lon / lat) at which time series is supposed to be
            retrieved
        scheme : str or iris interpolator object
            interpolation scheme (for details, see :func:`interpolate`)
        collapse_scalar : bool
            see :func:`interpolate`
            
        Returns
        -------
        list
            list of result dictionaries for each coordinate. Dictionary keys
            are: ``longitude, latitude, var_name``
        """
        if self.ndim != 3:
            raise Exception('Developers: Debug! Users: please contact '
                            'developers :)')
        
        data = self.interpolate(sample_points, scheme, collapse_scalar)
        var = self.var_name
        times = data.time_stamps()
        lats = [x[1] for x in sample_points if x[0] == "latitude"][0]
        lons = [x[1] for x in sample_points if x[0] == "longitude"][0]
        arr = data.grid.data
        grid_lons = data.longitude.points
        result = []
        for i, lat in enumerate(lats):
            lon = lons[i]
            j = np.where(grid_lons==lon)[0][0]
            
            data = StationData(latitude=lat, 
                               longitude=lon,
                               dataset_name=self.name)
            
            data[var] = Series(arr[:, i, j], index=times)
            result.append(data)
        return result

    def _check_vert_scheme(self, sample_points, vert_scheme):
        """Helper method that checks and infers vertical scheme for time
        series computation from 3D data (used in :func:`_to_timeseries_3D`)"""
        from pyaerocom import vert_coords as vc
        if 'altitude' in [sp[0] for sp in sample_points]:
            if not self._check_altitude_access():
                raise DataDimensionError('Cannot access altitude '
                                         'information')
            if vert_scheme is not None and not vert_scheme=='altitude':
                    raise ValueError('Conflict: Input sample points include ' 
                                     'altitude information but input for '
                                     'vert_scheme is {}'.format(vert_scheme))
            vert_scheme = 'altitude'
        elif vert_scheme == 'surface':
            #presume data dimensions have been sorted
            cname = self.dimcoord_names[-1]        
            if not vc.supported(cname):
                raise DataDimensionError('Vertical dimension coordinate {} is '
                                         'not supported. Cannot infer surface '
                                         'level'.format(cname))
        if vert_scheme is None:
            vert_scheme ='mean'
        return vert_scheme
    
    def _to_timeseries_3D(self, sample_points, scheme, collapse_scalar,
                          vert_scheme='profile'):

        # data contains vertical dimension
        vert_scheme = self._check_vert_scheme(sample_points, vert_scheme)
        if vert_scheme in ('altitude', 'profile'):
            raise NotImplementedError('Coming soon...')
        cname = self.dimcoord_names[-1]
        
        try:
            # check if vertical scheme can be converted into valid iris 
            # aggregator (in which case vertical dimension is collopsed)
            aggr = str_to_iris(vert_scheme)
            data = self.collapsed(cname, aggr)
        except KeyError:
            from pyaerocom import vert_coords as vc
            if vert_scheme == 'surface':
                cname = self.dimcoord_names[-1]
                coord = vc.VerticalCoordinate(cname)
                if coord.lev_increases_with_alt:
                    vert_index = np.argmin(self.grid.coord(cname).points)
                else:
                    vert_index = np.argmax(self.grid.coord(cname).points)
                data = self[:,:,:,vert_index]
        
                    
        return data.to_time_series(sample_points, scheme, 
                                   collapse_scalar)
        
    def to_time_series_single_coord(self, latitude, longitude):
        """Make time series dictionary of single location using neirest coordinate
        
        Todo
        ----
        Crop before extraction
        
        Parameters
        ----------
        latitude : float
            latitude of coordinate
        longitude : float
            longitude of coordinate
            
        Returns
        -------
        dict
            dictionary containing results
        """
        self.check_dimcoords_tseries()
        if not self.ndim == 3:
            raise NDimError('So far, timeseries can only be extracted '
                            'from 3 dimensional data...')
        lons = self.longitude.points
        lats = self.latitude.points
        lon_idx = np.argmin(np.abs(lons - longitude))
        lat_idx = np.argmin(np.abs(lats - latitude))
        times = self.time_stamps()
        data = self.grid.data[:, lat_idx, lon_idx]
        return {'latitude'      : latitude, 
                'longitude'     : longitude,
                'name'          : self.name,
                self.var_name   : Series(data, times)}
        
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
        if not any([x.name() == to_ts_type for x in cube.coords()]):
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
        suppl = {}
        suppl.update(self.suppl_info)
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
    
    def aerocom_filename(self, at_stations=False):
        """Filename of data following Aerocom 3 conventions
        
        Parameters
        ----------
        at_stations : str
            if True, then AtStations string will be included in filename
    
        Returns
        -------
        str
            generated file name based on what is in this object
        """
        from pyaerocom.io import FileConventionRead
        f = self.from_files[0]
        fconv = FileConventionRead().from_file(f)
        base_info = fconv.get_info_from_file(f)
    
        vert_pos = base_info['vert_pos']
        if vert_pos is None:
            vert_pos = 'UNDEFINED'
        if at_stations:
            vert_pos += 'AtStations'
            
        name = [fconv.name, self.name, self.var_name, vert_pos,
                str(pd.Timestamp(self.start).year), self.ts_type]
        return '_'.format(fconv.file_sep).join(name) + '.nc'
    
    def compute_at_stations_file(self, stat_lats=None, stat_lons=None,
                                 out_dir=None, savename=None,
                                 obs_data=None):
        """Creates and saves new netcdf file at input lat / lon coordinates
        
        This method can be used to reduce the size of too large grid files.
        It reduces the lon / lat dimensionality corresponding to the locations
        of the input lat / lon coordinates.
        
        Parameters
        ----------
        stat_lats 
        """
        from pyaerocom import UngriddedData, print_log
        print_log.info('Computing AtStations file. This may take a while')
        if isinstance(obs_data, UngriddedData):
            stat_lons = obs_data.longitude
            stat_lats = obs_data.latitude
        
        if not len(stat_lons) == len(stat_lats):
            raise ValueError('Longitude and latitude arrays need to have the '
                             'same length (since they are supposed to belong) '
                             'to station_coordinates')
        if out_dir is None:
            out_dir = const.CACHEDIR
        if savename is None:
            savename = self.aerocom_filename(at_stations=True)
        lons = self.longitude.points
        lats = self.latitude.points
        
        lon_idx = []
        lat_idx = []
        
        for lat, lon in zip(stat_lats, stat_lons):
            lon_idx.append(closest_index(lons, lon))
            lat_idx.append(closest_index(lats, lat))
        
        lon_idx = sorted(dict.fromkeys(lon_idx))
        lat_idx = sorted(dict.fromkeys(lat_idx))
        try:
            self.check_dimcoords_tseries()
        except DimensionOrderError:
            self.reorder_dimensions_tseries()
          
        subset = self[:, lat_idx][:,:,lon_idx]
        # make sure everything went well with the dimensions
        subset.check_dimcoords_tseries()
        path = subset.to_netcdf(out_dir, savename)
        print_log.info('Finished computing AtStations file.')
        return path
        
    def to_netcdf(self, out_dir, savename=None):
        """Save as netcdf file
        
        Paraemeters
        -----------
        out_dir : str
            output direcory (must exist)
        savename : :obj:`str`, optional
            name of file. If None, :func:`aerocom_filename` is used
            
        Returns
        -------
        str
            file path
        """
        if savename is None:
            savename = self.aerocom_filename()
        fp = os.path.join(out_dir, savename)
        iris.save(self.grid, fp)
        return fp
        
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
        if self._size_GB > self._MAX_SIZE_GB:
            raise MemoryError('Data is too large (grid size: {}, file: {} GB) '
                              'for interpolation (which requires loading data '
                              'into memory)'.format(self.shape, self._size_GB))
        if isinstance(scheme, str):
            scheme = str_to_iris(scheme)
        if not sample_points:
            sample_points = []
        sample_points.extend(list(coords.items()))
        print_log.info('Interpolating data of shape {}. This may take a while.'
                       .format(self.shape))
        try:
            itp_cube = self.grid.interpolate(sample_points, scheme, 
                                             collapse_scalar)
        except MemoryError:
            raise MemoryError("Interpolation failed since grid of interpolated "
                              "Cube is too large")
        print_log.info('Successfully interpolated cube')
        return GriddedData(itp_cube, **self.suppl_info)
    
    def regrid(self, other, scheme='areaweighted', **kwargs):
        """Regrid this grid to grid resolution of other grid
        
        Parameters
        ----------
        other : GriddedData
            other data object
        scheme : str
            regridding scheme (e.g. linear, neirest, areaweighted)
            
        Returns
        -------
        GriddedData 
            regridded data object (new instance, this object remains unchanged)
        """
        if not isinstance(other, GriddedData):
            other = GriddedData(other)
        if isinstance(scheme, str):
            scheme = str_to_iris(scheme, **kwargs)
            
        self._check_lonlat_bounds()
        other._check_lonlat_bounds()
        data_rg = self.grid.regrid(other.grid, scheme)
        suppl = od(**self.suppl_info)
        suppl['regridded'] = True
        return GriddedData(data_rg, **suppl)        
    
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
        if not isinstance(time_idx, int):
            try:
                t = to_pandas_timestamp(time_idx).to_datetime64()
                time_idx = np.argmin(abs(self.time_stamps() - t))
            except:
                raise ValueError('Failed to interpret input time stamp')
        
        from pyaerocom.plot.mapping import plot_griddeddata_on_map 
        
        data = self[time_idx].grid.data
        lons = self.longitude.points
        lats = self.latitude.points
        
        fig = plot_griddeddata_on_map(data, lons, lats, self.var_name, 
                                      xlim=xlim, ylim=ylim, **kwargs)
        
        try:
            t = cftime_to_datetime64(self.time[time_idx])[0]
            tstr = datetime2str(t, self.ts_type)
        except:
            tstr = datetime2str(self.time_stamps()[time_idx], 
                                self.ts_type)
        fig.axes[0].set_title("{} ({}, {})".format(self.name, 
                              self.var_name, tstr))
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
                                            self.start,
                                            self.stop))
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
    
    @property
    def _size_GB(self):
        """Size of original data files from which this object is created
        
        These method is intended to be used for operations that actually 
        require the *realisation* of the (lazy loaded) data. 
        """
        return sum([os.path.getsize(f) for f in self.from_files]) / 10**9
    
    def __getattr__(self, attr):
        return self[attr]
        
    
    def __getitem__(self, indices_or_attr):
        """x.__getitem__(y) <==> x[y]"""
        if isinstance(indices_or_attr, str):
            if indices_or_attr in self.__dict__:
                return self.__dict__[indices_or_attr]
            if not indices_or_attr in self.coord_names:
                raise AttributeError("'pyaerocom.GriddedData' object has no "
                                     "attribute '{}'".format(indices_or_attr))
            return self.grid.coord(indices_or_attr)
        sub = self.grid.__getitem__(indices_or_attr)
        return GriddedData(sub, **self.suppl_info)
    
    def __contains__(self, val):
        """Check if variable or coordinate matchs input string"""
        return val is self.name or val in self.coord_names
     
    def __dir__(self):
        return self.coord_names + super().__dir__()
    
    def __str__(self):
        """For now, use string representation of underlying data"""
        return ("pyaerocom.GriddedData: %s\nGrid data: %s"
                %(self.name, self.grid.__str__()))
    
    def __repr__(self):
        """For now, use representation of underlying data"""
        return "pyaerocom.GriddedData\nGrid data: %s" %self.grid.__repr__()
    
    #sorted out
    def _to_timeseries_iter_coords_2D(self, sample_points, scheme, 
                                      collapse_scalar):
        """Extract time-series for provided input coordinates (lon, lat)
        
        This method extracts the time-series at all input coordinates by 
        iterating over the coordinate locations, cropping the grid around the 
        coordinate and then interpolating it using
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
            are: ``latitude, longitude, altitude, var_name``
        """
        raise NotImplementedError
        if not scheme=="nearest":
            raise NotImplementedError
        self.check_dimcoords_tseries()
        
        lats, lons = None, None
        for val in sample_points:
            name, vals = val[0], val[1]
            if name == 'latitude':
                lats = vals
            elif name == 'longitude':
                lons = vals
        
        var = self.var_name
        times = self.time_stamps()
        grid_lats = self.latitude.points
        grid_lons = self.longitude.points
        result = []
        totnum = len(lats)
        for i, lat in enumerate(lats):
            if i%10 == 0:
                print('At coord {} of {}'.format(i+1, totnum))
            lon = lons[i]
            
            lat_idx = np.argmin(np.abs(grid_lats - lat))
            lon_idx = np.argmin(np.abs(grid_lons - lon))
            
            
            #: TODO review indexing [:,:] style vs. extract method vs. lazy data
            C = iris.Constraint(latitude=grid_lats[lat_idx],
                               longitude=grid_lons[lon_idx])
            
            sub = self.extract(C)
            
            vals = sub.grid.data
            #sub = self.grid[:, lat_idx, lon_idx]
            # first slice, then access data
            data = Series(vals, index=times)
            result.append({'latitude'   :   lat,
                           'longitude'  :   lon,
                           'name'       :   self.name, 
                            var         :   data})
        return result

                
if __name__=='__main__':
    import matplotlib.pyplot as plt
    import pyaerocom as pya
    
    plt.close("all")
    
    r = pya.io.ReadGridded('SPRINTARS-T213_AP3-CTRL2016-PD')
    d = r.read_var('ec550aer')
    RUN_OLD_STUFF = False
    
    reader = pya.io.ReadGridded('ECMWF_CAMS_REAN')
    data = reader.read_var('od550aer', 2010)
    
    t1 = data.to_time_series(longitude=[30], latitude=[40])
    ts = data.to_time_series_single_coord(longitude=30, latitude=40)
    
    if RUN_OLD_STUFF:
        from pyaerocom.io.testfiles import get
        from matplotlib.pyplot import figure
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
