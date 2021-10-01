#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from cf_units import Unit
from collections import OrderedDict as od

import os

import iris
from iris.analysis.cartography import area_weights
from iris.analysis import MEAN
from iris.exceptions import UnitConversionError
import numpy as np
import pandas as pd
from pathlib import Path

from pyaerocom import const, logger, print_log
from pyaerocom.helpers_landsea_masks import load_region_mask_iris
from pyaerocom.tstype import TsType
from pyaerocom.exceptions import (CoordinateError,
                                  DataDimensionError,
                                  DataExtractionError,
                                  DimensionOrderError,
                                  ResamplingError,
                                  TemporalResolutionError,
                                  VariableDefinitionError,
                                  VariableNotFoundError)

from pyaerocom.time_config import IRIS_AGGREGATORS, TS_TYPE_TO_NUMPY_FREQ
from pyaerocom.time_resampler import TimeResampler
from pyaerocom.helpers import (get_time_rng_constraint,
                               get_lon_rng_constraint,
                               get_lat_rng_constraint,
                               cftime_to_datetime64,
                               str_to_iris,
                               to_pandas_timestamp,
                               datetime2str,
                               isrange, isnumeric,
                               delete_all_coords_cube,
                               copy_coords_cube,
                               make_dummy_cube_latlon,
                               check_coord_circular,
                               extract_latlon_dataarray)

from pyaerocom.mathutils import closest_index, exponent
from pyaerocom.stationdata import StationData
from pyaerocom.region import Region
from pyaerocom.units_helpers import UALIASES
from pyaerocom.vert_coords import AltitudeAccess

class GriddedData(object):
    """pyaerocom object representing gridded data (e.g. model diagnostics)

    Gridded data refers to data that can be represented on a regular,
    multidimensional grid. In :mod:`pyaerocom` this comprises both model output
    and diagnostics as well as gridded level 3 satellite data, typically with
    dimensions `latitude, longitude, time` (for surface or columnar data) and
    an additional dimension `lev` (or similar) for vertically resolved data.

    Under the hood, this data object is based on (but
    not inherited from) the :class:`iris.cube.Cube` object, and makes large use
    of the therein implemented functionality (many methods implemented here in
    :class:`GriddedData` are simply wrappers for `Cube` methods.

    Note
    ----
    Note that the implemented functionality in this class is mostly limited to
    what is needed in the pyaerocom API (e.g. for :mod:`pyaerocom.colocation`
    routines or data import) and is not aimed at replacing or competing with
    similar data classes such as :class:`iris.cube.Cube` or
    :class:`xarray.DataArray`. Rather, dependent on the use case, one or
    another of such gridded data objects is needed for optimal processing,
    which is why :class:`GriddedData` provides methods and / or attributes to
    convert to or from other such data classes (e.g. :attr:`GriddedData.cube`
    is an instance of :class:`iris.cube.Cube` and method
    :func:`GriddedData.to_xarray` can be used to convert to
    :class:`xarray.DataArray`). Thus, :class:`GriddedData` can be considered
    rather high-level as compared to the other mentioned data classes from
    iris or xarray.


    Note
    ----
    Since :class:`GriddedData` object is based on the
    :class:`iris.cube.Cube` object it is optimised for netCDF files that follow
    the CF conventions and may not work out of the box for files that do not
    follow this standard.

    Parameters
    ----------
    input : :obj:`str:` or :obj:`Cube`
        data input. Can be a single .nc file or a preloaded iris Cube.
    var_name : :obj:`str`, optional
        variable name that is extracted if `input` is a file path. Irrelevant
        if `input` is preloaded Cube
    check_unit : bool
        if True, the assigned unit is checked and if it is an alias to another
        unit the unit string will be updated. It will print a warning if the
        unit is invalid or not equal the associated AeroCom unit for the input
        variable. Set `convert_unit_on_init` to True, if you want an
        automatic conversion to AeroCom units. Defaults to True.
    convert_unit_on_init : bool
        if True and if unit check indicates non-conformity with AeroCom unit
        it will be converted automatically, and warning will be printed if that
        conversion fails. Defaults to True.
    """
    _grid = None
    _GRID_IO = const.GRID_IO
    #: Req. order of dimension coordinates for time-series computation
    COORDS_ORDER_TSERIES = ['time', 'latitude', 'longitude']
    _MAX_SIZE_GB = 64 #maximum file size for in-memory operations

    SUPPORTED_VERT_SCHEMES = ['mean', 'max', 'min', 'surface', 'altitude',
                              'profile']

    _META_ADD = od(from_files           = [],
                   data_id              = 'n/d',
                   var_name_read        = 'n/d',
                   ts_type              = 'n/d',
                   vert_code            = None,
                   regridded            = False,
                   outliers_removed     = False,
                   computed             = False,
                   concatenated         = False,
                   region               = None,
                   reader               = None)

    def __init__(self, input=None, var_name=None,
                 check_unit=True, convert_unit_on_init=True,
                 **meta):

        if input is None:
            input = iris.cube.Cube([])

        self._grid = None
        self._reader = None
        #attribute used to store area weights (if applicable, see method
        #area_weights)
        self._area_weights = None
        self._altitude_access = None

        # list of coordinate names as returned by name() method of iris coordinate
        # will be filled upon access of coord_names
        self._coord_names = None
        # list of containing var_name attributes of all coordinates
        self._coord_var_names = None
        self._coord_standard_names = None
        self._coord_long_names = None

        if input:
            self.load_input(input, var_name)

        self.update_meta(**meta)
        if self.has_data and self.var_name is not None and check_unit:
            self.check_unit(convert_unit_on_init)

    @property
    def var_name(self):
        """Name of variable"""
        return self.grid.var_name

    @var_name.setter
    def var_name(self, val):
        """Name of variable"""
        if not isinstance(val, str):
            raise ValueError('Invalid input for var_name, need str, got {}'
                             .format(val))
        self.grid.var_name = val

    @property
    def var_name_aerocom(self):
        """AeroCom variable name"""
        try:
            return const.VARS[self.var_name].var_name_aerocom
        except Exception:
            return None

    @property
    def var_info(self):
        """Print information about variable"""
        if not self.var_name in const.VARS:
            try:
                return const.VARS[self.var_name_aerocom]
            except Exception:
                raise VariableDefinitionError('No default access available for '
                                              'variable {}'.format(self.var_name))
        return const.VARS[self.var_name]

    @property
    def ts_type(self):
        """
        Temporal resolution of data
        """
        if self.metadata['ts_type'] == 'n/d':
            const.print_log.warning('ts_type is not set in GriddedData, trying '
                                    'to infer.')
            self.infer_ts_type()

        return self.metadata['ts_type']

    @ts_type.setter
    def ts_type(self, val):
        TsType(val) # this will raise an error if input is invalid
        self.metadata['ts_type'] = val

    @property
    def vert_code(self):
        """
        Vertical code of data (e.g. Column, Surface, ModelLevel)
        """
        return self.metadata['vert_code']

    @property
    def standard_name(self):
        """
        Standard name of variable
        """
        return self.grid.standard_name

    @property
    def long_name(self):
        """Long name of variable"""
        return self.grid.long_name

    @long_name.setter
    def long_name(self, val):
        self.grid.long_name = val

    @property
    def unit_ok(self):
        """Boolean specifying if variable unit is AeroCom default"""
        return self.check_unit()

    @property
    def suppl_info(self):
        w = DeprecationWarning('Outdated attribute suppl_info. Please use '
                               'metadata instead')
        const.print_log.warning(w)
        return self.metadata

    @property
    def metadata(self):
        return self.cube.attributes


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
    def reader(self):
        """Instance of reader class from which this object was created"""
        r = self._reader
        from pyaerocom.io import ReadGridded
        if not isinstance(r, ReadGridded):
            self._reader = r = ReadGridded(self.data_id)
        return r

    @reader.setter
    def reader(self, val):
        self._reader = val

    @property
    def concatenated(self):
        return self.metadata['concatenated']

    @property
    def computed(self):
        return self.metadata['computed']

    @property
    def units(self):
        """Unit of data"""
        return self.grid.units

    @units.setter
    def units(self, val):
        self.grid.units = val

    @property
    def data(self):
        """Data array (n-dimensional numpy array)

        Note
        ----
        This is a pointer to the data object of the underlying iris.Cube
        instance and will load the data into memory. Thus, in case of large
        datasets, this may lead to a memory error
        """
        return self.grid.data

    @data.setter
    def data(self, array):
        if not isinstance(array, np.ndarray):
            raise ValueError('Cannot set data array: need numpy.ndarray')
        elif not array.shape == self.grid.data.shape:
            raise DataDimensionError('Cannot assign dataarray: shape mismatch. '
                                     'Got: {}, Need: {}'
                                     .format(array.shape,self.grid.shape))
        self.grid.data = array

    @property
    def altitude_access(self):
        if not isinstance(self._altitude_access, AltitudeAccess):
            self._altitude_access = AltitudeAccess(self)
        return self._altitude_access

    @property
    def delta_t(self):
        """Array containing timedelta values for each time stamp"""
        ts = self.time_stamps()
        if len(ts) < 2:
            raise AttributeError('Need at least 2 timestamps in GriddedData in '
                                 'order to compute delta-t')
        return (ts[1:] - ts[0:-1])

    def check_frequency(self):
        """Check if all datapoints are sampled at the same time frequency"""
        dt = np.unique(self.delta_t)
        if len(dt) > 1:
            raise AttributeError('Irregular time-frequency')
        freq = TS_TYPE_TO_NUMPY_FREQ[self.ts_type]
        if not int(dt.astype('timedelta64[{}]'.format(freq))) == 1:
            raise AttributeError('Mismatch between sampling freq and '
                                 'actual frequency of values in time dimension ')

    def infer_ts_type(self):
        """Try to infer sampling frequency from time dimension data

        Returns
        -------
        str
            ts_type that was inferred (is assigned to metadata too)

        Raises
        ------
        DataDimensionError
            if data object does not contain a time dimension
        """
        if not self.has_time_dim:
            raise DataDimensionError('Cannot infer frequency. Data has no time '
                                     'dimension')
        dt = np.unique(self.delta_t)
        if len(dt) > 1:
            raise ValueError('Could not identify unique frequency')
        dt = dt[0]
        for ts_type, freq in TS_TYPE_TO_NUMPY_FREQ.items():
            val = dt.astype('timedelta64[{}]'.format(freq)).astype(int)
            if val == 1:
                self.metadata['ts_type'] = ts_type
                return ts_type
        raise AttributeError('Failed to infer ts_type from data')

    @property
    def TS_TYPES(self):
        """List with valid filename encryptions specifying temporal resolution
        """
        return self.io_opts.GRID_IO.TS_TYPES

    @property
    def from_files(self):
        """List of file paths from which this data object was created"""
        return self.metadata['from_files']

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
    def base_year(self):
        """Base year of time dimension

        Note
        ----
        Changing this attribute will update the time-dimension.
        """
        if not self.has_time_dim:
            raise DataDimensionError('Could not access base year: data has no '
                                     'time dimension')
        try:
            return self.time.units.utime().origin.year
        except Exception as e:
            raise DataDimensionError('Could access base-year. Unexpected error: '
                                     '{}'.format(repr(e)))

    @base_year.setter
    def base_year(self, val):
        self.change_base_year(val)

    def change_base_year(self, new_year, inplace=True):
        """
        Changes base year of time dimension

        Relevant, e.g. for climatological analyses.

        ToDo
        ----
        Account for leap years.

        Note
        ----
        This method does not account for offsets arising from leap years (
        affecting daily or higher resolution data).
        It is thus recommended to use this method with care. E.g. if you use
        this method on a 2016 daily data object, containing a calendar that
        supports leap years, you'll end up with 366 time stamps also in the new
        data object.

        Parameters
        -----------
        new_year : int
            new base year (can also be other than integer if it is convertible)
        inplace : bool
            if True, modify this object, else, use a copy

        Returns
        -------
        GriddedData
            modified data object
        """
        if inplace:
            data = self
        else:
            data = self.copy()
        from pyaerocom.io.iris_io import correct_time_coord
        data.cube = correct_time_coord(data.cube, data.ts_type, new_year)
        return data

    @property
    def start(self):
        """Start time of dataset as datetime64 object"""
        if not self.has_time_dim:
            raise ValueError('GriddedData has no time dimension')
        t = cftime_to_datetime64(self.time[0])[0]

        #try:
        # ToDo: check if this is needed
        np_freq = TsType(self.ts_type).to_numpy_freq() #TS_TYPE_TO_NUMPY_FREQ[self.ts_type]
        dtype_appr = 'datetime64[{}]'.format(np_freq)
        t=t.astype(dtype_appr)
