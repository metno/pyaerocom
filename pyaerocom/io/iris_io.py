"""
Module containing helper functions related to iris I/O methods. These contain
reading of Cubes, and some methods to perform quality checks of the data, e.g.

1. checking and correction of time definition
2. number and length of dimension coordinates must match data array
3. Longitude definition from -180 to 180 (corrected if defined on 0 -> 360 interval)
"""

import logging
from datetime import datetime

import cf_units
import iris
import iris.coords
import iris.util

from pyaerocom.units.helpers import get_standard_unit

try:
    # as of iris version 3
    from iris.util import equalise_attributes
except ImportError:
    # old iris version installed
    from iris.experimental.equalise_cubes import equalise_attributes

from pathlib import Path
from traceback import format_exc

import numpy as np

from pyaerocom import const
from pyaerocom.exceptions import (
    FileConventionError,
    NetcdfError,
    UnresolvableTimeDefinitionError,
    VariableDefinitionError,
)
from pyaerocom.helpers import make_datetimeindex_from_year
from pyaerocom.io.file_conventions import FileConventionRead
from pyaerocom.io.helpers import add_file_to_log
from pyaerocom.units.datetime import TsType, cftime_to_datetime64

from pyaerocom.units import Unit

logger = logging.getLogger(__name__)


def load_cubes_custom(files, var_name=None, file_convention=None, perform_fmt_checks=True):
    """Load multiple NetCDF files into CubeList

    Note
    ----
    This function does not apply any concatenation or merging of the variable
    data in the individual files, it only loads the files into individual
    instances of :class:`iris.cube.Cube`, which can be accessed via the
    returned list.

    Parameters
    ----------
    files : list
        list of netcdf file paths
    var_name : str
        name of variable to be imported from input files.
    file_convention : :obj:`FileConventionRead`, optional
        Aerocom file convention. If provided, then the data content (e.g.
        dimension definitions) is tested against definition in file name
    perform_fmt_checks : bool
        if True, additional quality checks (and corrections) are (attempted to
        be) performed.

    Returns
    -------
    list
        loaded cube instances.
    list
        list containing all files from which the input variable could be
        successfully loaded.
    """
    cubes = []
    loaded_files = []

    for i, _file in enumerate(files):
        try:
            cube = load_cube_custom(
                file=_file,
                var_name=var_name,
                file_convention=file_convention,
                perform_fmt_checks=perform_fmt_checks,
            )
            cubes.append(cube)
            loaded_files.append(_file)
        except Exception:
            msg = f"Failed to load {_file}. Reason: {format_exc()}"
            logger.warning(msg)

            if const.WRITE_FILEIO_ERR_LOG:
                add_file_to_log(_file, msg)
    return (cubes, loaded_files)


def load_cube_custom(file, var_name=None, file_convention=None, perform_fmt_checks=None):
    """Load netcdf file as iris.Cube

    Parameters
    ----------
    file : str
        netcdf file
    var_name : str
        name of variable to read
    quality_check : bool
        if True, then a quality check of data is performed against the
        information provided in the filename
    file_convention : :obj:`FileConventionRead`, optional
        Aerocom file convention. If provided, then the data content (e.g.
        dimension definitions) is tested against definition in file name
    perform_fmt_checks : bool
        if True, additional quality checks (and corrections) are (attempted to
        be) performed.

    Returns
    -------
    iris.cube.Cube
        loaded data as Cube
    """
    if isinstance(file, Path):
        file = str(file)  # iris load does not like PosixPath
    if perform_fmt_checks is None:
        perform_fmt_checks = const.GRID_IO.PERFORM_FMT_CHECKS

    cube_list = iris.load(file)
    cube = None
    if var_name is None:
        if not len(cube_list) == 1:
            vars_avail = [c.var_name for c in cube_list]
            raise NetcdfError(
                f"Could not load single cube from {file}. Please "
                f"specify var_name. Input file contains the "
                f"following variables: {vars_avail}"
            )
        cube = cube_list[0]
        var_name = cube.var_name
    else:
        for c in cube_list:
            if c.var_name == var_name:
                cube = c
                break
    if cube is None:
        raise NetcdfError(f"Variable {var_name} not available in file {file}")
    if perform_fmt_checks:
        cube = _cube_quality_check(cube, file, file_convention)
    return cube


