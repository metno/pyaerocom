import glob
import os
import shutil


from pyaerocom import const
from pyaerocom._lowlevel_helpers import (
    DirLoc,
    StrType,
    TypeValidator,
    check_make_json,
    read_json,
    sort_dict_by_name,
    write_json,
)
from pyaerocom.aeroval.glob_defaults import (
    statistics_defaults,
    statistics_trend,
    extended_statistics,
    var_ranges_defaults,
    var_web_info,
)

from pyaerocom.aeroval.helpers import read_json, write_json
from pyaerocom.aeroval.setupclasses import EvalSetup
from pyaerocom.aeroval.varinfo_web import VarinfoWeb
from pyaerocom.exceptions import VariableDefinitionError
from pyaerocom.mathutils import _init_stats_dummy
from pyaerocom.variable_helpers import get_aliases


class ProjectOutput:
    """JSON output for project"""
    proj_id = StrType()
    json_basedir = DirLoc(assert_exists=True)
    def __init__(self, proj_id:str, json_basedir:str):
        self.proj_id = proj_id
        self.json_basedir = json_basedir

    @property
    def proj_dir(self):
        """Project directory"""
        fp = os.path.join(self.json_basedir, self.proj_id)
        if not os.path.exists(fp):
            os.mkdir(fp)
            const.print_log.info(
                f'Creating AeroVal project directory at {fp}')
        return fp

    @property
    def experiments_file(self):
        """json file containing region specifications"""
        fp = os.path.join(self.proj_dir, 'experiments.json')
        fp = check_make_json(fp)
        return fp

    @property
    def available_experiments(self):
        """
        List of available experiments
        """
        return list(read_json(self.experiments_file).keys())

    def _add_entry_experiments_json(self, exp_id, data):
        fp = self.experiments_file
        current = read_json(fp)
        current[exp_id] = data
        write_json(current, self.experiments_file, indent=4)

    def _del_entry_experiments_json(self, exp_id):
        current = read_json(self.experiments_file)
        try:
            del current[exp_id]
        except KeyError:
            const.print_log.warning(
                f'no such experiment registered: {exp_id}')
        write_json(current, self.experiments_file, indent=4)


