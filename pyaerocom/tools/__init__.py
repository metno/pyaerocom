#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 11:34:57 2021

@author: jonasg
"""
def browse_database(*args, **kwargs):
    from pyaerocom.io.utils import browse_database
    return browse_database(*args, **kwargs)

def clear_cache():
    """
    Delete all *.pkl files in cache directory
    """
    from pyaerocom.io.cachehandler_ungridded import CacheHandlerUngridded
    ch = CacheHandlerUngridded()
    ch.delete_all_cache_files()