# =============================================================================
#         except Exception:
#             logger.exception('Failed to round start time {} to beginning of '
#                              'frequency {}'.format(t, self.ts_type))
# =============================================================================
        return t.astype('datetime64[us]')

    @property
    def stop(self):
        """Start time of dataset as datetime64 object"""
        if not self.has_time_dim:
            raise ValueError('GriddedData has no time dimension')
        t = cftime_to_datetime64(self.time[-1])[0]

        np_freq = TsType(self.ts_type).to_numpy_freq() #TS_TYPE_TO_NUMPY_FREQ[self.ts_type]
        dtype_appr = 'datetime64[{}]'.format(np_freq)

        t = t.astype(dtype_appr) + np.timedelta64(1, np_freq)
        t = t.astype('datetime64[us]') - np.timedelta64(1,'us')
        return t

    @property
    def cube(self):
        """Instance of underlying cube object"""
        return self.grid

    @cube.setter
    def cube(self, val):
        """Instance of underlying cube object"""
        self.grid = val

    @property
    def grid(self):
        """Underlying grid data object"""
        return self._grid

    @grid.setter
    def grid(self, value):
        if not isinstance(value, iris.cube.Cube):
            raise TypeError("Grid data format %s is not supported, need Cube"
                            %type(value))

        for key, val in self._META_ADD.items():
            if not key in value.attributes:
                value.attributes[key] = val
        self._grid = value

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
        return const.VARS[self.var_name]

    @property
    def name(self):
        """ID of model to which data belongs"""
        logger.warning('Deprecated attribute name, please use data_id instead')
        return self.metadata["data_id"]

    @property
    def data_id(self):
        """ID of data object (e.g. model run ID, obsnetwork ID)

        Note
        ----
        This attribute was formerly named ``name`` which is alse the
        corresponding attribute name in :attr:`metadata`
        """
        try:
            return self.metadata['data_id']
        except KeyError:
            return 'undefined'

    @property
    def is_climatology(self):
        ff = self.from_files
        if len(ff) == 1 and '9999' in os.path.basename(ff[0]):
            return True
        return False

    @property
    def has_data(self):
        """True if sum of shape of underlying Cube instance is > 0, else False
        """
        return True if bool(sum(self._grid.shape)) else False

    @property
    def shape(self):
        return self._grid.shape

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
        elif self._coord_names is None:
            self._update_coord_info()
        return self._coord_names

    @property
    def dimcoord_names(self):
        """List containing coordinate names"""
        if not self.has_data:
            return []
        return [c.name() for c in self.grid.dim_coords]

    @property
    def area_weights(self):
        """Area weights of lat / lon grid"""
        if self._area_weights is None:
            self.calc_area_weights()
        return self._area_weights

    @area_weights.setter
    def area_weights(self, val):
        raise AttributeError("Area weights cannot be set manually yet...")

    @property
    def has_latlon_dims(self):
        """Boolean specifying whether data has latitude and longitude dimensions"""
        return all([dim in self.dimcoord_names for dim in ['latitude',
                                                           'longitude']])
    @property
    def has_time_dim(self):
        """Boolean specifying whether data has latitude and longitude dimensions"""
        return 'time' in self.dimcoord_names

    def _read_netcdf(self, input, var_name, perform_fmt_checks):
        from pyaerocom.io.iris_io import load_cube_custom
        self.grid = load_cube_custom(input, var_name,
                                     perform_fmt_checks=perform_fmt_checks)
        if not 'from_files' in self.metadata:
            self.metadata['from_files'] = []
        elif not isinstance(self.metadata["from_files"], list):
            self.metadata["from_files"] = [self.metadata["from_files"]]
        self.metadata["from_files"].append(input)
        try:
            from pyaerocom.io.helpers import get_metadata_from_filename
            self.update_meta(**get_metadata_from_filename(input))
        except Exception:
            logger.warning('Failed to access metadata from filename')

    def load_input(self, input, var_name=None, perform_fmt_checks=None):
        """Import input as cube

        Parameters
        ----------
        input : :obj:`str:` or :obj:`Cube`
            data input. Can be a single .nc file or a preloaded iris Cube.
        var_name : :obj:`str`, optional
            variable name that is extracted if `input` is a file path . Irrelevant
            if `input` is preloaded Cube
        perform_fmt_checks : bool, optional
            perform formatting checks based on information in filenames. Only
            relevant if input is a file

        """
        if isinstance(input, iris.cube.Cube):
            self.grid = input #instance of Cube
        elif isinstance(input, Path) and input.exists():
            self._read_netcdf(str(input), var_name, perform_fmt_checks)
        elif isinstance(input, str) and os.path.exists(input):
            self._read_netcdf(input, var_name, perform_fmt_checks)
        else:
            raise IOError('Failed to load input: {}'.format(input))

        if var_name is not None and self.var_name != var_name:
            try:
                self.var_name = var_name
            except ValueError:
                const.print_log.warning('Could not update var_name, invalid input '
                                     '{} (need str)'.format(var_name))

    def _check_invalid_unit_alias(self):
        """Check for units that have been invalidated by iris

        iris lib relies on CF conventions and if the unit in the NetCDF file
        is invalid, it will set the variable unit to UNKNOWN and put the
        actually provided unit into the attributes. pyaerocom can handle
        some of these invalid units, which is checked here and updated
        accordingly

        Parameters
        ----------
        cube : iris.cube.Cube
            loaded instance of data Cube

        Returns
        -------
        iris.cube.Cube
            input cube that has been checked for supported units and updated
            if applicable
        """
        cube = self.grid
        if ('invalid_units' in cube.attributes and
            cube.attributes['invalid_units'] in UALIASES):

            from_unit = cube.attributes['invalid_units']
            to_unit = UALIASES[from_unit]
            const.print_log.info('Updating invalid unit in {} from {} to {}'
                                 .format(repr(cube), from_unit, to_unit))
            del cube.attributes['invalid_units']
            cube.units = to_unit
        return cube

    def check_unit(self, try_convert_if_wrong=False):
        """Check if unit is correct"""
        from pyaerocom.exceptions import VariableDefinitionError
        self._check_invalid_unit_alias()
        unit_ok = False
        to_unit = None
        try:
            var = const.VARS[self.cube.var_name]
            to_unit = var.units
            current_unit = self.units
            if to_unit == current_unit: # string match e.g. both are m-1
                unit_ok = True
            elif Unit(to_unit).convert(1, current_unit) == 1:
                self.units = to_unit
                const.print_log.info(
                   f'Updating unit string from {current_unit} to {to_unit} '
                   f'in GriddedData.')
                unit_ok = True
        except (VariableDefinitionError, ValueError):
            pass

        if not unit_ok and try_convert_if_wrong and isinstance(to_unit, str):
            const.print_log.warning(
                f'Unit {self.units} in GriddedData {self.short_str()} is not '
                f'AeroCom conform ({to_unit}). Trying to convert ... '
                )
            try:
                self.convert_unit(to_unit)
                unit_ok = True
            except Exception as e:
                const.print_log.warning(
                    f'Failed to convert unit from {self.units} to {to_unit}. '
                    f'Reason: {e}')

        return unit_ok

    def _try_convert_non_cf_unit(self, new_unit):
        import pyaerocom.units_helpers as uh
        from pyaerocom.time_config import SI_TO_TS_TYPE
        current = str(self.units)
        # check if it is deposition and if units are implicit
        try:
            mulfac = uh.get_unit_conversion_fac(from_unit=current,
                                                to_unit=new_unit,
                                                var_name=self.var_name)
            self._apply_unit_mulfac(new_unit, mulfac)

        except Exception as e:
            if self.var_info.is_rate:
                unit = current
                if not unit.endswith('-1'):
                    self.units = unit = str(
                        uh.check_rate_units_implicit(unit, self.ts_type))

                cf_freq = unit.split()[-1].split('-1')[0]

                if not cf_freq in SI_TO_TS_TYPE:
                    raise ValueError(f'Invalid rate unit {unit}, must end with '
                                     f' h-1, d-1, etc...')

                check_to = unit.replace(f'{cf_freq}-1', f'{uh.RATES_FREQ_DEFAULT}-1')
                fac1 =  uh.get_unit_conversion_fac(unit,
                                                   check_to) # e.g. h-1 -> d-1

                fac2 = uh.get_unit_conversion_fac(
                            check_to,
                            new_unit,
                            self.var_name) # kg N m-2 d-1 -> kg m-2 d-1
                mulfac = fac1*fac2
                self._apply_unit_mulfac(new_unit,
                                        mulfac)

            else:
                raise UnitConversionError(
                    f'Failed to convert unit to {new_unit} in '
                    f'{self.short_str()}. Reason: {repr(e)}')
            const.print_log.info(
                f'Succesfully converted unit from {current} to {new_unit} in '
                f'{self.short_str()}')

    def _apply_unit_mulfac(self, new_unit, mulfac):

        if mulfac != 1:
            new_cube = self._grid * mulfac
            new_cube.attributes.update(self._grid.attributes)
            new_cube.var_name = self.var_name
            self._grid = new_cube
        self.units = new_unit
        return self

    def convert_unit(self, new_unit, inplace=True):
        """Convert unit of data to new unit

        Parameters
        ----------
        new_unit : str or cf_units.Unit
            new unit of data
        inplace : bool
            convert in this instance or create a new one
        """
        data_out = self if inplace else self.copy()
        try:
            data_out.grid.convert_units(new_unit)
        except ValueError as e:
            data_out._try_convert_non_cf_unit(new_unit)
        return data_out

    def time_stamps(self):
        """Convert time stamps into list of numpy datetime64 objects

        The conversion is done using method :func:`cfunit_to_datetime64`

        Returns
        -------
        list
            list containing all time stamps as datetime64 objects
        """
        if self.has_time_dim:
            return cftime_to_datetime64(self.time)

    def years_avail(self):
        """
        Generate list of years that are available in this dataset

        Returns
        -------
        list

        """
        toyear = lambda x: int(str(x.astype('datetime64[Y]')))

        return [x for x in set(map(toyear, self.time_stamps()))]

    def split_years(self, years=None):
        """
        Generator to split data object into individual years

        Note
        ----
        This is a generator method and thus should be looped over

        Parameters
        ----------
        years : list, optional
            List of years that should be excluded. If None, it uses output
            from :func:`years_avail`.

        Yields
        ------
        GriddedData
            single year data object

        """

        from pyaerocom.helpers import start_stop_from_year
        if years is None:
            years = self.years_avail()
        if len(years) == 1:
            const.print_log.info('Nothing to split... GriddedData contains '
                                 'only {}'.format(years[0]))
            yield self
        for year in years:
            start, stop = start_stop_from_year(year)
            yield self.crop(time_range=(start, stop))

    def check_coord_order(self):
        """Wrapper for :func:`check_dimcoords_tseries`"""
        logger.warning(DeprecationWarning('Method was renamed, please use '
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
        DataDimensionError
            if dimension of data is not supported (currently, 3D or 4D data
            is supported)
        DimensionOrderError
            if dimensions are not in the right order (in which case
            :func:`reorder_dimensions_tseries` may be used to catch the
            Exception)
        """
        if not self.ndim in (3,4):
            raise DataDimensionError('Time series extraction requires at least 3 '
                            'coordinates in cube')

        order = self.COORDS_ORDER_TSERIES
        for i, coord in enumerate(order):
            dims = self.cube.coord_dims(coord)
            if len(dims) == 0:
                raise DataDimensionError('Coord {} is not associated with a '
                                         'data dimension in cube'
                                         .format(coord))
            elif len(dims) > 1:
                raise NotImplementedError('Coord {} is associated with '
                                          'multiple dimensions. This cannot '
                                          'yet be handled...'.format(coord))

            if not dims[0] == i:
                raise DimensionOrderError('Invalid order of grid dimensions')

    def reorder_dimensions_tseries(self):
        """Reorders dimensions of data such that :func:`to_time_series` works
        """
        order = self.COORDS_ORDER_TSERIES
        new_order = []
        #coord_names = [c.name() for c in self.grid.dim_coords]
        for coord in order:
            dims = self.cube.coord_dims(coord)
            if len(dims) == 0:
                raise DataDimensionError('Coord {} is not associated with a '
                                         'data dimension in cube'
                                         .format(coord))
            elif len(dims) > 1:
                raise NotImplementedError('Coord {} is associated with '
                                          'multiple dimensions. This cannot '
                                          'yet be handled...'.format(coord))
            new_order.append(dims[0])

        if not len(new_order) == self.ndim:
            for i in range(self.ndim):
                if not i in new_order:
                    new_order.append(i)
        self.transpose(new_order)
        self.check_dimcoords_tseries()

    def reorder_dimensions_tseries_old(self):
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

        Wrapper for :func:`iris.cube.Cube.transpose`

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

    def mean_at_coords(self, latitude=None, longitude=None,
                       time_resample_kwargs=None, **kwargs):
        """Compute mean value at all input locations

        Parameters
        ----------
        latitude : 1D list or similar
            list of latitude coordinates of coordinate locations. If None,
            please provided coords in iris style as list of (lat, lon) tuples
            via `coords` (handled via arg kwargs)
        longitude : 1D list or similar
            list of longitude coordinates of coordinate locations. If None,
            please provided coords in iris style as list of (lat, lon) tuples
            via `coords` (handled via arg kwargs)
        time_resample_kwargs : dict, optional
            time resampling arguments passed to
            :func:`StationData.resample_time`
        **kwargs
            additional keyword args passed to :func:`to_time_series`

        Returns
        -------
        float
            mean value at coordinates over all times available in this object

        """
        ts = self.to_time_series(latitude=latitude,
                                 longitude=longitude,
                                 **kwargs)
        mean =  []
        for stat in ts:
            if isinstance(time_resample_kwargs, dict):
                stat.resample_time(self.var_name,
                                   inplace=True,
                                   **time_resample_kwargs)
            data = stat[self.var_name].values
            if len(data) > 0:
                data = np.nanmean(data)
            mean.append(data)
        return np.nanmean(mean)

    def _coords_to_iris_sample_points(self, **coords):

        sample_points = []
        num = None
        for cname, vals in coords.items():
            if isnumeric(vals):
                vals= [vals]
            if num is None:
                num = len(vals)
            elif num != len(vals):
                raise ValueError('All coord arrays need to have same length')
            sample_points.append((cname, vals))
        return sample_points

    def _iris_sample_points_to_coords(self, sample_points):
        lats, lons = None, None
        for (name, vals) in sample_points:
            if isnumeric(vals):
                vals = [vals]
            if name in ('lat', 'latitude'):
                lats = vals
            elif name in ('lon', 'longitude'):
                lons = vals
        if not lats or not lons or not len(lats) == len(lons):
            raise ValueError('Could not extract latitude or longitude info '
                             'from sampling_points or both input arrays '
                             'do not have the same lenght')

        return dict(lat=lats, lon=lons)

    def to_time_series(self, sample_points=None, scheme="nearest",
                       vert_scheme=None, add_meta=None, use_iris=False,
                       **coords):

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
        add_meta : dict, optional
            dictionary specifying additional metadata for individual input
            coordinates. Keys are meta attribute names (e.g. station_name)
            and corresponding values are lists (with length of input coords)
            or single entries that are supposed to be assigned to each station.
            E.g. `add_meta=dict(station_name=[<list_of_station_names>])`).
        **coords
            additional keyword args that may be used to provide the interpolation
            coordinates (for details, see :func:`interpolate`)

        Returns
        -------
        list
            list of result dictionaries for each coordinate. Dictionary keys
            are: ``longitude, latitude, var_name``
        """
        if 'collapse_scalar' in coords: #for backwards compatibility
            collapse_scalar = coords.pop('collapse_scalar')
        else:
            collapse_scalar = True
        try:
            self.check_dimcoords_tseries()
        except DimensionOrderError:
            self.reorder_dimensions_tseries()
        pinfo = False
        if np.prod(self.shape) > 5913000: # (shape of 2x2 deg, daily data)
            pinfo = True
            from time import time
            t0 = time()
            const.print_log.info('Extracting timeseries data from large array '
                                 '(shape: {}). This may take a while...'
                                 .format(self.shape))
        # if the method makes it to this point, it is 3 or 4 dimensional
        # and the first 3 dimensions are time, latitude, longitude.
# =============================================================================
#         lens = [len(x[1]) for x in sample_points]
#         if not all([lens[0]==x for x in lens]):
#             raise ValueError("Arrays for sample coordinates must have the "
#                              "same lengths")
# =============================================================================
        if self.ndim == 3: #data does not contain vertical dimension
            if use_iris:
                if sample_points is None:
                    sample_points = self._coords_to_iris_sample_points(**coords)
                result = self._to_timeseries_2D(sample_points, scheme,
                                                collapse_scalar=collapse_scalar,
                                                add_meta=add_meta)
            else:
                if not coords:
                    coords = self._iris_sample_points_to_coords(sample_points)
                result = self._to_time_series_xarray(scheme=scheme,
                                                     add_meta=add_meta,
                                                     **coords)
            if pinfo:
                const.print_log.info('Time series extraction successful. '
                                     'Elapsed time: {:.0f} s'
                                     .format(time() - t0))
            return result

        if sample_points is None:
            sample_points = self._coords_to_iris_sample_points(**coords)
        return self._to_timeseries_3D(sample_points, scheme,
                                      collapse_scalar=collapse_scalar,
                                      vert_scheme=vert_scheme,
                                      add_meta=add_meta)

    def _to_time_series_xarray(self, scheme='nearest',
                               add_meta=None, ts_type=None, **coords):

        try:
            self.check_dimcoords_tseries()
        except DimensionOrderError:
            self.reorder_dimensions_tseries()

        arr = self.to_xarray()

        if not len(coords) == 2:
            raise NotImplementedError('Please provide only latitude / longitude '
                                      'sampling points as input')
        for coord, vals in coords.items():
            if coord in ('lat', 'latitude'):
                if isinstance(vals, str) or isnumeric(vals):
                    vals = [vals]
                lat = vals
            elif coord in ('lon', 'longitude'):
                if isinstance(vals, str) or isnumeric(vals):
                    vals = [vals]
                lon = vals
        if lat is None or lon is None:
            raise ValueError('Please provide latitude and longitude coords')
        subset = extract_latlon_dataarray(arr, lat, lon, method=scheme,
                                          new_index_name='latlon')

        lat_id = subset.attrs['lat_dimname']
        lon_id = subset.attrs['lon_dimname']
        var = self.var_name
        times = self.time_stamps()

        meta_iter = {}
        meta_glob = {}
        if add_meta is not None:
            for meta_key, meta_val in add_meta.items():
                try:
                    if not len(meta_val) == len(lon):
                        raise ValueError
                    meta_iter[meta_key] = meta_val
                except Exception:
                    meta_glob[meta_key] = meta_val

        result = []
        subset = subset.compute()
        data_np = subset.data
        lats = subset[lat_id].data
        lons = subset[lon_id].data
        for sidx in range(subset.shape[-1]):

            data = StationData(latitude=lats[sidx],
                               longitude=lons[sidx],
                               data_id=self.name,
                               ts_type=self.ts_type)

            data.var_info[var] = {'units':self.units}

            vals = data_np[:, sidx]

            data[var] = pd.Series(vals, index=times)
            for meta_key, meta_val in meta_iter.items():
                data[meta_key] = meta_val[sidx]
            for meta_key, meta_val in meta_glob.items():
                data[meta_key] = meta_val

            if ts_type is not None:
                data.resample_time(var, ts_type, how='mean', inplace=True)
            result.append(data)
        return result

    def _to_timeseries_2D(self, sample_points, scheme, collapse_scalar,
                          add_meta=None, ts_type=None):
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

        #lats, lons = tuple_list_to_lists(sample_points)
        lats = [x[1] for x in sample_points if x[0] == "latitude"][0]
        lons = [x[1] for x in sample_points if x[0] == "longitude"][0]
        arr = data.grid.data
        grid_lons = data.longitude.points
        result = []
        meta_iter = {}
        meta_glob = {}
        if add_meta is not None:
            for meta_key, meta_val in add_meta.items():
                try:
                    if not len(meta_val) == len(lons):
                        raise ValueError
                    meta_iter[meta_key] = meta_val
                except Exception:
                    meta_glob[meta_key] = meta_val

        for i, lat in enumerate(lats):
            lon = lons[i]
            j = np.where(grid_lons==lon)[0][0]

            data = StationData(latitude=lat,
                               longitude=lon,
                               data_id=self.name,
                               ts_type=self.ts_type)
            data.var_info[var] = {'units':self.units}
            vals = arr[:, i, j]

            data[var] = pd.Series(vals, index=times)
            for meta_key, meta_val in meta_iter.items():
                data[meta_key] = meta_val[i]
            for meta_key, meta_val in meta_glob.items():
                data[meta_key] = meta_val

            if ts_type is not None:
                data.resample_time(var, ts_type, how='mean', inplace=True)
            result.append(data)

        return result

    def _to_timeseries_3D(self, sample_points, scheme, collapse_scalar,
                          vert_scheme='surface', add_meta=None):

        # Data contains vertical dimension
        data = self._apply_vert_scheme(sample_points, vert_scheme)

        # ToDo: check if _to_timeseries_2D can be called here
        return data.to_time_series(sample_points, scheme,
                                   collapse_scalar, add_meta=add_meta)

    def _apply_vert_scheme(self, sample_points, vert_scheme=None):
        """Helper method that checks and infers vertical scheme for time
        series computation from 3D data (used in :func:`_to_timeseries_3D`)"""

        if vert_scheme is None:
            const.print_log.info('Setting vert_scheme in GriddedData to mean')
            vert_scheme ='mean'
        try:
            self.check_dimcoords_tseries()
        except DimensionOrderError:
            self.reorder_dimensions_tseries()

        cname = self.dimcoord_names[-1]

        if not vert_scheme in self.SUPPORTED_VERT_SCHEMES:
            raise ValueError('Invalid input for vert_scheme: {}. Supported '
                             'schemes are: {}'
                             .format(vert_scheme, self.SUPPORTED_VERT_SCHEMES))
        if vert_scheme == 'surface':
            vert_index = self._infer_index_surface_level()
            return self[:,:,:,vert_index]
        elif vert_scheme == 'altitude':
            if not 'altitude' in [sp[0] for sp in sample_points]:
                raise ValueError('Require altitude specification in sample '
                                 'points for vert_scheme altitude')
            if not self.check_altitude_access():
                raise DataDimensionError('Cannot access altitude '
                                         'information')
            raise NotImplementedError('Cannot yet retrieve timeseries at '
                                      'altitude levels. Coming soon...')
        elif vert_scheme == 'profile':
            raise NotImplementedError('Cannot yet retrieve profile timeseries')
        else:
            try:
                # check if vertical scheme can be converted into valid iris
                # aggregator (in which case vertical dimension is collapsed)
                aggr = str_to_iris(vert_scheme)
            except KeyError:
                pass
            else:
                return self.collapsed(cname, aggr)

        raise NotImplementedError('Cannot yet retrieve timeseries '
                                  'from 4D data for vert_scheme {} '
                                  .format(vert_scheme))

    def check_altitude_access(self):
        """Checks if altitude levels can be accessed

        Returns
        -------
        bool
            True, if altitude access is provided, else False

        """
        return self.altitude_access.check_altitude_access()

    def get_altitude(self, **coords):
        """Extract (or try to compute) altitude values at input coordinates"""
        if not isinstance(self._altitude_access, AltitudeAccess):
            self.check_altitude_access()
        self._altitude_access.get_altitude(**coords)
        raise NotImplementedError('Coming soon...')

    def extract_surface_level(self):
        """Extract surface level from 4D field"""
        if not self.ndim==4:
            raise DataDimensionError('Can only extract surface level for 4D '
                                     'gridded data object')
        idx = self._infer_index_surface_level()
        return self[:,:,:,idx]

    def _infer_index_surface_level(self):
        if not self.ndim == 4:
            raise DataDimensionError('Can only infer surface level for 4D '
                                     'gridded data object')
        try:
            self.check_dimcoords_tseries()
        except DimensionOrderError:
            self.reorder_dimensions_tseries()
        cname = self.dimcoord_names[-1]
        coord = self[cname]
        from pyaerocom import vert_coords as vc
        if 'positive' in coord.attributes:
            if coord.attributes['positive'] == 'up':
                return np.argmin(self.grid.dim_coords[3].points)
            elif coord.attributes['positive'] == 'down':
                return np.argmax(self.grid.dim_coords[3].points)

        try:
            coord = vc.VerticalCoordinate(cname)
            if coord.lev_increases_with_alt:
                # vertical coordinate values increase with altitude -> find lowest value (e.g. altitude)
                return np.argmin(self.grid.dim_coords[3].points)
            else:
                # vertical coordinate values decrease with altitude -> find highest value (e.g. pressure)
                return np.argmax(self.grid.dim_coords[3].points)
        except Exception:
            if not const.GRID_IO.INFER_SURFACE_LEVEL:
                raise DataExtractionError('Cannot infer surface level since '
                                          'global option INFER_SURFACE_LEVEL in'
                                          'pyaerocom.const.GRID_IO is deactivated')
            const.print_log.info(
                'Inferring surface level in GriddedData based on mean value of '
                '{} data in first and last level since CF coordinate info is '
                'missing... The level with the largest mean value will be '
                'assumed to be the surface. If mean values in both levels'
                .format(self.var_name))
            last_lev_idx = self.shape[-1] - 1
            mean_first_idx = np.nanmean(self[0, :, :, 0].data)
            mean_last_idx = np.nanmean(self[0, :, :, last_lev_idx].data)
            if exponent(mean_first_idx) == exponent(mean_last_idx):
                raise DataExtractionError('Could not infer surface level. '
                    '{} data in first and last level is of similar magnitude...'
                    .format(self.var_name))
            elif mean_first_idx > mean_last_idx:
                return 0
            return last_lev_idx

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
        raise NameError(DeprecationWarning('This method is deprecated since '
                                           'version 0.8.0'))
# =============================================================================
#         self.check_dimcoords_tseries()
#         if not self.ndim == 3:
#             raise DataDimensionError('So far, timeseries can only be extracted '
#                                      'from 3 dimensional data...')
#         lons = self.longitude.points
#         lats = self.latitude.points
#         lon_idx = np.argmin(np.abs(lons - longitude))
#         lat_idx = np.argmin(np.abs(lats - latitude))
#         times = self.time_stamps()
#         data = self.grid.data[:, lat_idx, lon_idx]
#         return {'latitude'      : latitude,
#                 'longitude'     : longitude,
#                 'name'          : self.name,
#                 self.var_name   : pd.Series(data, times)}
# =============================================================================

    def _closest_time_idx(self, t):
        """Find closest index to input in time dimension"""
        t = self.time.units.date2num(to_pandas_timestamp(t))
        return self.time.nearest_neighbour_index(t)

    def find_closest_index(self, **dimcoord_vals):
        """Find the closest indices for dimension coordinate values"""
        idx = {}
        for dim, val in dimcoord_vals.items():
            if not dim in self.coord_names:
                raise DataDimensionError('No such dimension {}'.format(dim))
            elif dim == 'time':
                idx[dim] = self._closest_time_idx(val)
            else:
                idx[dim] = self[dim].nearest_neighbour_index(val)
        return idx

    def isel(self, **kwargs):
        raise NotImplementedError('Please use method sel for data selection '
                                  'based on dimension values')

    def sel(self, use_neirest=True, **dimcoord_vals):
        """Select subset by dimension names

        Note
        ----
        This is a BETA version, please use with care

        Parameters
        ----------
        **dimcoord_vals
            key / value pairs specifying coordinate values to be extracted

        Returns
        -------
        GriddedData
            subset data object
        """
        constraints = []
        rng_funs = {'time'   : get_time_rng_constraint,
                    'longitude' : get_lon_rng_constraint,
                    'latitude' : get_lat_rng_constraint}

        coord_vals = {}
        for dim, val in dimcoord_vals.items():
            is_rng = isrange(val)
            if is_rng:
                c = rng_funs[dim](*val)
                constraints.append(c)
            else:
                if dim == 'time':
                    if isnumeric(val) and val in self['time'].points:
                        _tval = val
                    else:
                        _idx = self._closest_time_idx(val)
                        _tval = self.time[_idx].points[0]
                    _cval = self['time'].units.num2date(_tval)
                    if not use_neirest and _cval != val:
                        raise DataExtractionError('No such value {} in dim {}. '
                                                  'Use option use_neirest to '
                                                  'disregard and extract '
                                                  'neirest neighbour'.format
                                                  (val, dim))
                else:
                    _idx = self[dim].nearest_neighbour_index(val)
                    _cval = self[dim][_idx].points[0]
                    if not use_neirest and _cval != val:
                        raise DataExtractionError('No such value {} in dim {}'
                                                  'Use option use_neirest to '
                                                  'disregard and extract '
                                                  'neirest neighbour'.format
                                                  (val, dim))
                coord_vals[dim] = _cval

        if coord_vals:
            constraints.append(iris.Constraint(coord_values=coord_vals))

        if len(constraints) > 0:
            c = constraints[0]
            for cadd in constraints[1:]:
                c = c & cadd
        subset = self.extract(c)
        if subset is None:
            raise DataExtractionError('Failed to extract subset for input '
                                      'coordinates {}'.format(dimcoord_vals))
        return subset

    # TODO: Test, confirm and remove beta flag in docstring
    def remove_outliers(self, low=None, high=None, inplace=True):
        """Remove outliers from data

        Parameters
        ----------
        low : float
            lower end of valid range for input variable. If None, then the
            corresponding value from the default settings for this variable
            are used (cf. minimum attribute of `available variables
            <https://pyaerocom.met.no/config_files.html#variables>`__)
        high : float
            upper end of valid range for input variable. If None, then the
            corresponding value from the default settings for this variable
            are used (cf. maximum attribute of `available variables
            <https://pyaerocom.met.no/config_files.html#variables>`__)
        inplace : bool
            if True, this object is modified, else outliers are removed in
            a copy of this object

        Returns
        -------
        GriddedData
            modified data object
        """
        if low is None:
            low = self.var_info.minimum
            logger.info('Setting {} outlier lower lim: {:.2f}'
                        .format(self.var_name, low))
        if high is None:
            high = self.var_info.maximum
            logger.info('Setting {} outlier upper lim: {:.2f}'
                        .format(self.var_name, high))
        obj = self if inplace else self.copy()
        obj._ensure_is_masked_array()

        data = obj.grid.data

        mask = np.logical_or(data<low, data>high)
        obj.grid.data[mask] = np.ma.masked
        obj.metadata['outliers_removed'] = True
        return obj

    def _ensure_is_masked_array(self):
        """Make sure underlying data is masked array

        Required, e.g. for removal of outliers

        Note
        ----
        Will trigger "realisation" of data (i.e. loading of numpy array) in
        case data is lazily loaded.
        """
        if not np.ma.is_masked(self.cube.data):
            self.cube.data = np.ma.masked_array(self.cube.data)

    def _resample_time_iris(self, to_ts_type):
        """Resample time dimension using iris funcitonality

        This does not allow to specify further constraints but just
        aggregates to input resolution

        Parameters
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
        #from pyaerocom.tstype import TsType
        to = TsType(to_ts_type)
        current = TsType(self.ts_type)

        if current == to:
            logger.info('Data is already in {} resolution'.format(to_ts_type))
            return self
        if not to_ts_type in IRIS_AGGREGATORS:
            raise TemporalResolutionError('Resolution {} cannot '
                'converted'.format(to_ts_type))
        elif current < to: #current resolution is smaller than desired
            raise TemporalResolutionError('Cannot increase '
                'temporal resolution from {} to {}'.format(self.ts_type,
                                          to_ts_type))
        cube = self.grid

        # Create aggregators
        aggrs = ['yearly']
        if not to_ts_type in aggrs:
            aggrs.append(to_ts_type)

        for aggr in aggrs:
            if not aggr in [c.name() for c in cube.aux_coords]:
                # this adds the corresponding aggregator to the cube
                IRIS_AGGREGATORS[aggr](cube, 'time', name=aggr)
            #IRIS_AGGREGATORS[to_ts_type](cube, 'time', name=to_ts_type)
        # not downscale
        aggregated = cube.aggregated_by(aggrs, MEAN)
        data = GriddedData(aggregated, **self.metadata)
        data.metadata['ts_type'] = to_ts_type
        data.check_dimcoords_tseries()
        return data

    def _resample_time_xarray(self, to_ts_type, how, apply_constraints,
                              min_num_obs):
        import xarray as xarr

        arr = xarr.DataArray.from_iris(self.cube)
        from_ts_type = self.ts_type
        try:
            rs = TimeResampler(arr)
            arr_out = rs.resample(to_ts_type,
                                  from_ts_type=from_ts_type,
                                  how=how,
                                  apply_constraints=apply_constraints,
                                  min_num_obs=min_num_obs)
        except ValueError: # likely non-standard datetime objects in array (cf https://github.com/pydata/xarray/issues/3426)
            arr['time'] = self.time_stamps()
            rs = TimeResampler(arr)
            arr_out = rs.resample(to_ts_type,
                                  from_ts_type=from_ts_type,
                                  how=how,
                                  apply_constraints=apply_constraints,
                                  min_num_obs=min_num_obs)
        data = GriddedData(arr_out.to_iris(),
                           check_unit=False,
                           convert_unit_on_init=False,
                           **self.metadata)
        data.metadata['ts_type'] = to_ts_type
        data.metadata.update(rs.last_setup)
        # in case of these aggregators, the data unit can be kept
        # ToDo: this is a quick fix and needs revision, should also check
        # if this can be handled automatically by iris, since iris knows
        # about cf Units and will perhaps change a unit automatically when
        # e.g. a cumulative sum is applied to the time dimension (for instance)
        # if precip data in mm hr-1 is converted from hourly -> daily using
        # cumulative sum.
        if rs.last_units_preserved:
            data.units = self.units
        else:
            print_log.info(
                f'Cannot infer unit when aggregating using {how}. Please set '
                f'unit in returned data object!'
                )
        try:
            data.check_dimcoords_tseries()
        except:
            data.reorder_dimensions_tseries()
        return data

    def resample_time(self, to_ts_type='monthly', how=None,
                      apply_constraints=None, min_num_obs=None,
                      use_iris=False):
        """Resample time to input resolution

        Parameters
        ----------
        to_ts_type : str
            either of the supported temporal resolutions (cf.
            :attr:`IRIS_AGGREGATORS` in :mod:`helpers`, e.g. "monthly")
        how : str
            string specifying how the data is to be aggregated, default is mean
        apply_constraints : bool, optional
            if True, hierarchical resampling is applied using input
            `min_num_obs` (if provided) or else, using constraints
            specified in :attr:`pyaerocom.const.OBS_MIN_NUM_RESAMPLE`
        min_num_obs : dict or int, optinal
            integer or nested dictionary specifying minimum number of
            observations required to resample from higher to lower frequency.
            For instance, if `input_data` is hourly and `to_ts_type` is
            monthly, you may specify something like::

                min_num_obs =
                    {'monthly'  :   {'daily'  : 7},
                     'daily'    :   {'hourly' : 6}}

            to require at least 6 hours per day and 7 days per month.
        use_iris : bool
            option to use resampling scheme from iris library rather than
            xarray.

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
        if how is None:
            how = 'mean'
        if not self.has_time_dim:
            raise DataDimensionError('Require time dimension in GriddedData: '
                                     '{}'.format(self.short_str()))
        if use_iris and not apply_constraints and how=='mean':
            return self._resample_time_iris(to_ts_type)

        try:
            return self._resample_time_xarray(to_ts_type, how,
                                              apply_constraints,
                                              min_num_obs)
        except NotImplementedError as e:
            raise ResamplingError('Resampling of time in GriddedData failed '
                                  'using xarray. Reason: {}. Please try again '
                                  'with input arg use_iris=True'
                                  .format(repr(e)))

    def downscale_time(self, to_ts_type='monthly'):
        msg = DeprecationWarning('This method is deprecated. Please use new '
                                 'name resample_time')
        print_log.warning(msg)
        return self.resample_time(to_ts_type)

    def add_aggregator(self, aggr_name):
        raise NotImplementedError

    def calc_area_weights(self):
        """Calculate area weights for grid"""
        if not self.has_latlon_dims:
            raise DataDimensionError('Data does not have latitude and longitude '
                                     'dimensions. This is required for '
                                     'computation of area weights.')
        self._check_lonlat_bounds()
        self._area_weights = area_weights(self.grid)
        return self.area_weights

    def filter_altitude(self, alt_range=None):
        """Currently dummy method that makes life easier in :class:`Filter`

        Returns
        -------
        GriddedData
            current instance
        """
        const.logger.info('Altitude filtering is not applied in GriddedData '
                          'and will be skipped')
        return self

    def filter_region(self, region_id, inplace=False, **kwargs):
        """Filter region based on ID

        This works both for rectangular regions and mask regions

        Parameters
        -----------
        region_id : str
            name of region
        inplace : bool
            if True, the current data object is modified, else a new object
            is returned
        **kwargs
            additional keyword args passed to :func:`apply_region_mask` if
            input region is a mask.

        Returns
        -------
        GriddedData
            filtered data object
        """
        if region_id in const.HTAP_REGIONS:
            return self.apply_region_mask(region_id, inplace=inplace, **kwargs)
        return self.crop(region=region_id)

    def apply_region_mask(self, region_id, thresh_coast=0.5, inplace=False):
        """Apply a masked region filter
        """

        if not region_id in const.HTAP_REGIONS:
            raise ValueError('Invalid input for region_id: {}, choose from: {}'
                             .format(region_id, const.HTAP_REGIONS))

        # get Iris mask
        mask_iris = load_region_mask_iris(region_id)

        # Reads mask to griddedata
        mask  = GriddedData(mask_iris,
                            check_unit=False,
                            convert_unit_on_init=False)
        mask = mask.regrid(self.cube)

        #mask.quickplot_map(vmin=0, vmax=1)
        npm = mask.cube.data

        if isinstance(npm, np.ma.core.MaskedArray):
            npm = npm.filled(np.nan)

        thresh_mask = npm > thresh_coast
        npm[thresh_mask] = 0
        npm[~thresh_mask] = 1

        #griddeddata = self.copy()

        try:
            if inplace:
                griddeddata = self
            else:
                griddeddata = self.copy()

            # UPDATE MASK WITH REGIONAL MASK.
            griddeddata.cube.data[:, npm.astype(bool)] = np.nan
            griddeddata.metadata['region'] = region_id

        except MemoryError:
            raise NotImplementedError("Coming soon... ")

        return griddeddata

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
        suppl = {}
        suppl.update(self.metadata)
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
            suppl["region"] = region.name
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
                time_range = (pd.Timestamp(time_range[0]),
                              pd.Timestamp(time_range[1]))
            if all(isinstance(x, pd.Timestamp) for x in time_range):
                logger.info("Cropping along time axis based on Timestamps")
                time_constraint = get_time_rng_constraint(*time_range)
                try:
                    self.cube.coord("time").bounds = None
                except Exception:
                    pass
                data = data.extract(time_constraint)
            elif all(isinstance(x, int) for x in time_range):
                logger.info("Cropping along time axis based on indices")
                data = data[time_range[0]:time_range[1]]
            if not data:
                raise DataExtractionError("Failed to apply temporal cropping")
        return GriddedData(data, check_unit=False,
                           convert_unit_on_init=False, **suppl)

    def get_area_weighted_timeseries(self, region=None):
        """Helper method to extract area weighted mean timeseries

        Parameters
        ----------
        region
            optional, name of AeroCom default region for which the mean is to
            be calculated (e.g. EUROPE)

        Returns
        -------
        StationData
            station data containing area weighted mean
        """
        try:
            self.check_dimcoords_tseries()
        except DimensionOrderError:
            self.reorder_dimensions_tseries()
        if self.ndim != 3:
            raise NotImplementedError('Area weighted mean can only computed '
                                      'for data containing latitude and '
                                      'longitude data')
        stat = StationData()
        stat.station_name = self.data_id
        if region is not None:
            d = self.crop(region=region)
            stat['region'] = region
        else:
            d = self
        vals = d.area_weighted_mean()

        stat[self.var_name] = pd.Series(vals, d.time_stamps())
        return stat

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
        const.print_log.warning(
            DeprecationWarning('This method is deprecated. Please use '
                               'aerocom_savename instead')
        )
        from pyaerocom.io import FileConventionRead
        f = self.from_files[0]
        fconv = FileConventionRead().from_file(f)
        base_info = fconv.get_info_from_file(f)

        vert_code = base_info['vert_code']
        if vert_code is None:
            vert_code = 'UNDEFINED'
        if at_stations:
            vert_code += 'AtStations'

        name = [fconv.name, self.name, self.var_name, vert_code,
                str(pd.Timestamp(self.start).year), self.ts_type]
        return f'{fconv.file_sep}'.join(name) + '.nc'

    def aerocom_savename(self, data_id=None, var_name=None,
                         vert_code=None, year=None, ts_type=None):
        """Get filename for saving following AeroCom conventions"""
        from pyaerocom.io.helpers import aerocom_savename
        if vert_code is None:
            try:
                from pyaerocom.io.fileconventions import FileConventionRead
                f = self.from_files[0]
                fconv = FileConventionRead().from_file(f)
                vert_code = fconv.get_info_from_file(f)['vert_code']
            except Exception:
                pass

        if vert_code in (None, ''):
            raise ValueError('Please provide input vert_code')

        if data_id is None:
            data_id = self.data_id
        if var_name is None:
            var_name = self.var_name
        if year is None:
            start = pd.Timestamp(self.start).year
            stop = pd.Timestamp(self.stop).year
            if stop > start:
                raise ValueError('Cannot create AeroCom savename for multiyear '
                                 'data... please split first')
            year = str(start)
        else:
            year = str(year)
        if ts_type is None:
            ts_type = self.ts_type
        return aerocom_savename(data_id, var_name, vert_code, year, ts_type)

    def compute_at_stations_file(self, latitudes=None, longitudes=None,
                                 out_dir=None, savename=None,
                                 obs_data=None):
        """Creates and saves new netcdf file at input lat / lon coordinates

        This method can be used to reduce the size of too large grid files.
        It reduces the lon / lat dimensionality corresponding to the locations
        of the input lat / lon coordinates.

        """
        from pyaerocom import UngriddedData, print_log
        print_log.info('Computing AtStations file. This may take a while')
        if isinstance(obs_data, UngriddedData):
            longitudes = obs_data.longitude
            latitudes = obs_data.latitude

        if not len(longitudes) == len(latitudes):
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

        for lat, lon in zip(latitudes, longitudes):
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

    def to_xarray(self):
        from xarray import DataArray
        arr = DataArray.from_iris(self.cube)
        return arr

    def _check_meta_netcdf(self):
        """Get rid of empty entries and convert bools to int in meta"""
        meta_out = {}
        for k, v in self.metadata.items():
            if type(v) == bool:
                meta_out[k] = int(v)
            elif v != None:
                meta_out[k] = v
        self.cube.attributes = meta_out

    def _to_netcdf_aerocom(self, out_dir, **kwargs):

        years = self.years_avail()
        outpaths = []
        for subset in self.split_years(years):
            subset._check_meta_netcdf()
            savename = subset.aerocom_savename(**kwargs)
            fp = os.path.join(out_dir, savename)
            iris.save(subset.grid, fp)
            outpaths.append(fp)
        return outpaths

    def to_netcdf(self, out_dir, savename=None, **kwargs):
        """Save as NetCDF file

        Parameters
        -----------
        out_dir : str
            output direcory (must exist)
        savename : str, optional
            name of file. If None, :func:`aerocom_savename` is used which is
            generated automatically and may be modified via `**kwargs`
        **kwargs
            keywords for name

        Returns
        -------
        list
            list of output files created
        """

        if savename is None: #use AeroCom convention
            return self._to_netcdf_aerocom(out_dir, **kwargs)
        self._check_meta_netcdf()
        fp = os.path.join(out_dir, savename)
        iris.save(self.grid, fp)

        return [fp]

    def interpolate(self, sample_points=None, scheme="nearest",
                    collapse_scalar=True, **coords):
        """Interpolate cube at certain discrete points

        Reimplementation of method :func:`iris.cube.Cube.interpolate`, for
        details `see here <http://scitools.org.uk/iris/docs/v1.10.0/iris/iris/
        cube.html#iris.cube.Cube.interpolate>`__

        Note
        ----
        The input coordinates may also be provided using the input arg
        `**coords` which provides a more intuitive option (e.g. input
        ``(sample_points=[("longitude", [10, 20]), ("latitude", [1, 2])])``
        is the same as input ``(longitude=[10, 20], latitude=[1,2])``

        Parameters
        ----------
        sample_points : list
            sequence of coordinate pairs over which to interpolate
        scheme : str or iris interpolator object
            interpolation scheme, pyaerocom default is nearest. If input is
            string, it is converted into the corresponding iris Interpolator
            object, see :func:`str_to_iris` for valid strings
        collapse_scalar : bool
            Whether to collapse the dimension of scalar sample points in the
            resulting cube. Default is True.
        **coords
            additional keyword args that may be used to provide the interpolation
            coordinates in an easier way than using the ``Cube`` argument
            `sample_points`. May also be a combination of both.

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
        print_log.info('Interpolating data of shape {}. This may take a while.'
                       .format(self.shape))
        try:
            itp_cube = self.grid.interpolate(sample_points, scheme,
                                             collapse_scalar)
        except MemoryError:
            raise MemoryError("Interpolation failed since grid of interpolated "
                              "Cube is too large")
        print_log.info('Successfully interpolated cube')
        return GriddedData(itp_cube, **self.metadata)

    def regrid(self, other=None, lat_res_deg=None, lon_res_deg=None,
               scheme='areaweighted', **kwargs):
        """Regrid this grid to grid resolution of other grid

        Parameters
        ----------
        other : GriddedData or Cube, optional
            other data object to regrid to. If None, then input args
            `lat_res` and `lon_res` are used to regrid.
        lat_res_deg : float or int, optional
            latitude resolution in degrees (is only used if input arg `other`
            is None)
        lon_res_deg : float or int, optional
            longitude resolution in degrees (is only used if input arg `other`
            is None)
        scheme : str
            regridding scheme (e.g. linear, neirest, areaweighted)

        Returns
        -------
        GriddedData
            regridded data object (new instance, this object remains unchanged)
        """

        if isinstance(other, iris.cube.Cube):
            other = GriddedData(other,
                                check_unit=False,
                                convert_unit_on_init=False)
        if isinstance(scheme, str):
            scheme = str_to_iris(scheme, **kwargs)

        if other is None:
            if any(x is None for x in (lat_res_deg, lon_res_deg)):
                raise ValueError('Missing input for regridding. Need either '
                                 'other data object or both lat_res_deg and '
                                 'lon_res_deg specified')
            dummy = make_dummy_cube_latlon(lat_res_deg=lat_res_deg,
                                           lon_res_deg=lon_res_deg)
            other = GriddedData(dummy,
                                check_unit=False,
                                convert_unit_on_init=False)

        if not (self.has_latlon_dims * other.has_latlon_dims):
            raise DataDimensionError('Can only regrid data objects with '
                                     'latitude and longitude dimensions')

        self._check_lonlat_bounds()
        other._check_lonlat_bounds()

        self.check_lon_circular()
        other.check_lon_circular()

        data_rg = self.grid.regrid(other.grid, scheme)
        suppl = od(**self.metadata)
        suppl['regridded'] = True
        data_out = GriddedData(data_rg, **suppl)
        return data_out

    def check_lon_circular(self):
        """Check if latitude and longitude coordinates are circular"""
        if not self.has_latlon_dims:
            raise DataDimensionError('No lat lon dimensions available...')
        if not self.longitude.circular:
            self.longitude.circular = check_coord_circular(self.longitude.points,
                                                           360)
        return self.longitude.circular

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
        return GriddedData(collapsed, **self.cube.attributes)

    def extract(self, constraint, inplace=False):
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
        data_crop = self.grid.extract(constraint)
        if not data_crop:
            raise DataExtractionError("Failed to extract subset")
        if inplace:
            self.cube = data_crop
        else:
            return GriddedData(data_crop, **self.metadata)

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
        data_crop = self.grid.intersection(*args, **kwargs)

        return GriddedData(data_crop, **self.metadata)

    def quickplot_map(self, time_idx=0, xlim=(-180, 180), ylim=(-90, 90),
                      add_mean=True, **kwargs):
        """Make a quick plot onto a map

        Parameters
        ----------
        time_idx : int
            index in time to be plotted
        xlim : tuple
            2-element tuple specifying plotted longitude range
        ylim : tuple
            2-element tuple specifying plotted latitude range
        add_mean : bool
            if True, the mean value over the region and period is inserted
        **kwargs
            additional keyword arguments passed to
            :func:`pyaerocom.quickplot.plot_map`

        Returns
        -------
        fig
            matplotlib figure instance containing plot
        """
        if not 'latitude' in self.dimcoord_names:
            raise DataDimensionError('Missing latitude dimension...')
        elif not 'longitude' in self.dimcoord_names:
            raise DataDimensionError('Missing longitude dimension...')
        tstr = ''
        if 'time' in self.dimcoord_names:
            if not self.ndim == 3:
                raise DataDimensionError('Invalid number of dimensions: {}. '
                                         'Expected 3.'.format(self.ndim))
            if not isinstance(time_idx, int):
                try:
                    t = to_pandas_timestamp(time_idx).to_datetime64()
                    time_idx = np.argmin(abs(self.time_stamps() - t))
                except Exception:
                    raise ValueError('Failed to interpret input time stamp')

            data = self[time_idx]
            try:
                t = cftime_to_datetime64(self.time[time_idx])[0]
                tstr = datetime2str(t, self.ts_type)
            except Exception:
                try:
                    tstr = datetime2str(self.time_stamps()[time_idx],
                                        self.ts_type)
                except Exception:
                    print_log.warning('Failed to retrieve ts_type in '
                                      'GriddedData {}'.format(repr(self)))
        else:
            if not self.ndim == 2:
                raise DataDimensionError('Invalid number of dimensions: {}. '
                                         'Expected 2.'.format(self.ndim))
            data = self

        from pyaerocom.plot.mapping import plot_griddeddata_on_map

        lons = self.longitude.contiguous_bounds()
        lats = self.latitude.contiguous_bounds()

        fig = plot_griddeddata_on_map(data=data.grid.data, lons=lons,
                                      lats=lats,
                                      var_name=self.var_name,
                                      unit=self.units,
                                      xlim=xlim, ylim=ylim,
                                      **kwargs)

        fig.axes[0].set_title("{} ({}, {})".format(self.data_id,
                              self.var_name, tstr))
        if add_mean:
            from pyaerocom.plot.config import COLOR_THEME

            ax = fig.axes[0]
            try:
                from pyaerocom.mathutils import exponent
                mean = data.mean()
                vstr = ('{:.%sf}'% (abs(exponent(mean)) + 1)).format(mean)
                mustr = 'Mean={}'.format(vstr)
                u = str(self.units)
                if not u=='1':
                    mustr += ' [{}]'.format(u)
                ax.text(0.02, 0.02, mustr,
                        color=COLOR_THEME.color_map_text,
                        transform=ax.transAxes,
                        fontsize=22,
                        bbox=dict(facecolor='#ffffff', edgecolor='none',
                                  alpha=0.65))
            except Exception as e:
                print_log.warning('Failed to compute / add area weighted mean. '
                                  'Reason: {}'.format(repr(e)))

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

    def area_weighted_mean(self):
        """Get area weighted mean"""
        ws = self.area_weights
        collapsed = self.collapsed(coords=["longitude", "latitude"],
                                   aggregator=MEAN,
                                   weights=ws)
        return collapsed.grid.data

    def mean(self, areaweighted=True):
        """Mean value of data array

        Note
        ----
        Corresponds to numerical mean of underlying N-dimensional numpy array.
        Does not consider area-weights or any other advanced averaging.
        """
        #make sure data is in memory
        if areaweighted:
            avg = self.area_weighted_mean().mean()
            return avg

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
        return "ID: {}, Var: {}".format(self.data_id, self.var_name)

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
        raise NotImplementedError
        return sum([os.path.getsize(f) for f in self.from_files]) / 10**9

    def __getattr__(self, attr):
        return self[attr]

    def _check_coordinate_access(self, val):
        if self._coord_standard_names is None:
            self._update_coord_info()
        if val in self._coord_standard_names:
            return {'standard_name' : val}
        elif val in self._coord_var_names:
            return {'var_name' : val}
        elif val in self._coord_long_names:
            return {'long_name' : val}
        raise CoordinateError('Could not associate one of the coordinates with '
                              'input string {}'.format(val))

    def copy(self):
        """Copy this data object"""
        return GriddedData(self.cube.copy())

    def delete_aux_vars(self):
        """Delete auxiliary variables and iris AuxFactories"""
        c = self.cube
        for aux_fac in c.aux_factories:

            c.remove_aux_factory(aux_fac)

        for coord in c.coords():
            if isinstance(coord, iris.coords.AuxCoord):
                c.remove_coord(coord.name())

    def search_other(self, var_name, require_same_shape=True):
        """Searches data for another variable"""
        if require_same_shape and self.concatenated or self.computed:
            raise NotImplementedError('Coming soon...')
        for file in self.from_files:
            try:
                from pyaerocom.io.iris_io import load_cube_custom
                cube = load_cube_custom(file, var_name=var_name,
                                        perform__fmt_checks=False)
                return GriddedData(cube, from_files=file)
            except Exception:
                pass
        if var_name in self.reader.vars_provided:
            return self.reader.read_var(var_name,
                                        start=self.start,
                                        stop=self.stop,
                                        ts_type=self.ts_type,
                                        flex_ts_type=True)
        raise VariableNotFoundError('Could not find variable {}'.format(var_name))

    def update_meta(self, **kwargs):
        """Update metadata dictionary"""
        for key, val in kwargs.items():
            if key == 'var_name' and not isinstance(val, str):
                const.print_log.warning('Skipping assignment of var_name from '
                                     'metadata in GriddedData, since attr. '
                                     'needs to be str and is {}'.format(val))
                continue
            self._grid.attributes[key] = val

    def delete_all_coords(self, inplace=True):
        """Deletes all coordinates (dimension + auxiliary) in this object"""
        if inplace:
            obj = self
        else:
            obj = self.copy()
        delete_all_coords_cube(obj.cube, inplace=True)
        return obj

    def copy_coords(self, other, inplace=True):
        """Copy all coordinates from other data object

        Requires the underlying data to be the same shape.

        Warning
        --------
        This operation will delete all existing coordinates and auxiliary
        coordinates and will then copy the ones from the input data object.
        No checks of any kind will be performed

        Parameters
        ----------
        other : GriddedData or Cube
            other data object (needs to be same shape as this object)

        Returns
        -------
        GriddedData
            data object containing coordinates from other object
        """
        if inplace:
            obj = self
        else:
            obj = self.copy()
        if isinstance(other, iris.cube.Cube):
            other = GriddedData(other)
        if not other.shape == obj.shape:
            raise DataDimensionError('Cannot copy coordinates: shape mismatch')
        copy_coords_cube(to_cube=obj.cube, from_cube=other.cube, inplace=True)
        return obj

    def _update_coord_info(self):
        n, vn, sn, ln = [], [], [], []
        for c in self.grid.coords():
            n.append(c.name())
            vn.append(c.var_name)
            sn.append(c.standard_name)
            ln.append(c.long_name)
        self._coord_names = n
        self._coord_var_names = vn
        self._coord_standard_names = sn
        self._coord_long_names = ln

    def __getitem__(self, indices_or_attr):
        """x.__getitem__(y) <==> x[y]"""

        if isinstance(indices_or_attr, str):
            if indices_or_attr in self.__dict__:
                return self.__dict__[indices_or_attr]
            try:
                which = self._check_coordinate_access(indices_or_attr)
                return self.grid.coord(**which)
            except Exception:
                raise AttributeError("GriddedData object has no "
                                     "attribute {}"
                                     .format(indices_or_attr))

        sub = self.grid.__getitem__(indices_or_attr)
        return GriddedData(sub, **self.metadata)

    def __contains__(self, val):
        """Check if variable or coordinate matchs input string"""
        return val is self.name or val in self.coord_names

    def __dir__(self):
        return self.coord_names + super().__dir__()

    def __str__(self):
        """For now, use string representation of underlying data"""
        st = (f'pyaerocom.GriddedData: ({self.var_name}, {self.data_id})\n'
              f'{self._grid.__str__()}')
        return st

    def __repr__(self):
        """For now, use representation of underlying data"""
        return (f'pyaerocom.GriddedData: ({self.var_name}, {self.data_id})\n'
                f'{self._grid.__repr__()}')

    def __add__(self, other):
        raise NotImplementedError('Coming soon')

    def short_str(self):
        """Short string representation"""
        return (f'{self.var_name} ({self.data_id}, freq={self.ts_type}, '
                f'unit={self.units})')

    ### Deprecated (but still supported) stuff
    @property
    def unit(self):
        """Unit of data"""
        const.print_log.warning(DeprecationWarning('Attr. unit is deprecated, '
                                                'please use units instead'))
        return self.grid.units

    @unit.setter
    def unit(self, val):
        const.print_log.warning(DeprecationWarning('Attr. unit is deprecated, '
                                                'please use units instead'))
        self.grid.units = val

if __name__=='__main__':
    import matplotlib.pyplot as plt
    import pyaerocom as pya
    plt.close("all")
    pya.initialise_testdata()
    # print("uses last changes ")
    data = pya.io.ReadGridded('TM5-met2010_CTRL-TEST').read_var('od550aer',
                                                                start=2010,
                                                                ts_type='daily')


