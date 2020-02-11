#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains high level scripts that perform certain tasks

Note
----
These are utility methods and not so much processing or plotting methods. See
e.g. highlevel_plotting.py for plotting methods.
"""
from pyaerocom import const
from pyaerocom.io.cachehandler_ungridded import CacheHandlerUngridded
import glob, os

def clear_cache():
    """
    Delete all *.pkl files in cache directory
    """
    ch = CacheHandlerUngridded()
    ch.delete_all_cache_files()
    
    for f in glob.glob('{}/*'.format(const.CACHEDIR)):
        os.remove(f)
        
    
if __name__=='__main__':
    clear_cache()
    
    