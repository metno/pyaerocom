# -*- coding: utf-8 -*-
from getpass import getuser
import os
from pyaerocom import const
from pyaerocom._lowlevel_helpers import (ConstrainedContainer,
                                         NestedContainer, AsciiFileLoc)
from pyaerocom.colocation_auto import ColocationSetup
from pyaerocom.aeroval.var_names_web import VAR_MAPPING
from pyaerocom.aeroval.filemanagement import (OutputPathManager,
                                              ExperimentOutput)
from pyaerocom.aeroval.collections import ObsCollection, ModelCollection
from pyaerocom.aeroval.helpers import (read_json, write_json,
                                       _check_statistics_periods,
                                       _get_min_max_year_periods)
from pyaerocom.aeroval.aux_io_helpers import ReadAuxHandler
from pyaerocom.exceptions import AeroValConfigError

class ModelMapsSetup(ConstrainedContainer):
    def __init__(self, **kwargs):
        self.res_deg = 5
        self.vmin_vmax = {}
        self.update(**kwargs)

class StatisticsSetup(ConstrainedContainer):
    DEFAULT_FREQS = ['monthly', 'yearly']
    def __init__(self, **kwargs):
        self.weighted_stats = True
        self.annual_stats_constrained = False
        self.freqs = self.DEFAULT_FREQS
        self.main_freq = self.DEFAULT_FREQS[0]
        self.periods = []
        self.add_trends = False
        self.seasonal_stats = True
        self.update(**kwargs)

class WebDisplaySetup(ConstrainedContainer):
    CONSTRAINT_VALS = {
        'map_zoom' : ['World', 'Europe']
        }
    def __init__(self, **kwargs):
        self.regions_how = 'default'
        self.map_zoom = 'World'
        self.add_maps = False
        self.modelorder_from_config = True
        self.obsorder_from_config = True
        self.var_order_menu = []
        self.update(**kwargs)

class EvalRunOptions(ConstrainedContainer):
    def __init__(self, **kwargs):
        # bool options run (do not affect results)
        self.clear_existing_json = True
        self.only_json = False
        self.only_colocation = False
        #: If True, process only maps (skip obs evaluation)
        self.only_maps = False
        self.update(**kwargs)

class ProjectInfo(ConstrainedContainer):
    def __init__(self, proj_id: str):
        self.proj_id = proj_id

class ExperimentInfo(ConstrainedContainer):
    #: status of experiment
    CONSTRAINT_VALS = {
        'exp_status' : ['public', 'experimental']
        }
    def __init__(self, exp_id: str, **kwargs):
        self.exp_id = exp_id
        self.exp_name = ''
        self.exp_descr = ''
        self.exp_status = 'experimental'
        self.exp_pi = getuser()
        self.update(**kwargs)

class EvalSetup(NestedContainer, ConstrainedContainer):
    """Composite class representing a whole analysis setup

    This represents the level at which json I/O happens for configuration
    setup files.
    """
    gridded_io_aux_file = AsciiFileLoc(
        default=None,
        assert_exists=False,
        auto_create=False,
        logger=const.print_log,
        tooltip='.py file containing additional read methods for modeldata')
    ADD_GLOB = ['gridded_io_aux_file']
    def __init__(self, proj_id:str, exp_id:str, **kwargs):
        self.proj_info = ProjectInfo(proj_id=proj_id)
        self.exp_info = ExperimentInfo(exp_id=exp_id)

        self.modelmaps_opts = ModelMapsSetup()
        self.colocation_opts = ColocationSetup(
                                    save_coldata=True,
                                    keep_data=False,
                                    regrid_res_deg=5,
                                    min_num_obs=const.OBS_MIN_NUM_RESAMPLE,
                                    resample_how='mean'
                                    )
        self.statistics_opts = StatisticsSetup(
                                    weighted_stats=True,
                                    annual_stats_constrained=False
                                    )
        self.webdisp_opts = WebDisplaySetup(add_maps=False)

        self.processing_opts = EvalRunOptions()

        self.obs_cfg = ObsCollection()
        self.model_cfg = ModelCollection()

        self.var_mapping = VAR_MAPPING
        self.path_manager = OutputPathManager(self.proj_id, self.exp_id)
        self.gridded_aux_funs = {}
        self.update(**kwargs)
        if self.gridded_io_aux_file is not None:
           self._import_gridded_aux_funs()

    def _import_gridded_aux_funs(self):

         h = ReadAuxHandler(self.gridded_io_aux_file)
         self.gridded_aux_funs.update(**h.import_all())

    def get_model_entry(self, model_name):
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
        cfg._check_update_aux_funcs(self.gridded_aux_funs)
        cfg = cfg.to_dict()
        cfg['model_name'] = model_name
        return cfg

    def get_obs_entry(self, obs_name):
        """Get obs

        Parameters
        ----------
        model_name : str
            name of model run

        Returns
        -------
        dict
            Dictionary that specifies the model setup ready for the analysis
        """
        cfg = self.obs_cfg.get_entry(obs_name).to_dict()
        cfg['obs_name'] = obs_name
        return cfg


    @property
    def proj_id(self) -> str:
        """
        str: proj ID (wrapper to :attr:`proj_info.proj_id`)
        """
        return self.proj_info.proj_id

    @property
    def exp_id(self) -> str:
        """
        str: experiment ID (wrapper to :attr:`exp_info.exp_id`)
        """
        return self.exp_info.exp_id

    @property
    def json_filename(self) -> str:
        """
        str: Savename of config file: cfg_<proj_id>_<exp_id>.json
        """
        return f'cfg_{self.proj_id}_{self.exp_id}.json'

    def to_json(self, outdir, ignore_nan=True, indent=3):
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
        filepath = os.path.join(outdir, self.json_filename)
        write_json(self.json_repr(), filepath,
                   ignore_nan=ignore_nan,
                   indent=indent)

    @staticmethod
    def from_json(filepath):
        """Load configuration from json config file"""
        settings = read_json(filepath)
        return EvalSetup(**settings)

    def _check_time_config(self):
        periods = self.statistics_opts.periods
        colstart = self.colocation_opts['start']
        colstop = self.colocation_opts['stop']

        if len(periods) == 0:
            if colstart is None:
                raise AeroValConfigError(
                    'Either periods or start must be set...'
                    )
            per = self.colocation_opts._period_from_start_stop()
            periods = [per]
            const.print_log.info(
                f'periods is not set, inferred {per} from start '
                f'/ stop colocation settings.')

        self.statistics_opts.periods = _check_statistics_periods(periods)
        start, stop = _get_min_max_year_periods(periods)
        if colstart is None:
            self.colocation_opts['start'] = start
        if colstop is None:
            self.colocation_opts['stop'] = stop + 1 # add 1 year since we want to include stop year

    @property
    def exp_output(self):
        """
        ExperimentOutput: JSON output file manager
        """
        return ExperimentOutput(self.exp_id, self.proj_id,
                                self.path_manager.json_basedir)



if __name__ == '__main__':
    stp = EvalSetup('bla', 'blub', addmethods_cfg={'add_methods_file': 'bla'})
    stp['bla'] = 42
    stp.update(res_deg=10)
    d = stp.json_repr()