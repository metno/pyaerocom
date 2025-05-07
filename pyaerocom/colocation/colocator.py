"""
Classes and methods to perform high-level colocation.
"""

import glob
import logging
import os
import traceback
import warnings
from collections import defaultdict
from typing import Any

import pandas as pd

from pyaerocom import const
from pyaerocom.colocation.colocation_utils import (
    colocate_gridded_gridded,
    colocate_gridded_ungridded,
    correct_model_stp_coldata,
)
from pyaerocom.exceptions import (
    ColocationError,
    ColocationSetupError,
    DataCoverageError,
)
from pyaerocom.griddeddata import GriddedData
from pyaerocom.helpers import start_stop, to_datestring_YYYYMMDD
from pyaerocom.io import ReadCAMS2_83, ReadGridded, ReadUngridded
from pyaerocom.io.helpers import get_all_supported_ids_ungridded
from pyaerocom.io.mscw_ctm.reader import ReadMscwCtm
from pyaerocom.stats.mda8.const import MDA8_INPUT_VARS
from pyaerocom.stats.mda8.mda8 import mda8_colocated_data
from pyaerocom.ungridded_data_container import UngriddedDataContainer
from pyaerocom.units import Unit
from pyaerocom.units.datetime import get_lowest_resolution, to_pandas_timestamp

from .colocated_data import ColocatedData
from .colocation_3d import ColocatedDataLists, colocate_vertical_profile_gridded
from .colocation_setup import ColocationSetup

logger = logging.getLogger(__name__)


