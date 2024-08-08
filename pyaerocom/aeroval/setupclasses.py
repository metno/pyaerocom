import logging
import os
import sys
from datetime import timedelta
from functools import cached_property
from getpass import getuser
from pathlib import Path
from typing import Annotated, Literal

from pyaerocom.aeroval.glob_defaults import VarWebInfo, VarWebScaleAndColormap

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

import aerovaldb
import pandas as pd
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PositiveInt,
    computed_field,
    field_serializer,
    field_validator,
)

from pyaerocom import __version__, const
from pyaerocom.aeroval.aux_io_helpers import ReadAuxHandler
from pyaerocom.aeroval.collections import ModelCollection, ObsCollection
from pyaerocom.aeroval.exceptions import ConfigError
from pyaerocom.aeroval.helpers import (
    _check_statistics_periods,
    _get_min_max_year_periods,
    check_if_year,
)
from pyaerocom.aeroval.json_utils import read_json, set_float_serialization_precision
from pyaerocom.colocation.colocation_setup import ColocationSetup

logger = logging.getLogger(__name__)


class OutputPaths(BaseModel):
    """
    Setup class for output paths of json files and co-located data

    This interface generates all paths required for an experiment.

    Attributes
    ----------
    proj_id : str
        project ID
    exp_id : str
        experiment ID
    json_basedir : str, Path
    avdb_resource : str, Path, None
        An aerovaldb resource identifier as expected by aerovaldb.open()[1].
        If not provided, pyaerocom will fall back to using json_basedir, for
        backwards compatibility.

        [1] https://aerovaldb.readthedocs.io/en/latest/api.html#aerovaldb.open
    """

    # Pydantic ConfigDict
    model_config = ConfigDict(arbitrary_types_allowed=True)

    _JSON_SUBDIRS: list[str] = [
        "map",
        "ts",
        "ts/diurnal",
        "scat",
        "hm",
        "hm/ts",
        "contour",
        "profiles",
    ]
    avdb_resource: Path | str | None = None

    json_basedir: Path | str = Field(
        default=os.path.join(const.OUTPUTDIR, "aeroval/data"), validate_default=True
    )
    coldata_basedir: Path | str = Field(
        default=os.path.join(const.OUTPUTDIR, "aeroval/coldata"), validate_default=True
    )

    @field_validator("json_basedir", "coldata_basedir")
    @classmethod
    def validate_basedirs(cls, v):
        if not os.path.exists(v):
            tmp = Path(v) if isinstance(v, str) else v
            tmp.mkdir(parents=True, exist_ok=True)
        return v

    proj_id: str
    exp_id: str

    def _check_init_dir(self, loc, assert_exists):
        if assert_exists and not os.path.exists(loc):
            os.makedirs(loc)
        return loc

    def get_coldata_dir(self, assert_exists=True):
        loc = os.path.join(self.coldata_basedir, self.proj_id, self.exp_id)
        return self._check_init_dir(loc, assert_exists)

    def get_json_output_dirs(self, assert_exists=True):
        out = {}
        base = os.path.join(self.json_basedir, self.proj_id, self.exp_id)
        for subdir in self._JSON_SUBDIRS:
            loc = self._check_init_dir(os.path.join(base, subdir), assert_exists)
            out[subdir] = loc
        # for cams2_83 the extra 'forecast' folder will contain the median scores if computed
        if self.proj_id == "cams2-83":
            loc = self._check_init_dir(os.path.join(base, "forecast"), assert_exists)
            out["forecast"] = loc
        return out


class ModelMapsSetup(BaseModel):
    maps_freq: Literal["hourly", "daily", "monthly", "yearly", "coarsest"] = "coarsest"
    maps_res_deg: PositiveInt = 5


class CAMS2_83Setup(BaseModel):
    use_cams2_83: bool = False


