#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 13:01:34 2019

@author: hannas
"""

from pyaerocom.region import Region
from pyaerocom.filter import Filter


class LandSeaMask(object):
    MASK_FILENAMSE = {'EUROPE' : 'XY.nc'}
    def __init__(self, name):
        # call super
        self._name = None
        self.name = name
    
    @property
    def name(self):
        return self.name
    
    @name.setter
    def name(self, value):
        if not self._name_exists(value):
            raise ValueError()
        self._name = value
        
    def load_mask_file(self):
        from pyaerocom import const
        try:
            data_dir = const.SUPPLDIRS['landseamasks']
        except KeyError:
            raise 
    def real_hpt_region():
        pass
    
    # need def apply filter to ungridded, gridded and 
    