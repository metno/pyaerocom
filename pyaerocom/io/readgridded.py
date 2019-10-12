#!/usr/bin/env python3

################################################################
# readgridded.py
#
# model data reading class
#
# this file is part of the aerocom_pt package
#
#################################################################
# Created 20171030 by Jan Griesfeller for Met Norway
#
# Last changed: See git log
#################################################################

#Copyright (C) 2017 met.no
#Contact information:
#Norwegian Meteorological Institute
#Box 43 Blindern
#0313 OSLO
#NORWAY
#E-mail: jan.griesfeller@met.no
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#MA 02110-1301, USA

from glob import glob
import os
from collections import OrderedDict as od
import numpy as np
import pandas as pd
import iris

from pyaerocom import const, print_log, logger
from pyaerocom.variable import Variable, is_3d
from pyaerocom.io.aux_read_cubes import (compute_angstrom_coeff_cubes,
                                         multiply_cubes,
                                         subtract_cubes)
from pyaerocom.helpers import to_pandas_timestamp, get_highest_resolution
from pyaerocom.exceptions import (DataCoverageError,
                                  DataQueryError,
                                  DataSourceError,
                                  FileConventionError,
                                  IllegalArgumentError, 
                                  TemporalResolutionError,
                                  VarNotAvailableError)

from pyaerocom.io.fileconventions import FileConventionRead
from pyaerocom.io import AerocomBrowser
from pyaerocom.io.iris_io import load_cubes_custom, concatenate_iris_cubes
from pyaerocom.io.helpers import add_file_to_log
from pyaerocom.griddeddata import GriddedData


class ReadGridded(object):
    """Class for reading gridded files based on network or model ID
    
    Note
    ----
    The reading only works if files are stored using a valid file naming 
    convention. See package data file `file_conventions.ini <http://
    aerocom.met.no/pyaerocom/config_files.html#file-conventions>`__ for valid
    keys. You may define your own fileconvention in this file, if you wish.
    
    Attributes
    ----------
    data_id : str
        string ID for model or obsdata network (see e.g. Aerocom interface map
        plots lower left corner)
    data : GriddedData
        imported data object 
    data_dir : str
        directory containing result files for this model
    start : pandas.Timestamp
        start time for data import
    stop : pandas.Timestamp
        stop time for data import
    file_convention : FileConventionRead
        class specifying details of the file naming convention for the model
    files : list
        list containing all filenames that were found.
        Filled, e.g. in :func:`ReadGridded.get_model_files`
    from_files : list
        List of all netCDF files that were used to concatenate the current 
        data cube (i.e. that can be based on certain matching settings such as
        var_name or time interval). 
    ts_types : list
        list of all sampling frequencies (e.g. hourly, daily, monthly) that 
        were inferred from filenames (based on Aerocom file naming convention) 
        of all files that were found
    vars : list
        list containing all variable names (e.g. od550aer) that were inferred 
        from filenames based on Aerocom model file naming convention
    years : list
        list of available years as inferred from the filenames in the data 
        directory.
        
    Parameters
    ----------
    data_id : str
        string ID of model (e.g. "AATSR_SU_v4.3","CAM5.3-Oslo_CTRL2016")
    data_dir : str, optional
        directory containing data files. If provided, only this directory is
        considered for data files, else the input `data_id` is used to search 
        for the corresponding directory.
    file_convention : str
        string ID specifying the file convention of this model (cf. 
        installation file `file_conventions.ini <https://github.com/metno/
        pyaerocom/blob/master/pyaerocom/data/file_conventions.ini>`__)
    init : bool
        if True, the model directory is searched (:func:`search_data_dir`) on
        instantiation and if it is found, all valid files for this model are 
        searched using :func:`search_all_files`.

        
    """
    AUX_REQUIRES = {'ang4487aer'    : ['od440aer', 'od870aer'],
                    'od550gt1aer'   : ['od550aer', 'od550lt1aer'],
                    'conc*'        : ['mmr*', 'rho']}
    
    AUX_ALT_VARS = {'od440aer'  :   ['od443aer'],
                    'od870aer'  :   ['od865aer']}
    
    AUX_FUNS = {'ang4487aer'   :    compute_angstrom_coeff_cubes,
                'od550gt1aer'  :    subtract_cubes,
                'conc*'        :    multiply_cubes}
    
    _data_dir = ""
    
    VERT_ALT = {'Surface' : 'ModelLevel'}

    def __init__(self, data_id=None, data_dir=None, file_convention="aerocom3", 
                 init=True):
    