def _cube_quality_check(cube, file, file_convention=None):
    """Perform quality check of loaded cube data

    This includes the following checks (not all of them may be applicable):

        - Make sure dimensionless variables have unit 1 (and not empty string)

    """
    coords = get_coord_names_cube(cube)
    try:
        cube = _check_cube_unitless(cube)
    except VariableDefinitionError:
        pass

    grid_io = const.GRID_IO
    if grid_io.CHECK_TIME_FILENAME:
        try:
            cube = _check_correct_time_dim(cube, file, file_convention)
        except FileConventionError:
            logger.warning(
                "WARNING: failed to check / validate "
                "time dim. using information in "
                "filename. Reason: invalid file name "
                "convention"
            )

    if grid_io.CHECK_DIM_COORDS:
        cube = check_dim_coords_cube(cube)

    if "time" in coords and grid_io.DEL_TIME_BOUNDS:
        cube.coord("time").bounds = None

    if "longitude" in coords and grid_io.SHIFT_LONS:
        cube = check_and_regrid_lons_cube(cube)
    return cube


def check_and_regrid_lons_cube(cube):
    """Checks and corrects for if longitudes of :attr:`grid` are 0 -> 360

    Note
    ----
    This method checks if the maximum of the current longitudes array
    exceeds 180. Thus, it is not recommended to use this function after
    subsetting a cube, rather, it should be checked directly when the
    file is loaded (cf. :func:`load_input`)

    Parameters
    ----------
    cube : iris.cube.Cube
        gridded data loaded as iris.Cube

    Returns
    -------
    bool
        True, if longitudes were on 0 -> 360 and have been rolled, else
        False
    """
    if cube.coord("longitude").points.max() > 180:
        logger.info(
            "Rearranging longitude dimension from 0 -> 360 definition to -180 -> 180 definition"
        )
        cube = cube.intersection(longitude=(-180, 180))
    return cube


def check_dim_coord_names_cube(cube):
    from pyaerocom import const

    coords = dict(
        lon=const.COORDINFO["lon"],
        lat=const.COORDINFO["lat"],
        time=const.COORDINFO["time"],
    )

    for coord in cube.dim_coords:
        cv, cs, cn = coord.var_name, coord.standard_name, coord.long_name
        c = None
        if cv in coords:
            c = coords[cv]
        elif cs in coords:
            c = coords[cs]
        elif cn in coords:
            c = coords[cn]
        if c is not None:
            var_name = c.var_name
            std_name = c.standard_name
            lng_name = c.long_name
            if not coord.var_name == var_name:
                logger.warning(
                    f"Invalid var_name {coord.standard_name} for "
                    f"coord {coord.var_name} in cube. Overwriting with {std_name}"
                )
                coord.var_name = var_name
            if not coord.standard_name == std_name:
                logger.warning(
                    f"Invalid standard_name {coord.standard_name} for "
                    f"coord {coord.var_name} in cube. Overwriting with {std_name}"
                )
                coord.standard_name = std_name
            if not coord.long_name == lng_name:
                logger.warning(
                    f"Invalid long_name {coord.long_name} for "
                    f"coord {coord.var_name} in cube. Overwriting with {lng_name}"
                )
                coord.long_name = lng_name
    return cube


def check_dim_coords_cube(cube):
    """Checks, and if necessary and applicable, updates coords names in Cube

    Parameters
    ----------
    cube : iris.cube.Cube
        input cube

    Returns
    -------
    iris.cube.Cube
        updated or unchanged cube
    """
    cube = check_dim_coord_names_cube(cube)
    return cube


def _check_cube_unitless(cube):
    """Make sure unit in Cube is 1 if variable is dimensionless"""
    var = cube.var_name
    if var not in const.VARS:
        raise VariableDefinitionError(f"No such pyaerocom default variable: {cube.var_name}")

    unit = Unit(cube.units)
    if str(get_standard_unit(var)) == "1" and unit.is_unknown():
        cube.units = Unit("1")
    return cube


def _get_info_from_filename(file, file_convention=None):
    """Load meta-information from filename

    Parameters
    ----------
    """
    if file_convention is None:
        file_convention = FileConventionRead(from_file=file)
    return file_convention.get_info_from_file(file)


