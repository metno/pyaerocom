#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module containing helper functions related to iris I/O methods. These contain
reading of Cubes, and some methods to perform quality checks of the data, e.g.

1. checking and correction of time definition
2. number and length of dimension coordinates must match data array
3. Longitude definition from -180 to 180 (corrected if defined on 0 -> 360 intervall)

"""
import os
from datetime import datetime
from numpy import datetime64, asarray, arange
import cf_units

import iris
from iris.experimental.equalise_cubes import equalise_attributes

from pyaerocom import const, logger
from pyaerocom.exceptions import NetcdfError
from pyaerocom.helpers import cftime_to_datetime64
from pyaerocom.io.helpers import add_file_to_log
from pyaerocom.io.fileconventions import FileConventionRead

TSTR_TO_NP_DT = {"hourly"  :  "datetime64[h]",
                 "3hourly" :  "datetime64[3h]",
                 "daily"   :  "datetime64[D]",
                 "monthly" :  "datetime64[M]"}

TSTR_TO_NP_TD = {"hourly"  :  "timedelta64[h]",
                 "3hourly" :  "timedelta64[3h]",
                 "daily"   :  "timedelta64[D]",
                 "monthly" :  "timedelta64[M]"}


TSTR_TO_CF = {"hourly"  :  "hours",
              "3hourly" :  "hours",
              "daily"   :  "days",
              "monthly" :  "days"}

def load_cube_custom(file, var_name=None, grid_io=None,
                     file_convention=None):
    """Load netcdf file as iris.Cube
    
    Parameters
    ----------
    files : list
        netcdf file
    var_name : str
        name of variable to read
    quality_check : bool
        if True, then a quality check of data is performed against the
        information provided in the filename
    file_convention : :obj:`FileConventionRead`, optional
        Aerocom file convention. If provided, then the data content (e.g. 
        dimension definitions) is tested against definition in file name.
    
    Returns
    -------
    iris.cube.Cube
        loaded data as Cube
    """
    if grid_io is None:
        grid_io = const.GRID_IO
    cube_list = iris.load(file)
    _num = len(cube_list)
    if _num != 1:
        if _num == 0:
            raise NetcdfError('Data from file {} could not be loaded using iris'
                              .format(file))
        else:
            logger.warning('File {} contains more than one data '
                           'field: {}'.format(file, cube_list))
    cube = None
    if var_name is None:
        if not len(cube_list) == 1:
            vars_avail = [c.var_name for c in cube_list]
            raise NetcdfError('Could not load single cube from {}. Please '
                              'specify var_name. Input file contains the '
                              'following variables: {}'.format(file, 
                                                               vars_avail))
        cube = cube_list[0]
        var_name = cube.var_name
    else:
        for c in cube_list:
            if c.var_name == var_name:
                cube = c
    if cube is None:
        raise NetcdfError('Variable {} not available in file {}'.format(var_name, 
                                                                        file))
    if file_convention is None:
        try:
            file_convention = FileConventionRead(from_file=file)
        except:
            pass
    
    if isinstance(file_convention, FileConventionRead):
        finfo = file_convention.get_info_from_file(file)
        if grid_io.CHECK_TIME_FILENAME:
            if not check_time_coord(cube, ts_type=finfo["ts_type"], 
                                    year=finfo["year"]):
            
                msg = ("Invalid time dimension coordinate in file {}. " 
                       .format(os.path.basename(file)))
                logger.warning(msg)
                if grid_io.CORRECT_TIME_FILENAME:
                    logger.warning("Attempting to correct time coordinate "
                                   "using information in file name")
                    cube = correct_time_coord(cube, 
                                              ts_type=finfo["ts_type"],
                                              year=finfo["year"]) 
                if const.WRITE_FILEIO_ERR_LOG:
                    add_file_to_log(file, 'Invalid time dimension')
        else:
            logger.warning("WARNING: Automatic check of time "
                           "array in netCDF files is deactivated. "
                           "This may cause problems in case "
                           "the time dimension is not CF conform.")
    
    if grid_io.CHECK_DIM_COORDS:
        cube = check_dim_coords_cube(cube)
    
    try:
        if grid_io.DEL_TIME_BOUNDS:
            cube.coord("time").bounds = None
    except:
        logger.warning("Failed to access time coordinate in GriddedData")
        
    if grid_io.SHIFT_LONS:
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
    from pyaerocom import print_log
    try:
        if cube.coord("longitude").points.max() > 180:
            logger.info("Rolling longitudes to -180 -> 180 definition")
            cube = cube.intersection(longitude=(-180, 180))
    except Exception as e:
        print_log.warning('Failed to roll longitudes: {}'.format(repr(e)))
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
# =============================================================================
#         if cube.ndim == 4:
#             raise NotImplementedError('Cannot handle 4D data yet')
# =============================================================================
    if not cube.ndim == len(cube.dim_coords):
        dim_names = [c.name() for c in cube.dim_coords]
        raise NetcdfError('Dimension mismatch between data and coords.'
                          'Cube dimension: {}. Registered dimensions : {}'
                          .format(cube.ndim, dim_names))
    for i, coord in enumerate(cube.dim_coords):
        if not len(coord.points) == cube.shape[i]:
            raise NetcdfError('Length mismatch of dimension coord {} '
                              '({} points) and data dimension ({} points) '
                              .format(coord.name(), len(coord.points),
                                      cube.shape[i]))
# =============================================================================
#             if not coord.standard_name in self.VALID_DIM_STANDARD_NAMES:
#                 raise NetcdfError('Invalid standard name of dimension coord. '
#                                   'var_name: {}; standard_name: {}; '
#                                   'long_name: {}'.format(coord.var_name,
#                                                          coord.standard_name, 
#                                                          coord.long_name))
# =============================================================================

    return cube

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
        temporal resolution of data (e.g. "hourly", "daily"). This information
        is e.g. encrypted in the filename of a NetCDF file and may be 
        accessed using :class:`pyaerocom.io.FileConventionRead`
    year : int
        interger specifying year of observation, e.g. 2017
    
    Returns
    -------
    bool
        True, if time dimension is ok, False if not
    """
    
    ok = True
    test_idx = [0,1,2,7] #7, since last accessible index in a 3hourly dataset of one day is 7
    try:
        try:
            t = cube.coord("time")
        except:
            raise AttributeError("Cube does not contain time dimension")
        if not isinstance(t, iris.coords.DimCoord):
            raise AttributeError("Time is not a DimCoord instance")
        try:
            cftime_to_datetime64(0, cfunit=t.units)
        except:
            raise ValueError("Could not convert time unit string")
        tres_np = TSTR_TO_NP_TD[ts_type]
        conv = TSTR_TO_NP_DT[ts_type]
        base = datetime64("%s-01-01 00:00:00" %year).astype(conv)
        test_datenums = asarray(test_idx)
        ts_nominal = base + test_datenums.astype(tres_np)
        dts_nominal = ts_nominal[1:] - ts_nominal[:-1]
        ts_values = cftime_to_datetime64(t[test_idx].points, cfunit=t.units).astype(conv)
        dts_values = ts_values[1:] - ts_values[:-1]
        if not all(ts_values == ts_nominal):
            raise ValueError("Time match error, nominal dates for test array"
                             "%s (unit=%s): %s\nReceived values after "
                             "conversion: %s"
                             %(test_datenums, t.units.origin,
                               ts_nominal, ts_values))
        elif not all(dts_values == dts_nominal):
            raise ValueError("Time match error, time steps for test array"
                             "%s (unit=%s): %s\nReceived values after "
                             "conversion: %s"
                             %(test_datenums, t.units.origin,
                               dts_nominal, dts_values))
    except Exception as e:
        logger.warning("Invalid time dimension.\n"
                       "Error message: {}".format(repr(e)))
        ok = False
    return ok

