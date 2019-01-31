#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collection of station data classes
"""
import numpy as np
from pyaerocom._lowlevel_helpers import dict_to_str, list_to_shortstr

class VerticalProfile(object):
    """Object for single variable profile data
        
    Attributes
    ----------
    var_name : str
        name of variable
    data : list
        array of values
    
    """
    def __init__(self, var_name, **location_info):
        self.var_name = var_name
        
        self._data = []
        self._altitude = []
        self.dtime = []
        
        self.vert_coord_name = None
        self.vert_coord_vals = {}
        
        self.update(**location_info)
      
    def update(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v
            
    @property
    def data(self):
        """Array containing data values corresponding to data"""
        return np.float64(self._data)
    
    @data.setter
    def data(self, val):
        self._data = val
        
    @property
    def altitude(self):
        """Array containing altitude values corresponding to data"""
        if len(self._altitude) == len(self.data):
            return np.float64(self._altitude)
        return self.compute_altitude()
    
    @altitude.setter
    def altitude(self, val):
        self._altitude = val
        
    def compute_altitude(self):
        """Compute altitude based on vertical coorinate information"""
        from pyaerocom.vert_coords import _VertCoordConverter as conv
        if not self.vert_coord_info:
            raise ValueError('No information about vertical coordinate found')
        elif not self.vert_coord_name in conv.supported:
            raise ValueError('Name of vertical coordinate not registered')
        raise NotImplementedError
            
    def __len__(self):
        return len(self['data'])
    
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
            elif isinstance(v, np.ndarray) and v.ndim==1:
                arrays += "\n{} (array, {} items)".format(k, len(v))
                arrays += list_to_shortstr(v)
            else:
                s += "\n%s: %s" %(k,v)
        s += arrays
        return s
    
if __name__=="__main__":
    
    d = VerticalProfile("Blaaaaaaaa")
    d.update(dict(bla=42, blub=43))
    print(d)
        
        
        

