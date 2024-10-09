import glob
import logging
import os
import pathlib
import shutil
from collections import namedtuple

import aerovaldb

from pyaerocom import const
from pyaerocom._lowlevel_helpers import (
    DirLoc,
    StrType,
    TypeValidator,
    sort_dict_by_name,
)
from pyaerocom.aeroval.collections import ObsCollection
from pyaerocom.aeroval.glob_defaults import (
    VariableInfo,
    extended_statistics,
    statistics_defaults,
    statistics_mean_trend,
    statistics_median_trend,
    statistics_model_only,
    statistics_obs_only,
    statistics_trend,
)
from pyaerocom.aeroval.json_utils import round_floats
from pyaerocom.aeroval.modelentry import ModelEntry
from pyaerocom.aeroval import EvalSetup
from pyaerocom.aeroval.varinfo_web import VarinfoWeb
from pyaerocom.colocation.colocated_data import ColocatedData
from pyaerocom.exceptions import EntryNotAvailable, VariableDefinitionError
from pyaerocom.stats.mda8.const import MDA8_OUTPUT_VARS
from pyaerocom.stats.stats import _init_stats_dummy
from pyaerocom.utils import recursive_defaultdict
from pyaerocom.variable_helpers import get_aliases, get_variable

MapInfo = namedtuple(
    "MapInfo",
    ["obs_network", "obs_var", "vert_code", "mod_name", "mod_var", "time_period"],
)

logger = logging.getLogger(__name__)


class ProjectOutput:
    """JSON output for project"""

    proj_id = StrType()

    json_basedir = DirLoc(assert_exists=True)

    def __init__(self, proj_id: str, resource: str | pathlib.Path | aerovaldb.AerovalDB):
        self.proj_id = proj_id

        if isinstance(resource, pathlib.Path):
            resource = str(resource)

        if isinstance(resource, str):
            self.avdb = aerovaldb.open(resource)
        elif isinstance(resource, aerovaldb.AerovalDB):
            self.avdb = resource
        else:
            raise ValueError(f"Expected string or AerovalDB, got {type(resource)}.")

        # TODO: Only works for json_files, check if this is needed, and remove / rewrite
        # functionality that requires direct knowledge of _basedir.
        self.json_basedir = self.avdb._basedir

    @property
    def proj_dir(self) -> str:
        """Project directory"""
        fp = os.path.join(self.json_basedir, self.proj_id)
        if not os.path.exists(fp):
            os.mkdir(fp)
            logger.info(f"Creating AeroVal project directory at {fp}")
        return fp

    @property
    def experiments_file(self) -> str:
        """json file containing region specifications"""
        fp = os.path.join(self.proj_dir, "experiments.json")
        return fp

    @property
    def available_experiments(self) -> list:
        """
        List of available experiments
        """
        return list(self.avdb.get_experiments(self.proj_id, default={}))