class Colocator:
    """High level class for running co-location

    Note
    ----
    This object requires and instance from :class:`ColocationSetup`.
    """

    SUPPORTED_GRIDDED_READERS: dict = {
        "ReadGridded": ReadGridded,
        "ReadMscwCtm": ReadMscwCtm,
        "ReadCAMS2_83": ReadCAMS2_83,
    }

    MODELS_WITH_KWARGS = [ReadMscwCtm]

    STATUS_CODES: dict[int, str] = {
        1: "SUCCESS",
        2: "NOT OK: Missing/invalid model variable",
        3: "NOT OK: Missing/invalid obs variable",
        4: "NOT OK: Failed to read model variable",
        5: "NOT OK: Colocation failed",
    }

    def __init__(self, colocation_setup: ColocationSetup | dict, **kwargs):
        if not colocation_setup:
            raise ValueError(
                "An instance ColocationSetup or a dict must be provided to Colocator."
            )
        if not isinstance(colocation_setup, ColocationSetup):
            colocation_setup = ColocationSetup(**colocation_setup)
            warnings.warn(
                DeprecationWarning(
                    "Future versions of Pyaerocom will require Colocator to ingest an instance of ColocationSetup."
                )
            )

        self.colocation_setup = colocation_setup
        self.logging: bool = True
        self._loaded_model_data: dict | None = {}
        self.data: dict = {}

        self._processing_status: list[str] = []
        self.files_written: list[str] = []

        self._model_reader: ReadGridded | ReadMscwCtm | ReadCAMS2_83 | None = None
        self._obs_reader: Any | None = None
        self._obs_is_vertical_profile: bool = False
        self.obs_filters: dict = colocation_setup.obs_filters.copy()

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
        ovars = self.colocation_setup.obs_vars
        model_vars = []
        for ovar in ovars:
            if ovar in self.colocation_setup.model_add_vars:
                model_vars.append(self.colocation_setup.model_add_vars[ovar])
            else:
                model_vars.append(ovar)

        for ovar, mvars in self.colocation_setup.model_add_vars.items():
            if ovar not in ovars:
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
        if self.colocation_setup.pyaro_config is not None:
            return True

        return True if self.colocation_setup.obs_id in get_all_supported_ids_ungridded() else False

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
            if self._model_reader.data_id == self.colocation_setup.model_id:
                return self._model_reader
            logger.info(
                f"Reloading outdated model reader. ID of current reader: "
                f"{self._model_reader.data_id}. New ID: {self.colocation_setup.model_id}"
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
        elif self.obs_is_ungridded and self.colocation_setup.obs_id in reader.data_ids:
            return True
        elif self.colocation_setup.obs_id == reader.data_id:
            return True

    @property
    def obs_reader(self):
        """
        Observation data reader
        """

        if not self._check_data_id_obs_reader():
            if self.obs_is_ungridded:
                self._obs_reader = ReadUngridded(
                    data_ids=[self.colocation_setup.obs_id],
                    data_dirs=self.colocation_setup.obs_data_dir,
                    configs=[
                        self.colocation_setup.pyaro_config,
                    ],
                )
            else:
                self._obs_reader = self._instantiate_gridded_reader(what="obs")
        return self._obs_reader

    @property
    def output_dir(self):
        """
        str: Output directory for colocated data NetCDF files
        """
        loc = os.path.join(self.colocation_setup.basedir_coldata, self.get_model_name())
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
        if self.colocation_setup.model_name is None:
            if self.colocation_setup.model_id is None:
                raise AttributeError(
                    "Neither model_name nor model_id are set. These must be set in ColocationSetup."
                )
            return self.colocation_setup.model_id
        return self.colocation_setup.model_name

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
        if self.colocation_setup.obs_name is None:
            if self.colocation_setup.obs_id is None:
                raise AttributeError("Neither obs_name nor obs_id are set")
            return self.colocation_setup.obs_id
        return self.colocation_setup.obs_name

    def get_model_data(self, model_var: str):
        if model_var in self._loaded_model_data:
            mdata = self._loaded_model_data[model_var]
            if mdata.data_id == self.colocation_setup.model_id:
                return mdata
        self._check_add_model_read_aux(model_var)
        mdata = self._read_gridded(var_name=model_var, is_model=True)
        self._loaded_model_data[model_var] = mdata
        return mdata

    def get_obs_data(self, obs_var: str):
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

    def prepare_run(self, var_list: list[str] | None = None) -> dict:
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

        if isinstance(self.colocation_setup.obs_vars, str):
            self.colocation_setup.obs_vars = (self.colocation_setup.obs_vars,)

        self._check_obs_vars_available()
        self._check_obs_filters()
        self._check_model_add_vars()
        self._check_set_start_stop()

        vars_to_process = self._find_var_matches()
        if var_list is not None:
            vars_to_process = self._filter_var_matches_varlist(vars_to_process, var_list)

        (vars_to_process, ts_types) = self._check_load_model_data(vars_to_process)

        if self.colocation_setup.save_coldata and not self.colocation_setup.reanalyse_existing:
            vars_to_process = self._filter_var_matches_files_not_exist(vars_to_process, ts_types)
        return vars_to_process

    def run(self, var_list: list[str] | None = None):
        """Perform colocation for current setup

        See also :func:`prepare_run`.

        Parameters
        ----------
        var_list : list, optional
            list of variables supposed to be analysed. The default is None,
            in which case all defined variables are attempted to be colocated.

        Returns
        -------
        dict
            nested dictionary, where keys are model variables, values are
            dictionaries comprising key / value pairs of obs variables and
            associated instances of :class:`ColocatedData`.
        """
        # MDA8 is a daily value so it doesn't make sense to calculate it if
        # no frequency is daily or coarser.
        calc_mda8 = False
        if self.colocation_setup.main_freq in ["daily", "monthly", "yearly"]:
            calc_mda8 = True
        if any(x in ["daily", "monthly", "yearly"] for x in self.colocation_setup.freqs):
            calc_mda8 = True

        data_out = defaultdict(lambda: dict())
        # TODO: see if the following could be solved via custom context manager
        try:
            vars_to_process = self.prepare_run(var_list)
        except Exception as ex:
            logger.exception(ex)
            if self.colocation_setup.raise_exceptions:
                self._print_processing_status()
                logger.critical(f"ABORTED: raise_exceptions is True: {traceback.format_exc()}\n")
                raise ex
            vars_to_process = {}
        self._print_coloc_info(vars_to_process)
        for mod_var, obs_var in vars_to_process.items():
            try:
                coldata = self._run_helper(
                    mod_var, obs_var
                )  # note this can be ColocatedData or ColocatedDataLists
                data_out[mod_var][obs_var] = coldata

                if calc_mda8 and (obs_var in MDA8_INPUT_VARS):
                    try:
                        mda8 = mda8_colocated_data(
                            coldata, obs_var=f"{obs_var}mda8", mod_var=f"{mod_var}mda8"
                        )
                    except ValueError as e:
                        logger.debug(e)
                    else:
                        self._save_coldata(mda8)
                        logger.info(
                            "Successfully calculated mda8 for [%s, %s].",
                            obs_var,
                            mod_var,
                        )
                        data_out[f"{mod_var}mda8"][f"{obs_var}mda8"] = mda8

                self._processing_status.append([mod_var, obs_var, 1])
            except Exception:
                msg = f"Failed to perform analysis: {traceback.format_exc()}\n"
                logger.warning(msg)
                self._processing_status.append([mod_var, obs_var, 5])
                if self.colocation_setup.raise_exceptions:
                    self._print_processing_status()
                    logger.critical("ABORTED: raise_exceptions is True\n")

                    raise ColocationError(traceback.format_exc())
        logger.info("Colocation finished")

        self._print_processing_status()
        if self.colocation_setup.keep_data:
            self.data = data_out
        return dict(data_out)

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
        obs_vars = self.colocation_setup.obs_vars
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
            data_ids=[self.colocation_setup.obs_id],
            vars_to_retrieve=var_name,
            only_cached=self.colocation_setup.obs_cache_only,
            filter_post=obs_filters_post,
            **self.colocation_setup.read_opts_ungridded,
        )
        obs_data.check_unit(var_name)

        if self.colocation_setup.obs_remove_outliers:
            oor = self.colocation_setup.obs_outlier_ranges
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
        obs_vars = self.colocation_setup.obs_vars
        if any([x in self.colocation_setup.obs_filters for x in obs_vars]):
            # variable specific obs_filters
            for ovar in obs_vars:
                if ovar not in self.colocation_setup.obs_filters:
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
                msg = f"Failed to load model data: {self.colocation_setup.model_id} ({mvar}). Reason {e}"
                logger.warning(msg)
                self._processing_status.append([mvar, ovar, 4])
                if self.colocation_setup.raise_exceptions:
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
        for ovar, mvars in self.colocation_setup.model_add_vars.items():
            if not isinstance(mvars, list | tuple):
                raise ValueError("Values of model_add_vars need to be list or tuple")
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
            data_id = self.colocation_setup.model_id
            data_dir = self.colocation_setup.model_data_dir
        else:
            data_id = self.colocation_setup.obs_id
            data_dir = self.colocation_setup.obs_data_dir
        reader_class = self._get_gridded_reader_class(what=what)
        if what == "model" and reader_class in self.MODELS_WITH_KWARGS:
            reader = reader_class(
                data_id=data_id, data_dir=data_dir, **self.colocation_setup.model_kwargs
            )
        else:
            reader = reader_class(data_id=data_id, data_dir=data_dir)
        return reader

    def _get_gridded_reader_class(self, what):
        """Returns the class of the reader for gridded data."""
        try:
            reader = self.SUPPORTED_GRIDDED_READERS[self.colocation_setup.gridded_reader_id[what]]
        except KeyError as e:
            raise NotImplementedError(
                f"Reader {self.colocation_setup.gridded_reader_id[what]} is not supported: {e}"
            )
        return reader

    def _check_add_model_read_aux(self, model_var):
        if model_var not in self.colocation_setup.model_read_aux:
            return False
        info = self.colocation_setup.model_read_aux[model_var]
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
        if not len(self.colocation_setup.obs_vars) > 0:
            raise ColocationSetupError("no observation variables specified...")
        oreader = self.obs_reader
        if self.obs_is_ungridded:
            avail = oreader.get_vars_supported(
                self.colocation_setup.obs_id, self.colocation_setup.obs_vars
            )
        else:
            avail = []
            for ovar in self.colocation_setup.obs_vars:
                if oreader.has_var(ovar):
                    avail.append(ovar)

        if len(self.colocation_setup.obs_vars) > len(avail):
            for ovar in self.colocation_setup.obs_vars:
                if ovar not in avail:
                    logger.warning(
                        f"Obs variable {ovar} is not available in {self.colocation_setup.obs_id} "
                        f"and will be ignored"
                    )
                    self._processing_status.append([None, ovar, 3])

            if self.colocation_setup.raise_exceptions:
                invalid = [var for var in self.colocation_setup.obs_vars if var not in avail]
                invalid = "; ".join(invalid)
                raise DataCoverageError(
                    f"Invalid obs var(s) for {self.colocation_setup.obs_id}: {invalid}"
                )

            self.obs_vars = avail

    def _print_processing_status(self):
        mname = self.get_model_name()
        oname = self.get_obs_name()
        logger.info(f"Colocation processing status for {mname} vs. {oname}")
        logger.info(self.processing_status)

    def _filter_var_matches_var_name(self, var_matches, var_name):
        filtered = {}
        for mvar, ovar in var_matches.items():
            if mvar == var_name or ovar == var_name:
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
        muv = self.colocation_setup.model_use_vars
        modreader = self.model_reader
        for ovar in self.colocation_setup.obs_vars:
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

            if ovar in self.colocation_setup.model_add_vars:  # observation variable
                addvars = self.colocation_setup.model_add_vars[ovar]
                for addvar in addvars:
                    self._check_add_model_read_aux(addvar)
                    if modreader.has_var(addvar):
                        var_matches[addvar] = ovar
                    else:
                        self._processing_status.append([addvar, ovar, 2])
                        all_ok = False

        if not all_ok and self.colocation_setup.raise_exceptions:
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
        tst = self.colocation_setup.ts_type  # default
        if is_model and self.colocation_setup.model_ts_type_read is not None:
            tst = self.colocation_setup.model_ts_type_read
            if tst == "":
                tst = self.colocation_setup.ts_type
        elif not is_model and self.colocation_setup.obs_ts_type_read is not None:
            tst = self.obs_ts_type_read
        if isinstance(tst, dict):
            if var_name in tst:
                tst = tst[var_name]
            else:
                tst = self.colocation_setup.ts_type
        return tst

    def _read_gridded(self, var_name, is_model):
        start, stop = self.colocation_setup.start, self.colocation_setup.stop
        ts_type_read = self._get_ts_type_read(var_name, is_model)
        kwargs = {}
        if is_model:
            reader = self.model_reader
            vert_which = self.colocation_setup.obs_vert_type

            kwargs.update(**self.colocation_setup.model_kwargs)
            if self.colocation_setup.model_use_climatology:
                # overwrite start and stop to read climatology file for model
                start, stop = 9999, None
            if var_name in self.colocation_setup.model_read_opts:
                kwargs.update(self.colocation_setup.model_read_opts[var_name])
        else:
            reader = self.obs_reader
            vert_which = None
            ts_type_read = self.colocation_setup.obs_ts_type_read
            kwargs.update(self._eval_obs_filters(var_name))

        try:
            data = reader.read_var(
                var_name,
                start=start,
                stop=stop,
                ts_type=ts_type_read,
                vert_which=vert_which,
                flex_ts_type=self.colocation_setup.flex_ts_type,
                **kwargs,
            )
        except DataCoverageError:
            vert_which_alt = self._try_get_vert_which_alt(is_model, var_name)
            data = reader.read_var(
                var_name,
                start=start,
                stop=stop,
                ts_type=ts_type_read,
                flex_ts_type=self.colocation_setup.flex_ts_type,
                vert_which=vert_which_alt,
            )

        data = self._check_remove_outliers_gridded(data, var_name, is_model)
        return data

    def _try_get_vert_which_alt(self, is_model, var_name):
        if is_model:
            if self.colocation_setup.obs_vert_type in self.colocation_setup.OBS_VERT_TYPES_ALT:
                return self.colocation_setup.OBS_VERT_TYPES_ALT[
                    self.colocation_setup.obs_vert_type
                ]
        raise DataCoverageError(f"No alternative vert type found for {var_name}")

    def _check_remove_outliers_gridded(self, data: GriddedData, var_name: str, is_model: bool):
        if is_model:
            rm_outliers = self.colocation_setup.model_remove_outliers
            outlier_ranges = self.colocation_setup.model_outlier_ranges
        else:
            rm_outliers = self.colocation_setup.obs_remove_outliers
            outlier_ranges = self.colocation_setup.obs_outlier_ranges

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

    def _eval_obs_filters(self, var_name: str):
        obs_filters = self.obs_filters
        if var_name in obs_filters:
            # return obs_filters[var_name]
            obs_filters = obs_filters[var_name]
        if not isinstance(obs_filters, dict):
            raise AttributeError(
                f"Detected obs_filters attribute in Colocator class, "
                f"which is not a dictionary: {obs_filters}"
            )
        return obs_filters if len(obs_filters) > 0 else {}

    def _save_coldata(self, coldata: ColocatedData):
        """Helper for saving colocateddata"""
        obs_var, mod_var = coldata.metadata["var_name_input"]
        if mod_var in self.colocation_setup.model_rename_vars:
            mvar = self.colocation_setup.model_rename_vars[mod_var]
            logger.info(
                f"Renaming model variable from {mod_var} to {mvar} in "
                f"ColocatedData before saving to NetCDF."
            )
            coldata.rename_variable(mod_var, mvar, self.colocation_setup.model_id)
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
                vertical_layer = coldata.vertical_layer

            savename = self._coldata_savename(
                obs_var, mvar, coldata.ts_type, vertical_layer=vertical_layer
            )

        else:
            savename = self._coldata_savename(obs_var, mvar, coldata.ts_type)
        fp = coldata.to_netcdf(self.output_dir, savename=savename)
        self.files_written.append(fp)
        msg = f"WRITE: {fp}\n"
        logger.info(msg)

    def _eval_resample_how(self, model_var: str, obs_var: str):
        rshow = self.colocation_setup.resample_how
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
        if self.colocation_setup.model_use_climatology:
            if 9999 not in yrs_avail:
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
        if self.colocation_setup.start is None:
            self._infer_start_stop_yr_from_model_reader()
            start, stop = self.start, self.stop
        else:
            start, stop = self.colocation_setup.start, self.colocation_setup.stop
        if self.colocation_setup.model_use_climatology:
            if self.colocation_setup.stop is not None or not isinstance(
                self.colocation_setup.start, int
            ):
                raise ColocationSetupError(
                    "Conflict: only single year analyses are support for model "
                    'climatology fields, please specify "start" as integer '
                    'denoting the year, and set "stop"=None'
                )
        self.start, self.stop = start_stop(start, stop)

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
            filter_name=self.colocation_setup.filter_name,
            vertical_layer=vertical_layer,
        )
        return f"{name}.nc"

    def _get_colocation_ts_type(self, model_ts_type, obs_ts_type=None):
        chk = [self.colocation_setup.ts_type, model_ts_type]
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

        if self.colocation_setup.model_use_climatology:
            baseyr = self.start.year
        else:
            baseyr = None
        # input args shared between all colocation functions
        args = dict(
            data=model_data,
            data_ref=obs_data,
            start=self.start,
            stop=self.stop,
            filter_name=self.colocation_setup.filter_name,
            regrid_res_deg=self.colocation_setup.regrid_res_deg,
            harmonise_units=self.colocation_setup.harmonise_units,
            update_baseyear_gridded=baseyr,
            min_num_obs=self.colocation_setup.min_num_obs,
            colocate_time=self.colocation_setup.colocate_time,
            resample_how=rshow,
            add_meta_keys=[],
        )
        # check if the station_type key has been passed to the ungridded data object
        # (not all readers may do that, currently only the CAMS2_83 reader does)
        if isinstance(obs_data, UngriddedDataContainer):
            are_there_station_types = {
                "station_type" in dict for dict in obs_data.metadata.values()
            }
            if are_there_station_types == {True, False}:
                raise ValueError("some stations have `station_type` metadata while others do not")
            if are_there_station_types == {True}:  # all have station_type
                args.update(add_meta_keys=["station_type"])

        if self.obs_is_ungridded:
            ts_type = self._get_colocation_ts_type(model_data.ts_type)
            args.update(
                ts_type=ts_type,
                var_ref=obs_var,
                use_climatology_ref=self.colocation_setup.obs_use_climatology,
            )
        else:
            ts_type = self._get_colocation_ts_type(model_data.ts_type, obs_data.ts_type)
            args.update(ts_type=ts_type)
        if self.obs_is_vertical_profile:
            args.update(
                colocation_layer_limits=self.colocation_setup.colocation_layer_limits,
                profile_layer_limits=self.colocation_setup.profile_layer_limits,
            )
        return args

    def _check_dimensionality(self, args):
        mdata = args["data"]
        odata = args["data_ref"]
        from pyaerocom.exceptions import DataDimensionError
        from pyaerocom.griddeddata import GriddedData

        if mdata.ndim == 4 and self.colocation_setup.obs_vert_type == "Surface":
            mdata = mdata.extract_surface_level()
            args["data"] = mdata

        if isinstance(odata, GriddedData):
            if odata.ndim == 4 and self.colocation_setup.obs_vert_type == "Surface":
                odata = odata.extract_surface_level()
                args["data_ref"] = odata
            elif odata.ndim > 3:
                raise DataDimensionError(
                    f"cannot co-locate model data with more than 3 dimensions: {odata}"
                )
        return args

    def _run_helper(self, model_var: str, obs_var: str):
        logger.info(
            f"Running {self.colocation_setup.model_id} ({model_var}) vs. {self.colocation_setup.obs_id} ({obs_var})"
        )
        args = self._prepare_colocation_args(model_var, obs_var)
        args = self._check_dimensionality(args)
        coldata = self._colocation_func(**args)

        if isinstance(coldata, ColocatedData):
            coldata.data.attrs["model_name"] = self.get_model_name()
            coldata.data.attrs["obs_name"] = self.get_obs_name()
            coldata.data.attrs["vert_code"] = self.colocation_setup.obs_vert_type

            coldata.data.attrs.update(**self.colocation_setup.add_meta)

            if self.colocation_setup.zeros_to_nan:
                coldata = coldata.set_zeros_nan()
            if self.colocation_setup.model_to_stp:
                coldata = correct_model_stp_coldata(coldata)
            if self.colocation_setup.save_coldata:
                self._save_coldata(coldata)

        elif isinstance(coldata, ColocatedDataLists):  # look into intertools chain.from_iterable
            for i_list in coldata:
                for coldata_obj in i_list:
                    coldata_obj.data.attrs["model_name"] = self.get_model_name()
                    coldata_obj.data.attrs["obs_name"] = self.get_obs_name()
                    coldata_obj.data.attrs["vert_code"] = self.colocation_setup.obs_vert_type
                    coldata_obj.data.attrs.update(**self.colocation_setup.add_meta)
                    if self.colocation_setup.zeros_to_nan:
                        coldata_obj = coldata_obj.set_zeros_nan()
                    if self.colocation_setup.model_to_stp:  # TODO: check is this needs modifying
                        coldata = correct_model_stp_coldata(coldata_obj)
                    if self.colocation_setup.save_coldata:
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
        key_vals = []
        for key, val in var_matches.items():
            key_vals.append(f"{key}\t{val}")
        logger.info(
            "The following variable combinations will be colocated\nMODEL-VAR\tOBS-VAR\n"
            + "\n".join(key_vals)
        )
