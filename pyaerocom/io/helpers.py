#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
I/O helper methods of the pyaerocom package
"""
from pyaerocom import const
from pyaerocom.io import AerocomBrowser
from pyaerocom import __dir__
import os
from pyaerocom.exceptions import (VarNotAvailableError, VariableDefinitionError)


from collections import OrderedDict as od

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

def add_file_to_log(filepath, err_msg):
    
    try:
        dirname = os.path.dirname(filepath)
        spl = dirname.split(os.sep)
        if spl[-1].lower() == 'renamed':
            model_or_obs_id = spl[-2]
        else:
            model_or_obs_id = spl[-1]
    except:
        model_or_obs_id = 'others'
    logdir = const.LOGFILESDIR
    found = False
    logfile = os.path.join(logdir, model_or_obs_id + '.log')
    if os.path.exists(logfile):
        with open(logfile, 'r') as f:
            for line in f:
                if filepath == line.strip():
                    found = True
                    break
        
    if not found:
        with open(logfile, 'a+') as f:
            f.write(filepath + '\n')
        with open(os.path.join(logdir, model_or_obs_id + '_ERR.log'), 'a+') as ferr:
            ferr.write('{}\n{}\n\n'.format(filepath,
                                           err_msg))
        
def get_standard_name(var_name):
    """Get standard name of aerocom variable
    
    Parameters
    ----------
    var_name : str
        HTAP2 variable name
    
    Returns
    --------
    str
        corresponding standard name
        
    Raises
    ------
    VarNotAvailableError
        if input variable is not defined in *variables.ini* file
    VariableDefinitionError
        if standarad name is not set for variable in *variables.ini* file
    """
    if not var_name in const.VAR_PARAM:
        raise VarNotAvailableError('No such variable {}. Check variables.ini'.format(var_name))
    name = const.VAR_PARAM[var_name].standard_name
    if name is None:
        raise VariableDefinitionError('standard_name not defined for variable')
    return name

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
    if not os.path.exists(data_dir):
        raise IOError("Data directory {} of observation network {} does not "
                      "exists".format(data_dir, obs_id))
    return data_dir

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
        sub = os.listdir(mdir)
        for item in sub:
            path = os.path.join(mdir, item, "renamed")
            if os.path.isdir(path):
                print("\n%s\n" %path)
                add = True
                if check_nc_file:
                    add = False
                    for name in os.listdir(path):
                        if name.endswith(".nc"):
                            add = True
                            break
                if add:
                    names.append(item)
    names = sorted(od.fromkeys(names))
    if update_inifile:
        fpath = os.path.join(__dir__, "data", "names.txt")
        f = open(fpath, "w") 
        for name in names:
            f.write("%s\n" %name)
        f.close()
    return names

def get_all_names():
    """Try to import all model IDs from file names.txt in data directory"""
    try:
        with open(os.path.join(__dir__, "data", "names.txt")) as f:
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
    