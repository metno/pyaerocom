#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from copy import deepcopy
from datetime import datetime
from collections import OrderedDict as od
import pandas as pd
from pyaerocom import logger
from pyaerocom._lowlevel_helpers import BrowseDict
from pyaerocom.exceptions import (DataExtractionError, VarNotAvailableError,
                                  TimeMatchError, DataCoverageError,
                                  MetaDataError, DataUnitError)
from pyaerocom import StationData
from pyaerocom._lowlevel_helpers import dict_to_str, list_to_shortstr
from pyaerocom.mathutils import in_range
from pyaerocom.helpers import (to_pandas_timestamp, same_meta_dict, 
                               TS_TYPE_TO_PANDAS_FREQ)

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
    
    TODO
    ----
    Include unit attribute for each variable (in pyaerocom.io package: make
    sure to include units during ungridded read, if available)
    
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
    var_idx : dict
        mapping of variable name (keys, e.g. od550aer) to numerical variable 
        index of this variable in data numpy array (in column specified by
        :attr:`_VARINDEX`)
    """
    __version__ = '0.13'
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
    
    def __init__(self, num_points=None):
        if num_points is None:
            num_points = self._ROWNO
        #keep private, this is not supposed to be used by the user
        self._data = np.empty([num_points, self._COLNO]) * np.nan
        self.unit = BrowseDict()
        self.metadata = od()
        self.data_revision = od()
        self.meta_idx = od()
        self.var_idx = od()
        
        self.filter_hist = od()
    
    @property
    def contains_vars(self):
        """List of all variables in this dataset"""
        return [k for k in self.var_idx.keys()]
    
    @property
    def contains_datasets(self):
        """List of all datasets in this object"""
        datasets = []
        for info in self.metadata.values():
            ds = info['dataset_name']
            if not ds in datasets:
                datasets.append(ds)
        return datasets
    
    @property
    def contains_instruments(self):
        """List of all instruments in this object"""
        instruments = []
        for info in self.metadata.values():
            try:
                instr = info['instrument_name']
                if instr is not None and not instr in instruments:
                    instruments.append(instr)
            except:
                pass
        return instruments
    
    @property
    def shape(self):
        """Shape of data array"""
        return self._data.shape
    
    @property
    def is_empty(self):
        """Boolean specifying whether this object contains data or not"""
        return True if len(self.metadata) == 0 else False

    @property
    def vars_to_retrieve(self):
        logger.warning(DeprecationWarning("Attribute vars_to_retrieve is "
                                          "deprectated. Please use attr "
                                          "contains_vars instead"))
        return self.contains_vars
    
    @property
    def is_filtered(self):
        """Boolean specifying whether this data object has been filtered
        
        Note
        ----
        Details about applied filtering can be found in :attr:`filter_hist`
        """
        if len(self.filter_hist) > 0:
            return True
        return False
    
    @property
    def longitude(self):
        """Longitudes of stations"""
        return [stat['stat_lon'] for stat in self.metadata.values()]

    @longitude.setter
    def longitude(self, value):
        raise AttributeError("Station longitudes cannot be changed")

    @property
    def latitude(self):
        """Latitudes of stations"""
        return [stat['stat_lat'] for stat in self.metadata.values()]

    @latitude.setter
    def latitude(self, value):
        raise AttributeError("Station latitudes cannot be changed")
        
    @property
    def altitude(self):
        """Alttudes of stations"""
        return [stat['stat_alt'] for stat in self.metadata.values()]

    @altitude.setter
    def altitude(self, value):
        raise AttributeError("Station altitudes cannot be changed")
        
    @property
    def station_name(self):
        """Latitudes of data"""
        stat_names = [self.metadata[np.float(x)]['station_name'] for x in range(len(self.metadata))]
        return stat_names

    @station_name.setter
    def station_name(self, value):
        raise AttributeError("Station names cannot be changed")
    
    @property
    def time(self):
        """Time dimension of data"""
        raise NotImplementedError

    @time.setter
    def time(self, value):
        raise AttributeError("Time array cannot be changed")
        
    def last_filter_applied(self):
        if not self.is_filtered:
            raise AttributeError('No filters were applied so far')
        return self.filter_hist[max(self.filter_hist.keys())]
    
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

    def _to_timeseries_helper(self, val, start_date=None, end_date=None, 
                              freq=None):
        """small helper routine for self.to_timeseries to not to repeat the 
        same code fragment three times"""
        raise NotImplementedError('Outdated, cf. new version of to_timeseries ')
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
    
    def to_gridded_data(self):
        lons = self.longitude
        lats = self.latitude
        raise NotImplementedError
        
    # TODO: review docstring        
    def to_timeseries(self, station_name=None, start_date=None, end_date=None, 
                      freq=None):
        """Convert this object into individual pandas.Series objects

        Parameters
        ----------
        station_name : :obj:`tuple` or :obj:`str:`, optional
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
        from warnings import warn
        msg = ('This method does currently not work due to recent API changes, '
               'and is therefore a wrapper for method to_station_data or '
               'to_station_data_all dependent on whether a station name is '
               'provided or not.')
        warn(DeprecationWarning(msg))
        if station_name is None:
            return self.to_station_data_all(start=start_date, stop=end_date,
                                            freq=freq)
        if isinstance(station_name, str):
            station_name = [station_name]
        if isinstance(station_name, list):
            indices = []
            for meta_idx, info in self.metadata.items():
                if info['station_name'] in station_name:
                    indices.append(meta_idx)
            if len(indices) == 0:
                raise MetaDataError('No such station(s): {}'.format(station_name))
            elif len(indices) == 1:
                # return single dictionary, like before 
                # TODO: maybe change this after clarification
                return self.to_station_data(start=start_date, stop=end_date,
                                            freq=freq)
            else:
                out_data = []
                for meta_idx in indices:
                    try:
                        out_data.append(self.to_station_data(start=start_date, 
                                                             stop=end_date,
                                                             freq=freq))
                    except (VarNotAvailableError, TimeMatchError, 
                            DataCoverageError) as e:
                        logger.warning('Failed to convert to StationData '
                               'Error: {}'.format(repr(e)))
                return out_data
                    
    
    # TODO: see docstring
    def to_station_data(self, meta_idx, vars_to_convert=None, start=None, 
                        stop=None, freq=None, interp_nans=False, 
                        min_coverage_interp=0.68, 
                        data_as_series=True, _test_mode=False):
        """Convert data from one station to :class:`StationData`
        
        Todo
        ----
        - Review for retrieval of profile data (e.g. Lidar data)
        - Handle stop time if only year is provided 
        
        Parameters
        ----------
        meta_idx : float
            index of station or name of station.
        vars_to_convert : :obj:`list` or :obj:`str`, optional
            variables that are supposed to be converted. If None, use all 
            variables that are available for this station
        start
            start time, optional (if not None, input must be convertible into
            pandas.Timestamp)
        stop 
            stop time, optional (if not None, input must be convertible into
            pandas.Timestamp)
        freq : str
            pandas frequency string (e.g. 'D' for daily, 'M' for month end) or
            valid pyaerocom ts_type
        interp_nans : bool
            if True, all NaN values in the time series for each 
            variable are interpolated using linear interpolation
        min_coverage_interp : float
            required coverage fraction for interpolation (default is 0.68, i.e.
            roughly corresponding to 1 sigma)
        data_as_series : bool
            if True, all data columns are returned as time-series
            
        
        Returns
        -------
        StationData
            data of this station (can be used like dictionary if desired)
        """
        if isinstance(meta_idx, str):
            try:
                meta_idx = self.station_name.index(meta_idx)
            except ValueError:
                raise ValueError('No such station {} in UngriddedData'.format(meta_idx))
                
        if isinstance(vars_to_convert, str):
            vars_to_convert = [vars_to_convert]
        if start is None:
            start = pd.Timestamp('1970')
        else:
            start = to_pandas_timestamp(start)
        if stop is None:
            stop = pd.Timestamp('2200')
        else:
            stop = to_pandas_timestamp(stop)
        
        if freq in TS_TYPE_TO_PANDAS_FREQ:
            freq = TS_TYPE_TO_PANDAS_FREQ[freq]
        
        stat_data = StationData()
        val = self.metadata[meta_idx]
        
        # do not return anything for stations without data
        # TODO: consider writing stat_lon, stat_lat and stat_alt
        stat_data['station_name'] = val['station_name']
        stat_data['latitude'] = val['stat_lat']
        stat_data['longitude'] = val['stat_lon']
        stat_data['altitude'] = val['stat_alt']
        stat_data['PI'] = val['PI']
        stat_data['dataset_name'] = val['dataset_name']
        stat_data['ts_type_src'] = val['ts_type']
        if 'instrument_name' in val:
            stat_data['instrument_name'] = val['instrument_name']
        
        if 'files' in val:
            stat_data['files'] = val['files']
        
        if vars_to_convert is None:
            vars_to_convert = val['variables']
        vars_to_convert = np.intersect1d(vars_to_convert, val['variables']) 
        if not len(vars_to_convert) >= 1:
            raise VarNotAvailableError('None of the input variables matches, '
                                       'or station does not contain data')
        first_var = vars_to_convert[0]
        indices_first = self.meta_idx[meta_idx][first_var]
        dtime = self._data[indices_first, self._TIMEINDEX].astype('datetime64[s]')
        stat_data['dtime'] = dtime
        if not any([start <= t <= stop for t in dtime]):
            raise TimeMatchError('No data available for station {} ({}) in '
                                 'time interval {} - {}'
                                 .format(stat_data['station_name'],
                                         stat_data['dataset_name'],
                                         start, stop))
        for var in vars_to_convert:
            indices = self.meta_idx[meta_idx][var]
            data = self._data[indices, self._DATAINDEX]
            if data_as_series:
                data = pd.Series(data, dtime)
                if not data.index.is_monotonic:
                    data = data.sort_index()
                data = data[start:stop]
                if _test_mode:
                    data[0] = np.nan
                    data[4:6] = np.nan
                if interp_nans:
                    coverage = 1 - data.isnull().sum() / len(data)
                    if coverage < min_coverage_interp:
                        raise DataCoverageError('{} data of station {} ({}) in '
                                                'time interval {} - {} contains '
                                                'too many invalid measurements '
                                                'for interpolation.'
                                                .format(var,
                                                        stat_data['station_name'],
                                                        stat_data['dataset_name'],
                                                        start, stop))
                    data = data.interpolate().dropna()
                if freq is not None:
                    data = data.resample(freq).mean()     
            stat_data[var] = data
        return stat_data
    
    def to_station_data_all(self, vars_to_convert=None, start=None, stop=None, 
                            freq=None, interp_nans=False, 
                            min_coverage_interp=0.68):
        """Convert all possible stations to :class:`StationData` objects

        Parameters
        ----------
        vars_to_convert : :obj:`list` or :obj:`str`, optional
            variables that are supposed to be converted. If None, use all 
            variables that are available for this station
        start
            start time, optional (if not None, input must be convertible into
            pandas.Timestamp)
        stop 
            stop time, optional (if not None, input must be convertible into
            pandas.Timestamp)
        freq : str
            pandas frequency string (e.g. 'D' for daily, 'M' for month end)
        interp_nans : bool
            if True, all NaN values in the time series for each 
            variable are interpolated using linear interpolation
        min_coverage_interp : float
            required coverage fraction for interpolation (default is 0.68, i.e.
            roughly corresponding to 1 sigma)

        Returns
        -------
        list 
            list containing loaded instances of :class:`StationData` for each
            station in :attr:`metadata`, where :func:`to_station_data` was 
            successful, and ``None`` entries for meta data indices where 
            :func:`to_station_data` failed (e.g. because no temporal match, 
            etc.)

        """
        out_data = []
        for index, val in self.metadata.items():
            try:
                data = self.to_station_data(index, vars_to_convert, start, 
                                            stop, freq, interp_nans, 
                                            min_coverage_interp)
                
                out_data.append(data)
            # catch the exceptions that are acceptable
            except (VarNotAvailableError, TimeMatchError, 
                    DataCoverageError) as e:
                logger.warning('Failed to convert to StationData '
                               'Error: {}'.format(repr(e)))
                # append None to make sure indices of stations are 
                # preserved in output array
                out_data.append(None)
        return out_data
    
    # TODO: check more general cases (i.e. no need to convert to StationData
    # if no time conversion is required)
    def get_variable_data(self, variables, start=None, stop=None,
                          ts_type=None, **kwargs):
        """Extract all data points of a certain variable
        
        Parameters
        ----------
        vars_to_extract : :obj:`str` or :obj:`list`
            all variables that are supposed to be accessed
        """
        if isinstance(variables, str):
            variables = [variables]
        all_stations = self.to_station_data_all(variables, start, stop, 
                                                freq=ts_type, **kwargs)
        result = {}
        num_stats = {}
        for var in variables:
            result[var] = []
            num_stats[var] = 0
        for stat_data in all_stations:
            if stat_data is not None:
                num_points = len(stat_data.dtime)
                for var in variables:
                    if var in stat_data:
                        num_stats[var] += 1
                        result[var].extend(stat_data[var])
                    else:
                        result[var].extend([np.nan]*num_points)
        result['num_stats'] = num_stats
        return result
                     
        
    def _check_filter_match(self, meta, str_f, list_f, range_f):
        """Helper method that checks if station meta item matches filters
        
        Note
        ----
        This method is used in :func:`apply_filter`
        """
        for k, v in str_f.items():
            if not meta[k] == v:
                return False
        for k, v in list_f.items():
            if not meta[k] in v:
                return False
        for k, v in range_f.items():
            if not in_range(meta[k], v[0], v[1]):
                return False
        return True
    
    def _init_meta_filters(self, **filter_attributes):
        """Init filter dictionary for :func:`apply_filter_meta`
        
        Parameters
        ----------
        **filter_attributes
            valid meta keywords that are supposed to be filtered and the 
            corresponding filter values (or value ranges)
            Only valid meta keywords are considered (e.g. dataset_name, 
            stat_lon, stat_lat, stat_alt, ts_type)
            
        Returns
        -------
        tuple
            3-element tuple containing
            
            - dict: string match filters for metakeys \
              (e.g. dict['dataset_name'] = 'AeronetSunV2Lev2.daily')
            - dict: in-list match filters for metakeys \
              (e.g. dict['station_name'] = ['stat1', 'stat2', 'stat3'])
            - dict: in-range dictionary for metakeys \
              (e.g. dict['stat_lon'] = [-30, 30])
            
        """
        # initiate filters that are checked
        valid_keys = self.metadata[0].keys()
        str_f = {}
        list_f = {}
        range_f = {}
        for key, val in filter_attributes.items():
            if not key in valid_keys:
                raise IOError('Invalid input parameter for filtering: {}. '
                              'Please choose from {}'.format(key, valid_keys))
            
            if isinstance(val, str):
                str_f[key] = val
            elif isinstance(val, (list, np.ndarray, tuple)): 
                if all([isinstance(x, str) for x in val]):
                    list_f[key] = val
                elif len(val) == 2:
                    try:
                        low, high = float(val[0]), float(val[1])
                        range_f[key] = [low, high]
                    except:
                        raise IOError('Failed to convert input ({}) specifying '
                                      'value range of {} into floating point '
                                      'numbers'.format(list(val), key))
        return (str_f, list_f, range_f)
    
    # TODO: check, confirm and remove Beta version note in docstring                   
    def filter_by_meta(self, **filter_attributes):
        """Flexible method to filter these data based on input meta specs
        
        Note
        ----
        Beta version
        
        Todo
        ----
        Check filter history (attr filter_hist) before applying filter in 
        order to see if filter(s) already have been applied before
        
        Parameters
        ----------
        **filter_attributes
            valid meta keywords that are supposed to be filtered and the 
            corresponding filter values (or value ranges)
            Only valid meta keywords are considered (e.g. dataset_name, 
            stat_lon, stat_lat, stat_alt, ts_type)
            
        Returns
        -------
        UngriddedData
            filtered ungridded data object
        
        Raises
        ------
        NotImplementedError
            when variables are supposed to be filtered (not yet possible)
        IOError
            if any of the input keys are not valid meta key
            
        Example
        -------
        >>> import pyaerocom as pya
        >>> r = pya.io.ReadUngridded(['AeronetSunV2Lev2.daily', 
                                      'AeronetSunV3Lev2.daily'], 'od550aer')
        >>> data = r.read()
        >>> data_filtered = data.filter_by_meta(dataset_name='AeronetSunV2Lev2.daily',
        ...                                     stat_lon=[-30, 30],
        ...                                     stat_lat=[20, 70],
        ...                                     stat_alt=[0, 1000])
        """
        new = UngriddedData()
        meta_idx_new = 0.0
        data_idx_new = 0
    
        
        if 'variables' in filter_attributes:
            raise NotImplementedError('Cannot yet filter by variables')
            
        filters = self._init_meta_filters(**filter_attributes)
        for meta_idx, meta in self.metadata.items():
            if self._check_filter_match(meta, *filters):
                new.metadata[meta_idx_new] = meta
                new.meta_idx[meta_idx_new] = od()
                for var in meta['variables']:
                    indices = self.meta_idx[meta_idx][var]
                    
                    totnum = len(indices)
                    if (data_idx_new + totnum) >= new._ROWNO:
                    #if totnum < data_obj._CHUNKSIZE, then the latter is used
                        new.add_chunk(totnum)
                    stop = data_idx_new + totnum
                    
                    new._data[data_idx_new:stop, :] = self._data[indices, :]
                    new.meta_idx[meta_idx_new][var] = np.arange(data_idx_new,
                                                                stop)
                    new.var_idx[var] = self.var_idx[var]
                    data_idx_new += totnum
                
                meta_idx_new += 1
            else:
                logger.debug('{} does not match filter and will be ignored'
                             .format(meta))
        if meta_idx_new == 0 or data_idx_new == 0:
            raise DataExtractionError('Filtering results in empty data object')
        new._data = new._data[:data_idx_new]
        # write history of filtering applied 
        new.filter_hist.update(self.filter_hist)
        time_str = datetime.now().strftime('%Y%m%d%H%M%S')
        new.filter_hist[int(time_str)] = filter_attributes
        new.data_revision.update(self.data_revision)
        
        return new
    
    
    def extract_dataset(self, dataset_name):
        """Extract single dataset into new instance of :class:`UngriddedData`
        
        Note
        ----
        Beta version. Please doublecheck correctness.
        
        Parameters
        -----------
        dataset_name : str
            ID of dataset
        
        Returns
        -------
        UngriddedData
            new instance of ungridded data containing only data from specified
            input network
        """
        logger.info('Extracting dataset {} from data object'.format(dataset_name))
        if not dataset_name in self.contains_datasets:
            raise AttributeError('Dataset {} is not contained in this data '
                                 'object'.format(dataset_name))
        new = UngriddedData()
        meta_idx_new = 0.0
        data_idx_new = 0
        
        for meta_idx, meta in self.metadata.items():
            if meta['dataset_name'] == dataset_name:
                new.metadata[meta_idx_new] = meta
                new.meta_idx[meta_idx_new] = od()
                for var in meta['variables']:
                    indices = self.meta_idx[meta_idx][var]
                    totnum = len(indices)
                    if (data_idx_new + totnum) >= new._ROWNO:
                    #if totnum < data_obj._CHUNKSIZE, then the latter is used
                        new.add_chunk(totnum)
                    stop = data_idx_new + totnum
                    
                    new._data[data_idx_new:stop, :] = self._data[indices, :]
                    new.meta_idx[meta_idx_new][var] = np.arange(data_idx_new,
                                                                stop)
                    data_idx_new += totnum
                
                meta_idx_new += 1
        if meta_idx_new == 0 or data_idx_new == 0:
            raise DataExtractionError('Filtering results in empty data object')
        new._data = new._data[:data_idx_new]
        time_str = datetime.now().strftime('%Y%m%d%H%M%S')
        new.filter_hist[int(time_str)] = {'dataset_name' : dataset_name}
        new.data_revision[dataset_name] = self.data_revision[dataset_name]
        return new
        
    def station_data_to_ascii(self, vars_to_convert=None, start=None, stop=None, 
                              freq=None, interp_nans=False, 
                              min_coverage_interp=0.68):
        """
        TODO
        ----
        Write docstring
        """
        raise NotImplementedError
        
    def code_lat_lon_in_float(self):
        """method to code lat and lon in a single number so that we can use np.unique to
        determine single locations"""

        # multiply lons with 10 ** (three times the needed) precision and add the lats muliplied with 1E(precision) to it
        self.coded_loc = self._data[:, self._LONINDEX] * 10 ** (3 * self._LOCATION_PRECISION) + (
                self._data[:, self._LATINDEX] + self._LAT_OFFSET) * (10 ** self._LOCATION_PRECISION)
        return self.coded_loc
    
    def decode_lat_lon_from_float(self):
        """method to decode lat and lon from a single number calculated by code_lat_lon_in_float
        """

        lons = np.trunc(self.coded_loc / 10 ** (2 * self._LOCATION_PRECISION)) / 10 ** self._LOCATION_PRECISION
        lats = (self.coded_loc - np.trunc(self.coded_loc / 10 ** (2 * self._LOCATION_PRECISION)) * 10 ** (
                2 * self._LOCATION_PRECISION)) / (10 ** self._LOCATION_PRECISION) - self._LAT_OFFSET

        return lats, lons
            

    def _find_common_meta(self, ignore_keys=['PI', 'var_info']):
        """Searches all metadata dictionaries that are the same
        
        Parameters
        ----------
        ignore_keys : list
            list containing meta keys that are supposed to be ignored
            
        Returns
        -------
        tuple
            2-element tuple containing
            
            - list containing lists with common meta indices
            - list containing corresponding meta dictionaries
        """
        meta_registered = []
        same_indices = []
        for meta_key, meta in self.metadata.items():
            found = False
            for idx, meta_reg in enumerate(meta_registered):
                if same_meta_dict(meta_reg, meta, ignore_keys=ignore_keys):
                    same_indices[idx].append(meta_key)
                    found = True
            if not found:
                meta_registered.append(meta)
                same_indices.append([meta_key])
        return same_indices, meta_registered
    
    def merge_common_meta(self, ignore_keys=['PI', 'var_info']):
        """Merge all meta entries that are the same
            
        Todo
        ----
        Keep mapping of ``var_info`` (if defined in ``metadata``) to data 
        points (e.g. EBAS), since the data sources may be at different 
        wavelengths
        
        Parameters
        ----------
        ignore_keys : list
            list containing meta keys that are supposed to be ignored
            
        Returns
        -------
        UngriddedData
            merged data object
        """
        lst_meta_idx, lst_meta = self._find_common_meta()
        new = UngriddedData(num_points=self.shape[0])
        didx = 0
        for i, idx_lst in enumerate(lst_meta_idx):
            _meta_check = lst_meta[i]
            _meta_idx_new = od()
            for meta_idx in idx_lst:
                meta = self.metadata[meta_idx]
                if not same_meta_dict(meta, _meta_check,  
                                      ignore_keys=ignore_keys):
                    raise ValueError('Unexpected error. Please debug or '
                                     'contact jonasg@met.no')
                data_var_idx = self.meta_idx[meta_idx]
                for var, data_idx in data_var_idx.items():
                    num = len(data_idx)
                    stop = didx + num
                    new._data[didx:stop, :] = self._data[data_idx]
                    if not var in _meta_idx_new:
                        _meta_idx_new[var] = np.arange(didx, stop)
                    else:
                        _idx = np.append(_meta_idx_new[var], np.arange(didx, stop))
                        _meta_idx_new[var] = _idx
                    didx += num
            
            new.meta_idx[i] = _meta_idx_new
            new.metadata[i] = _meta_check
        new.var_idx.update(self.var_idx)
        new.unit = self.unit
        new.filter_hist.update(self.filter_hist)
        return new
        
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
            obj.unit = other.unit
            obj.data_revision = other.data_revision
            obj.meta_idx = other.meta_idx
            obj.var_idx = other.var_idx
        else:
            # get offset in metadata index
            meta_offset = max([x for x in obj.metadata.keys()]) + 1
            data_offset = obj.shape[0]
            for var, unit in other.unit:
                if var in obj.unit.items():
                    if not unit == obj.unit[var]:
                        raise DataUnitError('Cannot merge other instance of '
                                        'UngriddedData since units for variable '
                                        '{} do not match.'.format(var))
                else:
                    obj.unit[var]=unit
                    
            # add this offset to indices of meta dictionary in input data object
            for meta_idx_other, meta_other in other.metadata.items():
                meta_idx = meta_offset + meta_idx_other
                obj.metadata[meta_idx] = meta_other
                _idx_map = od()
                for var_name, indices in other.meta_idx[meta_idx_other].items():
                    _idx_map[var_name] = np.asarray(indices) + data_offset
                obj.meta_idx[meta_idx] = _idx_map
            
            for var, idx in other.var_idx.items():
                if var in obj.var_idx: #variable already exists in this object
                    if not idx == obj.var_idx[var]:
                        other.change_var_idx(var, obj.var_idx[var])
