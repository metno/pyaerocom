#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
I/O helper methods of the pyaerocom package
"""
import pyaerocom.config as paths
from pyaerocom import __dir__
from os.path import join, isdir
from collections import OrderedDict as od
from os import listdir

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
    