#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
I/O helper methods of the pyaerocom package
"""
from pyaerocom import const
from pyaerocom.helpers import cftime_to_datetime64
from pyaerocom import __dir__
from os.path import join, isdir
from collections import OrderedDict as od
from os import listdir    
from iris.coords import DimCoord
from datetime import datetime
from numpy import datetime64, asarray, arange
import cf_units
import fnmatch, re

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


def search_data_dir_aerocom(name_or_pattern, ignorecase=True, 
                            verbose=const.VERBOSE):
    """Search Aerocom data directory based on model / data ID
    
    Parameters
    ----------
    name_or_pattern : str
        name of model
    verbose : bool
        print output
        
    Returns
    -------
    str
        Model directory
        
    Raises
    ------
    IOError
        if model directory cannot be found
    """
    pattern = fnmatch.translate(name_or_pattern)
    _candidates = []
    _msgs = []
    #
    for obs_id in const.OBS_IDS:
        if ignorecase:
            match = name_or_pattern.lower() == obs_id.lower()
        else:
            match = name_or_pattern == obs_id
        if match:
            if verbose:
                print("Found match for search pattern in obs network "
                      "directories {}".format(obs_id))
            return const.OBSCONFIG[obs_id]["PATH"]
        else:
            if ignorecase:
                match = bool(re.search(pattern, obs_id, re.IGNORECASE))
            else:
                match = bool(re.search(pattern, obs_id))
        if match:
            _candidates.append(obs_id)
        
    for search_dir in const.MODELDIRS:
        # get the directories
        if isdir(search_dir):
            #subdirs = listdir(search_dir)
            subdirs = [x for x in listdir(search_dir) if isdir(join(search_dir, x))]
            for subdir in subdirs:
                
                if ignorecase:
                    match = bool(re.search(pattern, subdir,re.IGNORECASE))
                else:
                    match = bool(re.search(pattern, subdir))
                if match:
                    ok = True
                    if ignorecase:
                        match = name_or_pattern.lower() == subdir.lower()
                    else:
                        match = name_or_pattern == subdir
                    if match:
                        ok = True
                        if verbose:
                            print("Found match for ID {}".format(name_or_pattern))
                        _dir = join(search_dir, subdir)
                        if const.GRID_IO.USE_RENAMED_DIR:
                            if verbose:
                                print("Checking if renamed directory exists")
                            _dir = join(_dir, "renamed")
                        if isdir(_dir):
                            if verbose:
                                print('Found directory {}'.format(_dir))    
                            return _dir
                        else:
                            ok = False
                            if verbose:
                                _msgs.append("Renamed folder does not exist "
                                      "in {}".format(join(search_dir, subdir)))
                    if ok:
                        _candidates.append(subdir)
        else:
            if verbose:
                _msgs.append('directory %s does not exist\n'
                             %search_dir)
    for msg in _msgs:
        print(msg)
    msg=""
    if _candidates:
        if len(_candidates) == 1:
            if verbose:
                print("Found exactly one match for search pattern "
                      "{}: {}".format(name_or_pattern, _candidates[0]))
                return _candidates[0]
        else:
            msg = ("Found multiple matches. Please choose from the "
                  "following list: {}".format(_candidates))
        
    raise IOError("No unique match found for ID ot pattern {}. "
                  "{}".format(name_or_pattern, msg))

def search_data_dir_aerocom_old(name, verbose=const.VERBOSE):
    """Search Aerocom data directory based on model / data ID
    
    Parameters
    ----------
    name : str
        name of model
    verbose : bool
        print output
        
    Returns
    -------
    str
        Model directory
        
    Raises
    ------
    IOError
        if model directory cannot be found
    """
    sid = name
    _candidates = []
    _msgs = []
    for search_dir in const.MODELDIRS:
        if verbose:
            print('Searching dir for ID %s in: %s' 
                  %(name, search_dir))
        # get the directories
        if isdir(search_dir):
            #subdirs = listdir(search_dir)
            subdirs = [x for x in listdir(search_dir) if isdir(join(search_dir, x))]
            for subdir in subdirs:
                if sid == subdir:
                    _dir = join(search_dir, subdir)
                    if const.GRID_IO.USE_RENAMED_DIR:
                        _dir = join(_dir, "renamed")
                    if isdir(_dir):
                        if verbose:
                            print('Found directory: {}'.format(_dir))    
                        return _dir
                    else:
                        if verbose:
                            _msgs.append("renamed folder does not exist "
                                  "in {}".format(join(search_dir, subdir)))
                elif (sid.lower() in subdir.lower()):
                    _candidates.append(subdir)
        else:
            if verbose:
                _msgs.append('directory: %s does not exist\n'
                             %search_dir)
    print("Model directory could not be found.")
    for msg in _msgs:
        print(msg)

    if _candidates:
        print("Did you mean either of: {} ?".format(_candidates))
    raise IOError("Model directory for name {} could not be found".format(name))
    
def check_time_coord(cube, ts_type, year, verbose=const.VERBOSE):
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
                             %(test_datenums, t.units.name,
                               ts_nominal, ts_values))
        elif not all(dts_values == dts_nominal):
            raise ValueError("Time match error, time steps for test array"
                             "%s (unit=%s): %s\nReceived values after "
                             "conversion: %s"
                             %(test_datenums, t.units.name,
                               dts_nominal, dts_values))
    except Exception as e:
        if verbose:
            print("Invalid time dimension.\n"
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
    