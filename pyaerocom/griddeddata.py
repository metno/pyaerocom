from __future__ import annotations

import logging
import os
import warnings
from pathlib import Path

import iris
import numpy as np
import pandas as pd
import xarray as xr
from iris.analysis import MEAN
from iris.analysis.cartography import area_weights

from pyaerocom import const
from pyaerocom._warnings import ignore_warnings
from pyaerocom.exceptions import (
    CoordinateError,
    DataDimensionError,
    DataExtractionError,
    DimensionOrderError,
    ResamplingError,
    TemporalResolutionError,
    VariableDefinitionError,
    VariableNotFoundError,
)
from pyaerocom.units.datetime import cftime_to_datetime64, datetime2str, to_pandas_timestamp
from pyaerocom.helpers import (
    check_coord_circular,
    copy_coords_cube,
    delete_all_coords_cube,
    extract_latlon_dataarray,
    get_lat_rng_constraint,
    get_lon_rng_constraint,
    get_time_rng_constraint,
    isnumeric,
    isrange,
    make_dummy_cube_latlon,
    str_to_iris,
)
from pyaerocom.helpers_landsea_masks import load_region_mask_iris
from pyaerocom.mathutils import estimate_value_range, exponent
from pyaerocom.projection_information import ProjectionInformation
from pyaerocom.region import Region
from pyaerocom.stationdata import StationData
from pyaerocom.units.datetime.time_config import IRIS_AGGREGATORS, TS_TYPE_TO_NUMPY_FREQ
from pyaerocom.time_resampler import TimeResampler
from pyaerocom.units.datetime import TsType
from pyaerocom.units import Unit
from pyaerocom.units.helpers import get_standard_unit
from pyaerocom.variable import Variable
from pyaerocom.vert_coords import AltitudeAccess

from pyaerocom.units.logging import LoggingCallback
from pyaerocom.units import convert_unit

logger = logging.getLogger(__name__)