# =============================================================================
#         if not isinstance(data_id, str):
#             if isinstance(data_id, list):
#                 msg = ("Input for data_id is list. You might want to use "
#                        "class ReadGriddedMulti for import?")
#             else:
#                 msg = ("Invalid input for data_id. Need str, got: %s"
#                        %type(data_id))
#             raise TypeError(msg)
# =============================================================================
            
        self._data_dir = None
        
        #: data_id of gridded dataset        
        self._data_id = data_id
        
        self.logger = logger
        
        #: Dictionary containing loaded results for different variables
        self.data = od()
        
        #: Cube lists for each loaded variable
        self.loaded_cubes = od()
        
        # file naming convention. Default is aerocom3 file convention, change 
        # using self.file_convention.import_default("aerocom2"). Is 
        # automatically updated in class ReadGridded
        self.file_convention = FileConventionRead(file_convention)
        
        self.file_info = None
                
        #: List of unique Aerocom variable names that were identified from 
        #: the filenames in the data directory
        self._vars_2d = []
        self._vars_3d = []
        
        
        
        #: This object can be used to 
        self.browser = AerocomBrowser()
        
        self._aux_avail = None
        
        # these can be filled using method add_aux_compute and they will not 
        # affect global settings of the reader class
        self._aux_requires = {}
        self._aux_funs = {}
        
        self.ignore_vert_code = False
        if data_dir is not None:
            self.data_dir = data_dir
        elif data_id:
            self.search_data_dir()
        if self.data_dir is not None:
            try:
                self.search_all_files()
            except DataCoverageError as e:
                print_log.warning(repr(e))

    def reinit(self):
        """Reinit everything that is loaded specific to data_dir"""
        self.file_info = None
        self._vars_2d = []
        self._vars_3d =[]
        self.loaded_cubes = od()
        self.data = od()
      
    @property
    def data_id(self):
        return self._data_id
    
    @data_id.setter
    def data_id(self, val):
        if val is None:
            val = ''
        if not isinstance(val, str):
            raise ValueError('Invalid input for data_id, need str')
        self._data_id = val
        
    @property
    def data_dir(self):
        """Directory of data files"""
        return self._data_dir
    
    @data_dir.setter
    def data_dir(self, val):
        if not isinstance(val, str) or not os.path.isdir(val):
            raise FileNotFoundError('Input data directory {} does not exist'
                                    .format(val))
        self._data_dir = val
        self.reinit() 
            
    @property
    def years_avail(self):
        """Available years"""
        if self.file_info is None:
            self.search_all_files()
        return sorted(self.file_info.year.unique())
    
    @property
    def years(self):
        """Available years"""
        print_log.warning(DeprecationWarning('Attr. "years" is deprecated '
                                             '(but still works). Please use '
                                             '"years_avail" instead.'))
        return self.years_avail
    
    @property
    def experiments(self):
        """List of all experiments that are available in this dataset"""
        if self.file_info is None:
            self.search_all_files()
        return sorted(self.file_info.experiment.unique())
    
    @property
    def files(self):
        """List  of data files"""
        if self.file_info is None:
            self.search_all_files()
        return [os.path.join(self.data_dir, x) for x in 
                sorted(self.file_info.filename.values)]
      
    @property
    def ts_types(self):
        """Available frequencies"""
        return self.file_info.ts_type.unique()
    
    @property
    def vars(self):
        return sorted(self._vars_2d + self._vars_3d)
    
    @property
    def vars_provided(self):
        """Variables provided by this interface"""
        v = []
        v.extend(self.vars)
        
        self._aux_avail = []
        for aux_var in self.AUX_REQUIRES.keys():
            try:
                self._get_aux_vars_and_fun(aux_var)
                if not aux_var in v:
                    v.append(aux_var)
                self._aux_avail.append(aux_var)
            except: #this auxiliary variable cannot be computed
                pass
        for aux_var in self._aux_requires.keys():
            try:
                self._get_aux_vars_and_fun(aux_var)
                if not aux_var in v:
                    v.append(aux_var)
                self._aux_avail.append(aux_var)
            except: #this auxiliary variable cannot be computed
                pass
        #v.extend(self.AUX_REQUIRES.keys())
        #also add standard names of 3D variables if not already in list
        for var in self._vars_3d:
            var = var.lower().replace('3d','')
            if not var in v:
                v.append(var)
        return v
    
    @property
    def file_type(self):
        """File type of data files"""
        return const.GRID_IO.FILE_TYPE
    
    @property
    def TS_TYPES(self):
        """List with valid filename encryptions specifying temporal resolution
        """
        return const.GRID_IO.TS_TYPES
    
    @property
    def start(self):
        """First available year in the dataset (inferred from filenames)
        
        Note
        ----
        This is not variable or ts_type specific, so it is not necessarily 
        given that data from this year is available for all variables in 
        :attr:`vars` or all frequencies liste in :attr:`ts_types`
        """
        if len(self.years_avail) == 0:
            raise AttributeError('No information about available years accessible'
                                 'please run method search_all_files first')
        yr = sorted(self.years_avail)[0]
        if yr == 9999:
            yr = 2222
        return to_pandas_timestamp(yr)
            
    @property
    def stop(self):
        """Last available year in the dataset (inferred from filenames)
        
        Note
        ----
        This is not variable or ts_type specific, so it is not necessarily 
        given that data from this year is available for all variables in 
        :attr:`vars` or all frequencies liste in :attr:`ts_types`
        """
        if len(self.years_avail) == 0:
            raise AttributeError('No information about available years accessible'
                                 'please run method search_all_files first')
        years = sorted(self.years_avail)
        year = years[-1]
        
        if year == 9999:
            self.logger.warning('Data contains climatology. Will be ignored '
                                'as stop time, using last year')
            if len(years) == 1:
                year = 2222
            else:
                year = years[-2]
            
        return to_pandas_timestamp('{}-12-31 23:59:59'.format(year))
    
    def has_var(self, var_name):
        """Check if variable is available
        
        Parameters
        ----------
        var_name : str
            variable to be checked
        
        Returns
        -------
        bool
        """
        if var_name in self.vars_provided or self.check_compute_var(var_name):
            return True
        return False
    
    def _get_years_to_load(self, start=None, stop=None):
        """Array containing year numbers that are supposed to be loaded
        
        Returns
        -------
        ndarray
            all years to be loaded
        """
        start_provided = False
        if start is None:
            start = self.start
            if start.year == 2222:
                return np.array([9999])
        else:
            start_provided = True
            if start == 9999:
                return np.array([9999])
            start = to_pandas_timestamp(start)
        
        if stop is None:
            if start_provided:
                stop = to_pandas_timestamp(start)
            else:
                stop = self.stop
        else:
            stop = to_pandas_timestamp(stop)
        if const.MIN_YEAR > start.year:
            print_log.warning('First available year {} of data {} is smaller '
                              'than supported first year {}.'
                              .format(start, self.data_id, 
                                             const.MIN_YEAR))
            start = const.MIN_YEAR
        if const.MAX_YEAR < stop.year:
            raise ValueError('Last available year {} of data {} is larger '
                             'than supported last year {}.'
                             .format(start, self.data_id, const.MAX_YEAR))
            stop = const.MAX_YEAR
            
        if start and stop:
            return np.arange(start.year, stop.year + 1, 1)
        
        if not self.years_avail:
            raise AttributeError("No information available for available "
                                 "years. Please run method "
                                 "search_all_files first")   
        return np.array(self.years_avail)
    
    def search_data_dir(self):
        """Search data directory based on model ID
        
        Wrapper for method :func:`search_data_dir_aerocom`
        
        Returns
        -------
        str
            data directory
        
        Raises
        ------
        IOError 
            if directory cannot be found
        """
        _dir = self.browser.find_data_dir(self.data_id)
        self.data_dir = _dir
        return _dir
            
    @staticmethod
    def _eval_data_id(data_id):
        spl = data_id.split('_')
        name, meteo = '',''
        experiment = spl[-1]
        if len(spl) > 1:
            sspl = spl[0].split('-')
            if len(sspl) > 1:
                name = sspl[0]
                meteo = sspl[-1]
        return (name, meteo, experiment)
    
    def _update_file_convention(self, files):
        """Update current file convention based on input files
        
        Loops over all files in input list and as updates the file convention
        based on the first file in list that matches one of the registered 
        conventions.
        
        Updates class :attr:`file_convention`
        
        Raises
        ------
        FileNotFoundError
            if none of the input files matches a registered convention.
        """
        for file in files:
            try:
                self.file_convention.from_file(os.path.basename(file))
                return
            except:
                pass
        
        raise FileNotFoundError('None of the available files in {} matches a '
                                'registered pyaerocom file convention'
                                .format(self.data_dir))
        
    def search_all_files(self, update_file_convention=True):
        """Search all valid model files for this model
        
        This method browses the data directory and finds all valid files, that
        is, file that are named according to one of the aerocom file naming
        conventions. The file list is stored in :attr:`files`.
        
        Note
        ----
        It is presumed, that naming conventions of files in
        the data directory are not mixed but all correspond to either of the 
        conventions defined in 
        
        Parameters
        ----------
        update_file_convention : bool
            if True, the first file in `data_dir` is used to identify the
            file naming convention (cf. :class:`FileConventionRead`)
            
        Raises
        ------
        DataCoverageError
            if no valid files could be found
        """
        result = []
        files_ignored = []
        # get all netcdf files in folder
        nc_files = glob(self.data_dir + '/*{}'.format(self.file_type))
        if len(nc_files) == 0:
            print_log.warning('No files of type {} could be found in current '
                              'data_dir={}'.format(self.file_type, 
                                        os.path.abspath(self.data_dir)))
            return
        
        if update_file_convention:
            # Check if the found file has a naming according the aerocom conventions
            # and set the convention for all files (maybe this need to be 
            # updated in case there can be more than one file naming convention
            # within one model directory)
            try:
                self._update_file_convention(nc_files)
            except FileNotFoundError as e:
                print_log.warning(repr(e))
                return
                
        _vars_temp = []
        _vars_temp_3d = []
        
        for _file in nc_files:
            # TODO: resolve this in a more general way...
            if 'ModelLevelAtStations' in _file:
                const.logger.info('Ignoring file {}'.format(_file))
                files_ignored.append(os.path.basename(_file))
                continue
            try:
                info = self.file_convention.get_info_from_file(_file)
                if not self.data_id:
                    self.data_id = info['data_id']
                var_name = info['var_name']
                _is_3d = False
                if is_3d(var_name):
                    _vars_temp_3d.append(var_name)
                    _is_3d = True
                else:
                    _vars_temp.append(var_name)
                
                if not info["ts_type"] in self.TS_TYPES:
                    raise TemporalResolutionError('Invalid frequency {}'
                                                  .format(info["ts_type"]))
                
                name, meteo, experiment = self._eval_data_id(info['data_id']) 
                result.append([var_name, info['year'], info['ts_type'], 
                               info['vert_code'], self.data_id, 
                               name, meteo, experiment, 
                               info['is_at_stations'],
                               _is_3d, os.path.basename(_file)])
                    
            except (FileConventionError, DataSourceError, 
                    TemporalResolutionError) as e:
                msg = ("Failed to import file {}\nModel: {}\n"
                       "Error: {}".format(os.path.basename(_file), 
                                         self.data_id, repr(e)))
                logger.warning(msg)
                if const.WRITE_FILEIO_ERR_LOG:
                    add_file_to_log(_file, msg)
        
        if len(_vars_temp + _vars_temp_3d) == 0:
            raise AttributeError("Failed to extract information from filenames")
        # make sorted list of unique vars

        self._vars_2d = sorted(od.fromkeys(_vars_temp))
        self._vars_3d = sorted(od.fromkeys(_vars_temp_3d))
        
        
        header = ['var_name', 'year', 'ts_type', 'vert_code', 'data_id', 'name',
                  'meteo', 'experiment', 'is_at_stations', '3D', 'filename']
        df = pd.DataFrame(result, columns=header)
        df.sort_values(['var_name', 'year', 'ts_type', 'data_id', 'name',
                        'meteo', 'experiment', 'is_at_stations', '3D'], 
                        inplace=True)
        
        uv = df.vert_code.unique()
        if len(uv) == 1 and uv[0] == '':
            self.ignore_vert_code = True
        self.file_info = df
        
        if len(df) == 0:
            raise DataCoverageError('No files could be found for data {} and '
                                    'years range {}-{}'.format(self.data_id))
    
    def filter_files(self, var_name=None, ts_type=None, start=None, stop=None, 
                     experiment=None, vert_which=None, is_at_stations=False,
                     df=None):
        """Filter file database 
        
        Parameters
        ----------
        var_name : str
            variable that are supposed to be read
        ts_type : str
            string specifying temporal resolution (choose from 
            "hourly", "3hourly", "daily", "monthly"). If None, prioritised 
            of the available resolutions is used
        start : Timestamp or str, optional
            start time of data import 
        stop : Timestamp or str, optional
            stop time of data import
        experiment : str
            name of experiment (only relevant if this dataset contains more 
            than one experiment)
        vert_which : str or dict, optional
            valid AeroCom vertical info string encoded in name (e.g. Column,
            ModelLevel) or dictionary containing var_name as key and vertical
            coded string as value, accordingly
        flex_ts_type : bool
            if True and if applicable, then another ts_type is used in case 
            the input ts_type is not available for this variable
        prefer_longer : bool
            if True and applicable, the ts_type resulting in the longer time
            coverage will be preferred over other possible frequencies that 
            match the query.
        
        """
        if df is None:
            df = self.file_info
            
        yrs = self._get_years_to_load(start, stop)
        year_cond = df.year.isin(yrs)
        
        if var_name is None:
            var_cond = df.var_name.isin(df.var_name.values)
        else:
            var_cond = df.var_name == var_name
        if vert_which is None:
            vert_cond = df.vert_code.isin(df.vert_code.values)
        else:
            vert_cond = df.vert_code == vert_which
        if ts_type is None:
            freq_cond = df.ts_type.isin(df.ts_type.values)
        else:
            freq_cond = df.ts_type == ts_type
        if experiment is None:
            exp_cond = df.experiment.isin(df.experiment.values)
        else:
            exp_cond = df.experiment == experiment
        
        return df.loc[(var_cond) & 
                      (year_cond) &
                      (freq_cond) &
                      (exp_cond) &
                      (vert_cond) &
                      (df.is_at_stations==is_at_stations)]
        
    def _infer_ts_type(self, df, ts_type, flex_ts_type,
                       prefer_longer):
        ts_types = df.ts_type.unique()
        
        if len(ts_types) == 1:
            # only one frequency available
            if flex_ts_type or ts_type is None or ts_types[0] == ts_type:
                # all good
                return ts_types[0]
            raise DataCoverageError('No files could be found for ts_type {}'
                                    .format(ts_type))
        highest_avail = get_highest_resolution(*ts_types)
        # there is more than one frequency available -> decision making 
        # gets more complicated
        if not flex_ts_type:
            if ts_type is None:
                return highest_avail
            elif ts_type in ts_types:
                return ts_type
            raise DataCoverageError('Failed to infer ts_type')
            
        # ts_type is flexible
        if ts_type is None:
            # initiate with highest available
            ts_type = highest_avail
        
        if not prefer_longer:
            return ts_type
        
        # ts_type is flexible and user prefers the longer period over 
        # higher resolution
        ts_type = ts_types[0]
        subset = self.filter_files(ts_type=ts_type, df=df)
        for _ts_type in ts_types[1:]:
            _subset = self.filter_files(ts_type=_ts_type, df=df)
            if len(_subset) > len(subset):
                subset = _subset
                ts_type = _ts_type
        return ts_type
    
    def filter_query(self, var_name, ts_type=None, start=None, stop=None, 
                         experiment=None, vert_which=None, 
                         is_at_stations=False, flex_ts_type=True, 
                         prefer_longer=False):
        """Filter files for read query based on input specs
        
        Parameters
        ----------
        
        
        Returns
        -------
        DataFrame 
            dataframe containing filtered dataset
        """
        if not var_name in self.file_info.var_name.values:
            raise DataCoverageError('Variable {} is not available in dataset '
                                    '{}'.format(var_name, self.data_id))
            
        subset = self.filter_files(var_name=var_name, 
                                   ts_type=None, # disregard ts_type in 1. iteration
                                   start=start, stop=stop, 
                                   experiment=experiment, 
                                   vert_which=vert_which, 
                                   is_at_stations=is_at_stations)
        if len(subset) == 0:
            if vert_which in self.VERT_ALT:
                vc =self.VERT_ALT[vert_which]
                const.print_log.warning('No files could be found for var {} and '
                                        'vert_which {} in {}. Trying to find '
                                        'alternative options'
                                        .format(var_name, vert_which, 
                                                self.data_id))
                return self.filter_query(var_name, ts_type, start, stop, 
                                             experiment, vert_which=vc, 
                                             is_at_stations=is_at_stations,
                                             flex_ts_type=flex_ts_type, 
                                             prefer_longer=prefer_longer)
            raise DataCoverageError('No files could be found')
        ts_type = self._infer_ts_type(subset, ts_type, flex_ts_type, 
                                      prefer_longer)
        subset = self.filter_files(ts_type=ts_type, start=start, 
                                   stop=stop, df=subset)
        if len(subset) == len(subset.year.unique()):
            return subset
        
        # File request could not be resolved such that every year only occurs
        # once
        msg =''
        exps = subset.experiment.unique()
        verts = subset.vert_code.unique()
        
        if len(exps) > 1:
            msg += 'Found multiple experiments. Choose from: {}'.format(exps)
        if len(verts) > 1:
            if msg:
                msg += '; '
            msg += 'Found multiple vertical codes. Choose from: {}'.format(verts)
        raise DataQueryError('Failed to uniquely identify data files for input '
                             'query. Reason: {}'.format(msg))
        
    def get_files(self, var_name, ts_type=None, start=None, stop=None, 
                  experiment=None, vert_which=None, 
                  is_at_stations=False, flex_ts_type=True, 
                  prefer_longer=False):
        """Get data files based on input specs"""
        subset = self.filter_query(var_name, ts_type, start, stop, 
                                       experiment, vert_which, 
                                       is_at_stations, flex_ts_type,
                                       prefer_longer)
        
        return self._generate_file_paths(subset)

    def _generate_file_paths(self, df=None):
        if df is None:
            df = self.file_info
        return sorted([os.path.join(self.data_dir, x) for x in df.filename.values])
    
    def get_var_info_from_files(self):
        """Creates dicitonary that contains variable specific meta information
        
        Returns
        -------
        OrderedDict
            dictionary where keys are available variables and values (for each
            variable) contain information about available ts_types, years, etc.
        """
        result = od()
        for file in self.files:
            finfo = self.file_convention.get_info_from_file(file)
            var_name = finfo['var_name']
            if not var_name in result:
                result[var_name] = var_info = od()
                for key in finfo.keys():
                    if not key == 'var_name':
                        var_info[key] = []
            else:
                var_info = result[var_name]
            for key, val in finfo.items():
                if key == 'var_name':
                    continue
                if val is not None and not val in var_info[key]:
                    var_info[key].append(val)
        # now check auxiliary variables
        for var_to_compute in self.AUX_REQUIRES.keys():
            if var_to_compute in result:
                continue
            try:
                vars_to_read = self._get_aux_vars_and_fun(var_to_compute)[0]
            except VarNotAvailableError:
                pass
            else:
                # init result info dict for aux variable
                result[var_to_compute] = var_info = od()
                first = result[vars_to_read[0]]
                # init with results from first required variable
                var_info.update(**first)
                if len(vars_to_read) > 1:
                    for info_other in vars_to_read[1:]:
                        other = result[info_other]
                        for key, info in var_info.items():
                            # compute match with other variable
                            var_info[key] = list(np.intersect1d(info,
                                                               other[key]))
                var_info['aux_vars'] = vars_to_read
                            
        return result
        
    def update(self, **kwargs):
        """Update one or more valid parameters
        
        Parameters
        ----------
        **kwargs
            keyword args that will be used to update (overwrite) valid class 
            attributes such as `data, data_dir, files`
        """
        for k, v in kwargs.items():
            if k in self.__dict__:
                self.logger.info("Updating %s in ModelImportResult for model %s"
                            "New value: %s" %(k, self.data_id, v))
                self.__dict__[k] = v
            else:
                self.logger.info("Ignoring key %s in ModelImportResult.update()" %k)
                 
    def concatenate_cubes(self, cubes):
        """Concatenate list of cubes into one cube
        
        Parameters
        ----------
        CubeList
            list of individual cubes
        
        Returns
        -------
        Cube
            Single cube that contains concatenated cubes from input list
            
        Raises 
        ------
        iris.exceptions.ConcatenateError
            if concatenation of all cubes failed 
        """        
        return concatenate_iris_cubes(cubes, error_on_mismatch=True)
    
