#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
I/O helper methods of the pyaerocom package
"""
import pyaerocom.config as paths
from pyaerocom.helpers import cftime_to_datetime64
from pyaerocom import __dir__
from os.path import join, isdir
from collections import OrderedDict as od
from os import listdir    
from iris.coords import DimCoord
from datetime import datetime
from numpy import datetime64, asarray, arange
import cf_units

TSTR_TO_NP = {"hourly"  :  "timedelta64[h]",
              "3hourly" :  "timedelta64[3h]",
              "daily"   :  "timedelta64[D]",
              "monthly" :  "timedelta64[M]"}


TSTR_TO_CF = {"hourly"  :  "hours",
              "3hourly" :  "hours",
              "daily"   :  "days",
              "monthly" :  "days"}

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
        tres_np = TSTR_TO_NP[ts_type]
        base = datetime64("%s-01-01 00:00:00" %year) 
        test_datenums = asarray([0, 1, 10])
        ts_nominal = base + test_datenums.astype(tres_np)
        ts_values = cftime_to_datetime64(test_datenums, cfunit=t.units)
        if not all(ts_values == ts_nominal):
            raise ValueError("Time match error, nominal dates for test array"
                             "%s (unit=%s): %s\nReceived values after "
                             "conversion: %s"
                             %(test_datenums, t.units.name,
                               ts_nominal, ts_values))
    except Exception as e:
        print("Invalid time dimension. Error message: %s" %repr(e))
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
    tunit_str = '%s since %s-01-01 00:00:00' %(tres_str, year)
    num = cube.shape[tindex_cube]

    tunit = cf_units.Unit(tunit_str, calendar=cf_units.CALENDAR_STANDARD)
    tres_np = TSTR_TO_NP[ts_type]
    base = datetime64("%s-01-01 00:00:00" %year) 
    times = base + arange(0, num, 1).astype(tres_np)
    # see this thread https://github.com/matplotlib/matplotlib/issues/2259/
    times = times.astype(datetime)
#    timestamps = datetime64(str(year)) + 
    time_nums = [tunit.date2num(t) for t in times]
    tcoord = DimCoord(time_nums, standard_name='time', units=tunit)
        
    #tcoord_dim = cube.coord_dims('time')
    try:
        cube.remove_coord('time')
    except:
        pass
    cube.add_dim_coord(tcoord, tindex_cube)
    return cube

def search_model_ids(update_inifile=True, check_nc_file=True):
    """Search model IDs in database
    
    Parameters
    ----------
    update_inifile : bool
        if True, the file *model_ids.txt* will be updated. The file is located
        in the installation *data* directory.
    check_nc_file : bool
        If True, only model IDs are included, for which at least one nc file
        can be detected in the corresponding renamed sub directory
    """
    model_ids = []
    for mdir in paths.MODELDIRS:
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
                    model_ids.append(item)
    model_ids = sorted(od.fromkeys(model_ids))       
    if update_inifile:
        fpath = join(__dir__, "data", "model_ids.txt")
        f = open(fpath, "w") 
        for model_id in model_ids:
            f.write("%s\n" %model_id)
        f.close()
    return model_ids

def get_all_model_ids():
    """Try to import all model IDs from file model_ids.txt in data directory"""
    try:
        with open(join(__dir__, "data", "model_ids.txt")) as f:
            model_ids = f.read().splitlines()
        f.close()
    except:
        try:
            model_ids = search_model_ids()
        except:
            raise Exception("Failed to access model IDs")
    return model_ids
    
if __name__=="__main__":
    #model_ids = search_model_ids()
    model_ids = get_all_model_ids()
    