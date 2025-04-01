import fnmatch
import logging
import sys
from collections.abc import Iterator
from copy import deepcopy

import numpy as np
import pandas as pd

from pyaerocom import const
from pyaerocom.dynamic_rec_array import DynamicRecArray
from pyaerocom.exceptions import (
    DataCoverageError,
    DataExtractionError,
    MetaDataError,
    VarNotAvailableError,
)
from pyaerocom.helpers import merge_station_data, start_stop
from pyaerocom.metastandards import STANDARD_META_KEYS
from pyaerocom.stationdata import StationData
from pyaerocom.ungridded_data_metadata import UngriddedDataMetadata
from pyaerocom.units.datetime import TsType
from pyaerocom.units.units_helpers import get_unit_conversion_fac

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

logger = logging.getLogger(__name__)


class UngriddedDataStructured(UngriddedDataMetadata):
    """Class implementing UngriddedData in a numpy structured array"""

    __version__ = "0.01"

    _dtype = [
        ("meta_id", "i4"),
        ("var_id", "i2"),
        ("start_time", "datetime64[s]"),
        ("end_time", "datetime64[s]"),
        ("data", "f"),  # data-value
        ("stdev", "f"),  # data-error
        (
            "dataaltitude",
            "i2",
        ),  # altitude of measurement (might be different from station)
        ("flag", "i2"),
    ]
    _nan_types = {
        "meta_id": np.iinfo("i4").min,
        "var_id": np.iinfo("i2").min,
        "start_time": np.datetime64("NaT"),
        "end_time": np.datetime64("NaT"),
        "data": np.nan,
        "stdev": np.nan,
        "dataaltitude": np.iinfo("i2").min,
        "flag": np.iinfo("i2").min,
    }

    def __init__(self, num_points: int = 100):
        super().__init__()  # initialize metadata
        self._dra = self._create_data_chunk(num_points)

        # filters applied
        self.filter_hist = {}

        self._is_vertical_profile = False

    @override
    def _new_from_meta_blocks(self, meta_ids: list, total: int = 100):
        # check for new variables of the stations
        new_var_idx = {}
        new_metadata = {}
        for meta_id in meta_ids:
            meta = self.metadata[meta_id]
            new_metadata[meta_id] = meta
            for var in meta["var_info"]:
                if var in self.ALLOWED_VERT_COORD_TYPES:
                    continue
                new_var_idx[var] = self.var_idx[var]

        midx = np.isin(self._dra.data["meta_id"], meta_ids)
        # data with the selected stations
        nd = self._dra.data[midx]
        size = len(nd)
        if size == 0:
            raise DataExtractionError("Filtering results in empty data object")

        new = self.__class__(size)
        new._dra.data = nd
        new.metadata = new_metadata
        new.var_idx = new_var_idx
        new.filter_hist = self.filter_hist
        new._is_vertical_profile = self._is_vertical_profile

        return new

    def _create_data_chunk(self, size):
        """create a datachunk of size and initialize it to _nan_type values"""
        data = DynamicRecArray(capacity=size, dtype=self._dtype)
        for k, v in self._nan_types.items():
            data._array[k] = v
        return data

    @override
    def copy(self):
        new = self.__class__()
        self._copy_metadata_to(new)
        new._dra = deepcopy(self._dra)
        return new

    @property
    @override
    def shape(self):
        return self._dra.data.shape

    @property
    @override
    def has_flag_data(self):
        return (self._dra.data["flag"] != self._nan_types["flag"]).any()

    @override
    def set_flags_nan(self, inplace=False):
        if not self.has_flag_data:
            raise AttributeError("Ungridded data object does not contain flagged data points")
        if inplace:
            obj = self
        else:
            obj = self.copy()

        obj._dra.data["flag"] = self._nan_types["flag"]
        obj._add_to_filter_history("set_flags_nan")
        return obj

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
            # user asks explicitly for station name, find all meta indices
            # that match this station
            meta_idx = self.find_station_meta_indices(meta_idx, allow_wildcards_station_name)
        if not isinstance(meta_idx, list):
            meta_idx = [meta_idx]

        stats = []
        start, stop = np.datetime64(start), np.datetime64(stop)

        if len(meta_idx) > 1:
            sub_idx = np.isin(self._dra.data["meta_id"], meta_idx)
            subdata = self._dra.data[sub_idx]
        else:
            subdata = self._dra.data
        for idx in meta_idx:
            try:
                stat = self._metablock_to_stationdata(
                    idx, vars_to_convert, start, stop, add_meta_keys, data=subdata
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

    def _metablock_to_stationdata(
        self,
        meta_idx,
        vars_to_convert,
        start=None,
        stop=None,
        add_meta_keys=None,
        data=None,
    ):
        """Convert one metadata index to StationData (helper method)

        Data might be a pre-computed internal dataset.

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

        for key in STANDARD_META_KEYS + add_meta_keys:
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

        # assign station coordinates explicitly
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
        if data is None:
            data = self._dra.data
        FOUND_ONE = False
        for var in vars_avail:
            # get indices of this station and variable
            idx = (data["meta_id"] == meta_idx) & (data["var_id"] == self.var_idx[var])

            # get subset
            subset = data[idx]

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
            alt_mask = subset["dataaltitude"] == self._nan_types["dataaltitude"]
            altitude = subset["dataaltitude"].astype("f4")
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
            assert isinstance(vi, dict)
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

    @override
    def _generate_station_index(self, by_station_name=True, ignore_index=None):
        """Generates index to loop over station names or metadata block indices.
        Needs to be implemented for :func:`to_station_data_all` to work"""
        if ignore_index is None:
            if by_station_name:
                return self.unique_station_names  # all station names
            return list(range(len(self.metadata)))  # all meta indices

        if not by_station_name:
            from pyaerocom.helpers import isnumeric

            if isnumeric(ignore_index):
                ignore_index = [ignore_index]
            if not isinstance(ignore_index, list):
                raise ValueError("Invalid input for ignore_index, need number or list")
            return [i for i in range(len(self.metadata)) if i not in ignore_index]

        # by station name and ignore certation stations
        _iter = []
        if isinstance(ignore_index, str):
            ignore_index = [ignore_index]
        if not isinstance(ignore_index, list):
            raise ValueError("Invalid input for ignore_index, need str or list")
        for stat_name in self.unique_station_names:
            ok = True
            for name_or_pattern in ignore_index:
                if fnmatch.fnmatch(stat_name, name_or_pattern):
                    ok = False
            if ok:
                _iter.append(stat_name)
        return _iter

    def check_convert_var_units(self, var_name, to_unit=None, inplace=True):
        obj = self if inplace else self.copy()

        # get the unit
        if to_unit is None:
            to_unit = const.VARS[var_name]["units"]

        for meta_idx, meta in obj.metadata.items():
            if var_name in meta["var_info"]:
                try:
                    unit = meta["var_info"][var_name]["units"]
                except KeyError:
                    add_str = ""
                    if "unit" in meta["var_info"][var_name]:
                        add_str = (
                            "Corresponding var_info dict contains "
                            'attr. "unit", which is deprecated, please '
                            "check corresponding reading routine. "
                        )
                    raise MetaDataError(
                        f"Failed to access unit information for variable {var_name} "
                        f"in metadata block {meta_idx}. {add_str}"
                    )
                fac = get_unit_conversion_fac(unit, to_unit, var_name)
                if fac != 1:
                    idx = (obj._dra.data["meta_id"] == meta_idx) & (
                        obj._dra.data["var_id"] == self.var_idx[var_name]
                    )
                    obj._dra.data["data"][idx] *= fac
                meta["var_info"][var_name]["units"] = to_unit

        return obj

    @override
    def remove_outliers(
        self,
        var_name,
        inplace=False,
        low=None,
        high=None,
        unit_ref=None,
        move_to_trash=True,
    ):
        """see super.remove_outliers move_to_trash is ignored for now"""
        if inplace:
            new = self
        else:
            new = self.copy()

        new.check_convert_var_units(var_name, to_unit=unit_ref)

        if low is None:
            low = const.VARS[var_name].minimum
            logger.info(f"Setting {var_name} outlier lower lim: {low:.2f}")
        if high is None:
            high = const.VARS[var_name].maximum
            logger.info(f"Setting {var_name} outlier upper lim: {high:.2f}")
        var_idx = new.var_idx[var_name]
        var_mask = new._dra.data["var_id"] == var_idx

        all_data = new._dra.data["data"]
        invalid_mask = np.logical_or(all_data < low, all_data > high)

        mask = invalid_mask * var_mask
        invalid_vals = new._dra.data["data"][mask]
        new._dra.data["data"][mask] = np.nan

        if move_to_trash:
            logger.warning("trash not implemented")

        new._add_to_filter_history(
            f"Removed {len(invalid_vals)} outliers from {var_name} data "
            f"(range: {low}-{high}, in trash: {move_to_trash})"
        )
        return new

    @override
    def _len_datapoints(self, meta_idx, var):
        if isinstance(meta_idx, float):
            meta_idx = [meta_idx]
        if isinstance(var, str):
            var = [var]
        var_idx = [self.var_idx[v] for v in var]
        return np.sum(
            np.isin(self._dra.data["meta_id"], meta_idx)
            & np.isin(self._dra.data["var_id"], var_idx)
        )

    @override
    def extract_vars(self, var_names, check_index=True):
        var_names_unaliased = []
        for var_name in var_names:
            if var_name in self.contains_vars:
                var_names_unaliased.append(var_name)
            else:
                # try alias
                _var = const.VARS[var_name].var_name_aerocom
                if _var in self.contains_vars:
                    var_names_unaliased.append(_var)
                else:
                    raise VarNotAvailableError(f"No such variable {var_name} in data")

        var_ids = [self.var_idx[x] for x in var_names_unaliased]
        idx = np.isin(self._dra.data["var_id"], var_ids)
        new = self.__class__()
        new._dra.data = deepcopy(self._dra.data[idx])
        # fix the metadata
        self._copy_metadata_to(new)
        for i, var in enumerate(var_names):
            new.var_idx[var] = var_ids[i]
        new.metadata = {}
        for meta_id, meta in self.metadata.items():
            common_vars = [var for var in var_names if var in meta["var_info"]]
            if len(common_vars):
                new.metadata[meta_id] = deepcopy(meta)
                new.metadata[meta_id]["var_info"] = {}
                new.metadata[meta_id]["variables"] = common_vars
                for var in common_vars:
                    new.metadata[meta_id]["var_info"][var] = deepcopy(meta["var_info"][var])
        return new

    @override
    def extract_var(self, var_name, check_index=True):
        new = self.extract_vars([var_name], check_index)
        new.filter_hist.update(self.filter_hist)
        new._add_to_filter_history(
            f"Created {var_name} single var object from multivar UngriddedData instance"
        )
        return new

    @override
    def all_datapoints_var(self, var_name):
        return self.extract_var(var_name)._dra.data["data"]

    @override
    def append_station_data(
        self,
        stats: StationData | Iterator[StationData],
        add_meta_keys: list[str] = [],
    ):
        if isinstance(stats, StationData):
            stats = [stats]
        # last meta_idx
        meta_idx = np.max(self._dra._array["meta_id"])
        if meta_idx == self._nan_types["meta_id"]:
            meta_idx = -1  # start at 0
        for station_data in stats:
            meta_idx += 1
            if not isinstance(station_data, StationData):
                raise ValueError("Need instances of StationData or dicts")

            # each file is a metadata-set of its own
            self.metadata[meta_idx] = {}
            self.metadata[meta_idx].update(
                station_data.get_meta(
                    force_single_value=False, quality_check=False, add_none_vals=True
                )
            )
            for key in add_meta_keys:
                if key in station_data:
                    self.metadata[meta_idx][key] = station_data[key]
            contains_vars = list(station_data.var_info)
            self.metadata[meta_idx]["variables"] = contains_vars

            for var in contains_vars:
                vardata = station_data[var]
                if isinstance(vardata, pd.Series):
                    times = vardata.index
                    values = vardata.values
                else:
                    times = station_data["dtime"]
                    values = vardata
                    if not len(times) == len(values):
                        raise ValueError
                if var not in self.var_idx:
                    self.var_idx[var] = len(self.var_idx)
                var_idx = self.var_idx[var]
                self.metadata[meta_idx]["var_info"] = {}
                self.metadata[meta_idx]["var_info"][var] = {}
                self.metadata[meta_idx]["var_info"][var].update(station_data["var_info"][var])
                for x in ("longitude", "latitude", "altitude"):
                    if x not in self.metadata[meta_idx]["var_info"][var]:
                        self.metadata[meta_idx]["var_info"][var][x] = station_data[x]

                uds = UngriddedDataStructured(num_points=len(values))
                v_data = uds._dra._array  # access to raw numpy-array
                v_data["meta_id"][:] = meta_idx
                v_data["var_id"][:] = var_idx
                v_data["data"] = values
                v_data["start_time"] = times
                # v_data["end_time"] not used
                # v_data["dataaltitude"] not used
                if var in station_data.data_err:
                    v_data["stdev"] = station_data.data_err[var]
                if var in station_data.data_flagged:
                    flags = station_data.data_flagged[var]
                    nans = ~np.isfinite(flags)
                    v_data["flag"][:] = flags
                    v_data["flag"][nans] = UngriddedDataStructured._nan_types["flag"]
                self._dra.append(v_data)

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

        meta_no_data = []
        distinct_metas = np.unique(obj._dra.data["meta_id"])
        for meta_idx, meta in obj.metadata.items():
            if not np.any(distinct_metas == meta_idx):
                # sanity check
                if bool(meta["var_info"]):
                    raise AttributeError(
                        "meta_idx {} suggests empty data block "
                        "but metadata[{}] contains variable "
                        "information"
                    )
                else:
                    meta_no_data.append(meta_idx)
        if len(meta_no_data):
            for meta_idx in meta_no_data:
                del obj.metadata[meta_idx]
        if len(obj.metadata) == 0:
            raise DataCoverageError("UngriddedData object appears to be empty")

        obj._add_to_filter_history(
            f"Removed {len(meta_no_data)} metadata blocks that have no data assigned"
        )
        return obj
