#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from datetime import datetime
from collections import OrderedDict as od
import fnmatch
import os
import pandas as pd
from pyaerocom import const
logger = const.logger
print_log = const.print_log
from pyaerocom._lowlevel_helpers import merge_dicts
from pyaerocom.exceptions import (DataExtractionError, VarNotAvailableError,
                                  TimeMatchError, DataCoverageError,
                                  MetaDataError, StationNotFoundError)
from pyaerocom.combine_vardata_ungridded import combine_vardata_ungridded
from pyaerocom.stationdata import StationData
from pyaerocom.region import Region
from pyaerocom.geodesy import get_country_info_coords
from pyaerocom.mathutils import in_range
from pyaerocom.helpers import (same_meta_dict,
                               start_stop_str,
                               start_stop, merge_station_data,
                               isnumeric)

from pyaerocom.metastandards import STANDARD_META_KEYS
from pyaerocom.units_helpers import get_unit_conversion_fac

from pyaerocom.helpers_landsea_masks import (load_region_mask_xr,
                                             get_mask_value)

class UngriddedData(object):
    """Class representing point-cloud data (ungridded)

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
    metadata : dict
        dictionary containing meta information about the data. Keys are
        floating point numbers corresponding to each station, values are
        corresponding dictionaries containing station information.
    meta_idx : dict
        dictionary containing index mapping for each station and variable. Keys
        correspond to metadata key (float -> station, see :attr:`metadata`) and
        values are dictionaries containing keys specifying variable name and
        corresponding values are arrays or lists, specifying indices (rows) of
        these station / variable information in :attr:`_data`. Note: this
        information is redunant and is there to accelarate station data
        extraction since the data index matches for a given metadata block
        do not need to be searched in the underlying numpy array.
    var_idx : dict
        mapping of variable name (keys, e.g. od550aer) to numerical variable
        index of this variable in data numpy array (in column specified by
        :attr:`_VARINDEX`)

    Parameters
    ----------
    num_points : :obj:`int`, optional
        inital number of total datapoints (number of rows in 2D dataarray)
    add_cols : :obj:`list`, optional
        list of additional index column names of 2D datarray.

    """
    #: version of class (for caching)
    __version__ = '0.21'

    #: default number of rows that are dynamically added if total number of
    #: data rows is reached.
    _CHUNKSIZE = 1000000

    #: The following indices specify what the individual rows of the datarray
    #: are reserved for. These may be expanded when creating an instance of
    #: this class by providing a list of additional index names.
    _METADATAKEYINDEX = 0
    _TIMEINDEX = 1
    _LATINDEX = 2
    _LONINDEX = 3
    _ALTITUDEINDEX = 4 # altitude of measurement device
    _VARINDEX = 5
    _DATAINDEX = 6
    _DATAHEIGHTINDEX = 7
    _DATAERRINDEX = 8 # col where errors can be stored
    _DATAFLAGINDEX = 9 # can be used to store flags
    _STOPTIMEINDEX = 10 # can be used to store stop time of acq.
    _TRASHINDEX = 11 #index where invalid data can be moved to (e.g. when outliers are removed)

    # The following number denotes the kept precision after the decimal dot of
    # the location (e.g denotes lat = 300.12345)
    # used to code lat and long in a single number for a uniqueness test
    _LOCATION_PRECISION = 5
    _LAT_OFFSET = 90.

    STANDARD_META_KEYS = STANDARD_META_KEYS

    @property
    def _ROWNO(self):
        return self._data.shape[0]

    def __init__(self, num_points=None, add_cols=None):

        if num_points is None:
            num_points = self._CHUNKSIZE

        self._chunksize = num_points
        self._index = self._init_index(add_cols)

        #keep private, this is not supposed to be used by the user
        self._data = np.empty([num_points, self._COLNO]) * np.nan

        self.metadata = od()
        # single value data revision is deprecated
        self.data_revision = od()
        self.meta_idx = od()
        self.var_idx = od()

        self._idx = -1

        self.filter_hist = od()

    def _get_data_revision_helper(self, data_id):
        """
        Helper method to get last data revision

        Parameters
        ----------
        data_id : str
            ID of dataset for which revision is to be retrieved

        Raises
        ------
        MetaDataError
            If multiple revisions are found for this dataset.

        Returns
        -------
        latest revision (None if no revision is available).

        """
        rev = None
        for meta in self.metadata.values():
            if meta['data_id'] == data_id:
                if rev is None:
                    rev = meta['data_revision']
                elif not meta['data_revision'] == rev:
                    raise MetaDataError('Found different data revisions for '
                                        'dataset {}'.format(data_id))
        if data_id in self.data_revision:
            if not rev == self.data_revision[data_id]:
                raise MetaDataError('Found different data revisions for '
                                    'dataset {}'.format(data_id))
        self.data_revision[data_id] = rev
        return rev

    def _check_index(self):
        """Checks if all indices are assigned correctly"""
        assert len(self.meta_idx) == len(self.metadata), \
            'Mismatch len(meta_idx) and len(metadata)'

        assert sum(self.meta_idx.keys()) == sum(self.metadata.keys()), \
            'Mismatch between keys of metadata dict and meta_idx dict'

        _varnums = self._data[:, self._VARINDEX]
        var_indices = np.unique(_varnums[~np.isnan(_varnums)])

        assert len(var_indices) == len(self.var_idx), \
            'Mismatch between number of variables in data array and var_idx attr.'

        assert sum(var_indices) == sum(self.var_idx.values()), \
            'Mismatch between variable indices in data array and var_idx attr.'

        vars_avail = self.var_idx

        for idx, meta in self.metadata.items():
            if not 'var_info' in meta:
                if not 'variables' in meta:
                    raise AttributeError('Need either variables (list) or '
                                         'var_info (dict) in meta block {}: {}'
                                         .format(idx, meta))
                meta['var_info'] = {}
                for v in meta['variables']:
                    meta['var_info'][v] = {}

            var_idx = self.meta_idx[idx]
            for var, indices in var_idx.items():
                if len(indices) == 0:
                    continue # no data assigned for this metadata index

                assert var in meta['var_info'], \
                    ('Var {} is indexed in meta_idx[{}] but not in metadata[{}]'
                     .format(var, idx, idx))

                var_idx_data = np.unique(self._data[indices, self._VARINDEX])
                assert len(var_idx_data) == 1, ('Found multiple variable indices for '
                          'var {}: {}'.format(var, var_idx_data))
                assert var_idx_data[0] == vars_avail[var], (
                    f'Mismatch between {var} index assigned in data and '
                    f'var_idx for {idx} in meta-block'
                    )

    @staticmethod
    def from_station_data(stats, add_meta_keys=None):
        """
        Create UngriddedData from input station data object(s)

        Parameters
        ----------
        stats : list or StationData
            input data object(s)
        add_meta_keys : list, optional
            list of metadata keys that are supposed to be imported from the
            input `StationData` objects, in addition to the default metadata
            retrieved via :func:`StationData.get_meta`.

        Raises
        ------
        ValueError
            if any of the input data objects is not an instance of
            :class:`StationData`.

        Returns
        -------
        UngriddedData
            ungridded data object created from input station data objects

        """
        if add_meta_keys is None:
            add_meta_keys = []
        elif isinstance(add_meta_keys, str):
            add_meta_keys = [add_meta_keys]
        elif not isinstance(add_meta_keys, list):
            raise ValueError(
                f'Invalid input for add_meta_keys {add_meta_keys}... need list'
                )
        if isinstance(stats, StationData):
            stats = [StationData]
        data_obj = UngriddedData(num_points=1000000)

        meta_key = 0.0
        idx = 0

        metadata = data_obj.metadata
        meta_idx = data_obj.meta_idx

        var_count_glob = -1
        for stat in stats:
            if isinstance(stat, dict):
                stat = StationData(**stat)
            elif not isinstance(stat, StationData):
                raise ValueError('Need instances of StationData or dicts')
            metadata[meta_key] = od()
            metadata[meta_key].update(stat.get_meta(force_single_value=False,
                                                    quality_check=False,
                                                    add_none_vals=True))
            for key in add_meta_keys:
                try:
                    val = stat[key]
                except KeyError:
                    val = 'undefined'

                metadata[meta_key][key] = val


            metadata[meta_key]['var_info'] = od()

            meta_idx[meta_key] = {}

            append_vars = list(stat.var_info.keys())

            for var in append_vars:
                if not var in data_obj.var_idx:
                    var_count_glob += 1
                    var_idx = var_count_glob
                    data_obj.var_idx[var] = var_idx
                else:
                    var_idx = data_obj.var_idx[var]

                vardata = stat[var]

                if isinstance(vardata, pd.Series):
                    times = vardata.index
                    values = vardata.values
                else:
                    times = stat['dtime']
                    values = vardata
                    if not len(times) == len(values):
                        raise ValueError

                times = np.asarray([np.datetime64(x, 's') for x in times])
                times = np.float64(times)

                num_times = len(times)
                #check if size of data object needs to be extended
                if (idx + num_times) >= data_obj._ROWNO:
                    #if totnum < data_obj._CHUNKSIZE, then the latter is used
                    data_obj.add_chunk(num_times)

                start = idx
                stop = start + num_times

                #write common meta info for this station (data lon, lat and
                #altitude are set to station locations)
                data_obj._data[start:stop,
                               data_obj._LATINDEX] = stat['latitude']
                data_obj._data[start:stop,
                               data_obj._LONINDEX] = stat['longitude']
                data_obj._data[start:stop,
                               data_obj._ALTITUDEINDEX] = stat['altitude']
                data_obj._data[start:stop,
                               data_obj._METADATAKEYINDEX] = meta_key

                # write data to data object
                data_obj._data[start:stop, data_obj._TIMEINDEX] = times

                data_obj._data[start:stop, data_obj._DATAINDEX] = values

                data_obj._data[start:stop, data_obj._VARINDEX] = var_idx

                if var in stat.data_flagged:
                    invalid = stat.data_flagged[var]
                    data_obj._data[start:stop, data_obj._DATAFLAGINDEX] = invalid

                if var in stat.data_err:
                    errs = stat.data_err[var]
                    data_obj._data[start:stop, data_obj._DATAERRINDEX] = errs

                var_info = stat['var_info'][var]
                metadata[meta_key]['var_info'][var] = od()
                metadata[meta_key]['var_info'][var].update(var_info)
                meta_idx[meta_key][var] = np.arange(start, stop)

                idx += num_times

            meta_key += 1

        # shorten data_obj._data to the right number of points
        data_obj._data = data_obj._data[:idx]

        data_obj._check_index()

        return data_obj

    def add_station_data(self, stat, meta_idx=None, data_idx=None,
                         check_index=False):
        raise NotImplementedError('Coming at some point')
        if meta_idx is None:
            meta_idx = self.last_meta_idx + 1
        elif meta_idx in self.meta_idx.keys():
            raise ValueError('Cannot add data at meta block index {}, index '
                             'already exists'.format(meta_idx))

        if data_idx is None:
            data_idx = self._data.shape[0]
        elif not np.all(np.isnan(self._data[data_idx, :])):
            raise ValueError('Cannot add data at data index {}, index '
                             'already exists'.format(data_idx))


    @property
    def last_meta_idx(self):
        """
        Index of last metadata block
        """
        return np.max(list(self.meta_idx.keys()))

    @property
    def index(self):
        return self._index

    @property
    def first_meta_idx(self):
        #First available metadata index
        return list(self.metadata.keys())[0]

    def _init_index(self, add_cols=None):
        """Init index mapping for columns in dataarray"""
        idx = od(meta           = self._METADATAKEYINDEX,
                 time           = self._TIMEINDEX,
                 stoptime       = self._STOPTIMEINDEX,
                 latitude       = self._LATINDEX,
                 longitude      = self._LONINDEX,
                 altitude       = self._ALTITUDEINDEX,
                 varidx         = self._VARINDEX,
                 data           = self._DATAINDEX,
                 dataerr        = self._DATAERRINDEX,
                 dataaltitude   = self._DATAHEIGHTINDEX,
                 dataflag       = self._DATAFLAGINDEX,
                 trash          = self._TRASHINDEX)

        next_idx = max(idx.values()) + 1
        if add_cols is not None:
            if not isinstance(add_cols, (list, tuple)):
                raise ValueError('Invalid input for add_cols. Need list or tuple')
            for name in add_cols:
                if name in idx:
                    raise ValueError('Cannot add new index with name {} since '
                                     'this index already exists at column '
                                     'position {}'.format(name, idx[name]))
                idx[name] = next_idx
                next_idx += 1
        return idx

    @property
    def _COLNO(self):
        return len(self._index)

    @property
    def has_flag_data(self):
        """Boolean specifying whether this object contains flag data"""
        return (~np.isnan(self._data[:, self._DATAFLAGINDEX])).any()

    def copy(self):
        """Make a copy of this object

        Returns
        -------
        UngriddedData
            copy of this object

        Raises
        ------
        MemoryError
            if copy is too big to fit into memory together with existing
            instance
        """
        from copy import deepcopy
        new = UngriddedData()
        new._data = np.copy(self._data)
        new.metadata = deepcopy(self.metadata)
        new.data_revision = self.data_revision
        new.meta_idx = deepcopy(self.meta_idx)
        new.var_idx = deepcopy(self.var_idx)
        new.filter_hist = deepcopy(self.filter_hist)
        return new

    @property
    def contains_vars(self):
        """List of all variables in this dataset"""
        return [k for k in self.var_idx.keys()]

    @property
    def contains_datasets(self):
        """List of all datasets in this object"""
        datasets = []
        for info in self.metadata.values():
            ds = info['data_id']
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
            except Exception:
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
        vals = []
        for v in self.metadata.values():
            try:
                vals.append(v['longitude'])
            except Exception:
                vals.append(np.nan)
        return vals

    @longitude.setter
    def longitude(self, value):
        raise AttributeError("Station longitudes cannot be changed")

    @property
    def latitude(self):
        """Latitudes of stations"""
        vals = []
        for v in self.metadata.values():
            try:
                vals.append(v['latitude'])
            except Exception:
                vals.append(np.nan)
        return vals

    @latitude.setter
    def latitude(self, value):
        raise AttributeError("Station latitudes cannot be changed")

    @property
    def altitude(self):
        """Altitudes of stations"""
        vals = []
        for v in self.metadata.values():
            try:
                vals.append(v['altitude'])
            except Exception:
                vals.append(np.nan)
        return vals

    @altitude.setter
    def altitude(self, value):
        raise AttributeError("Station altitudes cannot be changed")

    @property
    def station_name(self):
        """Latitudes of data"""
        vals = []
        for v in self.metadata.values():
            try:
                vals.append(v['station_name'])
            except Exception:
                vals.append(np.nan)
        return vals

    @station_name.setter
    def station_name(self, value):
        raise AttributeError("Station names cannot be changed")

    @property
    def unique_station_names(self):
        """List of unique station names"""
        return sorted(list(dict.fromkeys(self.station_name)))

    @property
    def available_meta_keys(self):
        """List of all available metadata keys

        Note
        ----
        This is a list of all metadata keys that exist in this dataset, but
        it does not mean that all of the keys are registered in all metadata
        blocks, especially if the data is merged from different sources with
        different metadata availability
        """
        metakeys = []
        for meta in self.metadata.values():
            for key in meta:
                if not key in metakeys:
                    metakeys.append(key)
        return metakeys

    @property
    def nonunique_station_names(self):
        """List of station names that occur more than once in metadata"""
        import collections
        lst = self.station_name
        return [item for item, count in collections.Counter(lst).items() if count > 1]

    @property
    def time(self):
        """Time dimension of data"""
        raise NotImplementedError

    @time.setter
    def time(self, value):
        raise AttributeError("Time array cannot be changed")

    def last_filter_applied(self):
        """Returns the last filter that was applied to this dataset

        To see all filters, check out :attr:`filter_hist`
        """
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
        if size is None or size < self._chunksize:
            size = self._chunksize
        chunk = np.empty([size, self._COLNO])*np.nan
        self._data = np.append(self._data, chunk, axis=0)
        logger.info("adding chunk, new array size ({})".format(self._data.shape))

    def _find_station_indices_wildcards(self, station_str):
        """Find indices of all metadata blocks matching input station name

        Parameters
        ----------
        station_str : str
            station name or wildcard pattern

        Returns
        -------
        list
           list containing all metadata indices that match the input station
           name or pattern

        Raises
        ------
        StationNotFoundError
            if no such station exists in this data object
        """
        idx = []
        for i, meta in self.metadata.items():
            if fnmatch.fnmatch(meta['station_name'], station_str):
                idx.append(i)
        if len(idx) == 0:
            raise StationNotFoundError('No station available in UngriddedData '
                                       'that matches pattern {}'
                                       .format(station_str))
        return idx

    def _find_station_indices(self, station_str):
        """Find indices of all metadata blocks matching input station name

        Parameters
        ----------
        station_str : str
            station name

        Returns
        -------
        list
           list containing all metadata indices that match the input station
           name or pattern

        Raises
        ------
        StationNotFoundError
            if no such station exists in this data object
        """
        idx = []
        for i, meta in self.metadata.items():
            if meta['station_name'] == station_str:
                idx.append(i)
        if len(idx) == 0:
            raise StationNotFoundError('No station available in UngriddedData '
                                       'that matches name {}'
                                       .format(station_str))
        return idx

    def _get_stat_coords(self):
        meta_idx = []
        coords = []
        for idx, meta in self.metadata.items():
            try:
                lat, lon = meta['latitude'], meta['longitude']
            except:
                const.print_log.warning('Could not retrieve lat lon coord '
                                        'at meta index {}'.format(idx))
                continue
            meta_idx.append(idx)
            coords.append((lat, lon))
        return (meta_idx, coords)

    def check_set_country(self):
        """CHecks all metadata entries for availability of country information

        Metadata blocks that are missing country entry will be updated based
        on country inferred from corresponding lat / lon coordinate. Uses
        :func:`pyaerocom.geodesy.get_country_info_coords` (library
        reverse-geocode) to retrieve countries. This may be errouneous
        close to country borders as it uses eucledian distance based on a list
        of known locations.

        Note
        ----
        Metadata blocks that do not contain latitude and longitude entries are
        skipped.

        Returns
        -------
        list
            metadata entries where country was added
        list
            corresponding countries that were inferred from lat / lon
        """
        meta_idx, coords = self._get_stat_coords()
        info = get_country_info_coords(coords)
        meta_idx_updated = []
        countries = []

        for i, idx in enumerate(meta_idx):
            meta = self.metadata[idx]
            if not 'country' in meta or meta['country'] is None:
                country = info[i]['country']
                meta['country'] = country
                meta['country_code'] = info[i]['country_code']
                meta_idx_updated.append(idx)
                countries.append(country)
        return (meta_idx_updated, countries)

    @property
    def countries_available(self):
        """
        Alphabetically sorted list of country names available
        """
        #self.check_set_country()
        countries = []
        for idx, meta in self.metadata.items():
            try:
                countries.append(meta['country'])
            except:
                const.logger.warning('No country information in meta block', idx)
        if len(countries) == 0:
            const.print_log.warning('None of the metadata blocks contains '
                                    'country information. You may want to '
                                    'run class method check_set_country first '
                                    'to automatically assign countries.')
        return sorted(dict.fromkeys(countries))

    def find_station_meta_indices(self, station_name_or_pattern,
                                  allow_wildcards=True):
        """Find indices of all metadata blocks matching input station name

        You may also use wildcard pattern as input (e.g. *Potenza*)

        Parameters
        ----------
        station_pattern : str
            station name or wildcard pattern
        allow_wildcards : bool
            if True, input station_pattern will be used as wildcard pattern and
            all matches are returned.

        Returns
        -------
        list
           list containing all metadata indices that match the input station
           name or pattern

        Raises
        ------
        StationNotFoundError
            if no such station exists in this data object
        """
        if not allow_wildcards:
            return self._find_station_indices(station_name_or_pattern)
        return self._find_station_indices_wildcards(station_name_or_pattern)

    # TODO: see docstring
    def to_station_data(self, meta_idx, vars_to_convert=None, start=None,
                        stop=None, freq=None,
                        merge_if_multi=True, merge_pref_attr=None,
                        merge_sort_by_largest=True, insert_nans=False,
                        allow_wildcards_station_name=True,
                        add_meta_keys=None,
                        **kwargs):
        """Convert data from one station to :class:`StationData`

        Todo
        ----
        - Review for retrieval of profile data (e.g. Lidar data)

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
        merge_if_multi : bool
            if True and if data request results in multiple instances of
            StationData objects, then these are attempted to be merged into one
            :class:`StationData` object using :func:`merge_station_data`
        merge_pref_attr
            only relevant for merging of multiple matches: preferred attribute
            that is used to sort the individual StationData objects by relevance.
            Needs to be available in each of the individual StationData objects.
            For details cf. :attr:`pref_attr` in docstring of
            :func:`merge_station_data`. Example could be `revision_date`. If
            None, then the stations will be sorted based on the number of
            available data points (if :attr:`merge_sort_by_largest` is True,
            which is default).
        merge_sort_by_largest : bool
            only relevant for merging of multiple matches: cf. prev. attr. and
            docstring of :func:`merge_station_data` method.
        insert_nans : bool
            if True, then the retrieved :class:`StationData` objects are filled
            with NaNs
        allow_wildcards_station_name : bool
            if True and if input `meta_idx` is a string (i.e. a station name or
            pattern), metadata matches will be identified applying wildcard
            matches between input `meta_idx` and all station names in this
            object.

        Returns
        -------
        StationData or list
            StationData object(s) containing results. list is only returned if
            input for meta_idx is station name and multiple matches are
            detected for that station (e.g. data from different instruments),
            else single instance of StationData. All variable time series are
            inserted as pandas Series
        """
        if isinstance(vars_to_convert, str):
            vars_to_convert = [vars_to_convert]
        elif vars_to_convert is None:
            vars_to_convert = self.contains_vars
            if len(vars_to_convert) == 0:
                raise DataCoverageError('UngriddedData object does not contain '
                                        'any variables')
        if start is None and stop is None:
            start = pd.Timestamp('1970')
            stop = pd.Timestamp('2200')
        else:
            start, stop = start_stop(start, stop)

        if isinstance(meta_idx, str):
            # user asks explicitely for station name, find all meta indices
            # that match this station
            meta_idx = self.find_station_meta_indices(meta_idx,
                                                      allow_wildcards_station_name)
        if not isinstance(meta_idx, list):
            meta_idx = [meta_idx]

        stats = []
        # ToDo: check consistency, consider using methods in helpers.py
        # check also Hans' issue on the topic
        start, stop = np.datetime64(start), np.datetime64(stop)

        for idx in meta_idx:
            try:
                stat = self._metablock_to_stationdata(idx,
                                                      vars_to_convert,
                                                      start, stop,
                                                      add_meta_keys)
                stats.append(stat)
            except (VarNotAvailableError, DataCoverageError) as e:
                logger.info('Skipping meta index {}. Reason: {}'
                            .format(idx, repr(e)))
        if merge_if_multi and len(stats) > 1:
            if len(vars_to_convert) > 1:
                raise NotImplementedError('Cannot yet merge multiple stations '
                                          'with multiple variables.')
            if merge_pref_attr is None:
                merge_pref_attr = self._try_infer_stat_merge_pref_attr(stats)
            merged = merge_station_data(stats, vars_to_convert,
                                        pref_attr=merge_pref_attr,
                                        sort_by_largest=merge_sort_by_largest,
                                        fill_missing_nan=False) #done below
            stats = [merged]

        stats_ok = []
        for stat in stats:
            for var in vars_to_convert:
                if not var in stat:
                    continue
                if freq is not None:
                    stat.resample_time(var, freq, inplace=True, **kwargs) # this does also insert NaNs, thus elif in next
                elif insert_nans:
                    stat.insert_nans_timeseries(var)
                if np.all(np.isnan(stat[var].values)):
                    stat = stat.remove_variable(var)
            if any([x in stat for x in vars_to_convert]):
                stats_ok.append(stat)

        if len(stats_ok) == 0:
            raise DataCoverageError('{} data could not be retrieved for meta '
                                    ' index (or station name) {}'
                                    .format(vars_to_convert, meta_idx))
        elif len(stats_ok) == 1:
            # return StationData object and not list
            return stats_ok[0]
        return stats_ok

    def _try_infer_stat_merge_pref_attr(self, stats):
        """Checks if a preferred attribute for handling of overlaps can be inferred

        Parameters
        ----------
        stats : list
            list of :class:`StationData` objects

        Returns
        -------
        str
            preferred merge attribute parameter, if applicable, else None
        """
        data_id = None
        pref_attr = None
        for stat in stats:
            if not 'data_id' in stat:
                return None
            elif data_id is None:
                data_id = stat['data_id']
                from pyaerocom.metastandards import DataSource
                s = DataSource(data_id=data_id) # reads default data source info that may contain preferred meta attribute
                pref_attr = s.stat_merge_pref_attr
                if pref_attr is None:
                    return None
            elif not stat['data_id'] == data_id: #station data objects contain different data sources
                return None
        return pref_attr

    ### TODO: check if both `variables` and `var_info` attrs are required in
    ### metdatda blocks
    def _metablock_to_stationdata(self, meta_idx, vars_to_convert,
                                  start=None, stop=None,
                                  add_meta_keys=None):
        """Convert one metadata index to StationData (helper method)

        See :func:`to_station_data` for input parameters
        """
        if add_meta_keys is None:
            add_meta_keys = []
        elif isinstance(add_meta_keys, str):
            add_meta_keys = [add_meta_keys]

        sd = StationData()
        meta = self.metadata[meta_idx]

        # TODO: make sure in reading classes that data_revision is assigned
        # to each metadata block and not only in self.data_revision
        rev = None
        if 'data_revision' in meta:
            rev = meta['data_revision']
        else:
            try:
                rev = self.data_revision[meta['data_id']]
            except Exception:
                logger.warning('Data revision could not be accessed')
        sd.data_revision = rev
        try:
            vars_avail = list(meta['var_info'].keys())
        except KeyError:
            if not 'variables' in meta or meta['variables'] in (None, []):
                raise VarNotAvailableError('Metablock does not contain variable '
                                           'information')
            vars_avail = meta['variables']

        for key in (self.STANDARD_META_KEYS + add_meta_keys):
            if key in sd.PROTECTED_KEYS:
                logger.warning(f'skipping protected key: {key}')
                continue
            try:
                sd[key] = meta[key]
            except KeyError:
                pass

        try:
            sd['ts_type_src'] = meta['ts_type']
        except KeyError:
            pass

        # assign station coordinates explicitely
        for ck in sd.STANDARD_COORD_KEYS:
            try:
                sd.station_coords[ck] = meta[ck]
            except KeyError:
                pass

        # if no input variables are provided, use the ones that are available
        # for this metadata block
        if vars_to_convert is None:
            vars_to_convert = vars_avail

        # find overlapping variables (ignore all other ones)
        vars_avail = np.intersect1d(vars_to_convert, vars_avail)
        if not len(vars_avail) >= 1:
            raise VarNotAvailableError('None of the input variables matches, '
                                       'or station does not contain data.')
        # init helper boolean that is set to True if valid data can be found
        # for at least one of the input variables
        FOUND_ONE = False
        for var in vars_avail:

            # get indices of this variable
            var_idx = self.meta_idx[meta_idx][var]

            # vector of timestamps corresponding to this variable
            dtime = self._data[var_idx,
                               self._TIMEINDEX].astype('datetime64[s]')

            # get subset
            subset = self._data[var_idx]

            # make sure to extract only valid timestamps
            if start is None:
                start = dtime.min()
            if stop is None:
                stop = dtime.max()

            # create access mask for valid time stamps
            tmask = np.logical_and(dtime >= start,
                                   dtime <= stop)

            # make sure there is some valid data
            if tmask.sum() == 0:
                logger.info('Ignoring station {}, var {} ({}): '
                            'no data available in specified time interval '
                            '{} - {}'.format(sd['station_name'],
                                             var,
                                             sd['data_id'],
                                             start, stop))
                continue

            dtime = dtime[tmask]
            subset = subset[tmask]

            vals = subset[:, self._DATAINDEX]
            if np.all(np.isnan(vals)):
                logger.warning('Ignoring station {}, var {} ({}):'
                            'All values are NaN'
                            .format(sd['station_name'], var, sd['data_id']))
                continue
            vals_err = subset[:, self._DATAERRINDEX]
            flagged = subset[:, self._DATAFLAGINDEX]
            altitude =  subset[:, self._DATAHEIGHTINDEX]

            data = pd.Series(vals, dtime)
            if not data.index.is_monotonic:
                data = data.sort_index()
            if any(~np.isnan(vals_err)):
                sd.data_err[var] = vals_err
            if any(~np.isnan(flagged)):
                sd.data_flagged[var] = flagged

            sd['dtime'] = data.index.values
            sd[var] = data
            sd['var_info'][var] = od()
            FOUND_ONE = True
            # check if there is information about altitude (then relevant 3D
            # variables and parameters are included too)
            if 'var_info' in meta:
                vi = meta['var_info']
            else:
                vi = {}
            if not np.isnan(altitude).all():
                if 'altitude' in vi:
                    sd.var_info['altitude'] = vi['altitude']
                sd.altitude = altitude
            if var in vi:
                sd.var_info[var].update(vi[var])

            if len(data.index) == len(data.index.unique()):
                sd.var_info[var]['overlap'] = False
            else:
                sd.var_info[var]['overlap'] = True
        if not FOUND_ONE:
            raise DataCoverageError('Could not retrieve any valid data for '
                                    'station {} and input variables {}'
                                    .format(sd['station_name'],
                                            vars_to_convert))
        return sd

    def _generate_station_index(self, by_station_name=True, ignore_index=None):
        """Generates index to loop over station names or metadata block indices"""
        if ignore_index is None:
            if by_station_name:
                return self.unique_station_names #all station names
            return list(range(len(self.metadata))) #all meta indices

        if not by_station_name:
            from pyaerocom.helpers import isnumeric
            if isnumeric(ignore_index):
                ignore_index = [ignore_index]
            if not isinstance(ignore_index, list):
                raise ValueError('Invalid input for ignore_index, need number '
                                 'or list')
            return [i for i in range(len(self.metadata)) if not i in ignore_index]

        # by station name and ignore certation stations
        _iter = []
        if isinstance(ignore_index, str):
            ignore_index = [ignore_index]
        if not isinstance(ignore_index, list):
            raise ValueError('Invalid input for ignore_index, need str or '
                             'list')
        for stat_name in self.unique_station_names:
            ok = True
            for name_or_pattern in ignore_index:
                if fnmatch.fnmatch(stat_name, name_or_pattern):
                    ok = False
            if ok:
                _iter.append(stat_name)
        return _iter

    def to_station_data_all(self, vars_to_convert=None, start=None, stop=None,
                            freq=None, by_station_name=True,
                            ignore_index=None, **kwargs):
        """Convert all data to :class:`StationData` objects

        Creates one instance of :class:`StationData` for each metadata block in
        this object.

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
            or valid pyaerocom ts_type (e.g. 'hourly', 'monthly').
        by_station_name : bool
            if True, then iter over unique_station_name (and merge multiple
            matches if applicable), else, iter over metadata index
        **kwargs
            additional keyword args passed to :func:`to_station_data` (e.g.
            `merge_if_multi, merge_pref_attr, merge_sort_by_largest,
            insert_nans`)

        Returns
        -------
        dict
            4-element dictionary containing following key / value pairs:

                - stats: list of :class:`StationData` objects
                - station_name: list of corresponding station names
                - latitude: list of latitude coordinates
                - longitude: list of longitude coordinates

        """
        out_data = {'stats'         : [],
                    'station_name'  : [],
                    'latitude'      : [],
                    'failed'        : [],
                    'longitude'     : []}

        _iter = self._generate_station_index(by_station_name,
                                             ignore_index)
        for idx in _iter:

            try:
                data = self.to_station_data(idx, vars_to_convert, start,
                                            stop, freq,
                                            merge_if_multi=True,
                                            allow_wildcards_station_name=False,
                                            **kwargs)

                out_data['latitude'].append(data['latitude'])
                out_data['longitude'].append(data['longitude'])
                out_data['station_name'].append(data['station_name'])
                out_data['stats'].append(data)

            # catch the exceptions that are acceptable
            except (VarNotAvailableError, TimeMatchError,
                    DataCoverageError) as e:
                logger.warning('Failed to convert to StationData '
                               'Error: {}'.format(repr(e)))
                out_data['failed'].append([idx, repr(e)])
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

    def _check_str_filter_match(self, meta, negate, str_f):
        # Check string equality for input meta data and filters. Supports
        # wildcard matching
        for metakey, filterval in str_f.items():
            # key does not exist in this specific meta_block
            if not metakey in meta:
                return False
            # check if this key is in negate list (then result will be True
            # for all that do not match the specified filter input value(s))
            neg = metakey in negate

            # actual value of this key in input metadata
            metaval = meta[metakey]

            # check equality of values
            match = metaval == filterval
            if match: # direct match found
                if neg: # key is flagged in negate -> no match
                    return False
            else: # no direct match found
                # check wildcard match
                if '*' in filterval: # no wildcard in
                    match = fnmatch.fnmatch(metaval, filterval)
                    if neg:
                        if match:
                            return False
                    else:
                        if not match:
                            return False
                elif not neg: # no match, no wildcard match and not inverted
                    return False
        return True

    def _check_filter_match(self, meta, negate, str_f, list_f, range_f, val_f):
        """Helper method that checks if station meta item matches filters

        Note
        ----
        This method is used in :func:`apply_filter`
        """
        if not self._check_str_filter_match(meta, negate, str_f):
            return False

        for metakey, filterval in list_f.items():
            if not metakey in meta:
                return False
            neg = metakey in negate
            metaval = meta[metakey]
            match = metaval == filterval
            if match: # lists are identical
                if neg:
                    return False
            else:
                # value in metadata block is different from filter value
                match = metaval in filterval
                if match:
                    if neg:
                        return False
                else:
                    # current metavalue is not equal the filterlist and is also
                    # not contained in the filterlist. However, one or more
                    # entries in the filterlist may be wildcard
                    if isinstance(metaval, str):
                        found = False
                        for entry in filterval:
                            if '*' in entry:
                                match = fnmatch.fnmatch(metaval, entry)
                                if match:
                                    found = True
                                    if neg:
                                        return False
                        if not found and not neg:
                            return False
        # range filter
        for metakey, filterval in range_f.items():
            if not metakey in meta:
                return False
            neg = metakey in negate
            match = in_range(meta[metakey], filterval[0], filterval[1])
            if (neg and match) or (not neg and not match):
                return False

        for metakey, filterval in val_f.items():
            if not metakey in meta:
                return False
            neg = metakey in negate
            match = meta[metakey] == filterval
            if (neg and match) or (not neg and not match):
                return False
        return True

    def _init_meta_filters(self, **filter_attributes):
        """Init filter dictionary for :func:`apply_filter_meta`

        Parameters
        ----------
        **filter_attributes
            valid meta keywords that are supposed to be filtered and the
            corresponding filter values (or value ranges)
            Only valid meta keywords are considered (e.g. data_id,
            longitude, latitude, altitude, ts_type)

        Returns
        -------
        tuple
            3-element tuple containing

            - dict: string match filters for metakeys \
              (e.g. dict['data_id'] = 'AeronetSunV2Lev2.daily')
            - dict: in-list match filters for metakeys \
              (e.g. dict['station_name'] = ['stat1', 'stat2', 'stat3'])
            - dict: in-range dictionary for metakeys \
              (e.g. dict['longitude'] = [-30, 30])

        """
        # initiate filters that are checked
        valid_keys = self.metadata[self.first_meta_idx].keys()
        str_f = {}
        list_f = {}
        range_f = {}
        val_f = {}
        for key, val in filter_attributes.items():
            if not key in valid_keys:
                raise IOError('Invalid input parameter for filtering: {}. '
                              'Please choose from {}'.format(key, valid_keys))

            if isinstance(val, str):
                str_f[key] = val
            elif isnumeric(val):
                val_f[key] = val
            elif isinstance(val, (list, np.ndarray, tuple)):
                if all([isinstance(x, str) for x in val]):
                    list_f[key] = val
                elif len(val) == 2:
                    try:
                        low, high = float(val[0]), float(val[1])
                        if not low < high:
                            raise ValueError('First entry needs to be smaller '
                                             'than 2nd')
                        range_f[key] = [low, high]
                    except Exception as e:
                        raise ValueError('Failed to convert input ({}) specifying '
                                         'value range of {} into floating point '
                                         'numbers. Reason: {}'
                                         .format(list(val), key, repr(e)))
        return (str_f, list_f, range_f, val_f)

    def check_convert_var_units(self, var_name, to_unit=None,
                                    inplace=True):
        obj = self if inplace else self.copy()


        # get the unit
        if to_unit is None:
            to_unit = const.VARS[var_name]['units']

        for i, meta in obj.metadata.items():
            if var_name in meta['var_info']:
                try:
                    unit = meta['var_info'][var_name]['units']
                except KeyError:
                    add_str = ''
                    if 'unit' in meta['var_info'][var_name]:
                        add_str = ('Corresponding var_info dict contains '
                                   'attr. "unit", which is deprecated, please '
                                   'check corresponding reading routine. ')
                    raise MetaDataError('Failed to access unit information for '
                                        'variable {} in metadata block {}. {}'
                                        .format(var_name, i, add_str))
                fac = get_unit_conversion_fac(unit, to_unit, var_name)
                if fac != 1:
                    meta_idx = obj.meta_idx[i][var_name]
                    current = obj._data[meta_idx, obj._DATAINDEX]
                    new = current * fac
                    obj._data[meta_idx, obj._DATAINDEX] = new
                    obj.metadata[i]['var_info'][var_name]['units'] = to_unit

        return obj

    def check_unit(self, var_name, unit=None):
        """Check if variable unit corresponds to AeroCom unit

        Parameters
        ----------
        var_name : str
            variable name for which unit is to be checked
        unit : :obj:`str`, optional
            unit to be checked, if None, AeroCom default unit is used

        Raises
        ------
        MetaDataError
            if unit information is not accessible for input variable name
        """
        if unit is None:
            unit = const.VARS[var_name]['units']

        units =  []
        for i, meta in self.metadata.items():
            if var_name in meta['var_info']:
                try:
                    u = meta['var_info'][var_name]['units']
                    if not u in units:
                        units.append(u)
                except KeyError:
                    add_str = ''
                    if 'unit' in meta['var_info'][var_name]:
                        add_str = ('Corresponding var_info dict contains '
                                   'attr. "unit", which is deprecated, please '
                                   'check corresponding reading routine. ')
                    raise MetaDataError('Failed to access unit information for '
                                        'variable {} in metadata block {}. {}'
                                        .format(var_name, i, add_str))
        if len(units) == 0 and str(unit) != '1':
            raise MetaDataError('Failed to access unit information for '
                                'variable {}. Expected unit {}'
                                .format(var_name, unit))
        for u in units:
            if not get_unit_conversion_fac(u, unit, var_name) == 1:
                raise MetaDataError(
                    f'Invalid unit {u} detected (expected {unit})')

    def set_flags_nan(self, inplace=False, verbose=False):
        """Set all flagged datapoints to NaN

        Parameters
        ----------
        inplace : bool
            if True, the flagged datapoints will be set to NaN in this object,
            otherwise a new oject will be created and returned

        Returns
        -------
        UngriddedData
            data object that has all flagged data values set to NaN

        Raises
        ------
        AttributeError
            if no flags are assigned
        """

        if not self.has_flag_data:
            raise AttributeError('Ungridded data object does not contain '
                                 'flagged data points')
        if inplace:
            obj = self
        else:
            obj = self.copy()
        mask = obj._data[:, obj._DATAFLAGINDEX] == 1

        obj._data[mask, obj._DATAINDEX] = np.nan
        obj._add_to_filter_history('set_flags_nan')
        return obj

    # TODO: check, confirm and remove Beta version note in docstring
    def remove_outliers(self, var_name, inplace=False, low=None, high=None,
                        unit_ref=None, move_to_trash=True):
        """Method that can be used to remove outliers from data

        Parameters
        ----------
        var_name : str
            variable name
        inplace : bool
            if True, the outliers will be removed in this object, otherwise
            a new oject will be created and returned
        low : float
            lower end of valid range for input variable. If None, then the
            corresponding value from the default settings for this variable
            are used (cf. minimum attribute of `available variables
            <https://pyaerocom.met.no/config_files.html#variables>`__)
        high : float
            upper end of valid range for input variable. If None, then the
            corresponding value from the default settings for this variable
            are used (cf. maximum attribute of `available variables
            <https://pyaerocom.met.no/config_files.html#variables>`__)
        unit_ref : str
            reference unit for assessment of input outlier ranges: all data
            needs to be in that unit, else an Exception will be raised
        move_to_trash : bool
            if True, then all detected outliers will be moved to the trash
            column of this data object (i.e. column no. specified at
            :attr:`UngriddedData._TRASHINDEX`).

        Returns
        -------
        UngriddedData
            ungridded data object that has all outliers for this variable
            removed.

        Raises
        ------
        ValueError
            if input :attr:`move_to_trash` is True and in case for some of the
            measurements there is already data in the trash.
        """
        if inplace:
            new = self
        else:
            new = self.copy()

        new.check_convert_var_units(var_name, to_unit=unit_ref)

        if low is None:
            low = const.VARS[var_name].minimum
            logger.info('Setting {} outlier lower lim: {:.2f}'.format(var_name, low))
        if high is None:
            high = const.VARS[var_name].maximum
            logger.info('Setting {} outlier upper lim: {:.2f}'.format(var_name, high))
        var_idx = new.var_idx[var_name]
        var_mask = new._data[:, new._VARINDEX] == var_idx

        all_data =  new._data[:, new._DATAINDEX]
        invalid_mask = np.logical_or(all_data<low, all_data>high)

        mask = invalid_mask * var_mask
        invalid_vals = new._data[mask, new._DATAINDEX]
        new._data[mask, new._DATAINDEX] = np.nan

        if move_to_trash:
            # check if trash is empty and put outliers into trash
            trash = new._data[mask, new._TRASHINDEX]
            if np.isnan(trash).sum() == len(trash): #trash is empty
                new._data[mask, new._TRASHINDEX] = invalid_vals
            else:
                raise ValueError('Trash is not empty for some of the datapoints. '
                                 'Please empty trash first using method '
                                 ':func:`empty_trash` or deactivate input arg '
                                 ':attr:`move_to_trash`')

        info = ('Removed {} outliers from {} data (range: {}-{}, in trash: {})'
                .format(len(invalid_vals), var_name, low, high, move_to_trash))

        new._add_to_filter_history(info)
        return new

    def _add_to_filter_history(self, info):
        """Add info to :attr:`filter_hist`

        Key is current system time string

        Parameter
        ---------
        info
            information to be appended to filter history
        """
        time_str = datetime.now().strftime('%Y%m%d%H%M%S')
        self.filter_hist[int(time_str)] = info

    def empty_trash(self):
        """Set all values in trash column to NaN"""
        self._data[:, self._TRASHINDEX] = np.nan

    @property
    def station_coordinates(self):
        """dictionary with station coordinates

        Returns
        -------
        dict
            dictionary containing station coordinates (latitude, longitude,
            altitude -> values) for all stations (keys) where these parameters
            are accessible.
        """
        d = {'station_name' : [],
             'latitude'     : [],
             'longitude'    : [],
             'altitude'     : []}

        for i, meta in self.metadata.items():
            if not 'station_name' in meta:
                print_log.warning('Skipping meta-block {}: station_name is not '
                                  'defined'.format(i))
                continue
            elif not all(name in meta for name in const.STANDARD_COORD_NAMES):
                print_log.warning('Skipping meta-block {} (station {}): '
                                  'one or more of the coordinates is not '
                                  'defined'.format(i, meta['station_name']))
                continue

            stat = meta['station_name']

            if stat in d['station_name']:
                continue
            d['station_name'].append(stat)
            for k in const.STANDARD_COORD_NAMES:
                d[k].append(meta[k])
        return d

    def _find_meta_matches(self, negate=None, *filters):
        """Find meta matches for input attributes

        Parameters
        ----------
        negate : list or str, optional
            specified meta key(s) provided in `*filters` that are
            supposed to be treated as 'not valid'. E.g. if
            `station_name="bad_site"` is input in `filter_attributes` and if
            `station_name` is listed in `negate`, then all metadata blocks
            containing "bad_site" as station_name will be excluded in output
            data object.
        *filters
            list of filters to be applied

        Returns
        -------
        tuple
            list of metadata indices that match input filter
        """
        if negate is None:
            negate = []
        elif isinstance(negate, str):
            negate = [negate]
        elif not isinstance(negate, list):
            raise ValueError(f'Invalid input for negate {negate}, '
                             f'need list or str or None')
        meta_matches = []
        totnum = 0
        for meta_idx, meta in self.metadata.items():
            if self._check_filter_match(meta,
                                        negate,
                                        *filters):
                meta_matches.append(meta_idx)
                for var in meta['var_info']:
                    try:
                        totnum += len(self.meta_idx[meta_idx][var])
                    except KeyError:
                        const.print_log.warning('Ignoring variable {} in '
                                             'meta block {} since no data '
                                             'could be found'.format(
                                              var, meta_idx))

        return (meta_matches, totnum)

    def filter_altitude(self, alt_range):
        """Filter altitude range

        Parameters
        ----------
        alt_range : list or tuple
            2-element list specifying altitude range to be filtered in m

        Returns
        -------
        UngriddedData
            filtered data object
        """
        return self.filter_by_meta(altitude=alt_range)

    def filter_region(self, region_id, check_mask=True,
                      check_country_meta=False, **kwargs):
        """Filter object by a certain region

        Parameters
        ----------
        region_id : str
            name of region (must be valid AeroCom region name or HTAP region)
        check_mask : bool
            if True and region_id a valid name for a binary mask, then the
            filtering is done based on that binary mask.
        check_country_meta : bool
            if True, then the input region_id is first checked against
            available country names in metadata. If that fails, it is assumed
            that this regions is either a valid name for registered rectangular
            regions or for available binary masks.
        **kwargs
            currently not used in method (makes usage in higher level classes
            such as :class:`Filter` easier as other data objects have the
            same method with possibly other input possibilities)

        Returns
        -------
        UngriddedData
            filtered data object (containing only stations that fall into
            input region)
        """
        if check_country_meta:
            if region_id in self.countries_available:
                return self.filter_by_meta(country=region_id)

        if region_id in const.HTAP_REGIONS and check_mask:
            return self.apply_region_mask(region_id)

        region = Region(region_id)
        return self.filter_by_meta(longitude=region.lon_range,
                                   latitude=region.lat_range)

    def apply_region_mask(self, region_id=None):
        """
        TODO : Write documentations

        Parameters
        ----------
        region_id : str or list (of strings)
            ID of region or IDs of multiple regions to be combined
        """
        if not region_id in const.HTAP_REGIONS:
            raise ValueError('Invalid input for region_id: {}, choose from: {}'
                             .format(region_id, const.HTAP_REGIONS))

        # 1. find matches -> list of meta indices that are in region
        # 2. Get total number of datapoints -> defines shape of output UngriddedData
        # 3. Create

        mask = load_region_mask_xr(region_id)

        meta_matches = []
        totnum = 0
        for meta_idx, meta in self.metadata.items():
            lon, lat = meta['longitude'], meta['latitude']

            mask_val = get_mask_value(lat, lon, mask)
            if mask_val >= 1: # coordinate is in mask
                meta_matches.append(meta_idx)
                for var in meta['var_info']:
                    totnum += len(self.meta_idx[meta_idx][var])

        new = self._new_from_meta_blocks(meta_matches, totnum)
        time_str = datetime.now().strftime('%Y%m%d%H%M%S')
        new.filter_hist[int(time_str)] = 'Applied mask {}'.format(region_id)
        new._check_index()
        return new

    def apply_filters(self, var_outlier_ranges=None, **filter_attributes):
        """Extended filtering method

        Combines :func:`filter_by_meta` and adds option to also remove outliers
        (keyword `remove_outliers`), set flagged data points to NaN (keyword
        `set_flags_nan`) and to extract individual variables (keyword
        `var_name`).

        Parameters
        ----------
        var_outlier_ranges : dict, optional
            dictionary specifying custom outlier ranges for individual
            variables.
        **filter_attributes : dict
            filters that are supposed to be applied to the data.
            To remove outliers, use keyword `remove_outliers`, to set flagged
            values to NaN, use keyword `set_flags_nan`, to extract single or
            multiple variables, use keyword `var_name`. Further filter keys
            are assumed to be metadata specific and are passed to
            :func:`filter_by_meta`.

        Returns
        -------
        UngriddedData
            filtered data object
        """
        data = self

        remove_outliers = False
        set_flags_nan = False
        extract_vars = None
        region_id = None
        if 'remove_outliers' in filter_attributes:
            remove_outliers = filter_attributes.pop('remove_outliers')
        if 'set_flags_nan' in filter_attributes:
            set_flags_nan = filter_attributes.pop('set_flags_nan')
        if 'var_name' in filter_attributes:
            extract_vars = filter_attributes.pop('var_name')
            if isinstance(extract_vars, str):
                extract_vars = [extract_vars]
            for var in extract_vars:
                if not var in data.contains_vars:
                    raise VarNotAvailableError('No such variable {} in '
                                               'UngriddedData object. '
                                               'Available vars: {}'
                                               .format(var, self.contains_vars))
        if 'region_id' in filter_attributes:
            region_id = filter_attributes.pop('region_id')

        if len(filter_attributes) > 0:
            data = data.filter_by_meta(**filter_attributes)

        if extract_vars is not None:
            data = data.extract_vars(extract_vars)

        if remove_outliers:
            if var_outlier_ranges is None:
                var_outlier_ranges = {}

            for var in data.contains_vars:
                lower, upper = None, None #uses pyaerocom default specified in variables.ini
                if var in var_outlier_ranges:
                    lower, upper = var_outlier_ranges[var]
                data = data.remove_outliers(var,
                                            inplace=True,
                                            low=lower,
                                            high=upper,
                                            move_to_trash=False)
        if set_flags_nan:
            if not data.has_flag_data:
                raise MetaDataError('Cannot apply filter "set_flags_nan" to '
                                    'UngriddedData object, since it does not '
                                    'contain flag information')
            data = data.set_flags_nan(inplace=True)
        if region_id:
            data = data.filter_region(region_id)
        return data

    def filter_by_meta(self, negate=None, **filter_attributes):
        """Flexible method to filter these data based on input meta specs

        Parameters
        ----------
        negate : list or str, optional
            specified meta key(s) provided via `filter_attributes` that are
            supposed to be treated as 'not valid'. E.g. if
            `station_name="bad_site"` is input in `filter_attributes` and if
            `station_name` is listed in `negate`, then all metadata blocks
            containing "bad_site" as station_name will be excluded in output
            data object.
        **filter_attributes
            valid meta keywords that are supposed to be filtered and the
            corresponding filter values (or value ranges)
            Only valid meta keywords are considered (e.g. data_id,
            longitude, latitude, altitude, ts_type)

        Returns
        -------
        UngriddedData
            filtered ungridded data object

        Raises
        ------
        NotImplementedError
            if attempt variables are supposed to be filtered (not yet possible)
        IOError
            if any of the input keys are not valid meta key

        Example
        -------
        >>> import pyaerocom as pya
        >>> r = pya.io.ReadUngridded(['AeronetSunV2Lev2.daily',
                                      'AeronetSunV3Lev2.daily'], 'od550aer')
        >>> data = r.read()
        >>> data_filtered = data.filter_by_meta(data_id='AeronetSunV2Lev2.daily',
        ...                                     longitude=[-30, 30],
        ...                                     latitude=[20, 70],
        ...                                     altitude=[0, 1000])
        """

        if 'variables' in filter_attributes:
            raise NotImplementedError('Cannot yet filter by variables')

        # separate filters by strin, list, etc.
        filters = self._init_meta_filters(**filter_attributes)

        # find all metadata blocks that match the filters
        meta_matches, totnum_new = self._find_meta_matches(negate,
                                                           *filters,
                                                           )
        if len(meta_matches) == len(self.metadata):
            const.logger.info('Input filters {} result in unchanged data '
                              'object'.format(filter_attributes))
            return self
        new = self._new_from_meta_blocks(meta_matches, totnum_new)
        time_str = datetime.now().strftime('%Y%m%d%H%M%S')
        new.filter_hist[int(time_str)] = filter_attributes
        return new

    def _new_from_meta_blocks(self, meta_indices, totnum_new):
        # make a new empty object with the right size (totnum_new)

        new = UngriddedData(num_points=totnum_new)

        meta_idx_new = 0.0
        data_idx_new = 0

        # loop over old meta_idx and extract data and create new meta_idx in
        # output data object
        for meta_idx in meta_indices:
            meta = self.metadata[meta_idx]
            new.metadata[meta_idx_new] = meta
            new.meta_idx[meta_idx_new] = od()
            for var in meta['var_info']:
                indices = self.meta_idx[meta_idx][var]
                totnum = len(indices)

                stop = data_idx_new + totnum

                new._data[data_idx_new:stop, :] = self._data[indices, :]
                new.meta_idx[meta_idx_new][var] = np.arange(data_idx_new,
                                                            stop)
                new.var_idx[var] = self.var_idx[var]
                data_idx_new += totnum

            meta_idx_new += 1

        if meta_idx_new == 0 or data_idx_new == 0:
            raise DataExtractionError('Filtering results in empty data object')
        new._data = new._data[:data_idx_new]

        # write history of filtering applied
        new.filter_hist.update(self.filter_hist)
        new.data_revision.update(self.data_revision)

        return new

    def clear_meta_no_data(self, inplace=True):
        """Remove all metadata blocks that do not have data associated with it

        Parameters
        ----------
        inplace : bool
            if True, the changes are applied to this instance directly, else
            to a copy

        Returns
        -------
        UngriddedData
            cleaned up data object

        Raises
        ------
        DataCoverageError
            if filtering results in empty data object
        """
        if inplace:
            obj = self
        else:
            obj = self.copy()
        meta_new = od()
        meta_idx_new = od()
        for idx, val in obj.meta_idx.items():
            meta = obj.metadata[idx]
            if not bool(val): # no data assigned with this metadata block
                # sanity check
                if bool(meta['var_info']):
                    raise AttributeError('meta_idx {} suggests empty data block '
                                         'but metadata[{}] contains variable '
                                         'information')
            else:
                meta_new[idx] = meta
                meta_idx_new[idx] = val
        num_removed = len(obj.metadata) - len(meta_new)
        if not bool(meta_new):
            raise DataCoverageError('UngriddedData object appears to be empty')
        elif num_removed > 0: # some meta blocks are empty
            obj.metadata = meta_new
            obj.meta_idx = meta_idx_new

        obj._add_to_filter_history('Removed {} metadata blocks that have no '
                                   'data assigned'.format(num_removed))
        obj._check_index()
        return obj

    def extract_dataset(self, data_id):
        """Extract single dataset into new instance of :class:`UngriddedData`

        Calls :func:`filter_by_meta`.

        Parameters
        -----------
        data_id : str
            ID of dataset

        Returns
        -------
        UngriddedData
            new instance of ungridded data containing only data from specified
            input network
        """
        logger.info('Extracting dataset {} from data object'.format(data_id))
        return self.filter_by_meta(data_id=data_id)

    def extract_var(self, var_name, check_index=True):
        """Split this object into single-var UngriddedData objects

        Parameters
        ----------
        var_name : str
            name of variable that is supposed to be extracted
        check_index : Bool
            Call :func:`_check_index` in the new data object.

        Returns
        -------
        UngriddedData
            new data object containing only input variable data
        """
        if not var_name in self.contains_vars:
            # try alias
            _var = const.VARS[var_name].var_name_aerocom
            if _var in self.contains_vars:
                var_name = _var
            else:
                raise VarNotAvailableError('No such variable {} in data'
                                           .format(var_name))
        elif len(self.contains_vars) == 1:
            const.print_log.info('Data object is already single variable. '
                                 'Returning copy')
            return self.copy()

        var_idx = self.var_idx[var_name]

        totnum = np.sum(self._data[:, self._VARINDEX] == var_idx)

        colnum, rownum = self.shape

        if rownum != len(self._init_index()):
            raise NotImplementedError('Cannot split UngriddedData objects that have '
                                      'additional columns other than default columns')

        subset = UngriddedData(totnum)

        subset.var_idx[var_name] = 0
        subset._index = self.index

        meta_idx = -1
        arr_idx = 0

        for midx, didx in self.meta_idx.items():
            if var_name in didx and len(didx[var_name]) > 0:
                meta_idx += 1
                meta =  {}
                _meta = self.metadata[midx]
                meta.update(_meta)
                meta['var_info'] = od()
                meta['var_info'][var_name] = _meta['var_info'][var_name]
                meta['variables'] = [var_name]
                subset.metadata[meta_idx] = meta

                idx = didx[var_name]

                subset.meta_idx[meta_idx] = {}

                num_add = len(idx)
                start = arr_idx
                stop = arr_idx + num_add
                subset.meta_idx[meta_idx][var_name] = np.arange(start, stop)

                subset._data[start:stop] = self._data[idx]
                subset._data[start:stop, subset._METADATAKEYINDEX] = meta_idx
                subset._data[start:stop, subset._VARINDEX] = 0

                arr_idx += num_add

        if check_index:
            subset._check_index()
        subset.filter_hist.update(self.filter_hist)
        subset._add_to_filter_history('Created {} single var object from '
                                      'multivar UngriddedData instance'
                                      .format(var_name))
        return subset

    def extract_vars(self, var_names, check_index=True):
        """Extract multiple variables from dataset

        Loops over input variable names and calls :func:`extract_var` to
        retrieve single variable UngriddedData objects for each variable and
        then merges all of these into one object

        Parameters
        ----------
        var_names : list or str
            list of variables to be extracted
        check_index : Bool
            Call :func:`_check_index` in the new data object.

        Returns
        -------
        UngriddedData
            new data object containing input variables

        Raises
        -------
        VarNotAvailableError
            if one of the input variables is not available in this data
            object
        """
        if isinstance(var_names, str):
            return self.extract_var(var_names)
        data = UngriddedData()

        for var in var_names:
            data.append(self.extract_var(var, check_index=False))
        if check_index:
            data._check_index()
        return data

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

    def _find_common_meta(self, ignore_keys=None):
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
        if ignore_keys is None:
            ignore_keys = []
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

        return same_indices


    def merge_common_meta(self, ignore_keys=None):
        """Merge all meta entries that are the same

        Note
        ----
        If there is an overlap in time between the data, the blocks are not
        merged

        Todo
        ----
        Keep mapping of ``var_info`` (if defined in ``metadata``) to data
        points (e.g. EBAS), since the data sources may be at different
        wavelengths.

        Parameters
        ----------
        ignore_keys : list
            list containing meta keys that are supposed to be ignored

        Returns
        -------
        UngriddedData
            merged data object
        """
        if ignore_keys is None:
            ignore_keys = []
        sh = self.shape
        lst_meta_idx = self._find_common_meta(ignore_keys)
        new = UngriddedData(num_points=self.shape[0])
        didx = 0
        for i, idx_lst in enumerate(lst_meta_idx):
            _meta_check = od()
            # write metadata of first index that matches
            _meta_check.update(self.metadata[idx_lst[0]])
            _meta_idx_new = od()
            for j, meta_idx in enumerate(idx_lst):
                if j > 0: # don't check first against first
                    meta = self.metadata[meta_idx]
                    merged = merge_dicts(meta, _meta_check)
                    for key in ignore_keys:
                        _meta_check[key] = merged[key]

                data_var_idx = self.meta_idx[meta_idx]
                for var, data_idx in data_var_idx.items():
                    num = len(data_idx)
                    stop = didx + num
                    new._data[didx:stop, :] = self._data[data_idx]
                    new._data[didx:stop, 0] = i
                    if not var in _meta_idx_new:
                        _meta_idx_new[var] = np.arange(didx, stop)
                    else:
                        _idx = np.append(_meta_idx_new[var], np.arange(didx, stop))
                        _meta_idx_new[var] = _idx
                    didx += num

            new.meta_idx[i] = _meta_idx_new
            new.metadata[i] = _meta_check
        new.var_idx.update(self.var_idx)
        new.filter_hist.update(self.filter_hist)
        if not new.shape == sh:
            raise Exception('FATAL: Mismatch in shape between initial and '
                            'and final object. Developers: please check')
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
            obj = self.copy()
        else:
            obj = self

        if obj.is_empty:
            obj._data = other._data
            obj.metadata = other.metadata
            #obj.unit = other.unit
            obj.data_revision = other.data_revision
            obj.meta_idx = other.meta_idx
            obj.var_idx = other.var_idx
        else:
            # get offset in metadata index
            meta_offset = max([x for x in obj.metadata.keys()]) + 1
            data_offset = obj.shape[0]

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
        obj.filter_hist.update(other.filter_hist)
        obj._check_index()
        return obj

    def colocate_vardata(self, var1, data_id1=None,
                         var2=None, data_id2=None, other=None,
                         **kwargs):
        if other is None:
            other = self
        if var2 is None:
            var2 = var1
        if data_id1 is None:
            contains = self.contains_datasets
            if len(contains) > 1:
                raise ValueError('Please provide data_id1 since data object '
                                 'contains more than 1 dataset...')
            data_id1 = contains[0]

        if data_id2 is None:
            contains = other.contains_datasets
            if len(contains) > 1:
                raise ValueError('Please provide data_id2 since data object '
                                 'contains more than 1 dataset...')
            data_id2 = contains[0]
        if self is other and data_id1 == data_id2 and var1 == var2:
            raise ValueError('Input combination too unspecific, please provide '
                             'either another data object, 2 different data IDs '
                             'or 2 different variable names')
        input_data = [(self, data_id1, var1),
                      (other, data_id2, var2)]
        statlist = combine_vardata_ungridded(input_data,
                                             **kwargs)

        new = UngriddedData.from_station_data(statlist)
        return new

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
        raise NotImplementedError('Coming soon')

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
                                                       meta['data_id']))
                            ok = False
                    except Exception: # attribute does not exist or is not iterable
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
                                                     meta_other['data_id']))
                                        ok = False
                                except Exception: # attribute does not exist or is not iterable
                                    ok = False
                        if ok and check_coordinates:
                            dlat = abs(meta['latitude']-meta_other['latitude'])
                            dlon = abs(meta['longitude']-meta_other['longitude'])
                            lon_fac = np.cos(np.deg2rad(meta['latitude']))
                            #compute distance between both station coords
                            dist = np.linalg.norm((dlat*lat_len,
                                                   dlon*lat_len*lon_fac))
                            if dist > max_diff_coords_km:
                                logger.warning('Coordinate of station '
                                               '{} varies more than {} km '
                                               'between {} and {} data. '
                                               'Retrieved distance: {:.2f} km '
                                               .format(name, max_diff_coords_km,
                                                       meta['data_id'],
                                                       meta_other['data_id'],
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

    def _meta_to_lists(self):
        meta = {k:[] for k in self.metadata[self.first_meta_idx].keys()}
        for meta_item in self.metadata.values():
            for k, v in meta.items():
                v.append(meta_item[k])
        return meta

    def get_timeseries(self, station_name, var_name, start=None, stop=None,
                      ts_type=None, insert_nans=True, **kwargs):
        """Get variable timeseries data for a certain station

        Parameters
        ----------
        station_name : :obj:`str` or :obj:`int`
            station name or index of station in metadata dict
        var_name : str
            name of variable to be retrieved
        start
            start time (optional)
        stop
            stop time (optional). If start time is provided and stop time not,
            then only the corresponding year inferred from start time will be
            considered
        ts_type : :obj:`str`, optional
            temporal resolution (can be pyaerocom ts_type or pandas freq.
            string)
        **kwargs
            Additional keyword args passed to method :func:`to_station_data`

        Returns
        -------
        pandas.Series
            time series data
        """
        if 'merge_if_multi' in kwargs:
            if not kwargs.pop['merge_if_multi']:
                print_log.warning('Invalid input merge_if_multi=False'
                                  'setting it to True')
        stat = self.to_station_data(station_name, var_name, start, stop,
                                    freq=ts_type, merge_if_multi=True,
                                    insert_nans=insert_nans,
                                    **kwargs)
        return stat.to_timeseries(var_name)

    def plot_station_timeseries(self, station_name, var_name, start=None,
                                stop=None, ts_type=None,
                                insert_nans=True, ax=None, **kwargs):
        """Plot time series of station and variable

        Parameters
        ----------
        station_name : :obj:`str` or :obj:`int`
            station name or index of station in metadata dict
        var_name : str
            name of variable to be retrieved
        start
            start time (optional)
        stop
            stop time (optional). If start time is provided and stop time not,
            then only the corresponding year inferred from start time will be
            considered
        ts_type : :obj:`str`, optional
            temporal resolution

        **kwargs
            Addifional keyword args passed to method :func:`pandas.Series.plot`

        Returns
        -------
        axes
            matplotlib axes instance

        """
        if ax is None:
            from pyaerocom.plot.config import FIGSIZE_DEFAULT
            fig, ax = plt.subplots(figsize=FIGSIZE_DEFAULT)

        stat = self.to_station_data(station_name, var_name, start, stop,
                                    freq=ts_type, merge_if_multi=True,
                                    insert_nans=insert_nans)
        #s = self.get_timeseries(station_name, var_name, start, stop, ts_type)
        #s.plot(ax=ax, **kwargs)
        ax = stat.plot_timeseries(var_name, ax=ax, **kwargs)
        return ax

    def plot_station_coordinates(self, var_name=None,
                                 start=None,
                                 stop=None, ts_type=None, color='r',
                                 marker='o', markersize=8, fontsize_base=10,
                                 legend=True, add_title=True,
                                 **kwargs):
        """Plot station coordinates on a map

        All input parameters are optional and may be used to add constraints
        related to which stations are plotted. Default is all stations of all
        times.

        Parameters
        ----------

        var_name : :obj:`str`, optional
            name of variable to be retrieved
        start
            start time (optional)
        stop
            stop time (optional). If start time is provided and stop time not,
            then only the corresponding year inferred from start time will be
            considered
        ts_type : :obj:`str`, optional
            temporal resolution
        color : str
            color of stations on map
        marker : str
            marker type of stations
        markersize : int
            size of station markers
        fontsize_base : int
            basic fontsize
        legend : bool
            if True, legend is added
        add_title : bool
            if True, title will be added
        **kwargs
            Addifional keyword args passed to
            :func:`pyaerocom.plot.plot_coordinates`

        Returns
        -------
        axes
            matplotlib axes instance

        """
        from pyaerocom.plot.plotcoordinates import plot_coordinates

        if len(self.contains_datasets) > 1:
            print_log.warning('UngriddedData object contains more than one '
                              'dataset ({}). Station coordinates will not be '
                              'distinguishable. You may want to apply a filter '
                              'first and plot them separately')

        subset = self
        if var_name is None:
            info_str = 'AllVars'
        else:
            if not isinstance(var_name, str):
                raise ValueError('Can only handle single variable (or all'
                                 '-> input var_name=None)')
            elif not var_name in subset.contains_vars:
                raise ValueError('Input variable {} is not available in dataset '
                                 .format(var_name))
            info_str = var_name

        try:
            info_str += '_{}'.format(start_stop_str(start, stop, ts_type))
        except Exception:
            info_str += '_AllTimes'
        if ts_type is not None:
            info_str += '_{}'.format(ts_type)

        if all([x is None for x in (var_name, start, stop)]): #use all stations
            all_meta = subset._meta_to_lists()
            lons, lats = all_meta['longitude'], all_meta['latitude']

        else:
            stat_data = subset.to_station_data_all(var_name, start, stop,
                                                 ts_type)

            if len(stat_data['stats']) == 0:
                raise DataCoverageError('No stations could be found for input '
                                        'specs (var, start, stop, freq)')
            lons = stat_data['longitude']
            lats = stat_data['latitude']
        if not 'label' in kwargs:
            kwargs['label'] = info_str

        ax = plot_coordinates(lons, lats,
                              color=color, marker=marker,
                              markersize=markersize,
                              legend=legend,
                              fontsize_base=fontsize_base, **kwargs)

        if 'title' in kwargs:
            title = kwargs['title']
        else:
            title = info_str
        if add_title:
            ax.set_title(title, fontsize=fontsize_base+4)
        return ax

    def save_as(self, file_name, save_dir):
        """
        Save this object to disk

        Note
        ----
        So far, only storage as pickled object via
        `CacheHandlerUngridded` is supported, so input file_name must end
        with .pkl

        Parameters
        ----------
        file_name : str
            name of output file
        save_dir : str
            name of output directory

        Returns
        -------
        str
            file path

        """
        from pyaerocom.io.cachehandler_ungridded import CacheHandlerUngridded

        if not os.path.exists(save_dir):
            raise FileNotFoundError('Directory does not exist: {}'.format(save_dir))
        elif not file_name.endswith('.pkl'):
            raise ValueError('Can only store files as pickle, file_name needs '
                             'to have format .pkl')
        ch = CacheHandlerUngridded()
        return ch.write(self, var_or_file_name=file_name,
                        cache_dir=save_dir)

    @staticmethod
    def from_cache(data_dir, file_name):
        """
        Load pickled instance of `UngriddedData`

        Parameters
        ----------
        data_dir : str
            directory where pickled object is stored
        file_name : str
            file name of pickled object (needs to end with pkl)

        Raises
        ------
        ValueError
            if loading failed

        Returns
        -------
        UngriddedData
            loaded UngriddedData object. If this method is called from an
            instance of `UngriddedData`, this instance remains unchanged.
            You may merge the returned reloaded instance using
            :func:`merge`.

        """
        from pyaerocom.io.cachehandler_ungridded import CacheHandlerUngridded
        ch = CacheHandlerUngridded()
        if ch.check_and_load(file_name, cache_dir=data_dir):
            return ch.loaded_data[file_name]
        raise ValueError('Failed to load UngriddedData object')

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

    def __iter__(self):
        return self

    #: ToDo revise cases of DataCoverageError
    def __next__(self):
        self._idx += 1
        if self._idx == len(self.metadata):
            self._idx = -1
            raise StopIteration
        try:
            return self[self._idx]
        except DataCoverageError:
            const.print_log.warning('No variable data in metadata block {}. '
                                    'Returning empty StationData'
                                    .format(self._idx))
            return StationData()

    def __repr__(self):
        return ('{} <networks: {}; vars: {}; instruments: {};'
                'No. of metadata units: {}'
                .format(type(self).__name__,self.contains_datasets,
                        self.contains_vars, self.contains_instruments,
                        len(self.metadata)))

    def __getitem__(self, key):
        if isnumeric(key) or key in self.unique_station_names:
            return self.to_station_data(key, insert_nans=True)
        raise KeyError('Invalid input key, need metadata index or station name ')

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
              '\nTotal no. of meta-blocks: {}'.format(self.contains_datasets,
                                                   self.contains_vars,
                                                   self.contains_instruments,
                                                   len(self.metadata)))
        if self.is_filtered:
            s += '\nFilters that were applied:'
            for tstamp, f in self.filter_hist.items():
                if f:
                    s += '\n Filter time log: {}'.format(tstamp)
                    if isinstance(f, dict):
                        for key, val in f.items():
                            s += '\n\t{}: {}'.format(key, val)
                    else:
                        s += '\n\t{}'.format(f)

        return s

    # DEPRECATED METHODS
    @property
    def vars_to_retrieve(self):
        logger.warning(DeprecationWarning("Attribute vars_to_retrieve is "
                                          "deprecated. Please use attr "
                                          "contains_vars instead"))
        return self.contains_vars

    def get_time_series(self, station, var_name, start=None, stop=None,
                        ts_type=None, **kwargs):
        """Get time series of station variable

        Parameters
        ----------
        station : :obj:`str` or :obj:`int`
            station name or index of station in metadata dict
        var_name : str
            name of variable to be retrieved
        start
            start time (optional)
        stop
            stop time (optional). If start time is provided and stop time not,
            then only the corresponding year inferred from start time will be
            considered
        ts_type : :obj:`str`, optional
            temporal resolution
        **kwargs
            Additional keyword args passed to method :func:`to_station_data`

        Returns
        -------
        pandas.Series
            time series data
        """
        logger.warning(DeprecationWarning('Outdated method, please use to_timeseries'))

        data = self.to_station_data(station, var_name,
                                     start, stop, freq=ts_type,
                                     **kwargs)
        if not isinstance(data, StationData):
            raise NotImplementedError('Multiple matches found for {}. Cannot '
                                      'yet merge multiple instances '
                                      'of StationData into one single '
                                      'timeseries. Coming soon...'.format(station))
        return data.to_timeseries(var_name)

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
        msg = ('This method name is deprecated, please use to_timeseries')
        warn(DeprecationWarning(msg))

        if station_name is None:
            stats = self.to_station_data_all(start=start_date, stop=end_date,
                                             freq=freq)
            stats['stats']
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

def reduce_array_closest(arr_nominal, arr_to_be_reduced):
    test = sorted(arr_to_be_reduced)
    closest_idx = []
    for num in sorted(arr_nominal):
        idx = np.argmin(abs(test - num))
        closest_idx.append(idx)
        test = test[(idx+1):]
    return closest_idx

if __name__ == "__main__":
    import pyaerocom as pya
    import matplotlib.pyplot as plt

    OBS_LOCAL = '/home/jonasg/MyPyaerocom/data/obsdata/'

    GHOST_EEA_LOCAL = os.path.join(OBS_LOCAL, 'GHOST/data/EEA_AQ_eReporting/daily')

    data = pya.io.ReadUngridded('GHOST.EEA.daily',
                                data_dir=GHOST_EEA_LOCAL).read(vars_to_retrieve='vmro3')



