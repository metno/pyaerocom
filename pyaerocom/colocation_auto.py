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
import traceback
from datetime import datetime

from pyaerocom._lowlevel_helpers import BrowseDict, chk_make_subdir
from pyaerocom import Filter, const
from pyaerocom.helpers import (to_pandas_timestamp, to_datestring_YYYYMMDD)
from pyaerocom.io.helpers import get_all_supported_ids_ungridded
from pyaerocom.colocation import (colocate_gridded_gridded,
                                  colocate_gridded_ungridded)
from pyaerocom import ColocatedData, print_log
from pyaerocom.io import ReadUngridded, ReadGridded
from pyaerocom.exceptions import (DataCoverageError,
                                  TemporalResolutionError)
         
class _ColocationOptions(BrowseDict):
    """This class contains options for Aerocom analysis
    """
    def __init__(self, REANALYSE_EXISTING=False, RAISE_EXCEPTIONS=False):
        self.REANALYSE_EXISTING = REANALYSE_EXISTING,
        self.RAISE_EXCEPTIONS = RAISE_EXCEPTIONS
                   
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
        specified in :attr:`model_use_vars` and which can be specified in form of a 
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
    
    
    def __init__(self, model_id=None, obs_id=None, obs_vars=None, 
                 start=None, stop=None, ts_type='daily',
                 filter_name='WORLD-noMOUNTAINS', 
                 model_use_vars=None, basedir_coldata=None, read_opts=None,
                 colocation_opts=None):
        if read_opts is None:
            read_opts = {}
        if colocation_opts is None:
            colocation_opts = {}
        if isinstance(obs_vars, str):
            obs_vars = [obs_vars]
        if model_use_vars is None: 
            model_use_vars = {}
        try:
            Filter(filter_name)
        except:
            raise ValueError('Invalid input for filter_name')
        if basedir_coldata is None:
            basedir_coldata = const.COLOCATEDDATADIR
        if not os.path.exists(basedir_coldata):
            const.print_log.info('Creating directory: {}'.format(basedir_coldata))
            os.mkdir(basedir_coldata)
            
        const.print_log.info('Output directory for colocated data:\n '
                             '{}'.format(basedir_coldata))
        const.print_log.info('Output directory for logfiles:\n '
                             '{}'.format(basedir_coldata))
        self.obs_vars = obs_vars
        
        self.model_use_vars = model_use_vars
        
        self.model_id = model_id
        self.obs_id = obs_id
    
        self.options = _ColocationOptions()

        
        self.start = start
        self.stop = stop
        
        self.ts_type = ts_type
        
        self.filter_name = filter_name
        
        self.basedir_coldata = basedir_coldata
        
        self.colocation_opts = colocation_opts
        self.read_opts = read_opts
        #self.read_opts.update(**read_opts)
     
    @property
    def basedir_logfiles(self):
        p = chk_make_subdir(self.basedir_coldata, 'logfiles')
        return p
    
    @property
    def UNGRIDDED_IDS(self):
        """ID's of all supported ungridded datasets"""
        return get_all_supported_ids_ungridded()
    
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
        self.data = {}
        self._ungridded_reader = ReadUngridded()
        
    def _init_log(self):
        logdir = chk_make_subdir(self._setup.basedir_logfiles, 
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
        
    def _coldata_savename(self, model_data, start=None, stop=None, 
                           ts_type=None):
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
        if ts_type is None:
            ts_type = model_data.ts_type
        
        start_str = to_datestring_YYYYMMDD(start)
        stop_str = to_datestring_YYYYMMDD(stop)
        ts_type_src = model_data.ts_type
        coll_data_name = ColocatedData._aerocom_savename(var_name=model_data.var_name,
                                                         obs_id=self.obs_id, 
                                                         model_id=model_data.data_id, 
                                                         ts_type_src=ts_type_src, 
                                                         start_str=start_str, 
                                                         stop_str=stop_str, 
                                                         ts_type=ts_type,
                                                         filter_name=self.filter_name)
        return coll_data_name + '.nc'
    
    def output_dir(self, task_name):
        """Output directory for colocated data"""
        return self._output_dirs[task_name]
    
    def _check_coldata_exists(self, model_id, coldata_savename):
        """Check if colocated data file exists"""
        folder = os.path.join(self.basedir_coldata,
                              model_id)
        if not os.path.exists(folder):
            return False
        files = os.listdir(folder)
        if coldata_savename in files:
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
                if self.obs_id in self._setup.UNGRIDDED_IDS:
                    self.data[self.model_id] = self._run_gridded_ungridded()
                        
                else:
                    self.data[self.model_id] = self._run_gridded_gridded()
            except:
                msg = ('Failed to perform analysis: {}\n'
                       .format(traceback.format_exc()))
                const.print_log.warning(msg)
                self._log.write(msg)
                if self.options.RAISE_EXCEPTIONS:
                    self._close_log()
                    raise Exception(traceback.format_exc())
        self._close_log()
        
    def _run_gridded_ungridded(self):
        """Analysis method for gridded vs. ungridded data"""
        start, stop = self.start, self.stop
        model_reader = ReadGridded(self.model_id, start, stop)
        
        obs_reader = ReadUngridded(self.obs_id)
        
        obs_vars = self.obs_vars
        
        obs_vars_avail = obs_reader.get_reader(self.obs_id).PROVIDES_VARIABLES
        
        for obs_var in obs_vars:
            if not obs_var in obs_vars_avail:
                raise DataCoverageError('Variable {} is not supported by {}'
                                        .format(obs_var, self.obs_id))
            
        var_matches = {}
        
        for obs_var in obs_vars:
            if obs_var in self.model_use_vars:
                model_var = self.model_use_vars[obs_var]
            else:
                model_var = obs_var
            
            if not model_var in model_reader.vars_provided:
                continue
            var_matches[obs_var] = model_var
        
        if len(var_matches) == 0:
            
            raise DataCoverageError('No variable matches between '
                                    '{} and {} for input vars: {}'
                                    .format(self.model_id, 
                                            self.obs_id, 
                                            self.obs_vars))
            
        all_ts_types = const.GRID_IO.TS_TYPES
        
        read_opts = self.read_opts
        rmo = False
        if 'remove_outliers' in read_opts:
            rmo = read_opts.pop('remove_outliers')
# =============================================================================
#         datalevel = None
#         if 'datalevel' in read_opts:
#             datalevel = read_opts.pop('datalevel')
# =============================================================================
        obs_data = obs_reader.read(datasets_to_read=self.obs_id, 
                                   vars_to_retrieve=list(var_matches),
                                   **read_opts)
        
        ts_type = self.ts_type
        
        if self.ts_type is None:
            raise Exception
        
        data_objs = {}
        
        for obs_var, model_var in var_matches.items():
            if rmo is True:
                obs_data.remove_outliers(obs_var, inplace=True,
                                         move_to_trash=False)
                
            print_log.info('Running {} / {} ({}, {})'.format(self.model_id, 
                                                             self.obs_id, 
                                                             model_var, 
                                                             obs_var))
            model_data = model_reader.read_var(model_var, start=start,
                                               stop=stop, ts_type=ts_type,
                                               flex_ts_type=True)
            if not model_data.ts_type in all_ts_types:
                raise TemporalResolutionError('Invalid temporal resolution {} '
                                              'in model {}'.format(model_data.ts_type,
                                                                   self.model_id))
                
            ts_type_src = model_data.ts_type
            if all_ts_types.index(ts_type) < all_ts_types.index(ts_type_src):
                print_log.info('Updating ts_type from {} to {} (highest '
                               'available in model {})'.format(ts_type, 
                                                               ts_type_src,
                                                               self.model_id))
                ts_type = ts_type_src
            
    
            out_dir = chk_make_subdir(self.basedir_coldata,
                                      self.model_id)
            savename = self._coldata_savename(model_data,
                                               start,
                                               stop,
                                               ts_type)
            
            file_exists = self._check_coldata_exists(model_data.data_id, 
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
            
            coldata = colocate_gridded_ungridded(gridded_data=model_data, 
                                                 ungridded_data=obs_data, 
                                                 ts_type=ts_type, 
                                                 start=start, stop=stop,
                                                 var_ref=obs_var,
                                                 filter_name=self.filter_name,
                                                 **self.colocation_opts)
            coldata.to_netcdf(out_dir)
            if self._log:
                self._log.write('WRITE: {}\n'.format(savename))
                print_log.info('Writing file {}'.format(savename))
            data_objs[model_var] = coldata
        return data_objs
    
    @staticmethod 
    def get_lowest_resolution(ts_type, *ts_types):
        all_ts_types = const.GRID_IO.TS_TYPES
        lowest = ts_type
        for freq in ts_types:
            if all_ts_types.index(lowest) < all_ts_types.index(freq):
                lowest = freq
        return lowest
            
    def _run_gridded_gridded(self):
        start, stop = self.start, self.stop
        model_reader = ReadGridded(self.model_id, start, stop)
        obs_reader = ReadGridded(self.obs_id, start, stop)
    
        obs_vars = self.obs_vars
        
        obs_vars_avail =  obs_reader.vars_provided
        
        for obs_var in obs_vars:
            if not obs_var in obs_vars_avail:
                raise DataCoverageError('Variable {} is not supported by {}'
                                        .format(obs_var, self.obs_id))
        var_matches = {}
        
        for obs_var in obs_vars:
            if obs_var in self.model_use_vars:
                model_var = self.model_use_vars[obs_var]
            else:
                model_var = obs_var
            
            if not model_var in model_reader.vars_provided:
                raise DataCoverageError('Variable {} not found in model data {}'
                                        .format(model_var, self.model_id))
            var_matches[obs_var] = model_var
                
        if len(var_matches) == 0:
            raise DataCoverageError('No variable matches between '
                                    '{} and {} for input vars: {}'
                                    .format(self.model_id, 
                                            self.obs_id, 
                                            self.obs_vars))
            
        all_ts_types = const.GRID_IO.TS_TYPES
        
        ts_type = self.ts_type
        
        if self.ts_type is None:
            raise Exception
        
        data_objs = {}
        
        for obs_var, model_var in var_matches.items():
            print_log.info('Running {} / {} ({}, {})'.format(self.model_id, 
                                                             self.obs_id, 
                                                             model_var, 
                                                             obs_var))
            
            model_data = model_reader.read_var(model_var, start=start,
                                               stop=stop, 
                                               ts_type=ts_type,
                                               flex_ts_type=True)
            
            if not model_data.ts_type in all_ts_types:
                raise TemporalResolutionError('Invalid temporal resolution {} '
                                              'in model {}'.format(model_data.ts_type,
                                                                   self.model_id))
            obs_data  = obs_reader.read_var(obs_var, 
                                            start=start,
                                            stop=stop,
                                            ts_type=ts_type,
                                            flex_ts_type=True)
            
            if not obs_data.ts_type in all_ts_types:
                raise TemporalResolutionError('Invalid temporal resolution {} '
                                              'in obs {}'.format(obs_data.ts_type,
                                                                 self.model_id))
            
            lowest = self.get_lowest_resolution(ts_type, model_data.ts_type,
                                                obs_data.ts_type)
            if lowest != ts_type:
                print_log.info('Updating ts_type from {} to {} (highest '
                               'available in {} / {} combination)'
                               .format(ts_type, lowest, self.model_id,
                                       self.obs_id))
                ts_type = lowest
                 
            out_dir = chk_make_subdir(self.basedir_coldata,
                                      self.model_id)
                           
            savename = self._coldata_savename(model_data,
                                              start,
                                              stop,
                                              ts_type)
            
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
                
            coldata = colocate_gridded_gridded(gridded_data=model_data,
                                               gridded_data_ref=obs_data, 
                                               ts_type=ts_type, 
                                               start=start, stop=stop, 
                                               filter_name=self.filter_name,
                                               **self.colocation_opts)
            coldata.to_netcdf(out_dir)
            if self._log:
                self._log.write('WRITE: {}\n'.format(savename))
                print_log.info('Writing file {}'.format(savename))
            data_objs[model_var] = coldata
        return data_objs
                    
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
    import matplotlib.pyplot as plt
    plt.close('all')
    
    model_use_vars = dict(scatc550dryaer  = 'ec550dryaer',
                          absc550aer      = 'abs5503Daer')
    
    MODEL_ID =  'CAM5.3-Oslo_AP3-CTRL2016-PD'
    stp = ColocationSetup(model_id = MODEL_ID,
                          obs_id='EBASMC',
                          obs_vars=list(model_use_vars), 
                          start=2010,
                          filter_name='WORLD-wMOUNTAINS',
                          model_use_vars=model_use_vars,
                          vert_scheme='surface',
                          read_opts=dict(station_names=['Jungfrau*',
                                                        'Zeppel*',
                                                        'Cape*Point*']))
    
    stp.options.RAISE_EXCEPTIONS = True
    stp.options.REANALYSE_EXISTING = True
    col = Colocator(stp)
    
    run = True
    if run:
        col.run()
        for model_id, vardict in col.data.items():
            for data in vardict.values():
                data.plot_scatter()
            
    else:
        from warnings import filterwarnings
        filterwarnings('ignore')
        import pyaerocom as pya
        model_vars = model_use_vars.values()
        
        r = pya.io.ReadGridded(MODEL_ID)
        
        
    
        for var in model_vars:
            d = r.read_var(var, start=2010, stop=None, ts_type='daily')
            print(d.ts_type)        
            
        obs = pya.io.ReadUngridded().read('EBASMC', list(model_use_vars),
                                          station_names='Jungfrau*')
        
                