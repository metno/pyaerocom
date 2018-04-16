#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
I/O helper methods of the pyaerocom package
"""
import pyaerocom.config as paths
from pyaerocom import __dir__
from os.path import exists, join, isdir, basename
from os import listdir
try:
    from CongigParser import ConfigParser
except ModuleNotFoundError:
    from configparser import ConfigParser

def search_model_ids(update_inifile=True):
    model_ids = []
    for mdir in paths.MODELDIRS:
        print("\n%s\n" %mdir)
        sub = listdir(mdir)
        for item in sub:
            path = join(mdir, item, "renamed")
            if isdir(path):
                print("\n%s\n" %path)
                model_ids.append(item)
    if update_inifile:
        fpath = join(__dir__, "data", "paths.ini")
        parser = ConfigParser()
        f = open(fpath, "w") 
        if not "models" in parser.sections():
            parser.add_section("models")
        idstr = ",".join([str(val) for val in model_ids])
        parser.set("models", "names", idstr)
        parser.write(f)
        f.close()
    return model_ids

if __name__=="__main__":
    model_ids = search_model_ids()