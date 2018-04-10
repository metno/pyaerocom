#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains functionality related to regions in pyaerocom
"""
from os.path import join, exists
from collections import OrderedDict as od
from configparser import ConfigParser
from pyaerocom import __dir__

class Region:
    """Interface that specifies a region
    
    See e.g. `here <>`__ for an overview of currently available default 
    region.
    """
    def __init__(self, name="WORLD", lon_range=None, lat_range=None, 
                 **kwargs):
        self.name = name
        # longitude / latitude range of data import
        self.lon_range = lon_range
        self.lat_range = lat_range
        
        # longitude / latitude range of data import
        self.lon_range_plot = None
        self.lat_range_plot = None
        
        self.lon_ticks = None
        self.lat_ticks = None
        
        try:
           self.import_default(self.name) 
        except:
           pass
    
    def import_default(self, name):
        fpath = join(__dir__, "data", "regions.ini")
        if not exists(fpath):
            raise IOError("File conventions ini file could not be found: %s"
                          %fpath)
        conf_reader = ConfigParser()
        conf_reader.read(fpath)
        if not name in conf_reader:
            raise NameError("No default available for %s" %name)
        self.name = name
        for key, val in conf_reader[name].items():
            if key in self.__dict__:
                if "," in val:
                    val = [float(x) for x in val.split(",")]
                else:
                    try:
                        val = int(val)
                    except:
                        pass
                self.__dict__[key] = val
        if self.lon_range_plot is None:
            self.lon_range_plot = self.lon_range
        if self.lat_range_plot is None:
            self.lat_range_plot = self.lat_range
    
    def __repr__(self):
       return ("Region %s %s" %(self.name, super(Region, self).__repr__()))
   
    def __str__(self):
        s = ("pyaeorocom Region\nName: %s\nLongitude range: %s\nLatitude "
             "range: %s" %(self.name, self.lon_range, self.lat_range))
        return s

def get_default_regions():
    """Get dictionary containing all default region IDs from region.ini file
    
    Returns
    -------
    dict
        dictionary containing all default regions that are found in 
        
    """
    fpath = join(__dir__, "data", "regions.ini")
    if not exists(fpath):
        raise IOError("File conventions ini file could not be found: %s"
                      %fpath)
    conf_reader = ConfigParser()
    conf_reader.read(fpath)
    all_regions = od()
    for region in conf_reader:
        if not region == "DEFAULT":
            all_regions[region] = Region(region)
        
    return all_regions
   
if __name__=="__main__":
    r = Region()
    r.import_default("EUROPE")
    
    regions = get_default_regions()
    for region_id, region in regions.items():
        print(region)