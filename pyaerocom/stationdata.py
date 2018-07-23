#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pyaerocom.station import Station
from pyaerocom import VerticalProfile

class StationData(Station):
    """Dict-like base class for single station data
    
    .. seealso::
        
        Base class :class:`Station`
        
    Attributes
    ----------
    dtime : list
        list / array containing index values
    
    """
    def __init__(self, *args, **kwargs):
        super(StationData, self).__init__(*args, **kwargs)
        self.dtime = []
    
    def check_dtime(self):
        """Checks if dtime attribute is array or list"""
        if not any([isinstance(self.dtime, x) for x in [list, np.ndarray]]):
            raise TypeError("dtime attribute is not iterable: {}".format(self.dtime))
        elif not len(self.dtime) > 0:
            raise AttributeError("No timestamps available")
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
        if not len(data) == len(self.index):
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
    
if __name__=="__main__":
    
    d = StationData()

    print(d)
        
        
        

