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
    stat_merge_pref_attr : str
        optional, a metadata attribute that is available in data and that
        is used to order the individual stations by relevance in case overlaps
        occur. The associated values of this attribute need to be sortable 
        (e.g. revision_date). This is only relevant in case overlaps occur. 
    """
    _types = dict(dataset_name          =   str,
                  data_product          =   str,
                  data_version          =   float,
                  data_level            =   float,
                  ts_type_src           =   str,
                  stat_merge_pref_attr  =   str, 
                  revision_date         =   np.datetime64,
                  website               =   str)
    
    _ini_file_name = 'data_sources.ini'
    def __init__(self, **info):

        self.data_id = None
        self.dataset_name = None
        self.data_product = None
        self.data_version = None
        self.data_level = None
        self.revision_date = None
        self.website = None
        
        self.ts_type_src = None
        
        self.stat_merge_pref_attr = None
        
        self.update(**info)
        if self.data_id is not None:
            self._parse_source_info_from_ini()
        
    @property
    def data_dir(self):
        """Directory containing data files"""
        from pyaerocom.io.helpers import get_obsnetwork_dir
        return get_obsnetwork_dir(self.data_id)
    
    
    def dataset_str(self):
        s = ''
        if self.dataset_name is not None:
            s += self.dataset_name
            hasv = False
            if self.data_version is not None:
                s += '(v{}'.format(self.data_version)
                hasv = True
            if self.data_level is not None:
                if hasv:
                    s += ', Lev {})'.format(self.data_level)
                else:
                    s += '(Lev {})'.format(self.data_level)
            else:
                s += ')'
        else:
            s += self.data_id
        return s
    
    def load_dataset_info(self):
        """Wrapper for :func:`_parse_source_info_from_ini`"""
        try:
            self._parse_source_info_from_ini()
        except:
            pass
        
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
                if k in self._types:
                    self[k] = self._types[k](v)
                else:
                    self[k] = str(v)
              
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
    filename : str
        name of file (may be full path or only filename)
    station_id : str
        Code or unique ID of station
    station_name :str
        name or ID of a station. Note, that the concept of a station in 
        pyaerocom is not necessarily related to a fixed coordinate. A station
        can also be a satellite, ship, or a human walking around and measuring
        something
    instrument_name : str
        name (or ID) of instrument
    PI : str
        principal investigator
    country : str
        string specifying country (or country ID)
    ts_type : str
        frequency of data (e.g. monthly). Note the difference between 
        :attr:`ts_type_src` of :class:`DataSource`, which specifies the freq.
        of the original files.
    latitude : float
        latitude coordinate
    longitude : float
        longitude coordinate
    altitude : float
        altitude coordinate
    
    """
    def __init__(self, **info):
        
        self.filename = None
        
        self.station_id = None
        self.station_name = None
        self.instrument_name = None
        self.PI = None
        
        self.country = None
        
        self.ts_type = None
        
        self.latitude = np.nan
        self.longitude = np.nan
        self.altitude = np.nan
        
        super(StationMetaData, self).__init__(**info)
                
     
if __name__ == '__main__':
    meta = StationMetaData(data_id = 'AeronetSunV3Lev2.daily',
                           ts_type = 'blaaaa')
    print(meta)
    print(meta.dataset_str())