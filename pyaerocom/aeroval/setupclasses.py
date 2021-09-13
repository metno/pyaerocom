# -*- coding: utf-8 -*-
from getpass import getuser
import os
from pyaerocom import const
from pyaerocom._lowlevel_helpers import (ConstrainedContainer,
                                         NestedContainer, AsciiFileLoc,
                                         EitherOf, StrType, ListOfStrings,
                                         DirLoc)

from pyaerocom.colocation_auto import ColocationSetup
from pyaerocom.aeroval.collections import ObsCollection, ModelCollection
from pyaerocom.aeroval.helpers import (read_json, write_json,
                                       _check_statistics_periods,
                                       _get_min_max_year_periods)
from pyaerocom.aeroval.aux_io_helpers import ReadAuxHandler
from pyaerocom.exceptions import AeroValConfigError


class OutputPaths(ConstrainedContainer):
    JSON_SUBDIRS = ['map', 'ts', 'ts/diurnal', 'scat', 'hm', 'hm/ts', 'contour']

    json_basedir = DirLoc(
        default=os.path.join(const.OUTPUTDIR, 'aeroval/data'),
        assert_exists=True,
        auto_create=True,
        logger=const.print_log,
        tooltip='Base directory for json output files')

    coldata_basedir = DirLoc(
        default=os.path.join(const.OUTPUTDIR, 'aeroval/coldata'),
        assert_exists=True,
        auto_create=True,
        logger=const.print_log,
        tooltip='Base directory for colocated data output files (NetCDF)')

    ADD_GLOB = ['coldata_basedir', 'json_basedir']
    proj_id = StrType()
    exp_id = StrType()
    def __init__(self, proj_id:str, exp_id:str,
                 json_basedir:str=None, coldata_basedir:str=None):
        self.proj_id = proj_id
        self.exp_id = exp_id
        if coldata_basedir:
            self.coldata_basedir = coldata_basedir
        if json_basedir:
            self.json_basedir = json_basedir

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
        for subdir in self.JSON_SUBDIRS:
            loc = self._check_init_dir(os.path.join(base, subdir),
                                       assert_exists)
            out[subdir] = loc
        return out

class ModelMapsSetup(ConstrainedContainer):
    maps_freq = EitherOf(['monthly', 'yearly'])
    def __init__(self, **kwargs):
        self.maps_res_deg = 5
        self.update(**kwargs)

class StatisticsSetup(ConstrainedContainer):
    """
    Setup options for statistical calculations

    Attributes
    ----------
    weighted_stats : bool
        if True, statistical parameters are calculated using area weights,
        this is only relevant for gridded / gridded evaluations.
    annual_stats_constrained : bool
        if True, then only sites are considered that satisfy a potentially
        specified annual resampling constraint (see
        :attr:`pyaerocom.colocation_auto.ColocationSetup.min_num_obs`). E.g.
        lets say you want to calculate statistical parameters (bias,
        correlation, etc.) for monthly model / obs data for a given site and
        year. Lets further say, that there are only 8 valid months of data, and
        4 months are missing, so statistics will be calculated for that year
        based on 8 vs. 8 values. Now if
        :attr:`pyaerocom.colocation_auto.ColocationSetup.min_num_obs` is
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


    Parameters
    ----------
    kwargs
        any of the supported attributes, e.g.
        `StatisticsSetup(annual_stats_constrained=True)`

    """
    MIN_NUM = 3
    def __init__(self, **kwargs):
        self.weighted_stats = True
        self.annual_stats_constrained = False
        self.add_trends = False
        self.trends_min_yrs = 7
        self.stats_tseries_base_freq = None
        self.update(**kwargs)

class TimeSetup(ConstrainedContainer):
    DEFAULT_FREQS = ['monthly', 'yearly']
    SEASONS = ['all', 'DJF', 'MAM', 'JJA', 'SON']
    main_freq = StrType()
    freqs = ListOfStrings()
    periods = ListOfStrings()
    def __init__(self, **kwargs):
        self.main_freq = self.DEFAULT_FREQS[0]
        self.freqs = self.DEFAULT_FREQS
        self.periods = []