class StatisticsSetup(BaseModel, extra="allow"):
    """
    Setup options for statistical calculations

    Attributes
    ----------
    weighted_stats : bool
        if True, statistics are calculated using area weights,
        this is only relevant for gridded / gridded evaluations.
    annual_stats_constrained : bool
        if True, then only sites are considered that satisfy a potentially
        specified annual resampling constraint (see
        :attr:`pyaerocom.colocation.ColocationSetup.min_num_obs`). E.g.

        lets say you want to calculate statistics (bias,
        correlation, etc.) for monthly model / obs data for a given site and
        year. Lets further say, that there are only 8 valid months of data, and
        4 months are missing, so statistics will be calculated for that year
        based on 8 vs. 8 values. Now if
        :attr:`pyaerocom.colocation.ColocationSetup.min_num_obs` is
        specified in way that requires e.g. at least 9 valid months to
        represent the whole year, then this station will not be considered in
        case `annual_stats_constrained` is True, else it will. Defaults to
        False.
    stats_tseries_base_freq : str, optional
        The statistics Time Series display in AeroVal (under Overall Evaluation)
        is computed in intervals of a certain frequency, which is specified
        via :attr:`TimeSetup.main_freq` (defaults to monthly). That is,
        monthly colocated data is used as a basis to compute the statistics
        for each month (e.g. if you have 10 sites, then statistics will be
        computed based on 10 monthly values for each month of the timeseries,
        1 value for each site). `stats_tseries_base_freq` may be specified in
        case a higher resolution is supposed to be used as a basis to compute
        the timeseries in the resolution specified by
        :attr:`TimeSetup.main_freq` (e.g. if daily is specified here, then for
        the above example 310 values would be used - 31 for each site - to
        compute the statistics for a given month (in this case, a month with 31
        days, obviously).
    drop_stats: tuple, optional
        tuple of strings with names of statistics (as determined by keys in
        aeroval.glob_defaults.py's statistics_defaults) to not compute. For example,
        setting drop_stats = ("mb", "mab"), results in json files in hm/ts with
        entries which do not contain the mean bias and mean absolute bias,
        but the other statistics are preserved.
    stats_decimals: int, optional
        If provided, overwrites the decimals key in glod_defaults for the statistics, which has a deault of 3.
        Setting this higher of lower changes the number of decimals shown on the Aeroval webpage.
    round_floats_precision: int, optional
        Sets the precision argument for the function `pyaerocom.aaeroval.json_utils:set_float_serialization_precision`


    Parameters
    ----------
    kwargs
        any of the supported attributes, e.g.
        `StatisticsSetup(annual_stats_constrained=True)`

    """

    # Pydantic ConfigDict
    model_config = ConfigDict(protected_namespaces=())
    # StatisticsSetup attributes
    MIN_NUM: PositiveInt = 1
    weighted_stats: bool = True
    annual_stats_constrained: bool = False

    # Trends config
    add_trends: bool = False  # Adding trend calculations, only trends over the average time series over stations in a region
    avg_over_trends: bool = (
        False  # Adds calculation of avg over trends of time series of stations in region
    )
    obs_min_yrs: PositiveInt = 0  # Removes stations with less than this number of years of valid data (a year with data points in all four seasons) Should in most cases be the same as stats_min_yrs
    stats_min_yrs: PositiveInt = obs_min_yrs  # Calculates trends if number of valid years are equal or more than this. Should in most cases be the same as obs_min_yrs
    sequential_yrs: bool = False  # Whether or not the min_yrs should be sequential

    stats_tseries_base_freq: str | None = None
    forecast_evaluation: bool = False
    forecast_days: PositiveInt = 4
    use_fairmode: bool = False
    use_diurnal: bool = False
    obs_only_stats: bool = False
    model_only_stats: bool = False
    drop_stats: tuple[str, ...] = ()
    stats_decimals: int | None = None
    round_floats_precision: int | None = None

    if round_floats_precision:
        set_float_serialization_precision(round_floats_precision)


