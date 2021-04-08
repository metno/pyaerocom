#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from copy import deepcopy
from collections import OrderedDict as od

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xray
from pyaerocom import logger, const

from pyaerocom.exceptions import (MetaDataError, VarNotAvailableError,
                                  DataCoverageError,
                                  DataExtractionError, DataDimensionError,
                                  UnitConversionError, DataUnitError,
                                  TemporalResolutionError)
from pyaerocom._lowlevel_helpers import (dict_to_str, list_to_shortstr,
                                         BrowseDict, merge_dicts)
from pyaerocom.metastandards import StationMetaData, STANDARD_META_KEYS
from pyaerocom.vertical_profile import VerticalProfile
from pyaerocom.tstype import TsType
from pyaerocom.time_resampler import TimeResampler
from pyaerocom.trends_engine import TrendsEngine
from pyaerocom.trends_helpers import _make_mobs_dataframe
from pyaerocom.helpers import (isnumeric, isrange, calc_climatology,
                               to_datetime64)

from pyaerocom.units_helpers import convert_unit, get_unit_conversion_fac
from pyaerocom.time_config import PANDAS_FREQ_TO_TS_TYPE

class StationData(StationMetaData):
    """Dict-like base class for single station data

    ToDo: write more detailed introduction

    Note
    ----
    Variable data (e.g. numpy array or pandas Series) can be directly
    assigned to the object. When  assigning variable data it is
    recommended to add variable metadata (e.g. unit, ts_type)
    in :attr:`var_info`, where key is variable name and value is dict with
    metadata entries.

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
    STANDARD_META_KEYS = STANDARD_META_KEYS

    VALID_TS_TYPES = const.GRID_IO.TS_TYPES

    #: Keys that are ignored when accessing metadata
    PROTECTED_KEYS = ['dtime','var_info', 'station_coords', 'data_err',
                      'overlap', 'numobs','data_flagged']
    def __init__(self, **meta_info):

        self.dtime = []

        self.var_info = BrowseDict()

        self.station_coords = dict.fromkeys(self.STANDARD_COORD_KEYS)

        self.data_err = BrowseDict()
        self.overlap = BrowseDict()
        self.numobs = BrowseDict()
        self.data_flagged = BrowseDict()

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

    @property
    def vars_available(self):
        """Number of variables available in this data object"""
        return list(self.var_info.keys())

    def has_var(self, var_name):
        """Checks if input variable is available in data object

        Parameters
        ----------
        var_name : str
            name of variable

        Returns
        -------
        bool
            True, if variable data is available, else False
        """
        if not var_name in self:
            return False
        if not var_name in self.var_info:
            const.print_log.warning('Variable {} exists in data but has no '
                                    'metadata assigned in :attr:`var_info`'
                                    .format(var_name))
        return True

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
        if not var_name in self.var_info:
            raise MetaDataError('Could not access variable metadata dict '
                                'for {}.'.format(var_name))
        try:
            return str(self.var_info[var_name]['units'])
        except KeyError:
            add_str = ''
            if 'unit' in self.var_info[var_name]:
                add_str = ('Corresponding var_info dict contains '
                           'attr. "unit", which is deprecated, please '
                           'check corresponding reading routine. ')
            raise MetaDataError('Failed to access units attribute for variable '
                                '{}. {}'.format(var_name, add_str))

    @property
    def units(self):
        """Dictionary containing units of all variables in this object"""
        ud = {}
        for var in self.var_info:
            ud[var] = self.get_unit(var)
        return ud

    def compute_trend(self, var_name, start_year=None, stop_year=None,
                      season=None, slope_confidence=None, **alt_range):
        if not self.has_var(var_name):
            raise VarNotAvailableError('No such variables {} in StationData'
                                       .format(var_name))
        #from pyaerocom.trends_helpers import compute_trends_station
        return compute_trends_station(self, var_name, start_year, stop_year,
                                      season, slope_confidence, **alt_range)

    def check_var_unit_aerocom(self, var_name):
        """Check if unit of input variable is AeroCom default, if not, convert

        Parameters
        ----------
        var_name : str
            name of variable

        Raises
        ------
        MetaDataError
            if unit information is not accessible for input variable name
        UnitConversionError
            if current unit cannot be converted into specified unit
            (e.g. 1 vs m-1)
        DataUnitError
            if current unit is not equal to AeroCom default and cannot
            be converted.
        """
        to_unit = const.VARS[var_name].units
        try:
            self.check_unit(var_name, to_unit)
        except Exception:
            try:
                self.convert_unit(var_name, to_unit)
            except UnitConversionError as e:
                raise UnitConversionError('Failed to convert unit of variable '
                                          '{}. Reason: {}'
                                          .format(var_name, repr(e)))

    def check_unit(self, var_name, unit=None):
        """Check if variable unit corresponds to a certain unit

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
        UnitConversionError
            if current unit cannot be converted into specified unit
            (e.g. 1 vs m-1)
        DataUnitError
            if current unit is not equal to input unit but can be converted
            (e.g. 1/Mm vs 1/m)
        """
        if unit is None:
            unit = const.VARS[var_name].units
        u = self.get_unit(var_name)
        if not get_unit_conversion_fac(u, unit, var_name) == 1:
            raise DataUnitError(f'Invalid unit {u} (expected {unit})')

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

        data = self[var_name]
        data = convert_unit(data, from_unit=unit, to_unit=to_unit,
                            var_name=var_name)

        self[var_name] = data
        self.var_info[var_name]['units'] = to_unit
        const.logger.info('Successfully converted unit of variable {} in {} '
                          'from {} to {}'.format(var_name, self.station_name,
                                                 unit, to_unit))

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

        Parameters
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
                    raise MetaDataError('{} information is not available in data'
                                        .format(key))
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
        return vals

    def get_meta(self, force_single_value=True, quality_check=True,
                 add_none_vals=False, add_meta_keys=None):
        """Return meta-data as dictionary

        By default, only default metadata keys are considered, use parameter
        `add_meta_keys` to add additional metadata.

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
        add_none_vals : bool
            Add metadata keys which have value set to None.
        add_meta_keys : str or list, optional
            Add none-standard metadata.

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
        if isinstance(add_meta_keys, str):
            add_meta_keys = [add_meta_keys]
        elif not isinstance(add_meta_keys, list):
            add_meta_keys = []
        meta = {}
        meta.update(self.get_station_coords(force_single_value,
                                            quality_check))
        keys = self.STANDARD_META_KEYS
        keys.extend(add_meta_keys)
        for key in keys:
            if not key in self:
                const.print_log.warning('No such key in StationData: {}'
                                     .format(key))
                continue
            elif key in self.PROTECTED_KEYS:
                # this is not metadata...
                continue
            elif key in self.STANDARD_COORD_KEYS:
                # this has been handled above
                continue
            if self[key] is None and not add_none_vals:
                logger.info('No metadata available for key {}'.format(key))
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

    def _check_meta_item(self, key):
        """Check if metadata item is valid

        Valid value types are dictionaries, lists, strings, numerical values
        and datetetime objects.
        """
        val = self[key]
        if val is None:
            return
        elif isinstance(val, np.ndarray):
            if val.ndim != 1:
                raise MetaDataError('Invalid metadata entry {} for key {}.'
                                    'Only 1d numpy arrays are supported...'
                                    .format(val, key))
            self[key] = list(val)
        elif not isinstance(val, (dict, list, str)) and not isnumeric(val):
            try:
                self[key] = to_datetime64(val)
            except Exception:
                raise MetaDataError('Invalid metadata entry {} for key {}.'
                                    'Only dicts, lists, strings, numerical '
                                    'values or datetime objects are supported'
                                    .format(val, key))

    def _merge_meta_item(self, key, val):
        """Merge meta item into this object

        Parameters
        ----------
        key
            key of metadata value
        val
            value to be added
        """
        current_val = self[key]
        same_type = isinstance(current_val, type(val))
        try:
            if isinstance(current_val, dict):
                if not same_type:
                    raise ValueError('Cannot merge meta item {} due to type '
                                     'mismatch'.format(key))
                elif not current_val == val:
                    self[key] = merge_dicts(current_val, val)

            elif isinstance(current_val, str):
                if not same_type:
                    if isinstance(val, list):
                        if not current_val in val:
                            newval = val.insert(0, current_val)
                        self[key] = newval
                    else:
                        raise ValueError('Cannot merge meta item {} due to type '
                                         'mismatch'.format(key))
                elif not current_val == val:
                    # both are str that may be already merged with ";" -> only
                    # add new entries
                    vals_in = [x.strip() for x in val.split(';')]

                    for item in vals_in:
                        if not item in current_val:
                            current_val += ';{}'.format(item)
                    self[key] = current_val

            elif isinstance(current_val, list):
                if not same_type:
                    val = [val]
                for item in val:
                    if not item in current_val:
                        current_val.append(item)
                self[key] = current_val

            elif isnumeric(current_val) and isnumeric(val):
                if np.isnan(current_val) and np.isnan(val):
                    self[key] = val
                elif val != current_val:
                    self[key] = [current_val, val]

            elif isinstance(val, list):
                if not current_val in val:
                    self[key] = val.insert(0, current_val)

            elif current_val != val:
                self[key] = [current_val, val]

            else: #they shoul be the same
                assert current_val == val, (current_val, val)
        except Exception as e:
            raise MetaDataError('Failed to merge metadata entries for key {}.\n'
                                'Value in current StationData: {}\n'
                                'Value to be merged: {}\n'
                                'Error: {}'
                                .format(key, current_val, val, repr(e)))



    def _append_meta_item(self, key, val):
        """Add a metadata item"""
        if not key in self or self[key] is None:
            self[key] = val
        else:
            self._merge_meta_item(key, val)

    def merge_meta_same_station(self, other, coord_tol_km=None,
                                check_coords=True, inplace=True,
                                add_meta_keys=None, raise_on_error=False):
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
        add_meta_keys : str or list, optional
            additional non-standard metadata keys that are supposed to be
            considered for merging.
        raise_on_error : bool
            if True, then an Exception will be raised in case one of the
            metadata items cannot be merged, which is most often due to
            unresolvable type differences of metadata values between the two
            objects

        """
        if add_meta_keys is None:
            add_meta_keys = []

        elif isinstance(add_meta_keys, str):
            add_meta_keys = [add_meta_keys]

        if not inplace:
            obj = self.copy()
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
        for key in keys:
            if key in self.STANDARD_COORD_KEYS:
                if self[key] is None and other[key] is not None:
                    self[key] = other[key]
            elif key in self.PROTECTED_KEYS:
                continue
            elif key in other and other[key] is not None:
                try:
                    self._check_meta_item(key)
                    other._check_meta_item(key)

                    obj._append_meta_item(key, other[key])
                except MetaDataError as e:
                    obj[key] = 'N/A_FAILED_TO_MERGE'
                    msg = ('Failed to merge meta item {}. Reason:{}'
                           .format(key, repr(e)))
                    if raise_on_error:
                        raise MetaDataError(msg)
                    else:
                        const.print_log.warning(msg)

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

    def _ensure_same_var_ts_type_other(self, other, var_name):
        ts_type = self.get_var_ts_type(var_name)
        ts_type1 = other.get_var_ts_type(var_name)
        if ts_type != ts_type1:
            # make sure each variable in the object has explicitely ts_type
            # assigned (rather than global specification)

            self._update_var_timeinfo()
            other._update_var_timeinfo()

            from pyaerocom.helpers import get_lowest_resolution
            ts_type = get_lowest_resolution(ts_type, ts_type1)
        return ts_type

    def _update_var_timeinfo(self):

        for var, info in self.var_info.items():
            data = self[var]
            if not isinstance(data, pd.Series):
                try:
                    self[var] = pd.Series(data, self.dtime)
                except Exception as e:
                    raise Exception('Unexpected error: {}.\nPlease debug...'
                                    .format(repr(e)))
            if not 'ts_type' in info or info['ts_type'] is None:
                if not self.ts_type in const.GRID_IO.TS_TYPES:
                    raise ValueError('Cannot identify ts_type for var {} '
                                     'in {}'.format(var, self))
                info['ts_type'] = self.ts_type
        self.ts_type = None

    def _merge_vardata_2d(self, other, var_name):
        """Merge 2D variable data (for details see :func:`merge_vardata`)"""
        ts_type = self._ensure_same_var_ts_type_other(other, var_name)

        s0 = self.resample_time(var_name, ts_type=ts_type,
                                inplace=True)[var_name].dropna()
        s1 = other.resample_time(var_name, inplace=True,
                                 ts_type=ts_type)[var_name].dropna()

        info = other.var_info[var_name]
        removed = None
        if 'overlap' in info and info['overlap']:
            raise NotImplementedError('Coming soon...')

        if len(s1) > 0: #there is data
            overlap = s0.index.intersection(s1.index)
            if len(overlap) > 0:
                removed = s1[overlap]
                # NOTE JGLISS: updated on 8.5.2020, cf. issue #106
                #s1 = s1.drop(index=overlap, inplace=True)
                s1.drop(index=overlap, inplace=True)
            #compute merged time series
            if len(s1) > 0:
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
        elif not var_name in self.var_info:
            raise MetaDataError('For merging of {} data, variable specific meta '
                                'data needs to be available in var_info dict '
                                .format(var_name))
        elif not var_name in other.var_info:
            raise MetaDataError('For merging of {} data, variable specific meta '
                                'data needs to be available in var_info dict '
                                .format(var_name))

        if self.get_unit(var_name) != other.get_unit(var_name):
            self.check_var_unit_aerocom(var_name)
            other.check_var_unit_aerocom(var_name)

        if self.check_if_3d(var_name):
            raise NotImplementedError('Coming soon...')
            #return self._merge_vardata_3d(other, var_name)
        else:
            return self._merge_vardata_2d(other, var_name)

    def merge_other(self, other, var_name, add_meta_keys=None):
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
        add_meta_keys : str or list, optional
            additional non-standard metadata keys that are supposed to be
            considered for merging.

        Returns
        -------
        StationData
            this object that has merged the other station
        """
        self.merge_vardata(other, var_name)
        self.merge_meta_same_station(other, add_meta_keys=add_meta_keys)

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

    def get_var_ts_type(self, var_name, try_infer=True):
        """Get ts_type for a certain variable

        Note
        ----
        Converts to ts_type string if assigned ts_type is in pandas format

        Parameters
        ----------
        var_name : str
            data variable name for which the ts_type is supposed to be
            retrieved
        try_infer : bool
            if ts_type is not available, try inferring it from data

        Returns
        -------
        str
            the corresponding data time resolution

        Raises
        ------
        MetaDataError
            if no metadata is available for this variable (e.g. if ``var_name``
            cannot be found in :attr:`var_info`)
        """
        # make sure there exists a var_info dict for this variable
        if not var_name in self.var_info:
            self.var_info[var_name] = {}

        # use variable specific entry if available
        if 'ts_type' in self.var_info[var_name]:
            return TsType(self.var_info[var_name]['ts_type']).val
        elif isinstance(self.ts_type, str):
            # ensures validity and corrects for pandas strings
            ts_type = TsType(self.ts_type).val
            self.var_info[var_name]['ts_type'] = ts_type
            return ts_type

        if try_infer:
            const.print_log.warning('Trying to infer ts_type in StationData {} '
                            'for variable {}'.format(self.station_name, var_name))
            from pyaerocom.helpers import infer_time_resolution
            try:
                s = self._to_ts_helper(var_name)
                ts_type = infer_time_resolution(s.index)
                self.var_info[var_name]['ts_type'] = ts_type
                return ts_type
            except Exception:
                pass #Raise standard error
        raise MetaDataError('Could not access ts_type for {}'.format(var_name))

    def remove_outliers(self, var_name, low=None, high=None,
                        check_unit=True):
        """Remove outliers from one of the variable timeseries

        Parameters
        ----------
        var_name : str
            variable name
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
        check_unit : bool
            if True, the unit of the data is checked against AeroCom default
        """
        if any([x is None for x in (low, high)]):
            info = const.VARS[var_name]
            if check_unit:
                try:
                    self.check_unit(var_name)
                except DataUnitError:
                    self.convert_unit(var_name, to_unit=info.units)
            if low is None:
                low = info.minimum
                logger.info('Setting {} outlier lower lim: {:.2f}'
                            .format(var_name, low))
            if high is None:
                high = info.maximum
                logger.info('Setting {} outlier upper lim: {:.2f}'
                            .format(var_name, high))

        d = self[var_name]
        invalid_mask = np.logical_or(d<low, d>high)
        d[invalid_mask] = np.nan
        self[var_name] = d

    def interpolate_timeseries(self, var_name, freq, min_coverage_interp=0.3,
                               resample_how='mean', inplace=False):
        """Interpolate one variable timeseries to a certain frequency

        ToDo: complete docstring
        """
        raise NotImplementedError('Needs review...')
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
            ts_type = PANDAS_FREQ_TO_TS_TYPE[new.index.freqstr]
            self[var_name] = new

            self.var_info[var_name]['ts_type'] = ts_type
            if len(self.var_info) > 1:
                self.ts_type = None
            else:
                self.ts_type = ts_type
        return new

    def calc_climatology(self, var_name, start=None, stop=None,
                         apply_constraints=None, min_num_obs=None,
                         clim_mincount=None, clim_freq=None,
                         set_year=None, resample_how=None):
        """Calculate climatological timeseries for input variable

        The computation is done as follows:

        1. retrieve monthly timesereries for climatological interval (if data
        is not already monthly). This is done by applying input resampling
        constraints via `apply_constraints` and `min_num_obs` and if these
        are unspecified, pyaerocom default is used (which is usually applying
        a hierarchical resampling)
        2. Climatological timeseries is then computed from that monthly
        timeseries, and if `apply_constraints` is True a further sampling
        coverage criterium is applied to compute the climatology, which can
        be specified via `mincount_month`, or, if unspecified, pyaerocom
        default is used (cf. :attr:`pyaerocom.const.CLIM_MIN_COUNT`)

        Parameters
        ----------
        var_name : str
            name of data variable
        start
            start time of data used to compute climatology
        stop
            start time of data used to compute climatology
        apply_constraints : bool, optional
            if True, then hierarchical resampling constraints are applied
            (for details see
            :func:`pyaerocom.time_resampler.TimeResampler.resample`)
        min_num_obs : dict or int, optional
            minimum number of observations required per period (when
            downsampling). For details see
            :func:`pyaerocom.time_resampler.TimeResampler.resample`)
        clim_micount : int, optional
            minimum number of of monthly values required per month of
            climatology
        set_year : int, optional
            if specified, the output data will be assigned the input year. Else
            the middle year of the climatological interval is used.
        resample_how : str
            how should the resampled data be averaged (e.g. mean, median)
        **kwargs
            Additional keyword args passed to
            :func:`pyaerocom.time_resampler.TimeResampler.resample`

        Returns
        -------
        StationData
            new instance of StationData containing climatological data
        """
        if clim_freq is None:
            clim_freq = const.CLIM_FREQ

        if resample_how is None:
            resample_how = const.CLIM_RESAMPLE_HOW

        ts_type = TsType(self.get_var_ts_type(var_name))

        monthly = TsType('monthly')
        if ts_type < monthly:
            raise TemporalResolutionError('Cannot compute climatology, {} data '
                                          'needs to be in monthly resolution '
                                          'or higher (is: {})'.format(
                                           var_name, ts_type))
        if ts_type < TsType(clim_freq): #current resolution is lower than input climatological freq
            supported = list(const.CLIM_MIN_COUNT.keys())
            if str(ts_type) in supported:
                clim_freq = str(ts_type)
            else: # use monthly
                clim_freq = 'monthly'

        ts= self.to_timeseries(var_name, freq=clim_freq,
                               resample_how=resample_how,
                               apply_constraints=apply_constraints,
                               min_num_obs=min_num_obs)

        if start is None:
            start = const.CLIM_START
        if stop is None:
            stop = const.CLIM_STOP
        if apply_constraints is None:
            apply_constraints = const.OBS_APPLY_TIME_RESAMPLE_CONSTRAINTS
        if apply_constraints and clim_mincount is None:
            clim_mincount = const.CLIM_MIN_COUNT[clim_freq]

        clim = calc_climatology(ts, start, stop,
                                min_count=clim_mincount,
                                set_year=set_year,
                                resample_how=resample_how)

        new = StationData()
        try:
            new.update(self.get_meta())
        except MetaDataError:
            new.update(self.get_meta(force_single_value=False))

        new[var_name] = clim['data']
        vi = {}
        if var_name in self.var_info:
            vi.update(self.var_info[var_name])

        new.var_info[var_name] = vi
        new.var_info[var_name]['ts_type'] = 'monthly'
        new.var_info[var_name]['ts_type_src'] = ts_type.base
        new.var_info[var_name]['is_climatology'] = True
        new.var_info[var_name]['clim_start'] = start
        new.var_info[var_name]['clim_stop'] = stop
        new.var_info[var_name]['clim_freq'] = clim_freq
        new.var_info[var_name]['clim_how'] = resample_how
        new.var_info[var_name]['clim_mincount'] = clim_mincount
        new.data_err[var_name] = clim['std']
        new.numobs[var_name] = clim['numobs']
        return new

    def resample_time(self, var_name, ts_type, how='mean',
                      apply_constraints=None, min_num_obs=None,
                      inplace=False, **kwargs):
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
        apply_constraints : bool, optional
            if True, then hierarchical resampling constraints are applied
            (for details see
            :func:`pyaerocom.time_resampler.TimeResampler.resample`)
        min_num_obs : dict or int, optional
            minimum number of observations required per period (when
            downsampling). For details see
            :func:`pyaerocom.time_resampler.TimeResampler.resample`)
        inplace : bool
            if True, then the current data object stored in self, will be
            overwritten with the resampled time-series
        **kwargs
            Additional keyword args passed to
            :func:`pyaerocom.time_resampler.TimeResampler.resample`

        Returns
        -------
        StationData
            with resampled variable timeseries
        """
        if inplace:
            outdata = self
        else:
            outdata = self.copy()
        if not var_name in outdata:
            raise KeyError("Variable {} does not exist".format(var_name))

        to_ts_type = TsType(ts_type) # make sure to use AeroCom ts_type

        try:
            from_ts_type = TsType(outdata.get_var_ts_type(var_name))
        except (MetaDataError, TemporalResolutionError):
            from_ts_type = None
            const.print_log.warning('Failed to access current temporal '
                                    'resolution of {} data in StationData {}. '
                                    'No resampling constraints will be applied'
                                    .format(var_name, outdata.station_name))

        data = outdata[var_name]

        if not isinstance(data, (pd.Series, xray.DataArray)):
            try:
                data = outdata.to_timeseries(var_name)
            except Exception as e:
                raise ValueError('{} data must be stored as pandas Series '
                                 'instance or as xarray.DataArray. Failed to '
                                 'convert to pandas Series.'
                                 'Error: {}'.format(repr(e)))
        resampler = TimeResampler(data)
        new = resampler.resample(to_ts_type=to_ts_type,
                                 from_ts_type=from_ts_type,
                                 how=how,
                                 apply_constraints=apply_constraints,
                                 min_num_obs=min_num_obs,
                                 **kwargs)

        outdata[var_name] = new
        outdata.var_info[var_name]['ts_type'] = to_ts_type.val
        outdata.var_info[var_name].update(resampler.last_setup)
        # there is other variables that are not resampled
        if len(outdata.var_info) > 1 and outdata.ts_type is not None:
            _tt = outdata.ts_type
            outdata.ts_type = None
            outdata.dtime = None
            for var, info in outdata.var_info.items():
                if not var == var_name:
                    info['ts_type'] = _tt
        else: #no other variables, update global class attributes
            outdata.ts_type = to_ts_type.val
            outdata.dtime = new.index.values

        return outdata

    def resample_timeseries(self, var_name, **kwargs):
        """Wrapper for :func:`resample_time` (for backwards compatibility)

        Note
        ----
        For backwards compatibility, this method will return a pandas Series
        instead of the actual StationData object
        """
        const.print_log.warning(DeprecationWarning('This method was renamed '
                                                   'to resample_time as a means '
                                                   'of harmonisation with GriddedData '
                                                   'and ColocatedData'))
        return self.resample_time(var_name, **kwargs)[var_name]

    def remove_variable(self, var_name):
        """Remove variable data

        Parameters
        ----------
        var_name : str
            name of variable that is to be removed

        Returns
        -------
        StationData
            current instance of this object, with data removed

        Raises
        ------
        VarNotAvailableError
            if the input variable is not available in this object
        """
        if not self.has_var(var_name):
            raise VarNotAvailableError('No such variable in StationData: {}'
                                       .format(var_name))
        self.pop(var_name)
        if var_name in self.var_info:
            self.var_info.pop(var_name)
        return self

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

        self.resample_time(var_name, ts_type, inplace=True)

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
        if isinstance(data, pd.Series):
            return data

        elif not data.ndim == 1:
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
        """Extract variable data within certain altitude range

        Note
        ----
        Beta version

        Parameters
        ----------
        var_name : str
            name of variable for which metadata is supposed to be extracted
        altitudes : list
            altitude range in m, e.g. [0, 1000]

        Returns
        -------
        pandas. Series or xarray.DataArray
            data object within input altitude range
        """

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
                if not isinstance(altitudes, slice):
                    altitudes = slice(altitudes[0], altitudes[1])
                return data.sel(altitude=altitudes)

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
                      apply_constraints=None, min_num_obs=None,
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
        apply_constraints : bool, optional
            if True, then hierarchical resampling constraints are applied
            (for details see
            :func:`pyaerocom.time_resampler.TimeResampler.resample`)
        min_num_obs : dict or int, optional
            minimum number of observations required per period (when
            downsampling). For details see
            :func:`pyaerocom.time_resampler.TimeResampler.resample`)
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
        if 'ts_type' in kwargs:
            if freq is not None:
                raise ValueError('Both freq and ts_type are provided as input')
            freq = kwargs.pop('ts_type')

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
            resampler = TimeResampler(data)
            try:
                from_ts_type = self.get_var_ts_type(var_name)
            except MetaDataError:
                from_ts_type = None
            data = resampler.resample(to_ts_type=freq,
                                      from_ts_type=from_ts_type,
                                      how=resample_how,
                                      apply_constraints=apply_constraints,
                                      min_num_obs=min_num_obs,
                                      **kwargs)

        return data

    def plot_timeseries(self, var_name, freq=None, resample_how='mean',
                        add_overlaps=False, legend=True, tit=None, **kwargs):
        """
        Plot timeseries for variable

        Note
        ----
        If you set input arg ``add_overlaps = True`` the overlapping timeseries
        data - if it exists - will be plotted on top of the actual timeseries
        using red colour and dashed line. As the overlapping data may be
        identical with the actual data, you might want to increase the line
        width of the actual timeseries using an additional input argument
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

        if 'ts_type' in kwargs:
            freq = kwargs.pop('ts_type')
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
                except Exception:
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
            except Exception:
                tit = 'Failed to retrieve station_name'
        s = self.to_timeseries(var_name, freq, resample_how)

        ax.plot(s, label=lbl, **kwargs)
        if add_overlaps and var_name in self.overlap:
            so = self.overlap[var_name]
            try:
                from pyaerocom.helpers import resample_timeseries
                so = resample_timeseries(so, freq, how=resample_how)
            except Exception:
                pass
            if var_name in self.overlap:
                ax.plot(so, '--', lw=1, c='r',
                        label='{} (overlap)'.format(var_name))
            else:
                tit += ' (No overlapping data found)'

        ylabel = var_name
        try:
            if 'units' in self.var_info[var_name]:
                u = self.var_info[var_name]['units']
                if u is not None and not u in [1, '1']:
                    ylabel += ' [{}]'.format(u)
        except Exception:
            logger.warning('Failed to access unit information for variable {}'
                           .format(var_name))
        ax.set_ylabel(ylabel)
        ax.set_title(tit)
        if legend:
            ax.legend()
        return ax

    def copy(self):
        new = StationData()
        for key, val in self.items():
            cpv = deepcopy(val)
            new[key] = cpv

        return new

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
                s += "\n{} ({}):".format(k, type(v).__name__)
                if v:
                    s = dict_to_str(v, s, indent=2)
                else:
                    s += ' <empty_dict>'
            elif isinstance(v, list):
                s += list_to_shortstr(v, name=k)
            elif isinstance(v, np.ndarray):
                if v.ndim==1:
                    arrays += list_to_shortstr(v, name=k)
                else:
                    arrays += "\n{} (ndarray, shape {})".format(k, v.shape)
                    arrays += "\n{}".format(v)
            elif isinstance(v, pd.Series):
                series += "\n{} (Series, {} items)".format(k, len(v))
            else:
                if isinstance(v,str) and v == '':
                    v = '<empty_str>'
                s += "\n{}: {}".format(k,v)
        if arrays:
            s += '\n\nData arrays\n.................'
            s += arrays
        if series:
            s += '\nPandas Series\n.................'
            s += series

        return s

