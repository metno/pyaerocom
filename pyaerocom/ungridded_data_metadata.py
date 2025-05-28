import abc
import fnmatch
import logging
import sys
from copy import deepcopy
from datetime import datetime
from typing import Any

import numpy as np

from pyaerocom import const
from pyaerocom.exceptions import DataCoverageError, MetaDataError, StationNotFoundError
from pyaerocom.helpers import isnumeric
from pyaerocom.helpers_landsea_masks import get_mask_value, load_region_mask_xr
from pyaerocom.mathutils import in_range
from pyaerocom.ungridded_data_container import UngriddedDataContainer
from pyaerocom.units.helpers import get_standard_unit
from pyaerocom.units.units_helpers import get_unit_conversion_fac

logger = logging.getLogger(__name__)


if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class UngriddedDataMetadata(UngriddedDataContainer):
    """Metadata-implementation for UngriddedDataContainer implementing
    metadata, i.e. metadata, data_revision, var_idx/variables, filter_hist and
    _is_vertical_profile. It does not do anything on the data-structure.

    This will only implement the UngriddedDataContainer partially. The data
    part needs to be implemented independently.

    """

    ALLOWED_VERT_COORD_TYPES = ["altitude"]

    def __init__(self):
        self.metadata = {}
        self._data_revision = {}
        self.var_idx = {}
        self.filter_hist = {}
        self._is_vertical_profile = False

    def _copy_metadata_to(self, other: Self) -> Self:
        """
        deepcopy metadata-fields to the other object
        """
        other.metadata = deepcopy(self.metadata)
        other._data_revision = deepcopy(self._data_revision)
        other.var_idx = deepcopy(self.var_idx)
        other.filter_hist = deepcopy(self.filter_hist)
        other.is_vertical_profile = self._is_vertical_profile

    @override
    def get_data_revision(self, data_id) -> str | None:
        """
        Get data revision for a data_id.

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
        if data_id not in self._data_revision:
            rev = None
            for meta in self.metadata.values():
                if meta["data_id"] == data_id:
                    if rev is None:
                        rev = meta["data_revision"]
                    elif not meta["data_revision"] == rev:
                        raise MetaDataError(
                            f"Found different data revisions for dataset {data_id}"
                        )
            self._data_revision[data_id] = rev
        return self._data_revision[data_id]

    @property
    def _first_meta_idx(self):
        """Give the index of the metadata of the first station/meta

        :return: dict
        """
        # First available metadata index
        if self.is_empty:
            raise DataCoverageError("no (meta)-data")
        return next(iter(self.metadata))

    @property
    @override
    def is_vertical_profile(self):
        """Boolean specifying whether is vertical profile"""
        return self._is_vertical_profile

    @is_vertical_profile.setter
    @override
    def is_vertical_profile(self, value):
        """
        Boolean specifying whether is vertical profile.
        Note must be set in ReadUngridded based on the reader
        because the instance of class used during reading is
        not the same as the instance used later in the workflow
        """
        self._is_vertical_profile = value

    def _list_from_metadata(
        self, metafield, undef=None, unique=False, allow_none=True
    ) -> list[Any]:
        """retrieve a station-metadata field as list

        :param metafield: one of the metadata-fields like "longitude" or "instrument"
        :param undef: default value if undefined
        :param unique: remove None and duplicate, defaults to False
        :param allow_none: allow none in unique lists
        :return: list of the metadata-fields values
        """
        ret_vals = []
        for info in self.metadata.values():
            try:
                val = info[metafield]
                if unique:
                    if val not in ret_vals:
                        if allow_none:
                            ret_vals.append(val)
                        elif val is not None:
                            ret_vals.append(val)
                else:
                    ret_vals.append(val)
            except KeyError:
                if not unique:
                    ret_vals.append(undef)
        return ret_vals

    @property
    @override
    def contains_vars(self) -> list[str]:
        """List of all variables in this dataset"""
        return list(self.var_idx)

    @property
    @override
    def contains_datasets(self):
        """List of all datasets in this object"""
        return self._list_from_metadata("data_id", unique=True)

    @property
    @override
    def contains_instruments(self):
        """List of all instruments in this object"""
        return self._list_from_metadata("instrument_name", unique=True, allow_none=False)

    @property
    @override
    def is_empty(self):
        """Boolean specifying whether this object contains data or not"""
        return True if len(self.metadata) == 0 else False

    @property
    @override
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
    @override
    def longitude(self):
        """Longitudes of stations"""
        return self._list_from_metadata("longitude", undef=np.nan)

    @property
    @override
    def latitude(self):
        """Latitudes of stations"""
        return self._list_from_metadata("latitude", undef=np.nan)

    @property
    @override
    def altitude(self):
        """Altitudes of stations"""
        return self._list_from_metadata("altitude", undef=np.nan)

    @property
    @override
    def station_name(self):
        """Station-names of stations"""
        return self._list_from_metadata("station_name", undef=np.nan)

    @property
    @override
    def unique_station_names(self):
        """List of unique station names"""
        return sorted(set(self.station_name))

    @property
    @override
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
                if key not in metakeys:
                    metakeys.append(key)
        return metakeys

    @property
    @override
    def nonunique_station_names(self):
        """List of station names that occur more than once in metadata"""
        import collections

        lst = self.station_name
        return [item for item, count in collections.Counter(lst).items() if count > 1]

    @override
    def last_filter_applied(self):
        """Returns the last filter that was applied to this dataset

        To see all filters, check out :attr:`filter_hist`
        """
        if not self.is_filtered:
            raise AttributeError("No filters were applied so far")
        return self.filter_hist[max(self.filter_hist)]

    @override
    def find_station_meta_indices(self, station_name_or_pattern, allow_wildcards=True):
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

    @override
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
            unit = get_standard_unit(var_name)

        units = []
        for i, meta in self.metadata.items():
            if var_name in meta["var_info"]:
                try:
                    u = meta["var_info"][var_name]["units"]
                    if u not in units:
                        units.append(u)
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
        if len(units) == 0 and str(unit) != "1":
            raise MetaDataError(
                f"Failed to access unit information for variable {var_name}. Expected unit {unit}"
            )
        for u in units:
            if not get_unit_conversion_fac(u, unit, var_name) == 1:
                raise MetaDataError(f"Invalid unit {u} detected (expected {unit})")

    def _add_to_filter_history(self, info):
        """Add info to :attr:`filter_hist`

        Key is current system time string

        Parameter
        ---------
        info
            information to be appended to filter history
        """
        time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        self.filter_hist[int(time_str)] = info

    @property
    @override
    def station_coordinates(self):
        """dictionary with station coordinates

        Returns
        -------
        dict
            dictionary containing station coordinates (latitude, longitude,
            altitude -> values) for all stations (keys) where these parameters
            are accessible.
        """
        d = {"station_name": [], "latitude": [], "longitude": [], "altitude": []}

        for i, meta in self.metadata.items():
            if "station_name" not in meta:
                logger.debug(f"Skipping meta-block {i}: station_name is not defined")
                continue
            elif not all(name in meta for name in const.STANDARD_COORD_NAMES):
                logger.debug(
                    f"Skipping meta-block {i} (station {meta['station_name']}): "
                    f"one or more of the coordinates is not defined"
                )
                continue

            stat = meta["station_name"]

            if stat in d["station_name"]:
                continue
            d["station_name"].append(stat)
            for k in const.STANDARD_COORD_NAMES:
                d[k].append(meta[k])
        return d

    @property
    def countries_available(self):
        """
        Alphabetically sorted list of country names available
        """
        countries = []
        for idx, meta in self.metadata.items():
            try:
                countries.append(meta["country"])
            except Exception:
                logger.warning("No country information in meta block", idx)
        if len(countries) == 0:
            logger.warning(
                "None of the metadata blocks contains "
                "country information. You may want to "
                "run class method check_set_country first "
                "to automatically assign countries."
            )
        return sorted(set(countries))

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
        valid_keys = self.metadata[self._first_meta_idx]
        str_f = {}
        list_f = {}
        range_f = {}
        val_f = {}
        for key, val in filter_attributes.items():
            if key not in valid_keys:
                raise OSError(
                    f"Invalid input parameter for filtering: {key}. "
                    f"Please choose from {valid_keys}"
                )

            if isinstance(val, str):
                str_f[key] = val
            elif isnumeric(val):
                val_f[key] = val
            elif isinstance(val, list | np.ndarray | tuple):
                if all([isinstance(x, str) for x in val]):
                    list_f[key] = val
                elif len(val) == 2 and all([isnumeric(x) for x in val]):
                    try:
                        low, high = float(val[0]), float(val[1])
                        if not low < high:
                            raise ValueError("First entry needs to be smaller than 2nd")
                        range_f[key] = [low, high]
                    except Exception:
                        list_f[key] = val
                else:
                    list_f[key] = val
        return (str_f, list_f, range_f, val_f)

    @abc.abstractmethod
    def _len_datapoints(self, meta_idx: float | list[float], var: str | list[str]):
        """Get the number of datapoints for meta_idx and var,
        needed internally by _find_meta_matches to calculate the
        total number of new data-size

        Parameters
        ----------
        meta_idx : index or indices of metadata-ids
        var : variable name or list of names

        Returns
        -------
        number of datapoints matching meta_idx and var
        """
        pass

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
            raise ValueError(f"Invalid input for negate {negate}, need list or str or None")
        meta_matches = []
        var_matches = []
        totnum = 0
        for meta_idx, meta in self.metadata.items():
            if self._check_filter_match(meta, negate, *filters):
                meta_matches.append(meta_idx)
                for var in meta["var_info"]:
                    if var in self.ALLOWED_VERT_COORD_TYPES:
                        continue  # altitude is not actually a variable but is stored in var_info like one
                    var_matches.append(var)
        totnum = self._len_datapoints(meta_matches, var_matches)
        return (meta_matches, totnum)

    def _check_str_filter_match(self, meta, negate, str_f):
        # Check string equality for input meta data and filters. Supports
        # wildcard matching
        for metakey, filterval in str_f.items():
            # key does not exist in this specific meta_block
            if metakey not in meta:
                return False
            # check if this key is in negate list (then result will be True
            # for all that do not match the specified filter input value(s))
            neg = metakey in negate

            # actual value of this key in input metadata
            metaval = meta[metakey]

            # check equality of values
            match = metaval == filterval
            if match:  # direct match found
                if neg:  # key is flagged in negate -> no match
                    return False
            else:  # no direct match found
                # check wildcard match
                if "*" in filterval:  # no wildcard in
                    match = fnmatch.fnmatch(metaval, filterval)
                    if neg:
                        if match:
                            return False
                    else:
                        if not match:
                            return False
                elif not neg:  # no match, no wildcard match and not inverted
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
            if metakey not in meta:
                return False
            neg = metakey in negate
            metaval = meta[metakey]
            match = metaval == filterval
            if match:  # lists are identical
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
                            if "*" in entry:
                                match = fnmatch.fnmatch(metaval, entry)
                                if match:
                                    found = True
                                    if neg:
                                        return False
                        if not found and not neg:
                            return False
        # range filter
        for metakey, filterval in range_f.items():
            if metakey not in meta:
                return False
            neg = metakey in negate
            match = in_range(meta[metakey], filterval[0], filterval[1])
            if (neg and match) or (not neg and not match):
                return False

        for metakey, filterval in val_f.items():
            if metakey not in meta:
                return False
            neg = metakey in negate
            match = meta[metakey] == filterval
            if (neg and match) or (not neg and not match):
                return False
        return True

    @override
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
        >>> r = pya.io.ReadUngridded(['AeronetSunV3Lev2.daily'], 'od550aer')
        >>> data = r.read()
        >>> data_filtered = data.filter_by_meta(data_id='AeronetSunV3Lev2.daily',
        ...                                     longitude=[-30, 30],
        ...                                     latitude=[20, 70],
        ...                                     altitude=[0, 1000])
        """

        if "variables" in filter_attributes:
            raise NotImplementedError("Cannot yet filter by variables")

        # separate filters by strin, list, etc.
        filters = self._init_meta_filters(**filter_attributes)

        # find all metadata blocks that match the filters
        meta_matches, totnum_new = self._find_meta_matches(
            negate,
            *filters,
        )
        if len(meta_matches) == len(self.metadata):
            logger.info(f"Input filters {filter_attributes} result in unchanged data object")
            return self
        new = self._new_from_meta_blocks(meta_matches, totnum_new)
        time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        new.filter_hist[int(time_str)] = filter_attributes
        return new

    @override
    def filter_by_projection(
        self, projection, xrange: tuple[float, float], yrange: tuple[float, float]
    ):
        """Filter the ungridded data to a horizontal bounding box given by a projection

        :param projection: a function turning projection(lat, lon) -> (x, y)
        :param xrange: x range (min/max included) in the projection plane
        :param yrange: y range (min/max included) in the projection plane
        """
        meta_matches = []
        totnum = 0
        for meta_idx, meta in self.metadata.items():
            lon = meta["longitude"]
            lat = meta["latitude"]
            x, y = projection(lat, lon)

            match_x = in_range(x, xrange[0], xrange[1])
            match_y = in_range(y, yrange[0], yrange[1])

            if match_x and match_y:
                meta_matches.append(meta_idx)
                for var in meta["var_info"]:
                    if var in self.ALLOWED_VERT_COORD_TYPES:
                        continue  # altitude is not actually a variable but is stored in var_info like one
                    try:
                        totnum += len(self.meta_idx[meta_idx][var])
                    except KeyError:
                        logger.debug(
                            f"Ignoring variable {var} in meta block {meta_idx} "
                            f"since no data could be found"
                        )

        if len(meta_matches) == len(self.metadata):
            logger.info("filter_by_projection result in unchanged data object")
            return self
        new = self._new_from_meta_blocks(meta_matches, totnum)
        return new

    @override
    def apply_region_mask(self, region_id=None):
        """
        TODO : Write documentations

        Parameters
        ----------
        region_id : str or list (of strings)
            ID of region or IDs of multiple regions to be combined
        """
        if region_id not in const.HTAP_REGIONS:
            raise ValueError(
                f"Invalid input for region_id: {region_id}, choose from: {const.HTAP_REGIONS}"
            )

        # 1. find matches -> list of meta indices that are in region
        # 2. Get total number of datapoints -> defines shape of output UngriddedData
        # 3. Create

        mask = load_region_mask_xr(region_id)

        meta_matches = []
        totnum = 0
        for meta_idx, meta in self.metadata.items():
            lon, lat = meta["longitude"], meta["latitude"]

            mask_val = get_mask_value(lat, lon, mask)
            if mask_val >= 1:  # coordinate is in mask
                meta_matches.append(meta_idx)
                for var in meta["var_info"]:
                    totnum += len(self.meta_idx[meta_idx][var])

        new = self._new_from_meta_blocks(meta_matches, totnum)
        time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        new.filter_hist[int(time_str)] = f"Applied mask {region_id}"
        new._check_index()
        return new

    def _meta_to_lists(self):
        """List metadata for plotting

        :return: list of metadata values
        """
        meta = {k: [] for k in self.metadata[self._first_meta_idx]}
        for meta_item in self.metadata.values():
            for k, v in meta.items():
                v.append(meta_item[k])
        return meta

    @override
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
        logger.info(f"Extracting dataset {data_id} from data object")
        return self.filter_by_meta(data_id=data_id)
