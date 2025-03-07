import abc


class UngriddedDataContainer(abc.ABC):
    """Base-class representing ungridded data like stations data, satellite data sondes"""

    @abc.abstractmethod
    @property
    def has_flag_data(self):
        """Boolean specifying whether this object contains flag data"""
        pass

    @abc.abstractmethod
    @property
    def is_vertical_profile(self):
        """Boolean specifying whether is vertical profile"""
        pass

    @abc.abstractmethod
    @is_vertical_profile.setter
    def is_vertical_profile(self, value):
        """
        Boolean specifying whether is vertical profile.
        Note must be set in ReadUngridded based on the reader
        because the instance of class used during reading is
        not the same as the instance used later in the workflow
        """
        pass

    @abc.abstractmethod
    @property
    def contains_vars(self) -> list[str]:
        """List of all variables in this dataset"""
        pass

    @abc.abstractmethod
    @property
    def contains_datasets(self) -> list[str]:
        """List of all datasets in this object"""
        pass

    @abc.abstractmethod
    @property
    def contains_instruments(self) -> list[str]:
        """List of all instruments in this object"""
        pass

    @abc.abstractmethod
    @property
    def is_empty(self) -> bool:
        """Boolean specifying whether this object contains data or not"""
        pass

    @abc.abstractmethod
    @property
    def is_filtered(self):
        """Boolean specifying whether this data object has been filtered

        Note
        ----
        Details about applied filtering can be found in :attr:`filter_hist`
        """
        pass

    @abc.abstractmethod
    @property
    def longitude(self) -> list[float]:
        """Longitudes of datapoints"""
        pass

    @abc.abstractmethod
    @property
    def latitude(self) -> list[float]:
        """Latitudes of stations"""
        pass

    @abc.abstractmethod
    @property
    def altitude(self) -> list[float]:
        """Altitudes of stations"""
        pass

    @abc.abstractmethod
    @property
    def station_name(self) -> list[str]:
        """station-name of data"""
        pass

    @abc.abstractmethod
    @property
    def time(self):
        """Time dimension of data"""
        pass

    @abc.abstractmethod
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
        pass

    @abc.abstractmethod
    @property
    def countries_available(self):
        """
        Alphabetically sorted list of country names available
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
            4-element dictionary containing following key / value pairs:

                - stats: list of :class:`StationData` objects
                - station_name: list of corresponding station names
                - latitude: list of latitude coordinates
                - longitude: list of longitude coordinates

        """
        pass

    @abc.abstractmethod
    def get_variable_data(
        self, variables, start=None, stop=None, ts_type=None, **kwargs
    ):  # pragma: no cover
        """Extract all data points of a certain variable

        Parameters
        ----------
        vars_to_extract : :obj:`str` or :obj:`list`
            all variables that are supposed to be accessed
        """
        pass

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

    @abc.abstractmethod
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
