#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pyaerocom import VerticalProfile, logger
from pyaerocom.exceptions import CoordinateError, MetaDataError
from pyaerocom._lowlevel_helpers import dict_to_str, list_to_shortstr, BrowseDict
from pyaerocom.metastandards import StationMetaData

class StationData(StationMetaData):
    """Dict-like base class for single station data
        
    Attributes
    ----------
    dtime : list
        list / array containing index values
    var_info :
    
    """
    #: List of keys that specify standard metadata attribute names. This 
    #: is used e.g. in :func:`get_meta`
    
    
    STANDARD_COORD_KEYS = ['latitude', 
                           'longitude',
                           'altitude']    
    #: dictionary specifying maximum allowed variation in m for numerical meta 
    #: parameters, that may be provided for each time stamp individually 
    COORD_MAX_VAR = {'latitude'     : 10,
                     'longitude'    : 10,
                     'altitude'     : 10}
    
    def __init__(self, **meta_info):

        
        
        self.dtime = []
        
        # dictionary that should be filled with available meta-information 
        # for each data column appended to this object
        self.var_info = BrowseDict()
        super(StationData, self).__init__(**meta_info)
        #super(StationData, self).__init__(*args, **kwargs)
     
    @property
    def STANDARD_META_KEYS(self):
        """List of standard keys for metadata"""
        return list(StationMetaData().keys())
    
    def get_station_coords(self, force_single_value=True, quality_check=True):
        """Return coordinates as dictionary
        
        Parameters
        ----------
        force_single_value : bool
            if True and coordinate values are lists or arrays, then they are 
            collapsed to single value using mean
        quality_check : bool
            if True, and coordinate values are lists or arrays, then the 
            standarad deviation in the values is compared to the upper limits
            allowed in the local variation. The upper limits are specified
            in attr. ``COORD_MAX_VAR``. 
        
        Returns
        -------
        dict
            dictionary containing the retrieved coordinates
            
        Raises
        ------
        AttributeError
            if one of the coordinate values is invalid
        CoordinateError
            if local variation in either of the three spatial coordinates is
            found too large
        """
        _check_var = False
        vals , stds = {}, {}
        for key in self.STANDARD_COORD_KEYS:
            if not key in self:
                raise MetaDataError('{} information is not available in data'.format(key))
            val = self[key]
            std = 0.0
            if force_single_value and not isinstance(val, (float, np.floating)):
                if isinstance(val, (int, np.integer)):
                    val = np.float64(val)
                elif isinstance(val, (list, np.ndarray)):
                    val = np.mean(val)
                    std = np.std(val)
                    if std > 0:
                        _check_var = True
                else:
                    raise AttributeError("Invalid value encountered for coord "
                                         "{}, need float, int, list or ndarray, "
                                         "got {}".format(key, type(val)))
            vals[key] = val
            stds[key] = std
        if _check_var:
            logger.debug("Performing quality check for coordinates")
            lat, dlat, dlon, dalt = (vals['latitude'],
                                     stds['latitude'],
                                     stds['longitude'],
                                     stds['altitude'])
            lat_len = 111e3 #approximate length of latitude degree in m
            if self.COORD_MAX_VAR['latitude'] < lat_len * dlat:
                raise CoordinateError("Variation in station latitude is "
                                      "exceeding upper limit of {} m".format(
                                      self.COORD_MAX_VAR['latitude']))
            elif self.COORD_MAX_VAR['longitude'] < (lat_len *
                                                    np.cos(np.deg2rad(lat)) * 
                                                    dlon):
                raise CoordinateError("Variation in station longitude is "
                                      "exceeding upper limit of {} m".format(
                                      self.COORD_MAX_VAR['latitude']))
            elif self.COORD_MAX_VAR['altitude'] < dalt:
                raise CoordinateError("Variation in station altitude is "
                                      "exceeding upper limit of {} m".format(
                                      self.COORD_MAX_VAR['latitude']))
        return vals
    
    def get_meta(self, force_single_value=True, quality_check=True):
        """Return meta-data as dictionary
        
        Parameters
        ----------
        force_single_value : bool
            if True, then each meta value that is list or array,is converted 
            to a single value. 
        quality_check : bool
            if True, and coordinate values are lists or arrays, then the 
            standarad deviation in the values is compared to the upper limits
            allowed in the local variation. The upper limits are specified
            in attr. ``COORD_MAX_VAR``. 
        
        Returns
        -------
        dict
            dictionary containing the retrieved meta-data
            
        Raises
        ------
        AttributeError
            if one of the meta entries is invalid
        MetaDataError
            in case of consistencies in meta data between individual time-stamps
        """
        meta = {}
        for key in self.STANDARD_META_KEYS:
            if self[key] is None:
                logger.warn('No metadata available for key {}'.format(key))
                continue
            
            val = self[key]
            if force_single_value and not isinstance(val, str):
                if not any([isinstance(val, x) for x in [list, np.ndarray]]):
                    raise AttributeError("Invalid value encountered for meta "
                                         "key {}, need str, list or ndarray, "
                                         "got {}".format(key, type(val)))
                if quality_check and not all([x == val[0] for x in val]):
                    logger.debug("Performing quality check for meta data")
                    raise MetaDataError("Inconsistencies in meta parameter {} "
                                        "between different time-stamps".format(
                                        key))
                val = val[0]
            meta[key] = val
        
        return meta
    
    def merge_meta(self, other, maxdist_km=1):
        """Merge meta information from other object
        
        Parameters
        ----------
        other : StationData
            other data object
        """
        ignore_keys = ['_coords', 'dtime', 'latitude', 'longitude',
                       'altitude','var_info']
        ignore_keys.extend(self.var_info.keys())
        
        from pyaerocom.mathutils import is_within_radius_km
        if self.longitude is not None:
            if not is_within_radius_km(self.longitude, self.latitude, 
                                       self.altitude, other.longitude, 
                                       other.latitude, other.altitude,
                                       maxdist_km):
                raise CoordinateError('Stations are not located at same '
                                      'coordinate')
        for k, v in other.items():
            if k in ignore_keys:
                continue
            
            if not k in self:
                self[k] = [v]
            else:
                if not isinstance(self[k], list):
                    self[k] = self[k]
                self[k].append(v)
                
        
    def merge_var_info(self, other, var_name):
        """Merge variable specific meta information from other object
        
        Parameters
        ----------
        other : StationData
            other data object 
        var_name : str
            variable name for which info is to be merged (needs to be both
            available in this object and the provided other object)
        """
        if not var_name in self.var_info:
            raise KeyError('No variable information available for {}'.format(var_name))
        info_this = self.var_info[var_name]
    
        info_other = other.var_info[var_name]
        for k, v in info_other.items():
            if not k in info_this:
                info_this[k] = v
            else:
                if not isinstance(info_this[k], list):
                    info_this[k] = [info_this[k]]
                    
                info_this[k].append(v)
        
    def get_data_columns(self):
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
        #self.check_dtime()
        #num = len(self.dtime)
        cols = {}
        for var_name in self.var_info:
            vals = self[var_name]
            if isinstance(vals, list):
                vals = np.asarray(vals)
            elif isinstance(vals, pd.Series):
                vals = vals.values
            elif isinstance(vals, VerticalProfile):
                raise NotImplementedError("This feature is not yet supported "
                                          "for data objects that contain also "
                                          "profile data")
            cols[var_name] = vals
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
        return pd.DataFrame(data=self.get_data_columns(), index=self.dtime)
    
    def to_timeseries(self, var_name, freq=None, resample_how='mean'):
        """Get pandas.Series object for one of the data columns
        
        Parameters
        ----------
        var_name : str
            name of variable (e.g. "od550aer")
        freq : str
            new temporal resolution (can be pandas freq. string, or pyaerocom
            ts_type)
        resample_how : str
            choose from mean or median (only relevant if input parameter freq 
            is provided, i.e. if resampling is applied)
            
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
        if isinstance(data, pd.Series):
            logger.info('Data is already instance of pandas.Series')
            return data
        if not data.ndim == 1:
            raise NotImplementedError('Multi-dimensional data columns cannot '
                                      'be converted to time-series')
        if not len(data) == len(self.dtime):
            raise ValueError("Mismatch between length of data array for "
                             "variable {} (length: {}) and time array  "
                             "(length: {}).".format(var_name, len(data), 
                               len(self.dtime)))
        s = pd.Series(data, index=self.dtime)
        if freq is not None:
            from pyaerocom.helpers import resample_timeseries
            s = resample_timeseries(s, freq, resample_how)
        return s
    
    def plot_variable(self, var_name, freq=None, resample_how='mean', 
                      **kwargs):
        """Plot timeseries for variable
        
        Parameters
        ----------
        var_name : str
            name of variable (e.g. "od550aer")
        freq : str
            new temporal resolution (can be pandas freq. string, or pyaerocom
            ts_type)
        resample_how : str
            choose from mean or median (only relevant if input parameter freq 
            is provided, i.e. if resampling is applied)
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
        s = self.to_timeseries(var_name, freq, resample_how)
        ax = s.plot(**kwargs)
        return ax
            
