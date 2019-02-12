#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collection of station data classes
"""
import numpy as np
from pyaerocom._lowlevel_helpers import dict_to_str, list_to_shortstr, BrowseDict

class VerticalProfile(object):
    """Object for single variable profile data
        
    Attributes
    ----------
    var_name : str
        name of variable
    
    """
    def __init__(self, data=None, altitude=None, var_name=None, 
                 unit=None, **location_info):
        self.var_name = var_name
        
        self._data = []
        self._data_err = []
        self._altitude = []
        self.dtime = []
        
        self.var_info = BrowseDict()
        self.var_info['altitude'] = {}
        
        self.vert_coord_name = None
        self.vert_coord_vals = {}
        
        self.update(**location_info)
        
        if data is not None:
            self.data = data
        if altitude is not None:
            self.altitude = altitude
        if unit is not None:
            self.unit = unit
      
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
    def data_err(self):
        """Array containing data values corresponding to data"""
        return np.float64(self._data_err)
    
    @data_err.setter
    def data_err(self, val):
        self._data_err = val
        
    @property
    def altitude(self):
        """Array containing altitude values corresponding to data"""
        if len(self._altitude) == len(self._data):
            return np.float64(self._altitude)
        return self.compute_altitude()
    
    def compute_altitude(self):
        """Compute altitude based on vertical coorinate information"""
        from pyaerocom.vert_coords import _VertCoordConverter as conv
        if not self.vert_coord_info:
            raise ValueError('No information about vertical coordinate found')
        elif not self.vert_coord_name in conv.supported:
            raise ValueError('Name of vertical coordinate not registered')
        raise NotImplementedError
        
    @altitude.setter
    def altitude(self, val):
        self._altitude = val
        
    @property
    def unit(self):
        if not 'unit' in self.var_info[self.var_name]:
            raise ValueError('Unit is not defined')
            
    @unit.setter
    def unit(self, val):
        self.set_unit(self.var_name, val)
        
    def set_unit(self, val, attr_name=None, auto_convert=True):
        """Set"""
        raise NotImplementedError
        
    
        
    def plot(self, whole_alt_range=False, rot_xlabels=30, **kwargs):
        """Simple plot method for vertical profile"""
        import matplotlib.pyplot as plt
        if 'figsize' in kwargs:
            figsize = kwargs.pop('figsize')
        else:
            figsize = (4, 8)
        if 'ax' in kwargs:
            ax = kwargs.pop('ax')
        else:
            _, ax = plt.subplots(1,1, figsize=figsize)
        ax.plot(self.data, self.altitude, '-x', **kwargs)
        if rot_xlabels:
            for lbl in ax.get_xticklabels():
                lbl.set_rotation(rot_xlabels)
                
        xlab = self.var_name
        ylab = 'Altitude'
        try:
            xlab += ' [{}]'.format(self.var_info[self.var_name]['unit'])
        except:
            pass
        
        try:
            ylab += ' [{}]'.format(self.var_info['altitude']['unit'])
        except:
            pass
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)
        
        if whole_alt_range:
            ax.set_ylim([np.min([0, self.altitude.min()]), self.altitude.max()])
        ax.figure.tight_layout()
        return ax
            
            
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
        
        
        