# =============================================================================
#     def _get_aux_fun(self, var_to_compute):
#         """Get method used to compute input variable
#         
#         Parameters
#         ----------
#         var_to_compute : str
#             variable to be computed
#         
#         Returns
#         -------
#         callable
#             method that is used to compute variable
#         
#         Raises
#         ------
#         AttributeError
#             if no function is defined for that variable name
#         """
#         if var_to_compute in self.AUX_FUNS:
#             return self.AUX_FUNS[var_to_compute]
#         elif var_to_compute in self._aux_funs:
#             return self._aux_funs[var_to_compute]
#         raise AttributeError('No method found for computation of {}'
#                              .format(var_to_compute))
#         
#     def _get_aux_vars(self, var_to_compute):
#         """Helper that searches auxiliary variables for computation of input var
#         
#         Parameters
#         ----------
#         var_to_compute : str
#             one of the auxiliary variables that is supported by this interface
#             (cf. :attr:`AUX_REQUIRES`)
#         
#         Returns 
#         -------
#         list
#             list of variables that are used as input for computation method 
#             of input variable (cf. :attr:`AUX_FUNS`)
#             
#         Raises 
#         ------
#         VarNotAvailableError
#             if one of the required variables for computation is not available 
#             in the data
#         """
#         if var_to_compute in self._aux_requires:
#             vars_req = self._aux_requires[var_to_compute]
#         elif var_to_compute in self.AUX_REQUIRES:
#             vars_req = self.AUX_REQUIRES[var_to_compute]
#         
#         vars_to_read = []
#         for var in vars_req:
#             found = 0
#             if var in self.vars:
#                 found = 1
#                 vars_to_read.append(var)
#             elif var in self.AUX_ALT_VARS:
#                 for alt_var in list(self.AUX_ALT_VARS[var]):
#                     if alt_var in self.vars:
#                         found = 1
#                         vars_to_read.append(alt_var)
#                         break
#             if not found:
#                 raise VarNotAvailableError('Cannot compute {}, since {} '
#                                            '(req. for computation) is not '
#                                            'available in data'
#                                            .format(var_to_compute, 
#                                                    var))
#         return vars_to_read
# =============================================================================
    
    def _get_aux_vars_and_fun(self, var_to_compute):
        """Helper that searches auxiliary variables for computation of input var
        
        Parameters
        ----------
        var_to_compute : str
            one of the auxiliary variables that is supported by this interface
            (cf. :attr:`AUX_REQUIRES`)
        
        Returns 
        -------
        list
            list of variables that are used as input for computation method 
            of input variable (cf. :attr:`AUX_FUNS`)
            
        Raises 
        ------
        VarNotAvailableError
            if one of the required variables for computation is not available 
            in the data
        """
        if (var_to_compute in self._aux_requires and 
            var_to_compute in self._aux_funs):
            vars_req = self._aux_requires[var_to_compute]
            fun = self._aux_funs[var_to_compute]
        elif (var_to_compute in self.AUX_REQUIRES and 
              var_to_compute in self.AUX_FUNS):
            vars_req = self.AUX_REQUIRES[var_to_compute]
            fun = self.AUX_FUNS[var_to_compute]
        
        vars_to_read = []
        for var in vars_req:
            found = 0
            if var in self.vars:
                found = 1
                vars_to_read.append(var)
            elif var in self.AUX_ALT_VARS:
                for alt_var in list(self.AUX_ALT_VARS[var]):
                    if alt_var in self.vars:
                        found = 1
                        vars_to_read.append(alt_var)
                        break
            if not found:
                raise VarNotAvailableError('Cannot compute {}, since {} '
                                           '(req. for computation) is not '
                                           'available in data'
                                           .format(var_to_compute, 
                                                   var))
        return (vars_to_read, fun)
    
    def compute_var(self, var_name, start=None, stop=None, ts_type=None, 
                    experiment=None, vert_which=None, flex_ts_type=True, 
                    prefer_longer=False, vars_to_read=None, aux_fun=None, 
                    **kwargs):
        """Compute auxiliary variable
        
        Like :func:`read_var` but for auxiliary variables 
        (cf. :attr:`AUX_REQUIRES`)
        
        Parameters
        ----------
        var_name : str
            variable that are supposed to be read
        start : :obj:`Timestamp` or :obj:`str`, optional
            start time of data import (if valid input, then the current 
            :attr:`start` will be overwritten)
        stop : :obj:`Timestamp` or :obj:`str`, optional
            stop time of data import (if valid input, then the current 
            :attr:`start` will be overwritten)
        ts_type : str
            string specifying temporal resolution (choose from 
            "hourly", "3hourly", "daily", "monthly"). If None, prioritised 
            of the available resolutions is used
        experiment : str
            name of experiment (only relevant if this dataset contains more 
            than one experiment)
        vert_which : str
            valid AeroCom vertical info string encoded in name (e.g. Column,
            ModelLevel)
        flex_ts_type : bool
            if True and if applicable,start=None, stop=None,
                 ts_type=None, flex_ts_type=True then another ts_type is used in case 
            the input ts_type is not available for this variable
        prefer_longer : bool
            if True and applicable, the ts_type resulting in the longer time
            coverage will be preferred over other possible frequencies that 
            match the query.
        **kwargs
            additional keyword args passed to :func:`_load_var`
            
        Returns
        -------
        GriddedData
            loaded data object
        """
        if vars_to_read is not None:
            self.add_aux_compute(var_name, vars_to_read, aux_fun)
        vars_to_read, aux_fun = self._get_aux_vars_and_fun(var_name)
        
        data = []
        # all variables that are required need to be in the same temporal
        # resolution
        try:
            ts_type = self.find_common_ts_type(vars_to_read, start, stop, 
                                               ts_type, experiment, 
                                               vert_which=vert_which,
                                               flex_ts_type=flex_ts_type)  
        except DataCoverageError:
            if not vert_which in self.VERT_ALT:
                raise
            vert_which = self.VERT_ALT[vert_which]
            
            ts_type = self.find_common_ts_type(vars_to_read, start, stop, 
                                               ts_type, experiment, 
                                               vert_which=vert_which,
                                               flex_ts_type=flex_ts_type)  
        for var in vars_to_read:
            aux_data = self._load_var(var_name=var, 
                                      ts_type=ts_type, 
                                      start=start, stop=stop,
                                      experiment=experiment,
                                      vert_which=vert_which,
                                      flex_ts_type=flex_ts_type,
                                      prefer_longer=prefer_longer,
                                      **kwargs)
            data.append(aux_data)

        cube = aux_fun(*data)
        cube.var_name = var_name
        
        data = GriddedData(cube, data_id=self.data_id, 
                           ts_type=data[0].ts_type,
                           computed=True)
        return data
    
    def find_common_ts_type(self, vars_to_read, start=None, stop=None,
                            ts_type=None, experiment=None, vert_which=None, 
                            flex_ts_type=True):
        """Find common ts_type for list of variables to be read
        
        Parameters
        ----------
        vars_to_read : list
            list of variables that is supposed to be read
        start : :obj:`Timestamp` or :obj:`str`, optional
            start time of data import (if valid input, then the current 
            :attr:`start` will be overwritten)
        stop : :obj:`Timestamp` or :obj:`str`, optional
            stop time of data import (if valid input, then the current 
            :attr:`start` will be overwritten)
        ts_type : str
            string specifying temporal resolution (choose from 
            "hourly", "3hourly", "daily", "monthly"). If None, prioritised 
            of the available resolutions is used
        experiment : str
            name of experiment (only relevant if this dataset contains more 
            than one experiment)
        vert_which : str
            valid AeroCom vertical info string encoded in name (e.g. Column,
            ModelLevel)
        flex_ts_type : bool
            if True and if applicable,start=None, stop=None,
                 ts_type=None, flex_ts_type=True then another ts_type is used in case 
            the input ts_type is not available for this variable
        
        Returns
        -------
        str 
            common ts_type for input variable
            
        Raises
        ------
        DataCoverageError
            if no match can be found
            
        """
        if isinstance(vars_to_read, str):
            vars_to_read = [vars_to_read]
        
        common = self.filter_files(var_name=vars_to_read[0], 
                                   start=start,
                                   stop=stop,
                                   experiment=experiment,
                                   vert_which=vert_which).ts_type.unique()
        if len(common) == 0:
            raise DataCoverageError('Could not find any file matches for query '
                                    'and variable {}'.format(vars_to_read[0]))
        for var in vars_to_read[1:]:
            _tt = self.filter_files(var_name=var, 
                                    start=start,
                                    stop=stop,
                                    experiment=experiment,
                                    vert_which=vert_which)
            common = np.intersect1d(common, _tt.ts_type.unique())
            
        if len(common) == 0:
            raise DataCoverageError('Could not find common ts_type for '
                                    'variables {}'.format(vars_to_read))
        elif len(common) == 1:
            if ts_type is None or flex_ts_type:
                return common[0]
            elif ts_type == common[0]:
                return ts_type
            raise DataCoverageError('Could not find files with ts_type={} for '
                                    'all input variables: {}'
                                    .format(ts_type, vars_to_read))
        if ts_type is not None:
            if ts_type in common:
                return ts_type
            
        if not flex_ts_type:
            raise DataCoverageError('Could not find files with ts_type={} for '
                                    'all input variables: {}'
                                    .format(ts_type, vars_to_read))
        
        common_sorted = [x for x in const.GRID_IO.TS_TYPES if x in common]
        return common_sorted[0]
    
    def add_aux_compute(self, var_name, vars_required, fun):
        """Register new variable to be computed
        
        Parameters
        ----------
        var_name : str
            variable name to be computed
        vars_required : list
            list of variables to read, that are required to compute `var_name`
        fun : callable
            function that takes a list of `GriddedData` objects as input and 
            that are read using variable names specified by `vars_required`.
        """
        if isinstance(vars_required, str):
            vars_required = [vars_required]
        if not isinstance(vars_required, list):
            raise ValueError('Invalid input for vars_required. Need str or list. '
                             'Got: {}'.format(vars_required))
        elif not callable(fun):
            raise ValueError('Invalid input for fun. Input is not a callable '
                             'object')
        self._aux_requires[var_name] = vars_required
        self._aux_funs[var_name] = fun
    
    def check_compute_var(self, var_name):
        """Check if variable name belongs to family that can be computed
        
        For instance, if input var_name is `concdust` this method will check
        :attr:`AUX_REQUIRES` to see if there is a variable family pattern
        (`conc*`) defined that specifies how to compute these variables. If 
        a match is found, the required variables and computation method is 
        added via :func:`add_aux_compute`.
        
        Note
        ----
        BETA version, use with care
        
        Parameters
        -----------
        var_name : str
            variable name to be checked
        
        Returns
        -------
        bool
            True if match is found, else False
        """
        
        if '*' in var_name:
            from pyaerocom.exceptions import VariableDefinitionError
            raise VariableDefinitionError('Invalid variable name {}. Must not '
                                          'contain *'.format(var_name))
        if var_name in self.AUX_REQUIRES:
            return True
        elif var_name in self._aux_requires:
            return True
        import fnmatch
        patterns = [x for x in self.AUX_REQUIRES if '*' in x]
        vars_found = []
        for pattern in patterns:
            if fnmatch.fnmatch(var_name, pattern):
                vars_required = self.AUX_REQUIRES[pattern]
                for addvar in vars_required:
                    
                    if not '*' in addvar:
                        vars_found.append(addvar)
                    else:
                        _addvar = var_name
                        spl1 = pattern.split('*')
                        spl2 = addvar.split('*')
                        if len(spl1) != len(spl2):
                            raise AttributeError('variable patterns in '
                                                 'AUX_REQUIRES and corresponding '
                                                 'values (with * in name) need '
                                                 'to have the same number of '
                                                 'wildcard delimiters')
                        for i, substr in enumerate(spl1):
                            if bool(substr):
                                _addvar = _addvar.replace(substr, spl2[i])
                        vars_found.append(_addvar)
                if (len(vars_found) == len(vars_required) and
                    all([x in self.vars_provided for x in vars_found])):
                    
                    self.add_aux_compute(var_name, 
                                         vars_required=vars_found,
                                         fun=self.AUX_FUNS[pattern])
                        
                    return True
        return False
    
                
    # TODO: add from_vars input arg for computation and corresponding method
    def read_var(self, var_name, start=None, stop=None,
                 ts_type=None, experiment=None, vert_which=None, 
                 flex_ts_type=True, prefer_longer=False, 
                 aux_vars=None, aux_fun=None,
                 **kwargs):
        """Read model data for a specific variable
        
        This method searches all valid files for a given variable and for a 
        provided temporal resolution (e.g. *daily, monthly*), optionally
        within a certain time window, that may be specified on class 
        instantiation or using the corresponding input parameters provided in 
        this method.
        
        The individual NetCDF files for a given temporal period are loaded as
        instances of the :class:`iris.Cube` object and appended to an instance
        of the :class:`iris.cube.CubeList` object. The latter is then used to 
        concatenate the individual cubes in time into a single instance of the
        :class:`pyaerocom.GriddedData` class. In order to ensure that this
        works, several things need to be ensured, which are listed in the 
        following and which may be controlled within the global settings for 
        NetCDF import using the attribute :attr:`GRID_IO` (instance of
        :class:`OnLoad`) in the default instance of the 
        :class:`pyaerocom.config.Config` object accessible via 
        ``pyaerocom.const``.
        
        
        Parameters
        ----------
        var_name : str
            variable that are supposed to be read
        start : Timestamp or str, optional
            start time of data import 
        stop : Timestamp or str, optional
            stop time of data import
        ts_type : str
            string specifying temporal resolution (choose from 
            "hourly", "3hourly", "daily", "monthly"). If None, prioritised 
            of the available resolutions is used
        experiment : str
            name of experiment (only relevant if this dataset contains more 
            than one experiment)
        vert_which : str or dict, optional
            valid AeroCom vertical info string encoded in name (e.g. Column,
            ModelLevel) or dictionary containing var_name as key and vertical
            coded string as value, accordingly
        flex_ts_type : bool
            if True and if applicable, then another ts_type is used in case 
            the input ts_type is not available for this variable
        prefer_longer : bool
            if True and applicable, the ts_type resulting in the longer time
            coverage will be preferred over other possible frequencies that 
            match the query.
        aux_vars : list
            only relevant if `var_name` is not available for reading but needs
            to be computed: list of variables that are required to compute 
            `var_name`
        aux_fun : callable
            only relevant if `var_name` is not available for reading but needs
            to be computed: custom method for computation (cf. 
            :func:`add_aux_compute` for details)
        **kwargs
            additional keyword args parsed to :func:`_load_var`
            
        Returns
        -------
        GriddedData
            loaded data object
            
        Raises
        ------
        AttributeError
            if none of the ts_types identified from file names is valid
        VarNotAvailableError
            if specified ts_type is not supported
        """
        if aux_vars is not None:
            self.add_aux_compute(var_name, aux_vars, aux_fun)
        
        if isinstance(ts_type, dict):
            try:
                ts_type = ts_type[var_name]
            except:
                const.print_log.info('Setting ts_type to None, since input '
                                     'dict {} does not contain specification '
                                     'variable to read {}'.format(ts_type, 
                                                                  var_name))
                ts_type = None
                
        #ts_type = self._check_ts_type(ts_type)
        var_to_read = None
        do_compute = (var_name in self._aux_requires and 
                      self.check_compute_var(var_name))
        if not do_compute:
            if var_name in self.vars:
                var_to_read = var_name  
            else:
                # e.g. user asks for od550aer but files contain only 3d var od5503daer
                #if not var_to_read in self.vars: 
                for var in self._vars_3d:
                    if Variable(var).var_name == var_name:
                        var_to_read = var
                if var_to_read is None:
                    for alias in const.VARS[var_name].aliases:
                        if alias in self.vars:
                            const.print_log.info('Did not find {} field, loading '
                                                 '{} instead'.format(var_name,
                                                  alias))
                            var_to_read = alias
        
        if isinstance(vert_which, dict):
            try:
                vert_which = vert_which[var_name]
            except:
                const.print_log.info('Setting vert_which to None, since input '
                                     'dict {} does not contain specification '
                                     'variable to read {}'.format(vert_which, 
                                                                  var_name))
                vert_which = None
                
        if var_to_read is not None: # variable can be read directly
            data = self._load_var(var_name=var_to_read, 
                                  ts_type=ts_type, 
                                  start=start, stop=stop,
                                  experiment=experiment, 
                                  vert_which=vert_which,
                                  flex_ts_type=flex_ts_type, 
                                  prefer_longer=prefer_longer,
                                  **kwargs)
        
        elif self.check_compute_var(var_name):
            data = self.compute_var(var_name=var_name, 
                                    start=start, stop=stop, 
                                    ts_type=ts_type, 
                                    experiment=experiment, 
                                    vert_which=vert_which,
                                    flex_ts_type=flex_ts_type, 
                                    prefer_longer=prefer_longer)

