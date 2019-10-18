#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 13:01:34 2019

Message from Jonas 

Think we should stick to that (namely that the filtering is done in the data object). 
The idea that I have currently is that all data objects (ColocatedData, UngriddedData, GriddedData) 
get a new method filter_region(self, region_id) which has all the logic to filter either rectangles 
but which can also handle the masks if the input region_id corresponds to a mask. If we have it like 
that, we can also get rid of the private sub methods _apply_gridded, _apply_ungridded, _apply_colocated
 in the Filter class (because then we can call the filter_region class in Filter.apply directly).

We also should think about the altitude filtering (currently in Filter only 
applied for UngriddedData), which should also happen in the data objects, 
e.g. via filter_region(self, region_id, alt_range=None).

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
    