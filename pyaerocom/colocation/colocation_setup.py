import logging
import os
import sys
from collections.abc import Callable
from functools import cached_property
from pathlib import Path
from typing import Literal

import pandas as pd
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)

from pyaerocom import const
from pyaerocom.climatology_config import ClimatologyConfig
from pyaerocom._lowlevel_helpers import LayerLimits, RegridResDeg
from pyaerocom.config import ALL_REGION_NAME
from pyaerocom.helpers import start_stop
from pyaerocom.io.pyaro.pyaro_config import PyaroConfig

logger = logging.getLogger(__name__)


if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class ColocationSetup(BaseModel):
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

    pyaro_config: PyaroConfig
        In the case Pyaro is used, a config must be provided. In that case obs_id(see below)
        is ignored and only the config is used.
    obs_id : str
        ID of observation network to be used.
    obs_vars : tuple[str, ...]
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
    basedir_coldata : str | Path
        Base directory for storing of colocated data files.
    save_coldata : bool
        if True, colocated data objects are saved as NetCDF file.
    obs_name : str, optional
        if provided, this string will be used in colocated data filename to
        specify obsnetwork, else obs_id will be used.
    obs_data_dir : str, optional
        location of obs data. If None, attempt to infer obs location based on
        obs ID.
    obs_use_climatology : ClimatologyConfig | bool, optional
        Configuration for climatology. If True is given, a default configuration is made.
        With False, climatology is turned off
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
    model_kwargs: dict
        Key word arguments to be given to the model reader class's read_var and init function
    gridded_reader_id : dict
        BETA: dictionary specifying which gridded reader is supposed to be used
        for model (and gridded obs) reading. Note: this is a workaround
        solution and will likely be removed in the future when the gridded
        reading API is more harmonised
        (see https://github.com/metno/pyaerocom/issues/174).
    flex_ts_type : bool
        Boolean specifying whether reading frequency of gridded data is
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
    regrid_res_deg : float or dict, optional
        regrid resolution in degrees. If specified, the input gridded data
        objects will be regridded in lon / lat dimension to the input
        resolution (if input is float, both lat and lon are regridded to that
        resolution, if input is dict, use keys `lat_res_deg` and `lon_res_deg`
        to specify regrid resolutions, respectively). Default is None.
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
        skipped for the associated variable. This flag is also used for contour-plots.
        Default is True.
    raise_exceptions : bool
        if True, Exceptions that may occur for individual variables to be
        processed, are raised, else the analysis is skipped for such cases.
    keep_data : bool
        if True, then all colocated data objects computed when running
        :func:`run` will be stored in :attr:`data`. Defaults to True.
    add_meta : dict
        additional metadata that is supposed to be added to each output
        :class:`ColocatedData` object.
    main_freq:
        Main output frequency for AeroVal (some of the AeroVal processing
        steps are only done for this resolution, since they would create too
        much output otherwise, such as statistics timeseries or scatter plot in
        "Overall Evaluation" tab on AeroVal).
        Note that this frequency needs to be included in next setting "freqs".
    freqs:
        Frequencies for which statistical parameters are computed
    """

    ##########################
    # Pydantic ConfigDict
    ##########################
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        allow="extra",
        protected_namespaces=(),
        # TODO
        # frozen=True,  # make immutable
        # validate_assignment=True,
    )

    #########################
    # Init Input
    #########################

    model_id: str | None
    obs_id: str | None
    obs_vars: tuple[str, ...] | str

    @field_validator("obs_vars")
    @classmethod
    def validate_obs_vars(cls, v):
        if isinstance(v, str):
            return (v,)
        return v

    ts_type: str
    start: pd.Timestamp | int | str | None
    stop: pd.Timestamp | int | str | None

    @field_validator("start", "stop")
    @classmethod
    def validate_start_stop(cls, v):
        if isinstance(v, int):
            return v
        if isinstance(v, str):
            return pd.Timestamp(v)

    pyaro_config: PyaroConfig | None = None

    ###############################
    # Attributes with defaults
    ###############################

    #: Dictionary specifying alternative vertical types that may be used to
    #: read model data. E.g. consider the variable is  ec550aer,
    #: obs_vert_type='Surface' and obs_vert_type_alt=dict(Surface='ModelLevel').
    #: Now, if a model that is used for the analysis does not contain a data
    #: file for ec550aer at the surface ('*ec550aer*Surface*.nc'), then, the
    #: colocation routine will look for '*ec550aer*ModelLevel*.nc' and if this
    #: exists, it will load it and extract the surface level.
    OBS_VERT_TYPES_ALT: dict[str, str] = {"Surface": "ModelLevel", "2D": "2D"}

    #: do not raise Exception if invalid item is attempted to be assigned
    #: (Overwritten from base class)
    CRASH_ON_INVALID: bool = False

    FORBIDDEN_KEYS: list[str] = [
        "var_outlier_ranges",  # deprecated since v0.12.0
        "var_ref_outlier_ranges",  # deprecated since v0.12.0
        "remove_outliers",  # deprecated since v0.12.0
    ]

    # crashes if input filter name is invalid
    filter_name: str = f"{ALL_REGION_NAME}-wMOUNTAINS"

    basedir_coldata: str | Path = Field(default=const.COLOCATEDDATADIR, validate_default=True)

    @field_validator("basedir_coldata")
    @classmethod
    def validate_basedirs(cls, v):
        if not os.path.exists(v):
            tmp = Path(v) if isinstance(v, str) else v
            tmp.mkdir(parents=True, exist_ok=True)
        return v

    save_coldata: bool = False

    # Options related to obs reading and processing
    obs_name: str | None = None
    obs_data_dir: Path | str | None = None

    obs_use_climatology: ClimatologyConfig | bool = False

    @field_validator("obs_use_climatology")
    @classmethod
    def validate_obs_use_climatology(cls, v):
        if isinstance(v, ClimatologyConfig):
            return v

        if isinstance(v, bool):
            if v:
                return ClimatologyConfig()
            else:
                return v

        raise ValidationError

    obs_cache_only: bool = False  # only relevant if obs is ungridded
    obs_vert_type: str | None = None
    obs_ts_type_read: str | dict | None = None
    obs_filters: dict = {}
    colocation_layer_limits: tuple[LayerLimits, ...] | None = None
    profile_layer_limits: tuple[LayerLimits, ...] | None = None
    read_opts_ungridded: dict | None = {}

    # Attributes related to model data
    model_name: str | None = None
    model_data_dir: Path | str | None = None

    model_read_opts: dict | None = {}

    model_use_vars: dict[str, str] | None = {}
    model_rename_vars: dict[str, str] | None = {}
    model_add_vars: dict[str, tuple[str, ...]] | None = {}
    model_to_stp: bool = False

    model_ts_type_read: str | dict | None = None
    model_read_aux: (
        dict[str, dict[Literal["vars_required", "fun"], list[str] | Callable]] | None
    ) = {}
    model_use_climatology: bool = False

    gridded_reader_id: dict[str, str] = {"model": "ReadGridded", "obs": "ReadGridded"}

    flex_ts_type: bool = True

    # Options related to time resampling
    min_num_obs: dict | int | None = None
    resample_how: str | dict | None = "mean"

    # Options related to outlier removal
    obs_remove_outliers: bool = False
    model_remove_outliers: bool = False

    # Custom outlier ranges for model and obs
    obs_outlier_ranges: dict[str, tuple[float, float]] | None = {}
    model_outlier_ranges: dict[str, tuple[float, float]] | None = {}
    zeros_to_nan: bool = False
    harmonise_units: bool = False
    regrid_res_deg: float | RegridResDeg | None = None
    colocate_time: bool = False
    reanalyse_existing: bool = True
    raise_exceptions: bool = False
    keep_data: bool = True
    add_meta: dict | None = {}

    model_kwargs: dict = {}

    main_freq: str = "monthly"
    freqs: list[str] = ["monthly", "yearly"]

    @field_validator("model_kwargs")
    @classmethod
    def validate_kwargs(cls, v):
        forbidden = [
            "vert_which",
        ]  # Forbidden key names which are not found in colocation_setup.model_field, or has another name there
        for key in v:
            if key in list(cls.model_fields.keys()) + forbidden:
                raise ValueError(f"Key {key} not allowed in model_kwargs")
        return v

    # Override __init__ to allow for positional arguments
    def __init__(
        self,
        model_id: str | None = None,
        pyaro_config: PyaroConfig | None = None,
        obs_id: str | None = None,
        obs_vars: tuple[str, ...] | None = (),
        ts_type: str = "monthly",
        start: pd.Timestamp | int | None = None,
        stop: pd.Timestamp | int | None = None,
        basedir_coldata: str = const.COLOCATEDDATADIR,
        save_coldata: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(
            model_id=model_id,
            pyaro_config=pyaro_config,
            obs_id=obs_id,
            obs_vars=obs_vars,
            ts_type=ts_type,
            start=start,
            stop=stop,
            basedir_coldata=basedir_coldata,
            save_coldata=save_coldata,
            **kwargs,
        )

    # Model validator for forbidden keys
    @model_validator(mode="after")
    def validate_no_forbidden_keys(self):
        for key in self.FORBIDDEN_KEYS:
            if key in ColocationSetup.model_fields:
                raise ValidationError
        return self

    @cached_property
    def basedir_logfiles(self):
        p = Path(self.basedir_coldata) / "logfiles"
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)
        return str(p)

    @model_validator(mode="after")
    def validate_pyaro_config(self):
        if self.pyaro_config is None:
            return self
        if self.pyaro_config.name != self.obs_id:
            logger.info(
                f"Data ID in Pyaro config {self.pyaro_config.name} does not match obs_id {self.obs_id}. Setting Pyaro config to None!"
            )
            self.pyaro_config = None
        if self.pyaro_config is not None:
            if isinstance(self.pyaro_config, dict):
                logger.info("pyaro config was given as dict. Will try to convert to PyaroConfig")
                self.pyaro_config = PyaroConfig(**self.pyaro_config)
            if self.pyaro_config.name != self.obs_id:
                logger.info(
                    f"Data ID in Pyaro config {self.pyaro_config.name} does not match obs_id {self.obs_id}. Setting Obs ID to match Pyaro Config!"
                )
                self.obs_id = self.pyaro_config.name
            if self.obs_id is None:
                self.obs_id = self.pyaro_config.name
        return self

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

    def _period_from_start_stop(self) -> str:
        start, stop = start_stop(self.start, self.stop, stop_sub_sec=False)
        y0, y1 = start.year, stop.year
        assert y0 <= y1
        if y0 == y1:
            return str(y0)
        else:
            return f"{y0}-{y1}"

    def update(self, data: dict) -> Self:
        # provide an update() method analogous to MutableMapping's one

        # validate values in data
        update = self.model_dump()
        update.update(data)
        self.model_validate(update)
        # assign values from data
        for k, v in data.items():
            logger.debug(f"updating value of '{k}' from '{getattr(self, k, None)}' to '{v}'")
            setattr(self, k, v)
        return self
