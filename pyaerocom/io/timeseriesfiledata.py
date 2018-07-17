#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from pyaerocom.utils import dict_to_str, list_to_shortstr, BrowseDict

class TimeSeriesFileData(BrowseDict):
    """Low level dict-like class for results from timeseries file reads
    
    The idea is to provide a common interface for storage of time-series data
    from file I/O operations. The interface is simply a dictionary and only 
    contains little logic.
    
    Attributes
    ----------
    dtime : ndarray
        numpy array or list, containing time stamps of data
        
    """
    def __init__(self, *args, **kwargs):
        super(TimeSeriesFileData, self).__init__(*args, **kwargs)
        self.dtime = []
    
    @property
    def num_timestamps(self):
        """Total number of timestamps in this object"""
        return len(self.dtime)        
    
    def check_time(self):
        """Check if time dimension is valid"""
        if not len(self.dtime) > 0:
            raise ValueError("No time stamps available")
       
    def len_flat(self, num_of_vars):
        """The total number of observations  considering input variables
        
        The total number of observations *C* is determined from the number of 
        available time-stamps *T* and the number of considered variables *V*, 
        as *C=TxV*.
        
        Parameters
        ----------
        num_of_vars
            number of variables to be considered
            
        Returns
        -------
        int
        """
        return len(self.dtime) * num_of_vars
        
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
        self.check_time()
        num = len(self.dtime)
        cols = {}
        for k, v in self.items():
            if isinstance(v, list):
                v = np.asarray(v)
            if isinstance(v, np.ndarray) and len(v) == num:
                cols[k] = v
        if not cols:
            raise AttributeError("No datacolumns could be found that match the "
                                 "number of available time stamps")
        return cols
                
    def to_dataframe(self):
        """Convert this object to pandas dataframe
        
        Find all key/value pairs that contain observation data (i.e. values
        must be list or array and must have the same length as attribute 
        ``time``)
        
        """
        cols = self.data_columns
        return pd.DataFrame(data=cols, index=self.dtime)
        
        
    
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
        self.check_time()
        data = self[varname]
        if not len(data) == len(self.dtime):
            raise ValueError("Mismatch between length of data array for "
                             "variable {} (length: {}) and time array  "
                             "(length: {}).".format(varname, len(data), 
                               len(self.dtime)))
        return pd.Series(data, index=self.dtime)
    
        
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
            elif isinstance(v, np.ndarray):
                arrays += "\n{} (array, {} items)".format(k, len(v))
                arrays += list_to_shortstr(v)
            else:
                s += "\n%s: %s" %(k,v)
        s += arrays
        return s
    
if __name__=="__main__":
    
    d = TimeSeriesFileData()
    print(d)
        
        
        

