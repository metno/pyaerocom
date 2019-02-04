#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 13:26:36 2019

@author: jonasg
"""
import os
import numpy as np
from pyaerocom._lowlevel_helpers import BrowseDict
from pyaerocom import const

class DataSource(BrowseDict):
    """Dict-like object defining a data source
    
    Attributes
    ----------
    data_id
        name (or ID) of dataset (e.g. AeronetSunV3Lev2.daily)
    dataset_name
        name of dataset (e.g. AERONET)
    data_product
        data product (e.g. SDA, Inv, Sun for Aeronet)
    data_version
        version of data (e.g. 3)
    data_level 
        level of data (e.g. 2)
    revision_date
        last revision date of dataset
    ts_type_src 
        sampling frequency as defined in data files (use None if undefined)
    
    
    """
    _types = dict(dataset_name  =   str,
                  data_product  =   str,
                  data_version  =   float,
                  data_level    =   float,
                  ts_type_src   =   str,
                  revision_date =   np.datetime64)
    
    _ini_file_name = 'data_sources.ini'
    def __init__(self, **info):

        self.data_id = None
        self.dataset_name = None
        self.data_product = None
        self.data_version = None
        self.data_level = None
        self.revision_date = None
        
        self.ts_type_src = None
        
        self.update(**info)
        if self.data_id is not None:
            self._parse_source_info_from_ini()
        
    @property
    def data_dir(self):
        """Directory containing data files"""
        from pyaerocom.io.helpers import get_obsnetwork_dir
        return get_obsnetwork_dir(self.data_id)
    
    def _parse_source_info_from_ini(self):
        """Parse source info from ini file"""
        try:
            from ConfigParser import ConfigParser
        except:
            from configparser import ConfigParser
        cfg = ConfigParser()
        file = os.path.join(const.DIR_INI_FILES, self._ini_file_name)
        if not os.path.exists(file):
            raise IOError('File {} does not exist'.format(self._ini_file_name))
        cfg.read(file)
        if self.data_id in cfg:
            for k, v in cfg[self.data_id].items():
                if k in self:
                    self[k] = self._types[k](v)
    
# =============================================================================
#     def __setitem__(self, key, val):
#         super(DataSource, self).__setitem__(key, val)
#         if key == 'data_id':
#             self._parse_source_info_from_ini()
# =============================================================================
            
            
              
class StationMetaData(DataSource):
    """This object defines a standard for station metadata in pyaerocom
    
    Variable names associated with meta data can vary significantly between 
    different conventions (e.g. conventions in modellers community vs. 
    observations community). 
    
    Note
    ----
    - This object is a dictionary and can be easily expanded
    - In many cases, only some of the attributes are relevant
    
    Attributes
    ----------
    station_name
        name or ID of a station. Note, that the concept of a station in 
        pyaerocom is not necessarily related to a fixed coordinate. A station
        can also be a satellite, ship, or a human walking around and measuring
        something
    instrument_name 
        name (or ID) of instrument
    PI 
        principal investigator
    ts_type
        frequency of data (e.g. monthly). Note the difference between 
        :attr:`ts_type_src` of :class:`DataSource`, which specifies the freq.
        of the original files.
    latitude
        latitude coordinate
    longitude 
        longitude coordinate
    altitude
        altitude coordinate
    
    """
    def __init__(self, **info):
        
        self.station_name = None
        self.instrument_name = None
        self.PI = None
        
        self.ts_type = None
        self.latitude = None
        self.longitude = None
        self.altitude = None
        
        super(StationMetaData, self).__init__(**info)
        
if __name__ == '__main__':
    meta = StationMetaData(data_id = 'AeronetSunV3Lev2.daily',
                           ts_type = 'blaaaa')
    print(meta)