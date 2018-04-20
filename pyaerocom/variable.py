#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains functionality related to regions in pyaerocom
"""
from os.path import join, exists
from ast import literal_eval
from collections import OrderedDict as od
from warnings import warn
from configparser import ConfigParser
from pyaerocom import __dir__

class Variable(object):
    """Interface that specifies a region
    
    See `regions.ini <https://github.com/metno/pyaerocom/blob/master/
    pyaerocom/data/regions.ini>`__ file for an overview of currently available 
    default regions.
    
    Attributes
    ----------
    var_name : str
        AEROCOM variable name (see e.g. `AEROCOM protocol 
        <http://aerocom.met.no/protocol_table.html>`__ for a list of current
        variables)
    NOT COMPLETE YET
    
    Parameters
    ----------
    var_name : str
        string ID of variable (see file variables.ini for valid IDs)
    **kwargs
        additional keyword 
        
    Example
    -------
    
    >>> v = Variable(var_name="od550aer")
    >>> print(v)
    pyaeorocom Variable
    Name: od550aer
    Unit: ''
    Value range: 0 - 1.0
    Levels colorbar: [0.0, 0.01, ..., 0.9, 1.0]
    >>> v = Variable(var_name="MyOwn", map_vmin=0.2, map_vmax=0.6, unit="lightyears")
    >>> print(v)
    pyaeorocom Variable
    Name: MyOwn
    Unit: lightyears
    Value range: 0.2 - 0.6
    Levels colorbar: None
    
    """
    def __init__(self, var_name="od550aer", **kwargs):
        self.var_name = var_name
        
        self.unit = ''
        self.map_vmin = None
        self.map_vmax = None
        self.map_cbar_levels = None
        
        if isinstance(var_name, str):
           self.import_default(self.var_name) 
        
        for k, v in kwargs.items():
            if k in self.__dict__:
                self.__dict__[k] = v
        
    
    def import_default(self, var_name):
        """Import information about default region
        
        Parameters
        ----------
        name : str
            strind ID of region (must be specified in `regions.ini <https://
            github.com/metno/pyaerocom/blob/master/pyaerocom/data/regions.ini>`__ 
            file)
            
        Returns
        -------
        bool
            True, if default could be loaded, False if not
        Raises
        ------
        IOError
            if regions.ini file does not exist

        
        """
        fpath = join(__dir__, "data", "variables.ini")
        if not exists(fpath):
            raise IOError("File conventions ini file could not be found: %s"
                          %fpath)
        conf_reader = ConfigParser()
        conf_reader.read(fpath)
        if not var_name in conf_reader:
            return False
        self.var_name = var_name
        for key, val in conf_reader[var_name].items():
            if key in self.__dict__:
                if "," in val:
                    
                    val = list(literal_eval(val))# [float(x) for x in val.split(",")]
                else:
                    try:
                        val = int(val)
                    except:
                        pass
                self.__dict__[key] = val
        return True
    
    def __repr__(self):
       return ("Variable %s %s" %(self.var_name, super(Variable, self).__repr__()))
   
    def __str__(self):
        l = self.map_cbar_levels
        if l and len(l) > 4:
            cbl_str = "[%s, %s, ..., %s, %s]" %(l[0], l[1], l[-2], l[-1])
        else:
            cbl_str = "None"
        s = ("pyaeorocom Variable\nName: %s\n"
             "Unit: %s\n"
             "Value range: %s - %s\n"
             "Levels colorbar: %s"
             %(self.var_name, self.unit, self.map_vmin, self.map_vmax,
               cbl_str))
        return s
   
if __name__=="__main__":

    r = Variable("od550aer")
    
    import doctest
    doctest.testmod()