import logging
import os
import warnings
from copy import deepcopy
from pathlib import Path

from pyaerocom import const
from pyaerocom.combine_vardata_ungridded import combine_vardata_ungridded
from pyaerocom.exceptions import (
    DataRetrievalError,
    NetworkNotImplemented,
    NetworkNotSupported,
)
from pyaerocom.helpers import varlist_aerocom
from pyaerocom.io import ReadUngriddedBase
from pyaerocom.io.cachehandler_ungridded import CacheHandlerUngridded
from pyaerocom.io.cams2_83.read_obs import ReadCAMS2_83
from pyaerocom.io.cnemc.reader import ReadCNEMC
from pyaerocom.io.gaw.reader import ReadGAW
from pyaerocom.io.ghost.reader import ReadGhost
from pyaerocom.io.icos.reader import ReadICOS
from pyaerocom.io.icpforests.reader import ReadICPForest
from pyaerocom.io.pyaro.pyaro_config import PyaroConfig
from pyaerocom.io.pyaro.read_pyaro import ReadPyaro
from pyaerocom.io.read_aasetal import ReadAasEtal
from pyaerocom.io.read_aeronet_invv3 import ReadAeronetInvV3
from pyaerocom.io.read_aeronet_sdav3 import ReadAeronetSdaV3
from pyaerocom.io.read_aeronet_sunv3 import ReadAeronetSunV3
from pyaerocom.io.read_airnow import ReadAirNow
from pyaerocom.io.read_earlinet import ReadEarlinet
from pyaerocom.io.read_eprofile import ReadEprofile
from pyaerocom.io.read_ebas import ReadEbas
from pyaerocom.io.read_eea_aqerep import ReadEEAAQEREP
from pyaerocom.io.read_eea_aqerep_v2 import ReadEEAAQEREP_V2
from pyaerocom.variable import get_aliases

logger = logging.getLogger(__name__)


