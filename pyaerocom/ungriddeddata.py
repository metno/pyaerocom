#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from copy import deepcopy
from collections import OrderedDict as od
import pandas as pd
from math import isclose
from pyaerocom import logger
from pyaerocom.exceptions import DataExtractionError
from pyaerocom.utils import dict_to_str, list_to_shortstr

class UngriddedData(object):
    """Class representing ungridded data
    
    The data is organised in a 2-dimensional numpy array where the first index 
    (rows) axis corresponds to individual measurements (i.e. one timestamp of 
    one variable) and along the second dimension (containing 11 columns) the 
    actual values are stored (in column 6) along with additional information,
    such as metadata index (can be used as key in :attr:`metadata` to access
    additional information related to this measurement), timestamp, latitude, 
    longitude, altitude of instrument, variable index and, in case of 3D 
    data (e.g. LIDAR profiles), also the altitude corresponding to the data 
    value.
        
    Note
    ----
    
    That said, let's look at two examples.
    
    **Example 1**: Suppose you load 3 variables from 5 files, each of which 
    contains 30 timestamps. This corresponds to a total of 3*5*30=450 data 
    points and hence, the shape of the underlying numpy array will be 450x11.
    
    **Example 2**: 3 variables, 5 files, 30 timestamps, but each variable 
    is height resolved, containing 100 altitudes => 3*5*30*100=4500 data points, 
    thus, the final shape will be 4500x11.
    
    Attributes
    ----------
    _data : ndarray
        (private) numpy array of dtype np.float64 initially of shape (10000,8)
        data point array
    metadata : dict
        dictionary containing meta information about the data. Keys are 
        floating point numbers corresponding to each station, values are 
        corresponding dictionaries containing station information.
    mata_idx : dict
        dictionary containing index mapping for each station and variable. Keys
        correspond to metadata key (float -> station, see :attr:`metadata`) and 
        variables are dictionaries containing keys specifying variable name and 
        values are arrays or lists, specifying indices (rows) of these 
        station / variable information in :attr:`_data`.
    """
    __version__ = '0.1.0'
    _METADATAKEYINDEX = 0
    _TIMEINDEX = 1
    _LATINDEX = 2
    _LONINDEX = 3
    _ALTITUDEINDEX = 4 # altitude of measurement device
    _VARINDEX = 5
    _DATAINDEX = 6
    _DATAHEIGHTINDEX = 7

    _COLNO = 11
    _ROWNO = 10000
    _CHUNKSIZE = 1000
    
    # The following number denotes the kept precision after the decimal dot of
    # the location (e.g denotes lat = 300.12345)
    # used to code lat and long in a single number for a uniqueness test
    _LOCATION_PRECISION = 5
    _LAT_OFFSET = np.float(90.)
    
    def __init__(self):
        #keep private, this is not supposed to be used by the user
        self._data = np.empty([self._ROWNO, self._COLNO]) * np.nan
        self.metadata = od()
        self.meta_idx = od()
        
        self.contains_vars = []
        
        #self.logger = logging.getLogger(__name__)
    
    @property
    def vars_to_retrieve(self):
        logger.warning(DeprecationWarning("Attribute vars_to_retrieve is "
                                          "deprectated. Please use attr "
                                          "contains_vars instead"))
        return self.contains_vars
    
    def add_chunk(self, size=None):
        """Extend the size of the data array
        
        Parameters
        ----------
        size : :obj:`int`, optional
            number of additional rows. If None (default) or smaller than 
            minimum chunksize specified in attribute ``_CHUNKSIZE``, then the
            latter is used.
        """
        if size is None or size < self._CHUNKSIZE:
            size = self._CHUNKSIZE
        chunk = np.empty([size, self._COLNO])*np.nan
        self._data = np.append(self._data, chunk, axis=0)
        self._ROWNO += size
        logger.info("adding chunk, new array size ({})".format(self._data.shape))
