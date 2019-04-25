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
from pyaerocom.helpers import (to_pandas_timestamp, to_datestring_YYYYMMDD,
                               get_lowest_resolution)
from pyaerocom.io.helpers import get_all_supported_ids_ungridded
from pyaerocom.colocation import (colocate_gridded_gridded,
                                  colocate_gridded_ungridded)
from pyaerocom import ColocatedData, print_log
from pyaerocom.io import ReadUngridded, ReadGridded
from pyaerocom.exceptions import (DataCoverageError,
                                  TemporalResolutionError)
                   
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
    ts_type 
        string specifying colocation frequency
    start 
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
    regrid_res_deg : :obj:`int`, optional
        resolution in degrees for regridding of model grid (done before 
        colocation)
    remove_outliers : bool
        if True, outliers are removed from model and obs data before colocation, 
        else not.
    vert_scheme : :obj:`str`, optional
        vertical scheme used for colocation
    harmonise_units : bool
        if True, units are attempted to be harmonised (note: raises Exception
        if True and units cannot be harmonised).    
    model_use_vars : :obj:`dict`, optional
        dictionary that specifies mapping of model variables. Keys are 
        observation variables, values are the corresponding model variables 
        (e.g. model_use_vars=dict(od550aer='od550csaer'))
    model_read_aux : :obj:`dict`, optional
        may be used to specify additional computation methods of variables from
        models. Keys are obs variables, values are dictionaries with keys 
        `vars_required` (list of required variables for computation of var 
        and `fun` (method that takes list of read data objects and computes
        and returns var)
    read_opts_ungridded : :obj:`dict`, optional
        dictionary that specifies reading constraints for ungridded reading
        (c.g. :class:`pyaerocom.io.ReadUngridded`).  
    obs_vert_type : :obj:`str` or :obj:`dict`, optional
        Aerocom vertical code encoded in the model filenames (only AeroCom 3 
        and later). Specifies which model file should be read in case there are
        multiple options (e.g. surface level data can be read from a 
        *Surface*.nc file as well as from a *ModelLevel*.nc file). If input is 
        string (e.g. 'Surface'), then the corresponding vertical type code is 
        used for reading of all variables that are colocated (i.e. that are 
        specified in :attr:`obs_vars`). Else (if input is dictionary, e.g. 
        `obs_vert_type=dict(od550aer='Column', ec550aer='ModelLevel')`), 
        information is extracted variable specific, for those who are defined
        in the dictionary, for all others, `None` is used.
    var_outlier_ranges : :obj:`dict`, optional
        dictionary specifying outlier ranges for individual variables. 
        (e.g. dict(od550aer = [-0.05, 10], ang4487aer=[0,4]))
    model_ts_type_read : :obj:`str` or :obj:`dict`, optional
        may be specified to explicitly define the reading frequency of the 
        model data. Not to be confused with :attr:`ts_type`, which specifies 
        the frequency used for colocation. Can be specified variable specific 
        by providing a dictionary.
    obs_ts_type_read : :obj:`str` or :obj:`dict`, optional
        may be specified to explicitly define the reading frequency of the 
        observation data (so far, this does only apply to gridded obsdata such
        as satellites). For ungridded reading, the frequency may be specified
        via :attr:`obs_id`, where applicable (e.g. AeronetSunV3Lev2.daily).
        Not to be confused with :attr:`ts_type`, which specifies the
        frequency used for colocation. Can be specified variable specific in
        form of dictionary.
    basedir_coldata : str
        base directory for storing of colocated data files
    save_coldata : bool
        if True, colocated data objects are saved as NetCDF file.
    """ 
    #: Dictionary specifying alternative vertical types that may be used to 
    #: read model data. E.g. consider the variable is  ec550aer, 
    #: obs_vert_type='Surface' and obs_vert_type_alt=dict(Surface='ModelLevel').
    #: Now, if a model that is used for the analysis does not contain a data 
    #: file for ec550aer at the surface ('*ec550aer*Surface*.nc'), then, the
    #: colocation routine will look for '*ec550aer*ModelLevel*.nc' and if this
    #: exists, it will load it and extract the surface level.
    OBS_VERT_TYPES_ALT = {'Surface'    :   'ModelLevel'}
    
    def __init__(self, model_id=None, obs_id=None, obs_vars=None, 
                 ts_type='daily', start=None, stop=None,
                 filter_name='WORLD-noMOUNTAINS', 
                 regrid_res_deg=None, remove_outliers=True,
                 vert_scheme=None, harmonise_units=False, 
                 model_use_vars=None, model_read_aux=None, 
                 read_opts_ungridded=None, obs_vert_type=None, 
                 var_outlier_ranges=None, model_ts_type_read=None, 
                 obs_ts_type_read=None, basedir_coldata=None, 
                 save_coldata=True):
        
        if isinstance(obs_vars, str):
            obs_vars = [obs_vars]
        try:
            Filter(filter_name)
        except:
            raise ValueError('Invalid input for filter_name')
        self.save_coldata = save_coldata
        if save_coldata:
            if basedir_coldata is None:
                basedir_coldata = const.COLOCATEDDATADIR
            if not os.path.exists(basedir_coldata):
                const.print_log.info('Creating directory: {}'.format(basedir_coldata))
                os.mkdir(basedir_coldata)
        
        self.obs_vars = obs_vars
        self.obs_vert_type = obs_vert_type
        self.read_opts_ungridded = read_opts_ungridded
        self.obs_ts_type_read = obs_ts_type_read
        
        self.model_use_vars = model_use_vars
        
        self.model_id = model_id
        self.obs_id = obs_id
        
        self.start = start
        self.stop = stop
        
        self.ts_type = ts_type
        
        self.filter_name = filter_name
        
        self.remove_outliers = remove_outliers
        self.var_outlier_ranges = var_outlier_ranges
        self.harmonise_units = harmonise_units
        self.vert_scheme = vert_scheme
        self.regrid_res_deg = regrid_res_deg
        
        self.basedir_coldata = basedir_coldata
    
        self.model_ts_type_read = model_ts_type_read
        self.model_read_aux = model_read_aux
        
        #: If True, existing colocated data files will be re-computed and overwritten
        self.reanalyse_existing = False
        #: If True, the colocation routine will raise any Exception that may occur, 
        #: else (False), expected expcetions will be ignored and logged.
        self.raise_exceptions = False
        
     
    @property
    def basedir_logfiles(self):
        """Base directory for storing logfiles"""
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
            if key in self and isinstance(self[key], dict):
                if not isinstance(val, dict):
                    raise ValueError('Cannot update dict {} with non-dict input {}'
                                     .format(key, val))
                self[key].update(val)
            else:
                self[key] = val

class Colocator(ColocationSetup):
    """High level class for running colocation
    
    Note
    ----
    This object inherits from :class:`ColocationSetup` and is also instantiated
    as such. For attributes, please see base class.
    """
    
    def __init__(self, **kwargs):
        super(Colocator, self).__init__(**kwargs)
    
        self._log = None
        self.data = {}
     
    def run(self, **opts):
        """Perform colocation for current setup
        
        The current setup comprises at least
        
        Parameters
        ----------
        **opts
            keyword args that may be specified to change the current setup
            before colocation
            
        """
        self.update(**opts)
        
        self._init_log()
        
        self._log.write('\n\nModel: {}\n'.format(self.model_id))
        try:
            if self.obs_id in self.UNGRIDDED_IDS:
                self.data[self.model_id] = self._run_gridded_ungridded()
            else:
                self.data[self.model_id] = self._run_gridded_gridded()
        except:
            msg = ('Failed to perform analysis: {}\n'
                   .format(traceback.format_exc()))
            const.print_log.warning(msg)
            self._log.write(msg)
            if self.raise_exceptions:
                self._close_log()
                raise Exception(traceback.format_exc())
        finally:
            self._close_log()
            
    @staticmethod
    def get_lowest_resolution(ts_type, *ts_types):
        """Get the lowest resolution ts_type of input ts_types"""
        return get_lowest_resolution(ts_type, *ts_types)
        
    def output_dir(self, task_name):
        """Output directory for colocated data"""
        return self._output_dirs[task_name]
    
    def _check_add_model_read_aux(self, model_var, model_reader):
        if not isinstance(self.model_read_aux, dict):
            return False
        if not model_var in self.model_read_aux:
            return False
        info = self.model_read_aux[model_var]
        if not isinstance(info, dict):
            raise ValueError('Invalid value for model_read_aux of variable '
                             '{}. Need dictionary, got {}'
                             .format(model_var, info))
        elif not all([x in info for x in ['vars_required', 'fun']]):
            raise ValueError('Invalid value for model_read_aux dict of variable '
                             '{}. Require keys vars_required and fun in dict, '
                             'got {}'.format(model_var, info))
        model_reader.add_aux_compute(var_name=model_var, **info)
        return True
    
    def _find_var_matches(self, obs_vars, model_reader):
        """Find variable matches in model data for input obs variables"""
        var_matches = {}
        
        for obs_var in obs_vars:
            if isinstance(self.model_use_vars, dict) and obs_var in self.model_use_vars:
                model_var = self.model_use_vars[obs_var]
            else:
                model_var = obs_var
            
            self._check_add_model_read_aux(model_var, model_reader)
                
            if not model_var in model_reader.vars_provided:
                continue
            var_matches[obs_var] = model_var
        
        if len(var_matches) == 0:
            
            raise DataCoverageError('No variable matches between '
                                    '{} and {} for input vars: {}'
                                    .format(self.model_id, 
                                            self.obs_id, 
                                            self.obs_vars))
        return var_matches
    
    def _read_gridded(self, reader, var_name, start, stop, is_model=True):
        if is_model:
            vert_which = self.obs_vert_type
            ts_type_read = self.model_ts_type_read
        else:
            vert_which = None
            ts_type_read = self.obs_ts_type_read
        try:
            data = reader.read_var(var_name, 
                                   start=start,
                                   stop=stop, 
                                   ts_type=ts_type_read,
                                   flex_ts_type=True,
                                   vert_which=vert_which)
        except DataCoverageError:
            msg = ('No data files available for dataset {} ({})'
                   .format(reader.data_id, var_name))
            if not is_model or not self.obs_vert_type in self.OBS_VERT_TYPES_ALT:
                raise DataCoverageError(msg)
                
            # if request refers to model data, try to read alternative dataset
            # that may be used to extract the data
            obs_vert_type_alt = self.OBS_VERT_TYPES_ALT[self.obs_vert_type]
            data = reader.read_var(var_name, 
                                   start=start,
                                   stop=stop, 
                                   ts_type=ts_type_read,
                                   flex_ts_type=True,
                                   vert_which=obs_vert_type_alt)
        except Exception as e:
            msg = ('Failed to load gridded data: {} / {}. Reason {}'
                   .format(reader.data_id, var_name, repr(e)))
            const.print_log.warning(msg)
            self._log.write(msg)
            if self.raise_exceptions:
                self._close_log()
                raise Exception(msg)
        return data
    
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

        var_matches = self._find_var_matches(obs_vars, model_reader)
        
        if self.read_opts_ungridded is not None:
            ropts = self.read_opts_ungridded
        else:
            ropts = {}
        obs_data = obs_reader.read(datasets_to_read=self.obs_id, 
                                   vars_to_retrieve=obs_vars,
                                   **ropts)
        
        if self.remove_outliers:
            self._update_var_outlier_ranges(var_matches)
                            
        all_ts_types = const.GRID_IO.TS_TYPES
        
        ts_type = self.ts_type
        
        data_objs = {}
        for obs_var, model_var in var_matches.items():
                
            print_log.info('Running {} / {} ({}, {})'.format(self.model_id, 
                                                             self.obs_id, 
                                                             model_var, 
                                                             obs_var))
            
            model_data = self._read_gridded(reader=model_reader, 
                                            var_name=model_var, 
                                            start=start, 
                                            stop=stop, 
                                            is_model=True)
            
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
            
            
            if self.save_coldata:
                savename = self._coldata_savename(model_data, start, stop, ts_type)
                
                file_exists = self._check_coldata_exists(model_data.data_id, 
                                                         savename)
                
                out_dir = chk_make_subdir(self.basedir_coldata, self.model_id)
                if file_exists:
                    if not self.reanalyse_existing:
                        if self._log:
                            self._log.write('SKIP: {}\n'
                                            .format(savename))
                            print_log.info('Skip {} (file already '
                                           'exists)'.format(savename))
                        continue
                    else:
                        print_log.info('Deleting and recomputing existing '
                                       'colocated data file {}'.format(savename))
                        print_log.info('REMOVE: {}\n'.format(savename))
                        os.remove(os.path.join(out_dir, savename))
                        
            try:
                coldata = colocate_gridded_ungridded(gridded_data=model_data, 
                                                     ungridded_data=obs_data, 
                                                     ts_type=ts_type, 
                                                     start=start, stop=stop,
                                                     var_ref=obs_var,
                                                     filter_name=self.filter_name,
                                                     regrid_res_deg=self.regrid_res_deg,
                                                     remove_outliers=self.remove_outliers,
                                                     vert_scheme=self.vert_scheme,
                                                     harmonise_units=self.harmonise_units,
                                                     var_outlier_ranges=self.var_outlier_ranges)
                if self.save_coldata:
                    coldata.to_netcdf(out_dir)
                if self._log:
                    self._log.write('WRITE: {}\n'.format(savename))
                    print_log.info('Writing file {}'.format(savename))
                data_objs[model_var] = coldata
            except Exception as e:
                msg = ('Colocation between model {} / {} and obs {} / {} '
                       'failed: Reason {}'.format(self.model_id,
                                                  model_var, 
                                                  self.obs_id,
                                                  obs_var,
                                                  repr(e)))
                const.print_log.warning(msg)
                self._log.write(msg)
                if self.raise_exceptions:
                    self._close_log()
                    raise Exception(msg)
                    
        return data_objs
    
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
        
        var_matches = self._find_var_matches(obs_vars, model_reader)
        if self.remove_outliers:
            self._update_var_outlier_ranges(var_matches)
            
        all_ts_types = const.GRID_IO.TS_TYPES
        
        ts_type = self.ts_type
        
        data_objs = {}
        
        for obs_var, model_var in var_matches.items():
            print_log.info('Running {} / {} ({}, {})'.format(self.model_id, 
                                                             self.obs_id, 
                                                             model_var, 
                                                             obs_var))
            
            model_data = self._read_gridded(reader=model_reader, 
                                            var_name=model_var, 
                                            start=start, 
                                            stop=stop, 
                                            is_model=True)
            
            if not model_data.ts_type in all_ts_types:
                raise TemporalResolutionError('Invalid temporal resolution {} '
                                              'in model {}'.format(model_data.ts_type,
                                                                   self.model_id))
            obs_data  = self._read_gridded(reader=obs_reader, 
                                           var_name=obs_var, 
                                           start=start,
                                           stop=stop,
                                           is_model=False)
            
            if not obs_data.ts_type in all_ts_types:
                raise TemporalResolutionError('Invalid temporal resolution {} '
                                              'in obs {}'.format(obs_data.ts_type,
                                                                 self.model_id))
            
            # update colocation ts_type, based on the available resolution in
            # model and obs.
            lowest = self.get_lowest_resolution(ts_type, model_data.ts_type,
                                                obs_data.ts_type)
            if lowest != ts_type:
                print_log.info('Updating ts_type from {} to {} (highest '
                               'available in {} / {} combination)'
                               .format(ts_type, lowest, self.model_id,
                                       self.obs_id))
                ts_type = lowest
            
            if self.save_coldata:
                out_dir = chk_make_subdir(self.basedir_coldata,
                                          self.model_id)
                               
                savename = self._coldata_savename(model_data,
                                                  start,
                                                  stop,
                                                  ts_type)
                
                file_exists = self._check_coldata_exists(self.model_id,
                                                          savename)
                if file_exists:
                    if not self.reanalyse_existing:
                        if self._log:
                            self._log.write('SKIP: {}\n'.format(savename))
                            print_log.info('Skip {} (file already '
                                           'exists)'.format(savename))
                        continue
                    else:
                        os.remove(os.path.join(out_dir, savename))
            try:  
                coldata = colocate_gridded_gridded(gridded_data=model_data,
                                                   gridded_data_ref=obs_data, 
                                                   ts_type=ts_type, 
                                                   start=start, stop=stop, 
                                                   filter_name=self.filter_name,
                                                   regrid_res_deg=self.regrid_res_deg,
                                                   remove_outliers=self.remove_outliers,
                                                   vert_scheme=self.vert_scheme,
                                                   harmonise_units=self.harmonise_units,
                                                   var_outlier_ranges=self.var_outlier_ranges)
                if self.save_coldata:
                    coldata.to_netcdf(out_dir)
                if self._log:
                    self._log.write('WRITE: {}\n'.format(savename))
                    print_log.info('Writing file {}'.format(savename))
                data_objs[model_var] = coldata
            except Exception as e:
                msg = ('Colocation between model {} / {} and obs {} / {} '
                       'failed: Reason {}'.format(self.model_id,
                                                  model_var, 
                                                  self.obs_id,
                                                  obs_var,
                                                  repr(e)))
                const.print_log.warning(msg)
                self._log.write(msg)
                if self.raise_exceptions:
                    self._close_log()
                    raise Exception(msg)
        return data_objs
    
    def _init_log(self):
        logdir = chk_make_subdir(self.basedir_logfiles, 
                                 self.model_id)
                                 
        
        fname = ('{}_{}.log'.format(self.obs_id, datetime.today().strftime('%Y%m%d')))
        self._log = log = open(os.path.join(logdir, fname), 'a+')
        log.write('\n------------------ NEW ----------------\n')
        log.write('Timestamp: {}\n\n'.format(datetime.today().strftime('%d-%m-%Y %H:%M')))
        log.write('Analysis configuration\n')
        for k, v in self.items():
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
    
    def _update_var_outlier_ranges(self, var_matches):
        if not isinstance(self.var_outlier_ranges, dict):
            return
        for ovar, mvar in var_matches.items():
            oname = const.VARS[ovar].var_name
            if oname != ovar:
                if ovar in self.var_outlier_ranges:
                    if not oname in self.var_outlier_ranges:
                        self.var_outlier_ranges[oname] = self.var_outlier_ranges[ovar]
                    
            mname = const.VARS[mvar].var_name
            if mname != mvar:
                if mvar in self.var_outlier_ranges:
                    if not mname in self.var_outlier_ranges:
                        self.var_outlier_ranges[mname] = self.var_outlier_ranges[mvar]
    
    def __call__(self, **kwargs):
        raise NotImplementedError
        self.update(**kwargs)
        self.run()
        
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    plt.close('all')

    
    MODEL_ID =  'CAM5.3-Oslo_AP3-CTRL2016-PD'
    col = Colocator(model_id = MODEL_ID,
                    obs_id='AeronetSunV3Lev2.daily',
                    obs_vars=['od550aer', 'ang4487aer'], 
                    start=2010,
                    filter_name='WORLD-wMOUNTAINS',
                    model_use_vars=dict(od550aer = 'od550csaer'),
                    vert_scheme=dict(od550aer='Column'))
    
    col.raise_exceptions = True
    col.reanalyse_existing = True
    
    print(col)
    
    
    run = False
    if run:
        col.run()
        for model_id, vardict in col.data.items():
            for data in vardict.values():
                data.plot_scatter()