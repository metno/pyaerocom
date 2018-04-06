#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Low level classes and methods for reading
"""
from collections import OrderedDict as od
from os.path import join, exists
try:
    from ConfigParser import ConfigParser
except: 
    from configparser import ConfigParser
from pyaerocom import __dir__

class FileConventionRead:
    """Class that represents a file naming convention for reading Aerocom files
    
    Attributes
    ----------
    name : str
        name of this convention (e.g. "aerocom3")
    file_sep : str
        filename delimiter for accessing different variables
    year_pos : int
        position of year information in filename after splitting using 
        delimiter :attr:`file_sep` 
    var_pos : int
        position of variable information in filename after splitting using 
        delimiter :attr:`file_sep` 
    ts_pos : int
        position of information of temporal resolution in filename after 
        splitting using delimiter :attr:`file_sep` 
    """
    def __init__(self, name="aerocom3", file_sep=None, year_pos=None,
                 var_pos=None, ts_pos=None):
       self.name = name
       self.file_sep = file_sep
       self.year_pos = year_pos
       self.var_pos = var_pos
       self.ts_pos = ts_pos
       
       try:
           self.import_default(self.name) 
       except:
           pass
       
    def import_default(self, name):
        """Checks and load default information from database"""
        fpath = join(__dir__, "data", "file_conventions.ini")
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
                try:
                    val = int(val)
                except:
                    pass
                self.__dict__[key] = val
                
    
    def from_dict(self, new_vals):
        """Load info from dictionary
        
        Parameters
        ----------
        new_vals : dict
            dictionary containing information
        
        Returns
        -------
        self
        """
        for k, v in new_vals.items():
            if k in self.__dict__:
                self.__dict__[k] = v
        return self
    
    def to_dict(self):
        """Convert this object to ordered dictionary"""
        return od(name = self.name,
                  file_sep = self.file_sep,
                  year_pos = self.year_pos,
                  var_pos = self.var_pos,
                  ts_pos = self.ts_pos)
                
    def __str__(self):
        s = "pyaeorocom FileConventionRead\n"
        for k, v in self.to_dict().items():
            s += "%s: %s\n" %(k, v)
        return s
    
if __name__=="__main__":
    conf = FileConventionRead()
    
    print(conf)
        
    d = od(name = "Fake",
           file_sep = 10,
           year_pos = -6,
           var_pos = 15,
           ts_pos = 3)
    print(conf.from_dict(d))
    try:
        conf.import_default("blaaa")
    except NameError:
        print("Works as expected")
    conf.import_default("aerocom3")
    print(conf)
    
    conf = FileConventionRead(name="aerocom2")
    print(conf)