def _check_correct_time_dim(cube, file, file_convention=None):
    """Check if time dimension in input Cube is correct

    Note
    -----
    Needs information about time dimension encoded in filename, since the
    check is done against what is specified in the filename. E.g. AeroCom
    format
    Parameters
    ----------
    cube : iris.cube.Cube
        loaded Cube instance, for which time dimension is supposed to be
        checked
    file : str
        path to file from which the Cube was imported
    file_convention : FileConventionRead
        file naming convention specifying how time dimension information is
        encoded in the filenames.

    """
    finfo = _get_info_from_filename(file, file_convention)

    ts_type = TsType(finfo["ts_type"])
    year = finfo["year"]

    if not const.MIN_YEAR <= year <= const.MAX_YEAR:
        raise FileConventionError(f"Invalid year in file: {year}")
    elif year == 9999:
        logger.info(
            "Cannot compare NetCDF time dimension for climatological data "
            "(9999 in filename). Skipping this check."
        )
    else:
        try:
            check_time_coord(cube, ts_type, year)
        except UnresolvableTimeDefinitionError as e:
            raise UnresolvableTimeDefinitionError(repr(e))
        except Exception as e:
            msg = f"Invalid time dimension coordinate in file:\n{file}.\nError: repr({e})\n"
            logger.warning(msg)
            if const.GRID_IO.CORRECT_TIME_FILENAME:
                add_msg = "Attempting to correct time coordinate using information in file name"
                msg += add_msg
                logger.info(add_msg)
                try:
                    cube = correct_time_coord(cube, ts_type=finfo["ts_type"], year=finfo["year"])
                except Exception:
                    add_msg = (
                        f"Unable to correct time dimension using the "
                        f"information provided in the file name. Error:\n"
                        f"{format_exc()}.\n\nThe file will be imported regardless!"
                    )
                    msg += add_msg
                    logger.warning(msg)
            if const.WRITE_FILEIO_ERR_LOG:
                add_file_to_log(file, msg)
    return cube


def _check_leap_year(num, num_per, ts_type):
    if ts_type == "daily" and num + 1 == num_per:
        return True
    elif ts_type == "3hourly" and num + 8 == num_per:
        return True
    elif ts_type == "hourly" and num + 24 == num_per:
        return True
    return False


def check_time_coord(cube, ts_type, year):
    """Method that checks the time coordinate of an iris Cube

    This method checks if the time dimension of a cube is accessible and
    according to the standard (i.e. fully usable). It only checks, and does not
    correct. For the latter, please see :func:`correct_time_coord`.

    Parameters
    ----------
    cube : Cube
        cube containing data
    ts_type : str
        pyaerocom ts_type
    year :
        year of data

    Returns
    -------
    bool
        True, if time dimension is ok, False if not
    """
    if isinstance(ts_type, str):
        ts_type = TsType(ts_type)
    if "time" not in get_coord_names_cube(cube):
        raise AttributeError("Cube does not contain time dimension")
    tdim = cube.coord("time")

    if not isinstance(tdim, iris.coords.DimCoord):
        raise AttributeError("Time is not a DimCoord instance")
    try:
        cftime_to_datetime64(0, cfunit=tdim.units)
    except Exception:
        raise ValueError("Could not convert time unit string")

    freq = ts_type.to_pandas_freq()

    tidx = make_datetimeindex_from_year(freq, year)

    num_per = len(tidx)
    num = len(tdim.points)

    if not num == num_per:
        if tidx[0].is_leap_year:
            if not _check_leap_year(num, num_per, ts_type):
                raise UnresolvableTimeDefinitionError(
                    f"Expected {len(tidx)} timestamps but data has {num}"
                )

        else:
            raise UnresolvableTimeDefinitionError(
                f"Expected {len(tidx)} timestamps but data has {num}"
            )

    # ToDo: check why MS is not working for period conversion
    if freq == "MS":
        freq = "M"
    # convert first and last timestamps of index array into periods
    # (e.g. January and December for monthly data)
    per0 = tidx[0].to_period(freq)
    per1 = tidx[-1].to_period(freq)

    # first and last timestamp in data
    t0, t1 = cftime_to_datetime64([tdim.points[0], tdim.points[-1]], cfunit=tdim.units)

    if not per0.start_time <= t0 <= per0.end_time:
        raise ValueError(f"First timestamp of data {t0} does not lie in first period: {per0}")
    elif not per1.start_time <= t1 <= per1.end_time:
        raise ValueError(f"Last timestamp of data {t1} does not lie in end period: {per1}")


def get_dim_names_cube(cube):
    return [c.name() for c in cube.dim_coords]


def get_coord_names_cube(cube):
    return [c.name() for c in cube.coords()]


def _get_time_index_cube(cube):
    """
    Get array index of time dimension for input Cube

    Parameters
    ----------
    cube : iris.cube.Cube
        data cube.

    Raises
    ------
    IndexError
        if index cannot be retrieved (e.g. data does not contain time
        dimension).

    Returns
    -------
    int

    """
    dim_names = get_dim_names_cube(cube)
    if "time" in dim_names:
        return dim_names.index("time")

    idx_miss = []
    if cube.ndim != len(dim_names):  # one dimension is missing
        for idx in range(len(cube.shape)):
            coords = cube.coords(contains_dimension=idx, dim_coords=True)
            if len(coords) == 0:
                idx_miss.append(idx)
    if len(idx_miss) == 1:
        return idx_miss[0]

    raise IndexError(f"Failed to identify data index of time dimension in cube {repr(cube)}")