def compute_trends_station(station, var_name, start_year=None,
                           stop_year=None, season=None, slope_confidence=0.68,
                           **alt_range):
    """Method to compute trends for a :class:`StationData` object

    Note
    ----
    This method is badly designed and will be outsourced at some point.
    Please do not use and use :func:`StationData.compute_trend` directly
    (which will need to be rewritten as well, as it uses this method at the
    moment...)

    No docstring because you shouldn't use this method!
    """
    # load additional information about data source (if applicable)
    if not 'trends' in station:
        station['trends'] = od()
    tr = station['trends']
    if not var_name in tr:
        station['trends'][var_name] = trv = TrendsEngine(var_name)
    else:
        trv = station['trends'][var_name]

    freq = station.get_var_ts_type(var_name)

    ts_types = const.GRID_IO.TS_TYPES

    if not trv.has_daily:
        if not freq in ts_types or (ts_types.index(freq) <= ts_types.index('daily')):
            trv['daily'] = station.to_timeseries(var_name, freq='daily', **alt_range)
    # monthly is mandatory
    if not trv.has_monthly:
        if freq in ts_types and ts_types.index(freq) > ts_types.index('monthly'):
            raise TemporalResolutionError('Need monthly or higher')
        ms = station.to_timeseries(var_name, freq='monthly', **alt_range)
        trv['monthly'] = ms
    else:
        ms = trv['monthly']

    if len(ms) == 0 or all(np.isnan(ms)):
        raise DataCoverageError('Failed to retrieve monthly timeseries for '
                                '{} ({})'.format(station.station_name,
                                 var_name))

    if trv._mobs is None:
        trv._mobs = _make_mobs_dataframe(ms)

    result = trv.compute_trend(start_year, stop_year, season,
                               slope_confidence)

    try:
        trv.meta.update(station.get_meta(add_none_vals=True))
    except MetaDataError:
        trv.meta.update(station.get_meta(force_single_value=False,
                                         add_none_vals=True))
    if var_name in station.var_info:
        trv.meta.update(station.var_info[var_name])
    return result

if __name__=="__main__":
    import pyaerocom as pya
    import matplotlib.pyplot as plt

    empty = StationData()

    empty.var_info['bla'] = dict(blub=42)

    empty_copy = empty.copy()
    empty_copy.var_info['bla']['blub'] = 1

    print(empty.var_info['bla']['blub'])
    print(empty_copy.var_info['bla']['blub'])

    for var in set('abc', 'bl'):
        print(var)
