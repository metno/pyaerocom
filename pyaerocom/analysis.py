#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
High level module containing analysis classes and methods to perform 
colocation.

.. note::
    
    This is a development module and may undergo significant, non-backwards 
    compatible changes in the near future (date: 21.9.2018)
"""
import os
import numpy as np
from functools import reduce
import matplotlib.pyplot as plt

from pyaerocom._lowlevel_helpers import BrowseDict, chk_make_subdir
from pyaerocom import Filter, const
from pyaerocom.helpers import (to_pandas_timestamp, to_datestring_YYYYMMDD,
                               start_stop_from_year)
from pyaerocom.colocation import (colocate_gridded_gridded,
                                  colocate_gridded_ungridded_2D)
from pyaerocom import ColocatedData
from pyaerocom.io import ReadUngridded, ReadGridded
from pyaerocom.exceptions import NetworkNotSupported, DataCoverageError

class _AnalysisTasks(BrowseDict):
    """This class contains available Aerocom analysis tasks
    
    Note
    ----
    
    
    Attributes
    ----------
    
    """
    _TASKS_AVAIL = ['colocate']
    _NAMES_OUTPUT_DIRS = {'colocate'           :   'colocated_data',
                          'plot_maps'           :   'maps',
                          'plot_scatter'        :   'scatter',
                          'plot_stat_tseries'   :   'stat_tseries'}
    def __init__(self, colocate=True, plot_maps=False,
                 plot_scatter=False, plot_stat_tseries=False):
        self.colocate = colocate
        self.plot_maps = plot_maps
        self.plot_scatter = plot_scatter
        self.plot_stat_tseries = plot_stat_tseries
    
            
class _AnalysisOptions(BrowseDict):
    """This class contains options for Aerocom analysis
    """
    def __init__(self, REANALYSE_EXISTING=False, ONLY_FIRST=False,
                 RAISE_EXCEPTIONS=False):
        
        self.REANALYSE_EXISTING = REANALYSE_EXISTING
        self.ONLY_FIRST = ONLY_FIRST
        self.RAISE_EXCEPTIONS = RAISE_EXCEPTIONS
    
class _TS_TYPESetup(BrowseDict):
    """Dict-like class that handles which ts_types are analysed for a scenario
    
    
    """
    def __init__(self, *args, **kwargs):
        self.read_alt = {}
        super(_TS_TYPESetup, self).__init__(*args, **kwargs)
        
    def __str__(self):
        s ='ts_type settings (<read>: <analyse>)\n'
        for key, val in self.items():
            if key == 'read_alt':
                continue
            s+=' {}:{}\n'.format(key, val)
        if self['read_alt']:
            s+=' Alternative ts_types (read)\n'
            for key, val in self['read_alt'].items():
                s+='   {}:{}\n'.format(key, val)
           
            
class AnalysisSetup(BrowseDict):
    """Setup class for model / obs intercomparison
    
    An instance of this setup class can be used to run a colocation analysis
    between a model and an observation network and will create a number of 
    :class:`pya.ColocatedData` instances and save them as netCDF file.
    
    Note
    ----
    This is a very first draft and may change
    
    Attributes
    ----------
    vars_to_analyse : list
        variables to be analysed (should be available in model and obs data)
    
    Todo
    ----
    Complete docstring
    """
    def __init__(self, vars_to_analyse=None, model_id=None, obs_id=None, 
                 years=None, filter_name='WORLD-noMOUNTAINS',
                 ts_type_setup=None, out_basedir=None, 
                 init_dirs=True, **tasks_or_opts):
        
        if ts_type_setup is None:
            ts_type_setup = dict(monthly=['monthly', 'yearly'],
                                 daily = ['monthly', 'yearly'])
        try:
            Filter(filter_name)
        except:
            raise ValueError('Invalid input for filter_name')
        if out_basedir is None:
            out_basedir = const.OUT_BASEDIR
            
        self.vars_to_analyse = vars_to_analyse
        
        self.model_id = model_id
        self.obs_id = obs_id
        
        if not isinstance(ts_type_setup, _TS_TYPESetup):
            ts_type_setup = _TS_TYPESetup(**ts_type_setup)
        
        self.tasks = _AnalysisTasks()
        self.options = _AnalysisOptions()
        
        self.ts_type_setup = ts_type_setup
        self.years = years
        
        self.out_basedir = out_basedir
        self._output_dirs = {}
        self.update(**tasks_or_opts)
        if init_dirs:
            self._check_create_output_dirs()
        else:
            for key in self.tasks:
                self._output_dirs[key] = None
    
    def _check_create_output_dirs(self):
        """Create subdirectories for analysis output"""
        dirnames = self.tasks._NAMES_OUTPUT_DIRS 
        base = self.out_basedir
        for task, name in dirnames.items():
            self._output_dirs[task] = chk_make_subdir(base, name)
        return self._output_dirs
            
    def __dir__(self):
        return self.keys()
    
    def update(self, **kwargs):
        for key, val in kwargs.items():
            if key in self.tasks:
                self.tasks[key] = val
            elif key in self.options:
                self.options[key] = val
            else:
                self[key] = val


class Analyser(AnalysisSetup):
    """High level class for running analysis
    
    Inherits from :class:`AnalysisSetup`
    
    TODO
    ----
    - Implement more flexible handling of time intervals for analysis
    - write docstring
    """
    def __init__(self, *args, **kwargs):
        super(self, Analyser).__init__(*args, **kwargs)
        self._log = None
       
    def _init_log(self):
        self._log = log = open('output/result_log_{}.csv'
                               .format(self.obs_id), 'w+')
        log.write('Analysis configuration\n')
        for k, v in stp.items():
            if k == 'model_id':
                continue
            elif k == 'ts_type_setup':
                log.write('TS_TYPES (<read>: <analyse>)\n')
                for key, val in v.items():
                    if key == 'read_alt':
                        continue
                    log.write(' {}:{}\n'.format(key, val))
                if v['read_alt']:
                    log.write(' Alternative TS_TYPES (read)\n')
                    for key, val in v['read_alt'].items():
                        log.write('   {}:{}\n'.format(key, val))
            else:
                log.write('{}: {}\n'.format(k, v))
        
    def _close_log(self):
        if self.log is not None:
            self._log.close()
            self._log = None
            
    def _prepare_ts_types(self, model_reader):
        """Prep. ts_types for analysis based on what is available in model data
        
        Parameters
        ----------
        model_reader : ReadGridded
            instance of model reader class
        
        """
        ts_type_setup = self.ts_type_setup
        ts_type_read = list(ts_type_setup.keys())
        ts_type_matches = list(np.intersect1d(ts_type_read, 
                                              model_reader.ts_types))
        if 'read_alt' in ts_type_setup:
            ts_type_read_alt = ts_type_setup.read_alt
            for ts_type, ts_types_alt in ts_type_read_alt.items():
                if not ts_type in ts_type_matches:
                    for ts_type_alt in ts_types_alt:
                        if ts_type_alt in model_reader.ts_types:
                            ts_type_matches.append(ts_type_alt)
                            ts_type_setup[ts_type_alt] = ts_type_setup[ts_type]
                            break
        return (ts_type_matches, ts_type_setup)
   

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
        
        For analysis parameters, see :class:`AnalysisSetup`, for analysis tasks
        see :class:`_AnalysisTasks`, for analysis options see 
        :class:`_AnalysisOptions`
        """
        if model_ids is None:
            if self.model_id is None:
                raise AttributeError('Model ID is not set')
            model_ids = [model_ids]
        elif not isinstance(model_ids, (list, tuple, np.ndarray)):
            model_ids = list(model_ids)
            
        self._init_log()
        for model_id in model_ids:
            self.model_id = model_id
            try:
                ReadUngridded(self.obs_id)
                self._run_gridded_ungridded()
                
            except NetworkNotSupported:
                self._run_gridded_gridded()
        self._close_log()
        
    def _run_gridded_ungridded(self):
        """Analysis method for gridded vs. ungridded data"""
        obs_reader = ReadUngridded()
        obs_data = obs_reader.read(self.obs_id, self.vars_to_analyse)
        
        ts_types = const.GRID_IO.TS_TYPES
        
            
        model_reader = ReadGridded(self.model_id)
        
        var_matches = list(reduce(np.intersect1d, (self.vars_to_analyse, 
                                                   model_reader.vars_provided,
                                                   obs_data.contains_vars)))
        
        if len(var_matches) == 0:
            raise DataCoverageError('No variable matches between '
                                    '{} and {} for input vars: {}'
                                    .format(self.model_id, 
                                            self.obs_id, 
                                            self.vars_to_analyse))
        
        year_matches = list(np.intersect1d(self.years, model_reader.years))
        if len(year_matches) == 0:
            raise DataCoverageError('No year matches between {} and {} for '
                                    'input vars: {}'.format(self.model_id, 
                                                 self.obs_id, 
                                                 self.vars_to_analyse))
        ts_type_matches, ts_type_setup = self._prepare_ts_types(model_reader)            
        if len(ts_type_matches) == 0:
            raise DataCoverageError('No ts_type matches between {} and {} for '
                                    'input vars: {}'.format(self.model_id, 
                                                            self.obs_id, 
                                                            self.vars_to_analyse))
        
                    
        for year in year_matches:
            start, stop = start_stop_from_year(year)
            for ts_type in ts_type_matches:
                ts_types_ana = ts_type_setup[ts_type]
                model_reader.read(var_matches, 
                                  start=year,
                                  ts_type=ts_type,
                                  flex_ts_type=False)
                            
                if len(model_reader.data) == 0:
                    if self._log:    
                        self._log.write('No model data available ({}, {})\n'
                                        .format(year, ts_type))
                    continue
                
                for var, model_data in model_reader.data.items():
                    if not var in obs_reader.data:
                        if self._log:    
                            self._log.write('No obs data available ({}, {})\n'
                                            .format(year, ts_type))
                        continue
                    for ts_type_ana in ts_types_ana:
                        if ts_types.index(ts_type_ana) >= ts_types.index(ts_type):
                        
                            out_dir = self.output_dir('colocate')
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
                                    continue
                                else:
                                    os.remove(os.path.join(out_dir, savename))
                            
                            data_coll = colocate_gridded_ungridded_2D(
                                                    model_data, obs_data, 
                                                    ts_type=ts_type_ana, 
                                                    start=start, stop=stop,
                                                    filter_name=self.filter_name)
                                
                            data_coll.to_netcdf(out_dir)
                            if self._log:
                                self._log.write('WRITE: {}\n'.format(savename))
                            
                            plt.close('all')
                        
    def _run_gridded_gridded(self):
    
        ts_types = const.GRID_IO.TS_TYPES
            
        model_reader = ReadGridded(self.model_id)
        obs_reader = ReadGridded(self.obs_id)
    
        var_matches = list(reduce(np.intersect1d, (self.vars_to_analyse, 
                                                   model_reader.vars_provided,
                                                   obs_reader.vars)))
        
        if len(var_matches) == 0:
            raise DataCoverageError('No variable matches between {} and {} for '
                                    'input vars: {}'.format(self.model_id, 
                                                            self.obs_id, 
                                                            self.vars_to_analyse))
        
        year_matches = list(reduce(np.intersect1d, (self.years, 
                                                    model_reader.years,
                                                    obs_reader.years)))
        
        if len(year_matches) == 0:
            raise DataCoverageError('No year matches between {} and {} for '
                                    'input vars: {}'.format(self.model_id, 
                                                            self.obs_id, 
                                                            self.vars_to_analyse))
            
        
        ts_type_matches, ts_type_setup = self._prepare_ts_types(model_reader)            
        if len(ts_type_matches) == 0:
            raise DataCoverageError('No ts_type matches between '
                                                   '{} and {} for input vars: {}'
                                                   .format(self.model_id, 
                                                           self.obs_id, 
                                                           self.vars_to_analyse))
        
                    
        for year in year_matches:
            start, stop = start_stop_from_year(year)
            for ts_type in ts_type_matches:
                ts_types_ana = ts_type_setup[ts_type]
                # reads only year if starttime is provided but not stop time
                model_reader.read(var_matches, 
                                  start=year,
                                  ts_type=ts_type,
                                  flex_ts_type=False)
                
                obs_reader.read(var_matches, start=year,
                                ts_type = ts_type,
                                flex_ts_type=True)
                
                if len(model_reader.data) == 0:
                    if self._log:    
                        self._log.write('No model data available ({}, {})\n'.format(year, 
                                      ts_type))
                    continue
                
                for var, model_data in model_reader.data.items():
                    if not var in obs_reader.data:
                        if self._log:    
                            self._log.write('No obs data available ({}, {})\n'
                                            .format(year, ts_type))
                        continue
                    for ts_type_ana in ts_types_ana:
                        if ts_types.index(ts_type_ana) >= ts_types.index(ts_type):
                            obs_data = obs_reader.data[var]
                            out_dir = self.output_dir('colocate')
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
                                    continue
                                else:
                                    os.remove(os.path.join(out_dir, savename))
                                
                            data_coll = colocate_gridded_gridded(
                                            model_data, obs_data, 
                                            ts_type=ts_type_ana, 
                                            start=start, stop=stop, 
                                            filter_name=self.filter_name)
                                
                            if data_coll.save_name_aerocom + '.nc' != savename:
                                raise Exception
                            data_coll.to_netcdf(out_dir)
                            save_name_fig = data_coll.save_name_aerocom + '_SCAT.png'
                            if self._log:
                                self._log.write('WRITE: {}\n'.format(savename))
                                
                            data_coll.plot_scatter(savefig=True, 
                                               save_dir=dirs['scatter_plots'],
                                               save_name=save_name_fig)
                            plt.close('all')
                            
    def __call__(self, **kwargs):
        self.update(**kwargs)
        self.run()
if __name__ == '__main__':
    
    stp = AnalysisSetup(['od550aer', 'ec550aer'], 
                        model_id='bla', obs_id='blub',
                        years=[2010, 2016, 2017],
                        filter_name='europe')
                