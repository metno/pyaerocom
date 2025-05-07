import abc
import logging
import os
from collections.abc import Iterator

from pyaerocom import const
from pyaerocom.exceptions import (
    DataCoverageError,
    StationCoordinateError,
    TimeMatchError,
    VarNotAvailableError,
)
from pyaerocom.helpers import isnumeric
from pyaerocom.region import Region
from pyaerocom.stationdata import StationData

logger = logging.getLogger(__name__)


class UngriddedDataContainer(abc.ABC):
    """Base-class representing ungridded data like stations data, satellite data sondes"""

    @classmethod
    def from_station_data(
        cls,
        stats: StationData | Iterator[StationData],
        add_meta_keys: list[str] = [],
    ):
        """
        Create UngriddedDataContainer from input station data object(s)

        Parameters
        ----------
        stats : iterator of StationData, or StationData
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
        UngriddedDataContainer
            ungridded data object created from input station data objects

        """
        if isinstance(stats, StationData):
            stats = [stats]
        data = cls()
        data.append_station_data(stats, add_meta_keys)
        return data

    @abc.abstractmethod
    def get_data_revision(self, data_id):
        """
        Get the data revision of the data_id

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
        pass

    @property
    @abc.abstractmethod
    def shape(self):
        """Shape of data array"""
        pass

    @property
    @abc.abstractmethod
    def has_flag_data(self):
        """Boolean specifying whether this object contains flag data"""
        pass

    @property
    def is_vertical_profile(self):
        """Boolean specifying whether is vertical profile"""
        return self._is_vertical_profile

    @is_vertical_profile.setter
    @abc.abstractmethod
    def is_vertical_profile(self, value):
        """
        Boolean specifying whether is vertical profile.
        Note must be set in ReadUngridded based on the reader
        because the instance of class used during reading is
        not the same as the instance used later in the workflow
        """
        pass

    @property
    @abc.abstractmethod
    def contains_vars(self) -> list[str]:
        """List of all variables in this dataset"""
        pass

    @property
    @abc.abstractmethod
    def contains_datasets(self) -> list[str]:
        """List of all datasets in this object"""
        pass

    @property
    @abc.abstractmethod
    def contains_instruments(self) -> list[str]:
        """List of all instruments in this object"""
        pass

    @property
    @abc.abstractmethod
    def is_empty(self) -> bool:
        """Boolean specifying whether this object contains data or not"""
        pass

    @property
    @abc.abstractmethod
    def longitude(self) -> list[float]:
        """Longitudes of datapoints"""
        pass

    @property
    @abc.abstractmethod
    def latitude(self) -> list[float]:
        """Latitudes of stations"""
        pass

    @property
    @abc.abstractmethod
    def altitude(self) -> list[float]:
        """Altitudes of stations"""
        pass

    @property
    @abc.abstractmethod
    def station_name(self) -> list[str]:
        """station-name of data"""
        pass

    @property
    @abc.abstractmethod
    def unique_station_names(self) -> list[str]:
        """List of unique and sorted station names"""
        pass

    @property
    @abc.abstractmethod
    def available_meta_keys(self):
        """List of all available metadata keys

        Note
        ----
        This is a list of all metadata keys that exist in this dataset, but
        it does not mean that all of the keys are registered in all metadata
        blocks, especially if the data is merged from different sources with
        different metadata availability
        """
        pass

    @property
    @abc.abstractmethod
    def is_filtered(self):
        """Boolean specifying whether this data object has been filtered

        Note
        ----
        Details about applied filtering can be found in :attr:`filter_hist`
        """
        pass

    @property
    @abc.abstractmethod
    def countries_available(self):
        """
        Alphabetically sorted list of country names available
        """
        pass

    @property
    @abc.abstractmethod
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

    @abc.abstractmethod
    def append_station_data(
        self,
        stats: StationData | Iterator[StationData],
        add_meta_keys: list[str] | None = None,
    ):
        """
        Append StationData(s) to this UngriddedDataContainer

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
        UngriddedDataContainer
            ungridded data object created from input station data objects

        """
        pass

    @abc.abstractmethod
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
        pass

    @abc.abstractmethod
    def _generate_station_index(self, by_station_name=True, ignore_index=None):
        """Generates index to loop over station names or metadata block indices.
        Needs to be implemented for :func:`to_station_data_all` to work"""
        pass

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
        this object by looping over :func:`to_station_data`.

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

    @abc.abstractmethod
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
        pass

    @abc.abstractmethod
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
        pass

    @abc.abstractmethod
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
        pass

    @property
    @abc.abstractmethod
    def station_coordinates(self):
        """dictionary with station coordinates

        Returns
        -------
        dict
            dictionary containing station coordinates (latitude, longitude,
            altitude -> values) for all stations (keys) where these parameters
            are accessible.
        """
        pass

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

    def filter_region(self, region_id, check_mask=True, check_country_meta=False, **kwargs):
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
        return self.filter_by_meta(longitude=region.lon_range, latitude=region.lat_range)

    @abc.abstractmethod
    def apply_region_mask(self, region_id=None):
        """
        TODO : Write documentations

        Parameters
        ----------
        region_id : str or list (of strings)
            ID of region or IDs of multiple regions to be combined
        """
        pass

    def filter_by_projection(
        self, projection, xrange: tuple[float, float], yrange: tuple[float, float]
    ):
        """Filter the ungridded data to a horizontal bounding box given by a projection

        :param projection: a function turning projection(lat, lon) -> (x, y)
        :param xrange: x range (min/max included) in the projection plane
        :param yrange: y range (min/max included) in the projection plane
        """
        pass

    @abc.abstractmethod
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
        pass

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
        UngriddedDataContainer
            filtered data object
        """
        data = self

        remove_outliers = False
        set_flags_nan = False
        extract_vars = None
        region_id = None
        if "remove_outliers" in filter_attributes:
            remove_outliers = filter_attributes.pop("remove_outliers")
        if "set_flags_nan" in filter_attributes:
            set_flags_nan = filter_attributes.pop("set_flags_nan")
        if "var_name" in filter_attributes:
            extract_vars = filter_attributes.pop("var_name")
            if isinstance(extract_vars, str):
                extract_vars = [extract_vars]
            for var in extract_vars:
                if var not in data.contains_vars:
                    raise VarNotAvailableError(
                        f"No such variable {var} in UngriddedData object. "
                        f"Available vars: {self.contains_vars}"
                    )
        if "region_id" in filter_attributes:
            region_id = filter_attributes.pop("region_id")

        if len(filter_attributes) > 0:
            data = data.filter_by_meta(**filter_attributes)

        if extract_vars is not None:
            data = data.extract_vars(extract_vars)

        if remove_outliers:
            if var_outlier_ranges is None:
                var_outlier_ranges = {}

            for var in data.contains_vars:
                lower, upper = (
                    None,
                    None,
                )  # uses pyaerocom default specified in variables.ini
                if var in var_outlier_ranges:
                    lower, upper = var_outlier_ranges[var]
                data = data.remove_outliers(
                    var, inplace=True, low=lower, high=upper, move_to_trash=False
                )
        if set_flags_nan:
            if not data.has_flag_data:
                # jgriesfeller 20230210
                # not sure if raising this exception is the right thing to do
                # the fake variables (vars computed from other variables) might not have
                # and do not need flags (because that has been done during the read of the
                # variable they are computed from)
                # disabling and logging it for now
                # raise MetaDataError(
                logger.info(
                    'Cannot apply filter "set_flags_nan" to '
                    "UngriddedData object, since it does not "
                    "contain flag information"
                )
            else:
                data = data.set_flags_nan(inplace=True)
        if region_id:
            data = data.filter_region(region_id)
        return data

    @abc.abstractmethod
    def extract_dataset(self, data_id):
        """Extract single dataset into new instance of :class:`UngriddedData`

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
        pass

    @abc.abstractmethod
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
        pass

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
        pass

    @abc.abstractmethod
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
        pass

    @abc.abstractmethod
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
        pass

    @abc.abstractmethod
    def copy(self):
        """Make a copy/clone of this object

        Returns
        -------
        UngriddedDataContainer
            clone of this object

        Raises
        ------
        MemoryError
            if copy is too big to fit into memory together with existing
            instance
        """
        pass

    @abc.abstractmethod
    def _new_from_meta_blocks(self, meta_ids: list, total: int = 1000000):
        """Create a duplicate of this UngriddedDataContainer containing
        only the meta_ids. This method is needed in meta/station filtering.

        :param meta_ids: list of station ids to select
        :param total: guessed number of points, to initialize the new container
        :return: UngriddedDataContainer
        :raises: DataExtractionError if new object empty
        """
        pass

    def merge(self, other, new_obj=True):
        """Merge another data object with this one

        Parameters
        -----------
        other : UngriddedDataContainer
            other data object
        new_obj : bool
            if True, this object remains unchanged and the merged data objects
            are returned in a new instance of :class:`UngriddedDataContainer`. If False,
            then this object is modified

        Returns
        -------
        UngriddedDataContainer
            merged data object

        Raises
        -------
        ValueError
            if input object is not an instance of :class:`UngriddedDataContainer`
        """
        if not isinstance(other, UngriddedDataContainer):
            raise ValueError(f"merge needs UngriddedDataContainer to merge, got: {type(other)}")

        if new_obj:
            obj = self.copy()
        else:
            obj = self
        if self == other:
            return obj

        for var in other.contains_vars:
            # convert variable by variable, since to_station_data_all
            # fails is not implemented for multiple variables
            all_stations = other.to_station_data_all(vars_to_convert=var)
            obj.append_station_data(all_stations["stats"])

        # update metadata
        obj._data_revision.update(other._data_revision)
        obj.filter_hist.update(other.filter_hist)

        return obj

    def append(self, other):
        """Append other instance of :class:`UngriddedDataContainer` to this object

        Note
        ----
        Calls :func:`merge(other, new_obj=False)`

        Parameters
        -----------
        other : UngriddedDataContainer
            other data object

        Returns
        -------
        UngriddedData
            merged data object

        Raises
        -------
        ValueError
            if input object is not an instance of :class:`UngriddedDataContainer`

        """
        return self.merge(other, new_obj=False)

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
            raise ValueError("Need string (e.g. variable name, station name, instrument name")
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
        return f"{type(self).__name__} <networks: {self.contains_datasets}; vars: {self.contains_vars}; instruments: {self.contains_instruments}; No. of metadata units: {len(self.metadata)}>"

    def __getitem__(self, key):
        if isnumeric(key) or key in self.unique_station_names:
            return self.to_station_data(key, insert_nans=True)
        raise KeyError("Invalid input key, need metadata index or station name ")

    def __and__(self, other):
        """Merge this object with another using the logical ``and`` operator

        Example
        -------
        >>> from pyaerocom.io import ReadAeronetSdaV3
        >>> read = ReadAeronetSdaV3()

        >>> d0 = read.read(last_file=10)
        >>> d1 = read.read(first_file=10, last_file=20)

        >>> merged = d0 & d1

        >>> print(d0.shape, d1.shape, merged.shape)
        (9868, 12) (12336, 12) (22204, 12)
        """
        return self.merge(other, new_obj=True)

    @staticmethod
    def _try_infer_stat_merge_pref_attr(stats):
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
            if "data_id" not in stat:
                return None
            elif data_id is None:
                data_id = stat["data_id"]
                from pyaerocom.metastandards import DataSource

                s = DataSource(
                    data_id=data_id
                )  # reads default data source info that may contain preferred meta attribute
                pref_attr = s.stat_merge_pref_attr
                if pref_attr is None:
                    return None
            elif (
                not stat["data_id"] == data_id
            ):  # station data objects contain different data sources
                return None
        return pref_attr

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
        raise ValueError("Failed to load UngriddedData object")

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
            raise FileNotFoundError(f"Directory does not exist: {save_dir}")
        elif not file_name.endswith(".pkl"):
            raise ValueError("Can only store files as pickle, file_name needs to have format .pkl")
        ch = CacheHandlerUngridded()
        return ch.write(self, var_or_file_name=file_name, cache_dir=save_dir)
