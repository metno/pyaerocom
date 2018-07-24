#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 11:07:06 2018

@author: jonasg
"""
import os
try:
    from ConfigParser import ConfigParser
except: 
    from configparser import ConfigParser
from ast import literal_eval

from pyaerocom import __dir__, logger
from pyaerocom.utils import BrowseDict


class EbasVarInfo(BrowseDict):
    """EBAS I/O variable information for Aerocom
    
    See `variables.ini <https://github.com/metno/pyaerocom/blob/master/
    pyaerocom/data/variables.ini>`__ file for an overview of currently available 
    default variables.
    
    Attributes
    ----------
    var_name : str
        Aerocom variable name
    
    """
    def __init__(self, var_name="od550aer", init=True, **kwargs):
        self.var_name = var_name
        
        self.component = None
        self.matrix = None
        self.instrument = None
        
        self.requires = None
        self.scale_factor = None
        # imports default information and, on top, variable information (if 
        # applicable)
        if init:
            self.parse_from_ini(var_name) 
        
    @staticmethod
    def PROVIDES_VARIABLES():
        data = EbasVarInfo.open_config()
        return [k for k in data.keys()]
        
    @staticmethod
    def open_config():
        fpath = os.path.join(__dir__, "data", "ebas_config.ini")
        if not os.path.exists(fpath):
            raise IOError("Ebas config file could not be found: %s"
                          %fpath)
        conf_reader = ConfigParser()
        conf_reader.read(fpath)
        return conf_reader
    
    def parse_from_ini(self, var_name=None, conf_reader=None):
        """Import information about default region
        
        Parameters
        ----------
        var_name : str
            strind ID of region (must be specified in `regions.ini <https://
            github.com/metno/pyaerocom/blob/master/pyaerocom/data/regions.ini>`__ 
            file)
        conf_reader : ConfigParser
            open config parser object
            
        Returns
        -------
        bool
            True, if default could be loaded, False if not
        
        Raises
        ------
        IOError
            if regions.ini file does not exist

        
        """
        if conf_reader is None:
            conf_reader = self.open_config()
        
        if not var_name in conf_reader:
            raise IOError("No variable information found for {}".format(var_name))
        var_info = conf_reader[var_name]
        for key in self.keys():
            if key in var_info:
                val = var_info[key]
                if key == 'var_name':
                    self[key] = val
                elif key =='scale_factor':
                    self[key] = val.split(',')[0]
                else:
                    self[key] = [x for x in val.split(',')]

   
    def __str__(self):
        head = "Pyaerocom {}".format(type(self).__name__)
        s = "\n{}\n{}".format(head, len(head)*"-")
        for k, v in self.items():
                s += "\n%s: %s" %(k,v)
        return s
    
if __name__=="__main__":
    pv = EbasVarInfo.PROVIDES_VARIABLES()
    print(pv)
    
    info = EbasVarInfo('WET_SO4T')
    print(info)