class ExperimentOutput(ProjectOutput):
    """JSON output for experiment"""

    cfg = TypeValidator(EvalSetup)

    def __init__(self, cfg: EvalSetup):
        self.cfg = cfg
        super().__init__(
            cfg.proj_id,
            (
                cfg.path_manager.json_basedir
                if cfg.path_manager.avdb_resource is None
                else cfg.path_manager.json_basedir
            ),
        )

        # dictionary that will be filled by json cleanup methods to check for
        # invalid or outdated json files across different output directories
        self._invalid = dict(models=[], obs=[])

    @property
    def exp_id(self) -> str:
        """Experiment ID"""
        return self.cfg.exp_id

    @property
    def exp_dir(self) -> str:
        """Experiment directory"""
        fp = os.path.join(self.proj_dir, self.exp_id)
        if not os.path.exists(fp):
            os.mkdir(fp)
            logger.info(f"Creating AeroVal experiment directory at {fp}")
        return fp

    @property
    def regions_file(self) -> str:
        """json file containing region specifications"""
        fp = os.path.join(self.exp_dir, "regions.json")
        return fp

    @property
    def statistics_file(self) -> str:
        """json file containing region specifications"""
        fp = os.path.join(self.exp_dir, "statistics.json")
        return fp

    @property
    def var_ranges_file(self) -> str:
        """json file containing region specifications"""
        fp = os.path.join(self.exp_dir, "ranges.json")
        return fp

    @property
    def menu_file(self) -> str:
        """json file containing region specifications"""
        fp = os.path.join(self.exp_dir, "menu.json")
        return fp

    @property
    def results_available(self) -> bool:
        """
        bool: True if results are available for this experiment, else False
        """
        if self.exp_id not in os.listdir(self.proj_dir):
            return False
        elif not len(self._get_json_output_files("map")) > 0:
            return False
        return True

    @property
    def out_dirs_json(self) -> dict:
        """
        json output directories (`dict`)
        """
        return self.cfg.path_manager.get_json_output_dirs()

    def update_menu(self) -> None:
        """Update menu

        The menu.json file is created based on the available json map files in the
        map directory of an experiment.

        Parameters
        ----------
        menu_file : str
            path to json menu file
        delete_mode : bool
            if True, then no attempts are being made to find json files for the
            experiment specified in `config`.

        """
        avail = self._create_menu_dict()
        avail = self._sort_menu_entries(avail)
        with self.avdb.lock():
            self.avdb.put_menu(avail, self.proj_id, self.exp_id)

    def update_interface(self) -> None:
        """
        Update web interface

        Steps:

        1. Check if results are available, and if so:
        2. Add entry for this experiment in experiments.json
        3. Create/update ranges.json file in experiment directory
        4. Update menu.json against available output and evaluation setup
        5. Synchronise content of heatmap json files with menu
        6. Create/update file statistics.json in experiment directory
        7. Copy json version of EvalSetup into experiment directory

        Returns
        -------
        None

        """
        if not self.results_available:
            logger.warning(f"no output available for experiment {self.exp_id} in {self.proj_id}")
            return
        exp_data = {"public": self.cfg.exp_info.public}
        self._add_entry_experiments_json(self.exp_id, exp_data)
        self._create_var_ranges_json()
        self.update_menu()
        self._sync_heatmaps_with_menu_and_regions()

        self._create_statistics_json()
        # AeroVal frontend needs periods to be set in config json file...
        # make sure they are
        self.cfg._check_time_config()
        with self.avdb.lock():
            self.avdb.put_config(self.cfg.json_repr(), self.proj_id, self.exp_id)

    def _sync_heatmaps_with_menu_and_regions(self) -> None:
        """
        Synchronise content of heatmap json files with content of menu.json
        """
        with self.avdb.lock():
            menu = self.avdb.get_menu(self.proj_id, self.exp_id, default={})
            all_regions = self.avdb.get_regions(self.proj_id, self.exp_id, default={})
            for uri in self.avdb.list_glob_stats(
                self.proj_id, self.exp_id, access_type=aerovaldb.AccessType.URI
            ):
                data = self.avdb.get_by_uri(uri)
                hm = {}
                for vardisp, info in menu.items():
                    obs_dict = info["obs"]
                    if vardisp not in hm:
                        hm[vardisp] = {}
                    for obs, vdict in obs_dict.items():
                        if obs not in hm[vardisp]:
                            hm[vardisp][obs] = {}
                        for vert_code, mdict in vdict.items():
                            if vert_code not in hm[vardisp][obs]:
                                hm[vardisp][obs][vert_code] = {}
                            for mod, minfo in mdict.items():
                                if mod not in hm[vardisp][obs][vert_code]:
                                    hm[vardisp][obs][vert_code][mod] = {}
                                modvar = minfo["model_var"]
                                hm_data = data[vardisp][obs][vert_code][mod][modvar]
                                hm_data = self._check_hm_all_regions_avail(all_regions, hm_data)
                                hm[vardisp][obs][vert_code][mod][modvar] = hm_data

                self.avdb.put_by_uri(hm, uri)

    def _check_hm_all_regions_avail(self, all_regions, hm_data) -> dict:
        if all([x in hm_data for x in all_regions]):
            return hm_data
        # some regions are not available in this subset
        periods = self.cfg.time_cfg._get_all_period_strings()
        dummy_stats = _init_stats_dummy()
        for region in all_regions:
            if region not in hm_data:
                hm_data[region] = {}
                for per in periods:
                    hm_data[region][per] = dummy_stats
        return hm_data

    @staticmethod
    def _info_from_map_file(filename: str) -> MapInfo:
        """
        Separate map filename into meta info on obs and model content

        Parameters
        ----------
        filename : str
            name of file in "map" subdirectory of json output directory for
            this experiment

        Raises
        ------
        ValueError
            if input filename is invalid

        Returns
        -------
        str
            name of observation network
        str
            name of observation variable
        str
            name of vertical code (e.g. Surface)
        str
            name of model
        str
            name of model variable
        str
            Time period
        """
        spl = os.path.basename(filename).split(".json")[0].split("_")
        if len(spl) != 4:
            raise ValueError(
                f"invalid map filename: {filename}. Must "
                f"contain exactly 3 underscores _ to separate "
                f"obsinfo, vertical, model info, and periods"
            )
        obsinfo = spl[0]
        vert_code = spl[1]
        modinfo = spl[2]
        time_period = spl[3]

        mspl = modinfo.split("-")
        mod_var = mspl[-1]
        mod_id = "-".join(mspl[:-1])

        ospl = obsinfo.split("-")
        obs_var = ospl[-1]
        obs_network = "-".join(ospl[:-1])

        return MapInfo(obs_network, obs_var, vert_code, mod_id, mod_var, time_period)

    def _results_summary(self) -> dict[str, list[str]]:
        res = [[], [], [], [], [], []]
        files = self._get_json_output_files("map")
        for file in files:
            map_info = self._info_from_map_file(file)
            for i, entry in enumerate(map_info):
                res[i].append(entry)
        output = {}
        for i, name in enumerate(["obs", "ovar", "vc", "mod", "mvar", "per"]):
            output[name] = list(set(res[i]))
        return output

    def clean_json_files(self) -> list[str]:
        """Checks all existing json files and removes outdated data

        This may be relevant when updating a model name or similar.

        Returns:
        list[str] :
            The list of file paths that where modified / removed.
        """
        modified = []
        logger.info(
            "Running clean_json_files: Checking json output directories for "
            "outdated or invalid data and cleaning up."
        )
        outdirs = self.out_dirs_json
        mapfiles = self._get_json_output_files("map")
        rmmap = []
        vert_codes = self.cfg.obs_cfg.all_vert_types
        for file_path in mapfiles:
            try:
                (
                    obs_network,
                    obs_var,
                    vert_code,
                    mod_name,
                    mod_var,
                    time_period,
                ) = self._info_from_map_file(file_path)
            except Exception as e:
                logger.warning(
                    f"FATAL: invalid file convention for map json file:"
                    f" {file_path}. This file will be deleted. Error message: "
                    f"{repr(e)}"
                )
                rmmap.append(file_path)
                continue
            if not self._is_part_of_experiment(obs_network, obs_var, mod_name, mod_var):
                rmmap.append(file_path)
            elif vert_code not in vert_codes:
                rmmap.append(file_path)

        scatfiles = os.listdir(outdirs["scat"])
        for file_path in rmmap:  # delete map files
            logger.info(f"Deleting outdated map json file: {file_path}.")
            os.remove(file_path)
            modified.append(file_path)
            fname = os.path.basename(file_path)
            if fname in scatfiles:
                scfp = os.path.join(outdirs["scat"], fname)
                logger.info(f"Deleting outdated scatter json file: {scfp}.")
                os.remove(scfp)
                modified.append(file_path)

        tsfiles = self._get_json_output_files("ts")

        for file_path in tsfiles:
            if self._check_clean_ts_file(file_path):
                modified.append(file_path)
        modified.extend(self._clean_modelmap_files())
        self.update_interface()  # will take care of heatmap data
        return modified

    def _check_clean_ts_file(self, fp) -> bool:
        fname = os.path.basename(fp)
        spl = fname.split(".json")[0].split("_")
        vert_code, obsinfo = spl[-1], spl[-2]
        if vert_code not in self.cfg.obs_cfg.all_vert_types:
            logger.warning(
                f"Invalid or outdated vert code {vert_code} in ts file {fp}. File will be deleted."
            )
            os.remove(fp)
            return True
        obs_name = str.join("-", obsinfo.split("-")[:-1])
        if obs_name in self._invalid["obs"]:
            logger.info(
                f"Invalid or outdated obs name {obs_name} in ts file {fp}. "
                f"File will be deleted."
            )
            os.remove(fp)
            return True

        with self.avdb.lock():
            try:
                # TODO: Hack to get uri. Ideally this should be rewritten to use URIs directly further
                # up.
                uri = self.avdb._get_uri_for_file(fp)
                data = self.avdb.get_by_uri(uri)
            except Exception:
                logger.exception(f"FATAL: detected corrupt json file: {fp}. Removing file...")
                os.remove(fp)
                return True

            models_avail = list(data)
            models_in_exp = self.cfg.model_cfg.web_interface_names
            if all([mod in models_in_exp for mod in models_avail]):
                # nothing to clean up
                return False
            modified = False
            data_new = {}
            for mod_name in models_avail:
                if mod_name in models_in_exp:
                    data_new[mod_name] = data[mod_name]
                else:
                    modified = True
                    logger.info(f"Removing data for model {mod_name} from ts file: {fp}")

            self.avdb.put_by_uri(data_new, uri)
        return modified

    def _clean_modelmap_files(self) -> list[str]:
        # Note: to be called after cleanup of files in map subdir
        json_files = self._get_json_output_files("contour")
        rm = []
        for file in json_files:
            if not self.cfg.webdisp_opts.add_model_maps:
                rm.append(file)
            else:
                fname = os.path.basename(file)
                spl = fname.split(".")[0].split("_")
                if not len(spl) == 2:
                    msg = f"FATAL: invalid file convention for map json file: {file}."
                    if len(spl) > 2:
                        msg += "Likely due to underscore being present in model or variable name."
                    rm.append(file)
                    logger.warning(msg)
                elif spl[-1] in self._invalid["models"]:
                    rm.append(file)

        removed = []
        for file in rm:
            os.remove(file)
            removed.append(file)
            file1 = file.replace(".json", ".geojson")
            if os.path.exists(file1):
                os.remove(file1)
                removed.append(file)
        return removed

    def delete_experiment_data(self, also_coldata=True) -> None:
        """Delete all data associated with a certain experiment

        Note
        ----
        This simply deletes the experiment directory with all the json files
        and, if `also_coldata` is True, also the associated co-located data
        objects.

        Parameters
        ----------
        also_coldata : bool
            if True and if output directory for colocated data is default and
            specific for input experiment ID, then also all associated colocated
            NetCDF files are deleted. Defaults to True.
        """
        self.avdb.rm_experiment_data(self.proj_id, self.exp_id)

        if also_coldata:
            coldir = self.cfg.path_manager.get_coldata_dir()
            if os.path.exists(coldir):
                logger.info(f"Deleting everything under {coldir}")
                shutil.rmtree(coldir)
        self._del_entry_experiments_json(self.exp_id)

    def get_model_order_menu(self) -> list:
        """Order of models in menu

        Note
        ----
        Returns empty list if no specific order is to be used in which case
        the models will be alphabetically ordered
        """
        order = []
        if len(self.cfg.webdisp_opts.model_order_menu) > 0:
            if self.cfg.webdisp_opts.modelorder_from_config:
                raise AttributeError(
                    "Conflict: modelorder_from_config must be deactivated if "
                    "model_order_menu is specified explicitly"
                )
            order.extend(self.cfg.webdisp_opts.model_order_menu)
        elif self.cfg.webdisp_opts.obsorder_from_config:
            order.extend(self.cfg.model_cfg.web_interface_names)
        return order

    def get_obs_order_menu(self) -> list:
        """Order of observation entries in menu"""
        order = []
        if len(self.cfg.webdisp_opts.obs_order_menu) > 0:
            if self.cfg.webdisp_opts.obsorder_from_config:
                raise AttributeError(
                    "Conflict: obsorder_from_config must be deactivated if "
                    "obs_order_menu is specified explicitly"
                )
            order.extend(self.cfg.webdisp_opts.obs_order_menu)
        elif self.cfg.webdisp_opts.obsorder_from_config:
            order.extend(self.cfg.obs_cfg.web_interface_names)
        return order

    def _get_json_output_files(self, dirname) -> list[str]:
        dirloc = self.out_dirs_json[dirname]
        return glob.glob(f"{dirloc}/*.json")

    def _get_cmap_info(self, var) -> dict[str, str | list[float]]:
        var_ranges_defaults = self.cfg.var_scale_colmap
        if var in var_ranges_defaults:
            return var_ranges_defaults[var]
        try:
            varinfo = VarinfoWeb(var)
            # TODO: get unit from pyaerocom/data/variables.ini
            info = dict(scale=varinfo.cmap_bins, colmap=varinfo.cmap, unit=varinfo.unit)
        except (VariableDefinitionError, AttributeError):
            info = var_ranges_defaults["default"]
            logger.warning(
                f"Failed to infer cmap and variable "
                f"ranges for {var}, using default "
                f"settings which are {info}"
            )

        return info

    def _create_var_ranges_json(self) -> None:
        with self.avdb.lock():
            ranges = self.avdb.get_ranges(self.proj_id, self.exp_id, default={})

            avail = self._results_summary()
            all_vars = list(set(avail["ovar"] + avail["mvar"]))
            for var in all_vars:
                if var not in ranges or ranges[var]["scale"] == []:
                    ranges[var] = self._get_cmap_info(var)
                ranges[var]["unit"] = get_variable(var).units
            self.avdb.put_ranges(ranges, self.proj_id, self.exp_id)

    def _create_statistics_json(self) -> None:
        if self.cfg.statistics_opts.obs_only_stats:
            stats_info = statistics_obs_only
        elif self.cfg.statistics_opts.model_only_stats:
            stats_info = statistics_model_only
        else:
            stats_info = statistics_defaults
            stats_info.update(extended_statistics)

        # configurable statistics - drop any statistics provided in drop_stats
        if self.cfg.statistics_opts.drop_stats:
            for stat in self.cfg.statistics_opts.drop_stats:
                stats_info.pop(stat, None)

        # configure the number of decimals shown in statistics if provided
        if self.cfg.statistics_opts.stats_decimals:
            for stat in stats_info:
                stats_info[stat].update(decimals=self.cfg.statistics_opts.stats_decimals)

        if self.cfg.statistics_opts.add_trends:
            if self.cfg.processing_opts.obs_only:
                obs_statistics_trend = {
                    key: val for key, val in statistics_trend.items() if "mod" not in key
                }
                stats_info.update(obs_statistics_trend)
            else:
                stats_info.update(statistics_trend)

                if self.cfg.statistics_opts.avg_over_trends:
                    stats_info.update(statistics_mean_trend)
                    stats_info.update(statistics_median_trend)

        with self.avdb.lock():
            self.avdb.put_statistics(stats_info, self.proj_id, self.exp_id)

    def _get_var_name_and_type(self, var_name: str) -> VariableInfo:
        """Get menu name and type of observation variable

        Parameters
        ----------
        var_name : str
            Name of variable

        Returns
        -------
        VariableInfo :
            named tuple containing
            - menu name of this variable.
            - Vertical type of this variable (ie. 2D, 3D).
            - Category of this variable.
        """
        if var_name in self.cfg.var_web_info:
            name, tp, cat = self.cfg.var_web_info[var_name]
        else:
            name, tp, cat = var_name, "UNDEFINED", "UNDEFINED"
            logger.warning(f"Missing menu name definition for var {var_name}.")

        return VariableInfo(name, tp, cat)

    def _init_menu_entry(self, var: str) -> dict:
        name, tp, cat = self._get_var_name_and_type(var)
        out = {"type": tp, "cat": cat, "name": name, "obs": {}}
        try:
            lname = const.VARS[var].description
        except VariableDefinitionError:
            lname = "UNDEFINED"

        out["longname"] = lname
        try:
            # Comes in as a string. split() here breaks up based on space and returns either just the element in a list or the components of the string in a list
            only_use_in = const.VARS[var].only_use_in.split(" ")
            # only return only_use_in if key exists, otherwise do not
            out["only_use_in"] = only_use_in
        except AttributeError:
            pass
        return out

    def _check_ovar_mvar_entry(
        self, mcfg: ModelEntry, mod_var, ocfg: ObsCollection, obs_var
    ) -> bool:
        muv = mcfg.model_use_vars
        mrv = mcfg.model_rename_vars

        mvar_aliases = get_aliases(mod_var)
        for ovar, mvars in mcfg.model_add_vars.items():
            if obs_var in mvars:
                # for evaluation of entries in model_add_vars, the output json
                # files use the model variable both for obs and for model as a
                # workaround for the AeroVal heatmap display (which is based on
                # observation variables on the y-axis). E.g. if
                # model_add_vars=dict(od550aer=['od550so4']) then there will
                # 2 co-located data objects one where model od550aer is
                # co-located with obs od550aer and one where model od550so4
                # is co-located with obs od550aer, thus for the latter,
                # the obs variable is set to od550so4, so it shows up as a
                # separate entry in AeroVal.
                if obs_var in mrv:
                    # model_rename_vars is specified for that obs variable,
                    # e.g. using the above example, the output obs variable
                    # would be od550so4, however, the user want to rename
                    # the corresponding model variable via e.g.
                    # model_rename_vars=dict(od550so4='MyVar'). Thus,
                    # check if model variable is MyVar
                    if mod_var == mrv[obs_var]:
                        return True
                elif obs_var == mod_var:
                    # if match, then they should be the same here
                    return True

        obs_vars = ocfg.get_all_vars()
        if obs_var in obs_vars:
            if obs_var in muv:
                mvar_to_use = muv[obs_var]
                if mvar_to_use == mod_var:
                    # obs var is different from mod_var but this mapping is
                    # specified in mcfg.model_use_vars
                    return True
                elif mvar_to_use in mvar_aliases:
                    # user specified an alias name in config for the
                    # observation variable e.g. model_use_vars=dict(
                    # ac550aer=absc550dryaer).
                    return True
                elif mvar_to_use in mrv and mrv[mvar_to_use] == mod_var:
                    # user wants to rename the model variable
                    return True
            if obs_var in mrv and mrv[obs_var] == mod_var:
                # obs variable is in model_rename_vars
                return True
            elif mod_var in get_aliases(obs_var):
                # model var is an alias to obs var e.g. sconcpm10 to concpm10
                return True
            elif mod_var == obs_var:
                # default setting, includes cases where mcfg.model_use_vars
                # is set and the value of the model variable in
                # mcfg.model_use_vars is an alias for obs_var
                return True
        return False

    def _is_part_of_experiment(self, obs_name, obs_var, mod_name, mod_var) -> bool:
        """
        Check if input combination of model and obs var is valid

        Note
        ----
        The input parameters are supposed to be retrieved from json files
        stored in the map subdirectory of an existing AeroVal experiment. In
        complex setup cases the variable mapping (model / obs variables)
        used in these json filenames may not be the trivial one expected from
        the configuaration. These are cases where one specifies
        model_add_vars, or model_use_vars or model_rename_vars in a model
        entry.

        Parameters
        ----------
        obs_name : str
            Name of obs dataset.
        obs_var : str
            Name of obs variable.
        mod_name : str
            Name of model
        mod_var : str
            Name of model variable

        Returns
        -------
        bool
            True if this combination is valid, else False.

        """

        # MDA8 is computed on-the-fly ONLY if a MDA8_INPUT_VAR at hourly freq is detected.
        # Consequently, it is not specified in a config but should be included as part of the experiment.
        if obs_var in MDA8_OUTPUT_VARS and mod_var in MDA8_OUTPUT_VARS:
            return True

        # get model entry for model name
        try:
            mcfg = self.cfg.model_cfg.get_entry(mod_name)
        except EntryNotAvailable:
            self._invalid["models"].append(mod_name)
            return False
        # mapping of obs / model variables to be used

        # search obs entry (may have web_interface_name set, so have to
        # check keys of ObsCollection but also the individual entries for
        # occurence of web_interface_name).
        allobs = self.cfg.obs_cfg
        obs_matches = []
        for key, ocfg in allobs.items():
            if obs_name == allobs.get_web_interface_name(key):
                obs_matches.append(ocfg)
        if len(obs_matches) == 0:
            self._invalid["obs"].append(obs_name)
            # obs dataset is not part of experiment
            return False
        # first, check model_add_vars
        for ocfg in obs_matches:
            if self._check_ovar_mvar_entry(mcfg, mod_var, ocfg, obs_var):
                return True
        return False

    def _create_menu_dict(self) -> dict:
        new = {}
        files = self._get_json_output_files("map")
        for file in files:
            (obs_name, obs_var, vert_code, mod_name, mod_var, per) = self._info_from_map_file(file)

            if self._is_part_of_experiment(obs_name, obs_var, mod_name, mod_var):
                mcfg = self.cfg.model_cfg.get_entry(mod_name)
                var = mcfg.get_varname_web(mod_var, obs_var)
                if var not in new:
                    new[var] = self._init_menu_entry(var)

                if obs_name not in new[var]["obs"]:
                    new[var]["obs"][obs_name] = {}

                if vert_code not in new[var]["obs"][obs_name]:
                    new[var]["obs"][obs_name][vert_code] = {}
                if mod_name not in new[var]["obs"][obs_name][vert_code]:
                    new[var]["obs"][obs_name][vert_code][mod_name] = {}

                model_id = mcfg["model_id"]
                new[var]["obs"][obs_name][vert_code][mod_name] = {
                    "model_id": model_id,
                    "model_var": mod_var,
                    "obs_var": obs_var,
                }
            else:
                logger.warning(
                    f"Invalid entry: model {mod_name} ({mod_var}), obs {obs_name} ({obs_var})"
                )
        return new

    def _sort_menu_entries(self, avail: dict) -> dict:
        """
        Used in method :func:`update_menu_evaluation_iface`

        Sorts results of different menu entries (i.e. variables, observations
        and models).

        Parameters
        ----------
        avail : dict
            nested dictionary contining info about available results

        Returns
        -------
        dict
            input dictionary sorted in variable, obs and model layers. The order
            of variables, observations and models may be specified in
            AerocomEvaluation class and if not, alphabetic order is used.

        """
        # sort first layer (i.e. variables)
        avail = sort_dict_by_name(avail, pref_list=self.cfg.webdisp_opts.var_order_menu)

        new_sorted = {}
        for var, info in avail.items():
            new_sorted[var] = info
            obs_order = self.get_obs_order_menu()
            sorted_obs = sort_dict_by_name(info["obs"], pref_list=obs_order)
            new_sorted[var]["obs"] = sorted_obs
            for obs_name, vert_codes in sorted_obs.items():
                vert_codes_sorted = sort_dict_by_name(vert_codes)
                new_sorted[var]["obs"][obs_name] = vert_codes_sorted
                for vert_code, models in vert_codes_sorted.items():
                    model_order = self.get_model_order_menu()
                    models_sorted = sort_dict_by_name(models, pref_list=model_order)
                    new_sorted[var]["obs"][obs_name][vert_code] = models_sorted
        return new_sorted

    def _add_entry_experiments_json(self, exp_id: str, data) -> None:
        with self.avdb.lock():
            current = self.avdb.get_experiments(self.proj_id, default={})

            current[exp_id] = data

            self.avdb.put_experiments(current, self.proj_id)

    def _del_entry_experiments_json(self, exp_id) -> None:
        """
        Remove an entry from experiments.json

        Parameters
        ----------
        exp_id : str
            name of experiment

        Returns
        -------
        None

        """
        with self.avdb.lock():
            current = self.avdb.get_experiments(self.proj_id, default={})

            try:
                del current[exp_id]
            except KeyError:
                logger.warning(f"no such experiment registered: {exp_id}")
            self.avdb.put_experiments(current, self.proj_id)

    def reorder_experiments(self, exp_order=None) -> None:
        """Reorder experiment order in evaluation interface

        Puts experiment list into order as specified by `exp_order`, all
        remaining experiments are sorted alphabetically.

        Parameters
        ----------
        exp_order : list, optional
            desired experiment order, if None, then alphabetical order is used.
        """
        if exp_order is None:
            exp_order = []
        elif not isinstance(exp_order, list):
            raise ValueError("need list as input")

        with self.avdb.lock():
            current = self.avdb.get_experiments(self.proj_id, default={})

            current = sort_dict_by_name(current, pref_list=exp_order)
            self.avdb.put_experiments(current, self.proj_id)

    def add_heatmap_timeseries_entry(
        self,
        entry: dict,
        region: str,
        network: str,
        obsvar: str,
        layer: str,
        modelname: str,
        modvar: str,
    ):
        """Adds a heatmap entry to hm/ts

        :param entry: The entry to be added.
        :param network: Observation network
        :param obsvar: Observation variable
        :param layer: Vertical layer
        :param modelname: Model name
        :param modvar: Model variable
        """
        project = self.proj_id
        experiment = self.exp_id

        with self.avdb.lock():
            glob_stats = self.avdb.get_heatmap_timeseries(
                project, experiment, region, network, obsvar, layer, default={}
            )
            glob_stats = recursive_defaultdict(glob_stats)
            glob_stats[obsvar][network][layer][modelname][modvar] = round_floats(entry)
            self.avdb.put_heatmap_timeseries(
                glob_stats,
                project,
                experiment,
                region,
                network,
                obsvar,
                layer,
            )

    def add_forecast_entry(
        self,
        entry: dict,
        region: str,
        network: str,
        obsvar: str,
        layer: str,
        modelname: str,
        modvar: str,
    ):
        """Adds a forecast entry to forecast

        :param entry: The entry to be added.
        :param network: Observation network
        :param obsvar: Observation variable
        :param layer: Vertical layer
        :param modelname: Model name
        :param modvar: Model variable
        """
        project = self.proj_id
        experiment = self.exp_id

        with self.avdb.lock():
            glob_stats = self.avdb.get_forecast(
                project, experiment, region, network, obsvar, layer, default={}
            )
            glob_stats = recursive_defaultdict(glob_stats)
            glob_stats[obsvar][network][layer][modelname][modvar] = round_floats(entry)
            self.avdb.put_forecast(
                glob_stats,
                project,
                experiment,
                region,
                network,
                obsvar,
                layer,
            )

    def add_heatmap_entry(
        self,
        entry,
        frequency: str,
        network: str,
        obsvar: str,
        layer: str,
        modelname: str,
        modvar: str,
    ):
        """Adds a heatmap entry to glob_stats

        :param entry: The entry to be added.
        :param region: The region (eg. ALL)
        :param obsvar: Observation variable.
        :param layer: Vertical Layer (eg. SURFACE)
        :param modelname: Model name
        :param modelvar: Model variable.
        """
        project = self.proj_id
        experiment = self.exp_id

        with self.avdb.lock():
            glob_stats = self.avdb.get_glob_stats(project, experiment, frequency, default={})
            glob_stats = recursive_defaultdict(glob_stats)
            glob_stats[obsvar][network][layer][modelname][modvar] = entry
            self.avdb.put_glob_stats(glob_stats, project, experiment, frequency)

    def write_station_data(self, data):
        """Writes timeseries weekly.

        :param data: Data to be written.
        """
        project = self.proj_id
        experiment = self.exp_id

        location = data["station_name"]
        network = data["obs_name"]
        obsvar = data["var_name_web"]
        layer = data["vert_code"]
        modelname = data["model_name"]
        with self.avdb.lock():
            station_data = self.avdb.get_timeseries_weekly(
                project, experiment, location, network, obsvar, layer, default={}
            )
            station_data[modelname] = round_floats(data)
            self.avdb.put_timeseries_weekly(
                station_data, project, experiment, location, network, obsvar, layer
            )

    def write_timeseries(self, data):
        """Write timeseries

        Args:
            data: The timeseries object to be written.

        Note:
        -----
        All necessary metadata will be read from the data object.
        """
        if not isinstance(data, list):
            data = [data]

        project = self.proj_id
        experiment = self.exp_id
        with self.avdb.lock():
            for d in data:
                location = d["station_name"]
                network = d["obs_name"]
                obsvar = d["var_name_web"]
                layer = d["vert_code"]
                modelname = d["model_name"]

                timeseries = self.avdb.get_timeseries(
                    project, experiment, location, network, obsvar, layer, default={}
                )
                timeseries[modelname] = round_floats(d)
                self.avdb.put_timeseries(
                    timeseries, project, experiment, location, network, obsvar, layer
                )

    def add_profile_entry(
        self,
        data: ColocatedData,
        profile_viz: dict,
        periods: list[str],
        seasons: list[str],
        location,
        network,
        obsvar,
    ):
        """Adds an entry for the colocated data to profiles.json.

        Args:
            data (ColocatedData): For this vertical layer
            profile_viz (dict): Output of process_profile_data()
            periods (list[str]): periods to compute over (years)
            seasons (list[str]): seasons to compute over (e.g., All, DJF, etc.)
        """
        with self.avdb.lock():
            current = self.avdb.get_profiles(
                self.proj_id, self.exp_id, location, network, obsvar, default={}
            )
            current = recursive_defaultdict(current)

            for freq, coldata in data.items():
                model_name = coldata.model_name

                midpoint = (
                    float(coldata.data.attrs["vertical_layer"]["end"])
                    + float(coldata.data.attrs["vertical_layer"]["start"])
                ) / 2
                if "z" not in current[model_name]:
                    current[model_name]["z"] = [midpoint]  # initalize with midpoint

                if (
                    midpoint > current[model_name]["z"][-1]
                ):  # only store incremental increases in the layers
                    current[model_name]["z"].append(midpoint)

                # old boilerplate to get around recursive_default_dict issues
                if "obs" not in current[model_name]:
                    current[model_name]["obs"] = {}

                if freq not in current[model_name]["obs"]:
                    current[model_name]["obs"][freq] = {}

                if "mod" not in current[model_name]:
                    current[model_name]["mod"] = {}

                if freq not in current[model_name]["mod"]:
                    current[model_name]["mod"][freq] = {}

                for per in periods:
                    for season in seasons:
                        perstr = f"{per}-{season}"

                        if perstr not in current[model_name]["obs"][freq]:
                            current[model_name]["obs"][freq][perstr] = []
                        if perstr not in current[model_name]["mod"][freq]:
                            current[model_name]["mod"][freq][perstr] = []

                        current[model_name]["obs"][freq][perstr].append(
                            profile_viz["obs"][freq][perstr]
                        )
                        current[model_name]["mod"][freq][perstr].append(
                            profile_viz["mod"][freq][perstr]
                        )

                if "metadata" not in current[model_name]:
                    current[model_name]["metadata"] = {
                        "z_unit": coldata.data.attrs["altitude_units"],
                        "z_description": "Altitude ASL",
                        "z_long_description": "Altitude Above Sea Level",
                        "unit": coldata.unitstr,
                    }
                current[model_name] = round_floats(current[model_name])

            self.avdb.put_profiles(current, self.proj_id, self.exp_id, location, network, obsvar)
