#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
I/O helper methods of the pyaerocom package
"""
from pyaerocom import const, logger
from pyaerocom.io import AerocomBrowser
from pyaerocom.helpers import cftime_to_datetime64
from pyaerocom import __dir__
from os.path import join, exists, isdir
from os import listdir
from collections import OrderedDict as od

from iris.coords import DimCoord
from iris.experimental.equalise_cubes import equalise_attributes
from iris.util import unify_time_units
from iris._concatenate import concatenate

from datetime import datetime
from numpy import datetime64, asarray, arange
import cf_units

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

def add_file_to_log(filepath, err_msg, model_or_obs_id):
    logdir = const.LOGFILESDIR
    found = False
    logfile = join(logdir, model_or_obs_id + '.log')
    if exists(logfile):
        with open(logfile, 'r') as f:
            for line in f:
                if filepath == line.strip():
                    found = True
                    break
        
    if not found:
        with open(logfile, 'a+') as f:
            f.write(filepath + '\n')
        with open(join(logdir, model_or_obs_id + '_ERR.log'), 'a+') as ferr:
            ferr.write('{}\n{}\n\n'.format(filepath,
                                           err_msg))
        

def search_data_dir_aerocom(name_or_pattern, ignorecase=True):
    """Search Aerocom data directory based on model / data ID
    """
    browser = AerocomBrowser()
    return browser.find_data_dir(name_or_pattern, ignorecase)

def get_obsnetwork_dir(obs_id):
    """Returns data path for obsnetwork ID
    
    Parameters
    ----------
    obs_id : str
        ID  of obsnetwork (e.g. AeronetSunV2Lev2.daily)
        
    Returns
    -------
    str
        corresponding directory from ``pyaerocom.const``
        
    Raises
    ------
    ValueError
        if obs_id is invalid
    IOError
        if directory does not exist
    """
    if not obs_id in const.OBS_IDS:
        raise ValueError("Observation network ID {} does not exist".format(obs_id))
        
    data_dir = const.OBSCONFIG[obs_id]['PATH']
    if not exists(data_dir):
        raise IOError("Data directory {} of observation network {} does not "
                      "exists".format(data_dir, obs_id))
    return data_dir
    
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
        if not isinstance(t, DimCoord):
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

def correct_time_coord(cube, ts_type, year, tindex_cube=0):
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
    tcoord = DimCoord(time_nums, standard_name='time', units=tunit)
        
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
    unify_time_units(cubes)
    
    #now concatenate the cube list to one cube
    cubes_concat = concatenate(cubes, error_on_mismatch)
    
    return cubes_concat

def search_names(update_inifile=True, check_nc_file=True):
    """Search model IDs in database
    
    Parameters
    ----------
    update_inifile : bool
        if True, the file *names.txt* will be updated. The file is located
        in the installation *data* directory.
    check_nc_file : bool
        If True, only model IDs are included, for which at least one nc file
        can be detected in the corresponding renamed sub directory
    """
    names = []
    for mdir in const.MODELDIRS:
        print("\n%s\n" %mdir)
        sub = listdir(mdir)
        for item in sub:
            path = join(mdir, item, "renamed")
            if isdir(path):
                print("\n%s\n" %path)
                add = True
                if check_nc_file:
                    add = False
                    for name in listdir(path):
                        if name.endswith(".nc"):
                            add = True
                            break
                if add:
                    names.append(item)
    names = sorted(od.fromkeys(names))
    if update_inifile:
        fpath = join(__dir__, "data", "names.txt")
        f = open(fpath, "w") 
        for name in names:
            f.write("%s\n" %name)
        f.close()
    return names

def get_all_names():
    """Try to import all model IDs from file names.txt in data directory"""
    try:
        with open(join(__dir__, "data", "names.txt")) as f:
            names = f.read().splitlines()
        f.close()
    except:
        try:
            names = search_names()
        except:
            raise Exception("Failed to access model IDs")
    return names
    
if __name__=="__main__":
    #names = search_names()
    names = get_all_names()
    