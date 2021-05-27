# -*- coding: utf-8 -*-
from getpass import getuser
import os
from pyaerocom import const
from pyaerocom._lowlevel_helpers import ConstrainedContainer
from pyaerocom.colocation_auto import ColocationSetup
from pyaerocom.aeroval.var_names_web import VAR_MAPPING
from pyaerocom.aeroval.filemanagement import OutputPathManager
from pyaerocom.aeroval.helpers import (make_info_str_eval_setup, read_json,
                                       write_json)

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

class AddMethodsSetup(ConstrainedContainer):
    def __init__(self, **kwargs):
        self.add_methods_file = ''
        self.add_methods = {}
        self.update(**kwargs)

class EvalSetup(ConstrainedContainer):
    """Composite class representing a whole analysis setup

    This represents the level at which json I/O happens for configuration
    setup files.
    """
    def __init__(self, proj_id:str, exp_id:str, **kwargs):
        self.proj_info =  ProjectInfo(proj_id=proj_id)
        self.exp_info = ExperimentInfo(exp_id=exp_id)

        self.modelmaps_opts = ModelMapsSetup()
        self.colocation_opts = ColocationSetup(
                                    save_coldata=True,
                                    keep_data=False,
                                    regrid_res_deg=5
                                    )
        self.statistics_opts = StatisticsSetup(
                                    weighted_stats=True,
                                    annual_stats_constrained=False
                                    )
        self.webdisp_opts = WebDisplaySetup(add_maps=False)

        self.processing_opts = EvalRunOptions()
        self.addmethods_cfg = AddMethodsSetup()
        self.obs_cfg = {}
        self.model_cfg = {}
        self.var_mapping = VAR_MAPPING
        self.path_manager = OutputPathManager()
        self.update(**kwargs)

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

    def to_dict(self) -> dict:
        """
        Convert to dictionary

        Returns
        -------
        dict
            dict representation of the setup

        """
        output = {}
        self.update_summary_str()
        for key, val in self.items():
            if isinstance(val, ConstrainedContainer):
                output[key] = val.to_dict()
            else:
                output[key] = val
        return output

    @staticmethod
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
        write_json(self.to_dict(), filepath,
                   ignore_nan=ignore_nan,
                   indent=indent)

    @staticmethod
    def from_json(filepath):
        """Load configuration from json config file"""
        settings = read_json(filepath)
        return EvalSetup(**settings)

    def __setitem__(self, key, val):
        if key in self:
            setattr(self, key, val)
        for attr, subcfg in self.items():
            if isinstance(subcfg, ConstrainedContainer) and key in subcfg:
                setattr(subcfg, key, val)


if __name__ == '__main__':
    stp = EvalSetup('bla', 'blub')
    stp.update(res_deg=10)
    d = stp.to_dict()