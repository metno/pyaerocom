#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Small helper utility functions for pyaerocom
"""

class _BrowserDict(dict):
    """Dictionary with get and set attribute methods
    """
    def __getattr__(self, key):
        return self[key]
    
    def __setattr__(self, key, val):
        self[key] = val
       

def str_underline(s):
    """Create underlined string"""
    return "{}\n{}\n".format(s, len(s)*"-")