def correct_time_coord(cube, ts_type, year):
    """Method that corrects the time coordinate of an iris Cube
    
    Parameters
    ----------
    cube : Cube
        cube containing data
    ts_type : str
        temporal resolution of data (e.g. "hourly", "daily"). This information
        is e.g. encrypted in the filename of a NetCDF file and may be 
        accessed using :class:`pyaerocom.io.FileConventionRead`
    year : int
        interger specifying year of observation, e.g. 2017
    tindex_cube : int
        index of time dimension in Cube
    
    Returns
    -------
    Cube
        the same instance of the input cube with corrected time dimension axis
        
    """
    tindex_cube = None
    dim_lens = []
    for i, coord in enumerate(cube.dim_coords):
        dim_lens.append(len(coord.points))
        if coord.name() == 'time':
            tindex_cube = i
    if tindex_cube is None:
        if cube.ndim != len(cube.dim_coords): #one dimension is missing
            for idx, dim_len in enumerate(cube.shape):
                if not dim_len in dim_lens: #candidate
                    tindex_cube = idx
    if tindex_cube is None:
        raise NetcdfError('Failed to identify data index of time dimension in '
                          'cube {}'.format(repr(cube)))
    tres_str = TSTR_TO_CF[ts_type]
    conv = TSTR_TO_NP_DT[ts_type]
    tunit_str = '%s since %s-01-01 00:00:00' %(tres_str, year)
    num = cube.shape[tindex_cube]

    tunit = cf_units.Unit(tunit_str, calendar=cf_units.CALENDAR_STANDARD)
    tres_np = TSTR_TO_NP_TD[ts_type]
    base = datetime64("%s-01-01 00:00:00" %year).astype(conv)
    times = base + arange(0, num, 1).astype(tres_np)
    # see this thread https://github.com/matplotlib/matplotlib/issues/2259/
    times_dt = times.astype("datetime64[s]").astype(datetime)
