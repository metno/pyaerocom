"""
Classes and methods to perform high-level colocation.
"""
import glob
import logging
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path

from cf_units import Unit

if sys.version_info >= (3, 10):  # pragma: no cover
    from importlib import metadata
else:  # pragma: no cover
    import importlib_metadata as metadata

import pandas as pd

from pyaerocom import const
from pyaerocom._lowlevel_helpers import BrowseDict, ListOfStrings, StrWithDefault, chk_make_subdir
from pyaerocom.colocateddata import ColocatedData
from pyaerocom.colocation import (
    colocate_gridded_gridded,
    colocate_gridded_ungridded,
    correct_model_stp_coldata,
)
from pyaerocom.colocation_3d import ColocatedDataLists, colocate_vertical_profile_gridded
from pyaerocom.config import ALL_REGION_NAME
from pyaerocom.exceptions import ColocationError, ColocationSetupError, DataCoverageError
from pyaerocom.helpers import (
    get_lowest_resolution,
    start_stop,
    to_datestring_YYYYMMDD,
    to_pandas_timestamp,
)
from pyaerocom.io import ReadGridded, ReadUngridded
from pyaerocom.io.helpers import get_all_supported_ids_ungridded

logger = logging.getLogger(__name__)


class ColocationSetup(BrowseDict):
    """
    Setup class for high-level model / obs co-location.

    An instance of this setup class can be used to run a colocation analysis
    between a model and an observation network and will create a number of
    :class:`pya.ColocatedData` instances, which can be saved automatically
    as NetCDF files.

    Apart from co-location, this class also handles reading of the input data
    for co-location. Supported co-location options are:

    1. gridded vs. ungridded data
    For instance 3D model data (instance of :class:`GriddedData`) with lat,
    lon and time dimension that is co-located with station based observations
    which are represented in pyaerocom through :class:`UngriddedData` objects.
    The co-location function used is
    :func:`pyaerocom.colocation.colocated_gridded_ungridded`. For this type of
    co-location, the output co-located data object will be 3-dimensional,
    with dimensions `data_source` (index 0: obs, index 1: model), `time` and
    `station_name`.

    2. gridded vs. gridded data
    For instance 3D model data that is co-located with 3D satellite data
    (both instances of :class:`GriddedData`), both objects with lat,
    lon and time dimensions. The co-location function used
    is :func:`pyaerocom.colocation.colocated_gridded_gridded`.
    For this type of co-location, the output co-located data object will be
    4-dimensional,  with dimensions `data_source` (index 0: obs, index 1:
    model), `time` and `latitude` and `longitude`.



    Attributes
    ----------
    model_id : str
        ID of model to be used.
    obs_id : str
        ID of observation network to be used.
    obs_vars : list
        Variables to be analysed (need to be available in input obs dataset).
        Variables that are not available in the model data output will be
        skipped. Alternatively, model variables to be used for a given obs
        variable can also be specified via attributes :attr:`model_use_vars`
        and :attr:`model_add_vars`.
    ts_type : str
        String specifying colocation output frequency.
    start
        Start time of colocation. Input can be integer denoting the year or
        anything that can be converted  into :class:`pandas.Timestamp` using
        :func:`pyaerocom.helpers.to_pandas_timestamp`. If None, than the first
        available date in the model data is used.
    stop
        stop time of colocation. int or anything that can be converted into
        :class:`pandas.Timestamp` using
        :func:`pyaerocom.helpers.to_pandas_timestamp` or None. If None and if
        ``start`` is on resolution of year (e.g. ``start=2010``) then ``stop``
        will be automatically set to the end of that year. Else, it will be
        set to the last available timestamp in the model data.
    filter_name : str
        name of filter to be applied. If None, no filter is used
        (to be precise, if None, then
         :attr:`pyaerocom.const.DEFAULT_REG_FILTER` is used which should
         default to `ALL-wMOUNTAINS`, that is, no filtering).
    basedir_coldata : str
        Base directory for storing of colocated data files.
    save_coldata : bool
        if True, colocated data objects are saved as NetCDF file.
    obs_name : str, optional
        if provided, this string will be used in colocated data filename to
        specify obsnetwork, else obs_id will be used.
    obs_data_dir : str, optional
        location of obs data. If None, attempt to infer obs location based on
        obs ID.
    obs_use_climatology : bool
        BETA if True, pyaerocom default climatology is computed from observation
        stations (so far only possible for unrgidded / gridded colocation).
    obs_vert_type : str
        AeroCom vertical code encoded in the model filenames (only AeroCom 3
        and later). Specifies which model file should be read in case there are
        multiple options (e.g. surface level data can be read from a
        *Surface*.nc file as well as from a *ModelLevel*.nc file). If input is
        string (e.g. 'Surface'), then the corresponding vertical type code is
        used for reading of all variables that are colocated (i.e. that are
        specified in :attr:`obs_vars`).
    obs_ts_type_read : str or dict, optional
        may be specified to explicitly define the reading frequency of the
        observation data (so far, this does only apply to gridded obsdata such
        as satellites), either as str (same for all obs variables) or variable
        specific as dict. For ungridded reading, the frequency may be specified
        via :attr:`obs_id`, where applicable (e.g. AeronetSunV3Lev2.daily).
        Not to be confused with :attr:`ts_type`, which specifies the
        frequency used for colocation. Can be specified variable specific in
        form of dictionary.
    obs_filters : dict
        filters applied to the observational dataset before co-location.
        In case of gridded / gridded, these are filters that can be passed to
        :func:`pyaerocom.io.ReadGridded.read_var`, for instance, `flex_ts_type`,
        or `constraints`. In case the obsdata is ungridded (gridded / ungridded
        co-locations) these are filters that are handled through keyword
        `filter_post` in :func:`pyaerocom.io.ReadUngridded.read`. These filters
        are applied to the :class:`UngriddedData` objects after reading and
        caching the data, so changing them, will not invalidate the latest
        cache of the :class:`UngriddedData`.
    read_opts_ungridded : dict, optional
        dictionary that specifies reading constraints for ungridded reading,
        and are passed as `**kwargs` to :func:`pyaerocom.io.ReadUngridded.read`.
        Note that - other than for `obs_filters` these filters are applied
        during the reading of the :class:`UngriddedData` objects and specifying
        them will deactivate caching.
    model_name : str, optional
        if provided, this string will be used in colocated data filename to
        specify model, else obs_id will be used.
    model_data_dir : str, optional
        Location of model data. If None, attempt to infer model location based
        on model ID.
    model_read_opts : dict, optional
        options for model reading (passed as keyword args to
        :func:`pyaerocom.io.ReadUngridded.read`).
    model_use_vars : dict, optional
        dictionary that specifies mapping of model variables. Keys are
        observation variables, values are the corresponding model variables
        (e.g. model_use_vars=dict(od550aer='od550csaer')). Example: your
        observation has var *od550aer* but your model model uses a different
        variable name for that variable, say *od550*. Then, you can specify
        this via `model_use_vars = {'od550aer' : 'od550'}`. NOTE: in this case,
        a model variable *od550aer* will be ignored, even if it exists
        (cf :attr:`model_add_vars`).
    model_rename_vars : dict, optional
        rename certain model variables **after** co-location, before storing
        the associated :class:`ColocatedData` object on disk. Keys are model
        variables, values are new names
        (e.g. `model_rename_vars={'od550aer':'MyAOD'}`).
        Note: this does not impact which variables are read from the model.
    model_add_vars : dict, optional
        additional model variables to be processed for one obs variable. E.g.
        `model_add_vars={'od550aer': ['od550so4', 'od550gt1aer']}` would
        co-locate both model SO4 AOD (od550so4) and model coarse mode AOD
        (od550gt1aer) with total AOD (od550aer) from obs (in addition to
        od550aer vs od550aer if applicable).
    model_to_stp : bool
        ALPHA (please do not use): convert model data values to STP conditions
        after co-location. Note: this only works for very particular settings
        at the moment and needs revision, as it relies on access to
        meteorological data.
    model_ts_type_read : str or dict, optional
        may be specified to explicitly define the reading frequency of the
        model data, either as str (same for all obs variables) or variable
        specific as dict. Not to be confused with :attr:`ts_type`, which
        specifies the output frequency of the co-located data.
    model_read_aux : dict, optional
        may be used to specify additional computation methods of variables from
        models. Keys are variables to be computed, values are dictionaries with
        keys `vars_required` (list of required variables for computation of var
        and `fun` (method that takes list of read data objects and computes
        and returns var).
    model_use_climatology : bool
        if True, attempt to use climatological model data field. Note: this
        only works if model data is in AeroCom conventions (climatological
        fields are indicated with 9999 as year in the filename) and if this is
        active, only single year analysis are supported (i.e. provide int to
        :attr:`start` to specify the year and leave :attr:`stop` empty).
    gridded_reader_id : dict
        BETA: dictionary specifying which gridded reader is supposed to be used
        for model (and gridded obs) reading. Note: this is a workaround
        solution and will likely be removed in the future when the gridded
        reading API is more harmonised
        (see https://github.com/metno/pyaerocom/issues/174).
    flex_ts_type : bool
        Bboolean specifying whether reading frequency of gridded data is
        allowed to be flexible. This includes all gridded data, whether it is
        model or gridded observation (e.g. satellites). Defaults to True.
    min_num_obs : dict or int, optional
        time resampling constraints applied, defaults to None, in which case
        no constraints are applied. For instance, say your input is in daily
        resolution and you want output in monthly and you want to make sure to
        have roughly 50% daily coverage for the monthly averages. Then you may
        specify `min_num_obs=15` which will ensure that at least 15 daily
        averages are available to compute a monthly average. However, you may
        also define a hierarchical scheme that first goes from daily to
        weekly and then from weekly to monthly, via a dict. E.g.
        `min_num_obs=dict(monthly=dict(weekly=4), weekly=dict(daily=3))` would
        ensure that each week has at least 3 daily values, as well as that each
        month has at least 4 weekly values.
    resample_how : str or dict, optional
        string specifying how data should be aggregated when resampling in time.
        Default is "mean". Can also be a nested dictionary, e.g.
        `resample_how={'conco3': 'daily': {'hourly' : 'max'}}` would use the
        maximum value to aggregate from hourly to daily for variable conco3,
        rather than the mean.
    obs_remove_outliers : bool
        if True, outliers are removed from obs data before colocation,
        else not. Default is False.
        Custom outlier ranges for each variable can be specified via
        :attr:`obs_outlier_ranges`, and for all other variables, the pyaerocom
        default outlier ranges are used. The latter are specified in
        `variables.ini` file via `minimum` and `maximum` attributes and can
        also be accessed through :attr:`pyaerocom.variable.Variable.minimum`
        and :attr:`pyaerocom.variable.Variable.maximum`, respectively.
    model_remove_outliers : bool
        if True, outliers are removed from model data (normally this should be
        set to False, as the models are supposed to be assessed, including
        outlier cases). Default is False.
        Custom outlier ranges for each variable can be specified via
        :attr:`model_outlier_ranges`, and for all other variables, the pyaerocom
        default outlier ranges are used. The latter are specified in
        `variables.ini` file via `minimum` and `maximum` attributes and can
        also be accessed through :attr:`pyaerocom.variable.Variable.minimum`
        and :attr:`pyaerocom.variable.Variable.maximum`, respectively.
    obs_outlier_ranges : dict, optional
        dictionary specifying outlier ranges for individual obs variables.
        (e.g. dict(od550aer = [-0.05, 10], ang4487aer=[0,4])). Only relevant
        if :attr:`obs_remove_outliers` is True.
    model_outlier_ranges : dict, optional
        like :attr:`obs_outlier_ranges` but for model variables. Only relevant
        if :attr:`model_remove_outliers` is True.
    zeros_to_nan : bool
        If True, zero's in output co-located data object will be converted to
        NaN. Default is False.
    harmonise_units : bool
        if True, units are attempted to be harmonised during co-location
        (note: raises Exception if True and in case units cannot be harmonised).
    regrid_res_deg : int, optional
        resolution in degrees for regridding of model grid (done before
        co-location). Default is None.
    colocate_time : bool
        if True and if obs and model sampling frequency (e.g. daily) are higher
        than output colocation frequency (e.g. monthly), then the datasets are
        first colocated in time (e.g. on a daily basis), before the monthly
        averages are calculated. Default is False.
    reanalyse_existing : bool
        if True, always redo co-location, even if there is already an existing
        co-located NetCDF file (under the output location specified by
        :attr:`basedir_coldata` ) for the given variable combination to be
        co-located. If False and output already exists, then co-location is
        skipped for the associated variable. Default is True.
    raise_exceptions : bool
        if True, Exceptions that may occur for individual variables to be
        processed, are raised, else the analysis is skipped for such cases.
    keep_data : bool
        if True, then all colocated data objects computed when running
        :func:`run` will be stored in :attr:`data`. Defaults to True.
    add_meta : dict
        additional metadata that is supposed to be added to each output
        :class:`ColocatedData` object.
    """

    #: Dictionary specifying alternative vertical types that may be used to
    #: read model data. E.g. consider the variable is  ec550aer,
    #: obs_vert_type='Surface' and obs_vert_type_alt=dict(Surface='ModelLevel').
    #: Now, if a model that is used for the analysis does not contain a data
    #: file for ec550aer at the surface ('*ec550aer*Surface*.nc'), then, the
    #: colocation routine will look for '*ec550aer*ModelLevel*.nc' and if this
    #: exists, it will load it and extract the surface level.
    OBS_VERT_TYPES_ALT = {"Surface": "ModelLevel", "2D": "2D"}

    #: do not raise Exception if invalid item is attempted to be assigned
    #: (Overwritten from base class)
    CRASH_ON_INVALID = False

    FORBIDDEN_KEYS = [
        "var_outlier_ranges",  # deprecated since v0.12.0
        "var_ref_outlier_ranges",  # deprecated since v0.12.0
        "remove_outliers",  # deprecated since v0.12.0
    ]

    ts_type = StrWithDefault("monthly")
    obs_vars = ListOfStrings()

    def __init__(
        self,
        model_id=None,
        obs_id=None,
        obs_vars=None,
        ts_type=None,
        start=None,
        stop=None,
        basedir_coldata=None,
        save_coldata=False,
        **kwargs,
    ):
        self.model_id = model_id
        self.obs_id = obs_id
        self.obs_vars = obs_vars

        self.ts_type = ts_type
        self.start = start
        self.stop = stop

        # crashes if input filter name is invalid
        self.filter_name = f"{ALL_REGION_NAME}-wMOUNTAINS"

        if basedir_coldata is not None:
            basedir_coldata = self._check_input_basedir_coldata(basedir_coldata)
        else:
            basedir_coldata = const.COLOCATEDDATADIR
        self.basedir_coldata = basedir_coldata
        self.save_coldata = save_coldata

        # END OF ASSIGNMENT OF MOST COMMON PARAMETERS - BELOW ARE FURTHER
        # CONFIG ATTRIBUTES, THAT ARE OPTIONAL AND LESS FREQUENTLY USED

        # Options related to obs reading and processing
        self.obs_name = None
        self.obs_data_dir = None
        self.obs_use_climatology = False

        self._obs_cache_only = False  # only relevant if obs is ungridded
        self.obs_vert_type = None
        self.obs_ts_type_read = None
        self.obs_filters = {}
        self._obs_is_vertical_profile = False
        self.colocation_layer_limits = None
        self.profile_layer_limits = None

        self.read_opts_ungridded = {}

        # Attributes related to model data
        self.model_name = None
        self.model_data_dir = None

        self.model_read_opts = {}

        self.model_use_vars = {}
        self.model_rename_vars = {}
        self.model_add_vars = {}
        self.model_to_stp = False

        self.model_ts_type_read = None
        self.model_read_aux = {}
        self.model_use_climatology = False

        self.gridded_reader_id = {"model": "ReadGridded", "obs": "ReadGridded"}

        self.flex_ts_type = True

        # Options related to time resampling
        self.min_num_obs = None
        self.resample_how = "mean"

        # Options related to outlier removal
        self.obs_remove_outliers = False
        self.model_remove_outliers = False

        # Custom outlier ranges for model and obs
        self.obs_outlier_ranges = {}
        self.model_outlier_ranges = {}

        self.zeros_to_nan = False
        self.harmonise_units = False
        self.regrid_res_deg = None
        self.colocate_time = False

        self.reanalyse_existing = True
        self.raise_exceptions = False
        self.keep_data = True

        self.add_meta = {}
        self.update(**kwargs)

    def _check_input_basedir_coldata(self, basedir_coldata):
        """
        Make sure input basedir_coldata is str and exists

        Parameters
        ----------
        basedir_coldata : str or Path
            basic output directory for colocated data

        Raises
        ------
        ValueError
            If input is invalid.

        Returns
        -------
        str
            valid output directory

        """
        if isinstance(basedir_coldata, Path):
            basedir_coldata = str(basedir_coldata)
        if isinstance(basedir_coldata, str):
            if not os.path.exists(basedir_coldata):
                os.mkdir(basedir_coldata)
            return basedir_coldata
        raise ValueError(f"Invalid input for basedir_coldata: {basedir_coldata}")

    def _check_basedir_coldata(self):
        """
        Make sure output directory for colocated data files exists

        Raises
        ------
        FileNotFoundError
            If :attr:`basedir_coldata` does not exist and cannot be created.

        Returns
        -------
        str
            current value of :attr:`basedir_coldata`

        """
        basedir_coldata = self.basedir_coldata
        if basedir_coldata is None:
            basedir_coldata = const.COLOCATEDDATADIR
            if not os.path.exists(basedir_coldata):
                logger.info(f"Creating directory: {basedir_coldata}")
                os.mkdir(basedir_coldata)
        elif isinstance(basedir_coldata, Path):
            basedir_coldata = str(basedir_coldata)
        if isinstance(basedir_coldata, str) and not os.path.exists(basedir_coldata):
            os.mkdir(basedir_coldata)
        if not os.path.exists(basedir_coldata):
            raise FileNotFoundError(
                f"Output directory for colocated data files {basedir_coldata} does not exist"
            )
        self.basedir_coldata = basedir_coldata
        return basedir_coldata

    @property
    def basedir_logfiles(self):
        """Base directory for storing logfiles"""
        p = chk_make_subdir(self.basedir_coldata, "logfiles")
        return p

    def add_glob_meta(self, **kwargs):
        """
        Add global metadata to :attr:`add_meta`

        Parameters
        ----------
        kwargs
            metadata to be added

        Returns
        -------
        None

        """
        self.add_meta.update(**kwargs)

    def __setitem__(self, key, val):
        if key == "basedir_coldata":
            val = self._check_input_basedir_coldata(val)
        super().__setitem__(key, val)

    def _period_from_start_stop(self) -> str:
        start, stop = start_stop(self.start, self.stop, stop_sub_sec=False)
        y0, y1 = start.year, stop.year
        assert y0 <= y1
        if y0 == y1:
            return str(y0)
        else:
            return f"{y0}-{y1}"


