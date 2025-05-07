from __future__ import annotations

import fnmatch
import logging
from datetime import datetime
from typing import Any

import numpy as np
import numpy.typing as npt
import pandas as pd

from pyaerocom import const
from pyaerocom._lowlevel_helpers import merge_dicts
from pyaerocom.combine_vardata_ungridded import combine_vardata_ungridded
from pyaerocom.exceptions import (
    DataCoverageError,
    DataExtractionError,
    MetaDataError,
    StationCoordinateError,
    TimeMatchError,
    VarNotAvailableError,
)
from pyaerocom.geodesy import get_country_info_coords
from pyaerocom.helpers import merge_station_data, same_meta_dict, start_stop
from pyaerocom.metastandards import STANDARD_META_KEYS
from pyaerocom.stationdata import StationData
from pyaerocom.ungridded_data_metadata import UngriddedDataMetadata
from pyaerocom.units.datetime import TsType
from pyaerocom.units.units_helpers import get_unit_conversion_fac

logger = logging.getLogger(__name__)


class UngriddedData(UngriddedDataMetadata):
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
    metadata : dict[float, dict[str, Any]]
        dictionary containing meta information about the data. Keys are
        floating point numbers corresponding to each station, values are
        corresponding dictionaries containing station information.
    meta_idx : dict[float, dict[str, list[int]]]
        dictionary containing index mapping for each station and variable. Keys
        correspond to metadata key (float -> station, see :attr:`metadata`) and
        values are dictionaries containing keys specifying variable name and
        corresponding values are arrays or lists, specifying indices (rows) of
        these station / variable information in :attr:`_data`. Note: this
        information is redundant and is there to accelerate station data
        extraction since the data index matches for a given metadata block
        do not need to be searched in the underlying numpy array.
    var_idx : dict[str, float]
        mapping of variable name (keys, e.g. od550aer) to numerical variable
        index of this variable in data numpy array (in column specified by
        :attr:`_VARINDEX`)

    Parameters
    ----------
    num_points : :obj:`int`, optional
        initial number of total datapoints (number of rows in 2D dataarray)
    add_cols : :obj:`list`, optional
        list of additional index column names of 2D datarray.

    """

    #: version of class (for caching)
    __version__ = "0.22"

    #: default number of rows that are dynamically added if total number of
    #: data rows is reached.
    _CHUNKSIZE = 10000000

    #: The following indices specify what the individual rows of the datarray
    #: are reserved for. These may be expanded when creating an instance of
    #: this class by providing a list of additional index names.
    _METADATAKEYINDEX = 0
    _TIMEINDEX = 1
    _LATINDEX = 2
    _LONINDEX = 3
    _ALTITUDEINDEX = 4  # altitude of measurement device
    _VARINDEX = 5
    _DATAINDEX = 6
    _DATAHEIGHTINDEX = 7
    _DATAERRINDEX = 8  # col where errors can be stored
    _DATAFLAGINDEX = 9  # can be used to store flags
    _STOPTIMEINDEX = 10  # can be used to store stop time of acq.
    _TRASHINDEX = 11  # index where invalid data can be moved to (e.g. when outliers are removed)

    # The following number denotes the kept precision after the decimal dot of
    # the location (e.g denotes lat = 300.12345)
    # used to code lat and long in a single number for a uniqueness test
    _LOCATION_PRECISION = 5
    _LAT_OFFSET = 90.0

    @property
    def _ROWNO(self):
        return self._data.shape[0]

    def __init__(self, num_points=None, add_cols=None):
        super().__init__()  # initialize metadata
        if num_points is None:
            num_points = self._CHUNKSIZE

        self._chunksize = num_points
        self._index = self._init_index(add_cols)

        # keep private, this is not supposed to be used by the user
        self._data = np.full([num_points, self._COLNO], np.nan)
        self.meta_idx = {}
        self._idx = -1

    @staticmethod
    def _from_raw_parts(
        data: npt.NDTArray[float],
        metadata: dict[float, dict[str, Any]],
        meta_idx: dict[float, dict[str, list[int]]],
        var_idx: dict[str, float],
    ) -> UngriddedData:
        data_obj = UngriddedData()

        data_obj._data = data
        data_obj.meta_idx = meta_idx
        data_obj.metadata = metadata
        data_obj.var_idx = var_idx

        return data_obj

    def _check_index(self):
        """Checks if all indices are assigned correctly"""
        assert len(self.meta_idx) == len(self.metadata), "Mismatch len(meta_idx) and len(metadata)"

        assert sum(self.meta_idx) == sum(
            self.metadata
        ), "Mismatch between keys of metadata dict and meta_idx dict"

        _varnums = self._data[:, self._VARINDEX]
        var_indices = np.unique(_varnums[~np.isnan(_varnums)])

        assert len(var_indices) == len(
            self.var_idx
        ), "Mismatch between number of variables in data array and var_idx attr."

        assert sum(var_indices) == sum(
            self.var_idx.values()
        ), "Mismatch between variable indices in data array and var_idx attr."

        vars_avail = self.var_idx

        for idx, meta in self.metadata.items():
            if "var_info" not in meta:
                if "variables" not in meta:
                    raise AttributeError(
                        f"Need either variables (list) or var_info (dict) "
                        f"in meta block {idx}: {meta}"
                    )
                meta["var_info"] = {}
                for v in meta["variables"]:
                    meta["var_info"][v] = {}

            var_idx = self.meta_idx[idx]
            for var, indices in var_idx.items():
                if len(indices) == 0:
                    continue  # no data assigned for this metadata index

                assert (
                    var in meta["var_info"]
                ), f"Var {var} is indexed in meta_idx[{idx}] but not in metadata[{idx}]"
                var_idx_data = np.unique(self._data[indices, self._VARINDEX])
                assert (
                    len(var_idx_data) == 1
                ), f"Found multiple variable indices for var {var}: {var_idx_data}"
                assert var_idx_data[0] == vars_avail[var], (
                    f"Mismatch between {var} index assigned in data and "
                    f"var_idx for {idx} in meta-block"
                )

    @staticmethod
    def from_station_data(
        stats: StationData, add_meta_keys: list[str] | None = None
    ) -> UngriddedData:
        """
        Create UngriddedData from input station data object(s)

        Parameters
        ----------
        stats : iterator or StationData
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
        UngriddedDataMeta
            ungridded data object created from input station data objects

        """
        if add_meta_keys is None:
            add_meta_keys = []
        elif isinstance(add_meta_keys, str):
            add_meta_keys = [add_meta_keys]
        elif not isinstance(add_meta_keys, list):
            raise ValueError(f"Invalid input for add_meta_keys {add_meta_keys}... need list")
        if isinstance(stats, StationData):
            stats = [stats]
        data_obj = UngriddedData()

        meta_key = 0.0
        idx = 0

        metadata = data_obj.metadata
        meta_idx = data_obj.meta_idx

        var_count_glob = -1
        for stat in stats:
            if isinstance(stat, dict):
                stat = StationData(**stat)
            elif not isinstance(stat, StationData):
                raise ValueError("Need instances of StationData or dicts")
            metadata[meta_key] = {}
            metadata[meta_key].update(
                stat.get_meta(force_single_value=False, quality_check=False, add_none_vals=True)
            )
            for key in add_meta_keys:
                try:
                    val = stat[key]
                except KeyError:
                    val = "undefined"

                metadata[meta_key][key] = val

            metadata[meta_key]["var_info"] = {}

            meta_idx[meta_key] = {}

            append_vars = list(stat.var_info)

            for var in append_vars:
                if var not in data_obj.var_idx:
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
                    times = stat["dtime"]
                    values = vardata
                    if not len(times) == len(values):
                        raise ValueError

                times = np.asarray(
                    [
                        (
                            np.datetime64(x.replace(tzinfo=None), "s")
                            if isinstance(x, datetime)
                            else np.datetime64(x, "s")
                        )
                        for x in times
                    ]
                )
                times = times.astype(np.float64)

                num_times = len(times)
                # check if size of data object needs to be extended
                if (idx + num_times) >= data_obj._ROWNO:
                    # if totnum < data_obj._CHUNKSIZE, then the latter is used
                    data_obj.add_chunk(num_times)

                start = idx
                stop = start + num_times

                # write common meta info for this station (data lon, lat and
                # altitude are set to station locations)
                data_obj._data[start:stop, data_obj._LATINDEX] = stat["latitude"]
                data_obj._data[start:stop, data_obj._LONINDEX] = stat["longitude"]
                data_obj._data[start:stop, data_obj._ALTITUDEINDEX] = stat["altitude"]
                data_obj._data[start:stop, data_obj._METADATAKEYINDEX] = meta_key

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

                var_info = stat["var_info"][var]
                metadata[meta_key]["var_info"][var] = {}
                metadata[meta_key]["var_info"][var].update(var_info)
                meta_idx[meta_key][var] = np.arange(start, stop)

                idx += num_times

            meta_key += 1

        # shorten data_obj._data to the right number of points
        data_obj._data = data_obj._data[:idx]

        data_obj._check_index()

        return data_obj

    def add_station_data(
        self, stat, meta_idx=None, data_idx=None, check_index=False
    ):  # pragma: no cover
        raise NotImplementedError("Coming at some point")
        if meta_idx is None:
            meta_idx = self.last_meta_idx + 1
        elif meta_idx in self.meta_idx:
            raise ValueError(
                f"Cannot add data at meta block index {meta_idx}, index already exists"
            )

        if data_idx is None:
            data_idx = self._data.shape[0]
        elif not np.all(np.isnan(self._data[data_idx, :])):
            raise ValueError(f"Cannot add data at data index {data_idx}, index already exists")

    @property
    def last_meta_idx(self):
        """
        Index of last metadata block
        """
        return np.max(list(self.meta_idx))

    @property
    def index(self):
        return self._index

    def _init_index(self, add_cols=None):
        """Init index mapping for columns in dataarray"""
        idx = dict(
            meta=self._METADATAKEYINDEX,
            time=self._TIMEINDEX,
            stoptime=self._STOPTIMEINDEX,
            latitude=self._LATINDEX,
            longitude=self._LONINDEX,
            altitude=self._ALTITUDEINDEX,
            varidx=self._VARINDEX,
            data=self._DATAINDEX,
            dataerr=self._DATAERRINDEX,
            dataaltitude=self._DATAHEIGHTINDEX,
            dataflag=self._DATAFLAGINDEX,
            trash=self._TRASHINDEX,
        )

        next_idx = max(idx.values()) + 1
        if add_cols is not None:
            if not isinstance(add_cols, list | tuple):
                raise ValueError("Invalid input for add_cols. Need list or tuple")
            for name in add_cols:
                if name in idx:
                    raise ValueError(
                        f"Cannot add new index with name {name} since "
                        f"this index already exists at column position {idx[name]}"
                    )
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
        self._copy_metadata_to(new)
        new._data = np.copy(self._data)
        new.meta_idx = deepcopy(self.meta_idx)
        return new

    @property
    def shape(self):
        """Shape of data array"""
        return self._data.shape

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
        chunk = np.full([size, self._COLNO], np.nan)
        self._data = np.append(self._data, chunk, axis=0)
        logger.info(f"adding chunk, new array size ({self._data.shape})")

    def _get_stat_coords(self):
        meta_idx = []
        coords = []
        for idx, meta in self.metadata.items():
            try:
                lat, lon = meta["latitude"], meta["longitude"]
            except Exception:
                logger.warning(f"Could not retrieve lat lon coord at meta index {idx}")
                continue
            meta_idx.append(idx)
            coords.append((lat, lon))
        return (meta_idx, coords)

    def _check_set_country(self):
        """CHecks all metadata entries for availability of country information

        Deprecated - no longer used?

        Metadata blocks that are missing country entry will be updated based
        on country inferred from corresponding lat / lon coordinate. Uses
        :func:`pyaerocom.geodesy.get_country_info_coords` (library
        reverse-geocode) to retrieve countries. This may be errouneous
        close to country borders as it uses Euclidean distance based on a list
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
        # HK 2025-04-30
        logger.warning(
            "This method is deprecated because no usage could be found, except for tests for check_country_available"
        )
        meta_idx, coords = self._get_stat_coords()
        info = get_country_info_coords(coords)
        meta_idx_updated = []
        countries = []

        for i, idx in enumerate(meta_idx):
            meta = self.metadata[idx]
            if "country" not in meta or meta["country"] is None:
                country = info[i]["country"]
                meta["country"] = country
                meta["country_code"] = info[i]["country_code"]
                meta_idx_updated.append(idx)
                countries.append(country)
        return (meta_idx_updated, countries)

    # TODO: see docstring
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
                rev = self.get_data_revision[meta["data_id"]]
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
        FOUND_ONE = False
        for var in vars_avail:
            # get indices of this variable
            var_idx = self.meta_idx[meta_idx][var]

            # vector of timestamps corresponding to this variable
            dtime = self._data[var_idx, self._TIMEINDEX].astype("datetime64[s]")

            # get subset
            subset = self._data[var_idx]

            # make sure to extract only valid timestamps
            if start is None:
                start = dtime.min()
            if stop is None:
                stop = dtime.max()

            # create access mask for valid time stamps
            tmask = np.logical_and(dtime >= start, dtime <= stop)

            # make sure there is some valid data
            if tmask.sum() == 0:
                logger.debug(
                    f"Ignoring station {sd['station_name']}, var {var} ({sd['data_id']}): "
                    f"no data available in specified time interval {start} - {stop}"
                )
                continue

            dtime = dtime[tmask]
            subset = subset[tmask]

            vals = subset[:, self._DATAINDEX]
            if np.all(np.isnan(vals)):
                logger.debug(
                    f"Ignoring station {sd['station_name']}, var {var} ({sd['data_id']}): "
                    f"All values are NaN"
                )
                continue
            vals_err = subset[:, self._DATAERRINDEX]
            flagged = subset[:, self._DATAFLAGINDEX]
            altitude = subset[:, self._DATAHEIGHTINDEX]

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

    def _generate_station_index(self, by_station_name=True, ignore_index=None):
        """Generates index to loop over station names or metadata block indices"""
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

    def to_station_data_all(
        self,
        vars_to_convert=None,
        start=None,
        stop=None,
        freq=None,
        ts_type_preferred=None,
        by_station_name=True,
        ignore_index=None,
        **kwargs,
    ):
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
            5-element dictionary containing following key / value pairs:

                - stats: list of :class:`StationData` objects
                - station_name: list of corresponding station names
                - station_type: list of corresponding station types, might be empty
                - latitude: list of latitude coordinates
                - longitude: list of longitude coordinates

        """
        out_data = {
            "stats": [],
            "station_name": [],
            "station_type": [],
            "latitude": [],
            "failed": [],
            "longitude": [],
        }

        _iter = self._generate_station_index(by_station_name, ignore_index)
        for idx in _iter:
            try:
                data = self.to_station_data(
                    idx,
                    vars_to_convert,
                    start,
                    stop,
                    freq,
                    merge_if_multi=True,
                    allow_wildcards_station_name=False,
                    ts_type_preferred=ts_type_preferred,
                    **kwargs,
                )
                out_data["latitude"].append(data["latitude"])
                out_data["longitude"].append(data["longitude"])
                out_data["station_name"].append(data["station_name"])
                if hasattr(data, "station_type"):
                    out_data["station_type"].append(data["station_type"])
                else:
                    logger.debug(
                        "No station_type found in StationData, station_type will be blank"
                    )
                out_data["stats"].append(data)

            # catch the exceptions that are acceptable
            except (
                VarNotAvailableError,
                TimeMatchError,
                DataCoverageError,
                NotImplementedError,
                StationCoordinateError,
            ) as e:
                logger.debug(f"Failed to convert to StationData Error: {repr(e)}")
                out_data["failed"].append([idx, repr(e)])
        return out_data

    def check_convert_var_units(self, var_name, to_unit=None, inplace=True):
        obj = self if inplace else self.copy()

        # get the unit
        if to_unit is None:
            to_unit = const.VARS[var_name]["units"]

        for i, meta in obj.metadata.items():
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
                        f"in metadata block {i}. {add_str}"
                    )
                fac = get_unit_conversion_fac(unit, to_unit, var_name)
                if fac != 1:
                    meta_idx = obj.meta_idx[i][var_name]
                    current = obj._data[meta_idx, obj._DATAINDEX]
                    new = current * fac
                    obj._data[meta_idx, obj._DATAINDEX] = new
                    obj.metadata[i]["var_info"][var_name]["units"] = to_unit

        return obj

    def set_flags_nan(self, inplace=False):
        """Set all flagged datapoints to NaN

        Parameters
        ----------
        inplace : bool
            if True, the flagged datapoints will be set to NaN in this object,
            otherwise a new object will be created and returned

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
            raise AttributeError("Ungridded data object does not contain flagged data points")
        if inplace:
            obj = self
        else:
            obj = self.copy()
        mask = obj._data[:, obj._DATAFLAGINDEX] == 1

        obj._data[mask, obj._DATAINDEX] = np.nan
        obj._add_to_filter_history("set_flags_nan")
        return obj

    def remove_outliers(
        self,
        var_name,
        inplace=False,
        low=None,
        high=None,
        move_to_trash=True,
    ):
        """Method that can be used to remove outliers from data

        Parameters
        ----------
        var_name : str
            variable name
        inplace : bool
            if True, the outliers will be removed in this object, otherwise
            a new object will be created and returned
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

        new.check_unit(var_name)

        if low is None:
            low = const.VARS[var_name].minimum
            logger.info(f"Setting {var_name} outlier lower lim: {low:.2f}")
        if high is None:
            high = const.VARS[var_name].maximum
            logger.info(f"Setting {var_name} outlier upper lim: {high:.2f}")
        var_idx = new.var_idx[var_name]
        var_mask = new._data[:, new._VARINDEX] == var_idx

        all_data = new._data[:, new._DATAINDEX]
        invalid_mask = np.logical_or(all_data < low, all_data > high)

        mask = invalid_mask * var_mask
        invalid_vals = new._data[mask, new._DATAINDEX]
        new._data[mask, new._DATAINDEX] = np.nan

        if move_to_trash:
            # check if trash is empty and put outliers into trash
            trash = new._data[mask, new._TRASHINDEX]
            if np.isnan(trash).sum() == len(trash):  # trash is empty
                new._data[mask, new._TRASHINDEX] = invalid_vals
            else:
                raise ValueError(
                    "Trash is not empty for some of the datapoints. "
                    "Please empty trash first using method "
                    ":func:`empty_trash` or deactivate input arg "
                    ":attr:`move_to_trash`"
                )

        new._add_to_filter_history(
            f"Removed {len(invalid_vals)} outliers from {var_name} data "
            f"(range: {low}-{high}, in trash: {move_to_trash})"
        )
        return new

    def empty_trash(self):
        """Set all values in trash column to NaN"""
        self._data[:, self._TRASHINDEX] = np.nan

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
            new.meta_idx[meta_idx_new] = {}
            for var in meta["var_info"]:
                if var in self.ALLOWED_VERT_COORD_TYPES:
                    continue
                indices = self.meta_idx[meta_idx][var]
                totnum = len(indices)

                stop = data_idx_new + totnum
                while stop > new._data.shape[0]:
                    new.add_chunk()
                new._data[data_idx_new:stop, :] = self._data[indices, :]
                new._data[data_idx_new:stop, new._METADATAKEYINDEX] = meta_idx_new
                new.meta_idx[meta_idx_new][var] = np.arange(data_idx_new, stop)
                new.var_idx[var] = self.var_idx[var]
                data_idx_new += totnum

            meta_idx_new += 1

        if meta_idx_new == 0 or data_idx_new == 0:
            raise DataExtractionError("Filtering results in empty data object")
        new._data = new._data[:data_idx_new]

        # write history of filtering applied
        new.filter_hist.update(self.filter_hist)
        new._data_revision.update(self._data_revision)

        return new

    def _len_datapoints(self, meta_idx, var):
        """Get the number of datapoints for meta_idx and var."""
        if isinstance(meta_idx, float):
            meta_idx = [meta_idx]
        if isinstance(var, str):
            var = [var]
        totnum = 0
        for m in meta_idx:
            for v in var:
                try:
                    totnum += len(self.meta_idx[m][v])
                except KeyError:
                    logger.debug(
                        f"Ignoring variable {var} in meta block {meta_idx} "
                        f"since no data could be found"
                    )
        return

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
        meta_new = {}
        meta_idx_new = {}
        for idx, val in obj.meta_idx.items():
            meta = obj.metadata[idx]
            if not bool(val):  # no data assigned with this metadata block
                # sanity check
                if bool(meta["var_info"]):
                    raise AttributeError(
                        "meta_idx {} suggests empty data block "
                        "but metadata[{}] contains variable "
                        "information"
                    )
            else:
                meta_new[idx] = meta
                meta_idx_new[idx] = val
        num_removed = len(obj.metadata) - len(meta_new)
        if not bool(meta_new):
            raise DataCoverageError("UngriddedData object appears to be empty")
        elif num_removed > 0:  # some meta blocks are empty
            obj.metadata = meta_new
            obj.meta_idx = meta_idx_new

        obj._add_to_filter_history(
            f"Removed {num_removed} metadata blocks that have no data assigned"
        )
        obj._check_index()
        return obj

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
        if var_name not in self.contains_vars:
            # try alias
            _var = const.VARS[var_name].var_name_aerocom
            if _var in self.contains_vars:
                var_name = _var
            else:
                raise VarNotAvailableError(f"No such variable {var_name} in data")
        elif len(self.contains_vars) == 1:
            logger.info("Data object is already single variable. Returning copy")
            return self.copy()

        var_idx = self.var_idx[var_name]

        totnum = np.sum(self._data[:, self._VARINDEX] == var_idx)

        colnum, rownum = self.shape

        if rownum != len(self._init_index()):
            raise NotImplementedError(
                "Cannot split UngriddedData objects that have "
                "additional columns other than default columns"
            )

        subset = UngriddedData(totnum)

        subset.var_idx[var_name] = 0
        subset._index = self.index

        meta_idx = -1
        arr_idx = 0

        for midx, didx in self.meta_idx.items():
            if var_name in didx and len(didx[var_name]) > 0:
                meta_idx += 1
                meta = {}
                _meta = self.metadata[midx]
                meta.update(_meta)
                meta["var_info"] = {}
                meta["var_info"][var_name] = _meta["var_info"][var_name]
                meta["variables"] = [var_name]
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
        subset._add_to_filter_history(
            f"Created {var_name} single var object from multivar UngriddedData instance"
        )
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
            _meta_check = {}
            # write metadata of first index that matches
            _meta_check.update(self.metadata[idx_lst[0]])
            _meta_idx_new = {}
            for j, meta_idx in enumerate(idx_lst):
                if j > 0:  # don't check first against first
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
                    if var not in _meta_idx_new:
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
            raise Exception(
                "FATAL: Mismatch in shape between initial and "
                "and final object. Developers: please check"
            )
        return new

    def append_station_data(self, stats, add_meta_keys=None):
        raise NotImplementedError()

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
            raise ValueError(
                f"Cannot add any UngriddedDataContainer to UngriddedData, got: {type(other)}, please switch order, or implement UngriddedData.append_station_data"
            )
        if new_obj:
            obj = self.copy()
        else:
            obj = self

        if obj.is_empty:
            obj._data = other._data
            obj.metadata = other.metadata
            # obj.unit = other.unit
            obj._data_revision = other._data_revision
            obj.meta_idx = other.meta_idx
            # potentially temporary fix for pyaro actrisebas reader
            # if len(other.meta_idx) != len(other.metadata):
            #     obj.meta_idx = {key: other.meta_idx[key] for key in other.metadata.keys()}
            obj.var_idx = other.var_idx
        else:
            # get offset in metadata index
            meta_offset = max(obj.metadata) + 1
            data_offset = obj.shape[0]

            # add this offset to indices of meta dictionary in input data object
            for meta_idx_other, meta_other in other.metadata.items():
                meta_idx = meta_offset + meta_idx_other
                obj.metadata[meta_idx] = meta_other
                _idx_map = {}
                for var_name, indices in other.meta_idx[meta_idx_other].items():
                    _idx_map[var_name] = np.asarray(indices) + data_offset
                obj.meta_idx[meta_idx] = _idx_map

            for var, idx in other.var_idx.items():
                if var in obj.var_idx:  # variable already exists in this object
                    if not idx == obj.var_idx[var]:
                        other._change_var_idx(var, obj.var_idx[var])
                else:  # variable does not yet exist
                    idx_exists = [v for v in obj.var_idx.values()]
                    if idx in idx_exists:
                        # variable index is already assigned to another
                        # variable and needs to be changed
                        new_idx = max(idx_exists) + 1
                        other._change_var_idx(var, new_idx)
                        obj.var_idx[var] = new_idx
                    else:
                        obj.var_idx[var] = idx
            obj._data = np.vstack([obj._data, other._data])
            obj._data_revision.update(other._data_revision)
        obj.filter_hist.update(other.filter_hist)
        obj._check_index()
        return obj

    def colocate_vardata(
        self, var1, data_id1=None, var2=None, data_id2=None, other=None, **kwargs
    ):
        # UNTESTED UNDOCUMENTED METHOD, HK 2025-03-15
        if other is None:
            other = self
        if var2 is None:
            var2 = var1
        if data_id1 is None:
            contains = self.contains_datasets
            if len(contains) > 1:
                raise ValueError(
                    "Please provide data_id1 since data object contains more than 1 dataset..."
                )
            data_id1 = contains[0]

        if data_id2 is None:
            contains = other.contains_datasets
            if len(contains) > 1:
                raise ValueError(
                    "Please provide data_id2 since data object contains more than 1 dataset..."
                )
            data_id2 = contains[0]
        if self is other and data_id1 == data_id2 and var1 == var2:
            raise ValueError(
                "Input combination too unspecific, please provide "
                "either another data object, 2 different data IDs "
                "or 2 different variable names"
            )
        input_data = [(self, data_id1, var1), (other, data_id2, var2)]
        statlist = combine_vardata_ungridded(input_data, **kwargs)

        new = UngriddedData.from_station_data(statlist)
        return new

    def _change_var_idx(self, var_name, new_idx):
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
            raise ValueError(
                "Fatal: variable index cannot be assigned a new "
                "index that is already assigned to one of the "
                "variables in this object"
            )
        cidx = self.var_idx[var_name]
        self.var_idx[var_name] = new_idx
        var_indices = np.where(self._data[:, self._VARINDEX] == cidx)
        self._data[var_indices, self._VARINDEX] = new_idx

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
        if var_name not in self.var_idx:
            raise AttributeError(f"Variable {var_name} not available in data")
        idx = self.var_idx[var_name]
        mask = np.where(self._data[:, self._VARINDEX] == idx)[0]
        return self._data[mask, self._DATAINDEX]

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
            logger.debug(
                f"No variable data in metadata block {self._idx}. Returning empty StationData"
            )
            return StationData()

    def __repr__(self):
        return f"{type(self).__name__} <networks: {self.contains_datasets}; vars: {self.contains_vars}; instruments: {self.contains_instruments}; No. of metadata units: {len(self.metadata)}"


def reduce_array_closest(arr_nominal, arr_to_be_reduced):
    logger.warning("This method is deprecated because no usage could be found, HK 2025-03-13")

    test = sorted(arr_to_be_reduced)
    closest_idx = []
    for num in sorted(arr_nominal):
        idx = np.argmin(abs(test - num))
        closest_idx.append(idx)
        test = test[(idx + 1) :]
    return closest_idx
