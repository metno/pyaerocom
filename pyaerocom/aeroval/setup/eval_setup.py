import logging
import os
import sys
from datetime import timedelta
from functools import cached_property
from pathlib import Path
from typing import Annotated

from pyaerocom.aeroval.glob_defaults import VarWebInfo, VarWebScaleAndColormap
from pyaerocom.aeroval.obsentry import ObsEntry

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

import subprocess

import aerovaldb
import pandas as pd
from pydantic import (
    BaseModel,
    ConfigDict,
    computed_field,
    field_serializer,
    model_validator,
)

from pyaerocom.aeroval.aux_io_helpers import ReadAuxHandler
from pyaerocom.aeroval.collections import ModelCollection, ObsCollection
from pyaerocom.aeroval.exceptions import ConfigError
from pyaerocom.aeroval.helpers import (
    _check_statistics_periods,
    _get_min_max_year_periods,
    check_if_year,
)
from pyaerocom.aeroval.json_utils import read_json
from pyaerocom.colocation.colocation_setup import ColocationSetup

from .output_paths import OutputPaths
from .model_maps_setup import ModelMapsSetup
from .statistics_setup import StatisticsSetup
from .time_setup import TimeSetup
from .web_display_setup import WebDisplaySetup
from .eval_run_options import EvalRunOptions
from .project_info import ProjectInfo
from .experiment_info import ExperimentInfo
from .cams2_83_setup import CAMS2_83Setup

logger = logging.getLogger(__name__)


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

    @model_validator(mode="after")
    def model_validator(self) -> Self:
        # Add missing variables to var_order_menu.
        var_order_menu = set(self.webdisp_opts.var_order_menu)
        obs_cfg = self.obs_cfg

        variables = set()
        for entry in obs_cfg:
            for var in entry.obs_vars:
                variables.add(var)

        if not var_order_menu.issuperset(variables):
            missing_vars = sorted(variables - var_order_menu)
            ls = list(self.webdisp_opts.var_order_menu)
            ls.extend(missing_vars)
            self.webdisp_opts.var_order_menu = tuple(ls)
            logger.info(
                f"Some variables are configured as obsvars but not included in var_order_menu. They have been appended to var_order_menu. Missing variables: {', '.join(missing_vars)}."
            )

        return self

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

    @computed_field
    @cached_property
    def obs_cfg(self) -> ObsCollection:
        oc = ObsCollection()
        for k, v in self.model_extra.get("obs_cfg", {}).items():
            oc.add_entry(k, v)
        return oc

    @field_serializer("obs_cfg")
    def serialize_obs_cfg(self, obs_cfg: ObsCollection):
        return obs_cfg.as_dict()

    @computed_field
    @cached_property
    def model_cfg(self) -> ModelCollection:
        mc = ModelCollection()
        for k, v in self.model_extra.get("model_cfg", {}).items():
            mc.add_entry(k, v)
        return mc

    @field_serializer("model_cfg")
    def serialize_model_cfg(self, model_cfg: ModelCollection):
        return model_cfg.as_dict()

    @computed_field
    @cached_property
    def pip_freeze(self) -> list[str]:
        reqs = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
        splt = [x for x in reqs.decode().split("\n") if x != ""]

        return sorted(splt)

    ###########################
    ##       Methods
    ###########################

    def get_obs_entry(self, obs_name) -> ObsEntry:
        """Returns ObsEntry instance for network obs_name"""
        return self.obs_cfg.get_entry(obs_name)

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