class TimeSetup(BaseModel):
    DEFAULT_FREQS: Literal["monthly", "yearly"] = "monthly"
    SEASONS: list[str] = ["all", "DJF", "MAM", "JJA", "SON"]
    main_freq: str = "monthly"
    freqs: list[str] = ["monthly", "yearly"]
    periods: list[str] = Field(default_factory=list)
    add_seasons: bool = True

    def get_seasons(self):
        """
        Get list of seasons to be analysed

        Returns :attr:`SEASONS` if :attr:`add_seasons` it True, else `[
        'all']` (only whole year).

        Returns
        -------
        list
            list of season strings for analysis

        """
        if self.add_seasons:
            return self.SEASONS
        return ["all"]

    def _get_all_period_strings(self):
        """
        Get list of all period strings for evaluation

        Returns
        -------
        list
            list of period / season strings
        """
        output = []
        for per in self.periods:
            for season in self.get_seasons():
                perstr = f"{per}-{season}"
                output.append(perstr)
        return output


class WebDisplaySetup(BaseModel):
    # Pydantic ConfigDict
    model_config = ConfigDict(protected_namespaces=())
    # WebDisplaySetup attributes
    map_zoom: Literal["World", "Europe", "xEMEP"] = "World"
    regions_how: Literal["default", "aerocom", "htap", "country"] = "default"
    map_zoom: str = "World"
    add_model_maps: bool = False
    modelorder_from_config: bool = True
    obsorder_from_config: bool = True
    var_order_menu: tuple[str, ...] = ()
    obs_order_menu: tuple[str, ...] = ()
    model_order_menu: tuple[str, ...] = ()
    hide_charts: tuple[str, ...] = ()
    hide_pages: tuple[str, ...] = ()
    ts_annotations: dict[str, str] = Field(default_factory=dict)
    pages: tuple[str, ...] = ("maps", "evaluation", "intercomp", "overall", "infos")


class EvalRunOptions(BaseModel):
    clear_existing_json: bool = True
    only_json: bool = False
    only_colocation: bool = False
    #: If True, process only maps (skip obs evaluation)
    only_model_maps: bool = False
    obs_only: bool = False


class ProjectInfo(BaseModel):
    proj_id: str


class ExperimentInfo(BaseModel):
    exp_id: str
    exp_name: str = ""
    exp_descr: str = ""
    public: bool = False
    exp_pi: str = getuser()
    pyaerocom_version: str = __version__


