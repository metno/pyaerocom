#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
High level module containing analysis classes and methods to perform 
colocation.

NOTE
----

This module will be deprecated soon but most of the code will be refactored 
into colocation.py module.
"""
import os
import numpy as np
import traceback
import matplotlib.pyplot as plt
from datetime import datetime

from pyaerocom._lowlevel_helpers import BrowseDict, chk_make_subdir
from pyaerocom import Filter, const
from pyaerocom.helpers import (to_pandas_timestamp, to_datestring_YYYYMMDD)
from pyaerocom.io.helpers import get_all_supported_ids_ungridded
from pyaerocom.colocation import (colocate_gridded_gridded,
                                  colocate_gridded_ungridded_2D)
from pyaerocom import ColocatedData, print_log
from pyaerocom.io import ReadUngridded, ReadGridded
from pyaerocom.exceptions import NetworkNotSupported, DataCoverageError


    
            
class _ColocationOptions(BrowseDict):
    """This class contains options for Aerocom analysis
    """
    def __init__(self, REANALYSE_EXISTING=False, RAISE_EXCEPTIONS=False):
        self.REANALYSE_EXISTING = REANALYSE_EXISTING,
        self.RAISE_EXCEPTIONS = RAISE_EXCEPTIONS
           
   
class VarSetup(BrowseDict):
    """Variable setup for analysis (dictionary)
    
    Attributes
    -----------
    var_name : str
        variable name
    obs_id : str
        ID of observation network
    var_name_obs : :obj:`str`, optional
        variable name of observation data. If None, ``var_name`` is used for
        observation network
    vert_scheme : :obj:`str`, optional
        vertical scheme for time-series retrieval in case of 4D data (cf.
        :func:`pyaerocom.GriddedData.to_time_series`)
        
    Parameters
    ----------
    see attributes
    """
    def __init__(self, var_name, obs_id, var_name_obs=None, vert_scheme=None):
        self.var_name = var_name
        self.obs_id = obs_id
        self.var_name_obs = var_name_obs
        self.vert_scheme = vert_scheme
        
class ColocationSetup(BrowseDict):
    """Setup class for model / obs intercomparison
    
    An instance of this setup class can be used to run a colocation analysis
    between a model and an observation network and will create a number of 
    :class:`pya.ColocatedData` instances and save them as netCDF file.
    
    Note
    ----
    This is a very first draft and will likely undergo significant changes
    
    Attributes
    ----------
    model_id : str
        ID of model to be used
    obs_id : str
        ID of observation network to be used
    obs_vars : :obj:`str` or :obj:`list`, optional
        variables to be analysed. If any of the provided variables to be 
        analysed in the model data is not available in obsdata, the obsdata 
        will be checked against potential alternative variables which are
        specified in :attr:`model_alt_vars` and which can be specified in form of a 
        dictionary for each . If None, all
        variables are analysed that are available both in model and obsdata.
    start : :obj:`pandas.Timestamp`, optional
        start time. Input can be anything that can be converted into 
        :class:`pandas.Timestamp` using 
        :func:`pyaerocom.helpers.to_pandas_timestamp`. If None, than the first
        available date in the model data is used.
    stop
        stop time. Anything that can be converted into 
        :class:`pandas.Timestamp` using 
        :func:`pyaerocom.helpers.to_pandas_timestamp` or None. If None and if
        ``start`` is on resolution of year (e.g. ``start=2010``) then ``stop``
        will be automatically set to the end of that year. Else, it will be 
        set to the last available timestamp in the model data.
    filter_name : str
        name of filter to be applied
    ts_types_ana : :obj:`list` or similar, optional
        names of frequencies to be analysed (for which colocated data objects
        are created)
    
    """ 
    #: all ID's of ungridded datasets
    _UNGRIDDED_IDS = get_all_supported_ids_ungridded()
    def __init__(self, model_id=None, obs_id=None, obs_vars=None, 
                 start=None, stop=None, filter_name='WORLD-noMOUNTAINS',
                 vert_scheme=None, model_alt_vars=None, 
                 basedir_coldata=None, basedir_logfiles=None, read_opts=None):
        if read_opts is None:
            read_opts = {}
        if isinstance(obs_vars, str):
            obs_vars = [obs_vars]
        if model_alt_vars is None: 
            model_alt_vars = {}
        try:
            Filter(filter_name)
        except:
            raise ValueError('Invalid input for filter_name')
        if basedir_coldata is None:
            basedir_coldata = const.COLOCATEDDATADIR
        if not os.path.exists(basedir_coldata):
            const.print_log.info('Creating directory: {}'.format(basedir_coldata))
            os.mkdir(basedir_coldata)
        if basedir_logfiles is None:
            basedir_logfiles = chk_make_subdir(basedir_coldata, 'logfiles')
            
        const.print_log.info('Output directory for colocated data:\n '
                             '{}'.format(basedir_coldata))
        const.print_log.info('Output directory for logfiles:\n '
                             '{}'.format(basedir_coldata))
        self.obs_vars = obs_vars
        
        self.model_alt_vars = model_alt_vars
        
        self.model_id = model_id
        self.obs_id = obs_id
    
        self.options = _ColocationOptions()

        self.start = start
        self.stop = stop
        self.filter_name = filter_name
        self.vert_scheme = vert_scheme
        
        self.basedir_coldata = basedir_coldata
        self.basedir_logfiles = basedir_logfiles
    
        self._read_opts = {}
        self._read_opts.update(**read_opts)
            
    def __dir__(self):
        return self.keys()
    
    def update(self, **kwargs):
        for key, val in kwargs.items():
            if key in self.options:
                self.options[key] = val
            else:
                self[key] = val


class Colocator(object):
    """High level class for running colocation

    TODO
    ----
    - write docstring
    """
    
    def __init__(self, setup=None, **kwargs):
        if setup is None:
            setup = ColocationSetup()
        setup.update(**kwargs)
        self._setup = setup
        self._log = None
        self._last_coldata = None
        self._ungridded_reader = ReadUngridded()
        
    def _init_log(self):
        logdir = chk_make_subdir(self.basedir_logfiles, 
                                 datetime.today().strftime('%Y%m%d'))
        if self.start is None:
            start_str = 'ModelStart'
        else:
            start_str = to_datestring_YYYYMMDD(self.start)
    
        if self.stop is None:
            if isinstance(self.start, int): #is year
                stop_str = to_datestring_YYYYMMDD(self.start + 1)
            else:
                stop_str = 'None'
        else:
            stop_str = to_datestring_YYYYMMDD(self.stop)
        
        fname = ('result_log_{}_{}_{}.txt'
                 .format(self.obs_id, start_str, stop_str))
        self._log = log = open(os.path.join(logdir, fname), 'w+')
        log.write('Analysis configuration\n')
        for k, v in self._setup.items():
            if k == 'model_id':
                continue
            else:
                log.write('{}: {}\n'.format(k, v))
        
    def _close_log(self):
        if self._log is not None:
            self._log.close()
            self._log = None
        
    def _coldata_save_name(self, model_data, ts_type_ana, start=None,
                           stop=None):
        """Based on current setup, get savename of colocated data file
        """
        if start is None:
            start = model_data.start
        else:
            start = to_pandas_timestamp(start)    
        if stop is None:
            stop = model_data.stop
        else:
            stop = to_pandas_timestamp(stop)
        
        start_str = to_datestring_YYYYMMDD(start)
        stop_str = to_datestring_YYYYMMDD(stop)
        ts_type_src = model_data.ts_type
        coll_data_name = ColocatedData._aerocom_savename(model_data.var_name,
                                                          self.obs_id, 
                                                          self.model_id, 
                                                          ts_type_src, 
                                                          start_str, 
                                                          stop_str, 
                                                          ts_type_ana, 
                                                          self.filter_name)
        return coll_data_name + '.nc'
    
    def output_dir(self, task_name):
        """Output directory for colocated data"""
        return self._output_dirs[task_name]
    
    def _check_coldata_exists(self, model_id, coldata_save_name):
        """Check if colocated data file exists"""
        folder = os.path.join(self.output_dir('colocate'),
                              model_id)
        if not os.path.exists(folder):
            return False
        files = os.listdir(folder)
        if coldata_save_name in files:
            return True
        return False
    
    def run(self, model_ids=None):
        """Run current analysis
        
        For analysis parameters, see :class:`ColocationSetup`, for analysis tasks
        see :class:`_AnalysisTasks`, for analysis options see 
        :class:`_ColocationOptions`
        """
        if model_ids is None:
            if self.model_id is None:
                raise AttributeError('Model ID is not set')
            model_ids = [self.model_id]
        elif isinstance(model_ids, str):
            model_ids = [model_ids]
            
        self._init_log()
        for model_id in model_ids:
            self._log.write('\n\nModel: {}\n'.format(model_id))
            self.model_id = model_id
            try:
                if self.obs_id in self._UNGRIDDED_IDS:
                    self._run_gridded_ungridded()
                        
                else:
                    self._run_gridded_gridded()
            except:
                self._log.write('Failed to perform analysis: {}\n'
                                .format(traceback.format_exc()))
                if self.options.RAISE_EXCEPTIONS:
                    self._close_log()
                    raise Exception(traceback.format_exc())
        self._close_log()
        
    def _run_gridded_ungridded(self):
        """Analysis method for gridded vs. ungridded data"""
        start, stop = self.start, self.stop
        model_reader = ReadGridded(self.model_id, start, stop)
        
        obs_reader = ReadUngridded(self.obs_id)
        obs_vars = obs_reader.get_reader(self.obs_id).PROVIDES_VARIABLES
    
        obs_vars = self.obs_vars
        if obs_vars is None:
            obs_vars = model_reader.vars_provided
            
        var_matches = {}
        
        for var in obs_vars:
            if var in model_reader.vars_provided: #candidate
                if var in self.model_alt_vars:
                    if self.model_alt_vars[var] in obs_vars:
                        var_matches[var] = self.model_alt_vars[var]
                else:
                    if var in obs_vars:
                        var_matches[var] = var
        
        if len(var_matches) == 0:
            
            raise DataCoverageError('No variable matches between '
                                    '{} and {} for input vars: {}'
                                    .format(self.model_id, 
                                            self.obs_id, 
                                            self.obs_vars))
            
        all_ts_types = const.GRID_IO.TS_TYPES
        ts_types_ana = self.ts_types_ana
        if ts_types_ana is None:
            ts_types_ana = self._setup.TS_TYPES_ANA_DEFAULT['ungridded']
        
        ts_types_read = self.ts_types_read
        if ts_types_read is None:
            ts_types_read = model_reader.ts_types
        
        
        vars_model = list(var_matches.keys())
        vars_obs = list(var_matches.values())
        
        obs_data = obs_reader.read(datasets_to_read=self.obs_id, 
                                   vars_to_retrieve=vars_obs)
        
        for ts_type_read in ts_types_read:
            model_data_vars = model_reader.read(vars_model, 
                                                start=start,
                                                stop=stop,
                                                ts_type=ts_type_read,
                                                flex_ts_type=False)
                        
            if len(model_data_vars)==0:
                if self._log:    
                    self._log.write('No model data available ({}-{}, {})\n'
                                    .format(start, stop, ts_type_read))
                continue
            
            for model_data in model_data_vars:
                var = model_data.var_info.var_name
                obs_var = var_matches[var]
                if not obs_var in obs_reader.data:
                    if self._log:    
                        self._log.write('No obs data available for variable {} '
                                        '({}-{}, {})\n'
                                        .format(obs_var, start, stop, 
                                                ts_type_read))
                    continue
                for ts_type_ana in ts_types_ana:
    
                    if all_ts_types.index(ts_type_ana) >= all_ts_types.index(ts_type_read):
                    
                        out_dir = chk_make_subdir(self.output_dir('colocate'),
                                                  self.model_id)
                        savename = self._coldata_save_name(model_data,
                                                           ts_type_ana, 
                                                           start,
                                                           stop)
                        file_exists = self._check_coldata_exists(
                                                            self.model_id, 
                                                            savename)
                        if file_exists:
                            if not self.options.REANALYSE_EXISTING:
                                if self._log:
                                    self._log.write('SKIP: {}\n'
                                                    .format(savename))
                                    print_log.info('Skip {} (file already '
                                                   'exists)'.format(savename))
                                continue
                            else:
                                os.remove(os.path.join(out_dir, savename))
                        
                        data_coll = colocate_gridded_ungridded_2D(
                                                model_data, obs_data, 
                                                ts_type=ts_type_ana, 
                                                start=start, stop=stop,
                                                var_ref=obs_var,
                                                filter_name=self.filter_name)
                        self._last_coldata = data_coll
                        data_coll.to_netcdf(out_dir)
                        if self._log:
                            self._log.write('WRITE: {}\n'.format(savename))
                            print_log.info('Writing {}'.format(savename))
                        
                        plt.close('all')
                    
    def _run_gridded_gridded(self):
    
        start, stop = self.start, self.stop
        model_reader = ReadGridded(self.model_id, start, stop)
        obs_reader = ReadGridded(self.obs_id, start, stop)
    
        obs_vars = self.obs_vars
        if obs_vars is None:
            obs_vars = model_reader.vars_provided
            
        var_matches = {}
        for var in obs_vars:
            if var in model_reader.vars_provided: #candidate
                # first check if the variable pair was defined explicitely
                if var in self.model_alt_vars:
                    if self.model_alt_vars[var] in obs_reader.vars_provided:
                        var_matches[var] = self.model_alt_vars[var]
                else:
                    if var in obs_reader.vars_provided:
                        var_matches[var] = var
        
        if len(var_matches) == 0:
            raise DataCoverageError('No variable matches between {} and {} for '
                                    'input vars: {}'.format(self.model_id, 
                                                            self.obs_id, 
                                                            self.obs_vars))
            
        all_ts_types = const.GRID_IO.TS_TYPES
        ts_types_ana = self.ts_types_ana
        if ts_types_ana is None:
            ts_types_ana = self._setup.TS_TYPES_ANA_DEFAULT['gridded']
        
        ts_types_read = self.ts_types_read
        if ts_types_read is None:
            ts_types_read = model_reader.ts_types
        
        vars_model = list(var_matches.keys())
        vars_obs = list(var_matches.values())
        flex_obs = self._setup.options.TS_TYPE_OBS_FLEX
        for ts_type_read in ts_types_read:
            # reads only year if starttime is provided but not stop time
            model_data_vars = model_reader.read(vars_model, 
                                                start=start,
                                                stop=stop,
                                                ts_type=ts_type_read,
                                                flex_ts_type=False)
            
            if len(model_data_vars) == 0:
                if self._log:    
                    self._log.write('No model data available ({}-{}, {})\n'
                                    .format(start, stop, ts_type_read))
                continue
            
            obs_data_vars = obs_reader.read(vars_obs, 
                                            start=start,
                                            stop=stop,
                                            ts_type=ts_type_read,
                                            flex_ts_type=flex_obs)
            if len(obs_data_vars) == 0:
                if self._log:    
                    self._log.write('No obs data available for variables {} '
                                    '({}-{}, {})\n'
                                    .format(vars_obs, start, stop, 
                                            ts_type_read))
                continue
            
            for model_data in model_data_vars:
                var = model_data.var_name
                obs_data = None
                for _obs in obs_data_vars:
                    if _obs.var_name == var_matches[var]:
                        obs_data = _obs
                        break
                if obs_data is None:
                    if self._log:    
                        self._log.write('No obs data available for model var {} '
                                        '({}-{}, {})\n'
                                        .format(var, start, stop, 
                                            ts_type_read))
                    continue
                for ts_type_ana in ts_types_ana:
                    # model resolution (ts_type) must be equal or higher 
                    # than the current analysis setting (since )
                    if all_ts_types.index(ts_type_ana) >= all_ts_types.index(ts_type_read):
                        out_dir = chk_make_subdir(self.output_dir('colocate'),
                                                  self.model_id)
                                                  
                        savename = self._coldata_save_name(model_data,
                                                           ts_type_ana, 
                                                           start,
                                                           stop)
                        
                        file_exists = self._check_coldata_exists(self.model_id,
                                                                  savename)
                        if file_exists:
                            if not self.options.REANALYSE_EXISTING:
                                if self._log:
                                    self._log.write('SKIP: {}\n'.format(savename))
                                    print_log.info('Skip {} (file already '
                                                   'exists)'.format(savename))
                                continue
                            else:
                                os.remove(os.path.join(out_dir, savename))
                            
                        data_coll = colocate_gridded_gridded(
                                        model_data, obs_data, 
                                        ts_type=ts_type_ana, 
                                        start=start, stop=stop, 
                                        filter_name=self.filter_name)
                        self._last_coldata = data_coll
                        if data_coll.save_name_aerocom + '.nc' != savename:
                            raise Exception
                        data_coll.to_netcdf(out_dir)
                        if self._log:
                            self._log.write('WRITE: {}\n'.format(savename))
                            print_log.info('Writing {}'.format(savename))
    
    def __getitem__(self, key):
        if key in self._setup:
            return self._setup[key]
        raise AttributeError('Invalid attr. for ColocationSetup')
        
    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        elif key in self._setup:
            return self._setup[key]
        
    def __dir__(self):
        return list(self._setup.keys()) + super().__dir__()
    
    def __setitem__(self, key, val):
        if not key in self._setup:
            raise AttributeError('Invalid attr. for ColocationSetup')
            self._setup[key] = val
            
            
    def __call__(self, **kwargs):
        raise NotImplementedError
        self.update(**kwargs)
        self.run()
        
if __name__ == '__main__':
    model_alt_vars = dict(scatc550dryaer  = 'ec550dryaer',
                          absc550aer      = 'abs5503Daer')
    
    stp = ColocationSetup(model_id = 'CAM5.3-Oslo_AP3-CTRL2016-PD',
                          obs_id='EBASMC',
                          obs_vars=['scatc550dryaer', 'absc550aer'], 
                          start=2010,
                          model_alt_vars=model_alt_vars,
                          read_opts=dict(station_names='Alert'))
    stp.run()
    
            