class GriddedData:
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
    COORDS_ORDER_TSERIES = ["time", "latitude", "longitude"]
    _MAX_SIZE_GB = 64  # maximum file size for in-memory operations

    SUPPORTED_VERT_SCHEMES = ["mean", "max", "min", "surface", "altitude", "profile"]

    _META_ADD = dict(
        from_files=[],
        data_id="undefined",
        var_name_read="undefined",
        ts_type="undefined",
        vert_code=None,
        regridded=False,
        outliers_removed=False,
        computed=False,
        concatenated=False,
        region=None,
        reader=None,
        proj_info=None,
    )

    def __init__(
        self,
        input=None,
        var_name=None,
        check_unit=True,
        convert_unit_on_init=True,
        proj_info: ProjectionInformation | None = None,
        **meta,
    ):
        if input is None:
            input = iris.cube.Cube([])

        self._grid = None
        self._reader = None
        # attribute used to store area weights (if applicable, see method
        # area_weights)
        self._area_weights = None
        self._altitude_access = None

        # list of coordinate names as returned by name() method of iris coordinate
        # will be filled upon access of coord_names
        self._coord_names = None
        # list of containing var_name attributes of all coordinates
        self._coord_var_names = None
        self._coord_standard_names = None
        self._coord_long_names = None
        # projection information
        meta.update({"proj_info": proj_info})

        if input:
            self.load_input(input, var_name)

        self.update_meta(**meta)
        if self.has_data and self.var_name is not None and check_unit:
            self.check_unit(convert_unit_on_init)

    @property
    def var_name(self) -> str:
        """Name of variable"""
        return self.grid.var_name

    @var_name.setter
    def var_name(self, val: str):
        """Name of variable"""
        if not isinstance(val, str):
            raise TypeError(f"Invalid input for var_name, need str, got {type(val)}")
        self.grid.var_name = val
        if "var_name" in self.metadata:
            self.metadata["var_name"] = val

    @property
    def var_name_aerocom(self):
        """AeroCom variable name"""
        try:
            return const.VARS[self.var_name].var_name_aerocom
        except VariableDefinitionError:
            return None

    @property
    def var_info(self):
        """Print information about variable"""
        if self.var_name in const.VARS:
            return const.VARS[self.var_name]
        var_name = self.var_name_aerocom
        if var_name in const.VARS:
            return const.VARS[var_name]
        else:
            raise VariableDefinitionError(
                f"No default access available for variable {self.var_name}"
            )

    @property
    def proj_info(self) -> ProjectionInformation:
        return self.metadata["proj_info"]

    @property
    def ts_type(self):
        """
        Temporal resolution of data
        """
        if self.metadata["ts_type"] == "undefined":
            logger.warning("ts_type is not set in GriddedData, trying to infer.")
            self.infer_ts_type()

        return self.metadata["ts_type"]

    @ts_type.setter
    def ts_type(self, val):
        TsType(val)  # this will raise an error if input is invalid
        self.metadata["ts_type"] = val

    @property
    def vert_code(self):
        """
        Vertical code of data (e.g. Column, Surface, ModelLevel)
        """
        return self.metadata["vert_code"]

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
        warnings.warn(
            "Outdated attribute suppl_info. Please use metadata instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.metadata

    @property
    def metadata(self):
        return self.cube.attributes

    @property
    def data_revision(self):
        """Revision string from file Revision.txt in the main data directory"""
        if self.from_files:
            data_dir = os.path.dirname(self.from_files[0])
            revision_file = os.path.join(data_dir, const.REVISION_FILE)
            if os.path.isfile(revision_file):
                with open(revision_file) as in_file:
                    revision = in_file.readline().strip()
                    in_file.close()

                return revision
        return "n/a"

    @property
    def reader(self):
        """Instance of reader class from which this object was created

        Note
        ----
        Currently only supports instances of :class:`ReadGridded`.
        """
        from pyaerocom.io import ReadGridded

        if not isinstance(self._reader, ReadGridded):
            self._reader = ReadGridded(self.data_id)
        return self._reader

    @reader.setter
    def reader(self, val):
        from pyaerocom.io import ReadGridded

        if not isinstance(val, ReadGridded):
            raise ValueError(
                "cannot set reader in GriddedData: need instance of class ReadGridded"
            )
        self._reader = val

    @property
    def concatenated(self):
        return self.metadata["concatenated"]

    @property
    def computed(self):
        return self.metadata["computed"]

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
            raise ValueError("Cannot set data array: need numpy.ndarray")
        elif not array.shape == self.grid.data.shape:
            raise DataDimensionError(
                f"Cannot assign dataarray: shape mismatch. "
                f"Got: {array.shape}, Need: {self.grid.shape}"
            )
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
            raise AttributeError(
                "Need at least 2 timestamps in GriddedData in order to compute delta-t"
            )
        return ts[1:] - ts[0:-1]

    def check_frequency(self):
        """Check if all datapoints are sampled at the same time frequency"""
        dt = np.unique(self.delta_t)
        if len(dt) > 1:
            raise AttributeError("Irregular time-frequency")
        freq = TS_TYPE_TO_NUMPY_FREQ[self.ts_type]
        if not int(dt.astype(f"timedelta64[{freq}]")) == 1:
            raise AttributeError(
                "Mismatch between sampling freq and actual frequency of values in time dimension "
            )

    @property
    def TS_TYPES(self):
        """List with valid filename encryptions specifying temporal resolution"""
        return self.io_opts.GRID_IO.TS_TYPES

    @property
    def from_files(self):
        """List of file paths from which this data object was created"""
        return self.metadata["from_files"]

    @property
    def is_masked(self):
        """Flag specifying whether data is masked or not

        Note
        ----
        This method only works if the data is loaded.
        """
        if self.grid.has_lazy_data():
            raise AttributeError(
                "Information cannot be accessed. Data is not available in memory (lazy loading)"
            )
        return isinstance(self.grid.data, np.ma.core.MaskedArray)

    @property
    def base_year(self):
        """Base year of time dimension

        Note
        ----
        Changing this attribute will update the time-dimension.
        """
        if not self.has_time_dim:
            raise DataDimensionError("Could not access base year: data has no time dimension")
        try:
            return self.time.units.utime().origin.year
        except Exception as e:
            raise DataDimensionError(f"Could access base-year. Unexpected error: {repr(e)}")

    @base_year.setter
    def base_year(self, val):
        self.change_base_year(val)

    @property
    def start(self):
        """Start time of dataset as datetime64 object"""
        if not self.has_time_dim:
            raise ValueError("GriddedData has no time dimension")
        t = cftime_to_datetime64(self.time[0])[0]

        # try:
        # ToDo: check if this is needed
        np_freq = TsType(self.ts_type).to_numpy_freq()  # TS_TYPE_TO_NUMPY_FREQ[self.ts_type]
        dtype_appr = f"datetime64[{np_freq}]"
        t = t.astype(dtype_appr)
        return t.astype("datetime64[us]")

    @property
    def stop(self):
        """Start time of dataset as datetime64 object"""
        if not self.has_time_dim:
            raise ValueError("GriddedData has no time dimension")
        t = cftime_to_datetime64(self.time[-1])[0]

        np_freq = TsType(self.ts_type).to_numpy_freq()  # TS_TYPE_TO_NUMPY_FREQ[self.ts_type]
        dtype_appr = f"datetime64[{np_freq}]"

        t = t.astype(dtype_appr) + np.timedelta64(1, np_freq)
        t = t.astype("datetime64[us]") - np.timedelta64(1, "us")
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
            raise TypeError(f"Grid data format {type(value)} is not supported, need Cube")

        for key, val in self._META_ADD.items():
            if key not in value.attributes:
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
        warnings.warn(
            "Deprecated attribute name, please use data_id instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.metadata["data_id"]

    @property
    def data_id(self):
        """ID of data object (e.g. model run ID, obsnetwork ID)

        Note
        ----
        This attribute was formerly named ``name`` which is also the
        corresponding attribute name in :attr:`metadata`
        """
        try:
            return self.metadata["data_id"]
        except KeyError:
            return "undefined"

    @property
    def is_climatology(self):
        ff = self.from_files
        if len(ff) == 1 and "9999" in os.path.basename(ff[0]):
            return True
        return False

    @property
    def has_data(self):
        """True if sum of shape of underlying Cube instance is > 0, else False"""
        return True if bool(sum(self._grid.shape)) else False

    @property
    def shape(self):
        return self._grid.shape

    @property
    def lon_res(self):
        if "longitude" not in self:
            raise AttributeError("Data does not contain longitude information")
        vals = np.diff(self.longitude.points)
        val = vals.mean()
        if vals.std() / val > 0.0001:
            raise ValueError("Check longitudes")
        return val

    @property
    def lat_res(self):
        if "latitude" not in self:
            raise AttributeError("Data does not contain longitude information")
        vals = np.diff(self.latitude.points)
        val = vals.mean()
        if vals.std() / val > 0.0001:
            raise ValueError("Check latitudes")
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
        return all([dim in self.dimcoord_names for dim in ["latitude", "longitude"]])

    @property
    def has_time_dim(self):
        """Boolean specifying whether data has latitude and longitude dimensions"""
        return "time" in self.dimcoord_names

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
            raise DataDimensionError("Cannot infer frequency. Data has no time dimension")
        dt = np.unique(self.delta_t)
        if len(dt) > 1:
            raise ValueError("Could not identify unique frequency")
        dt = dt[0]
        for ts_type, freq in TS_TYPE_TO_NUMPY_FREQ.items():
            val = dt.astype(f"timedelta64[{freq}]").astype(int)
            if val == 1:
                self.metadata["ts_type"] = ts_type
                return ts_type
        raise AttributeError("Failed to infer ts_type from data")

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

    def _read_netcdf(self, input, var_name, perform_fmt_checks):
        from pyaerocom.io.iris_io import load_cube_custom

        self.grid = load_cube_custom(input, var_name, perform_fmt_checks=perform_fmt_checks)
        if "from_files" not in self.metadata:
            self.metadata["from_files"] = []
        elif not isinstance(self.metadata["from_files"], list):
            self.metadata["from_files"] = [self.metadata["from_files"]]
        self.metadata["from_files"].append(input)
        try:
            from pyaerocom.io.helpers import get_metadata_from_filename

            self.update_meta(**get_metadata_from_filename(input))
        except Exception:
            logger.warning("Failed to access metadata from filename")

    def register_var_glob(self, delete_existing=True):
        vmin, vmax = self.estimate_value_range_from_data()
        vardef = Variable(
            var_name=self.var_name,
            standard_name=self.standard_name,
            long_name=self.long_name,
            units=self.units,
            minimum=vmin,
            maximum=vmax,
        )
        var_existed = False
        if delete_existing:
            varcol = const.VARS
            if self.var_name in varcol:
                varcol.delete_variable(self.var_name)
                var_existed = True
        const.VARS.add_var(vardef)
        if not var_existed:
            logger.warning(
                f"Adding variable {self.var_name} in pyaerocom.const.VARS. "
                f"since such a  "
                f"variable is not defined in pyaerocom. Minimum and maximum "
                f"values are added automatically based on value range in "
                f"associated GriddedData object to: minimum={vmin}, maximum="
                f"{vmax}. Since this will add the variable only temporarily "
                f"during this run, this might interrupt the processing "
                f"workflow unexpectedly when rerunning parts of the code without "
                f"explicitly calling GriddedData.register_var_glob. It may be best "
                f"to add this variable to pyaerocom/data/variables.ini."
            )
        return vardef

    @ignore_warnings(UserWarning, "Ignoring netCDF variable '.*' invalid units '.*'")
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
            self.grid = input  # instance of Cube
        elif isinstance(input, Path) and input.exists():
            self._read_netcdf(str(input), var_name, perform_fmt_checks)
        elif isinstance(input, str) and os.path.exists(input):
            self._read_netcdf(input, var_name, perform_fmt_checks)
        else:
            raise ValueError(f"Failed to load input: {input}")

        if var_name is not None and self.var_name != var_name:
            try:
                self.var_name = var_name
            except ValueError:
                logger.warning(f"Could not update var_name, invalid input {var_name} (need str)")

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
        if "invalid_units" in cube.attributes:
            try:
                cube.units = str(Unit(cube.attributes["invalid_units"]))
            except ValueError:
                pass
            else:
                del cube.attributes["invalid_units"]

        return cube

    def check_unit(self, try_convert_if_wrong: bool = False) -> bool:
        """Check if unit is correct"""
        self._check_invalid_unit_alias()
        unit_ok = False
        to_unit = None
        try:
            var = const.VARS[self.cube.var_name]
            to_unit = get_standard_unit(var.var_name)
            current_unit = self.units
            if to_unit == current_unit:  # string match e.g. both are m-1
                unit_ok = True
            elif Unit(to_unit).convert(1, current_unit) == 1:
                self.units = to_unit
                logger.info(
                    f"Updating unit string from {current_unit} to {to_unit} in GriddedData."
                )
                unit_ok = True
        except (VariableDefinitionError, ValueError):
            pass

        if not unit_ok and try_convert_if_wrong and isinstance(to_unit, str):
            logger.warning(
                f"Unit {self.units} in GriddedData {self.short_str()} is not "
                f"AeroCom conform ({to_unit}). Trying to convert ... "
            )
            if self.var_info.units == "1" and self.units.is_unknown():
                self.units = "1"
                unit_ok = True
            else:
                try:
                    self.convert_unit(to_unit)
                    unit_ok = True
                except Exception as e:
                    logger.warning(
                        f"Failed to convert unit from {self.units} to {to_unit}. Reason: {e}"
                    )

        return unit_ok

    def convert_unit(self, new_unit: str, inplace: bool = True) -> GriddedData:
        """Convert unit of data to new unit

        Parameters
        ----------
        new_unit : str or pyaerocom.units.Unit
            new unit of data
        inplace : bool
            convert in this instance or create a new one
        """
        out = self if inplace else self.copy()

        var_name = out.var_name
        out.grid = convert_unit(
            out.grid,
            from_unit=self.units,
            to_unit=new_unit,
            var_name=self.var_name,
            ts_type=self.ts_type,
            inplace=True,
            callback=LoggingCallback(logger),
        )
        out._grid.attributes.update(self._grid.attributes)
        out.var_name = var_name
        out.units = new_unit

        return out

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
        to_year = lambda x: int(str(x.astype("datetime64[Y]")))  # noqa: E731
        return sorted(set(to_year(date) for date in self.time_stamps()))

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
            logger.info(f"Nothing to split... GriddedData contains only {years[0]}")
            yield self
        for year in years:
            start, stop = start_stop_from_year(year)
            yield self.crop(time_range=(start, stop))

    def check_dimcoords_tseries(self) -> None:
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
        NotImplementedError
            if one of the required coordinates is associated with more than
            one dimension.
        DimensionOrderError
            if dimensions are not in the right order (in which case
            :func:`reorder_dimensions_tseries` may be used to catch the
            Exception)
        """
        if self.ndim not in (3, 4):
            raise DataDimensionError("Time series extraction requires at least 3 dimensions")
        # list of coordinates needed for timeseries extraction.
        needed = self.COORDS_ORDER_TSERIES
        for i, coord in enumerate(needed):
            dims = self.cube.coord_dims(coord)
            if len(dims) == 0:
                raise DataDimensionError(
                    f"Coord {coord} is not associated with a data dimension in cube"
                )
            elif len(dims) > 1:
                raise NotImplementedError(
                    f"Coord {coord} is associated with "
                    f"multiple dimensions. This cannot "
                    f"yet be handled..."
                )
            if not dims[0] == i:
                raise DimensionOrderError("Invalid order of grid dimensions")

    def reorder_dimensions_tseries(self) -> None:
        """Transpose dimensions of data such that :func:`to_time_series` works

        Raises
        ------
        DataDimensionError
            if not all needed coordinates are available
        NotImplementedError
            if one of the required coordinates is associated with more than
            one dimension.

        """
        # list of coordinates needed for timeseries extraction.
        needed = self.COORDS_ORDER_TSERIES
        new_order = []
        # coord_names = [c.name() for c in self.grid.dim_coords]
        for coord in needed:
            dims = self.cube.coord_dims(coord)
            if len(dims) == 0:
                raise DataDimensionError(
                    f"Coord {coord} is not associated with a data dimension in cube"
                )
            elif len(dims) > 1:
                raise NotImplementedError(
                    f"Coord {coord} is associated with "
                    "multiple dimensions. This cannot "
                    "yet be handled..."
                )
            new_order.append(dims[0])

        if not len(new_order) == self.ndim:
            for i in range(self.ndim):
                if i not in new_order:
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

    def mean_at_coords(self, latitude=None, longitude=None, time_resample_kwargs=None, **kwargs):
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
        ts = self.to_time_series(latitude=latitude, longitude=longitude, **kwargs)
        mean = []
        for stat in ts:
            if isinstance(time_resample_kwargs, dict):
                stat.resample_time(self.var_name, inplace=True, **time_resample_kwargs)
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
                vals = [vals]
            if num is None:
                num = len(vals)
            elif num != len(vals):
                raise ValueError("All coord arrays need to have same length")
            sample_points.append((cname, vals))
        return sample_points

    def _iris_sample_points_to_coords(self, sample_points):
        lats, lons = None, None
        for name, vals in sample_points:
            if isnumeric(vals):
                vals = [vals]
            if name in ("lat", "latitude"):
                lats = vals
            elif name in ("lon", "longitude"):
                lons = vals
        if not lats or not lons or not len(lats) == len(lons):
            raise ValueError(
                "Could not extract latitude or longitude info "
                "from sampling_points or both input arrays "
                "do not have the same length"
            )

        return dict(lat=lats, lon=lons)

    def to_time_series(
        self,
        sample_points=None,
        scheme="nearest",
        vert_scheme=None,
        add_meta=None,
        use_iris=False,
        **coords,
    ) -> list[StationData]:
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
        if "collapse_scalar" in coords:  # for backwards compatibility
            collapse_scalar = coords.pop("collapse_scalar")
        else:
            collapse_scalar = True
        if self.proj_info is None:
            try:
                self.check_dimcoords_tseries()
            except DimensionOrderError:
                self.reorder_dimensions_tseries()
        pinfo = False
        if np.prod(self.shape) > 5913000:  # (shape of 2x2 deg, daily data)
            pinfo = True
            from time import time

            t0 = time()
            logger.info(
                f"Extracting timeseries data from large array (shape: {self.shape}). "
                f"This may take a while..."
            )

        # if the method makes it to this point, it is 3 or 4 dimensional
        # and the first 3 dimensions are time, latitude, longitude.
        if self.ndim == 3:  # data does not contain vertical dimension
            if use_iris:
                if sample_points is None:
                    sample_points = self._coords_to_iris_sample_points(**coords)
                result = self._to_timeseries_2D(
                    sample_points, scheme, collapse_scalar=collapse_scalar, add_meta=add_meta
                )
            else:
                if not coords:
                    coords = self._iris_sample_points_to_coords(sample_points)
                result = self._to_time_series_xarray(scheme=scheme, add_meta=add_meta, **coords)
            if pinfo:
                logger.info(
                    f"Time series extraction successful. Elapsed time: {time() - t0:.0f} s"
                )
            return result

        if sample_points is None:
            sample_points = self._coords_to_iris_sample_points(**coords)

        return self._to_timeseries_3D(
            sample_points,
            scheme,
            collapse_scalar=collapse_scalar,
            vert_scheme=vert_scheme,
            add_meta=add_meta,
        )

    def _to_time_series_xarray(self, scheme="nearest", add_meta=None, ts_type=None, **coords):
        if self.proj_info is None:
            try:
                self.check_dimcoords_tseries()
            except DimensionOrderError:
                self.reorder_dimensions_tseries()

        arr = self.to_xarray()

        if not len(coords) == 2:
            raise NotImplementedError(
                "Please provide only latitude / longitude sampling points as input"
            )
        for coord, vals in coords.items():
            if coord in ("lat", "latitude"):
                if isinstance(vals, str) or isnumeric(vals):
                    vals = [vals]
                lat = vals
            elif coord in ("lon", "longitude"):
                if isinstance(vals, str) or isnumeric(vals):
                    vals = [vals]
                lon = vals
        if lat is None or lon is None:
            raise ValueError("Please provide latitude and longitude coords")
        if self.proj_info is None:
            subset = extract_latlon_dataarray(
                arr, lat, lon, method=scheme, new_index_name="latlon"
            )
        else:
            x, y = self.proj_info.to_proj(lat, lon)
            subset = extract_latlon_dataarray(
                arr,
                lon=x,
                lat=y,
                lon_dimname=self.proj_info.x_axis,
                lat_dimname=self.proj_info.y_axis,
                method=scheme,
                new_index_name="latlon",
            )

        lat_id = subset.attrs["lat_dimname"]
        lon_id = subset.attrs["lon_dimname"]
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
        if self.proj_info is None:
            lats = subset[lat_id].data
            lons = subset[lon_id].data
        else:
            lats, lons = self.proj_info.to_latlon(subset[lon_id].data, subset[lat_id].data)
        for sidx in range(subset.shape[-1]):
            data = StationData(
                latitude=lats[sidx],
                longitude=lons[sidx],
                data_id=self.data_id,
                ts_type=self.ts_type,
            )

            data.var_info[var] = {"units": self.units}

            vals = data_np[:, sidx]

            data[var] = pd.Series(vals, index=times)
            for meta_key, meta_val in meta_iter.items():
                data[meta_key] = meta_val[sidx]
            for meta_key, meta_val in meta_glob.items():
                data[meta_key] = meta_val

            if ts_type is not None:
                data.resample_time(var, ts_type, how="mean", inplace=True)
            result.append(data)
        return result

    def _to_timeseries_2D(
        self, sample_points, scheme, collapse_scalar, add_meta=None, ts_type=None
    ):
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
            raise Exception("Developers: Debug! Users: please contact developers :)")

        data = self.interpolate(sample_points, scheme, collapse_scalar)
        var = self.var_name
        times = data.time_stamps()

        # lats, lons = tuple_list_to_lists(sample_points)
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
            j = np.where(grid_lons == lon)[0][0]

            data = StationData(
                latitude=lat, longitude=lon, data_id=self.name, ts_type=self.ts_type
            )
            data.var_info[var] = {"units": self.units}
            vals = arr[:, i, j]

            data[var] = pd.Series(vals, index=times)
            for meta_key, meta_val in meta_iter.items():
                data[meta_key] = meta_val[i]
            for meta_key, meta_val in meta_glob.items():
                data[meta_key] = meta_val

            if ts_type is not None:
                data.resample_time(var, ts_type, how="mean", inplace=True)
            result.append(data)

        return result

    def _to_timeseries_3D(
        self, sample_points, scheme, collapse_scalar, vert_scheme, add_meta=None
    ):
        # Data contains vertical dimension
        data = self._apply_vert_scheme(sample_points, vert_scheme)

        # ToDo: check if _to_timeseries_2D can be called here
        return data.to_time_series(
            sample_points=sample_points,
            scheme=scheme,
            collapse_scalar=collapse_scalar,
            add_meta=add_meta,
        )

    def _apply_vert_scheme(self, sample_points, vert_scheme):
        """Helper method that checks and infers vertical scheme for time
        series computation from 3D data (used in :func:`_to_timeseries_3D`)"""

        try:
            self.check_dimcoords_tseries()
        except DimensionOrderError:
            self.reorder_dimensions_tseries()

        cname = self.dimcoord_names[-1]

        if vert_scheme not in self.SUPPORTED_VERT_SCHEMES:
            raise ValueError(
                f"Invalid input for vert_scheme: {vert_scheme}. Supported "
                f"schemes are: {self.SUPPORTED_VERT_SCHEMES}"
            )
        if vert_scheme == "surface":
            vert_index = self._infer_index_surface_level()
            return self[:, :, :, vert_index]
        elif vert_scheme == "altitude":
            raise NotImplementedError(
                "Cannot yet retrieve timeseries at altitude levels. Coming soon..."
            )
        elif vert_scheme == "profile":
            return self
        else:
            try:
                # check if vertical scheme can be converted into valid iris
                # aggregator (in which case vertical dimension is collapsed)
                aggr = str_to_iris(vert_scheme)
            except KeyError:
                pass
            else:
                return self.collapsed(cname, aggr)

        raise NotImplementedError(
            f"Cannot yet retrieve timeseries from 4D data for vert_scheme {vert_scheme}."
        )

    def extract_surface_level(self):
        """Extract surface level from 4D field"""
        if not self.ndim == 4:
            raise DataDimensionError("Can only extract surface level for 4D gridded data object")
        idx = self._infer_index_surface_level()
        return self[:, :, :, idx]

    def _infer_index_surface_level(self):
        if not self.ndim == 4:
            raise DataDimensionError("Can only infer surface level for 4D gridded data object")
        try:
            self.check_dimcoords_tseries()
        except DimensionOrderError:
            self.reorder_dimensions_tseries()
        cname = self.dimcoord_names[-1]
        coord = self[cname]
        from pyaerocom import vert_coords as vc

        if "positive" in coord.attributes:
            if coord.attributes["positive"] == "up":
                return np.argmin(self.grid.dim_coords[3].points)
            elif coord.attributes["positive"] == "down":
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
                raise DataExtractionError(
                    "Cannot infer surface level since "
                    "global option INFER_SURFACE_LEVEL in"
                    "pyaerocom.const.GRID_IO is deactivated"
                )
            logger.info(
                f"Inferring surface level in GriddedData based on mean value of "
                f"{self.var_name} data in first and last level since CF coordinate info is "
                f"missing... The level with the largest mean value will be "
                f"assumed to be the surface. If mean values in both levels"
            )
            last_lev_idx = self.shape[-1] - 1
            if last_lev_idx == 0:
                return 0

            mean_first_idx = np.nanmean(self[0, :, :, 0].data)
            mean_last_idx = np.nanmean(self[0, :, :, last_lev_idx].data)
            if exponent(mean_first_idx) == exponent(mean_last_idx):
                raise DataExtractionError(
                    f"Could not infer surface level. "
                    f"{self.var_name} data in first and last level is of similar magnitude..."
                )
            elif mean_first_idx > mean_last_idx:
                return 0
            return last_lev_idx

    def _closest_time_idx(self, t):
        """Find closest index to input in time dimension"""
        t = self.time.units.date2num(to_pandas_timestamp(t))
        return self.time.nearest_neighbour_index(t)

    def find_closest_index(self, **dimcoord_vals):
        """Find the closest indices for dimension coordinate values"""
        idx = {}
        for dim, val in dimcoord_vals.items():
            if dim not in self.coord_names:
                raise DataDimensionError(f"No such dimension {dim}")
            elif dim == "time":
                idx[dim] = self._closest_time_idx(val)
            else:
                idx[dim] = self[dim].nearest_neighbour_index(val)
        return idx

    def isel(self, **kwargs):
        raise NotImplementedError(
            "Please use method sel for data selection based on dimension values"
        )

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
        rng_funs = {
            "time": get_time_rng_constraint,
            "longitude": get_lon_rng_constraint,
            "latitude": get_lat_rng_constraint,
        }

        coord_vals = {}
        for dim, val in dimcoord_vals.items():
            is_rng = isrange(val)
            if is_rng:
                c = rng_funs[dim](*val)
                constraints.append(c)
            else:
                if dim == "time":
                    if isnumeric(val) and val in self["time"].points:
                        _tval = val
                    else:
                        _idx = self._closest_time_idx(val)
                        _tval = self.time[_idx].points[0]
                    _cval = self["time"].units.num2date(_tval)
                    if not use_neirest and _cval != val:
                        raise DataExtractionError(
                            f"No such value {val} in dim {dim}. "
                            f"Use option use_neirest to disregard and extract neirest neighbour"
                        )
                else:
                    _idx = self[dim].nearest_neighbour_index(val)
                    _cval = self[dim][_idx].points[0]
                    if not use_neirest and _cval != val:
                        raise DataExtractionError(
                            f"No such value {val} in dim {dim}"
                            f"Use option use_neirest to disregard and extract neirest neighbour"
                        )
                coord_vals[dim] = _cval

        if coord_vals:
            constraints.append(iris.Constraint(coord_values=coord_vals))

        if len(constraints) > 0:
            c = constraints[0]
            for cadd in constraints[1:]:
                c = c & cadd
        subset = self.extract(c)
        if subset is None:
            raise DataExtractionError(
                f"Failed to extract subset for input coordinates {dimcoord_vals}"
            )
        return subset

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
            logger.info(f"Setting {self.var_name} outlier lower lim: {low:.2f}")
        if high is None:
            high = self.var_info.maximum
            logger.info(f"Setting {self.var_name} outlier upper lim: {high:.2f}")
        obj = self if inplace else self.copy()
        obj._ensure_is_masked_array()

        data = obj.grid.data

        mask = np.logical_or(data < low, data > high)
        obj.grid.data[mask] = np.ma.masked
        obj.metadata["outliers_removed"] = True
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
        """Resample time dimension using iris functionality

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
        to = TsType(to_ts_type)
        current = TsType(self.ts_type)

        if current == to:
            logger.info(f"Data is already in {to_ts_type} resolution")
            return self
        if to_ts_type not in IRIS_AGGREGATORS:
            raise TemporalResolutionError(f"Resolution {to_ts_type} cannot converted")
        elif current < to:  # current resolution is smaller than desired
            raise TemporalResolutionError(
                f"Cannot increase temporal resolution from {self.ts_type} to {to_ts_type}"
            )
        cube = self.grid

        # Create aggregators
        aggrs = ["yearly"]
        if to_ts_type not in aggrs:
            aggrs.append(to_ts_type)

        for aggr in aggrs:
            if aggr not in [c.name() for c in cube.aux_coords]:
                # this adds the corresponding aggregator to the cube
                IRIS_AGGREGATORS[aggr](cube, "time", name=aggr)
            # IRIS_AGGREGATORS[to_ts_type](cube, 'time', name=to_ts_type)
        # not downscale
        aggregated = cube.aggregated_by(aggrs, MEAN)
        data = GriddedData(aggregated, **self.metadata)
        data.metadata["ts_type"] = to_ts_type
        data.check_dimcoords_tseries()
        return data

    def _resample_time_xarray(self, to_ts_type, how, min_num_obs):
        arr = xr.DataArray.from_iris(self.cube)
        from_ts_type = self.ts_type
        try:
            rs = TimeResampler(arr)
            arr_out = rs.resample(
                to_ts_type, from_ts_type=from_ts_type, how=how, min_num_obs=min_num_obs
            )
        except ValueError:  # likely non-standard datetime objects in array (cf https://github.com/pydata/xarray/issues/3426)
            arr["time"] = self.time_stamps()
            rs = TimeResampler(arr)
            arr_out = rs.resample(
                to_ts_type, from_ts_type=from_ts_type, how=how, min_num_obs=min_num_obs
            )
        data = GriddedData(
            arr_out.to_iris(), check_unit=False, convert_unit_on_init=False, **self.metadata
        )
        data.metadata["ts_type"] = to_ts_type
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
            logger.info(
                f"Cannot infer unit when aggregating using {how}. Please set "
                f"unit in returned data object!"
            )
        try:
            data.check_dimcoords_tseries()
        except Exception:
            data.reorder_dimensions_tseries()
        return data

    def resample_time(self, to_ts_type, how=None, min_num_obs=None, use_iris=False):
        """Resample time to input resolution

        Parameters
        ----------
        to_ts_type : str
            either of the supported temporal resolutions (cf.
            :attr:`IRIS_AGGREGATORS` in :mod:`helpers`, e.g. "monthly")
        how : str
            string specifying how the data is to be aggregated, default is mean
        min_num_obs : dict or int, optional
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
            how = "mean"
        if not self.has_time_dim:
            raise DataDimensionError(f"Require time dimension in GriddedData: {self.short_str()}")
        if not use_iris:
            try:
                data = self._resample_time_xarray(to_ts_type, how, min_num_obs)
            except NotImplementedError as e:
                raise ResamplingError(
                    f"Resampling of time in GriddedData failed using xarray. "
                    f"Reason: {repr(e)}. Please try again with input arg use_iris=True"
                )
        else:
            if min_num_obs is not None or how != "mean":
                raise ValueError(
                    "min_num_obs needs to be None and how needs "
                    "to be mean for the iris resampling routine"
                )
            data = self._resample_time_iris(to_ts_type)
        return data

    def calc_area_weights(self):
        """Calculate area weights for grid"""
        if not self.has_latlon_dims:
            raise DataDimensionError(
                "Data does not have latitude and longitude "
                "dimensions. This is required for "
                "computation of area weights."
            )
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
        logger.info("Altitude filtering is not applied in GriddedData and will be skipped")
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
        """Apply a masked region filter"""

        if region_id not in const.HTAP_REGIONS:
            raise ValueError(
                f"Invalid input for region_id: {region_id}, choose from: {const.HTAP_REGIONS}"
            )

        # get Iris mask
        mask_iris = load_region_mask_iris(region_id)

        # Reads mask to griddedata
        mask = GriddedData(mask_iris, check_unit=False, convert_unit_on_init=False)
        mask = mask.regrid(self.cube)

        # mask.quickplot_map(vmin=0, vmax=1)
        npm = mask.cube.data

        if isinstance(npm, np.ma.core.MaskedArray):
            npm = npm.filled(np.nan)

        thresh_mask = npm > thresh_coast
        npm[thresh_mask] = 0
        npm[~thresh_mask] = 1

        # griddeddata = self.copy()

        try:
            if inplace:
                griddeddata = self
            else:
                griddeddata = self.copy()

            # UPDATE MASK WITH REGIONAL MASK.
            griddeddata.cube.data[:, npm.astype(bool)] = np.nan
            griddeddata.metadata["region"] = region_id

        except MemoryError:
            raise NotImplementedError("Coming soon... ")

        return griddeddata

    def crop(self, lon_range=None, lat_range=None, time_range=None, region=None):
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
                    logger.warning(
                        f"Failed to access longitude / latitude range using region ID {region}. "
                        f"Error msg: {repr(e)}"
                    )
            if not isinstance(region, Region):
                raise ValueError("Invalid input for region")
            suppl["region"] = region.name
            lon_range, lat_range = region.lon_range, region.lat_range
        if lon_range is not None and lat_range is not None:
            data = self.grid.intersection(longitude=lon_range, latitude=lat_range)
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
            assert len(time_range) == 2
            if all(isinstance(x, str | np.datetime64) for x in time_range):
                time_range = (pd.Timestamp(time_range[0]), pd.Timestamp(time_range[1]))
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
                data = data[time_range[0] : time_range[1]]
            else:
                raise DataExtractionError("Failed to apply temporal cropping")
        return GriddedData(data, check_unit=False, convert_unit_on_init=False, **suppl)

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
            raise NotImplementedError(
                "Area weighted mean can only computed "
                "for data containing latitude and "
                "longitude data"
            )
        stat = StationData()
        stat.station_name = self.data_id
        if region is not None:
            d = self.crop(region=region)
            stat["region"] = region
        else:
            d = self
        vals = d.area_weighted_mean()

        stat[self.var_name] = pd.Series(vals, d.time_stamps())
        return stat

    # redefined methods from iris.Cube class. This includes all Cube
    # processing methods that exist in the Cube class and that work on the
    # Cube and return a Cube instance. These may be expanded (e.g. for
    # instance what they accept as input
    def aerocom_filename(self, at_stations=False):  # pragma: no cover
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
        warnings.warn(
            "This method is deprecated. Please use aerocom_savename instead",
            DeprecationWarning,
            stacklevel=2,
        )
        from pyaerocom.io import FileConventionRead

        f = self.from_files[0]
        fconv = FileConventionRead().from_file(f)
        base_info = fconv.get_info_from_file(f)

        vert_code = base_info["vert_code"]
        if vert_code is None:
            vert_code = "UNDEFINED"
        if at_stations:
            vert_code += "AtStations"

        name = [
            fconv.name,
            self.name,
            self.var_name,
            vert_code,
            str(pd.Timestamp(self.start).year),
            self.ts_type,
        ]
        return f"{fconv.file_sep}".join(name) + ".nc"

    def aerocom_savename(
        self, data_id=None, var_name=None, vert_code=None, year=None, ts_type=None
    ):
        """Get filename for saving following AeroCom conventions

        Parameters
        ----------
        data_id : str, optional
            data ID used in output filename. Defaults to None, in which case
            :attr:`data_id` is used.
        var_name : str, optional
            variable name used in output filename. Defaults to None, in which
            case :attr:`var_name` is used.
        vert_code : str, optional
            vertical code used in output filename (e.g. Surface,
            Column, ModelLevel). Defaults to None, in which
            case assigned value in :attr:`metadata` is used.
        year : str, optional
            year to be used in filename. If None, then it is attempted to be
            inferred from values in time dimension.
        ts_type : str, optional
            frequency string to be used in filename. If None,
            then :attr:`ts_type` is used.

        Raises
        ------
        ValueError
            if vertical code is not provided and cannot be inferred or if
            year is not provided and data is not single year. Note that if
            year is provided, then no sanity checking is done against time
            dimension.

        Returns
        -------
        str
            output filename following AeroCom Phase 3 conventions.

        """
        from pyaerocom.io.helpers import aerocom_savename

        if vert_code is None and self.metadata.get("vert_code", None) is not None:
            vert_code = self.metadata["vert_code"]

        if vert_code in (None, ""):
            raise ValueError("Please provide vert_code")

        if data_id is None:
            data_id = self.data_id
        if var_name is None:
            var_name = self.var_name
        if year is None:
            start = pd.Timestamp(self.start).year
            stop = pd.Timestamp(self.stop).year
            if stop > start:
                raise ValueError(
                    "Cannot create AeroCom savename for multiyear data... please split first"
                )
            year = str(start)
        else:
            year = str(year)
        if ts_type is None:
            ts_type = self.ts_type
        return aerocom_savename(data_id, var_name, vert_code, year, ts_type)

    def to_xarray(self):
        """
        Convert this object to an xarray.DataArray

        Returns
        -------
        DataArray

        """
        arr = xr.DataArray.from_iris(self.cube)
        return arr

    def _check_meta_netcdf(self):
        """Get rid of empty entries and convert bools to int in meta"""
        meta_out = {}
        for k, v in self.metadata.items():
            if isinstance(v, bool):
                meta_out[k] = int(v)
            elif v is not None:
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
            output directory (must exist)
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

        if savename is None:  # use AeroCom convention
            return self._to_netcdf_aerocom(out_dir, **kwargs)
        self._check_meta_netcdf()
        fp = os.path.join(out_dir, savename)
        iris.save(self.grid, fp)

        return [fp]

    def interpolate(self, sample_points=None, scheme="nearest", collapse_scalar=True, **coords):
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
            sequence of coordinate pairs over which to interpolate. Sample
            coords should be sorted in ascending order without duplicates.
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
        """
        if isinstance(scheme, str):
            scheme = str_to_iris(scheme)
        if not sample_points:
            sample_points = []
        sample_points.extend(list(coords.items()))
        logger.info(f"Interpolating data of shape {self.shape}. This may take a while.")
        try:
            itp_cube = self.grid.interpolate(sample_points, scheme, collapse_scalar)
        except MemoryError:
            raise MemoryError("Interpolation failed since grid of interpolated Cube is too large")
        logger.info("Successfully interpolated cube")
        return GriddedData(itp_cube, **self.metadata)

    def regrid(
        self, other=None, lat_res_deg=None, lon_res_deg=None, scheme="areaweighted", **kwargs
    ):
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
            other = GriddedData(other, check_unit=False, convert_unit_on_init=False)
        if isinstance(scheme, str):
            scheme = str_to_iris(scheme, **kwargs)

        self._check_lonlat_bounds()
        self.check_lon_circular()

        if other is None:
            if any(x is None for x in (lat_res_deg, lon_res_deg)):
                raise ValueError(
                    "Missing input for regridding. Need either "
                    "other data object or both lat_res_deg and "
                    "lon_res_deg specified"
                )
            lons = self.longitude.contiguous_bounds()
            lats = self.latitude.contiguous_bounds()

            lat_range = [np.min(lats), np.max(lats)]
            lon_range = [np.min(lons), np.max(lons)]
            dummy = make_dummy_cube_latlon(
                lat_res_deg=lat_res_deg,
                lon_res_deg=lon_res_deg,
                lat_range=lat_range,
                lon_range=lon_range,
            )
            other = GriddedData(dummy, check_unit=False, convert_unit_on_init=False)

        if not (self.has_latlon_dims * other.has_latlon_dims):
            raise DataDimensionError(
                "Can only regrid data objects with latitude and longitude dimensions"
            )

        other._check_lonlat_bounds()
        other.check_lon_circular()

        data_rg = self.grid.regrid(other.grid, scheme)

        suppl = dict(**self.metadata)
        suppl["regridded"] = True
        data_out = GriddedData(data_rg, **suppl)
        return data_out

    def check_lon_circular(self):
        """Check if latitude and longitude coordinates are circular"""
        if not self.has_latlon_dims:
            raise DataDimensionError("No lat lon dimensions available...")
        if not self.longitude.circular:
            self.longitude.circular = check_coord_circular(self.longitude.points, 360)
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

    def quickplot_map(
        self, time_idx=0, xlim=(-180, 180), ylim=(-90, 90), add_mean=True, **kwargs
    ):  # pragma: no cover
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
        if "latitude" not in self.dimcoord_names:
            raise DataDimensionError("Missing latitude dimension...")
        elif "longitude" not in self.dimcoord_names:
            raise DataDimensionError("Missing longitude dimension...")
        tstr = ""
        if "time" in self.dimcoord_names:
            if not self.ndim == 3:
                raise DataDimensionError(f"Invalid number of dimensions: {self.ndim}. Expected 3.")
            if not isinstance(time_idx, int):
                try:
                    t = to_pandas_timestamp(time_idx).to_datetime64()
                    time_idx = np.argmin(abs(self.time_stamps() - t))
                except Exception:
                    raise ValueError("Failed to interpret input time stamp")

            data = self[time_idx]
            try:
                t = cftime_to_datetime64(self.time[time_idx])[0]
                tstr = datetime2str(t, self.ts_type)
            except Exception:
                try:
                    tstr = datetime2str(self.time_stamps()[time_idx], self.ts_type)
                except Exception:
                    logger.warning(f"Failed to retrieve ts_type in GriddedData {repr(self)}")
        else:
            if not self.ndim == 2:
                raise DataDimensionError(f"Invalid number of dimensions: {self.ndim}. Expected 2.")
            data = self

        from pyaerocom.plot.mapping import plot_griddeddata_on_map

        lons = self.longitude.contiguous_bounds()
        lats = self.latitude.contiguous_bounds()

        fig = plot_griddeddata_on_map(
            data=data,
            lons=lons,
            lats=lats,
            var_name=self.var_name,
            unit=self.units,
            xlim=xlim,
            ylim=ylim,
            **kwargs,
        )

        fig.axes[0].set_title(f"{self.data_id} ({self.var_name}, {tstr})")
        if add_mean:
            from pyaerocom.plot.config import COLOR_THEME

            ax = fig.axes[0]
            try:
                from pyaerocom.mathutils import exponent

                mean = data.mean()
                vstr = f"{mean:.{abs(exponent(mean)) + 1}f}"
                mustr = f"Mean={vstr}"
                u = str(self.units)
                if not u == "1":
                    mustr += f" [{u}]"
                ax.text(
                    0.02,
                    0.02,
                    mustr,
                    color=COLOR_THEME.color_map_text,
                    transform=ax.transAxes,
                    fontsize=22,
                    bbox=dict(facecolor="#ffffff", edgecolor="none", alpha=0.65),
                )
            except Exception as e:
                logger.warning(f"Failed to compute / add area weighted mean. Reason: {repr(e)}")

        return fig

    def min(self):
        """Minimum value

        Returns
        -------
        float
        """
        # make sure data is in memory
        data = self.grid.data
        if self.is_masked:
            return data.data[~data.mask].min()
        return data.min()

    def max(self):
        """Maximum value

        Returns
        -------
        float
        """
        # make sure data is in memory
        data = self.grid.data
        if self.is_masked:
            return data.data[~data.mask].max()
        return data.max()

    def nanmin(self):
        """Minimum value excluding NaNs

        Returns
        -------
        float
        """
        return np.nanmin(self.cube.data)

    def nanmax(self):
        """Maximum value excluding NaNs

        Returns
        -------
        float
        """
        return np.nanmax(self.cube.data)

    def estimate_value_range_from_data(self, extend_percent=5):
        """
        Estimate lower and upper end of value range for these data

        Parameters
        ----------
        extend_percent : int
            percentage specifying to which extend min and max values are to
            be extended to estimate the value range. Defaults to 5.

        Returns
        -------
        float
            lower end of estimated value range
        float
            upper end of estimated value range

        """
        min, max = self.nanmin(), self.nanmax()
        return estimate_value_range(vmin=min, vmax=max, extend_percent=extend_percent)

    def area_weighted_mean(self):
        """Get area weighted mean"""
        ws = self.area_weights
        collapsed = self.collapsed(coords=["longitude", "latitude"], aggregator=MEAN, weights=ws)
        return collapsed.grid.data

    def mean(self, areaweighted=True):
        """Mean value of data array

        Note
        ----
        Corresponds to numerical mean of underlying N-dimensional numpy array.
        Does not consider area-weights or any other advanced averaging.
        """
        # make sure data is in memory
        if areaweighted:
            avg = self.area_weighted_mean().mean()
            return avg

        data = self.grid.data
        if self.is_masked:
            return data.data[~data.mask].mean()
        return data.mean()

    def std(self):
        """Standard deviation of values"""
        # make sure data is in memory
        data = self.grid.data
        if self.is_masked:
            return data.data[~data.mask].std()
        return data.std()

    def _check_lonlat_bounds(self):
        """Check if longitude and latitude bounds are set and if not, guess"""
        if not self.longitude.has_bounds():
            # guess_bounds needs at least 2 values to work
            try:
                self.longitude.guess_bounds()
            except ValueError:
                pass
        if not self.latitude.has_bounds():
            # guess_bounds needs at least 2 values to work
            try:
                self.latitude.guess_bounds()
            except ValueError:
                pass

    def __getattr__(self, attr):
        return self[attr]

    def _check_coordinate_access(self, val):
        if self._coord_standard_names is None:
            self._update_coord_info()
        if val in self._coord_standard_names:
            return {"standard_name": val}
        elif val in self._coord_var_names:
            return {"var_name": val}
        elif val in self._coord_long_names:
            return {"long_name": val}
        raise CoordinateError(
            f"Could not associate one of the coordinates with input string {val}"
        )

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

    def search_other(self, var_name):
        """Searches data for another variable

        The search is constrained to the time period spanned by this object
        and it is attempted to load the same frequency. Uses :attr:`reader`
        (instance of :class:`ReadGridded` to search for the other variable
        data).

        Parameters
        ----------
        var_name : str
            variable to be searched

        Raises
        ------
        VariableNotFoundError
            if data for input variable cannot be found.

        Returns
        -------
        GriddedData
            input variable data

        """

        if var_name in self.reader.vars_provided:
            data = self.reader.read_var(
                var_name, start=self.start, stop=self.stop, ts_type=self.ts_type, flex_ts_type=True
            )
            return data
        raise VariableNotFoundError(f"Could not find variable {var_name}")

    def update_meta(self, **kwargs):
        """Update metadata dictionary

        Parameters
        ----------
        **kwargs
            metadata to be added to :attr:`metadata`.
        """
        for key, val in kwargs.items():
            if key == "var_name" and not isinstance(val, str):
                logger.warning(
                    f"Skipping assignment of var_name from metadata in GriddedData, "
                    f"since attr. needs to be str and is {val}"
                )
            else:
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
        inplace : bool
            if True, then this object will be modified and returned, else a
            copy.

        Raises
        ------

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
            raise DataDimensionError("Cannot copy coordinates: shape mismatch")
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
                raise AttributeError(f"GriddedData object has no attribute {indices_or_attr}")

        sub = self.grid.__getitem__(indices_or_attr)
        return GriddedData(sub, **self.metadata)

    def __contains__(self, val):
        """Check if variable or coordinate matches input string"""
        return val is self.data_id or val in self.coord_names

    def __dir__(self):
        return self.coord_names + super().__dir__()

    def __str__(self):
        """For now, use string representation of underlying data"""
        st = f"pyaerocom.GriddedData: ({self.var_name}, {self.data_id})\n{self._grid.__str__()}"
        return st

    def __repr__(self):
        """For now, use representation of underlying data"""
        return f"pyaerocom.GriddedData: ({self.var_name}, {self.data_id})\n{self._grid.__repr__()}"

    def __add__(self, other):
        raise NotImplementedError("Coming soon")

    def short_str(self):
        """Short string representation"""
        return f"{self.var_name} ({self.data_id}, freq={self.ts_type}, unit={self.units})"

    ### Deprecated (but still supported) stuff
    @property
    def unit(self):
        """Unit of data"""
        warnings.warn(
            "Attr. unit is deprecated, please use units instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.grid.units

    @unit.setter
    def unit(self, val):
        warnings.warn(
            "Attr. unit is deprecated, please use units instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.grid.units = val