class EvalSetup(BaseModel):
    """Composite class representing a whole analysis setup

    This represents the level at which json I/O happens for configuration
    setup files.
    """

    ###########################
    ##   Pydantic ConfigDict
    ###########################
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow", protected_namespaces=())

    ########################################
    ## Regular & BaseModel-based Attributes
    ########################################

    io_aux_file: Annotated[
        Path | str, ".py file containing additional read methods for modeldata"
    ] = ""

    var_web_info_file: Annotated[Path | str, "config file containing additional variables"] = ""

    var_scale_colmap_file: Annotated[
        Path | str, "config file containing scales/ranges for variables"
    ] = ""

    _aux_funs: dict = {}

    @computed_field
    @cached_property
    def proj_info(self) -> ProjectInfo:
        if not hasattr(self, "model_extra") or self.model_extra is None:
            return ProjectInfo()
        model_args = {
            key: val for key, val in self.model_extra.items() if key in ProjectInfo.model_fields
        }
        return ProjectInfo(**model_args)

    @computed_field
    @cached_property
    def exp_info(self) -> ExperimentInfo:
        model_args = {
            key: val for key, val in self.model_extra.items() if key in ExperimentInfo.model_fields
        }
        return ExperimentInfo(**model_args)

    @computed_field
    @cached_property
    def json_filename(self) -> str:
        """
        str: Savename of config file: cfg_<proj_id>_<exp_id>.json
        """
        return f"cfg_{self.proj_info.proj_id}_{self.exp_info.exp_id}.json"

    @cached_property
    def gridded_aux_funs(self) -> dict:
        if not bool(self._aux_funs) and os.path.exists(self.io_aux_file):
            self._import_aux_funs()
        return self._aux_funs

    @cached_property
    def var_web_info(self) -> VarWebInfo:
        return VarWebInfo(config_file=self.var_web_info_file)

    @cached_property
    def var_scale_colmap(self) -> VarWebScaleAndColormap:
        return VarWebScaleAndColormap(config_file=self.var_scale_colmap_file)

    @computed_field
    @cached_property
    def path_manager(self) -> OutputPaths:
        if not hasattr(self, "model_extra") or self.model_extra is None:
            return OutputPaths()
        model_args = {
            key: val for key, val in self.model_extra.items() if key in OutputPaths.model_fields
        }
        return OutputPaths(**model_args)

    # Many computed_fields here have this hack to get keys from a general CFG into their appropriate respective classes
    # TODO: all these computed fields could be more easily defined if the config were
    # rigid enough to have them explicitly defined (e.g., in a TOML file), rather than dumping everything
    # into one large config dict and then dishing out the relevant parts to each class.
    @computed_field
    @cached_property
    def time_cfg(self) -> TimeSetup:
        if not hasattr(self, "model_extra") or self.model_extra is None:
            return TimeSetup()
        model_args = {
            key: val for key, val in self.model_extra.items() if key in TimeSetup.model_fields
        }
        return TimeSetup(**model_args)

    @computed_field
    @cached_property
    def modelmaps_opts(self) -> ModelMapsSetup:
        if not hasattr(self, "model_extra") or self.model_extra is None:
            return ModelMapsSetup()
        model_args = {
            key: val for key, val in self.model_extra.items() if key in ModelMapsSetup.model_fields
        }
        return ModelMapsSetup(**model_args)

    @computed_field
    @cached_property
    def cams2_83_cfg(self) -> CAMS2_83Setup:
        if not hasattr(self, "model_extra"):
            return CAMS2_83Setup()
        model_args = {
            key: val for key, val in self.model_extra.items() if key in CAMS2_83Setup.model_fields
        }
        return CAMS2_83Setup(**model_args)

    @computed_field
    @cached_property
    def webdisp_opts(self) -> WebDisplaySetup:
        if not hasattr(self, "model_extra") or self.model_extra is None:
            return WebDisplaySetup()
        model_args = {
            key: val
            for key, val in self.model_extra.items()
            if key in WebDisplaySetup.model_fields
        }
        return WebDisplaySetup(**model_args)

    @computed_field
    @cached_property
    def processing_opts(self) -> EvalRunOptions:
        if not hasattr(self, "model_extra") or self.model_extra is None:
            return EvalRunOptions()
        model_args = {
            key: val for key, val in self.model_extra.items() if key in EvalRunOptions.model_fields
        }
        return EvalRunOptions(**model_args)

    @computed_field
    @cached_property
    def statistics_opts(self) -> StatisticsSetup:
        if not hasattr(self, "model_extra") or self.model_extra is None:
            return StatisticsSetup(weighted_stats=True, annual_stats_constrained=False)
        model_args = {
            key: val
            for key, val in self.model_extra.items()
            if key in StatisticsSetup.model_fields
        }
        return StatisticsSetup(**model_args)

    @computed_field
    @cached_property
    def colocation_opts(self) -> ColocationSetup:
        if not hasattr(self, "model_extra") or self.model_extra is None:
            return ColocationSetup(save_coldata=True, keep_data=False, resample_how="mean")

        model_args = {
            key: val
            for key, val in self.model_extra.items()
            if key in ColocationSetup.model_fields
        }
        # need to pass some default values to the ColocationSetup if not provided in config
        default_dict = {
            "save_coldata": True,
            "keep_data": False,
            "resample_how": "mean",
        }
        for key in default_dict:
            if key not in model_args:
                model_args[key] = default_dict[key]

        return ColocationSetup(**model_args)

    ##################################
    ## Non-BaseModel-based attributes
    ##################################

    # These attributes require special attention b/c they're not based on Pydantic's BaseModel class.

    obs_cfg: ObsCollection | dict = ObsCollection()

    @field_validator("obs_cfg")
    def validate_obs_cfg(cls, v):
        if isinstance(v, ObsCollection):
            return v
        return ObsCollection(v)

    @field_serializer("obs_cfg")
    def serialize_obs_cfg(self, obs_cfg: ObsCollection):
        return obs_cfg.json_repr()

    model_cfg: ModelCollection | dict = ModelCollection()

    @field_validator("model_cfg")
    def validate_model_cfg(cls, v):
        if isinstance(v, ModelCollection):
            return v
        return ModelCollection(v)

    @field_serializer("model_cfg")
    def serialize_model_cfg(self, model_cfg: ModelCollection):
        return model_cfg.json_repr()

    ###########################
    ##       Methods
    ###########################

    def get_obs_entry(self, obs_name) -> dict:
        return self.obs_cfg.get_entry(obs_name).to_dict()

    def get_model_entry(self, model_name) -> dict:
        """Get model entry configuration

        Since the configuration files for experiments are in json format, they
        do not allow the storage of executable custom methods for model data
        reading. Instead, these can be specified in a python module that may
        be specified via :attr:`add_methods_file` and that contains a
        dictionary `FUNS` that maps the method names with the callable methods.

        As a result, this means that, by default, custom read methods for
        individual models in :attr:`model_config` do not contain the
        callable methods but only the names. This method will take care of
        handling this and will return a dictionary where potential custom
        method strings have been converted to the corresponding callable
        methods.

        Parameters
        ----------
        model_name : str
            name of model

        Returns
        -------
        dict
            Dictionary that specifies the model setup ready for the analysis
        """
        cfg = self.model_cfg.get_entry(model_name)
        cfg = cfg.prep_dict_analysis(self.gridded_aux_funs)
        return cfg

    def to_json(self, outdir: str, ignore_nan: bool = True, indent: int = 3) -> None:
        """
        Save configuration as JSON file

        Parameters
        ----------
        outdir : str
            directory where the config json file is supposed to be stored
        ignore_nan : bool
            set NaNs to Null when writing
        indent : int
            json indentation

        """
        with aerovaldb.open(
            self.path_manager.json_basedir
            if self.path_manager.avdb_resource is None
            else self.path_manager.json_basedir
        ) as db:
            with db.lock():
                db.put_config(self.json_repr(), self.proj_info.proj_id, self.exp_info.exp_id)

    @staticmethod
    def from_json(filepath: str) -> Self:
        """Load configuration from json config file"""
        settings = read_json(filepath)
        return EvalSetup(**settings)

    def json_repr(self):
        return self.model_dump()

    def _import_aux_funs(self) -> None:
        h = ReadAuxHandler(self.io_aux_file)
        self._aux_funs.update(**h.import_all())

    def _check_time_config(self) -> None:
        periods = self.time_cfg.periods
        colstart = self.colocation_opts.start
        colstop = self.colocation_opts.stop

        if len(periods) == 0:
            if colstart is None:
                raise ConfigError("Either periods or start must be set...")
            per = self.colocation_opts._period_from_start_stop()
            periods = [per]
            logger.info(
                f"periods is not set, inferred {per} from start / stop colocation settings."
            )

        self.time_cfg.periods = _check_statistics_periods(periods)
        start, stop = _get_min_max_year_periods(periods)
        start_yr = start.year
        stop_yr = stop.year
        years = check_if_year(periods)
        if not years:
            if start == stop and isinstance(start, pd.Timestamp):
                stop = start + timedelta(hours=23)
            elif isinstance(start, pd.Timestamp):
                stop = stop + timedelta(hours=23)

            if stop_yr == start_yr:
                stop_yr += 1
            if colstart is None:
                self.colocation_opts.start = start.strftime("%Y/%m/%d %H:%M:%S")
            if colstop is None:
                self.colocation_opts.stop = stop.strftime(
                    "%Y/%m/%d %H:%M:%S"
                )  # + 1  # add 1 year since we want to include stop year
        else:
            if colstart is None:
                self.colocation_opts.start = start_yr
            if colstop is None:
                self.colocation_opts.stop = (
                    stop_yr + 1
                )  # add 1 year since we want to include stop year
