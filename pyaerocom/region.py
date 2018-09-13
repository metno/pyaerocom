#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains functionality related to regions in pyaerocom
"""
from os.path import join, exists
from ast import literal_eval
from collections import OrderedDict as od
from configparser import ConfigParser
from pyaerocom import __dir__
from pyaerocom._lowlevel_helpers import BrowseDict

class Region(BrowseDict):
    """Interface that specifies an AEROCOM region
    
    Note
    ----
    Extended dictionary-like object
    
    Attributes
    ----------
    name : str
        ID of region (e.g. "EUROPE")
    lon_range : :obj:`list` or :obj:`tuple`
        longitude range (min, max) covered by region
    lat_range : :obj:`list` or :obj:`tuple`
        latitude range (min, max) covered by region
    lon_range_plot : :obj:`list` or :obj:`tuple`
        longitude range (min, max) used for plotting region. Defaults to 
        values of :attr:`lon_range` but may be extended, see e.g.
        `the example of india <http://aerocom.met.no/DATA/SURFOBS/
        ECMWF_OSUITE_NRT/plots/OD550_AER_an2018_d20180319_INDIA_MAP.ps.png>`__
    lat_range_plot : :obj:`list` or :obj:`tuple`
        latitude range (min, max) used for plotting region. Defaults to 
        values of :attr:`lat_range` but may be extended, see e.g.
        `the example of india <http://aerocom.met.no/DATA/SURFOBS/
        ECMWF_OSUITE_NRT/plots/OD550_AER_an2018_d20180319_INDIA_MAP.ps.png>`__
    
    Parameters
    ----------
    name : str
        ID of region (e.g. "EUROPE")
    lon_range : :obj:`list` or :obj:`tuple`
        longitude range (min, max) covered by region
    lat_range : :obj:`list` or :obj:`tuple`
        latitude range (min, max) covered by region
        
    Example
    -------
    Just initiate with a valid region ID
    
        >>> from pyaerocom import Region
        >>> europe = Region("EUROPE")
        >>> india = Region("INDIA")
        >>> print(europe)
        pyaeorocom Region
        Name: EUROPE
        Longitude range: [-20, 70]
        Latitude range: [30, 80]
        Longitude range (plots): [-20, 70]
        Latitude range (plots): [30, 80]
        >>> print(india)
        pyaeorocom Region
        Name: INDIA
        Longitude range: [65, 90]
        Latitude range: [5, 35]
        Longitude range (plots): [50, 100]
        Latitude range (plots): [0, 40]
        
    """
    def __init__(self, name="WORLD", lon_range=None, lat_range=None, 
                 **kwargs):
        self._name = name
        # longitude / latitude range of data import
        self.lon_range = lon_range
        self.lat_range = lat_range
        
        # longitude / latitude range of data import
        self.lon_range_plot = None
        self.lat_range_plot = None
        
        self.lon_ticks = None
        self.lat_ticks = None
        
        if isinstance(name, str):
           self.import_default(name) 
        
        for k, v in kwargs.items():
            if k in self:
                self[k] = v
    
    @property
    def name(self):
        return self._name
    
    def import_default(self, name):
        """Import information about default region
        
        Parameters
        ----------
        name : str
            strind ID of region (must be specified in `regions.ini <https://
            github.com/metno/pyaerocom/blob/master/pyaerocom/data/regions.ini>`__ 
            file)
            
        Raises
        ------
        IOError
            if regions.ini file does not exist
        NameError
            if default region with ID specified by input parameter ``name`` 
            cannot be found in regions.ini file
        """
        fpath = join(__dir__, "data", "regions.ini")
        if not exists(fpath):
            raise IOError("File conventions ini file could not be found: %s"
                          %fpath)
        conf_reader = ConfigParser()
        conf_reader.read(fpath)
        if not name in conf_reader:
            raise NameError("No default available for %s" %name)
        self._name = name
        for key, val in conf_reader[name].items():
            if key in self.keys():
                if "," in val:
                    #list of values
                    val = list(literal_eval(val))#[float(x) for x in val.split(",")]
                else:
                    try:
                        val = int(val)
                    except:
                        pass
                self[key] = val
        if self.lon_range_plot is None:
            self.lon_range_plot = self.lon_range
        if self.lat_range_plot is None:
            self.lat_range_plot = self.lat_range
    
    def __repr__(self):
       return ("Region %s %s" %(self.name, super(Region, self).__repr__()))
   
    def __str__(self):
        s = ("pyaeorocom Region\nName: %s\n"
             "Longitude range: %s\n"
             "Latitude range: %s\n" 
             "Longitude range (plots): %s\n"
             "Latitude range (plots): %s" 
             %(self.name, self.lon_range, self.lat_range,
               self.lon_range_plot, self.lat_range_plot))
        return s

def get_all_default_region_ids():
    """Get list containing IDs of all default regions
    
    Returns
    -------
    list
        all default region IDs (sections in `regions.ini <https://github.com/
        metno/pyaerocom/blob/master/pyaerocom/data/regions.ini>`__ file)
    """
    fpath = join(__dir__, "data", "regions.ini")
    if not exists(fpath):
        raise IOError("File conventions ini file could not be found: %s"
                      %fpath)
    conf_reader = ConfigParser()
    conf_reader.read(fpath)
    all_ids = []
    for rid, region in conf_reader.items():
        if not rid == "DEFAULT":
            all_ids.append(rid)
        
    return all_ids

def get_all_default_regions():
    """Get dictionary containing all default regions from region.ini file
    
    Note
    ----
        The values are already :class:`Region` instances, use 
        :func:`get_all_default_region_ids`
    
    Returns
    -------
    dict
        dictionary containing all default regions that are found in 
        the `regions.ini <https://github.com/metno/pyaerocom/blob/
        master/pyaerocom/data/regions.ini>`__ file
        
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
    
    regions = get_all_default_regions()
    for region_id, region in regions.items():
        print(region)
        
    all_ids = get_all_default_region_ids()
    