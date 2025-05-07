from __future__ import annotations
import logging
import warnings
from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

from pyaerocom import const
from pyaerocom._lowlevel_helpers import (
    BrowseDict,
    dict_to_str,
    list_to_shortstr,
    merge_dicts,
)
from pyaerocom.exceptions import (
    CoordinateError,
    DataDimensionError,
    DataExtractionError,
    DataUnitError,
    MetaDataError,
    StationCoordinateError,
    TemporalResolutionError,
    VarNotAvailableError,
)
from pyaerocom.helpers import calc_climatology, isnumeric, isrange
from pyaerocom.metastandards import STANDARD_META_KEYS, StationMetaData
from pyaerocom.time_resampler import TimeResampler
from pyaerocom.units.datetime import TsType, to_datetime64
from pyaerocom.units.helpers import get_standard_unit
from pyaerocom.units.logging import LoggingCallback

from pyaerocom.units import convert_unit

from pyaerocom.units.datetime import infer_time_resolution

from pyaerocom.geodesy import calc_distance

logger = logging.getLogger(__name__)


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
    # _COORD_MAX_VAR = 0.1 #km
    _COORD_MAX_VAR = 5.0  # km
    STANDARD_META_KEYS = STANDARD_META_KEYS

    VALID_TS_TYPES = const.GRID_IO.TS_TYPES

    #: Keys that are ignored when accessing metadata
    PROTECTED_KEYS = [
        "dtime",
        "var_info",
        "station_coords",
        "data_err",
        "overlap",
        "numobs",
        "data_flagged",
    ]

    def __init__(self, **meta_info):
        self.dtime = []

        self.var_info: BrowseDict[xr.DataArray, pd.Series] = BrowseDict()

        self.station_coords = dict.fromkeys(self.STANDARD_COORD_KEYS)

        self.data_err = BrowseDict()
        self.overlap = BrowseDict()
        self.numobs = BrowseDict()
        self.data_flagged = BrowseDict()

        super().__init__(**meta_info)

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
        return list(self.var_info)

    def has_var(self, var_name: str) -> bool:
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
        if var_name not in self:
            return False
        if var_name not in self.var_info:
            logger.warning(
                f"Variable {var_name} exists in data but has no "
                f"metadata assigned in :attr:`var_info`"
            )
        return True

    def get_unit(self, var_name: str) -> str:
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
        if var_name not in self.var_info:
            raise MetaDataError(f"Could not access variable metadata dict for {var_name}.")
        try:
            return str(self.var_info[var_name]["units"])
        except KeyError:
            add_str = ""
            if "unit" in self.var_info[var_name]:
                add_str = (
                    "Corresponding var_info dict contains "
                    'attr. "unit", which is deprecated, please '
                    "check corresponding reading routine. "
                )
            raise MetaDataError(
                f"Failed to access units attribute for variable {var_name}. {add_str}"
            )

    @property
    def units(self) -> dict[str, str]:
        """Dictionary containing units of all variables in this object"""
        ud = {}
        for var in self.var_info:
            ud[var] = self.get_unit(var)
        return ud

    def check_var_unit_aerocom(self, var_name: str):
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
        to_unit = get_standard_unit(var_name)
        try:
            self._check_unit(var_name, to_unit)
        except Exception:
            self.convert_unit(var_name, to_unit)

    def _check_unit(self, var_name: str, unit: str | None = None):
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
            unit = get_standard_unit(var_name)

        u = self.get_unit(var_name)
        if not convert_unit(1, u, unit, var_name) == 1:
            raise DataUnitError(f"Invalid unit {u} (expected {unit})")
        else:
            self.var_info[var_name]["units"] = unit

    def convert_unit(self, var_name: str, to_unit: str) -> None:
        """Try to convert unit of data

        Requires that unit of input variable is available in :attr:`var_info`

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
            ts_type = self.get_var_ts_type(var_name)
        except MetaDataError:
            ts_type = None

        fac = convert_unit(
            1,
            from_unit=unit,
            to_unit=to_unit,
            var_name=var_name,
            ts_type=ts_type,
            callback=LoggingCallback(logger),
        )

        self[var_name] = fac * self[var_name]
        if var_name in self.data_err:
            self.data_err[var_name] = fac * self.data_err[var_name]

        self.var_info[var_name]["units"] = to_unit

    def dist_other(self, other: StationData) -> float:
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
        cthis = self.get_station_coords()
        cother = other.get_station_coords()

        return calc_distance(
            cthis["latitude"],
            cthis["longitude"],
            cother["latitude"],
            cother["longitude"],
            cthis["altitude"],
            cother["altitude"],
        )

    def same_coords(self, other: StationData, tol_km: float | None = None) -> bool:
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

    def get_station_coords(self, force_single_value: bool = True) -> dict[str, float]:
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
        output = {}
        for key in self.STANDARD_COORD_KEYS:
            # prefer explicit if defined in station_coord dictionary (e.g. altitude
            # attribute in lidar data will be an array corresponding to profile
            # altitudes)
            val = self.station_coords[key]
            if val is not None:
                if not isnumeric(val):
                    raise MetaDataError(f"Station coordinate {key} must be numeric. Got: {val}")
                output[key] = val
            else:
                val = self[key]
                if force_single_value and not isinstance(val, float | np.floating):
                    if isinstance(val, int | np.integer):
                        val = np.float64(val)
                    elif isinstance(val, list | np.ndarray):
                        # ToDo: consider tolerance to be specified in input
                        # args.
                        maxdiff = np.max(val) - np.min(val)
                        if key in ("latitude", "longitude"):
                            tol = 0.05  # ca 5km at equator
                        else:
                            tol = 100  # m altitude tolerance
                        if maxdiff > tol:
                            raise StationCoordinateError(
                                f"meas point coordinate arrays of {key} vary "
                                f"too much to reduce them to a single "
                                f"coordinate. Order of difference in {key} is "
                                f"{maxdiff} and maximum allowed is {tol}."
                            )
                        val = np.mean(val)
                    else:
                        raise AttributeError(
                            f"Invalid value encountered for coord {key}, "
                            f"need float, int, list or ndarray, got {type(val)}"
                        )
                output[key] = val
        return output

    def get_meta(
        self,
        force_single_value: bool = True,
        quality_check: bool = True,
        add_none_vals: bool = False,
        add_meta_keys: str | list[str] | None = None,
    ):
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
            standard deviation in the values is compared to the upper limits
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
        meta.update(self.get_station_coords(force_single_value))
        keys = [k for k in self.STANDARD_META_KEYS]
        keys.extend(add_meta_keys)
        for key in keys:
            if key not in self:
                logger.warning(f"No such key in StationData: {key}")
                continue
            elif key in self.PROTECTED_KEYS:
                # this is not metadata...
                continue
            elif key in self.STANDARD_COORD_KEYS:
                # this has been handled above
                continue
            if self[key] is None and not add_none_vals:
                logger.debug(f"No metadata available for key {key}")
                continue

            val = self[key]
            if force_single_value and isinstance(val, list | tuple | np.ndarray):
                if quality_check and not all([x == val[0] for x in val]):
                    raise MetaDataError(f"Inconsistencies in meta parameter {key}")
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
                raise MetaDataError(
                    f"Invalid metadata entry {val} for key {key}. "
                    f"Only 1d numpy arrays are supported..."
                )
            self[key] = list(val)
        elif not isinstance(val, dict | list | str) and not isnumeric(val):
            try:
                self[key] = to_datetime64(val)
            except Exception:
                raise MetaDataError(
                    f"Invalid metadata entry {val} for key {key}. "
                    f"Only dicts, lists, strings, numerical "
                    f"values or datetime objects are supported."
                )

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
                    raise ValueError(f"Cannot merge meta item {key} due to type mismatch")
                elif not current_val == val:
                    self[key] = merge_dicts(current_val, val)

            elif isinstance(current_val, str):
                if not same_type:
                    if isinstance(val, list):
                        if current_val not in val:
                            newval = val.insert(0, current_val)
                        self[key] = newval
                    else:
                        raise ValueError(f"Cannot merge meta item {key} due to type mismatch")
                elif not current_val == val:
                    # both are str that may be already merged with ";" -> only
                    # add new entries
                    vals_in = [x.strip() for x in val.split(";")]

                    for item in vals_in:
                        if item not in current_val:
                            current_val += f";{item}"
                    self[key] = current_val

            elif isinstance(current_val, list):
                if not same_type:
                    val = [val]
                for item in val:
                    if item not in current_val:
                        current_val.append(item)
                self[key] = current_val

            elif isnumeric(current_val) and isnumeric(val):
                if np.isnan(current_val) and np.isnan(val):
                    self[key] = val
                elif val != current_val:
                    self[key] = [current_val, val]

            elif isinstance(val, list):
                if current_val not in val:
                    self[key] = val.insert(0, current_val)

            elif current_val != val:
                self[key] = [current_val, val]

            else:  # they should be the same
                assert current_val == val, (current_val, val)
        except Exception as e:
            raise MetaDataError(
                f"Failed to merge metadata entries for key {key}.\n"
                f"Value in current StationData: {current_val}\n"
                f"Value to be merged: {val}\n"
                f"Error: {repr(e)}"
            )

    def _append_meta_item(self, key, val):
        """Add a metadata item"""
        if key not in self or self[key] is None:
            self[key] = val
        else:
            self._merge_meta_item(key, val)

    def merge_meta_same_station(
        self,
        other: StationData,
        coord_tol_km: float | None = None,
        check_coords: bool = True,
        inplace: bool = True,
        add_meta_keys: str | list[str] | None = None,
        raise_on_error: bool = False,
    ) -> StationData:
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
                if not self.same_coords(other, coord_tol_km):
                    raise CoordinateError(
                        f"Station coordinates of {self.station_id} and {other.station_id} for species {self.vars_available} differ by more than {coord_tol_km} km."
                    )
            except MetaDataError:  #
                pass

        keys = [k for k in self.STANDARD_META_KEYS]
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
                    obj[key] = "N/A_FAILED_TO_MERGE"
                    msg = f"Failed to merge meta item {key}. Reason:{repr(e)}"
                    if raise_on_error:
                        raise MetaDataError(msg)
                    else:
                        logger.warning(msg)

        return obj

    def merge_varinfo(self, other: StationData, var_name: str) -> StationData:
        """Merge variable specific meta information from other object

        Parameters
        ----------
        other : StationData
            other data object
        var_name : str
            variable name for which info is to be merged (needs to be both
            available in this object and the provided other object)
        """
        if var_name not in self.var_info or var_name not in other.var_info:
            raise MetaDataError(f"No variable meta information available for {var_name}")

        info_this = self.var_info[var_name]
        info_other = other.var_info[var_name]
        for key, val in info_other.items():
            if key not in info_this or info_this[key] is None:
                info_this[key] = val
            else:
                if isinstance(info_this[key], str):
                    if not isinstance(val, str):
                        raise ValueError(f"Cannot merge meta item {key} due to type mismatch")
                    vals = [x.strip() for x in info_this[key].split(";")]
                    vals_in = [x.strip() for x in val.split(";")]

                    for _val in vals_in:
                        if _val not in vals:
                            info_this[key] = info_this[key] + f";{_val}"
                else:
                    if isinstance(val, list | np.ndarray):
                        if len(val) == 0 or info_this[key] == val:
                            continue

                        raise ValueError(
                            "Cannot append metadata value that is "
                            "already a list or numpy array due to "
                            "potential ambiguities"
                        )
                    if isinstance(info_this[key], list):
                        if val not in info_this[key]:
                            info_this[key].append(val)
                    else:
                        if not info_this[key] == val:
                            info_this[key] = [info_this[key], val]
        return self

    def check_if_3d(self, var_name: str) -> bool:
        """Checks if altitude data is available in this object"""
        if "altitude" in self:
            val = self["altitude"]
            if isnumeric(val):  # is numerical value
                return False
            # unique altitude values
            uvals = np.unique(val)
            if len(uvals) == 1:  # only one value in altitude array (NOT 3D)
                return False
            elif (
                len(uvals[~np.isnan(uvals)]) == 1
            ):  # only 2 unique values in altitude array but one is NaN
                return False
            return True
        return False

    def _check_ts_types_for_merge(self, other: StationData, var_name: str):
        ts_type = self.get_var_ts_type(var_name)
        ts_type1 = other.get_var_ts_type(var_name)
        if ts_type != ts_type1:
            # make sure each variable in the object has explicitly ts_type
            # assigned (rather than global specification)

            self._update_var_timeinfo()
            other._update_var_timeinfo()

            from pyaerocom.units.datetime import get_lowest_resolution

            ts_type = get_lowest_resolution(ts_type, ts_type1)
        return ts_type

    def _update_var_timeinfo(self):
        for var, info in self.var_info.items():
            data = self[var]
            if not isinstance(data, pd.Series):
                try:
                    self[var] = pd.Series(data, self.dtime)
                except Exception as e:
                    raise Exception(f"Unexpected error: {repr(e)}.\nPlease debug...")
            if "ts_type" not in info or info["ts_type"] is None:
                if self.ts_type not in const.GRID_IO.TS_TYPES:
                    raise ValueError(f"Cannot identify ts_type for var {var} in {self}")
                info["ts_type"] = self.ts_type
        self.ts_type = None

    def _merge_vardata_2d(
        self,
        other: StationData,
        var_name: str,
        resample_how: str | None = None,
        min_num_obs: dict | int | None = None,
    ):
        """Merge 2D variable data (for details see :func:`merge_vardata`)"""
        ts_type = self._check_ts_types_for_merge(other, var_name)

        s0 = self.resample_time(
            var_name,
            ts_type=ts_type,
            how=resample_how,
            min_num_obs=min_num_obs,
            inplace=True,
        )[var_name].dropna()
        s1 = other.resample_time(
            var_name,
            ts_type=ts_type,
            how=resample_how,
            min_num_obs=min_num_obs,
            inplace=True,
        )[var_name].dropna()

        info = other.var_info[var_name]
        removed = None
        if "overlap" in info and info["overlap"]:
            raise NotImplementedError("Coming soon...")

        if len(s1) > 0:  # there is data
            overlap = s0.index.intersection(s1.index)
            try:
                if len(overlap) > 0:
                    removed = s1[overlap]
                    # NOTE JGLISS: updated on 8.5.2020, cf. issue #106
                    # s1 = s1.drop(index=overlap, inplace=True)
                    s1.drop(index=overlap, inplace=True)
                # compute merged time series
                if len(s1) > 0:
                    s0 = pd.concat([s0, s1], verify_integrity=True)

                # sort the concatenated series based on timestamps
                s0.sort_index(inplace=True)
                self.merge_varinfo(other, var_name)
            except KeyError:
                logger.warning(
                    f"failed to merge {var_name} data from 2 StationData "
                    f"objects for station {self.station_name}. Ignoring 2nd "
                    f"data object."
                )

        # assign merged time series (overwrites previous one)
        self[var_name] = s0
        self.dtime = s0.index.values

        if removed is not None:
            if var_name in self.overlap:
                self.overlap[var_name] = pd.concat([self.overlap[var_name], removed])
                self.overlap[var_name].sort_index(inplace=True)
            else:
                self.overlap[var_name] = removed

        return self

    def merge_vardata(self, other: StationData, var_name: str, **kwargs):
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
        kwargs
            keyword args passed on to :func:`_merge_vardata_2d`

        Returns
        -------
        StationData
            this object merged with other object
        """
        if var_name not in self:
            raise VarNotAvailableError(
                f"StationData object does not contain data for variable {var_name}"
            )
        elif var_name not in other:
            raise VarNotAvailableError(
                "Input StationData object does not contain data for variable {var_name}"
            )
        elif var_name not in self.var_info:
            raise MetaDataError(
                f"For merging of {var_name} data, variable specific meta "
                f"data needs to be available in var_info dict"
            )
        elif var_name not in other.var_info:
            raise MetaDataError(
                f"For merging of {var_name} data, variable specific meta "
                f"data needs to be available in var_info dict"
            )

        if self.get_unit(var_name) != other.get_unit(var_name):
            self.check_var_unit_aerocom(var_name)
            other.check_var_unit_aerocom(var_name)

        if self.check_if_3d(var_name):
            raise NotImplementedError("Coming soon...")
            # return self._merge_vardata_3d(other, var_name)
        else:
            return self._merge_vardata_2d(other, var_name, **kwargs)

    def merge_other(
        self,
        other: StationData,
        var_name: str,
        add_meta_keys: str | list[str] | None = None,
        **kwargs,
    ) -> StationData:
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
        kwargs
            keyword args passed on to :func:`merge_vardata` (e.g time
            resampling settings)

        Returns
        -------
        StationData
            this object that has merged the other station
        """
        self.merge_vardata(other, var_name, **kwargs)
        self.merge_meta_same_station(other, add_meta_keys=add_meta_keys)

        return self

    def check_dtime(self):
        """Checks if dtime attribute is array or list"""
        if not any([isinstance(self.dtime, x) for x in [list, np.ndarray]]):
            raise TypeError(f"dtime attribute is not iterable: {self.dtime}")
        elif not len(self.dtime) > 0:
            raise AttributeError("No timestamps available")

    def get_var_ts_type(self, var_name: str, try_infer: bool = True) -> TsType:
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
        if var_name not in self.var_info:
            self.var_info[var_name] = {}

        # use variable specific entry if available
        if "ts_type" in self.var_info[var_name]:
            return TsType(self.var_info[var_name]["ts_type"])
        elif isinstance(self.ts_type, str):
            # ensures validity and corrects for pandas strings
            ts_type = TsType(self.ts_type)
            self.var_info[var_name]["ts_type"] = ts_type
            return ts_type

        if try_infer:
            logger.warning(
                f"Trying to infer ts_type in StationData {self.station_name} "
                f"for variable {var_name}"
            )

            try:
                s = self._to_ts_helper(var_name)
                ts_type = infer_time_resolution(s.index)
                self.var_info[var_name]["ts_type"] = ts_type
                return ts_type
            except Exception:
                pass  # Raise standard error
        raise MetaDataError(f"Could not access ts_type for {var_name}")

    def remove_outliers(
        self,
        var_name: str,
        low: float | None = None,
        high: float | None = None,
        check_unit: bool = True,
    ):
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
                    self.check_var_unit_aerocom(var_name)
                except DataUnitError:
                    self.convert_unit(var_name, to_unit=info.units)
            if low is None:
                low = info.minimum
                logger.info(f"Setting {var_name} outlier lower lim: {low:.2f}")
            if high is None:
                high = info.maximum
                logger.info(f"Setting {var_name} outlier upper lim: {high:.2f}")

        d = self[var_name]
        invalid_mask = np.logical_or(d < low, d > high)
        d[invalid_mask] = np.nan
        self[var_name] = d

    def calc_climatology(
        self,
        var_name: str,
        start=None,
        stop=None,
        min_num_obs=None,
        clim_mincount=None,
        clim_freq=None,
        set_year=None,
        resample_how=None,
    ) -> StationData:
        """Calculate climatological timeseries for input variable


        Parameters
        ----------
        var_name : str
            name of data variable
        start
            start time of data used to compute climatology
        stop
            start time of data used to compute climatology
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

        monthly = TsType("monthly")
        if ts_type < monthly:
            raise TemporalResolutionError(
                f"Cannot compute climatology, {var_name} data "
                f"needs to be in monthly resolution or higher (is: {ts_type})"
            )
        if ts_type < TsType(
            clim_freq
        ):  # current resolution is lower than input climatological freq
            if clim_mincount is None:
                supported = list(const.CLIM_MIN_COUNT)
            else:
                supported = list(clim_mincount)
            if str(ts_type) in supported:
                clim_freq = str(ts_type)
            else:  # use monthly
                clim_freq = "monthly"

        data = self.resample_time(
            var_name,
            ts_type=clim_freq,
            how=resample_how,
            min_num_obs=min_num_obs,
            inplace=False,
        )
        ts = data.to_timeseries(var_name)

        if start is None:
            start = const.CLIM_START
        if stop is None:
            stop = const.CLIM_STOP

        if clim_mincount is None:
            clim_mincount = const.CLIM_MIN_COUNT[clim_freq]
        if isinstance(clim_mincount, dict):
            clim_mincount = clim_mincount[clim_freq]

        clim = calc_climatology(
            ts,
            start,
            stop,
            min_count=clim_mincount,
            set_year=set_year,
            resample_how=resample_how,
        )

        new = StationData()
        try:
            new.update(self.get_meta())
        except MetaDataError:
            new.update(self.get_meta(force_single_value=False))

        new[var_name] = clim["data"]
        vi = {}
        if var_name in self.var_info:
            vi.update(self.var_info[var_name])

        new.var_info[var_name] = vi
        new.var_info[var_name]["ts_type"] = "monthly"
        new.var_info[var_name]["ts_type_src"] = ts_type.base
        new.var_info[var_name]["is_climatology"] = True
        new.var_info[var_name]["clim_start"] = start
        new.var_info[var_name]["clim_stop"] = stop
        new.var_info[var_name]["clim_freq"] = clim_freq
        new.var_info[var_name]["clim_how"] = resample_how
        new.var_info[var_name]["clim_mincount"] = clim_mincount
        new.data_err[var_name] = clim["std"]
        new.numobs[var_name] = clim["numobs"]
        return new

    def resample_time(
        self, var_name: str, ts_type: str, how=None, min_num_obs=None, inplace=False, **kwargs
    ):
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
        if var_name not in outdata:
            raise KeyError(f"Variable {var_name} does not exist")

        to_ts_type = TsType(ts_type)  # make sure to use AeroCom ts_type

        try:
            from_ts_type = TsType(outdata.get_var_ts_type(var_name))
        except (MetaDataError, TemporalResolutionError):
            from_ts_type = None
            logger.warning(
                f"Failed to access current temporal resolution of {var_name} data "
                f"in StationData {outdata.station_name}. "
                f"No resampling constraints will be applied"
            )

        data = outdata[var_name]

        if not isinstance(data, pd.Series | xr.DataArray):
            data = outdata.to_timeseries(var_name)
        resampler = TimeResampler(data)
        new = resampler.resample(
            to_ts_type=to_ts_type,
            from_ts_type=from_ts_type,
            how=how,
            min_num_obs=min_num_obs,
            **kwargs,
        )

        outdata[var_name] = new
        outdata.var_info[var_name]["ts_type"] = to_ts_type.val
        outdata.var_info[var_name].update(resampler.last_setup)
        # there is other variables that are not resampled
        if len(outdata.var_info) > 1 and outdata.ts_type is not None:
            _tt = outdata.ts_type
            outdata.ts_type = None
            outdata.dtime = None
            for var, info in outdata.var_info.items():
                if not var == var_name:
                    info["ts_type"] = _tt
        else:  # no other variables, update global class attributes
            outdata.ts_type = to_ts_type.val
            outdata.dtime = new.index.values

        return outdata

    def resample_timeseries(self, var_name: str, **kwargs):
        """Wrapper for :func:`resample_time` (for backwards compatibility)

        Note
        ----
        For backwards compatibility, this method will return a pandas Series
        instead of the actual StationData object
        """
        warnings.warn(
            "This method was renamed to resample_time as a means "
            "of harmonisation with GriddedData and ColocatedData",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.resample_time(var_name, **kwargs)[var_name]

    def remove_variable(self, var_name: str):
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
            raise VarNotAvailableError(f"No such variable in StationData: {var_name}")
        self.pop(var_name)
        if var_name in self.var_info:
            self.var_info.pop(var_name)
        return self

    def insert_nans_timeseries(self, var_name: str) -> StationData:
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

        Returns
        -------
        StationData
            the modified station data object

        """
        ts_type = self.get_var_ts_type(var_name)

        self.resample_time(var_name, ts_type, inplace=True)

        return self

    def _to_ts_helper(self, var_name: str) -> pd.Series:
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
            raise NotImplementedError(
                "Multi-dimensional data columns cannot be converted to time-series"
            )
        self.check_dtime()
        if not len(data) == len(self.dtime):
            raise ValueError(
                f"Mismatch between length of data array "
                f"for variable {var_name} (length: {len(data)}) "
                f"and time array  (length: {len(self.dtime)})."
            )
        self[var_name] = s = pd.Series(data, index=self.dtime)
        return s

    def select_altitude(self, var_name: str, altitudes: list) -> pd.Series | xr.DataArray:
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
            raise NotImplementedError(
                "So far only a range (low, high) is supported for altitude extraction."
            )

        if isinstance(data, xr.DataArray):
            if not sorted(data.dims) == ["altitude", "time"]:
                raise NotImplementedError(
                    "Can only handle dataarrays that contain 2 dimensions altitude and time"
                )
            if isrange(altitudes):
                if not isinstance(altitudes, slice):
                    altitudes = slice(altitudes[0], altitudes[1])
                result = data.sel(altitude=altitudes)
                if len(result.altitude) == 0:
                    raise ValueError("no data in specified altitude range")
                return result

            raise DataExtractionError("Cannot interpret input for altitude...")

        elif isinstance(data, pd.Series) or len(self.dtime) == len(data):
            if "altitude" not in self:
                raise ValueError("Missing altitude information")
            if not isinstance(data, pd.Series):
                data = pd.Series(data, self.dtime)
            alt = self.altitude
            if not isinstance(alt, list | np.ndarray):
                raise AttributeError("need 1D altitude array")
            elif not len(alt) == len(data):
                raise DataDimensionError(
                    f"Altitude data and {var_name} data have different lengths"
                )
            mask = np.logical_and(alt >= altitudes[0], alt <= altitudes[1])
            if mask.sum() == 0:
                raise ValueError("no data in specified altitude range")
            return data[mask]

        raise DataExtractionError(
            f"Cannot extract altitudes: type of {var_name} ({type(data)}) is not supported"
        )

    def to_timeseries(self, var_name: str, **kwargs) -> pd.Series:
        """Get pandas.Series object for one of the data columns

        Parameters
        ----------
        var_name : str
            name of variable (e.g. "od550aer")

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
        if var_name not in self:
            raise KeyError(f"Variable {var_name} does not exist")

        data = self[var_name]

        if isinstance(data, xr.DataArray):
            if not all([x in data.dims for x in ("time", "altitude")]):
                raise NotImplementedError(
                    "Can only handle dataarrays that contain 2 dimensions of time and altitude"
                )
            if "altitude" not in kwargs:
                raise ValueError(
                    "please specify altitude range via input "
                    "arg: altitude, e.g. altitude=(100,110)"
                )
            alt_info = kwargs.pop("altitude")
            data = self.select_altitude(var_name, alt_info)
            data = data.mean("altitude")
            data = data.to_series()

        if not isinstance(data, pd.Series):
            data = self._to_ts_helper(var_name)

        return data

    def plot_timeseries(
        self,
        var_name: str,
        add_overlaps: bool = False,
        legend: bool = True,
        tit: str | None = None,
        **kwargs,
    ):
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
        if "label" in kwargs:
            lbl = kwargs.pop("label")
        else:
            lbl = var_name
            try:
                ts_type = self.get_var_ts_type(var_name)
                lbl += f" ({ts_type})"
            except Exception:
                pass
        if "ax" not in kwargs:
            if "figsize" in kwargs:
                fs = kwargs.pop("figsize")
            else:
                fs = (16, 8)
            _, ax = plt.subplots(1, 1, figsize=fs)
        else:
            ax = kwargs.pop("ax")
            # keep existing title if it exists
            _tit = ax.get_title()
            if not _tit == "":
                tit = _tit

        if tit is None:
            try:
                tit = self.get_meta(force_single_value=True, quality_check=False)["station_name"]
            except Exception:
                tit = "Failed to retrieve station_name"
        s = self.to_timeseries(var_name)
        ax.plot(s, label=lbl, **kwargs)
        if add_overlaps and var_name in self.overlap:
            so = self.overlap[var_name]
            ax.plot(so, "--", lw=1, c="r", label=f"{var_name} (overlap)")

        ylabel = var_name
        try:
            if "units" in self.var_info[var_name]:
                u = self.var_info[var_name]["units"]
                if u is not None and u not in [1, "1"]:
                    ylabel += f" [{u}]"
        except Exception:
            logger.warning(f"Failed to access unit information for variable {var_name}")
        ax.set_ylabel(ylabel)
        ax.set_title(tit)
        if legend:
            ax.legend()
        return ax

    def copy(self) -> StationData:
        new = StationData()
        for key, val in self.items():
            cpv = deepcopy(val)
            new[key] = cpv

        return new

    def __str__(self) -> str:
        """String representation"""
        head = f"Pyaerocom {type(self).__name__}"
        s = f"\n{head}\n{len(head) * '-'}"
        arrays = ""
        series = ""

        for k, v in self.items():
            if k[0] == "_":
                continue
            if isinstance(v, dict):
                s += f"\n{k} ({type(v).__name__}):"
                if v:
                    s += dict_to_str(v, indent=2)
                else:
                    s += " <empty_dict>"
            elif isinstance(v, list):
                s += f"{k} : {list_to_shortstr(v)}"
            elif isinstance(v, np.ndarray):
                if v.ndim == 1:
                    arrays += f"{k} : {list_to_shortstr(v)}"
                else:
                    arrays += f"\n{k} (ndarray, shape {v.shape})"
                    arrays += f"\n{v}"
            elif isinstance(v, pd.Series):
                series += f"\n{k} (Series, {len(v)} items)"
            else:
                if isinstance(v, str) and v == "":
                    v = "<empty_str>"
                s += f"\n{k}: {v}"
        if arrays:
            s += "\n\nData arrays\n................."
            s += arrays
        if series:
            s += "\nPandas Series\n................."
            s += series

        return s
