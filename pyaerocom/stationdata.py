#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collection of station data classes

Currently:
    
    1. :class:`StationTimeseriesData`
    2. :class:`StationProfileData`
"""
import pandas as pd
import numpy as np
import abc
from pyaerocom.station import Station

class StationData(abc.ABC, Station):
    """TEMPLATE: Dict-like base class for single station data
    
    .. seealso::
        
        Base class :class:`Station`
        
    Note
    ----
    Implementations require specification of the key that should be used for
    indexing (e.g. dtime, or altitude z).
        
    Attributes
    ----------
    index : list
        list / array containing index values
    """
    def __init__(self, *args, **kwargs):
        super(StationData, self).__init__(*args, **kwargs)
        self.dtime = []
        self.z = []
    
    @abc.abstractproperty
    def index_key(self):
        pass
    
    @property
    def index(self):
        return self[self.index_key]
    
    def check_index(self):
        """Check if time dimension is valid"""
        if not len(self.index) > 0:
            raise ValueError("No data points available")
               
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
        self.check_index()
        num = len(self.index)
        cols = {}
        for k, v in self.items():
            if k is self.index_key:
                continue
            elif isinstance(v, list):
                v = np.asarray(v)
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
        return pd.DataFrame(data=self.data_columns, index=self.index)
    
    def to_timeseries(self, varname):
        """Get pandas.Series object for one of the data columns
        
        Parameters
        ----------
        varname : str
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
        if not varname in self:
            raise KeyError("Variable {} does not exist".format(varname))
        self.check_index()
        data = self[varname]
        if not len(data) == len(self.index):
            raise ValueError("Mismatch between length of data array for "
                             "variable {} (length: {}) and time array  "
                             "(length: {}).".format(varname, len(data), 
                               len(self.index)))
        return pd.Series(data, index=self.index)
    
    def plot_variable(self, varname, **kwargs):
        """Plot timeseries for variable
        
        Parameters
        ----------
        varname : str
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
        s = self.to_timeseries(varname)
        ax = s.plot(**kwargs)
        return ax
    
    def __len__(self):
        return len(self.index)
    
class StationTimeseriesData(StationData):
    @property
    def index_key(self):
        return 'dtime'

class StationProfileData(StationData):
    @property
    def index_key(self):
        return 'z'
    
if __name__=="__main__":
    
    d = StationTimeseriesData()

    print(d)
        
        
        