class WebDisplaySetup(ConstrainedContainer):

    map_zoom = EitherOf(['World', 'Europe'])
    regions_how = EitherOf(['default', 'aerocom', 'htap', 'country'])
    def __init__(self, **kwargs):
        self.regions_how = 'default'
        self.map_zoom = 'World'
        self.add_model_maps = False
        self.modelorder_from_config = True
        self.obsorder_from_config = True
        self.var_order_menu = []
        self.obs_order_menu = []
        self.model_order_menu = []
        self.update(**kwargs)

class EvalRunOptions(ConstrainedContainer):
    def __init__(self, **kwargs):
        # bool options run (do not affect results)
        self.clear_existing_json = True
        self.only_json = False
        self.only_colocation = False
        #: If True, process only maps (skip obs evaluation)
        self.only_model_maps = False
        self.update(**kwargs)

class ProjectInfo(ConstrainedContainer):
    def __init__(self, proj_id: str):
        self.proj_id = proj_id

class ExperimentInfo(ConstrainedContainer):
    def __init__(self, exp_id: str, **kwargs):
        self.exp_id = exp_id
        self.exp_name = ''
        self.exp_descr = ''
        self.public = False
        self.exp_pi = getuser()
        self.update(**kwargs)


class EvalSetup(NestedContainer, ConstrainedContainer):
    """Composite class representing a whole analysis setup

    This represents the level at which json I/O happens for configuration
    setup files.
    """
    IGNORE_JSON = ['_aux_funs']
    ADD_GLOB = ['io_aux_file']
    io_aux_file = AsciiFileLoc(
        default='',
        assert_exists=False,
        auto_create=False,
        logger=const.print_log,
        tooltip='.py file containing additional read methods for modeldata')
    _aux_funs = {}
    def __init__(self, proj_id:str, exp_id:str, **kwargs):
        self.proj_info = ProjectInfo(proj_id=proj_id)
        self.exp_info = ExperimentInfo(exp_id=exp_id)

        self.time_cfg = TimeSetup()

        self.modelmaps_opts = ModelMapsSetup()
        self.colocation_opts = ColocationSetup(
                                    save_coldata=True,
                                    keep_data=False,
                                    resample_how='mean'
                                    )
        self.statistics_opts = StatisticsSetup(
                                    weighted_stats=True,
                                    annual_stats_constrained=False
                                    )
        self.webdisp_opts = WebDisplaySetup(add_model_maps=False)

        self.processing_opts = EvalRunOptions()

        self.obs_cfg = ObsCollection()
        self.model_cfg = ModelCollection()

        self.var_web_info = {}
        self.path_manager = OutputPaths(self.proj_id, self.exp_id)
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

    @property
    def gridded_aux_funs(self):
        if not bool(self._aux_funs) and os.path.exists(self.io_aux_file):
            self._import_aux_funs()
        return self._aux_funs

    def get_all_vars(self) -> list:
        """
        Get list of all variables in this experiment

        Returns
        -------
        list

        """
        ovars = self.obs_cfg.get_all_vars()
        mvars = self.model_cfg.get_all_vars()
        return sorted(list(set(ovars + mvars)))

    def get_obs_entry(self, obs_name):
        return self.obs_cfg.get_entry(obs_name).to_dict()

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
        cfg = cfg.prep_dict_analysis(self.gridded_aux_funs)
        return cfg

    def to_json(self, outdir:str, ignore_nan:bool=True, indent:int=3) -> None:
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
        data = self.json_repr()
        write_json(data, filepath,
                   ignore_nan=ignore_nan,
                   indent=indent)

    @staticmethod
    def from_json(filepath:str) -> 'EvalSetup':
        """Load configuration from json config file"""
        settings = read_json(filepath)
        return EvalSetup(**settings)

    def _import_aux_funs(self):

         h = ReadAuxHandler(self.io_aux_file)
         self._aux_funs.update(**h.import_all())

    def _check_time_config(self):
        periods = self.time_cfg.periods
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

        self.time_cfg['periods'] = _check_statistics_periods(periods)
        start, stop = _get_min_max_year_periods(periods)
        if colstart is None:
            self.colocation_opts['start'] = start
        if colstop is None:
            self.colocation_opts['stop'] = stop + 1 # add 1 year since we want to include stop year



if __name__ == '__main__':
    stp = EvalSetup('bla', 'blub', addmethods_cfg={'add_methods_file': 'bla'})
    stp['bla'] = 42
    stp.update(res_deg=10)
    d = stp.json_repr()