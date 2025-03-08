import abc
import fnmatch
import logging

from pyaerocom.exceptions import (
    DataCoverageError,
    StationCoordinateError,
    TimeMatchError,
    VarNotAvailableError,
)

logger = logging.getLogger(__name__)


class UngriddedDataContainer(abc.ABC):
    """Base-class representing ungridded data like stations data, satellite data sondes"""

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
        pass

    @abc.abstractmethod
    def remove_outliers(
        self,
        var_name,
        inplace=False,
        low=None,
        high=None,
        unit_ref=None,
        move_to_trash=True,
    ):
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

    @abc.abstractmethod
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
        pass

    @abc.abstractmethod
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
        pass

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

    @abc.abstractmethod
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

    # def filter_by_meta -- unsure if need to implement?

    @abc.abstractmethod
    def copy(self):
        pass
