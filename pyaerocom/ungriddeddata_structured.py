import fnmatch
import logging
import sys
from typing import Any

import pandas as pd

import numpy as np

from pyaerocom.exceptions import (
    DataCoverageError,
    StationNotFoundError,
    VarNotAvailableError,
)
from pyaerocom.helpers import merge_station_data, start_stop
from pyaerocom.metastandards import STANDARD_META_KEYS
from pyaerocom.stationdata import StationData
from pyaerocom.tstype import TsType
from pyaerocom.ungridded_data import UngriddedDataContainer

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

logger = logging.getLogger(__name__)


class UngriddedDataStructured(UngriddedDataContainer):
    """Class implementing UngriddedData in a numpy structured array"""

    __version__ = "0.01"

    _dtype = [
        ("meta_id", "i4"),
        ("var_id", "i2"),
        ("start_time", "datetime64[s]"),
        ("end_time", "datetime64[s]"),
        ("data", "f"),  # data-value
        ("stdev", "f"),  # data-error
        ("height", "i2"),  # altitude of measurement (might be different from station)
        ("flag", "i2"),
    ]
    _nan_types = {
        "meta_id": -2147483647,
        "var_id": -32767,
        "start_time": np.datetime64("NaT"),
        "end_time": np.datetime64("NaT"),
        "data": np.nan,
        "stdev": np.nan,
        "height": -32767,
        "flag": -32767,
    }

    STANDARD_META_KEYS = STANDARD_META_KEYS

    def __init__(self, num_points: int = 100000):
        self._data = self._create_data_chunk(num_points)

        # station metadata dict[int, dict[str, Any]] with first int being the meta_id
        self.metadata = {}
        # station-name - meta-id translation
        self.meta_id = {}
        # var-name -> var-id translation
        self.var_id = {}
        # filters applied
        self.filter_hist = {}

        self._is_vertiacl_profile = False

    def _create_data_chunk(self, size):
        """create a datachunk of size and initialize it to _nan_type values"""
        data = np.empty(size, dtype=self._dtype)
        for k, v in self._nan_types.values:
            data[k] = v
        return data

    @property
    @override
    def has_flag_data(self):
        return (self._data["flag"] == -32767).any()

    @property
    @override
    def is_vertical_profile(self):
        return self._is_vertiacl_profile

    @is_vertical_profile.setter
    @override
    def is_vertical_profile(self, value):
        self._is_vertiacl_profile = value

    @property
    @override
    def contains_vars(self) -> list[str]:
        return list(self.var_id)

    def _list_from_metadata(self, metafield, undef=None, unique=False) -> list[Any]:
        """retrieve a station-metadata field as list

        :param metafield: one of the metadata-fields like "longitude" or "instrument"
        :param undef: default value if undefined
        :param unique: remove None and duplicate, defaults to False
        :return: list of the metadata-fields values
        """
        ret_vals = []
        for info in self.metadata.values():
            try:
                val = info[metafield]
                if unique and val is not None and val not in ret_vals:
                    ret_vals.append(val)
            except KeyError:
                if not unique:
                    ret_vals.append(undef)
        return ret_vals

    @property
    @override
    def contains_datasets(self) -> list[str]:
        return self._list_from_metadata("data_id")

    @property
    @override
    def contains_instruments(self):
        return self._list_from_metadata("instrument_name", unique=True)

    @property
    @override
    def is_empty(self):
        """Boolean specifying whether this object contains data or not"""
        return True if len(self.metadata) == 0 else False

    @property
    @override
    def longitude(self):
        return self._list_from_metadata("longitude", undef=np.nan)

    @property
    @override
    def latitude(self):
        return self._list_from_metadata("latitude", undef=np.nan)

    @property
    @override
    def altitude(self):
        return self._list_from_metadata("altitude", undef=np.nan)

    @property
    @override
    def station_name(self):
        return self._list_from_metadata("station_name", undef=np.nan)

    @property
    @override
    def unique_station_name(self):
        return sorted(self._list_from_metadata("station_name", unique=True))

    @property
    @override
    def available_meta_keys(self):
        metakeys = []
        for meta in self.metadata.values():
            for key in meta:
                if key not in metakeys:
                    metakeys.append(key)
        return metakeys

    @property
    @override
    def countries_available(self):
        countries = []
        for idx, meta in self.metadata.items():
            try:
                countries.append(meta["country"])
            except KeyError:
                logger.warning("No country information in meta block", idx)
        if len(countries) == 0:
            logger.warning(
                "None of the metadata blocks contains "
                "country information. You may want to "
                "run class method check_set_country first "
                "to automatically assign countries."
            )
        return sorted(set(countries))

    @property
    @override
    def find_station_meta_indices(self, station_name_or_pattern, allow_wildcards=True):
        if not allow_wildcards:

            def compare(x, y):
                return fnmatch.fnmatch(x, y)

        else:

            def compare(x, y):
                return x == y

        idx = []
        for i, meta in self.metadata.items():
            if compare(meta["station_name"], station_name_or_pattern):
                idx.append(i)
        if len(idx) == 0:
            raise StationNotFoundError(
                f"No station available in UngriddedData that matches name {station_name_or_pattern}"
            )
        return idx

    def to_station_data(
        self,
        meta_idx,
        vars_to_convert=None,
        start=None,
        stop=None,
        freq=None,
        ts_type_preferred=None,
        merge_if_multi=True,
        merge_pref_attr=None,
        merge_sort_by_largest=True,
        insert_nans=False,
        allow_wildcards_station_name=True,
        add_meta_keys=None,
        resample_how=None,
        min_num_obs=None,
    ):
        if isinstance(vars_to_convert, str):
            vars_to_convert = [vars_to_convert]
        elif vars_to_convert is None:
            vars_to_convert = self.contains_vars
            if len(vars_to_convert) == 0:
                raise DataCoverageError("UngriddedData object does not contain any variables")
        if start is None and stop is None:
            start = pd.Timestamp("1970")
            stop = pd.Timestamp("2200")
        else:
            start, stop = start_stop(start, stop)

        if isinstance(meta_idx, str):
            # user asks explicitely for station name, find all meta indices
            # that match this station
            meta_idx = self.find_station_meta_indices(meta_idx, allow_wildcards_station_name)
        if not isinstance(meta_idx, list):
            meta_idx = [meta_idx]

        stats = []
        # ToDo: check consistency, consider using methods in helpers.py
        # check also Hans' issue on the topic
        start, stop = np.datetime64(start), np.datetime64(stop)

        for idx in meta_idx:
            try:
                stat = self._metablock_to_stationdata(
                    idx, vars_to_convert, start, stop, add_meta_keys
                )
                if ts_type_preferred is not None:
                    if "ts_type" in stat["var_info"][vars_to_convert[0]].keys():
                        if TsType(stat["var_info"][vars_to_convert[0]]["ts_type"]) < TsType(
                            ts_type_preferred
                        ):
                            continue
                    elif "ts_type" in stat.keys():
                        if TsType(stat["ts_type"]) < TsType(ts_type_preferred):
                            continue
                    else:
                        raise KeyError("Could not find ts_type in stat")
                stats.append(stat)
            except (VarNotAvailableError, DataCoverageError) as e:
                logger.debug(f"Skipping meta index {idx}. Reason: {repr(e)}")
        if merge_if_multi and len(stats) > 1:
            if len(vars_to_convert) > 1:
                raise NotImplementedError(
                    "Cannot yet merge multiple stations with multiple variables."
                )
            if merge_pref_attr is None:
                merge_pref_attr = self._try_infer_stat_merge_pref_attr(stats)
            merged = merge_station_data(
                stats,
                vars_to_convert,
                pref_attr=merge_pref_attr,
                sort_by_largest=merge_sort_by_largest,
                fill_missing_nan=False,
                resample_how=resample_how,
                min_num_obs=min_num_obs,
            )
            stats = [merged]

        stats_ok = []
        for stat in stats:
            for var in vars_to_convert:
                if var not in stat:
                    continue
                if freq is not None:
                    stat.resample_time(
                        var,
                        freq,
                        how=resample_how,
                        min_num_obs=min_num_obs,
                        inplace=True,
                    )
                elif insert_nans:
                    stat.insert_nans_timeseries(var)
                if np.all(np.isnan(stat[var].values)):
                    stat = stat.remove_variable(var)
            if any([x in stat for x in vars_to_convert]):
                stats_ok.append(stat)

        if len(stats_ok) == 0:
            raise DataCoverageError(
                f"{vars_to_convert} data could not be retrieved "
                f"for meta index (or station name) {meta_idx}"
            )
        elif len(stats_ok) == 1:
            # return StationData object and not list
            return stats_ok[0]
        return stats_ok

    ### TODO: check if both `variables` and `var_info` attrs are required in
    ### metdatda blocks
    def _metablock_to_stationdata(
        self, meta_idx, vars_to_convert, start=None, stop=None, add_meta_keys=None
    ):
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
        if "data_revision" in meta:
            rev = meta["data_revision"]
        else:
            try:
                rev = self.data_revision[meta["data_id"]]
            except Exception:
                logger.debug("Data revision could not be accessed")
        sd.data_revision = rev
        try:
            vars_avail = list(meta["var_info"])
        except KeyError:
            if "variables" not in meta or meta["variables"] in (None, []):
                raise VarNotAvailableError("Metablock does not contain variable information")
            vars_avail = meta["variables"]

        for key in self.STANDARD_META_KEYS + add_meta_keys:
            if key in sd.PROTECTED_KEYS:
                logger.warning(f"skipping protected key: {key}")
                continue
            try:
                sd[key] = meta[key]
            except KeyError:
                pass

        try:
            sd["ts_type_src"] = meta["ts_type"]
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
            raise VarNotAvailableError(
                "None of the input variables matches, or station does not contain data."
            )
        # init helper boolean that is set to True if valid data can be found
        # for at least one of the input variables
        FOUND_ONE = False
        for var in vars_avail:
            # get indices of this station and variable
            var_idx = np.isin(self._data["meta_id"], meta_idx) & np.isin(self._data["var_id"], var)

            # get subset
            subset = self._data[var_idx]

            # vector of timestamps corresponding to this variable
            dtime = subset["start_time"]

            # make sure to extract only valid timestamps
            if start is None:
                start = dtime.min()
            if stop is None:
                stop = dtime.max()

            # create access mask for valid time stamps
            tmask = (dtime >= start) & (dtime <= stop)

            # make sure there is some valid data
            if tmask.sum() == 0:
                logger.debug(
                    f"Ignoring station {sd['station_name']}, var {var} ({sd['data_id']}): "
                    f"no data available in specified time interval {start} - {stop}"
                )
                continue

            dtime = dtime[tmask]
            subset = subset[tmask]

            vals = subset["data"]
            if np.all(np.isnan(vals)):
                logger.debug(
                    f"Ignoring station {sd['station_name']}, var {var} ({sd['data_id']}): "
                    f"All values are NaN"
                )
                continue
            vals_err = subset["stdev"]
            flag_mask = subset["flag"] == self._nan_types["flag"]
            flagged = subset["flag"].astype("f4")
            flagged[flag_mask] = np.nan
            alt_mask = subset["flag"] == self._nan_types["flag"]
            altitude = subset["height"].astype("f4")
            altitude[alt_mask] = np.nan

            data = pd.Series(vals, dtime)
            if not data.index.is_monotonic_increasing:
                data = data.sort_index()
            if any(~np.isnan(vals_err)):
                sd.data_err[var] = vals_err
            if any(~np.isnan(flagged)):
                sd.data_flagged[var] = flagged

            sd["dtime"] = data.index.values
            sd[var] = data
            sd["var_info"][var] = {}
            FOUND_ONE = True
            # check if there is information about altitude (then relevant 3D
            # variables and parameters are included too)
            if "var_info" in meta:
                vi = meta["var_info"]
            else:
                vi = {}
            if not np.isnan(altitude).all():
                if "altitude" in vi:
                    sd.var_info["altitude"] = vi["altitude"]
                sd.altitude = altitude
            if var in vi:
                sd.var_info[var].update(vi[var])

            if len(data.index) == len(data.index.unique()):
                sd.var_info[var]["overlap"] = False
            else:
                sd.var_info[var]["overlap"] = True
        if not FOUND_ONE:
            raise DataCoverageError(
                f"Could not retrieve any valid data for station {sd['station_name']} "
                f"and input variables {vars_to_convert}"
            )
        return sd

    @property
    @override
    def is_filtered(self):
        if len(self.filter_hist) > 0:
            return True
        return False
