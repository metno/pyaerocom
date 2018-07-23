#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collection of station data classes
"""
import numpy as np
from pyaerocom.utils import dict_to_str, list_to_shortstr, BrowseDict

class VerticalProfile(BrowseDict):
    """Dict-like object for single variable profile data
    
    .. seealso::
        
        Base class :class:`Station`
        
    Attributes
    ----------
    var_name : str
        name of variable
    data : list
        array of values
    
    """
    def __init__(self, var_name, **location_info):
        self.var_name = var_name
        
        self.data = []
        self.altitude = []
        self.dtime = []
        
        self.update(**location_info)
        
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
        
        
        

