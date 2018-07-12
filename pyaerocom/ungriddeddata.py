#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 13:39:55 2018

@author: jonasg
"""
import numpy as np
from collections import OrderedDict as od
import pandas as pd

class UngriddedData(object):
    """Class representing ungridded data
    
    The data is organised in a 2-dimensional numpy array where the first index
    axis corresponds to individual measurements and the second dimension 
    contains addit
    
    Attributes
    ----------
    _data : ndarray
        (private) numpy array of dtype np.float64 initially of shape (10000,8)
        data point array
    metadata : dict
        dictionary containing meta information about the data
    """
    _METADATAKEYINDEX = 0
    _TIMEINDEX = 1
    _LATINDEX = 2
    _LONINDEX = 3
    _ALTITUDEINDEX = 4
    _VARINDEX = 5
    _DATAINDEX = 6

    _COLNO = 11
    _ROWNO = 10000
    _CHUNKSIZE = 1000
    # The following number denotes the kept precision after the decimal dot of
    # the location (e.g denotes lat = 300.12345)
    # used to code lat and long in a single number for a uniqueness test
    _LOCATION_PRECISION = 5
    _LAT_OFFSET = np.float(90.)
    
    def __init__(self, verbose=True):
        #keep private, this is not supposed to be used by the user
        self._data = np.empty([self._ROWNO, self._COLNO])*np.nan
        self.metadata = od()
        self.verbose = verbose
    
    def add_chunk(self):
        chunk = np.empty([self._CHUNKSIZE, self._COLNO])*np.nan
        self._data = np.append(self._data, chunk, axis=0)
        self._ROWNO += self._CHUNKSIZE
        if self.verbose:
            print("adding chunk, new array size ({})".format(self._data.shape))
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
        temp_dict['station name'] = val['station name']
        temp_dict['latitude'] = val['latitude']
        temp_dict['longitude'] = val['longitude']
        temp_dict['altitude'] = val['altitude']
        temp_dict['PI'] = val['PI']
        temp_dict['dataset_name'] = val['dataset_name']
        if 'files' in val:
            temp_dict['files'] = val['files']
        for var in val['indexes']:
            if var in self.vars_to_retrieve:
                data_found_flag = True
                temp_dict[var] = pd.Series(self._data[val['indexes'][var], self._DATAINDEX],
                                           index=pd.to_datetime(
                                               self._data[
                                                   val['indexes'][var], self._TIMEINDEX],
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
            station name or list of station names to return
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
        >>> obj = pyaerocom.io.readobsdata.ReadUngridded(verbose=True)
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
            # user asked for a single station name
            # return a single dictionary in this case
            for index, val in self.metadata.items():
                if station_name == val['station name']:
                    # we might change this to return a list at some point
                    return self._to_timeseries_helper(val, start_date, 
                                                      end_date, freq)
        elif isinstance(station_name, list):
            # user asked for a list of station names
            # return list with matching station names
            for index, val in self.metadata.items():
                # print(val['station name'])
                if val['station name'] in station_name:
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
        """Longitudes of data"""

        lons = [self.metadata[np.float(x)]['longitude'] for x in range(len(self.metadata))]
        return lons

    @longitude.setter
    def longitude(self, value):
        raise AttributeError("Longitudes cannot be changed, please check "
                             "underlying data type stored in attribute grid")

    @property
    def latitude(self):
        """Latitudes of data"""
        lats = [self.metadata[np.float(x)]['latitude'] for x in range(len(self.metadata))]
        return lats

    @latitude.setter
    def latitude(self, value):
        raise AttributeError("Latitudes cannot be changed, please check "
                             "underlying data type stored in attribute grid")

    @property
    def station_name(self):
        """Latitudes of data"""
        stat_names = [self.metadata[np.float(x)]['station name'] for x in range(len(self.metadata))]
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