# =============================================================================
#                                     vars_to_read=self._aux_requires[var_name],
#                                     aux_fun=self._aux_funs[var_name])
#             
# =============================================================================
        else:
            raise VarNotAvailableError("Error: variable {} not available in "
                                       "files and can also not be computed."
                                       .format(var_name))
        
        if var_name in self.data:
            self.logger.warning("Warning: Data for variable {} already exists "
                           "and will be overwritten".format(var_name))
        
        data.reader = self
        self.data[var_name] = data
        
        return data
        
                
    def read(self, vars_to_retrieve=None, start=None, stop=None, ts_type=None, 
             experiment=None, vert_which=None, flex_ts_type=True, 
             prefer_longer=False, require_all_vars_avail=False, **kwargs):
        """Read all variables that could be found 
        
        Reads all variables that are available (i.e. in :attr:`vars`)
        
        Parameters
        ----------
        vars_to_retrieve : list or str, optional
            variables that are supposed to be read. If None, all variables
            that are available are read.
        start : Timestamp or str, optional
            start time of data import 
        stop : Timestamp or str, optional
            stop time of data import 
        ts_type : str, optional
            string specifying temporal resolution (choose from 
            "hourly", "3hourly", "daily", "monthly"). If None, prioritised 
            of the available resolutions is used
        experiment : str
            name of experiment (only relevant if this dataset contains more 
            than one experiment)
        vert_which : str or dict, optional
            valid AeroCom vertical info string encoded in name (e.g. Column,
            ModelLevel) or dictionary containing var_name as key and vertical
            coded string as value, accordingly
        flex_ts_type : bool
            if True and if applicable, then another ts_type is used in case 
            the input ts_type is not available for this variable
        prefer_longer : bool
            if True and applicable, the ts_type resulting in the longer time
            coverage will be preferred over other possible frequencies that 
            match the query.
        require_all_vars_avail : bool
            if True, it is strictly required that all input variables are 
            available. 
        **kwargs
            optional and support for deprecated input args
        
        Returns
        -------
        tuple
            loaded data objects (type :class:`GriddedData`)
            
        Raises 
        ------
        IOError
            if input variable names is not list or string
        VarNotAvailableError
            1. if ``require_all_vars_avail=True`` and one or more of the 
            desired variables is not available in this class
            2. if ``require_all_vars_avail=True`` and if none of the input 
            variables is available in this object
        """
        if vars_to_retrieve is None and 'var_names' in kwargs:
            const.print_log.warning(DeprecationWarning('Input arg var_names '
                                                       'is deprecated (but '
                                                       'still works). Please '
                                                       'use vars_to_retrieve '
                                                       'instead'))
            vars_to_retrieve = kwargs['var_names']
        if vars_to_retrieve is None:
            vars_to_retrieve = self.vars
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        elif not isinstance(vars_to_retrieve, list):
            raise IOError('Invalid input for vars_to_retrieve {}. Need string '
                          'or list of strings specifying var_names to load. '
                          'You may also leave it empty (None) in which case all '
                          'available variables are loaded'
                          .format(vars_to_retrieve))
        if require_all_vars_avail:
            if not all([var in self.vars_provided for var in vars_to_retrieve]):
                raise VarNotAvailableError('One or more of the specified vars '
                                        '({}) is not available in {} database. '
                                        'Available vars: {}'.format(
                                        vars_to_retrieve, self.data_id, 
                                        self.vars_provided))
        var_names = list(np.intersect1d(self.vars_provided, vars_to_retrieve))
        if len(var_names) == 0:
            raise VarNotAvailableError('None of the desired variables is '
                                        'available in {}'.format(self.data_id))
        data = []
        for var in var_names:
            try:
                data.append(self.read_var(var_name=var, 
                                          start=start, stop=stop, 
                                          ts_type=ts_type,
                                          experiment=experiment,
                                          vert_which=vert_which,
                                          flex_ts_type=flex_ts_type,
                                          prefer_longer=prefer_longer))
            except (VarNotAvailableError, DataCoverageError) as e:
                self.logger.warning(repr(e))
        return tuple(data)
    
    def _check_correct_units_cube(self, cube):
        if ('invalid_units' in cube.attributes and 
            cube.attributes['invalid_units'] in const.GRID_IO.UNITS_ALIASES):
            
            from_unit = cube.attributes['invalid_units']
            to_unit = const.GRID_IO.UNITS_ALIASES[from_unit]
            const.logger.info('Updating invalid unit in {} from {} to {}'
                              .format(repr(cube), from_unit, to_unit))
            
            cube.units = to_unit
        return cube
                
    def _load_files(self, files, var_name, perform_fmt_checks=None,
                    **kwargs):
        """Load list of files containing variable to read into Cube instances
        
        Parameters
        ----------
        files : list
            list of netcdf file
        var_name : str
            name of variable to read
        perform_fmt_checks : bool
            if True, the loaded data is checked for consistency with 
            AeroCom default requirements.
        **kwargs
            additional keyword args parsed to :func:`load_cubes_custom`.
        
        Returns
        -------
        CubeList
            list of loaded Cube instances
        list
            list containing corresponding filenames of loaded cubes
        """
        cubes, loaded_files = load_cubes_custom(files, var_name,
                                                perform_fmt_checks=perform_fmt_checks,
                                                **kwargs)
        for cube in cubes:
            cube = self._check_correct_units_cube(cube)
            
        if len(loaded_files) == 0:
            raise IOError("None of the input files could be loaded in {}"
                          .format(self.data_id))
        
        self.loaded_cubes[var_name] = cubes
        return (cubes, loaded_files)
    
    def _load_var(self, var_name, ts_type, start, stop,
                  experiment, vert_which, flex_ts_type, 
                  prefer_longer, **kwargs):
        """Find files corresponding to input specs and load into GriddedData
        
        Note 
        ----
        See :func:`read_var` for I/O info.
        """
        if self.ignore_vert_code:
            vert_which = None
        subset = self.filter_query(var_name, ts_type, start, stop, 
                                   experiment, vert_which, 
                                   is_at_stations=False, 
                                   flex_ts_type=flex_ts_type, 
                                   prefer_longer=prefer_longer)
        if len(subset) == 0:
            raise DataQueryError('Could not find file match for query')
        ts_types = subset.ts_type.unique()
        # sanity check
        if len(ts_types) > 1:
            raise DataQueryError('Fatal: subset contains more than one ts_type')
        
        ts_type = ts_types[0]
        match_files = self._generate_file_paths(subset)
        (cube_list, 
         from_files) = self._load_files(match_files, var_name, **kwargs)
        is_concat = False
        if len(cube_list) > 1:
            try:
                cube = self.concatenate_cubes(cube_list)
                is_concat = True
            except iris.exceptions.ConcatenateError as e:
                raise NotImplementedError('Failed to concatenate cubes: {}\n'
                                          'Error: {}'.format(cube_list, repr(e)))
        else:
            cube = cube_list[0]
        
        data = GriddedData(input=cube, 
                           from_files=from_files,
                           data_id=self.data_id, 
                           ts_type=ts_type,
                           concatenated=is_concat)
        
        # crop cube in time (if applicable)
        if not start == 9999:
            try:
                data = self._check_crop_time(data, start, stop)
            except:
                const.print_log.exception('Failed to crop time dimension in {}. '
                                          '(start: {}, stop: {})'
                                          .format(data, start, stop))
        return data
    
    def _check_crop_time(self, data, start, stop):
        crop_time = False
        crop_time_range = [self.start, self.stop]
        if start is not None:
            crop_time = True
            crop_time_range[0] = to_pandas_timestamp(start)
        if stop is not None:
            crop_time = True
            crop_time_range[1] = to_pandas_timestamp(stop)
        if crop_time:
            self.logger.info("Applying temporal cropping of result cube")
            data = data.crop(time_range=crop_time_range)
        return data
    
    def _check_ts_type(self, ts_type):
        """Check and, if applicable, update ts_type
        
        Returns
        -------
        str
            valid ts_type
        
        Raises
        ------
        ValueError
            
        """
        if ts_type is None:
            if len(self.ts_types) == 0:
                raise AttributeError('Apparently no files with a valid ts_type '
                                     'entry in their filename could be found')
                
            ts_type = self.ts_types[0]
        if not ts_type in self.TS_TYPES:
            raise ValueError("Invalid input for ts_type, got: {}, "
                             "allowed values: {}".format(ts_type, 
                                                         self.TS_TYPES))
        return ts_type
    
    def __getitem__(self, var_name):
        """Try access import result for one of the models
        
        Parameters
        ----------
        var_name : str
            string specifying variable that is supposed to be extracted
        
        Returns
        -------
        GriddedData
            the corresponding read class for this model
            
        Raises
        -------
        ValueError
            if results for ``var_name`` are not available
        """
        if not var_name in self.data:
            self.read_var(var_name)
        return self.data[var_name]
    
    def __str__(self):
        head = "Pyaerocom {}".format(type(self).__name__)
        s = ("\n{}\n{}\n"
             "Data ID: {}\n"
             "Data directory: {}\n"
             "Available experiments: {}\n"
             "Available years: {}\n"
             "Available frequencies {}\n"
             "Available variables: {}\n".format(head, 
                                                len(head)*"-",
                                                self.data_id,
                                                self.data_dir,
                                                self.experiments,
                                                self.years_avail,
                                                self.ts_types,
                                                self.vars))
        if self.data:
            s += "\nLoaded GriddedData objects:\n"
            for var_name, data in self.data.items():
                s += "{}\n".format(data.short_str())
