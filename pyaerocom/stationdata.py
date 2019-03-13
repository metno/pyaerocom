#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import xarray as xray
from pyaerocom import VerticalProfile, logger, const

from pyaerocom.exceptions import (MetaDataError, VarNotAvailableError,
                                  DataExtractionError, DataDimensionError,
                                  UnitConversionError)
from pyaerocom._lowlevel_helpers import dict_to_str, list_to_shortstr, BrowseDict
from pyaerocom.metastandards import StationMetaData
from pyaerocom.helpers import (resample_timeseries, isnumeric, isrange,
                               resample_time_dataarray,
                               unit_conversion_fac)

class StationData(StationMetaData):
    """Dict-like base class for single station data
    
    ToDo: write more detailed introduction
    
    Attributes
    ----------
    dtime : list
        list / array containing time index values
    var_info : dict
        dictionary containing information about each variable
    data_err : dict
        dictionary that may be used to store uncertainty timeseries or data
        arrays associated with the different variable data.
    overlap : dict
        dictionary that may be filled to store overlapping timeseries data 
        associated with one variable. This is, for instance, used in 
        :func:`merge_vardata` to store overlapping data from another station.
    
    """
    #: List of keys that specify standard metadata attribute names. This 
    #: is used e.g. in :func:`get_meta`
    STANDARD_COORD_KEYS = const.STANDARD_COORD_NAMES
    
    #: maximum numerical distance between coordinates associated with this
    #: station
    _COORD_MAX_VAR = 0.1 #km
    STANDARD_META_KEYS = list(StationMetaData().keys())
    def __init__(self, **meta_info):

        self.dtime = []
    
        self.var_info = BrowseDict()
        
        self.station_coords = dict.fromkeys(self.STANDARD_COORD_KEYS)
        
        self.data_err = BrowseDict()        
        self.overlap = BrowseDict()
        super(StationData, self).__init__(**meta_info)
    
    @property
    def default_vert_grid(self):
        """AeroCom default grid for vertical regridding
        
        For details, see :attr:`DEFAULT_VERT_GRID_DEF` in :class:`Config`
        
        Returns
        -------
        ndarray
            numpy array specifying default coordinates
        """
        return const.make_default_vert_grid()
    
    def get_unit(self, var_name):
        """Get unit of variable data
        
        Parameters
        ----------
        var_name : str
            name of variable
        
        Returns
        -------
        str
            unit of variable
        
        Raises
        ------
        MetaDataError
            if unit cannot be accessed for variable
        """
        try: 
            return str(self.var_info[var_name]['unit'])
        except KeyError:
            raise MetaDataError('Failed to access unit for variable {}'.format(var_name))
            
    def convert_unit(self, var_name, to_unit):
        """Try to convert unit of data
        
        Requires that unit of input variable is available in :attr:`var_info` 
        
        Note
        ----
        BETA version
        
        Parameters
        ----------
        var_name : str
            name of variable
        to_unit : str
            new unit
        
        Raises
        ------
        MetaDataError
            if variable unit cannot be accessed
        UnitConversionError
            if conversion failed
        """
        unit = self.get_unit(var_name)
        
        try:
            conv_fac = unit_conversion_fac(unit, to_unit)
            data = self[var_name]
            data *= conv_fac
            self[var_name] = data
            self.var_info[var_name]['unit'] = to_unit
            const.logger.info('Successfully converted unit of variable {} in {} '
                              'from {} to {}'.format(var_name, self.station_name,
                                                     unit, to_unit))
        except Exception as e:
            raise UnitConversionError('Failed to convert unit of variable {} in {} '
                              'from {} to {}. Error: {}'.format(var_name, self.station_name,
                                                         unit, to_unit, repr(e)))
        
    def dist_other(self, other):
        """Distance to other station in km
        
        Parameters
        ----------
        other : StationData
            other data object
            
        Returns
        -------
        float
            distance between this and other station in km
        """
        from pyaerocom.geodesy import calc_distance
        
        cthis = self.get_station_coords()
        cother = other.get_station_coords()
        
        return calc_distance(cthis['latitude'], cthis['longitude'],
                             cother['latitude'], cother['longitude'],
                             cthis['altitude'], cother['altitude'])
        
    def same_coords(self, other, tol_km=None):
        """Compare station coordinates of other station with this station
        
        Paremeters
        ----------
        other : StationData
            other data object
        tol_km : float
            distance tolerance in km
            
        Returns
        -------
        bool
            if True, then the two object are located within the specified 
            tolerance range
        """
        if tol_km is None:
            tol_km = self._COORD_MAX_VAR
        return True if self.dist_other(other) < tol_km else False
    
    def get_station_coords(self, force_single_value=True, quality_check=True):
        """Return coordinates as dictionary
        
        This method uses the standard coordinate names defined in 
        :attr:`STANDARD_COORD_KEYS` (latitude, longitude and altitude) to get
        the station coordinates. For each of these parameters tt first looks 
        in :attr:`station_coords` if the parameter is defined (i.e. it is not 
        None) and if not it checks if this object has an attribute that has 
        this name and uses that one. 
        
        Parameters
        ----------
        force_single_value : bool
            if True and coordinate values are lists or arrays, then they are 
            collapsed to single value using mean
        quality_check : bool
            if True, and coordinate values are lists or arrays, then the 
            standarad deviation in the values is compared to the upper limits
            allowed in the local variation. 
        
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
            # prefer explicit if defined in station_coord dictionary (e.g. altitude
            # attribute in lidar data will be an array corresponding to profile
            # altitudes)
            val = self.station_coords[key]
            if val is not None:
                if not isnumeric(val):
                    raise MetaDataError('Station coordinate {} must be numeric. '
                                        'Got: {}'.format(key, val))
                vals[key] = val
                stds[key] = 0
            else:
                if not key in self or self[key] is None:
                    raise MetaDataError('{} information is not available in data'.format(key))
                val = self[key]
                std = 0
                # TODO: review the quality check and make shorter
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
            raise NotImplementedError('This feature does currently not work '
                                      'due to recent API changes')
# =============================================================================
#             logger.debug("Performing quality check for coordinates")
#             lat, dlat, dlon, dalt = (vals['latitude'],
#                                      stds['latitude'],
#                                      stds['longitude'],
#                                      stds['altitude'])
#             lat_len = 111e3 #approximate length of latitude degree in m
#             if self.COORD_MAX_VAR['latitude'] < lat_len * dlat:
#                 raise CoordinateError("Variation in station latitude is "
#                                       "exceeding upper limit of {} m".format(
#                                       self.COORD_MAX_VAR['latitude']))
#             elif self.COORD_MAX_VAR['longitude'] < (lat_len *
#                                                     np.cos(np.deg2rad(lat)) * 
#                                                     dlon):
#                 raise CoordinateError("Variation in station longitude is "
#                                       "exceeding upper limit of {} m".format(
#                                       self.COORD_MAX_VAR['latitude']))
#             elif self.COORD_MAX_VAR['altitude'] < dalt:
#                 raise CoordinateError("Variation in station altitude is "
#                                       "exceeding upper limit of {} m".format(
#                                       self.COORD_MAX_VAR['latitude']))
# =============================================================================
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
        meta.update(self.get_station_coords(force_single_value, quality_check))
        for key in self.STANDARD_META_KEYS:
            if key in self.STANDARD_COORD_KEYS: # this has been handled above
                continue
            if self[key] is None:
                logger.warning('No metadata available for key {}'.format(key))
                continue
            
            val = self[key]
            if force_single_value and isinstance(val, (list, tuple, np.ndarray)):
                if quality_check and not all([x == val[0] for x in val]):
                    logger.debug("Performing quality check for meta data")
                    raise MetaDataError("Inconsistencies in meta parameter {} "
                                        "between different time-stamps".format(
                                        key))
                val = val[0]
            meta[key] = val
    
        return meta
    
    def _append_meta_item(self, key, val):
        """Add a metadata item"""
        if not key in self or self[key] == None:
            self[key] = val
        else:
            if isinstance(self[key], str):
                if not isinstance(val, str):
                    raise ValueError('Cannot merge meta item {} due to type '
                                     'mismatch'.format(key))
                vals = [x.strip() for x in self[key].split(';')]
                vals_in = [x.strip() for x in val.split(';')]
                
                for _val in vals_in:
                    if not _val in vals:
                        self[key] = self[key] + '; {}'.format(_val)
            else:
                if isinstance(val, (list, np.ndarray)):
                    raise ValueError('Cannot append metadata value that is '
                                     'already a list or numpy array due to '
                                     'potential ambiguities')
                if isinstance(self[key], list):
                    if not val in self[key]:
                        self[key].append(val)
                else:
                    if not self[key] == val:
                        self[key] = [self[key], val]
        return self
                        
    def merge_meta_same_station(self, other, coord_tol_km=None, 
                                check_coords=True, inplace=True,
                                **add_meta_keys):
        """Merge meta information from other object
        
        Note
        ----
        Coordinate attributes (latitude, longitude and altitude) are not 
        copied as they are required to be the same in both stations. The
        latter can be checked and ensured using input argument ``check_coords``
        
        Parameters
        ----------
        other : StationData
            other data object
        coord_tol_km : float
            maximum distance in km between coordinates of input StationData 
            object and self. Only relevant if :attr:`check_coords` is True. If
            None, then :attr:`_COORD_MAX_VAR` is used which is defined in the
            class header. 
        check_coords : bool
            if True, the coordinates are compared and checked if they are lying
            within a certain distance to each other (cf. :attr:`coord_tol_km`).
        inplace : bool
            if True, the metadata from the other station is added to the 
            metadata of this station, else, a new station is returned with the
            merged attributes.
        **add_meta_keys
            additional non-standard metadata keys that are supposed to be
            considered for merging.

                    
        """
        if not other.station_name == self.station_name:
            raise ValueError('Can only merged metadata from same station')
        
        if not inplace:
            from copy import deepcopy
            obj = deepcopy(self)
        else:
            obj = self
            
        if check_coords:
            if coord_tol_km is None:
                coord_tol_km = self._COORD_MAX_VAR
            try:
                self.same_coords(other, coord_tol_km)
            except MetaDataError: # 
                pass
                    
        keys = self.STANDARD_META_KEYS
        keys.extend(add_meta_keys)
        # remove station name from key list to be merged
        
        
        
        for key in keys:
            if key == 'station_name':
                continue
            if key in self.STANDARD_COORD_KEYS:
                if self[key] is None and other[key] is not None:
                    self[key] = other[key]
            
            elif key in other and other[key] is not None:
                obj._append_meta_item(key, other[key])
        
        return obj
        
    def merge_varinfo(self, other, var_name):
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
            raise KeyError('No variable meta information available for {}'
                           .format(var_name))
            
        info_this = self.var_info[var_name]
        info_other = other.var_info[var_name]
        for key, val in info_other.items():
            if not key in info_this or info_this[key] == None:
                info_this[key] = val
            else:
                if isinstance(info_this[key], str):
                    if not isinstance(val, str):
                        raise ValueError('Cannot merge meta item {} due to type '
                                         'mismatch'.format(key))
                    vals = [x.strip() for x in info_this[key].split(';')]
                    vals_in = [x.strip() for x in val.split(';')]
                    
                    for _val in vals_in:
                        if not _val in vals:
                            info_this[key] = info_this[key] + ';{}'.format(_val)
                else:
                    if isinstance(val, (list, np.ndarray)):
                        if len(val) == 0:
                            continue
                        elif type(info_this[key]) == type(val):
                            if info_this[key] == val:
                                continue
                            info_this[key] = [info_this[key], val]
                        raise ValueError('Cannot append metadata value that is '
                                         'already a list or numpy array due to '
                                         'potential ambiguities')
                    if isinstance(info_this[key], list):
                        if not val in info_this[key]:
                            info_this[key].append(val)
                    else:
                        if not info_this[key] == val:
                            info_this[key] = [info_this[key], val]
        return self
# =============================================================================
#         for k, v in info_other.items():
#             if not k in info_this:
#                 info_this[k] = v
#             else:
#                 if not isinstance(info_this[k], list):
#                     info_this[k] = [info_this[k]]
#                     
#                 info_this[k].append(v)
# =============================================================================
        
    def check_if_3d(self, var_name):
        """Checks if altitude data is available in this object"""
        if 'altitude' in self: 
            val = self['altitude']
            if isnumeric(val): # is numerical value
                return False
            # unique altitude values
            uvals = np.unique(val)
            if len(uvals) == 1: # only one value in altitude array (NOT 3D)
                return False
            elif len(uvals[~np.isnan(uvals)]) == 1: # only 2 unique values in altitude array but one is NaN
                return False
            return True
        return False
        
    def _merge_vardata_3d(self, other, var_name):
        """Merge 3D variable data (for details see :func:`merge_vardata`)"""
        raise NotImplementedError
        s0 = self[var_name]
        s1 = other[var_name]
        info = other.var_info[var_name]
        removed = None
        if info['overlap']:
            raise NotImplementedError('Coming soon...')
        
        if len(s1) > 0: #there is data
            overlap = s0.index.intersection(s1.index)
            if len(overlap) > 0:
                removed = s1[overlap]
                s1 = s1.drop(index=overlap, inplace=True)
            
            #compute merged time series
            s0 = pd.concat([s0, s1], verify_integrity=True)
            
            # sort the concatenated series based on timestamps
            s0.sort_index(inplace=True)
            self.merge_varinfo(other, var_name)
        
        # assign merged time series (overwrites previous one)
        self[var_name] = s0
        
        if removed is not None:
            if var_name in self.overlap:
                self.overlap[var_name] = pd.concat([self.overlap[var_name], 
                                                   removed])
                self.overlap[var_name].sort_index(inplace=True)
            else:
                self.overlap[var_name] = removed
                
        return self
    
    def _merge_vardata_2d(self, other, var_name):
        """Merge 2D variable data (for details see :func:`merge_vardata`)"""
        s0 = self[var_name].dropna()
        s1 = other[var_name].dropna()
        info = other.var_info[var_name]
        removed = None
        if info['overlap']:
            raise NotImplementedError('Coming soon...')
        
        if len(s1) > 0: #there is data
            overlap = s0.index.intersection(s1.index)
            if len(overlap) > 0:
                removed = s1[overlap]
                s1 = s1.drop(index=overlap, inplace=True)
            #compute merged time series
            s0 = pd.concat([s0, s1], verify_integrity=True)
            
            # sort the concatenated series based on timestamps
            s0.sort_index(inplace=True)
            self.merge_varinfo(other, var_name)
        
        # assign merged time series (overwrites previous one)
        self[var_name] = s0
        self.dtime = s0.index.values
        
        if removed is not None:
            if var_name in self.overlap:
                self.overlap[var_name] = pd.concat([self.overlap[var_name], 
                                                   removed])
                self.overlap[var_name].sort_index(inplace=True)
            else:
                self.overlap[var_name] = removed
                
        return self
    
    def merge_vardata(self, other, var_name):
        """Merge variable data from other object into this object
        
        Note
        ----
        This merges also the information about this variable in the dict
        :attr:`var_info`. It is required, that variable meta-info is 
        specified in both StationData objects.
        
        Note
        ----
        This method removes NaN's from the existing time series in the data
        objects. In order to fill up the time-series with NaNs again after 
        merging, call :func:`insert_nans_timeseries`
        
        Parameters
        ----------
        other : StationData
            other data object 
        var_name : str
            variable name for which info is to be merged (needs to be both
            available in this object and the provided other object)
            
        Returns
        -------
        StationData
            this object
        """
        if not var_name in self:
            raise VarNotAvailableError('StationData object does not contain '
                                       'data for variable {}'.format(var_name))
        elif not var_name in other:
            raise VarNotAvailableError('Input StationData object does not '
                                       'contain data for variable {}'.format(var_name))
        elif not isinstance(self[var_name], pd.Series):
            raise ValueError('Data needs to be of type pandas.Series')
        elif not isinstance(other[var_name], pd.Series):
            raise ValueError('Data needs to be of type pandas.Series')
        elif not var_name in self.var_info:
            raise MetaDataError('For merging of {} data, variable specific meta '
                                'data needs to be available in var_info dict '
                                .format(var_name))
        elif not var_name in other.var_info:
            raise MetaDataError('For merging of {} data, variable specific meta '
                                'data needs to be available in var_info dict '
                                .format(var_name))
            
        if self.check_if_3d(var_name):
            raise NotImplementedError
            #return self._merge_vardata_3d(other, var_name)
        else:
            return self._merge_vardata_2d(other, var_name)
         
    def merge_other(self, other, var_name, **add_meta_keys):
        """Merge other station data object
        
        Todo
        ----
        Should be independent of variable, i.e. it should be able to merge all
        data that is in the other object into this, even if this object does
        not contain that variable yet.
        
        Parameters
        ----------
        other : StationData
            other data object 
        var_name : str
            variable name for which info is to be merged (needs to be both
            available in this object and the provided other object)
            
        Returns
        -------
        StationData
            this object that has merged the other station
        """
        self.merge_meta_same_station(other, **add_meta_keys)
        self.merge_vardata(other, var_name)
        return self
        
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
    
    def get_var_ts_type(self, var_name):
        """Get ts_type for a certain variable
        
        Parameters
        ----------
        var_name : str
            data variable name for which the ts_type is supposed to be
            retrieved
        
        Returns
        -------
        str
            the corresponding data time resolution
        
        Raises
        ------
        MetaDataError
            if no metadata is available for this variable (e.g. if ``var_name``
            cannot be found in :attr:`var_info`) or if the 
        """
        if not var_name in self.var_info:
            raise MetaDataError('No variable specific metadata available '
                                'for {}'.format(var_name))
        
        if 'ts_type' in self.var_info[var_name]:
            tp = self.var_info[var_name]['ts_type']
        else:
            tp = self.ts_type
        if tp is None:
            raise MetaDataError('ts_type is not defined...')
        elif not tp in const.GRID_IO.TS_TYPES:
            raise MetaDataError('Invalid ts_type {}: need AEROCOM default {}'
                                .format(tp, const.GRID_IO.TS_TYPES))
        return tp
       
    def interpolate_timeseries(self, var_name, freq, min_coverage_interp=0.3,
                               resample_how='mean', inplace=False):
        """Interpolate one variable timeseries to a certain frequency
        
        ToDo: complete docstring
        """
        new = self.to_timeseries(var_name, freq=freq, 
                                  resample_how='mean')
        coverage = 1 - new.isnull().sum() / len(new)
        if coverage < min_coverage_interp:
            from pyaerocom.exceptions import DataCoverageError
            raise DataCoverageError('{} data of station {} ({}) in '
                                    'time interval {} - {} contains '
                                    'too many invalid measurements '
                                    'for interpolation.'
                                    .format(var_name,
                                            self.station_name,
                                            self.data_id,
                                            self.dtime[0],
                                            self.dtime[-1]))
        new = new.interpolate().dropna()
        if inplace:
            from pyaerocom.helpers import PANDAS_FREQ_TO_TS_TYPE
            ts_type = PANDAS_FREQ_TO_TS_TYPE[new.index.freqstr]
            self[var_name] = new
            
            self.var_info[var_name]['ts_type'] = ts_type        
            if len(self.var_info) > 1:     
                self.ts_type = None
            else:
                self.ts_type = ts_type
        return new
    
    def resample_timeseries(self, var_name, ts_type, how='mean',
                            inplace=False, min_num_obs=None):
        """Resample one of the time-series in this object
        
        Parameters
        ----------
        var_name : str
            name of data variable
        ts_type : str
            new frequency string (can be pyaerocom ts_type or valid pandas
            frequency string)
        how : str
            how should the resampled data be averaged (e.g. mean, median)
        inplace : bool
            if True, then the current data object stored in self, will be 
            overwritten with the resampled time-series
        min_num_obs : :obj:`int`, optional
            minimum number of observations required per period (when downsampling).
            E.g. if input is in daily resolution and freq is monthly and 
            min_num_obs is 10, then all months that have less than 10 days of data
            are set to nan.
            
        Returns
        -------
        pandas.Series
            resampled time-series
        """
        if not var_name in self:
            raise KeyError("Variable {} does not exist".format(var_name))
        data = self[var_name]
    
        if not isinstance(data, (pd.Series, xray.DataArray)):
            try:
                data = self.to_timeseries(var_name, inplace=inplace)
            except Exception as e:
                raise ValueError('{} data must be stored as pandas Series '
                                 'instance or as xarray.DataArray. Failed to '
                                 'convert to pandas Series.'
                                 'Error: {}'.format(repr(e)))
        
        if isinstance(data, pd.Series):
            new = resample_timeseries(data, freq=ts_type, how=how,
                                      min_num_obs=min_num_obs)
        elif isinstance(data, xray.DataArray):
            
            new = resample_time_dataarray(data, freq=ts_type, how=how, 
                                          min_num_obs=min_num_obs)
            
        
        if inplace:
            self[var_name] = new
            self.var_info[var_name]['ts_type'] = ts_type        
            if len(self.var_info) > 1:     
                self.ts_type = None
                self.dtime = None
            else:
                self.ts_type = ts_type
                self.dtime = new.index.values
        return new
    
    def insert_nans_timeseries(self, var_name):
        """Fill up missing values with NaNs in an existing time series
        
        Note
        ----
        This method does a resample of the data onto a regular grid. Thus, if
        the input ``ts_type`` is different from the actual current ``ts_type`` 
        of the data, this method will not only insert NaNs but at the same.
        
        Parameters
        ---------
        var_name : str
            variable name
        inplace : bool
            if True, the actual data in this object will be overwritten with 
            the new data that contains NaNs
        
        Returns
        -------
        StationData
            the modified station data object
        
        """
        ts_type = self.get_var_ts_type(var_name)
        
        self.resample_timeseries(var_name, ts_type, inplace=True)
        
        return self

    
    def _to_ts_helper(self, var_name):
        """Convert data internally to pandas.Series if it is not stored as such
        
        Parameters
        ----------
        var_name : str
            variable name of data
        
        Returns
        -------
        pandas.Series
            data as timeseries
        """
        data = self[var_name]
        if not data.ndim == 1:
            raise NotImplementedError('Multi-dimensional data columns '
                                      'cannot be converted to time-series')
        self.check_dtime()
        if not len(data) == len(self.dtime):
            raise ValueError("Mismatch between length of data array for "
                             "variable {} (length: {}) and time array  "
                             "(length: {}).".format(var_name, len(data), 
                               len(self.dtime)))    
        self[var_name] = s = pd.Series(data, index=self.dtime)
        return s
    
    def select_altitude(self, var_name, altitudes):
        
        data = self[var_name]
        
        if not isrange(altitudes):
            raise NotImplementedError('So far only a range (low, high) is '
                                      'supported for altitude extraction.')
            
        if isinstance(data, xray.DataArray):
            if not sorted(data.dims) == ['altitude', 'time']:
                raise NotImplementedError('Can only handle dataarrays that '
                                          'contain 2 dimensions altitude and '
                                          'time')
            if isrange(altitudes):
                                
                return data.sel(altitude=slice(altitudes[0], 
                                               altitudes[1]))
            
            raise DataExtractionError('Cannot intepret input for '
                                          'altitude...')
        elif isinstance(data, pd.Series) and isinstance(data.index, pd.DatetimeIndex):
            if not len(data.index.unique()) == 1:
                raise DataDimensionError('Failed to interpret data dimensions')
            elif not 'altitude' in self:
                raise ValueError('Missing altitude information')
            elif not len(self.altitude) == len(data):
                raise DataDimensionError('Altitude data and {} data have '
                                         'different lengths'.format(var_name))
            
            alts = self['altitude']
            mask = np.logical_and(alts>=altitudes[0],
                                  alts<=altitudes[1])
            return data[mask]
            
                    
        
        raise DataExtractionError('Cannot extract altitudes: type of '
                                  '{} ({}) is not supported'
                                  .format(var_name, type(data)))
        
        
    def to_timeseries(self, var_name, freq=None, resample_how='mean', 
                      **kwargs):
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
        **kwargs
            optional keyword args passed to :func:`resample_timeseries`
            
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
        data = self[var_name]
        alt_info = None
        # check if altitude subset is requested and process if applicable
        if 'altitude' in kwargs:
            alt_info =  kwargs.pop('altitude')
            data = self.select_altitude(var_name, alt_info)
        else:
            data = self[var_name]
            
        if isinstance(data, xray.DataArray):
            if not 'time' in data.dims:
                raise NotImplementedError('Can only handle dataarrays that '
                                          'contain time dimension')
            if 'altitude' in data.dims: # collapsing of altitude dimension has not been done
                data = data.mean('altitude')
            if not data.ndim == 1:
                raise Exception('please debug')
            data = data.to_series()
        
        if not isinstance(data, pd.Series):
            data = self._to_ts_helper(var_name)

        if freq is not None:
            data = resample_timeseries(data, freq, how=resample_how,
                                           **kwargs)

        return data
    
    def plot_timeseries(self, var_name, freq=None, resample_how='mean', 
                        add_overlaps=False, legend=True, tit=None, 
                        **kwargs):
        """Plot timeseries for variable
        
        Note
        ----
        If you set input arg ``add_overlaps = True`` the overlapping timeseries
        data - if it exists - will be plotted on top of the actual timeseries
        using red colour and dashed line. As the overlapping data may be 
        identical with the actual data, you might want to increase the line 
        width of the actual timeseries using an additional input argumend 
        ``lw=4``, or similar.
        
        Parameters
        ----------
        var_name : str
            name of variable (e.g. "od550aer")
        freq : :obj:`str`, optional
            sampling resolution of data (can be pandas freq. string, or 
            pyaerocom ts_type).
        resample_how : :obj:`str`, optional
            choose from mean or median (only relevant if input parameter freq 
            is provided, i.e. if resampling is applied)
        add_overlaps : bool
            if True and if overlapping data exists for this variable, it will 
            be added to the plot.
        tit : :obj:`str`, optional
            title of plot, if None, default title is used
        **kwargs
            additional keyword args passed to matplotlib ``plot`` method
            
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
        import matplotlib.pyplot as plt
        if 'label' in kwargs:
            lbl = kwargs.pop('label')
        else:
            lbl = var_name
            if freq is not None:
                lbl += ' ({} {})'.format(freq, resample_how)
            else:
                try:
                    ts_type = self.get_var_ts_type(var_name)
                    lbl += ' ({})'.format(ts_type)
                except:
                    pass
        if not 'ax' in kwargs:
            if 'figsize' in kwargs:
                fs = kwargs.pop('figsize')
            else:
                fs = (16, 8)
            _, ax = plt.subplots(1, 1, figsize=fs)
        else: 
            ax = kwargs.pop('ax')
            # keep existing title if it exists
            _tit = ax.get_title()
            if not _tit == '':
                tit = _tit
        
        if tit is None:
            try:
                tit = self.get_meta(force_single_value=True, 
                                      quality_check=False)['station_name']    
            except:
                tit = 'Failed to retrieve station_name'
        s = self.to_timeseries(var_name, freq, resample_how)
        
        ax.plot(s, label=lbl, **kwargs)
        if add_overlaps:
            so = self.overlap[var_name]
            try:
                so = resample_timeseries(so, freq, how=resample_how)
            except:
                pass
            if var_name in self.overlap:
                ax.plot(so, '--', lw=1, c='r', 
                        label='{} (overlap)'.format(var_name)) 
            else: 
                tit += ' (No overlapping data found)'
                
        ylabel = var_name
        try:
            if 'unit' in self.var_info[var_name]:
                u = self.var_info[var_name]['unit']
                if u is not None and not u in [1, '1']:
                    ylabel += ' [{}]'.format(u)
        except:
            logger.warning('Failed to access unit information for variable {}'
                           .format(var_name))
        ax.set_ylabel(ylabel)
        ax.set_title(tit)
        if legend:
            ax.legend()
        return ax
            
    def __str__(self):
        """String representation"""
        head = "Pyaerocom {}".format(type(self).__name__)
        s = "\n{}\n{}".format(head, len(head)*"-")
        arrays = ''
        series = ''
    
        for k, v in self.items():
            if k[0] == '_':
                continue
            if isinstance(v, dict) and v:
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
    
    s = StationData(station_name='Bla', revision_date='20, 21')
    s2 = StationData(station_name='Bla', revision_date='21, 22, 23',
                     latitude=30, longitude=10, altitude=400)
    
    print(s)
    s.merge_meta_same_station(s2)
    print(s2)
    print(s)
    