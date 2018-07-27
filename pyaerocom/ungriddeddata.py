#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import numpy as np
from collections import OrderedDict as od
import pandas as pd

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
        self._data = np.empty([self._ROWNO, self._COLNO])*np.nan
        self.metadata = od()
        self.meta_idx = od()
        
        self.logger = logging.getLogger(__name__)
    
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
        self.logger.info("adding chunk, new array size ({})".format(self._data.shape))
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
        """small helper routine for self.to_timeseries to not to repeat the same code fragment three times"""

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
    def longitude(self):
        """Longitudes of stations"""
        return [stat['stat_lon'] for stat in self.metadata.values()]

    @longitude.setter
    def longitude(self, value):
        raise AttributeError("Longitudes cannot be changed, please check "
                             "underlying data type stored in attribute grid")

    @property
    def latitude(self):
        """Latitudes of data"""
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
        
    def __getitem__(self, key, val):
        raise NotImplementedError
        
    