#    timestamps = datetime64(str(year)) + 
    time_nums = [tunit.date2num(t) for t in times_dt]
    tcoord = iris.coords.DimCoord(time_nums, standard_name='time', units=tunit)
        
    #tcoord_dim = cube.coord_dims('time')
    try:
        cube.remove_coord('time')
    except:
        pass
    cube.add_dim_coord(tcoord, tindex_cube)
    return cube

def concatenate_iris_cubes(cubes, error_on_mismatch=True):
    """Concatenate list of :class:`iris.Cube` instances cubes into single Cube
    
    Helper method for concatenating list of cubes and that helps 
    with handling the fact that the corresponding iris method is not well 
    defined in the sense of what it returns (i.e. instance of 
    :class:`Cube` or :class:`CubeList`, depending on whether all cubes 
    could be concatenated or not...)
    
    This method is not supposed to be called directly but rather 
    :func:`concatenate_cubes` (which ALWAYS returns instance of 
    :class:`Cube` or raises Exception) or :func:`concatenate_possible_cubes`
    (which ALWAYS returns instance of :class:`CubeList` or raises Exception)
    
    Parameters
    ----------
    cubes : CubeList
        list of individual cubes
    error_on_mismatch
        boolean specifying whether an Exception is supposed to be raised
        or not
        
    Returns
    -------
    :obj:`Cube` or :obj:`CubeList`
        result of concatenation 
    
    Raises
    ------
    iris.exceptions.ConcatenateError
        if ``error_on_mismatch=True`` and input cubes could not all concatenated
        into a single instance of :class:`iris.Cube` class.
        
    """
    var_name = cubes[0].var_name
    if const.GRID_IO.EQUALISE_METADATA:
        meta_init = cubes[0].metadata
        if not all([x.metadata == meta_init for x in cubes]):
            logger.warning("{} cubes to be concatenated have different meta "
                           "data settings. These will be unified using the "
                           "metadata dictionary of the first cube "
                           "(otherwise the method concatenate of the iris "
                           "package won't work)".format(var_name))
            for cube in cubes:
                cube.metadata = meta_init
                
    #now put the CubeList together and form one cube
    #1st equalise the cubes (remove non common attributes)
    equalise_attributes(cubes)
    #unify time units
    iris.util.unify_time_units(cubes)
    
    #now concatenate the cube list to one cube
    cubes_concat = iris._concatenate.concatenate(cubes, error_on_mismatch)
    
    return cubes_concat[0]

if __name__== "__main__":
    import pyaerocom as pya
    
    ddir = '/lustre/storeA/project/aerocom/aerocom-users-database/SATELLITE-DATA/CALIOP3/renamed/'
    f1 = 'aerocom.CALIOP3.monthly.ec5323Ddust.2006.nc'
    fconv = pya.io.FileConventionRead(from_file=f1)
    cube = load_cube_custom(ddir + f1)
    print(cube)
    
    data = pya.GriddedData(cube)
    print(data.start)
    print(data.stop)
    print(data)