#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from pyaerocom.timeseriesfiledata import TimeSeriesFileData
from pyaerocom.exceptions import CoordinateError, MetaDataError
from pyaerocom import logger

class StationData(TimeSeriesFileData):
    """Dict-like base class for results from station file imports (single files)
    
    .. seealso::
        
        Base class :class:`TimeSeriesFileData`
    
    Attributes
    ----------
    dtime : ndarray
        numpy array or list, containing time stamps of data
    station_name : str
        name of station (may also be replaced with list / array for each time
        stamp, see e.g. :class:`ReadAeronetSdaV3`)
    latitude : float
        latitude of station.
        
    """
    # keys specifying default meta data keys.
    META_KEYS = ['station_name',
                 'PI',
                 'dataset_name']
    
    # keys specifying the coordinates 
    COORD_KEYS = ['latitude',
                  'longitude',
                  'altitude']
    
    # dictionary specifying maximumg allowed variation in m for numerical meta 
    # parameters, that may be delivered for each time stamp individually 
    COORD_MAX_VAR = {'latitude'     : 10,
                     'longitude'    : 10,
                     'altitude'     : 10}
    
    
    def __init__(self, *args, **kwargs):
        super(StationData, self).__init__(*args, **kwargs)
        
        # meta data (strings, lists or arrays)
        self.station_name = ''
        self.PI = ''
        self.dataset_name = ''
        
        # coordinate data (floats, lists or arrays)
        self.latitude = np.nan
        self.longitude = np.nan
        self.altitude = np.nan
        
    
    def get_coords(self, force_single_value=True, quality_check=True):
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
            if force_single_value and not isinstance(val, float):
                if not any([isinstance(val, x) for x in [list, np.ndarray]]):
                    raise AttributeError("Invalid value encountered for coord "
                                         "{}, need float, list or ndarray, "
                                         "got {}".format(key, type(val)))
                val = np.mean(val)
                std = np.std(val)
                if std > 0:
                    _check_var = True
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
                    
if __name__=="__main__":
    
    d = StationData()
    print(d)
        
        
        