# =============================================================================
#     
#     def __setitem__(self, key, val):
#         if self.index_pointer >= self._ROWNO:
#             self._add_chunk()
#         self._data[key] = val
#         self.index_pointer += 1
#         
# =============================================================================
    def _to_timeseries_helper(self, val, start_date=None, end_date=None, 
                              freq=None):
        """small helper routine for self.to_timeseries to not to repeat the 
        same code fragment three times"""

        data_found_flag = False
        temp_dict = {}
        # do not return anything for stations without data
        temp_dict['station_name'] = val['station_name']
        temp_dict['latitude'] = val['stat_lat']
        temp_dict['longitude'] = val['stat_lon']
        temp_dict['altitude'] = val['stat_alt']
        temp_dict['PI'] = val['PI']
        temp_dict['dataset_name'] = val['dataset_name']
        if 'files' in val:
            temp_dict['files'] = val['files']
        for var in val['idx']:
            if var in self.vars_to_retrieve:
                data_found_flag = True
                temp_dict[var] = pd.Series(self._data[val['idx'][var], self._DATAINDEX],
                                           index=pd.to_datetime(
                                               self._data[
                                                   val['idx'][var], self._TIMEINDEX],
                                               unit='s'))

                temp_dict[var] = temp_dict[var][start_date:end_date].drop_duplicates()
                if freq is not None:
                    temp_dict[var] = temp_dict[var][start_date:end_date].resample(freq).mean()

        if data_found_flag:
            return temp_dict
        else:
            return None
        
    # TODO: review docstring        
    def to_timeseries(self, station_name=None, start_date=None, end_date=None, 
                      freq=None):
        """method to get the ObsData object data as dict using pd.Series for the variables

        Parameters
        ----------
        station_names : :obj:`tuple` or :obj:`str:`, optional
            station_name or list of station_names to return
        start_date, end_date : :obj:`str:`, optional
            date strings with start and end date to return
        freq : obj:`str:`, optional
            frequency to resample to using the pandas resample method
            us the offset aliases as noted in
            http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases

        Returns
        -------
        list or dictionary
            station_names is a string: dictionary with station data
            station_names is list or None: list of dictionaries with station data

        Example
        -------
        >>> import pyaerocom.io.readobsdata
        >>> obj = pyaerocom.io.readobsdata.ReadUngridded()
        >>> obj.read()
        >>> pdseries = obj.to_timeseries()
        >>> pdseriesmonthly = obj.to_timeseries(station_name='Avignon',start_date='2011-01-01', end_date='2012-12-31', freq='M')
        """

        out_data = []
        if station_name is None:
            # return all stations
            for index, val in self.metadata.items():
                data = self._to_timeseries_helper(val, start_date, 
                                                  end_date, freq)
                if data is not None:
                    out_data.append(data)
        elif isinstance(station_name, str):
            # user asked for a single station_name
            # return a single dictionary in this case
            for index, val in self.metadata.items():
                if station_name == val['station_name']:
                    # we might change this to return a list at some point
                    return self._to_timeseries_helper(val, start_date, 
                                                      end_date, freq)
        elif isinstance(station_name, list):
            # user asked for a list of station_names
            # return list with matching station_names
            for index, val in self.metadata.items():
                # print(val['station_name'])
                if val['station_name'] in station_name:
                    data = self._to_timeseries_helper(val)
                    if data is not None:
                        out_data.append(self._to_timeseries_helper(val, 
                                                                   start_date, 
                                                                   end_date, 
                                                                   freq))

        return out_data
    
    def code_lat_lon_in_float(self):
        """method to code lat and lon in a single number so that we can use np.unique to
        determine single locations"""

        # multiply lons with 10 ** (three times the needed) precision and add the lats muliplied with 1E(precision) to it
        self.coded_loc = self._data[:, self._LONINDEX] * 10 ** (3 * self._LOCATION_PRECISION) + (
                self._data[:, self._LATINDEX] + self._LAT_OFFSET) * (10 ** self._LOCATION_PRECISION)
        return self.coded_loc

    ###################################################################################
    def decode_lat_lon_from_float(self):
        """method to decode lat and lon from a single number calculated by code_lat_lon_in_float
        """

        lons = np.trunc(self.coded_loc / 10 ** (2 * self._LOCATION_PRECISION)) / 10 ** self._LOCATION_PRECISION
        lats = (self.coded_loc - np.trunc(self.coded_loc / 10 ** (2 * self._LOCATION_PRECISION)) * 10 ** (
                2 * self._LOCATION_PRECISION)) / (10 ** self._LOCATION_PRECISION) - self._LAT_OFFSET

        return lats, lons

    ###################################################################################
    @property
    def shape(self):
        """Shape of data array"""
        return self._data.shape
    
    @property
    def is_empty(self):
        return True if len(self.metadata) == 0 else False
    
    @property
    def all_datasets(self):
        """Return list of names of all datasets in this object"""
        datasets = []
        for info in self.metadata.values():
            ds = info['dataset_name']
            if not ds in datasets:
                datasets.append(ds)
        return datasets
        
    def merge(self, other, new_obj=True):
        """Merge another data object with this one
        
        Parameters
        -----------
        other : UngriddedData
            other data object
        new_obj : bool
            if True, this object remains unchanged and the merged data objects
            are returned in a new instance of :class:`UngriddedData`. If False, 
            then this object is modified
        
        Returns
        -------
        UngriddedData
            merged data object
            
        Raises
        -------
        ValueError
            if input object is not an instance of :class:`UngriddedData`
        """
        if not isinstance(other, UngriddedData):
            raise ValueError("Invalid input, need instance of UngriddedData, "
                             "got: {}".format(type(other)))
        if new_obj:
            obj = deepcopy(self)
        else:
            obj = self
        
        if obj.is_empty:
            obj._data = other._data
            obj.metadata = other.metadata
            obj.meta_idx = other.meta_idx
        else:
            # get offset in metadata index
            meta_offset = max([x for x in obj.metadata.keys()]) + 1
            data_offset = self.shape[0]
            # add this offset to indices of meta dictionary in input data object
            for meta_idx_other, meta_other in other.metadata.items():
                meta_idx = meta_offset + meta_idx_other
                obj.metadata[meta_idx] = meta_other
                _idx_map = od()
                for var_name, indices in other.meta_idx[meta_idx_other].items():
                    _idx_map[var_name] = np.asarray(indices) + data_offset
                obj.meta_idx[meta_idx] = _idx_map
            obj._data = np.vstack([obj._data, other._data])
        return obj
        
    def append(self, other):
        """Append other instance of :class:`UngriddedData` to this object
        
        Note
        ----
        Calls :func:`merge(other, new_obj=False)`
        
        Parameters
        -----------
        other : UngriddedData
            other data object
        
        Returns
        -------
        UngriddedData
            merged data object
            
        Raises
        -------
        ValueError
            if input object is not an instance of :class:`UngriddedData`
            
        """
        return self.merge(other, new_obj=False)
    
    def __and__(self, other):
        """Merge this object with another using the logical ``and`` operator
        
        Example
        -------
        >>> from pyaerocom.io import ReadAeronetSdaV2
        >>> read = ReadAeronetSdaV2()
        
        >>> d0 = read.read(last_file=10)
        >>> d1 = read.read(first_file=10, last_file=20)
    
        >>> merged = d0 & d1
        
        >>> print(d0.shape, d1.shape, merged.shape)
        (7326, 11) (9894, 11) (17220, 11)
        """
        return self.merge(other, new_obj=True)
        
    @property
    def longitude(self):
        """Longitudes of stations"""
        return [stat['stat_lon'] for stat in self.metadata.values()]

    @longitude.setter
    def longitude(self, value):
        raise AttributeError("Longitudes cannot be changed, please check "
                             "underlying data type stored in attribute grid")

    @property
    def latitude(self):
        """Latitudes of stations"""
        return [stat['stat_lat'] for stat in self.metadata.values()]

    @latitude.setter
    def latitude(self, value):
        raise AttributeError("Latitudes cannot be changed, please check "
                             "underlying data type stored in attribute grid")

    @property
    def station_name(self):
        """Latitudes of data"""
        stat_names = [self.metadata[np.float(x)]['station_name'] for x in range(len(self.metadata))]
        return stat_names

    @station_name.setter
    def station_name(self, value):
        raise AttributeError("Station names cannot be changed, please check "
                             "underlying data type stored in attribute grid")
    
    @property
    def time(self):
        """Time dimension of data"""
        raise NotImplementedError

    @time.setter
    def time(self, value):
        raise AttributeError("Time array cannot be changed, please check "
                             "underlying data type stored in attribute grid")
      
    def find_common_stations(self, other, check_vars_available=None,
                             check_coordinates=True, 
                             max_diff_coords_km=0.1):
        """Search common stations between two UngriddedData objects
        
        This method loops over all stations that are stored within this 
        object (using :attr:`metadata`) and checks if the corresponding 
        station exists in a second instance of :class:`UngriddedData` that
        is provided. The check is performed on basis of the station name, and
        optionally, if desired, for each station name match, the lon lat 
        coordinates can be compared within a certain radius (defaul 0.1 km).
        
        Note
        ----
        This is a beta version and thus, to be treated with care.
        
        Parameters
        ----------
        other : UngriddedData
            other object of ungridded data 
        check_vars_available : :obj:`list` (or similar), optional
            list of variables that need to be available in stations of both 
            datasets
        check_coordinates : bool
            if True, check that lon and lat coordinates of station candidates
            match within a certain range, specified by input parameter
            ``max_diff_coords_km``
            
        Returns
        -------
        OrderedDict
            dictionary where keys are meta_indices of the common station in 
            this object and corresponding values are meta indices of the 
            station in the other object
            
        """
        if len(self.all_datasets) > 1:
            raise NotImplementedError('This data object contains data from '
                                      'more than one dataset and thus may '
                                      'include multiple station matches for '
                                      'each station ID. This method, however '
                                      'is implemented such, that it checks '
                                      'only the first match for each station')
        elif len(other.all_datasets) > 1:
            raise NotImplementedError('Other data object contains data from '
                                      'more than one dataset and thus may '
                                      'include multiple station matches for '
                                      'each station ID. This method, however '
                                      'is implemented such, that it checks '
                                      'only the first match for each station')
        _check_vars = False
        if check_vars_available is not None:
            _check_vars = True
            if isinstance(check_vars_available, str):
                check_vars_available = [check_vars_available]
            elif isinstance(check_vars_available, (tuple, np.ndarray)):
                check_vars_available = list(check_vars_available)
            if not isinstance(check_vars_available, list):
                raise ValueError('Invalid input for check_vars_available. Need '
                                 'str or list-like, got: {}'
                                 .format(check_vars_available))
        lat_len = 111.0 #approximate length of latitude degree in km
        station_map = od()
        stations_other = other.station_name
        for meta_idx, meta in self.metadata.items():
            name = meta['station_name']
            # bool that is used to accelerate things
            ok = True
            if _check_vars:
                for var in check_vars_available:
                    try:
                        if not var in meta['variables']:
                            logger.debug('No {} in data of station {}'
                                         '({})'.format(var, name, 
                                                       meta['dataset_name']))
                            ok = False
                    except: # attribute does not exist or is not iterable
                        ok = False
            if ok and name in stations_other:
                for meta_idx_other, meta_other in other.metadata.items():
                    if meta_other['station_name'] == name:
                        if _check_vars:
                            for var in check_vars_available:
                                try:
                                    if not var in meta_other['variables']:
                                        logger.debug('No {} in data of station'
                                                     ' {} ({})'.format(var, 
                                                     name, 
                                                     meta_other['dataset_name']))
                                        ok = False
                                except: # attribute does not exist or is not iterable
                                    ok = False
                        if ok and check_coordinates:
                            dlat = abs(meta['stat_lat']-meta_other['stat_lat'])
                            dlon = abs(meta['stat_lon']-meta_other['stat_lon'])
                            lon_fac = np.cos(np.deg2rad(meta['stat_lat']))
                            #compute distance between both station coords
                            dist = np.linalg.norm((dlat*lat_len, 
                                                   dlon*lat_len*lon_fac))
                            print('Distance in km {}'.format(dist))
                            if dist > max_diff_coords_km:
                                logger.warning('Coordinate of station '
                                               '{} varies more than {} km '
                                               'between {} and {} data'
                                               .format(name, max_diff_coords_km,
                                                       meta['dataset_name'],
                                                       meta_other['dataset_name']))
                                ok = False
                        if ok: #match found
                            station_map[meta_idx] = meta_idx_other
                            logger.debug('Found station match {}'.format(name))
                            # no need to further iterate over the rest 
                            continue
                        
        return station_map
        
    
    def find_common_data_points(self, other, var_name, sampling_freq='daily'):
        if not isinstance(other, UngriddedData):
            raise NotImplementedError('So far, common data points can only be '
                                      'retrieved between two instances of '
                                      'UngriddedData')
        common = self.find_common_stations(other, check_vars_available=var_name,
                                           check_coordinates=True)
        if len(common) == 0:
            raise DataExtractionError('None of the stations in the two '
                                      'match')
        for idx_this, idx_other in common.items():
            data_idx_this = self.meta_idx[idx_this][var_name]
            data_idx_other = other.meta_idx[idx_other][var_name]
            time_this = self._data[data_idx_this, self._TIMEINDEX]
            time_other = other._data[data_idx_other, self._TIMEINDEX]
            
            
        return time_this, time_other
            
    def __getitem__(self, key, val):
        raise NotImplementedError
        
    def __str__(self):
        head = "Pyaerocom {}".format(type(self).__name__)
        s = "\n{}\n{}".format(head, len(head)*"-")
        arrays = ''
        for k, v in self.metadata.items():
            if isinstance(v, dict):
                s += "\n{} ({})".format(k, type(v))
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
            else:
                s += "\n%s: %s" %(k,v)
        s += arrays
        return s

def reduce_array_closest(arr_nominal, arr_to_be_reduced):
    test = sorted(arr_to_be_reduced)
    closest_idx = []
    for num in sorted(arr_nominal):
        idx = np.argmin(abs(test - num))
        closest_idx.append(idx)
        test = test[(idx+1):]
    return closest_idx    
        
if __name__ == "__main__":
    
    from pyaerocom import change_verbosity
    from pyaerocom.io import ReadAeronetSunV2, ReadAeronetSunV3
    change_verbosity('debug')
    read_v2 = ReadAeronetSunV2()
    read_v3 = ReadAeronetSunV3()
    
    data_v2 = read_v2.read(vars_to_retrieve='od550aer', last_file=30)
    data_v3 = read_v3.read(vars_to_retrieve='od550aer', last_file=30)
    
    #t0common_stats = data_v2.find_common_stations(data_v3)
    t0, t1 = data_v2.find_common_data_points(data_v3, 'od550aer')
    
    t1_red = reduce_array_closest(t1, t0)
    
    