class ExperimentOutput(ProjectOutput):
    """JSON output for experiment"""
    cfg = TypeValidator(EvalSetup)
    def __init__(self, cfg):
        self.cfg = cfg
        super(ExperimentOutput, self).__init__(cfg.proj_id,
                                               cfg.path_manager.json_basedir)

    @property
    def exp_id(self):
        """Experiment ID"""
        return self.cfg.exp_id

    @property
    def exp_dir(self):
        """Experiment directory"""
        fp = os.path.join(self.proj_dir, self.exp_id)
        if not os.path.exists(fp):
            os.mkdir(fp)
            const.print_log.info(
                f'Creating AeroVal experiment directory at {fp}')
        return fp

    @property
    def regions_file(self):
        """json file containing region specifications"""
        fp = os.path.join(self.exp_dir, 'regions.json')
        fp = check_make_json(fp)
        return fp

    @property
    def statistics_file(self):
        """json file containing region specifications"""
        fp = os.path.join(self.exp_dir, 'statistics.json')
        fp = check_make_json(fp)
        return fp

    @property
    def var_ranges_file(self):
        """json file containing region specifications"""
        fp = os.path.join(self.exp_dir, 'ranges.json')
        check_make_json(fp)
        return fp

    @property
    def menu_file(self):
        """json file containing region specifications"""
        fp = os.path.join(self.exp_dir, 'menu.json')
        check_make_json(fp)
        return fp


    @property
    def results_available(self):
        """
        bool: True if results are available for this experiment, else False
        """
        if not self.exp_id in os.listdir(self.proj_dir):
            return False
        elif not len(self._get_json_output_files('map')) > 0:
            return False
        return True

    def update_menu(self):
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
        write_json(avail, self.menu_file, indent=4)

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
            const.print_log.warning(
                f'no output available for experiment {self.exp_id} in '
                f'{self.proj_id}')
            return
        exp_data = {
            'public' : self.cfg.exp_info.public
            }
        self._add_entry_experiments_json(self.exp_id, exp_data)
        self._create_var_ranges_json()
        self.update_menu()
        #self.make_info_table_web()
        self._sync_heatmaps_with_menu_and_regions()

        self._create_statistics_json()
        # AeroVal frontend needs periods to be set in config json file...
        # make sure they are
        self.cfg._check_time_config()
        self.cfg.to_json(self.exp_dir)

    def _sync_heatmaps_with_menu_and_regions(self):
        """
        Synchronise content of heatmap json files with content of menu.json
        """
        menu = read_json(self.menu_file)
        all_regions = read_json(self.regions_file)
        for fp in self._get_json_output_files('hm'):
            data = read_json(fp)
            hm = {}
            for vardisp, info in menu.items():
                obs_dict = info['obs']
                if not vardisp in hm:
                    hm[vardisp] = {}
                for obs, vdict in obs_dict.items():
                    if not obs in hm[vardisp]:
                        hm[vardisp][obs] = {}
                    for vc, mdict in vdict.items():
                        if not vc in hm[vardisp][obs]:
                            hm[vardisp][obs][vc] = {}
                        for mod, minfo in mdict.items():
                            if not mod in hm[vardisp][obs][vc]:
                                hm[vardisp][obs][vc][mod] = {}
                            modvar = minfo['model_var']
                            hm_data = data[vardisp][obs][vc][mod][modvar]
                            hm_data = self._check_hm_all_regions_avail(
                                all_regions, hm_data)
                            hm[vardisp][obs][vc][mod][modvar] = hm_data

            write_json(hm, fp, ignore_nan=True)

    def _check_hm_all_regions_avail(self, all_regions, hm_data):
        if all([x in hm_data for x in all_regions]):
            return hm_data
        # some regions are not available in this subset
        periods = self.cfg.time_cfg._get_all_period_strings()
        dummy_stats = _init_stats_dummy()
        for region in all_regions:
            if not region in hm_data:
                hm_data[region] = {}
                for per in periods:
                    hm_data[region][per] = dummy_stats
        return hm_data

    @staticmethod
    def _info_from_map_file(filename):
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
        """
        spl = os.path.basename(filename).split('.json')[0].split('_')
        if len(spl) != 3:
            raise ValueError(f'invalid map filename: {filename}. Must '
                             f'contain exactly 2 underscores _ to separate '
                             f'obsinfo, vertical and model info')
        obsinfo = spl[0]
        vert_code = spl[1]
        modinfo = spl[2]

        mspl = modinfo.split('-')
        mvar = mspl[-1]
        mname = '-'.join(mspl[:-1])

        ospl = obsinfo.split('-')
        ovar = ospl[-1]
        oname = '-'.join(ospl[:-1])
        return (oname, ovar, vert_code, mname, mvar)

    def _results_summary(self):
        res = [[],[],[],[],[]]
        info = self._get_meta_from_map_files()
        for item in info:
            for i, entry in enumerate(item):
                res[i].append(entry)
        output = {}
        for i, name in enumerate(['obs', 'ovar', 'vc', 'mod', 'mvar']):
            output[name] = list(set(res[i]))
        return output

    # ToDo: rewrite or delete before v0.12.0
    def clean_json_files(self):
        """Checks all existing json files and removes outdated data

        This may be relevant when updating a model name or similar.
        """
        raise NotImplementedError('under revision')
        self._clean_modelmap_files()

        for file in self.all_map_files:
            (obs_name, obs_var, vc,
             mod_name, mod_var) = self._info_from_map_file(file)

            remove=False
            if not (obs_name in self.cfg.obs_cfg.web_iface_names and
                    mod_name in self.model_config):
                remove = True
            elif not obs_var in self._get_valid_obs_vars(obs_name):
                remove = True
            elif not vc in self.JSON_SUPPORTED_VERT_SCHEMES:
                remove = True
            else:
                mcfg = self.model_config[mod_name]
                if 'model_use_vars' in mcfg and obs_var in mcfg['model_use_vars']:
                    if not mod_var == mcfg['model_use_vars'][obs_var]:
                        remove=True

            if remove:
                const.print_log.info(f'Removing outdated map file: {file}')
                os.remove(os.path.join(self.out_dirs['map'], file))

        for fp in glob.glob('{}/*.json'.format(self.out_dirs['ts'])):
            self._check_clean_ts_file(fp)

        self.update_interface()

    # ToDo: rewrite or delete before v0.12.0
    def _clean_modelmap_files(self):
        raise NotImplementedError('under revision')
        all_vars = self.all_modelmap_vars
        all_mods = self.all_model_names
        out_dir = self.out_dirs['contour']

        for file in os.listdir(out_dir):
            spl = file.replace('.', '_').split('_')
            if not len(spl) == 4:
                raise ValueError(f'Invalid json map filename {file}')
            var, vc, mod_name = spl[:3]
            rm = (not var in all_vars or
                  not mod_name in all_mods or
                  not vc in self.JSON_SUPPORTED_VERT_SCHEMES)
            if rm:
                const.print_log.info(
                    f'Removing invalid model maps file {file}'
                    )
                os.remove(os.path.join(out_dir, file))

    def delete_experiment_data(self, also_coldata=True):
        """Delete all data associated with a certain experiment

        Parameters
        ----------
        base_dir : str, optional
            basic output direcory (containing subdirs of all projects)
        proj_name : str, optional
            name of project, if None, then this project is used
        exp_name : str, optional
            name experiment, if None, then this project is used
        also_coldata : bool
            if True and if output directory for colocated data is default and
            specific for input experiment ID, then also all associated colocated
            NetCDF files are deleted. Defaults to True.
        """
        if os.path.exists(self.exp_dir):
            const.print_log.info(f'Deleting everything under {self.exp_dir}')
            shutil.rmtree(self.exp_dir)

        if also_coldata:
            coldir = self.cfg.path_manager.get_coldata_dir()
            if os.path.exists(coldir):
                const.print_log.info(f'Deleting everything under {coldir}')
                shutil.rmtree(coldir)
        self._del_entry_experiments_json(self.exp_id)


    def get_model_order_menu(self):
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
                    'Conflict: modelorder_from_config must be deactivated if '
                    'model_order_menu is specified explicitly')
            order.extend(self.cfg.webdisp_opts.model_order_menu)
        elif self.cfg.webdisp_opts.obsorder_from_config:
            order.extend(self.cfg.model_cfg.web_iface_names)
        return order


    def get_obs_order_menu(self):
        order = []
        if len(self.cfg.webdisp_opts.obs_order_menu) > 0:
            if self.cfg.webdisp_opts.obsorder_from_config:
                raise AttributeError(
                    'Conflict: obsorder_from_config must be deactivated if '
                    'obs_order_menu is specified explicitly')
            order.extend(self.cfg.webdisp_opts.obs_order_menu)
        elif self.cfg.webdisp_opts.obsorder_from_config:
            order.extend(self.cfg.obs_cfg.web_iface_names)
        return order


    @property
    def out_dirs_json(self):
        return self.cfg.path_manager.get_json_output_dirs()


    def _get_json_output_files(self, dirname):
        dirloc = self.out_dirs_json[dirname]
        return glob.glob(f'{dirloc}/*.json')


    def _get_meta_from_map_files(self):
        """List of all existing map files"""
        files = self._get_json_output_files('map')
        tab = []
        for file in files:
            tab.append(self._info_from_map_file(file))
        return tab


    def _get_cmap_info(self, var):
        if var in var_ranges_defaults:
            return var_ranges_defaults[var]
        try:
            varinfo = VarinfoWeb(var)
            return dict(scale=varinfo.cmap_bins,
                        colmap=varinfo.cmap)
        except VariableDefinitionError:
            return dict(scale=[], colmap='coolwarm')


    def _create_var_ranges_json(self):
        try:
            ranges = read_json(self.var_ranges_file)
        except FileNotFoundError:
            ranges = {}
        avail = self._results_summary()
        all_vars = list(set(avail['ovar'] + avail['mvar']))
        for var in all_vars:
            if not var in ranges or ranges[var]['scale'] == []:
                ranges[var] = self._get_cmap_info(var)
        write_json(ranges, self.var_ranges_file, indent=4)


    def _create_statistics_json(self):
        stats_info = statistics_defaults
        stats_info.update(extended_statistics)
        if self.cfg.statistics_opts.add_trends:
            stats_info.update(statistics_trend)
        write_json(stats_info, self.statistics_file, indent=4)


    def _get_var_name_and_type(self, var_name):
        """Get menu name and type of observation variable

        Parameters
        ----------
        var_name : str
            Name of variable

        Returns
        -------
        str
            menu name of this variable
        str
            vertical type of this variable (2D, 3D)
        str
            variable category

        """
        if var_name in self.cfg.var_web_info:
            name, tp, cat = self.cfg.var_mapping[var_name]
        elif var_name in var_web_info:
            name, tp, cat = var_web_info[var_name]
        else:
            name, tp, cat = var_name, 'UNDEFINED', 'UNDEFINED'
            const.print_log.warning(
                f'Missing menu name definition for var {var_name}.')
        return (name, tp, cat)


    def _init_menu_entry(self, var : str) -> dict:
        name, tp, cat = self._get_var_name_and_type(var)
        try:
            lname = const.VARS[var].description
        except VariableDefinitionError:
            lname = 'UNDEFINED'
        return {'type'      :   tp,
                'cat'       :   cat,
                'name'      :   name,
                'longname'  :   lname,
                'obs'       :   {}}

    def _check_ovar_mvar_entry(self, mcfg, mod_var, ocfg, obs_var):

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
            elif mod_var == obs_var:
                # default setting, includes cases where mcfg.model_use_vars
                # is set and the value of the model variable in
                # mcfg.model_use_vars is an alias for obs_var
                return True
        return False

    def _is_part_of_experiment(self, obs_name, obs_var, mod_name, mod_var):
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
        # get model entry for model name
        mcfg = self.cfg.model_cfg.get_entry(mod_name)
        # mapping of obs / model variables to be used

        # search obs entry (may have web_interface_name set, so have to
        # check keys of ObsCollection but also the individual entries for
        # occurence of web_interface_name).
        allobs = self.cfg.obs_cfg
        obs_matches = []
        for key, ocfg in allobs.items():
            if obs_name == allobs.get_web_iface_name(key):
                obs_matches.append(ocfg)
        if len(obs_matches) == 0:
            # obs dataset is not part of experiment
            return False
        # first, check model_add_vars
        for ocfg in obs_matches:
            if self._check_ovar_mvar_entry(mcfg, mod_var, ocfg, obs_var):
                return True
        return False

    def _create_menu_dict(self):
        new = {}
        tab = self._get_meta_from_map_files()
        for (obs_name, obs_var, vert_code, mod_name, mod_var) in tab:
            if self._is_part_of_experiment(obs_name, obs_var,
                                           mod_name, mod_var):

                mcfg = self.cfg.model_cfg.get_entry(mod_name)
                var = mcfg.get_varname_web(mod_var, obs_var)
                if not var in new:
                    new[var] = self._init_menu_entry(var)

                if not obs_name in new[var]['obs']:
                    new[var]['obs'][obs_name] = {}

                if not vert_code in new[var]['obs'][obs_name]:
                    new[var]['obs'][obs_name][vert_code] = {}
                if not mod_name in new[var]['obs'][obs_name][vert_code]:
                    new[var]['obs'][obs_name][vert_code][mod_name] = {}

                model_id = mcfg['model_id']
                new[var]['obs'][obs_name][vert_code][mod_name] = {
                    'model_id'  : model_id,
                    'model_var' : mod_var,
                    'obs_var'   : obs_var}
            else:
                const.print_log.warning(
                    f'Invalid entry: model {mod_name} ({mod_var}), '
                    f'obs {obs_name} ({obs_var})')
        return new


    def _sort_menu_entries(self, avail):
        """
        Used in method :func:`update_menu_evaluation_iface`

        Sorts results of different menu entries (i.e. variables, observations
        and models).

        Parameters
        ----------
        avail : dict
            nested dictionary contining info about available results
        config : AerocomEvaluation
            Configuration class

        Returns
        -------
        dict
            input dictionary sorted in variable, obs and model layers. The order
            of variables, observations and models may be specified in
            AerocomEvaluation class and if not, alphabetic order is used.

        """
        # sort first layer (i.e. variables)
        avail = sort_dict_by_name(avail,
                                  pref_list=self.cfg.webdisp_opts.var_order_menu)

        new_sorted = {}
        for var, info in avail.items():
            new_sorted[var] = info
            obs_order = self.get_obs_order_menu()
            sorted_obs = sort_dict_by_name(info['obs'],
                                           pref_list=obs_order)
            new_sorted[var]['obs'] = sorted_obs
            for obs_name, vert_codes in sorted_obs.items():
                vert_codes_sorted = sort_dict_by_name(vert_codes)
                new_sorted[var]['obs'][obs_name] = vert_codes_sorted
                for vert_code, models in vert_codes_sorted.items():
                    model_order = self.get_model_order_menu()
                    models_sorted = sort_dict_by_name(models,
                                                      pref_list=model_order)
                    new_sorted[var]['obs'][obs_name][vert_code] = models_sorted
        return new_sorted


    def _check_clean_ts_file(self, fp):

        spl = os.path.basename(fp).split('OBS-')[-1].split(':')
        obs_name = spl[0]
        obs_var, vc, _ = spl[1].replace('.', '_').split('_')
        rm = (not vc in self.JSON_SUPPORTED_VERT_SCHEMES or
              not obs_name in self.obs_config or
              not obs_var in self._get_valid_obs_vars(obs_name))
        if rm:
            const.print_log.info('Removing outdated ts file: {}'.format(fp))
            os.remove(fp)
            return
        try:
            data = read_json(fp)
        except Exception:
            const.print_log.exception('FATAL: detected corrupt json file: {}. '
                                      'Removing file...'.format(fp))
            os.remove(fp)
            return
        if all([x in self.model_config for x in list(data.keys())]):
            return
        data_new = {}
        for mod_name in data.keys():
            if not mod_name in self.model_config:
                const.print_log.info('Removing model {} from {}'
                                .format(mod_name, os.path.basename(fp)))
                continue

            data_new[mod_name] = data[mod_name]

        write_json(data_new, fp)


    def _get_valid_obs_vars(self, obs_name):
        if obs_name in self._valid_obs_vars:
            return self._valid_obs_vars[obs_name]

        obs_vars = self.obs_config[obs_name]['obs_vars']
        add = []
        for mname, mcfg in self.model_config.items():
            if 'model_add_vars' in mcfg:
                for ovar, mvar in mcfg['model_add_vars'].items():
                    if ovar in obs_vars and not mvar in add:
                        add.append(mvar)
        obs_vars.extend(add)
        self._valid_obs_vars[obs_name]  = obs_vars
        return obs_vars