class Colocator(ColocationSetup):
    """High level class for running co-location

    Note
    ----
    This object inherits from :class:`ColocationSetup` and is also instantiated
    as such. For setup attributes, please see base class.
    """

    SUPPORTED_GRIDDED_READERS = {"ReadGridded": ReadGridded}
    SUPPORTED_GRIDDED_READERS.update(
        {ep.name: ep.load() for ep in metadata.entry_points(group="pyaerocom.gridded")}
    )

    STATUS_CODES = {
        1: "SUCCESS",
        2: "NOT OK: Missing/invalid model variable",
        3: "NOT OK: Missing/invalid obs variable",
        4: "NOT OK: Failed to read model variable",
        5: "NOT OK: Colocation failed",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._log = None
        self.logging = True
        self._loaded_model_data = {}
        self.data = {}

        self._processing_status = []
        self.files_written = []

        self._model_reader = None
        self._obs_reader = None

    @property
    def model_vars(self):
        """
        List of all model variables specified in config

        Note
        ----
        This method does not check if the variables are valid or available.

        Returns
        -------
        list
            list of all model variables specified in this setup.

        """
        ovars = self.obs_vars
        model_vars = []
        for ovar in ovars:
            if ovar in self.model_use_vars:
                model_vars.append(self.model_use_vars[ovar])
            else:
                model_vars.append(ovar)

        for ovar, mvars in self.model_add_vars.items():
            if not ovar in ovars:
                logger.warning(
                    f"Found entry in model_add_vars for obsvar {ovar} which "
                    f"is not specified in attr obs_vars, and will thus be "
                    f"ignored"
                )
            model_vars += mvars
        return model_vars

    @property
    def obs_is_ungridded(self):
        """
        bool: True if obs_id refers to an ungridded observation, else False
        """
        return True if self.obs_id in get_all_supported_ids_ungridded() else False

    @property
    def obs_is_vertical_profile(self):
        """
        bool: True if obs_id refers to a VerticalProfile, else False
        """
        return self._obs_is_vertical_profile

    @obs_is_vertical_profile.setter
    def obs_is_vertical_profile(self, value):
        self._obs_is_vertical_profile = value

    @property
    def model_reader(self):
        """
        Model data reader
        """
        if self._model_reader is not None:
            if self._model_reader.data_id == self.model_id:
                return self._model_reader
            logger.info(
                f"Reloading outdated model reader. ID of current reader: "
                f"{self._model_reader.data_id}. New ID: {self.model_id}"
            )
        self._model_reader = self._instantiate_gridded_reader(what="model")
        self._loaded_model_data = {}
        return self._model_reader

    def _check_data_id_obs_reader(self):
        """
        Check if obs_reader is instantiated with correct obs ID.

        Returns
        -------
        bool
            True if current obs reader can be used for obs reading, else False.
        """
        reader = self._obs_reader
        if reader is None:
            return False
        elif self.obs_is_ungridded and self.obs_id in reader.data_ids:
            return True
        elif self.obs_id == reader.data_id:
            return True

    @property
    def obs_reader(self):
        """
        Observation data reader
        """
        if not self._check_data_id_obs_reader():
            if self.obs_is_ungridded:
                self._obs_reader = ReadUngridded(
                    data_ids=[self.obs_id], data_dirs=self.obs_data_dir
                )
            else:
                self._obs_reader = self._instantiate_gridded_reader(what="obs")
        return self._obs_reader

    @property
    def output_dir(self):
        """
        str: Output directory for colocated data NetCDF files
        """
        self._check_basedir_coldata()
        loc = os.path.join(self.basedir_coldata, self.get_model_name())
        if not os.path.exists(loc):
            logger.info(f"Creating dir {loc}")
            os.mkdir(loc)
        return loc

    @property
    def processing_status(self):
        head = ["Model Var", "Obs Var", "Status"]
        tab = []
        for mvar, ovar, key in self._processing_status:
            tab.append([mvar, ovar, self.STATUS_CODES[key]])
        return pd.DataFrame(tab, columns=head)

    def get_model_name(self):
        """
        Get name of model

        Note
        ----
        Not to be confused with :attr:`model_id` which is always the database
        ID of the model, while model_name can differ from that and is used for
        output files, etc.

        Raises
        ------
        AttributeError
            If neither model_id or model_name are set

        Returns
        -------
        str
            preferably :attr:`model_name`, else :attr:`model_id`

        """
        if self.model_name is None:
            if self.model_id is None:
                raise AttributeError("Neither model_name nor model_id are set")
            return self.model_id
        return self.model_name

    def get_obs_name(self):
        """
        Get name of obsdata source

        Note
        ----
        Not to be confused with :attr:`obs_id` which is always the database
        ID of the observation dataset, while obs_name can differ from that
        and is used for output files, etc.

        Raises
        ------
        AttributeError
            If neither obs_id or obs_name are set

        Returns
        -------
        str
            preferably :attr:`obs_name`, else :attr:`obs_id`

        """
        if self.obs_name is None:
            if self.obs_id is None:
                raise AttributeError("Neither obs_name nor obs_id are set")
            return self.obs_id
        return self.obs_name

    def get_model_data(self, model_var):
        if model_var in self._loaded_model_data:
            mdata = self._loaded_model_data[model_var]
            if mdata.data_id == self.model_id:
                return mdata
        self._check_add_model_read_aux(model_var)
        mdata = self._read_gridded(var_name=model_var, is_model=True)
        self._loaded_model_data[model_var] = mdata
        return mdata

    def get_obs_data(self, obs_var):
        if self.obs_is_ungridded:
            return self._read_ungridded(obs_var)
        else:
            return self._read_gridded(obs_var, is_model=False)

    def get_start_str(self):
        if self.start is None:
            raise AttributeError("start time is not set")
        return to_datestring_YYYYMMDD(to_pandas_timestamp(self.start))

    def get_stop_str(self):
        if self.stop is None:
            raise AttributeError("stop time is not set")
        return to_datestring_YYYYMMDD(to_pandas_timestamp(self.stop))

    def prepare_run(self, var_list: list = None) -> dict:
        """
        Prepare colocation run for current setup.

        Parameters
        ----------
        var_name : str, optional
            Variable name that is supposed to be analysed. The default is None,
            in which case all defined variables are attempted to be colocated.

        Raises
        ------
        AttributeError
            If no observation variables are defined (:attr:`obs_vars` empty).

        Returns
        -------
        vars_to_process : dict
            Mapping of variables to be processed, keys are model vars, values
            are obs vars.

        """
        try:
            self._init_log()
        except Exception:
            logger.warning("Deactivating logging in Colocator")
            self.logging = False

        if isinstance(self.obs_vars, str):
            self.obs_vars = [self.obs_vars]
        elif not isinstance(self.obs_vars, list):
            raise AttributeError("obs_vars not defined or invalid, need list with strings...")
        self._check_obs_vars_available()
        self._check_obs_filters()
        self._check_model_add_vars()
        self._check_set_start_stop()

        vars_to_process = self._find_var_matches()
        if var_list is not None:
            vars_to_process = self._filter_var_matches_varlist(vars_to_process, var_list)

        (vars_to_process, ts_types) = self._check_load_model_data(vars_to_process)

        if self.save_coldata and not self.reanalyse_existing:
            vars_to_process = self._filter_var_matches_files_not_exist(vars_to_process, ts_types)
        return vars_to_process

    def run(self, var_list: list = None, **opts):
        """Perform colocation for current setup

        See also :func:`prepare_run`.

        Parameters
        ----------
        var_list : list, optional
            list of variables supposed to be analysed. The default is None,
            in which case all defined variables are attempted to be colocated.
        **opts
            keyword args that may be specified to change the current setup
            before colocation

        Returns
        -------
        dict
            nested dictionary, where keys are model variables, values are
            dictionaries comprising key / value pairs of obs variables and
            associated instances of :class:`ColocatedData`.
        """
        self.update(**opts)
        data_out = {}
        # ToDo: see if the following could be solved via custom context manager
        try:
            vars_to_process = self.prepare_run(var_list)
        except Exception:
            if self.raise_exceptions:
                self._print_processing_status()
                self._write_log("ABORTED: raise_exceptions is True\n")
                self._close_log()
                raise
            vars_to_process = {}
        self._print_coloc_info(vars_to_process)
        for mod_var, obs_var in vars_to_process.items():
            try:
                coldata = self._run_helper(
                    mod_var, obs_var
                )  # note this can be ColocatedData or ColocatedDataLists
                if not mod_var in data_out:
                    data_out[mod_var] = {}
                data_out[mod_var][obs_var] = coldata
                self._processing_status.append([mod_var, obs_var, 1])
            except Exception:
                msg = f"Failed to perform analysis: {traceback.format_exc()}\n"
                logger.warning(msg)
                self._processing_status.append([mod_var, obs_var, 5])
                self._write_log(msg)
                if self.raise_exceptions:
                    self._print_processing_status()
                    self._write_log("ABORTED: raise_exceptions is True\n")
                    self._close_log()
                    raise ColocationError(traceback.format_exc())
        self._write_log("Colocation finished")
        self._close_log()
        self._print_processing_status()
        if self.keep_data:
            self.data = data_out
        return data_out

    def get_nc_files_in_coldatadir(self):
        """
        Get list of NetCDF files in colocated data directory

        Returns
        -------
        list
            list of NetCDF file paths found

        """
        mask = f"{self.output_dir}/*.nc"
        return glob.glob(mask)

    def get_available_coldata_files(self, var_list: list = None) -> list:
        self._check_set_start_stop()

        def check_meta_match(meta, **kwargs):
            for key, val in kwargs.items():
                if not meta[key] == val:
                    return False
            return True

        mname = self.get_model_name()
        oname = self.get_obs_name()
        model_vars = self.model_vars
        obs_vars = self.obs_vars
        start, stop = self.get_start_str(), self.get_stop_str()
        valid = []
        all_files = self.get_nc_files_in_coldatadir()
        for file in all_files:
            try:
                meta = ColocatedData.get_meta_from_filename(file)
            except Exception:
                continue
            candidate = check_meta_match(
                meta, model_name=mname, obs_name=oname, start=start, stop=stop
            )
            if candidate and meta["model_var"] in model_vars and meta["obs_var"] in obs_vars:
                if var_list is None:
                    ok = True
                else:
                    ok = False
                    for var in var_list:
                        if meta["model_var"] == var or meta["obs_var"] == var:
                            ok = True
                            break
                if ok:
                    valid.append(file)

        return valid

    def _filter_var_matches_varlist(self, vars_to_process, var_list) -> dict:
        _vars_to_process = {}
        if isinstance(var_list, str):
            var_list = [var_list]
        for var_name in var_list:
            _subset = self._filter_var_matches_var_name(vars_to_process, var_name)
            _vars_to_process.update(**_subset)
        return _vars_to_process

    def _read_ungridded(self, var_name):
        """Helper to read UngriddedData

        Note
        ----
        reading is restricted to single variable UngriddedData objects here,
        due to multiple possibilities for variable specific obs filter
        definitions and because the colocation is done sequentially for each
        variable.

        Parameters
        ----------
        vars_to_read : str or list, optional
            variables that should be read from obs-network (:attr:`obs_id`)

        Returns
        -------
        UngriddedData
            loaded data object

        """
        obs_reader = self.obs_reader
        obs_filters_post = self._eval_obs_filters(var_name)

        obs_data = obs_reader.read(
            data_ids=[self.obs_id],
            vars_to_retrieve=var_name,
            only_cached=self._obs_cache_only,
            filter_post=obs_filters_post,
            **self.read_opts_ungridded,
        )

        if self.obs_remove_outliers:
            oor = self.obs_outlier_ranges
            if var_name in oor:
                low, high = oor[var_name]
            else:
                var_info = const.VARS[var_name]
                low, high = var_info.minimum, var_info.maximum
            obs_data.remove_outliers(
                var_name, low=low, high=high, inplace=True, move_to_trash=False
            )
        return obs_data

    def _check_obs_filters(self):
        obs_vars = self.obs_vars
        if any([x in self.obs_filters for x in obs_vars]):
            # variable specific obs_filters
            for ovar in obs_vars:
                if not ovar in self.obs_filters:
                    self.obs_filters[ovar] = {}

    def _check_load_model_data(self, var_matches):
        """
        Try to preload modeldata for input variable matches

        Note
        ----
        This will load all model fields for each obs variable in lazy mode, so
        should not require much storage. T

        Parameters
        ----------
        var_matches : dict
            dictionary specifying model / obs var pairs for colocation.

        Raises
        ------
        ColocationError
            If :attr:`raise_exceptions` is True and if one of the input
            model variables cannot be loaded.

        Returns
        -------
        filtered : dict
            `var_matches` filtered by entries for which model data could be
            successfully read.
        ts_types : dict
            data frequencies for each model variable that could be read. Those
            depend also on settings for :attr:`flex_ts_type`

        """
        filtered, ts_types = {}, {}
        for mvar, ovar in var_matches.items():
            try:
                mdata = self.get_model_data(mvar)
                filtered[mvar] = ovar
                ts_types[mvar] = mdata.ts_type
            except Exception as e:
                msg = f"Failed to load model data: {self.model_id} ({mvar}). Reason {e}"
                logger.warning(msg)
                self._write_log(msg + "\n")
                self._processing_status.append([mvar, ovar, 4])
                if self.raise_exceptions:
                    raise ColocationError(msg)
        return filtered, ts_types

    def _filter_var_matches_files_not_exist(self, var_matches, ts_types):
        filtered = {}
        for mvar, ovar in var_matches.items():
            ts_type = ts_types[mvar]
            fname = self._coldata_savename(ovar, mvar, ts_type)
            fp = os.path.join(self.output_dir, fname)
            if not os.path.exists(fp):
                filtered[mvar] = ovar
        return filtered

    def _check_model_add_vars(self):
        for ovar, mvars in self.model_add_vars.items():
            if not isinstance(mvars, list):
                raise ValueError("Values of model_add_vars need to be list")
            elif not all([isinstance(x, str) for x in mvars]):
                raise ValueError("Values of model_add_vars need to be list of strings")

    def _instantiate_gridded_reader(self, what):
        """
        Create reader for model or observational gridded data.

        Parameters
        ----------
        what : str
            Type of reader. ("model" or "obs")

        Returns
        -------
        Instance of reader class defined in self.SUPPORTED_GRIDDED_READERS
        """
        if what == "model":
            data_id = self.model_id
            data_dir = self.model_data_dir
        else:
            data_id = self.obs_id
            data_dir = self.obs_data_dir
        reader_class = self._get_gridded_reader_class(what=what)
        reader = reader_class(data_id=data_id, data_dir=data_dir)
        return reader

    def _get_gridded_reader_class(self, what):
        """Returns the class of the reader for gridded data."""
        try:
            reader = self.SUPPORTED_GRIDDED_READERS[self.gridded_reader_id[what]]
        except KeyError as e:
            raise NotImplementedError(
                f"Reader {self.gridded_reader_id[what]} is not supported: {e}"
            )
        return reader

    def _check_add_model_read_aux(self, model_var):
        if not model_var in self.model_read_aux:
            return False
        info = self.model_read_aux[model_var]
        if not isinstance(info, dict):
            raise ValueError(
                f"Invalid value for model_read_aux of variable {model_var}. "
                f"Need dictionary, got {info}"
            )
        elif not all([x in info for x in ["vars_required", "fun"]]):
            raise ValueError(
                f"Invalid value for model_read_aux dict of variable {model_var}. "
                f"Require keys vars_required and fun in dict, got {info}"
            )
        try:
            self.model_reader.add_aux_compute(var_name=model_var, **info)
        except DataCoverageError:
            return False
        return True

    def _check_obs_vars_available(self):
        if self.obs_vars == []:
            raise ColocationSetupError("no observation variables specified...")
        oreader = self.obs_reader
        if self.obs_is_ungridded:
            avail = oreader.get_vars_supported(self.obs_id, self.obs_vars)
        else:
            avail = []
            for ovar in self.obs_vars:
                if oreader.has_var(ovar):
                    avail.append(ovar)

        if len(self.obs_vars) > len(avail):
            for ovar in self.obs_vars:
                if not ovar in avail:
                    logger.warning(
                        f"Obs variable {ovar} is not available in {self.obs_id} "
                        f"and will be ignored"
                    )
                    self._processing_status.append([None, ovar, 3])

            if self.raise_exceptions:
                invalid = [var for var in self.obs_vars if not var in avail]
                invalid = "; ".join(invalid)
                raise DataCoverageError(f"Invalid obs var(s) for {self.obs_id}: {invalid}")

            self.obs_vars = avail

    def _print_processing_status(self):
        mname = self.get_model_name()
        oname = self.get_obs_name()
        logger.info(f"Colocation processing status for {mname} vs. {oname}")
        logger.info(self.processing_status)

    def _filter_var_matches_var_name(self, var_matches, var_name):
        filtered = {}
        for mvar, ovar in var_matches.items():
            if mvar in var_name or ovar in var_name:
                filtered[mvar] = ovar
        if len(filtered) == 0:
            raise DataCoverageError(var_name)
        return filtered

    def _find_var_matches(self):
        """Find variable matches in model data for input obs variables"""

        # dictionary that will map model variables (keys) with observation
        # variables (values)
        var_matches = {}

        all_ok = True
        muv = self.model_use_vars
        modreader = self.model_reader
        for ovar in self.obs_vars:
            if ovar in muv:
                mvar = muv[ovar]
            else:
                mvar = ovar
            self._check_add_model_read_aux(mvar)
            if modreader.has_var(mvar):
                var_matches[mvar] = ovar
            else:
                self._processing_status.append([mvar, ovar, 2])
                all_ok = False

            if ovar in self.model_add_vars:  # observation variable
                addvars = self.model_add_vars[ovar]
                for addvar in addvars:
                    self._check_add_model_read_aux(addvar)
                    if modreader.has_var(addvar):
                        var_matches[addvar] = ovar
                    else:
                        self._processing_status.append([addvar, ovar, 2])
                        all_ok = False

        if not all_ok and self.raise_exceptions:
            raise DataCoverageError("Some model variables are not available")

        return var_matches

    def _get_ts_type_read(self, var_name, is_model):
        """
        Get *desired* reading frequency for gridded reading

        Parameters
        ----------
        var_name : str
            Name of variable to be read.
        is_model : bool
            True if reading refers to model reading, else False (e.g. gridded
            satellite obs).

        Raises
        ------
        ValueError


        Returns
        -------
        str or None
            frequency to be read.

        """
        tst = self.ts_type  # default
        if is_model and self.model_ts_type_read is not None:
            tst = self.model_ts_type_read
            if tst == "":
                tst = self.ts_type
        elif not is_model and self.obs_ts_type_read is not None:
            tst = self.obs_ts_type_read
        if isinstance(tst, dict):
            if var_name in tst:
                tst = tst[var_name]
            else:
                tst = self.ts_type
        return tst

    def _read_gridded(self, var_name, is_model):
        start, stop = self.start, self.stop
        ts_type_read = self._get_ts_type_read(var_name, is_model)
        kwargs = {}
        if is_model:
            reader = self.model_reader
            vert_which = self.obs_vert_type
            if self.model_use_climatology:
                # overwrite start and stop to read climatology file for model
                start, stop = 9999, None
            if var_name in self.model_read_opts:
                kwargs.update(self.model_read_opts[var_name])
        else:
            reader = self.obs_reader
            vert_which = None
            ts_type_read = self.obs_ts_type_read
            kwargs.update(self._eval_obs_filters(var_name))

        try:
            data = reader.read_var(
                var_name,
                start=start,
                stop=stop,
                ts_type=ts_type_read,
                vert_which=vert_which,
                flex_ts_type=self.flex_ts_type,
                **kwargs,
            )
        except DataCoverageError:
            vert_which_alt = self._try_get_vert_which_alt(is_model, var_name)
            data = reader.read_var(
                var_name,
                start=start,
                stop=stop,
                ts_type=ts_type_read,
                flex_ts_type=self.flex_ts_type,
                vert_which=vert_which_alt,
            )

        data = self._check_remove_outliers_gridded(data, var_name, is_model)
        return data

    def _try_get_vert_which_alt(self, is_model, var_name):
        if is_model:
            if self.obs_vert_type in self.OBS_VERT_TYPES_ALT:
                return self.OBS_VERT_TYPES_ALT[self.obs_vert_type]
        raise DataCoverageError(f"No alternative vert type found for {var_name}")

    def _check_remove_outliers_gridded(self, data, var_name, is_model):
        if is_model:
            rm_outliers = self.model_remove_outliers
            outlier_ranges = self.model_outlier_ranges
        else:
            rm_outliers = self.obs_remove_outliers
            outlier_ranges = self.obs_outlier_ranges

        if len(outlier_ranges) > 0 and not rm_outliers:
            logger.warning(
                f"WARNING: Found definition of outlier ranges for {var_name} "
                f"({data.data_id}) but outlier removal is deactivated. Consider "
                f"checking your setup (note: model or obs outlier removal can be "
                f"activated via attrs. model_remove_outliers and remove_outliers, "
                f"respectively"
            )

        if rm_outliers:
            if var_name in outlier_ranges:
                low, high = outlier_ranges[var_name]
            else:
                var_info = const.VARS[var_name]
                low, high = var_info.minimum, var_info.maximum
            data.check_unit()
            data.remove_outliers(low, high, inplace=True)
        return data

    def _eval_obs_filters(self, var_name):
        obs_filters = self["obs_filters"]
        if var_name in obs_filters:
            obs_filters = obs_filters[var_name]
        remaining = {}
        if not isinstance(obs_filters, dict):
            raise AttributeError(
                f"Detected obs_filters attribute in Colocator class, "
                f"which is not a dictionary: {obs_filters}"
            )
        for key, val in obs_filters.items():
            # keep ts_type filter in remaining (added on 17.2.21, 0.10.0 -> 0.10.1)
            if key in self and not key == "ts_type":  # can be handled
                if isinstance(self[key], dict) and isinstance(val, dict):
                    self[key].update(val)
                else:
                    self[key] = val
            else:
                remaining[key] = val
        return remaining

    def _save_coldata(self, coldata):
        """Helper for saving colocateddata"""
        obs_var, mod_var = coldata.metadata["var_name_input"]
        if mod_var in self.model_rename_vars:
            mvar = self.model_rename_vars[mod_var]
            logger.info(
                f"Renaming model variable from {mod_var} to {mvar} in "
                f"ColocatedData before saving to NetCDF."
            )
            coldata.rename_variable(mod_var, mvar, self.model_id)
        else:
            mvar = mod_var

        if hasattr(coldata, "vertical_layer"):
            # save colocated vertical layer netCDF files with vertical layers in km
            if not Unit(coldata.data.altitude_units) == Unit("km"):
                start = Unit(coldata.data.altitude_units).convert(
                    coldata.vertical_layer["start"], other="km"
                )
                end = Unit(coldata.data.altitude_units).convert(
                    coldata.vertical_layer["end"], other="km"
                )
                vertical_layer = {"start": start, "end": end}
            else:
                vetical_layer = coldata.vertical_layer

            savename = self._coldata_savename(
                obs_var, mvar, coldata.ts_type, vertical_layer=vertical_layer
            )

        else:
            savename = self._coldata_savename(obs_var, mvar, coldata.ts_type)
        fp = coldata.to_netcdf(self.output_dir, savename=savename)
        self.files_written.append(fp)
        msg = f"WRITE: {fp}\n"
        self._write_log(msg)
        logger.info(msg)

    def _eval_resample_how(self, model_var, obs_var):
        rshow = self.resample_how
        if not isinstance(rshow, dict):
            return rshow

        if obs_var in rshow:
            return rshow[obs_var]
        elif model_var in rshow:
            return rshow[model_var]
        else:
            return None

    def _infer_start_stop_yr_from_model_reader(self):
        """
        Infer start / stop year for colocation from gridded model reader

        Sets :attr:`start` and :attr:`stop`

        """
        # get sorted list of years available in model data (files with year
        # 9999 denote climatological data)
        yrs_avail = self.model_reader.years_avail
        if self.model_use_climatology:
            if not 9999 in yrs_avail:
                raise DataCoverageError("No climatology files available")
            first, last = 9999, None
        else:
            if 9999 in yrs_avail:
                yrs_avail = [x for x in yrs_avail if not x == 9999]
            first, last = yrs_avail[0], yrs_avail[-1]
            if first == last:
                last = None
        self.start = first
        self.stop = last

    def _check_set_start_stop(self):
        if self.start is None:
            self._infer_start_stop_yr_from_model_reader()
        if self.model_use_climatology:
            if self.stop is not None or not isinstance(self.start, int):
                raise ColocationSetupError(
                    "Conflict: only single year analyses are support for model "
                    'climatology fields, please specify "start" as integer '
                    'denoting the year, and set "stop"=None'
                )
        self.start, self.stop = start_stop(self.start, self.stop)

    def _coldata_savename(self, obs_var, mod_var, ts_type, **kwargs):
        """Get filename of colocated data file for saving"""
        if "vertical_layer" in kwargs:
            vertical_layer = kwargs["vertical_layer"]
        else:
            vertical_layer = None
        name = ColocatedData._aerocom_savename(
            obs_var=obs_var,
            obs_id=self.get_obs_name(),
            mod_var=mod_var,
            mod_id=self.get_model_name(),
            start_str=self.get_start_str(),
            stop_str=self.get_stop_str(),
            ts_type=ts_type,
            filter_name=self.filter_name,
            vertical_layer=vertical_layer,
        )
        return f"{name}.nc"

    def _get_colocation_ts_type(self, model_ts_type, obs_ts_type=None):
        chk = [self.ts_type, model_ts_type]
        if obs_ts_type is not None:
            chk.append(obs_ts_type)
        return get_lowest_resolution(*chk)

    @property
    def _colocation_func(self):
        """
        Function used for colocation

        Returns
        -------
        callable
            function the performs co-location operation

        """

        if self.obs_is_vertical_profile:
            return colocate_vertical_profile_gridded
        if self.obs_is_ungridded:
            return colocate_gridded_ungridded
        else:
            return colocate_gridded_gridded

    def _prepare_colocation_args(self, model_var: str, obs_var: str):
        model_data = self.get_model_data(model_var)
        obs_data = self.get_obs_data(obs_var)

        if getattr(obs_data, "is_vertical_profile", None):
            self.obs_is_vertical_profile = obs_data.is_vertical_profile

        rshow = self._eval_resample_how(model_var, obs_var)

        if self.model_use_climatology:
            baseyr = self.start.year
        else:
            baseyr = None
        # input args shared between all colocation functions
        args = dict(
            data=model_data,
            data_ref=obs_data,
            start=self.start,
            stop=self.stop,
            filter_name=self.filter_name,
            regrid_res_deg=self.regrid_res_deg,
            harmonise_units=self.harmonise_units,
            update_baseyear_gridded=baseyr,
            min_num_obs=self.min_num_obs,
            colocate_time=self.colocate_time,
            resample_how=rshow,
        )
        if self.obs_is_ungridded:
            ts_type = self._get_colocation_ts_type(model_data.ts_type)
            args.update(
                ts_type=ts_type,
                var_ref=obs_var,
                use_climatology_ref=self.obs_use_climatology,
            )
        else:
            ts_type = self._get_colocation_ts_type(model_data.ts_type, obs_data.ts_type)
            args.update(ts_type=ts_type)
        if self.obs_is_vertical_profile:
            args.update(
                colocation_layer_limits=self.colocation_layer_limits,
                profile_layer_limits=self.profile_layer_limits,
            )
        return args

    def _check_dimensionality(self, args):
        mdata = args["data"]
        odata = args["data_ref"]
        from pyaerocom.exceptions import DataDimensionError
        from pyaerocom.griddeddata import GriddedData

        if mdata.ndim == 4 and self.obs_vert_type == "Surface":
            mdata = mdata.extract_surface_level()
            args["data"] = mdata

        if isinstance(odata, GriddedData):
            if odata.ndim == 4 and self.obs_vert_type == "Surface":
                odata = odata.extract_surface_level()
                args["data_ref"] = odata
            elif odata.ndim > 3:
                raise DataDimensionError(
                    f"cannot co-locate model data with more than 3 dimensions: {odata}"
                )
        return args

    def _run_helper(self, model_var: str, obs_var: str):
        logger.info(f"Running {self.model_id} ({model_var}) vs. {self.obs_id} ({obs_var})")
        args = self._prepare_colocation_args(model_var, obs_var)
        args = self._check_dimensionality(args)
        coldata = self._colocation_func(**args)

        if isinstance(coldata, ColocatedData):
            coldata.data.attrs["model_name"] = self.get_model_name()
            coldata.data.attrs["obs_name"] = self.get_obs_name()
            coldata.data.attrs["vert_code"] = self.obs_vert_type

            coldata.data.attrs.update(**self.add_meta)

            if self.zeros_to_nan:
                coldata = coldata.set_zeros_nan()
            if self.model_to_stp:
                coldata = correct_model_stp_coldata(coldata)
            if self.save_coldata:
                self._save_coldata(coldata)

        elif isinstance(coldata, ColocatedDataLists):  # look into intertools chain.from_iterable
            for i_list in coldata:
                for coldata_obj in i_list:
                    coldata_obj.data.attrs["model_name"] = self.get_model_name()
                    coldata_obj.data.attrs["obs_name"] = self.get_obs_name()
                    coldata_obj.data.attrs["vert_code"] = self.obs_vert_type
                    coldata_obj.data.attrs.update(**self.add_meta)
                    if self.zeros_to_nan:
                        coldata_obj = coldata_obj.set_zeros_nan()
                    if self.model_to_stp:  # TODO: check is this needs modifying
                        coldata = correct_model_stp_coldata(coldata_obj)
                    if self.save_coldata:
                        self._save_coldata(coldata_obj)

        else:
            raise Exception(
                f"Invalid coldata type returned by colocation function {self._colocation_func}"
            )

        return coldata

    def _print_coloc_info(self, var_matches):
        if not var_matches:
            logger.info("Nothing to colocate")
            return
        logger.info("The following variable combinations will be colocated\nMODEL-VAR\tOBS-VAR")

        for key, val in var_matches.items():
            logger.info(f"{key}\t{val}")

    def _init_log(self):
        logdir = chk_make_subdir(self.basedir_logfiles, self.get_model_name())
        oname = self.get_obs_name()
        datestr = datetime.today().strftime("%Y%m%d")
        datetimestr = datetime.today().strftime("%d-%m-%Y %H:%M")

        fname = f"{oname}_{datestr}.log"
        logfile = os.path.join(logdir, fname)
        self._log = log = open(logfile, "a+")
        log.write("\n------------------ NEW ----------------\n")
        log.write(f"Timestamp: {datetimestr}\n\n")
        log.write("Analysis configuration\n")
        ignore = ["_log", "logging", "data", "_model_reader", "_obs_reader"]
        for key, val in self.items():
            if key in ignore:
                continue
            log.write(f"{key}: {val}\n")

    def _write_log(self, msg):
        if self.logging:
            self._log.write(msg)

    def _close_log(self):
        if self._log is not None:
            self._log.close()
            self._log = None