# =============================================================================
#         if self.data_yearly:
#             s += "\nLoaded GriddedData objects (individual years):\n"
#             for var_name, yearly_data in self.data_yearly.items():
#                 if yearly_data:
#                     for year, data in yearly_data.items():
#                         s += "{}\n".format(data.short_str())
# =============================================================================
        return s.rstrip()
    
    ### DEPRECATED STUFF
    @property
    def name(self):
        """Deprecated name of attribute data_id"""
        const.print_log.warning(DeprecationWarning("Please use data_id"))
        return self.data_id
        
class ReadGriddedMulti(object):
    """Class for import of AEROCOM model data from multiple models
    
    This class provides an interface to import model results from an arbitrary
    number of models and specific for a certain time interval (that can be 
    defined, but must not be defined). Largely based on 
    :class:`ReadGridded`.
    
    ToDo
    ----
    
    Sub-class from ReadGridded
    
    Note
    ----
    The reading only works if files are stored using a valid file naming 
    convention. See package data file `file_conventions.ini <http://
    aerocom.met.no/pyaerocom/config_files.html#file-conventions>`__ for valid
    keys. You may define your own fileconvention in this file, if you wish.
    
    Attributes
    ----------
    data_ids : list
        list containing string IDs of all models that should be imported
    results : dict
        dictionary containing :class:`ReadGridded` instances for each
        name
    
    Examples
    --------
    >>> import pyaerocom, pandas
    >>> start, stop = pandas.Timestamp("2012-1-1"), pandas.Timestamp("2012-5-1")
    >>> models = ["AATSR_SU_v4.3", "CAM5.3-Oslo_CTRL2016"]
    >>> read = pyaerocom.io.ReadGriddedMulti(models, start, stop)
    >>> print(read.data_ids)
    ['AATSR_SU_v4.3', 'CAM5.3-Oslo_CTRL2016']
    >>> read_cam = read['CAM5.3-Oslo_CTRL2016']
    >>> assert type(read_cam) == pyaerocom.io.ReadGridded
    >>> for var in read_cam.vars: print(var)
    abs550aer
    deltaz3d
    humidity3d
    od440aer
    od550aer
    od550aer3d
    od550aerh2o
    od550dryaer
    od550dust
    od550lt1aer
    od870aer
    """

    def __init__(self, data_ids):
        const.print_log.warning(DeprecationWarning('ReadGriddedMulti class is '
                                                   'deprecated and will not '
                                                   'be further developed. '
                                                   'Please use ReadGridded.'))
        if isinstance(data_ids, str):
            data_ids = [data_ids]
        if not isinstance(data_ids, list) or not all([isinstance(x, str) for x in data_ids]):
            raise IllegalArgumentError("Please provide string or list of strings")
    
        self.data_ids = data_ids
        #: dictionary containing instances of :class:`ReadGridded` for each
        #: datset
        
        self.readers = {}
        self.data = {}
        
        self._init_readers()
        
    def _init_readers(self):
        for data_id in self.data_ids:
            self.readers[data_id] = ReadGridded(data_id)
        
    def read(self, vars_to_retrieve, start=None, stop=None,
             ts_type=None, **kwargs):
        """High level method to import data for multiple variables and models
        
        Parameters
        ----------
        var_names : :obj:`str` or :obj:`list`
            string IDs of all variables that are supposed to be imported
        start : :obj:`Timestamp` or :obj:`str`, optional
            start time of data import (if valid input, then the current 
            :attr:`start` will be overwritten)
        stop : :obj:`Timestamp` or :obj:`str`, optional
            stop time of data import (if valid input, then the current 
            :attr:`start` will be overwritten)
        ts_type : str
            string specifying temporal resolution (choose from 
            "hourly", "3hourly", "daily", "monthly").If None, prioritised 
            of the available resolutions is used
        flex_ts_type : bool
            if True and if applicable, then another ts_type is used in case 
            the input ts_type is not available for this variable
        
        Returns
        -------
        dict
            result dictionary
            
        Examples
        --------
        
            >>> read = ReadGriddedMulti(names=["ECMWF_CAMS_REAN",
            ...                                "ECMWF_OSUITE"])
            >>> read.read(["od550aer", "od550so4", "od550bc"])
            
        """
        if isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
            
        for data_id in self.data_ids:
            if not data_id in self.readers:
                self.readers[data_id] = ReadGridded(data_id)
            reader = self.readers[data_id]
            if not data_id in self.data:
                self.data[data_id] = {}
            for var in vars_to_retrieve:
                try:
                    data = reader.read_var(var, start, stop, ts_type, **kwargs)
                    self.data[data_id][var] = data
                except Exception as e:
                    const.print_log.exception('Failed to read data of {}\n'
                                            'Error message: {}'.format(data_id,
                                                                       repr(e)))
        return self.data
    
    def __str__(self):
        head = "Pyaerocom %s" %type(self).__name__
        s = ("\n%s\n%s\n"
             "Data-IDs: %s\n" %(head, len(head)*"-", self.data_ids))
        if bool(self.data):
            s += "\nLoaded data:"
            for name, vardata in self.data.items():
                for var, data in vardata.items():
                    s += "\n%s" %var
        return s
    
if __name__=="__main__":
    
    import matplotlib.pyplot as plt
    plt.close('all')
    import pyaerocom as pya
    
    r = ReadGridded(data_dir='/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III-2019/TM5_AP3-CTRL2019/renamed')
    
    print(r.data_id)