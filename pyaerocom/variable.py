#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains functionality related to regions in pyaerocom
"""
from os.path import join, exists
from ast import literal_eval
from configparser import ConfigParser
from pyaerocom import __dir__, logger
from pyaerocom.utils import BrowseDict, list_to_shortstr, dict_to_str

class Variable(BrowseDict):
    """Interface that specifies default settings for a variable
    
    See `variables.ini <https://github.com/metno/pyaerocom/blob/master/
    pyaerocom/data/variables.ini>`__ file for an overview of currently available 
    default variables.
    
    Parameters
    ----------
    var_name : str
        string ID of variable (see file variables.ini for valid IDs)
    **kwargs
        any valid class attribute (e.g. map_vmin, map_vmax, ...)
        
    Attributes
    ----------
    var_name : str
        AEROCOM variable name (see e.g. `AEROCOM protocol 
        <http://aerocom.met.no/protocol_table.html>`__ for a list of current
        variables)
    
    
    
        
    Example
    -------
    
    >>> v = Variable(var_name="od550aer")
    >>> print(v)
    pyaeorocom Variable
    Name: od550aer
    Unit: None
    Value range: 0 - 1.0
    Levels colorbar: [0.0, 0.01, ..., 0.9, 1.0]
    Colorbar ticks: [0.0, 0.02, ..., 0.7, 0.9]
    >>> v = Variable(var_name="MyOwn", map_vmin=0.2, map_vmax=0.6, unit="lightyears")
    >>> print(v)
    pyaeorocom Variable
    Name: MyOwn
    Unit: lightyears
    Value range: 0.2 - 0.6
    Levels colorbar: None
    Colorbar ticks: None
    
    """
    def __init__(self, var_name="od550aer", **kwargs):
        self.var_name = var_name
        
        self.unit = None
        self.aliases = []
        
        # settings for scatter plots
        self.scat_xlim = None
        self.scat_ylim = None
        self.scat_loglog = None
        self.scat_scale_factor = 1.0
        
        # settings for map plotting
        self.map_vmin = None
        self.map_vmax = None
        self.map_c_over = None 
        self.map_c_under = None
        self.map_cbar_levels = None
        self.map_cbar_ticks = None
        
        # imports default information and, on top, variable information (if 
        # applicable)
        self.parse_from_ini(var_name) 
        
        self.update(**kwargs)
            
    def parse_from_ini(self, var_name=None):
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
        
        var_info = {}
        if var_name is not None and var_name != 'DEFAULT':
            if var_name in conf_reader:
                logger.info("Found default configuration for variable "
                            "{}".format(var_name))
                var_info = conf_reader[var_name]
                self.var_name = var_name
            else:
                logger.warning("No default configuration available for "
                               "variable {}. Using DEFAULT settings".format(var_name))
            
        default = conf_reader['DEFAULT']
        
        for key in self.keys():
            ok = True
            if key in var_info:
                val = var_info[key]
            elif key in default:
                val = default[key]
            else:
                ok = False
            if ok:
                if "," in val:
                    val = list(literal_eval(val))# [float(x) for x in val.split(",")]
                else:
                    try:
                        val = int(val)
                    except:
                        try:
                            val = float(val)
                        except:
                            pass
                self[key] = val
    
    def unit_str(self):
        if self.unit is None:
            return ''
        else:
            return '[{}]'.format(self.unit)
        
    def __repr__(self):
       return ("Variable %s %s" %(self.var_name, super(Variable, self).__repr__()))
   
    def __str__(self):
        head = "Pyaerocom {}".format(type(self).__name__)
        s = "\n{}\n{}".format(head, len(head)*"-")
        arrays = ''
        for k, v in self.items():
            if isinstance(v, dict):
                s += "\n{} (dict)".format(k)
                s = dict_to_str(v, s)
            elif isinstance(v, list):
                s += "\n{} (list, {} items)".format(k, len(v))
                s += list_to_shortstr(v)
            else:
                s += "\n%s: %s" %(k,v)
        s += arrays
        return s
    
if __name__=="__main__":

    v = Variable("od550aer", the_answer=42)
    print(v)
    #import doctest
    #doctest.testmod()