# =============================================================================
#     def __getitem__(self, name):
#         if name in self._coords:
#             # no special treatment
#             return self._coords[name]
#         return self[name]
#     
#     def __setitem__(self, name, value):
#         if name in self._coords:
#             #special treatment
#             if isinstance(value, (int, np.integer)):
#                 value = float(value)
#             if not isinstance(value, (float, np.floating, 
#                                       tuple, list, np.ndarray)):
#                 raise ValueError('Need floating point or list-like, got: {}'
#                                  .format(value))
#             self._coords[name] = value
#         else:
#             # no special treatment
#             super(StationData, self).__setitem__(name, value)
# =============================================================================
            
    def __str__(self):
        """String representation"""
        head = "Pyaerocom {}".format(type(self).__name__)
        s = "\n{}\n{}".format(head, len(head)*"-")
        arrays = ''
        series = ''
    
        for k, v in self.items():
            if k[0] == '_':
                continue
            
            if isinstance(v, dict):
                s += "\n{} ({})".format(k, repr(v))
                s = dict_to_str(v, s)
            elif isinstance(v, list):
                s += "\n{} (list, {} items)".format(k, len(v))
                s += list_to_shortstr(v)
            elif isinstance(v, np.ndarray) and v.ndim==1:
                arrays += "\n{} (array, {} items)".format(k, len(v))
                arrays += list_to_shortstr(v)
            elif isinstance(v, np.ndarray):
                arrays += "\n{} (array, shape {})".format(k, v.shape)
                arrays += "\n{}".format(v)
            elif isinstance(v, pd.Series):
                series += "\n{} (Series, {} items)".format(k, len(v))
            else:
                s += "\n%s: %s" %(k,v)
        if arrays:
            s += '\n\nData arrays\n.................'
            s += arrays
        if series:
            s += '\nPandas Series\n.................'
            s += series
    
        return s
    
if __name__=="__main__":
    
    s = StationData()
    
    print(s)