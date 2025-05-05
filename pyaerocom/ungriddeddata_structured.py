import fnmatch
import logging
import sys
from collections.abc import Iterator
from copy import deepcopy

import numpy as np
import numpy.typing as npt
import pandas as pd
from pyaro.timeseries import Reader

from pyaerocom import const
from pyaerocom.dynamic_rec_array import DynamicRecArray
from pyaerocom.exceptions import (
    DataCoverageError,
    DataExtractionError,
    VarNotAvailableError,
)
from pyaerocom.helpers import merge_station_data, start_stop
from pyaerocom.metastandards import STANDARD_META_KEYS
from pyaerocom.stationdata import StationData
from pyaerocom.ungridded_data_container import UngriddedDataContainer
from pyaerocom.ungridded_data_metadata import UngriddedDataMetadata
from pyaerocom.units.datetime import TsType
from pyaerocom.units.helpers import get_standard_unit

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

logger = logging.getLogger(__name__)


class UngriddedDataStructured(UngriddedDataMetadata):
    """Class implementing UngriddedData in a numpy structured array"""

    __version__ = "0.01"
    _merging_error_logged = False

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
                if var in stat.data_flagged:
                    if len(stat.data_flagged[var]) != len(stat.dtime):
                        del stat.data_flagged[var]
                        if not self._merging_error_logged:
                            self._merging_error_logged = True
                            logger.warning(
                                "merging of station-data objects introduced rubbish flags, removing"
                            )
                if var in stat.data_err:
                    if len(stat.data_err[var]) != len(stat.dtime):
                        del stat.data_err[var]
                        if not self._merging_error_logged:
                            self._merging_error_logged = True
                            logger.warning(
                                "merging of station-data objects introduced rubbish stddev, removing"
                            )
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
                rev = self.get_data_revision(meta["data_id"])
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

            series = pd.Series(vals, dtime)
            if not series.index.is_monotonic_increasing:
                series = series.sort_index()
            if any(~np.isnan(vals_err)):
                sd.data_err[var] = vals_err
            if any(~np.isnan(flagged)):
                sd.data_flagged[var] = flagged

            sd["dtime"] = series.index.values
            sd[var] = series
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
                sd.altitude = altitude[0]  # TODO: Revise in case of moving stations
            if var in vi:
                sd.var_info[var].update(vi[var])

            if len(series.index) == len(series.index.unique()):
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

    @override
    def remove_outliers(
        self,
        var_name,
        inplace=False,
        low=None,
        high=None,
        move_to_trash=True,
    ):
        """see super.remove_outliers move_to_trash is ignored for now"""
        if inplace:
            new = self
        else:
            new = self.copy()

        new.check_unit(var_name)

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
            if "data_revision" in station_data:
                self.metadata[meta_idx]["data_revision"] = station_data.data_revision

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

                if "units" in self.metadata[meta_idx]["var_info"][var]:
                    u1 = self.metadata[meta_idx]["var_info"][var]
                    # u2 = station_data["var_info"][var]["units"]
                    station_data.convert_unit(var, u1)
                else:
                    station_data.convert_unit(var, get_standard_unit(var))
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
                    v_data["flag"][:] = flags
                    nans = ~np.isfinite(flags)
                    v_data["flag"][nans] = UngriddedDataStructured._nan_types["flag"]
                self._dra.append(v_data)

    @staticmethod
    def from_pyaro(
        data_id: str, reader: Reader, vars_to_retrieve: list[str], **kwargs
    ) -> UngriddedDataContainer:
        """Convert data from a pyaro-reader to UngriddedDataStructured

        :param data_id: data_id identifier
        :param reader: pyaro-reader
        :param vars_to_retrieve: selection of variables
        :param kwargs: internal parameters for testing/benchmarking
        :return: data as UngriddedDataContainer
        """

        def _calculate_ts_type(
            start: npt.NDArray[np.datetime64], end: npt.NDArray[np.datetime64]
        ) -> npt.NDArray:
            """convert start and end-time arrays to a ts-type array

            :param start: start-times
            :param end: end-times
            :return: ts-types as string-array
            """
            seconds = (end - start).astype("timedelta64[s]").astype(np.int32)

            # below line is the same as
            # uniq_seconds = np.sort(np.unique(seconds))
            # but several orders of magnitude faster for large array with only few distinct elements
            uniq_seconds = np.sort(np.nonzero(np.bincount(seconds))[0])

            @np.vectorize(otypes=[str])
            def memoized_ts_type(x: np.int32) -> str:
                if x == 0:
                    return TsType("hourly")
                return str(TsType.from_total_seconds(x))

            uniq_tstypes = memoized_ts_type(uniq_seconds)

            # Use np.searchsorted to find indices of structured_array elements in sorted_keys
            indices = np.searchsorted(uniq_seconds, seconds)

            # Use np.take to map indices to values
            return np.take(uniq_tstypes, indices)

        def _station_tstype_to_int_array(
            sarray: np.ndarray, mapping: dict[tuple[str, str], int]
        ) -> np.ndarray:
            """converter an array-view consisting of two str columns ("stations", "tstype") to an
            int-array using a mapping

            :param sarray: station,tstype view of a structured array
            :param mapping: (station,tstype) -> int mapping dictionary
            :return: array of ints
            """
            keys = np.array(
                list(mapping.keys()),
                dtype=[
                    ("stations", sarray["stations"].dtype),
                    ("tstype", sarray["tstype"].dtype),
                ],
            )
            values = np.array(list(mapping.values()), dtype="i4")

            # Sort keys to ensure correct indexing
            sorted_indices = np.argsort(keys)
            sorted_keys = keys[sorted_indices]
            sorted_values = values[sorted_indices]

            # Use np.searchsorted to find indices of structured_array elements in sorted_keys
            indices = np.searchsorted(sorted_keys, sarray)

            # Use np.take to map indices to values
            return np.take(sorted_values, indices)

        class _VariableMetaIds:
            """Class containing for each variable a dictionary of tuples of station and ts_type to
            the corresponding meta-d
            """

            def __init__(self):
                self._counter: int = 0
                # a meta must be split by variable as well as station and tstype
                # dictionary about var_meta[var][(station,ts_type)] = meta_id
                self._mapping: dict[str, dict[tuple[str, str], int]] = {}

            def append_var_station_tstype(
                self,
                var: str,
                station_tstype: np.ndarray | None,
            ):
                """append values of an array containing station and ts_type tuples
                :param var: variable
                :param station_tstype: structured array of stations and tstype
                """
                if var not in self._mapping:
                    self._mapping[var] = {}
                if len(station_tstype) == 0:
                    return

                mapping = self._mapping[var]
                # below line is for EEA-data about 10x faster than
                # uarray = np.unique(station_tstype, axis=0)
                uarray = np.array(list(set(station_tstype.tolist())), dtype=station_tstype.dtype)

                for row in uarray:
                    sx = (row[0], row[1])
                    if sx not in mapping:
                        mapping[sx] = self._counter
                        self._counter += 1
                return

            def __getitem__(self, var) -> dict[tuple[str, str], int]:
                """Get the (stations, tstype) -> metaid dictionary

                :param var: variable name
                :return: dictionary of tuple of stations and tstype to meta_ids
                """
                return self._mapping[var]

        ugs = UngriddedDataStructured()
        ugs.var_idx = {var: i for i, var in enumerate(vars_to_retrieve)}

        # a meta must be split by variable as well as station and tstype
        var_metas = _VariableMetaIds()
        # unit dictionary, var_units[var] = unit
        var_units: dict[str, str] = {}
        for var in vars_to_retrieve:
            logger.info(f"Getting data of {var} from pyaro/{data_id}")
            if "bench_dataset" in kwargs:
                var_data = kwargs["bench_dataset"]
            else:
                var_data = reader.data(varname=var)
            logger.info(f"Converting data of {var} from pyaro/{data_id} to ungridded")
            tstype = _calculate_ts_type(start=var_data.start_times, end=var_data.end_times)
            stations = var_data.stations
            station_tstype = np.rec.array(
                [stations, tstype],
                dtype=[("stations", stations.dtype), ("tstype", tstype.dtype)],
            )

            # set meta-ids for each variable but ensure that counter
            # is for all vars, var_metas contain (stations, tstype) tuples
            var_metas.append_var_station_tstype(var, station_tstype)
            if len(var_data) == 0:
                continue

            var_units[var] = var_data.units
            dra_data = {
                "meta_id": _station_tstype_to_int_array(station_tstype, var_metas[var]),
                "var_id": np.zeros(len(var_data), dtype="i2") + ugs.var_idx[var],
                "start_time": var_data.start_times,
                "end_time": var_data.end_times,
                "data": var_data.values,
                "stdev": var_data.standard_deviations,
                "dataaltitude": var_data.altitudes.astype("i2"),
                "flag": var_data.flags,  # TODO check for common undefined values?
            }
            ugs._dra.append_array(**dra_data)

        logger.info(f"Converting metadata from pyaro/{data_id} to ungridded")
        rev = None
        if "revision" in reader.metadata():
            rev = reader.metadata()["revision"]
        else:
            logger.warning(
                f"pyaro/{data_id} does not contain a 'revision', please inform data-provider, or pyaro-readers"
            )

        stations_with_metadata = reader.stations()
        for var in vars_to_retrieve:
            for station_tstype, meta_id in var_metas[var].items():
                (station_name, tstype) = station_tstype
                extra_metadata = stations_with_metadata[station_name].metadata
                d = {
                    "data_id": data_id,
                    "data_revision": rev,
                    "station_name": station_name,
                    "var_info": {
                        var: {"units": var_units[var]},
                    },
                    **stations_with_metadata[station_name],
                    **extra_metadata,
                }
                if "ts_type" not in d:
                    d["ts_type"] = tstype
                ugs.metadata[meta_id] = d

        logger.info(f"Finished converting from pyaro/{data_id} to UngriddedDataStructured")

        return ugs

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
        # faster implementation of: distinct_metas = np.unique(obj._dra.data["meta_id"])
        distinct_metas = np.nonzero(np.bincount(obj._dra.data["meta_id"]))[0]

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