def correct_time_coord(cube, ts_type, year):
    """Method that corrects the time coordinate of an iris Cube

    Parameters
    ----------
    cube : Cube
        cube containing data
    ts_type : TsType or str
        temporal resolution of data (e.g. "hourly", "daily"). This information
        is e.g. encoded in the filename of a NetCDF file and may be
        accessed using :class:`pyaerocom.io.FileConventionRead`
    year : int
        integer specifying start year, e.g. 2017

    Returns
    -------
    Cube
        the same instance of the input cube with corrected time dimension axis

    """
    tindex_cube = _get_time_index_cube(cube)
    coords = get_coord_names_cube(cube)

    if isinstance(ts_type, str):
        ts_type = TsType(ts_type)

    tres_str = ts_type.cf_base_unit
    conv = ts_type.datetime64_str
    tunit_str = f"{tres_str} since {year}-01-01 00:00:00"
    num = cube.shape[tindex_cube]

    tunit = Unit(tunit_str, calendar=cf_units.CALENDAR_STANDARD)
    tres_np = ts_type.timedelta64_str  # TSTR_TO_NP_TD[ts_type]
    base = np.datetime64(f"{year}-01-01 00:00:00").astype(conv)
    times = base + np.arange(0, num, 1).astype(tres_np)

    # see this thread https://github.com/matplotlib/matplotlib/issues/2259/
    times_dt = times.astype("datetime64[s]").astype(datetime)

    time_nums = [tunit.date2num(t) for t in times_dt]

    pd_freq = ts_type.to_pandas_freq()
    num_expected = len(make_datetimeindex_from_year(pd_freq, year))
    num_inferred = len(time_nums)
    if not num_inferred == num_expected:
        raise UnresolvableTimeDefinitionError(
            f"expected {num_expected} timestamps for {year} and "
            f"freq {ts_type} but got {num_inferred}"
        )
    tcoord = iris.coords.DimCoord(time_nums, standard_name="time", units=tunit)
    if "time" in coords:
        cube.remove_coord("time")

    cube.add_dim_coord(tcoord, tindex_cube)
    cube.attributes["timedim-corrected"] = True
    return cube


def _check_correct_dtypes_timedim_cube_list(cubes):
    try:
        dtypes = np.unique([cube.coord("time").points.dtype for cube in cubes])
    except iris.exceptions.CoordinateNotFoundError:
        return False
    corrected = False
    if len(dtypes) > 1:
        corrected = True
        for cube in cubes:
            new = cube.coord("time").points.astype(float)
            cube.coord("time").points = new
    return corrected


def concatenate_iris_cubes(cubes, error_on_mismatch=True):
    """Concatenate list of :class:`iris.Cube` instances cubes into single Cube

    Helper method for concatenating list of cubes

    This method is not supposed to be called directly but rather
    :func:`concatenate_cubes` (which ALWAYS returns instance of
    :class:`Cube` or raises Exception) or :func:`concatenate_possible_cubes`
    (which ALWAYS returns instance of :class:`CubeList` or raises Exception)

    Parameters
    ----------
    cubes : CubeList or list(Cubes)
        list of individual cubes
    error_on_mismatch
        boolean specifying whether an Exception is supposed to be raised
        or not

    Returns
    -------
    :obj:`Cube`
        result of concatenation

    Raises
    ------
    iris.exceptions.ConcatenateError
        if ``error_on_mismatch=True`` and input cubes could not all concatenated
        into a single instance of :class:`iris.Cube` class.

    """
    cubes = iris.cube.CubeList(cubes)
    var_name = cubes[0].var_name
    if const.GRID_IO.EQUALISE_METADATA:
        meta_init = cubes[0].metadata
        if not all([x.metadata == meta_init for x in cubes]):
            logger.warning(
                f"{var_name} cubes to be concatenated have different meta data settings. "
                f"These will be unified using the metadata dictionary of the first cube "
                f"(otherwise the method concatenate of the iris package won't work)"
            )
            for cube in cubes:
                cube.metadata = meta_init

    # now put the CubeList together and form one cube
    # 1st equalise the cubes (remove non common attributes)
    equalise_attributes(cubes)
    # unify time units
    iris.util.unify_time_units(cubes)
    # now concatenate the cube list to one cube

    try:
        cubes_concat = iris.cube.CubeList.concatenate_cube(cubes, error_on_mismatch)
    except Exception:
        if _check_correct_dtypes_timedim_cube_list(cubes):
            cubes_concat = iris.cube.CubeList.concatenate_cube(cubes, error_on_mismatch)
        else:
            raise

    return cubes_concat
