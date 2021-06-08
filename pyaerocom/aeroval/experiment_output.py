# -*- coding: utf-8 -*-
import glob
import os
from pyaerocom import const
from pyaerocom._lowlevel_helpers import (DirLoc, StrType, JSONFile,
                                         TypeValidator, sort_dict_by_name)
from pyaerocom.variable import get_variable
from pyaerocom.exceptions import VariableDefinitionError
from pyaerocom.aeroval.helpers import read_json, write_json
from pyaerocom.aeroval.setupclasses import EvalSetup

class ProjectOutput:
    """JSON output for project"""
    proj_id = StrType()
    json_basedir = DirLoc(assert_exists=True)
    experiments_file = JSONFile(assert_exists=True)

    def __init__(self, proj_id:str, json_basedir:str):
        self.proj_id = proj_id
        self.json_basedir = json_basedir

    @property
    def proj_dir(self):
        """Project directory"""
        return os.path.join(self.json_basedir, self.proj_id)

    @property
    def experiments_file(self):
        """json file containing region specifications"""
        return os.path.join(self.proj_dir, 'experiments.json')

    @property
    def available_experiments(self):
        return list(read_json(self.experiments_file).keys())


class ExperimentOutput(ProjectOutput):
    """JSON output for experiment"""
    cfg = TypeValidator(EvalSetup)
    def __init__(self, cfg):
        self.cfg = cfg
        super(ExperimentOutput, self).__init__(cfg.proj_id,
                                               cfg.path_manager.json_basedir)


    @property
    def exp_id(self):
        return self.cfg.exp_id

    @property
    def exp_dir(self):
        """Experiment directory"""
        return os.path.join(self.proj_dir, self.exp_id)

    @property
    def regions_file(self):
        """json file containing region specifications"""
        return os.path.join(self.exp_dir, 'regions.json')

    @property
    def menu_file(self):
        """json file containing region specifications"""
        return os.path.join(self.exp_dir, 'menu.json')

    @property
    def results_available(self):
        """
        bool: True if results are available for this experiment, else False
        """
        if not self.exp_id in os.listdir(self.proj_id):
            return False
        elif not len(self.all_map_files) > 0:
            return False
        return True

    def update_interface(self):
        self.update_menu()
        #self.make_info_table_web()
        self.update_heatmap_json()
        self.cfg.to_json(self.exp_dir)

    def update_heatmap_json(self):
        """
        Synchronise content of heatmap json files with content of menu.json
        """
        menu = read_json(self.menu_file)
        for fp in self._get_json_output_files('hm'):
            data = read_json(fp)
            hm = {}
            for vardisp, info in menu.items():
                obs_dict = info['obs']
                if not vardisp in hm:
                    hm[vardisp] = {}
                for obs, odict in obs_dict.items():
                    if not obs in hm[vardisp]:
                        hm[vardisp][obs] = {}
                    for ovar, vdict in odict.items():
                        if not ovar in hm[vardisp][obs]:
                            hm[vardisp][obs][ovar] = {}
                        for vc, mdict in vdict.items():
                            if not vc in hm[vardisp][obs][ovar]:
                                hm[vardisp][obs][ovar][vc] = {}
                            for mod, minfo in mdict.items():
                                if not mod in hm[vardisp][obs][ovar][vc]:
                                    hm[vardisp][obs][ovar][vc][mod] = {}
                                modvar = minfo['model_var']
                                if not modvar in hm[vardisp][obs][ovar][vc][mod]:
                                    hm[vardisp][obs][ovar][vc][mod][modvar] = {}

                                hm_data = data[ovar][obs][vc][mod][modvar]
                                hm[vardisp][obs][ovar][vc][mod][modvar] = hm_data
            write_json(hm, fp, ignore_nan=True)

    @staticmethod
    def _info_from_map_file(filename):
        spl = os.path.basename(filename).split('.json')[0].split('_')
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

    def clean_json_files(self):
        """Checks all existing json files and removes outdated data

        This may be relevant when updating a model name or similar.
        """
        self._clean_modelmap_files()

        for file in self.all_map_files:
            (obs_name, obs_var, vc,
             mod_name, mod_var) = self._info_from_map_file(file)

            remove=False
            if not (obs_name in self.iface_names and
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

    def _clean_modelmap_files(self):
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

    def delete_experiment_data(self, base_dir=None, proj_id=None, exp_id=None,
                               also_coldata=True):
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
        if proj_id is None:
            proj_id = self.proj_id
        if exp_id is None:
            exp_id = self.exp_id
        if base_dir is None:
            base_dir = self.out_basedir
        try:
            delete_experiment_data_evaluation_iface(base_dir, proj_id, exp_id)
        except NameError:
            pass
        if also_coldata:
            coldir = self.cfg_colocation['basedir_coldata']
            chk = os.path.normpath(f'{self.proj_id}/{self.exp_id}')
            if os.path.normpath(coldir).endswith(chk) and os.path.exists(coldir):
                const.print_log.info(f'Deleting everything under {coldir}')
                shutil.rmtree(coldir)
        self.update_menu(delete_mode=True)

    def make_info_table_evaluation_iface(self):
        """
        Make an information table for an aeroval experiment based on menu.json

        Returns
        -------
        dict
            dictionary containing meta information

        """
        if not os.path.exists(self.menu_file):
            raise FileNotFoundError(f'No menu.json found for {self.exp_id}')

        SKIP_META = ['data_source', 'var_name', 'lon_range',
                     'lat_range', 'alt_range']
        menu = read_json(self.menu_file)
        with open(self.menu_file, 'r') as f:
            menu = simplejson.load(f)
        table = {}
        for obs_var, info in exp.items():
            for obs_name, vert_types in info['obs'].items():
                for vert_type, models in vert_types.items():
                    for mname, minfo in models.items():
                        if not mname in table:
                            table[mname] = mi = {}
                            mi['id'] = model_id = minfo['id']
                        else:
                            mi = table[mname]
                            model_id = mi['id']
                            if minfo['id'] != mi['id']:
                                raise KeyError('Unexpected error: conflict in model ID and name')

                        try:
                            mo = mi['obs']
                        except Exception:
                            mi['obs'] = mo = {}
                        if 'var' in minfo:
                            mvar = minfo['var']
                        else:
                            mvar = obs_var
                        if not obs_var in mo:
                            mo[obs_var] = oi = {}
                        else:
                            oi = mo[obs_var]
                        if obs_name in oi:
                            raise Exception
                        oi[obs_name] = motab = {}
                        motab['model_var'] = mvar
                        motab['obs_id'] = config.get_obs_id(obs_name)
                        files = glob.glob('{}/{}/{}*REF-{}*.nc'
                                          .format(config.coldata_dir,
                                                  model_id, mvar, obs_name))

                        if not len(files) == 1:
                            if len(files) > 1:
                                motab['MULTIFILES'] = len(files)
                            else:
                                motab['NOFILES'] = True
                            continue

                        coldata = ColocatedData(files[0])
                        for k, v in coldata.metadata.items():
                            if not k in SKIP_META:
                                if isinstance(v, (list, tuple)):
                                    if len(v) == 2:
                                        motab['{}_obs'.format(k)] = str(v[0])
                                        motab['{}_mod'.format(k)] = str(v[1])
                                    else:
                                        motab[k] = ';'.join([str(x) for x in v])
                                else:
                                    motab[k] = str(v)
        return table

    def make_info_table_web(self):
        """Make and safe table with detailed infos about processed data files

        The table is stored in as file minfo.json in directory :attr:`exp_dir`.
        """
        table = make_info_table_evaluation_iface(self)
        outname = os.path.join(self.exp_dir, 'minfo.json')
        write_json()
        with open(outname, 'w+') as f:
            f.write(simplejson.dumps(table, indent=2))
        return table


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
            order.extend(self.cfg.model_cfg.keylist())
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
            order.extend(self.cfg.obs_cfg.keylist())
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
            (obs_name, obs_var, vert_code,
             mod_name, mod_var) = self._info_from_map_file(file)
            tab.append([obs_var, obs_name, vert_code, mod_name, mod_var])
        return tab

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
        avail = self._get_available_results_dict()
        avail = self._sort_menu_entries(avail)
        write_json(avail, self.menu_file, indent=4)

    @property
    def iface_names(self):
        """
        List of observation dataset names used in aeroval interface
        """
        return self.cfg.obs_cfg.web_iface_names

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

        try:
            name, tp, cat = self.cfg.var_mapping[var_name]
        except KeyError:
            name, tp, cat = var_name, 'UNDEFINED', 'UNDEFINED'
            const.print_log.warning(
                f'Missing menu name definition for var {var_name}.')
        return (name, tp, cat)

    def _get_available_results_dict(self):
        def var_dummy():
            """Helper that creates empty dict for variable info"""
            return {'type'      :   '',
                    'cat'       :   '',
                    'name'      :   '',
                    'longname'  :   '',
                    'obs'       :   {}}
        new = {}
        tab = self._get_meta_from_map_files()
        for (obs_var, obs_name, vert_code, mod_name, mod_var) in tab:
            modvarname = mod_var + '*' if mod_var != obs_var else mod_var
            if not modvarname in new:
                new[modvarname] = d = var_dummy()
                name, tp, cat = self._get_var_name_and_type(mod_var)
                d['name'] = name
                d['type'] = tp
                d['cat']  = cat
                try:
                    lname = const.VARS[mod_var].description
                except VariableDefinitionError:
                    lname = 'UNDEFINED'
                d['longname'] = lname
            else:
                d = new[modvarname]

            if not obs_name in d['obs']:
                d['obs'][obs_name] = dobs = {}
            else:
                dobs = d['obs'][obs_name]
            if not obs_var in dobs:
                dobs[obs_var] = dobsvar = {}
            else:
                dobsvar = dobs[obs_var]
            if not vert_code in dobsvar:
                dobsvar[vert_code] = dobs_vert = {}
            else:
                dobs_vert = dobsvar[vert_code]
            model_id = self.cfg.model_cfg.get_entry(mod_name)['model_id']
            dobs_vert[mod_name] = {'model_id'  : model_id,
                                   'model_var' : mod_var,
                                   'obs_var'   : obs_var}
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

if __name__ == '__main__':
    m = OutputPathManager('bla', 'blub')
    print(m)
    bd = os.path.join(const.OUTPUTDIR, 'tmp')
    pr = ExperimentOutput('bla', 'blub', json_basedir=bd)
    pr.experiments_file



