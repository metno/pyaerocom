#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from pyaerocom.exceptions import CoordinateError, MetaDataError
from pyaerocom import logger
from pyaerocom._lowlevel_helpers import dict_to_str, list_to_shortstr, BrowseDict

class Station(BrowseDict):
    """Dict-like base class for station information
    
    Attributes
    ----------
    dataset_name : str
        name of underlying dataset
    station_name : str
        name of station (may also be list / array in derived classes, e.g. in
        for each datapoint in derived subclass see e.g. 
        :class:`ReadAeronetSdaV3`)
    stat_lat : float
        latitude of station
        
    """
    #: keys specifying default meta data keys.
    META_KEYS = ['station_name',
                 'PI',
                 'dataset_name']
    
    #: keys specifying the coordinates 
    COORD_KEYS = ['stat_lat',
                  'stat_lon',
                  'stat_alt']
    
    #: dictionary specifying maximumg allowed variation in m for numerical meta 
    #: parameters, that may be delivered for each time stamp individually 
    COORD_MAX_VAR = {'stat_lat'     : 10,
                     'stat_lon'     : 10,
                     'stat_alt'     : 10}
    
    
    def __init__(self, *args, **kwargs):
        # meta data (strings, lists or arrays)
        self.dataset_name = ''
        self.station_name = ''
        self.PI = ''
        
        # coordinate data (floats, lists or arrays)
        self.stat_lat = np.nan
        self.stat_lon = np.nan
        self.stat_alt = np.nan
        
        super(Station, self).__init__(*args, **kwargs)
        
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
        for key in self.COORD_KEYS:
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
            lat, dlat, dlon, dalt = (vals['stat_lat'],
                                     stds['stat_lat'],
                                     stds['stat_lon'],
                                     stds['stat_alt'])
            lat_len = 111e3 #approximate length of latitude degree in m
            if self.COORD_MAX_VAR['stat_lat'] < lat_len * dlat:
                raise CoordinateError("Variation in station latitude is "
                                      "exceeding upper limit of {} m".format(
                                      self.COORD_MAX_VAR['stat_lat']))
            elif self.COORD_MAX_VAR['stat_lon'] < (lat_len * 
                                                    np.cos(np.deg2rad(lat)) * 
                                                    dlon):
                raise CoordinateError("Variation in station longitude is "
                                      "exceeding upper limit of {} m".format(
                                      self.COORD_MAX_VAR['stat_lat']))
            elif self.COORD_MAX_VAR['stat_alt'] < dalt:
                raise CoordinateError("Variation in station altitude is "
                                      "exceeding upper limit of {} m".format(
                                      self.COORD_MAX_VAR['stat_lat']))
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
        for key in self.META_KEYS:
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
    
    def __str__(self):
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
    
    s = Station()
    print(s)
        
        
        