# TODO Add check if data id of config is same as one already given by pyaerocom
class ReadUngridded:
    """Factory class for reading of ungridded data based on obsnetwork ID

    This class also features reading functionality that goes beyond reading
    of individual observation datasets; including, reading of multiple
    datasets and post computation of new variables based on datasets that can
    be read.

    Parameters
    ----------
    COMING SOON

    """

    SUPPORTED_READERS = [
        ReadAeronetInvV3,
        ReadAeronetSdaV3,
        ReadAeronetSunV3,
        ReadEarlinet,
        ReadEprofile,
        ReadEbas,
        ReadAasEtal,
        ReadAirNow,
        ReadEEAAQEREP,
        ReadEEAAQEREP_V2,
        ReadCAMS2_83,
        ReadGAW,
        ReadGhost,
        ReadCNEMC,
        ReadICOS,
        ReadICPForest,
    ]

    # Creates list of all readers excluding ReadPyaro
    INCLUDED_READERS = deepcopy(SUPPORTED_READERS)

    # Adds ReadPyaro to said list
    SUPPORTED_READERS.append(ReadPyaro)

    DONOTCACHE_NAME = "DONOTCACHE"

    def __init__(
        self,
        data_ids=None,
        ignore_cache=False,
        data_dirs=None,
        configs: PyaroConfig | list[PyaroConfig] | None = None,
    ):
        # will be assigned in setter method of data_ids
        self._data_ids = []
        self._data_dirs = {}

        #: dictionary containing reading classes for each dataset to read (will
        #: be accessed via get_reader)
        self._readers = {}

        if data_ids is not None:
            self.data_ids = data_ids

        if data_dirs is not None:
            self.data_dirs = data_dirs

        if ignore_cache:
            logger.info("Deactivating caching")
            const.CACHING = False

        self.config_ids = {}
        self.config_map = {}

        if isinstance(configs, PyaroConfig):
            configs = [configs]

        self._configs = configs

        if isinstance(configs, list):
            for config in configs:
                if config is not None:
                    self._init_pyaro_reader(config=config)

    @property
    def data_dirs(self):
        """
        dict: Data directory(ies) for dataset(s) to read (keys are data IDs)
        """
        return self._data_dirs

    @data_dirs.setter
    def data_dirs(self, val):
        if isinstance(val, Path):
            val = str(val)
        dsr = self.data_ids
        if len(dsr) < 2 and isinstance(val, str):
            val = {dsr[0]: val}
        elif not isinstance(val, dict):
            raise ValueError(f"Invalid input for data_dirs ({val}); needs to be a dictionary.")
        for data_dir in val.values():
            assert os.path.exists(data_dir), f"{data_dir} does not exist"
        self._data_dirs = val

    @property
    def post_compute(self):
        """Information about datasets that can be computed in post"""
        return const.OBS_UNGRIDDED_POST

    @property
    def INCLUDED_DATASETS(self):
        lst = []
        for reader in self.INCLUDED_READERS:
            lst.extend(reader.SUPPORTED_DATASETS)
        lst.extend(self.post_compute)
        return lst

    @property
    def SUPPORTED_DATASETS(self):
        """
        Returns list of strings containing all supported dataset names
        """
        lst = []
        for reader in self.SUPPORTED_READERS:
            lst.extend(reader.SUPPORTED_DATASETS)
        lst.extend(self.post_compute)
        lst.extend(list(self.config_ids.keys()))
        return lst

    @property
    def supported_datasets(self):
        """
        Wrapper for :attr:`SUPPORTED_DATASETS`
        """
        return self.SUPPORTED_DATASETS

    def _check_donotcachefile(self):
        """Check if donotcache file exists

        Returns
        -------
        bool
            True if file exists, else False
        """
        try:
            if os.path.exists(os.path.join(const.cache_basedir, self.DONOTCACHE_NAME)):
                return True
        except Exception:
            pass
        return False

    @property
    def ignore_cache(self):
        """Boolean specifying whether caching is active or not"""
        if self._check_donotcachefile() or not const.CACHING:
            return True
        return False

    @property
    def data_ids(self):
        """List of datasets supposed to be read"""
        return self._data_ids

    @data_ids.setter
    def data_ids(self, val):
        if isinstance(val, str):
            val = [val]
        elif not isinstance(val, tuple | list):
            raise OSError("Invalid input for parameter data_ids")
        self._data_ids = val

    @property
    def configs(self):
        """List configs"""
        return self._configs

    @configs.setter
    def configs(self, val: PyaroConfig | list[PyaroConfig]):
        if isinstance(val, PyaroConfig):
            val = [val]
        elif not isinstance(val, tuple | list):
            raise OSError("Invalid input for parameter data_ids")
        logger.warning(
            "You are now overwriting the list of configs. This will delete the previous configs, but will leave readeres associated with those configs intact. Use 'add_config' for safer usage!"
        )
        for config in val:
            self._init_pyaro_reader(config=config)
        self._configs = deepcopy(val)

    @property
    def data_id(self):
        """
        ID of dataset

        Note
        -----
        Only works if exactly one dataset is assigned to the reader, that is,
        length of :attr:`data_ids` is 1.

        Raises
        ------
        AttributeError
            if number of items in :attr:`data_ids` is unequal one.

        Returns
        -------
        str
            data ID

        """
        nids = len(self.data_ids)
        if nids == 0:
            raise AttributeError("No data_id assigned")
        elif nids > 1:
            raise AttributeError("Multiple data_ids assigned")
        return self.data_ids[0]

    def dataset_provides_variables(self, data_id=None):
        """List of variables provided by a certain dataset"""
        if data_id is None:
            data_id = self.data_id
        if data_id not in self._readers:
            reader = self.get_lowlevel_reader(data_id)
        else:
            reader = self._readers[data_id]
        return reader.PROVIDES_VARIABLES

    def get_reader(self, data_id):
        warnings.warn(
            "this method was renamed to get_lowlevel_reader, please use the new name",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_lowlevel_reader(data_id)

    def get_lowlevel_reader(self, data_id: str | None = None) -> ReadUngriddedBase:
        """Helper method that returns initiated reader class for input ID

        Parameters
        -----------
        data_id : str
            Name of dataset

        Returns
        -------
        ReadUngriddedBase
            instance of reading class (needs to be implementation of base
            class :class:`ReadUngriddedBase`).
        """

        if data_id is None:
            if len(self.data_ids) != 1:
                raise ValueError("Please specify dataset")
        if data_id not in self.supported_datasets:
            if data_id not in self.config_map:
                raise NetworkNotSupported(
                    f"Could not fetch reader class: Input "
                    f"network {data_id} is not supported by "
                    f"ReadUngridded"
                )
        elif data_id not in self.data_ids:
            self.data_ids.append(data_id)
        if data_id not in self._readers:
            _cls = self._find_read_class(data_id)
            reader = self._init_lowlevel_reader(_cls, data_id)
            self._readers[data_id] = reader
        return self._readers[data_id]

    def add_pyaro_reader(self, config: PyaroConfig) -> ReadUngriddedBase:
        return self._init_pyaro_reader(config=config)

    def _init_pyaro_reader(self, config: PyaroConfig) -> ReadUngriddedBase:
        """
        Initializes PyAro reader from config, and adds reader to list of readers. If no config is given, the config given when ReaderUngridded was initiated is used

        Parameters
        -----------
        config : PyaroConfig
            Config for reader

        Returns
        -------
        ReadUngriddedBase
            instance of reading class (needs to be implementation of base
            class :class:`ReadUngriddedBase`)


        Raises
        ------
        ValueError
            If both the config argument and self.config are None
        """
        name = config.name

        if name in self.INCLUDED_DATASETS:
            raise NameError(
                f"{name} from config {config} cannot have the same name as an included dataset"
            )

        if name in self._readers:
            return self._readers[name]

        else:
            reader = ReadPyaro(config=config)
            self._readers[name] = reader
            self._data_ids.append(name)
            self.config_ids[name] = config.reader_id
            self.config_map[name] = config
            return reader

    def add_config(self, config: PyaroConfig) -> None:
        """
        Adds single PyaroConfig to self.configs

        Parameters
        ----------
        config: PyaroConfig

        Raises
        ------
        ValueError
            If config is not PyaroConfig

        """
        if not isinstance(config, PyaroConfig):
            raise ValueError("Given config is not a PyaroConfig")

        self._init_pyaro_reader(config=config)
        self._configs.append(config)

    def _find_read_class(self, data_id):
        """Find reading class for dataset name

        Loops over all reading classes available in :attr:`SUPPORTED_READERS`
        and finds the first one that matches the input dataset name, by
        checking the attribute :attr:`SUPPORTED_DATASETS` in each respective
        reading class.

        Parameters
        -----------
        data_id : str
            Name of dataset

        Returns
        -------
        ReadUngriddedBase
            instance of reading class (needs to be implementation of base
            class :class:`ReadUngriddedBase`)

        Raises
        ------
        NetworkNotImplemented
            if network is supported but no reading routine is implemented yet

        """
        for _cls in self.SUPPORTED_READERS:
            if data_id in _cls.SUPPORTED_DATASETS:
                return _cls
        raise NetworkNotImplemented(f"Could not find reading class for dataset {data_id}")

    def _init_lowlevel_reader(self, reader, data_id):
        """
        Initiate lowlevel reader for input data ID

        Parameters
        ----------
        reader
            reader class (not instantiated)
        data_id : str
            ID of dataset to be isntantiated with input reader

        Returns
        -------
        ReadUngriddedBase
            instantiated reader class for input ID.

        """
        # if data_id is not None and config is not None:
        #     if data_id != config.name:
        #         raise ValueError(
        #             f"DATA ID and config are both given, but they are not equal, {data_id} != {config.data_id}"
        #         )
        # if config is None:
        #     config = self.config

        # if data_id is None:
        #     data_id = config.name

        if data_id is None:
            raise ValueError("Data_id can not be none")

        if data_id in self.config_map:
            return reader(config=self.config_map[data_id])

        if data_id in self.data_dirs:
            ddir = self.data_dirs[data_id]
            logger.info(f"Reading {data_id} from specified data location: {ddir}")
        else:
            ddir = None

        return reader(data_id=data_id, data_dir=ddir)

    def read_dataset(
        self,
        data_id,
        vars_to_retrieve=None,
        only_cached=False,
        filter_post=None,
        **kwargs,
    ):
        """Read dataset into an instance of :class:`ReadUngridded`

        Parameters
        ----------
        data_id : str
            name of dataset
        vars_to_retrieve : list
            variable or list of variables to be imported
        only_cached : bool
            if True, then nothing is reloaded but only data is loaded that is
            available as cached objects (not recommended to use but may be
            used if working offline without connection to database)
        filter_post : dict, optional
            filters applied to `UngriddedDataContainer` object AFTER it is read into
            memory, via :func:`UngriddedDataContainer.apply_filters`. This option was
            introduced in pyaerocom version 0.10.0 and should be used
            preferably over **kwargs. There is a certain flexibility with
            respect to how these filters can be defined, for instance, sub
            dicts for each `data_id`. The most common way would be
            to provide directly the input needed for
            `UngriddedDataContainer.apply_filters`. If you want to read multiple variables
            from one or more datasets, and if you want to apply variable
            specific filters, it is recommended to read the data individually
            for each variable and corresponding set of filters and then
            merge the individual filtered `UngriddedDataContainer` objects afterwards,
            e.g. using `data_var1 & data_var2`.
        **kwargs
            Additional input options for reading of data, which are applied
            WHILE the data is read. If any such additional options are
            provided that are applied during the reading, then automatic
            caching of the output `UngriddedDataContainer` object will be deactivated.
            Thus, it is recommended to handle data filtering via `filter_post`
            argument whenever possible, which will result in better performance
            as the unconstrained original data is read in and cached, and then
            the filtering is applied.

        Returns
        --------
        UngriddedDataContainer
            data object
        """
        force_caching = False
        if "force_caching" in kwargs:
            force_caching = kwargs.pop("force_caching")

        _caching = None
        if len(kwargs) > 0 and not force_caching:
            _caching = const.CACHING
            const.CACHING = False

            logger.info("Received additional reading constraints, ignoring caching")

        reader = self.get_lowlevel_reader(data_id)

        if vars_to_retrieve is None:
            vars_to_retrieve = reader.DEFAULT_VARS

        vars_to_retrieve = varlist_aerocom(vars_to_retrieve)

        # Since this interface enables to load multiple datasets, each of
        # which support a number of variables, here, only the variables are
        # considered that are supported by the dataset
        vars_available = [var for var in vars_to_retrieve if reader.var_supported(var)]

        if len(vars_available) == 0:
            raise DataRetrievalError(
                f"None of the input variables ({vars_to_retrieve}) is "
                f"supported by {data_id} interface"
            )
        cache = CacheHandlerUngridded(reader)
        if not self.ignore_cache and not isinstance(cache.reader, ReadPyaro):
            # initiate cache handler
            for var in vars_available:
                try:
                    cache.check_and_load(var, force_use_outdated=only_cached)
                except Exception:
                    logger.exception(
                        "Fatal: compatibility error between old cache file "
                        "and current version of code."
                    )

        if not only_cached:
            vars_to_read = [v for v in vars_available if v not in cache.loaded_data]
        else:
            vars_to_read = []

        data_read = None
        if len(vars_to_read) > 0:
            _loglevel = logger.level
            logger.setLevel(logging.INFO)
            data_read = reader.read(vars_to_read, **kwargs)
            logger.setLevel(_loglevel)

            for var in vars_to_read:
                # write the cache file
                if not self.ignore_cache and not isinstance(cache.reader, ReadPyaro):
                    try:
                        cache.write(data_read, var)
                    except Exception as e:
                        _caching = False
                        logger.warning(
                            f"Failed to write to cache directory. "
                            f"Error: {repr(e)}. Deactivating caching "
                            f"in pyaerocom"
                        )

        if len(vars_to_read) == len(vars_available):
            data_out = data_read
        else:
            data_out = None
            for var in vars_available:
                if var in cache.loaded_data:
                    if data_out is None:
                        data_out = cache.loaded_data[var]
                    else:
                        data_out.append(cache.loaded_data[var])
            if data_read is not None:
                if data_out is None:
                    data_out = data_read.copy()
                else:
                    data_out.append(data_read)

        # close the cache-object, keeps otherwise data-references
        cache = None

        if _caching is not None:
            const.CACHING = _caching

        if filter_post:
            filters = self._eval_filter_post(filter_post, data_id, vars_available)
            data_out = data_out.apply_filters(**filters)

        # Check to see if this reader is for a VerticalProfile
        # It is currently only allowed that a reader can be for a VerticalProfile, not a species
        if getattr(reader, "is_vertical_profile", None):
            data_out.is_vertical_profile = reader.is_vertical_profile

        return data_out

    def _eval_filter_post(self, filter_post, data_id, vars_available):
        filters = {}
        if not isinstance(filter_post, dict):
            raise ValueError(f"input filter_post must be dict, got {type(filter_post)}")
        elif len(filter_post) == 0:
            return filters

        if data_id in filter_post:
            # filters are specified specifically for that dataset
            subset = filter_post[data_id]
            return self._eval_filter_post(subset, data_id, vars_available)

        for key, val in filter_post.items():
            if key == "ignore_station_names":  # for backwards compatibility
                if isinstance(val, str | list):
                    filters["station_name"] = val
                    if "negate" not in filters:
                        filters["negate"] = []
                    filters["negate"].append("station_name")

                elif isinstance(val, dict):  # variable specific station filtering
                    if len(vars_available) > 1:
                        raise NotImplementedError(
                            f"Cannot filter different sites for multivariable "
                            f"UngriddedDataContainer objects (i.e. apply filter "
                            f"ignore_station_names={val} for UngriddedDataContainer "
                            f"object containing {vars_available}"
                        )
                    else:
                        # the variable that is available in the UngriddedDataContainer
                        # object
                        var = vars_available[0]
                        try:
                            filters["station_name"] = val[var]
                            if "negate" not in filters:
                                filters["negate"] = []
                            filters["negate"].append("station_name")
                        except KeyError:
                            continue
                else:
                    raise ValueError(f"Invalid input for ignore_station_names: {val}")
            else:
                filters[key] = val
        return filters

    def read_dataset_post(
        self,
        data_id,
        vars_to_retrieve,
        only_cached=False,
        filter_post=None,
        **kwargs,
    ):
        """Read dataset into an instance of :class:`ReadUngridded`

        Parameters
        ----------
        data_id : str
            name of dataset
        vars_to_retrieve : list
            variable or list of variables to be imported
        only_cached : bool
            if True, then nothing is reloaded but only data is loaded that is
            available as cached objects (not recommended to use but may be
            used if working offline without connection to database)
        filter_post : dict, optional
            filters applied to `UngriddedDataContainer` object AFTER it is read into
            memory, via :func:`UngriddedDataContainer.apply_filters`. This option was
            introduced in pyaerocom version 0.10.0 and should be used
            preferably over **kwargs. There is a certain flexibility with
            respect to how these filters can be defined, for instance, sub
            dicts for each `data_id`. The most common way would be
            to provide directly the input needed for
            `UngriddedDataContainer.apply_filters`. If you want to read multiple variables
            from one or more datasets, and if you want to apply variable
            specific filters, it is recommended to read the data individually
            for each variable and corresponding set of filters and then
            merge the individual filtered `UngriddedDataContainer` objects afterwards,
            e.g. using `data_var1 & data_var2`.
        **kwargs
            Additional input options for reading of data, which are applied
            WHILE the data is read. If any such additional options are
            provided that are applied during the reading, then automatic
            caching of the output `UngriddedDataContainer` object will be deactivated.
            Thus, it is recommended to handle data filtering via `filter_post`
            argument whenever possible, which will result in better performance
            as the unconstrained original data is read in and cached, and then
            the filtering is applied.

        Returns
        --------
        UngriddedDataContainer
            data object
        """
        aux_info = self.post_compute[data_id]
        loaded = []
        for var in vars_to_retrieve:
            input_data_ids_vars = []
            aux_info_var = aux_info["aux_requires"][var]
            for aux_id, aux_vars in aux_info_var.items():
                if aux_id in self.post_compute:
                    aux_data = self.read_dataset_post(
                        data_id=aux_id,
                        vars_to_retrieve=aux_vars,
                        only_cached=only_cached,
                        **kwargs,
                    )
                    for aux_var in aux_vars:
                        input_data_ids_vars.append((aux_data, aux_id, aux_var))
                else:
                    # read variables individually, so filter_post is more
                    # flexible if some post filters are specified for
                    # individual variables...
                    for aux_var in aux_vars:
                        _data = self.read_dataset(
                            data_id=aux_id,
                            vars_to_retrieve=aux_var,
                            only_cached=only_cached,
                            filter_post=filter_post,
                            **kwargs,
                        )
                        input_data_ids_vars.append((_data, aux_id, aux_var))

            aux_merge_how = aux_info["aux_merge_how"][var]

            if var in aux_info["aux_units"]:
                var_unit_out = aux_info["aux_units"][var]
            else:
                var_unit_out = None

            if aux_merge_how == "eval":
                # function MUST be defined
                aux_fun = aux_info["aux_funs"][var]
            else:
                aux_fun = None

            merged_stats = combine_vardata_ungridded(
                data_ids_and_vars=input_data_ids_vars,
                merge_eval_fun=aux_fun,
                merge_how=aux_merge_how,
                var_name_out=var,
                var_unit_out=var_unit_out,
                data_id_out=aux_info["data_id"],
            )
            ungridded_class = type(input_data_ids_vars[0][0])
            loaded.append(ungridded_class.from_station_data(merged_stats))
        first = loaded[0]
        if len(loaded) == 1:
            return first
        for data in loaded[1:]:
            first.append(data)
        return first

    def read(
        self,
        data_ids=None,
        vars_to_retrieve=None,
        only_cached=False,
        filter_post=None,
        configs: PyaroConfig | list[PyaroConfig] | None = None,
        **kwargs,
    ):
        """Read observations

        Iter over all datasets in :attr:`data_ids`, call
        :func:`read_dataset` and append to data object

        Parameters
        ----------
        data_ids : str or list
            data ID or list of all datasets to be imported
        vars_to_retrieve : str or list
            variable or list of variables to be imported
        only_cached : bool
            if True, then nothing is reloaded but only data is loaded that is
            available as cached objects (not recommended to use but may be
            used if working offline without connection to database)
        filter_post : dict, optional
            filters applied to `UngriddedDataContainer` object AFTER it is read into
            memory, via :func:`UngriddedDataContainer.apply_filters`. This option was
            introduced in pyaerocom version 0.10.0 and should be used
            preferably over **kwargs. There is a certain flexibility with
            respect to how these filters can be defined, for instance, sub
            dicts for each `data_id`. The most common way would be
            to provide directly the input needed for
            `UngriddedDataContainer.apply_filters`. If you want to read multiple variables
            from one or more datasets, and if you want to apply variable
            specific filters, it is recommended to read the data individually
            for each variable and corresponding set of filters and then
            merge the individual filtered `UngriddedDataContainer` objects afterwards,
            e.g. using `data_var1 & data_var2`.
        **kwargs
            Additional input options for reading of data, which are applied
            WHILE the data is read. If any such additional options are
            provided that are applied during the reading, then automatic
            caching of the output `UngriddedDataContainer` object will be deactivated.
            Thus, it is recommended to handle data filtering via `filter_post`
            argument whenever possible, which will result in better performance
            as the unconstrained original data is read in and cached, and then
            the filtering is applied.

        Example
        -------
        >>> import pyaerocom.io.readungridded as pio # doctest: +SKIP
        >>> from pyaerocom import const # doctest: +SKIP
        >>> obj = pio.ReadUngridded(data_ids=const.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME) # doctest: +SKIP
        >>> obj.read() # doctest: +SKIP
        >>> print(obj) # doctest: +SKIP
        >>> print(obj.metadata[0.]['latitude']) # doctest: +SKIP

        """
        if data_ids is None:
            data_ids = self.data_ids
        elif isinstance(data_ids, str):
            data_ids = [data_ids]

        if configs is not None:
            if not isinstance(configs, list):
                configs = [configs]
            for config in configs:
                self._init_pyaro_reader(config=config)
                data_ids.append(config.name)

        if isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]

        data = None
        for ds in data_ids:
            if ds in self.post_compute:
                data_to_append = self.read_dataset_post(
                    data_id=ds,
                    vars_to_retrieve=vars_to_retrieve,
                    only_cached=only_cached,
                    filter_post=filter_post,
                    **kwargs,
                )
            else:
                data_to_append = self.read_dataset(
                    data_id=ds,
                    vars_to_retrieve=vars_to_retrieve,
                    only_cached=only_cached,
                    filter_post=filter_post,
                    **kwargs,
                )

            if data is None:
                data = data_to_append
            else:
                try:
                    data.append(data_to_append)
                except ValueError:
                    # UngriddedData cannot add UngriddedDataStructured, while the other way works
                    # just re-ordering here in such cases
                    data_to_append.append(data)
                    data = data_to_append
                # TODO: Test this. UngriddedDataContainer can contain more than 1 variable
                if getattr(data_to_append, "is_vertical_profile", None):
                    data.is_vertical_profile = data_to_append.is_vertical_profile

            logger.info(f"Successfully imported {ds} data")
        return data

    def _check_var_alias(self, var, supported):
        # could be an alias
        aliases = get_aliases(var)
        for svar in supported:
            if svar in aliases:
                return svar
        raise ValueError()

    def get_vars_supported(self, obs_id: str, vars_desired: list[str]):
        """
        Filter input list of variables by supported ones for a certain data ID

        Parameters
        ----------
        obs_id : str
            ID of observation network
        vars_desired : list
            List of variables that are desired

        Returns
        -------
        list
            list of variables that can be read through the input network

        """
        obs_vars = []
        if isinstance(vars_desired, str):
            vars_desired = [vars_desired]
        if obs_id in self.post_compute:
            # check if all required are accessible
            postinfo = self.post_compute[obs_id]
            supported = postinfo["vars_supported"]
            for var in varlist_aerocom(vars_desired):
                if var not in supported:
                    try:
                        var = self._check_var_alias(var, supported)
                    except ValueError:
                        # no alias match, skip...
                        continue
                requires = postinfo["aux_requires"][var]
                all_good = True
                for ds, vars_required in requires.items():
                    if isinstance(vars_required, str):
                        vars_required = [vars_required]
                    vars_avail = self.get_vars_supported(ds, vars_required)
                    if not len(vars_required) == len(vars_avail):
                        all_good = False
                        break
                if all_good:
                    obs_vars.append(var)

        else:
            # check if variable can be read from a dataset on disk
            _oreader = self.get_lowlevel_reader(obs_id)
            for var in varlist_aerocom(vars_desired):
                if _oreader.var_supported(var):
                    obs_vars.append(var)
        return obs_vars

    def __str__(self):
        return "\n".join(str(self.get_lowlevel_reader(ds)) for ds in self.data_ids)