# =============================================================================
#                         raise AttributeError('Could not merge data objects. '
#                                              'Variable {} occurs in both '
#                                              'datasets but has different '
#                                              'variable index in data array'
#                                              .format(var))
# =============================================================================
                else: # variable does not yet exist
                    idx_exists = [v for v in obj.var_idx.values()]
                    if idx in idx_exists: 
                        # variable index is already assigned to another 
                        # variable and needs to be changed
                        new_idx = max(idx_exists)+1
                        other.change_var_idx(var, new_idx)
                        obj.var_idx[var] = new_idx
                    else:
                        obj.var_idx[var] = idx
            obj._data = np.vstack([obj._data, other._data])
            obj.data_revision.update(other.data_revision)
        return obj
    
    def change_var_idx(self, var_name, new_idx):
        """Change index that is assigned to variable
        
        Each variable in this object has assigned a unique index that is
        stored in the dictionary :attr:`var_idx` and which is used internally
        to access data from a certain variable from the data array 
        :attr:`_data` (the indices are stored in the data column specified by
        :attr:`_VARINDEX`, cf. class header).
        
        This index thus needs to be unique for each variable and hence, may 
        need to be updated, when two instances of :class:`UngriddedData` are 
        merged (cf. :func:`merge`). 

        And the latter is exactrly what this function does.
        
        Parameters
        ----------
        var_name : str
            name of variable
        new_idx : int
            new index of variable
            
        Raises
        ------
        ValueError
            if input ``new_idx`` already exist in this object as a variable 
            index
        """
        if new_idx in self.var_idx.values():
            raise ValueError('Fatal: variable index cannot be assigned a new '
                             'index that is already assigned to one of the '
                             'variables in this object')
        cidx = self.var_idx[var_name]
        self.var_idx[var_name] = new_idx
        var_indices = np.where(self._data[:, self._VARINDEX]==cidx)
        self._data[var_indices, self._VARINDEX] = new_idx
        
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
    
    def all_datapoints_var(self, var_name):
        """Get array of all data values of input variable
        
        Parameters
        ----------
        var_name : str
            variable name
            
        Returns
        -------
        ndarray
            1-d numpy array containing all values of this variable 
            
        Raises
        ------
        AttributeError
            if variable name is not available
        """
        if not var_name in self.var_idx:
            raise AttributeError('Variable {} not available in data'
                                 .format(var_name))
        idx = self.var_idx[var_name]
        mask = np.where(self._data[:, self._VARINDEX]==idx)[0]
        return self._data[mask, self._DATAINDEX]
    
    def num_obs_var_valid(self, var_name):
        """Number of valid observations of variable in this dataset
        
        Parameters
        ----------
        var_name : str
            name of variable
        
        Returns
        -------
        int
            number of valid observations (all values that are not NaN)
        """
        pass
    
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
        if len(self.contains_datasets) > 1:
            raise NotImplementedError('This data object contains data from '
                                      'more than one dataset and thus may '
                                      'include multiple station matches for '
                                      'each station ID. This method, however '
                                      'is implemented such, that it checks '
                                      'only the first match for each station')
        elif len(other.contains_datasets) > 1:
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
                            if dist > max_diff_coords_km:
                                logger.warning('Coordinate of station '
                                               '{} varies more than {} km '
                                               'between {} and {} data. '
                                               'Retrieved distance: {:.2f} km '
                                               .format(name, max_diff_coords_km,
                                                       meta['dataset_name'],
                                                       meta_other['dataset_name'],
                                                       dist))
                                ok = False
                        if ok: #match found
                            station_map[meta_idx] = meta_idx_other
                            logger.debug('Found station match {}'.format(name))
                            # no need to further iterate over the rest 
                            continue
                        
        return station_map
        
    # TODO: brute force at the moment, we need to rethink and define how to
    # work with time intervals and perform temporal merging.
    def find_common_data_points(self, other, var_name, sampling_freq='daily'):
        if not sampling_freq == 'daily':
            raise NotImplementedError('Currently only works with daily data')
        if not isinstance(other, UngriddedData):
            raise NotImplementedError('So far, common data points can only be '
                                      'retrieved between two instances of '
                                      'UngriddedData')
        #find all stations that are common
        common = self.find_common_stations(other, 
                                           check_vars_available=var_name,
                                           check_coordinates=True)
        if len(common) == 0:
            raise DataExtractionError('None of the stations in the two '
                                      'match')
        dates = []
        data_this_match = []
        data_other_match = []
        
        for idx_this, idx_other in common.items():
            data_idx_this = self.meta_idx[idx_this][var_name]
            data_idx_other = other.meta_idx[idx_other][var_name]
            
            # timestamps of variable match for station...
            dtimes_this = self._data[data_idx_this, self._TIMEINDEX]
            dtimes_other = other._data[data_idx_other, other._TIMEINDEX]
            # ... and corresponding data values of variable
            data_this = self._data[data_idx_this, self._DATAINDEX]
            data_other = other._data[data_idx_other, other._DATAINDEX]
            # round to daily resolution. looks too complicated, but is much 
            # faster than pandas combined with datetime 
            date_nums_this = (dtimes_this.astype('datetime64[s]').
                              astype('M8[D]').astype(int))
            date_nums_other = (dtimes_other.astype('datetime64[s]').
                               astype('M8[D]').astype(int))
            
            # TODO: loop over shorter array
            for idx, datenum in enumerate(date_nums_this):
                matches = np.where(date_nums_other==datenum)[0]
                if len(matches) == 1:
                    dates.append(datenum)
                    data_this_match.append(data_this[idx])
                    data_other_match.append(data_other[matches[0]])
        
        return (dates, data_this_match, data_other_match)
    
    def __contains__(self, key):
        """Check if input key (str) is valid dataset, variable, instrument or
        station name
        
        
        Parameters
        ----------
        key : str
            search key
            
        Returns
        -------
        bool
            True, if key can be found, False if not
        """
        
        if not isinstance(key, str):
            raise ValueError('Need string (e.g. variable name, station name, '
                             'instrument name')
        if key in self.contains_datasets:
            return True
        elif key in self.contains_vars:
            return True
        elif key in self.station_name:
            return True
        elif key in self.contains_instruments:
            return True
        return False
        
    def __repr__(self):
        return ('{} <networks: {}; vars: {}; instruments: {};'
                'No. of stations: {}'
                .format(type(self).__name__,self.contains_datasets,
                        self.contains_vars, self.contains_instruments,
                        len(self.metadata)))
        
    def __getitem__(self, key):
        return self.to_station_data(key)
    
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
    
    def __str__(self):
        head = "Pyaerocom {}".format(type(self).__name__)
        s = "\n{}\n{}".format(head, len(head)*"-")
        s += ('\nContains networks: {}'
              '\nContains variables: {}'
              '\nContains instruments: {}'
              '\nTotal no. of stations: {}'.format(self.contains_datasets,
                                                   self.contains_vars,
                                                   self.contains_instruments,
                                                   len(self.metadata)))
        if self.is_filtered:
            s += '\nFilters that were applied:'
            for tstamp, f in self.filter_hist.items():
                if f:
                    s += '\n Filter time log: {}'.format(tstamp)
                    for key, val in f.items():
                        s += '\n\t{}: {}'.format(key, val)
                    
        return s
    def __str__OLD(self):
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
    import matplotlib.pyplot as plt
    plt.close('all')
    
    change_verbosity('debug')
    read_v2 = ReadAeronetSunV2()
    read_v3 = ReadAeronetSunV3()
    
    read_v2.read_first_file()
    
    data_v2 = read_v2.read(vars_to_retrieve=read_v2.PROVIDES_VARIABLES, 
                           last_file=20)
    data_v3 = read_v3.read(vars_to_retrieve=read_v3.PROVIDES_VARIABLES, 
                           last_file=20)
    
    od550aer_all_v2 = data_v2.all_datapoints_var('od550aer')
    od550aer_all_v3 = data_v3.all_datapoints_var('od550aer')
    
    #t0common_stats = data_v2.find_common_stations(data_v3)
    dates, data_this, data_other = data_v2.find_common_data_points(data_v3, 
                                                                   'od550aer')
    
    plt.plot(data_this, data_other, ' *g')
    plt.xlabel('AOD 550 nm, Aeronet Sun V2')
    plt.ylabel('AOD 550 nm, Aeronet Sun V3')
    plt.xlim([0,8])
    plt.ylim([0,8])
    plt.grid()  
    
    data_monthly = data_v3.get_variable_data('od550aer',ts_type='monthly')['od550aer']
    print(data_monthly)
    #t0_red = reduce_array_closest(t1, t0)
    
    