#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pyaerocom.station import Station
from pyaerocom import VerticalProfile
from pyaerocom.utils import list_to_shortstr

class StationData(Station):
    """Dict-like base class for single station data
    
    .. seealso::
        
        Base class :class:`Station`
        
    Attributes
    ----------
    dtime : list
        list / array containing index values
    
    """
    NAMES_STAT_COORDS = {'latitude' : 'stat_lat', 
                         'longitude': 'stat_lon', 
                         'altitude' : 'stat_alt'}
    
    def __init__(self, *args, **kwargs):
        # these three variables may or may not be set. As you can see in the 
        # methods __getitem__ and __setitem__, if they are not set
        # explicitely, the returned value is the corresponding station 
        # coordinate. This enables flexible behaviour when it comes to 
        # treatment of these objects, since the general keywords can be used
        # (rather than the station specific ones) to access coordinates
        self._data_coords = {'latitude' : None, 
                             'longitude': None,
                             'altitude' : None}
        self.dtime = []
        self.instrument_name=None
        super(StationData, self).__init__(*args, **kwargs)
        
    @property
    def data_columns(self):
        """List containing all data columns
        
        Iterates over all key / value pairs and finds all values that are 
        lists or numpy arrays that match the length of the time-stamp array 
        (attr. ``time``)
        
        Returns
        -------
        list
            list containing N arrays, where N is the total number of 
            datacolumns found. 
        """
        self.check_dtime()
        num = len(self.dtime)
        cols = {}
        for k, v in self.items():
            if k is 'dtime':
                continue
            elif isinstance(v, list):
                v = np.asarray(v)
            elif isinstance(v, VerticalProfile):
                raise NotImplementedError("This feature is not yet supported "
                                          "for data objects that contain also "
                                          "profile data")
            if isinstance(v, np.ndarray) and len(v) == num:
                cols[k] = v
        if not cols:
            raise AttributeError("No datacolumns could be found")
        return cols
    
    def check_dtime(self):
        """Checks if dtime attribute is array or list"""
        if not any([isinstance(self.dtime, x) for x in [list, np.ndarray]]):
            raise TypeError("dtime attribute is not iterable: {}".format(self.dtime))
        elif not len(self.dtime) > 0:
            raise AttributeError("No timestamps available")         
    
    def to_dataframe(self):
        """Convert this object to pandas dataframe
        
        Find all key/value pairs that contain observation data (i.e. values
        must be list or array and must have the same length as attribute 
        ``time``)
        
        """
        return pd.DataFrame(data=self.data_columns, index=self.dtime)
    
    def to_timeseries(self, var_name):
        """Get pandas.Series object for one of the data columns
        
        Parameters
        ----------
        var_name : str
            name of variable (e.g. "od550aer")
        
        Returns
        -------
        Series
            time series object
        
        Raises 
        ------
        KeyError
            if variable key does not exist in this dictionary
        ValueError
            if length of data array does not equal the length of the time array
        """
        if not var_name in self:
            raise KeyError("Variable {} does not exist".format(var_name))
        self.check_dtime()
        data = self[var_name]
        if not data.ndim == 1:
            raise NotImplementedError('Multi-dimensional data columns cannot '
                                      'be converted to time-series')
        if not len(data) == len(self.dtime):
            raise ValueError("Mismatch between length of data array for "
                             "variable {} (length: {}) and time array  "
                             "(length: {}).".format(var_name, len(data), 
                               len(self.dtime)))
        return pd.Series(data, index=self.dtime)
    
    def plot_variable(self, var_name, **kwargs):
        """Plot timeseries for variable
        
        Parameters
        ----------
        var_name : str
            name of variable (e.g. "od550aer")
        **kwargs
            additional keyword args passed to ``Series.plot`` method
            
        Returns
        -------
        axes
            matplotlib.axes instance of plot
        
        Raises 
        ------
        KeyError
            if variable key does not exist in this dictionary
        ValueError
            if length of data array does not equal the length of the time array
        """
        s = self.to_timeseries(var_name)
        ax = s.plot(**kwargs)
        return ax
    
    def __getitem__(self, name):
        if not name in self.NAMES_STAT_COORDS:
            # no special treatment
            return super(StationData, self).__getitem__(name)
        if self._data_coords[name] is not None:
            return self._data_coords[name]
        stat_var = self.NAMES_STAT_COORDS[name]
        return self[stat_var]
    
    def __setitem__(self, name, value):
        if name in self.NAMES_STAT_COORDS:
            #special treatment
            if isinstance(value, (int, np.integer)):
                value = float(value)
            if not isinstance(value, (float, np.floating, 
                                      tuple, list, np.ndarray)):
                raise ValueError('Need floating point or list-like, got: {}'.format(value))
            self._data_coords[name] = value
        else:
            # no special treatment
            super(StationData, self).__setitem__(name, value)
            
    def __str__(self):
        s = super(StationData, self).__str__()
        s_data = ''
        for k, v in self._data_coords.items():
            if v is not None:
                if isinstance(v, list):
                    s_data += "\n{} (list, {} items)".format(k, len(v))
                    s_data += list_to_shortstr(v)
                elif isinstance(v, np.ndarray) and v.ndim==1:
                    s_data += "\n{} (array, {} items)".format(k, len(v))
                    s_data += list_to_shortstr(v)
                else:
                    s_data += "\n%s: %s" %(k,v)
        if s_data:
            s += '\nData coordinates\n.................'
            s += s_data
        return s
    
# =============================================================================
#     @property
#     def latitude(self):
#         """Single value, list or array of data latitude coordinates
#         
#         Note
#         ----
#         If not explicitely defined, the station latitude (:attr:`stat_lat`)
#         is used
#         """
#         if self._latitude is None:
#             return self.stat_lat
#         return self._latitude
#     
#     @latitude.setter
#     def latitude(self, value):
#         if not isinstance(value, (float, np.floating, tuple, list, np.ndarray)):
#             raise ValueError('Need floating point or list-like')
#         self._latitude = value
#         
#     @property
#     def longitude(self):
#         """Single value, list or array of data longitude coordinates
#         
#         Note
#         ----
#         If not explicitely defined, the station longitude (:attr:`stat_lon`)
#         is used
#         """
#         if self._longitude is None:
#             return self.stat_lon
#         return self._longitude
#     
#     @longitude.setter
#     def longitude(self, value):
#         if not isinstance(value, (float, np.floating, tuple, list, np.ndarray)):
#             raise ValueError('Need floating point or list-like')
#         self._longitude = value
#     
#     @property
#     def altitude(self):
#         """Single value, list or array of data altitude coordinates
#         
#         Note
#         ----
#         If not explicitely defined, the station altitude (:attr:`stat_alt`)
#         is used
#         """
#         if self._altitude is None:
#             return self.stat_alt
#         return self._altitude
#     
#     @altitude.setter
#     def altitude(self, value):
#         if not isinstance(value, (float, np.floating, tuple, list, np.ndarray)):
#             raise ValueError('Need floating point or list-like')
#         self._altitude = value
# =============================================================================
    
if __name__=="__main__":
    
    d = StationData()
    
    d.longitude = 42.
    print(d)
        
    
        
        

