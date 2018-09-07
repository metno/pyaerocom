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
import re
import logging
from os.path import isdir, basename
from collections import OrderedDict as od
import numpy as np
import pandas as pd
from datetime import datetime
import iris

from pyaerocom import const as CONST
from pyaerocom.helpers import to_pandas_timestamp
from pyaerocom.exceptions import (IllegalArgumentError, 
                                  DataCoverageError,
                                  VarNotAvailableError)
from pyaerocom.io.fileconventions import FileConventionRead
from pyaerocom.io import AerocomBrowser
from pyaerocom.io.iris_io import load_cube_custom, concatenate_iris_cubes
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
    name : str
        string ID for model or obsdata network (see e.g. Aerocom interface map
        plots lower left corner)
    data : GriddedData
        imported data object 
    data_dir : str
        directory containing result files for this model
    start_time : pandas.Timestamp
        start time for data import
    stop_time : pandas.Timestamp
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
    years :
        
    Parameters
    ----------
    name : str
        string ID of model (e.g. "AATSR_SU_v4.3","CAM5.3-Oslo_CTRL2016")
    start_time : :obj:`pandas.Timestamp` or :obj:`str`, optional
        desired start time of dataset (note, that strings are passed to 
        :class:`pandas.Timestamp` without further checking)
    stop_time : :obj:`pandas.Timestamp` or :obj:`str`, optional
        desired stop time of dataset (note, that strings are passed to 
        :class:`pandas.Timestamp` without further checking)
    file_convention : str
        string ID specifying the file convention of this model (cf. 
        installation file `file_conventions.ini <https://github.com/metno/
        pyaerocom/blob/master/pyaerocom/data/file_conventions.ini>`__)
    init : bool
        if True, the model directory is searched (:func:`search_data_dir`) on
        instantiation and if it is found, all valid files for this model are 
        searched using :func:`search_all_files`.
        
    Examples
    --------
    
        >>> read = ReadGridded(name="ECMWF_OSUITE")
        >>> read.read_var("od550aer")
        >>> read.read_var("od550so4")
        >>> read.read_var("od550bc")
        >>> print(data.short_str()) for data in read.data
        
    """
    #: Directory containing model data for this species
    _data_dir = ""
    _start_time = None
    _stop_time = None
    #VALID_DIM_STANDARD_NAMES = ['longitude', 'latitude', 'altitude', 'time']
    def __init__(self, name="", start_time=None, stop_time=None,
                 file_convention="aerocom3", init=True):
        # model ID
        if not isinstance(name, str):
            if isinstance(name, list):
                msg = ("Input for name is list. You might want to use "
                       "class ReadGriddedMulti for import?")
            else:
                msg = ("Invalid input for name. Need str, got: %s"
                       %type(name))
            raise TypeError(msg)
        
        #: name of gridded dataset        
        self.name = name
        
        self.logger = logging.getLogger(__name__)
        # only overwrite if there is input, note that the attributes
        # start_time and stop_time are defined below as @property getter and
        # setter methods, that ensure that the input is convertible to 
        # pandas.Timestamp
        if start_time is not None:
            self._start_time = to_pandas_timestamp(start_time)
        if stop_time is not None:
            self._stop_time = to_pandas_timestamp(stop_time)
        
        #: Dictionary containing loaded results for different variables
        self.data = od()
        
        # file naming convention. Default is aerocom3 file convention, change 
        # using self.file_convention.import_default("aerocom2"). Is 
        # automatically updated in class ReadGridded
        self.file_convention = FileConventionRead(file_convention)
        
        #: All files that were found for this model (updated, e.g. in class
        #: ReadGridded, method: `get_model_files`
        self.files = []
        
        #: All files that match a certain variable, ts_type and time period
        #: Will be filled in :func:`find_var_files_in_timeperiod` 
        self.match_files = None
        
        #: List of unique Aerocom temporal resolution strings that were 
        #: identified from the filenames in the data directory
        self.ts_types = []
        
        #: List of unique Aerocom variable names that were identified from 
        #: the filenames in the data directory
        self.vars = []
        
        #: List of unique years that were 
        #: identified from the filenames in the data directory
        self.years = []
        
        #: All files that could be loaded into cubes (i.e. instances 
        #: of :class:`iris.cube.Cube` class. Will be filled in method
        #: :func:`load_files` and loaded cubes can be accessed via 
        #: private attribute :attr:`_cubes`
        self.loaded_files = od()
        
        #: Cube lists for each loaded variable
        self.cubes = od()
        
        #: This object can be used to 
        self.browser = AerocomBrowser()
        
        self.read_errors = {}
        if init and name:
            self.search_data_dir()
            self.search_all_files()
                
    @property
    def data_dir(self):
        """Model directory"""
        dirloc = self._data_dir
        if not isdir(dirloc):
            raise IOError("Model directory for ID %s not available or does "
                          "not exist" %self.name)
        return dirloc
    
    @data_dir.setter
    def data_dir(self, value):
        if isinstance(value, str) and isdir(value):
            self._data_dir = value
        else:
            raise ValueError("Could not set directory: %s" %value)
            
    @property
    def vars_read(self):
        return [k for k in self.data.keys()]
    
    @property
    def file_type(self):
        """File type of data files"""
        return CONST.GRID_IO.FILE_TYPE
    
    @property
    def TS_TYPES(self):
        """List with valid filename encryptions specifying temporal resolution
        """
        return CONST.GRID_IO.TS_TYPES
    
    @property
    def start_time(self):
        """First available year in the dataset (inferred from filenames)
        
        Note
        ----
        This is not variable or ts_type specific, so it is not necessarily 
        given that data from this year is available for all variables in 
        :attr:`vars` or all frequencies liste in :attr:`ts_types`
        """
        if len(self.years) == 0:
            raise AttributeError('No information about available years accessible'
                                 'please run method search_all_files first')
        return to_pandas_timestamp(sorted(self.years)[0])
            
    @property
    def stop_time(self): 
        """Last available year in the dataset (inferred from filenames)
        
        Note
        ----
        This is not variable or ts_type specific, so it is not necessarily 
        given that data from this year is available for all variables in 
        :attr:`vars` or all frequencies liste in :attr:`ts_types`
        """
        if len(self.years) == 0:
            raise AttributeError('No information about available years accessible'
                                 'please run method search_all_files first')
        years = sorted(self.years)
        year = years[-1]
        
        if year == 9999:
            self.logger.warning('Data contains climatology. Cannot be handled '
                                'yet and will be ignored')
            year = years[-2]
            
        return to_pandas_timestamp('{}-12-31 23:59:59'.format(year))
    
# =============================================================================
#     @stop_time.setter
#     def stop_time(self, value):
#         value = to_pandas_timestamp(value)
#         self._stop_time = value
#     
# =============================================================================
    def get_years_to_load(self, start_time=None, stop_time=None):
        """Array containing year numbers that are supposed to be loaded
        
        Returns
        -------
        ndarray
            all years to be loaded
        """
        load_only_year = False
        if start_time is None:
            start_time = self.start_time
        else:
            start_time = to_pandas_timestamp(start_time)
            #take only this year
            if stop_time is None:
                load_only_year = True
                stop_time = start_time #same year
        if stop_time is None:
            stop_time = self.stop_time
        elif not load_only_year: #stop time was input
            stop_time = to_pandas_timestamp(stop_time)
            
        if start_time and stop_time:
            return np.arange(start_time.year, stop_time.year + 1, 1)
        if not self.years:
            raise AttributeError("No information available for available "
                                 "years. Please run method "
                                 "search_all_files first")
        return self.years
    
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
        _dir = self.browser.find_data_dir(self.name)
        self.data_dir = _dir
        return _dir
    
    # get the model directory (note that the folder "renamed" is used)
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
        IOError
            if none of the files in the data directory follows either of the 
            available naming conventions (cf. data file *fileconventions.ini*)
        """
        # get all netcdf files in folder
        nc_files = glob(self.data_dir + '/*{}'.format(self.file_type))
        if update_file_convention:
            # Check if the found file has a naming according the aerocom conventions
            # and set the convention for all files (maybe this need to be 
            # updated in case there can be more than one file naming convention
            # within one model directory)
            ok = False
            for file in nc_files:
                try:
                    self.file_convention.from_file(basename(file))
                    ok = True
                    break
                except:
                    pass
            if not ok:
                raise IOError("Failed to identify file naming convention "
                              "from files in model directory for model "
                              "%s\ndata_dir: %s"
                              %(self.name, self.data_dir))
        _vars_temp = []
        _years_temp = []
        _ts_types_temp = []
        for _file in nc_files:
            try:
                info = self.file_convention.get_info_from_file(_file)
                
                _vars_temp.append(info["var_name"])
                if info['var_name'] is None:
                    raise Exception
                _years_temp.append(info["year"])
                _ts_types_temp.append(info["ts_type"])
                self.files.append(_file)
                self.logger.debug('Read file {}'.format(_file))
            except Exception as e:
                msg = ("Failed to import file {}\nModel: {}\n"
                      "Error: {}".format(basename(_file), 
                                         self.name, repr(e)))
                self.logger.warning(msg)
                if CONST.WRITE_FILEIO_ERR_LOG:
                    add_file_to_log(_file, msg)
                    
        if not _vars_temp or not len(_vars_temp) == len(_years_temp):
            raise IOError("Failed to extract information from filenames")
        # make sorted list of unique vars

        self.vars = sorted(od.fromkeys(_vars_temp))
        self.years = sorted(od.fromkeys(_years_temp))
        
        _ts_types = od.fromkeys(_ts_types_temp)
        # write detected sampling frequencies in the preferred order
        self.ts_types = []
        for item in self.TS_TYPES:
            if item in _ts_types:
                self.ts_types.append(item)
        
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
                            "New value: %s" %(k, self.name, v))
                self.__dict__[k] = v
            else:
                self.logger.info("Ignoring key %s in ModelImportResult.update()" %k)
    
    def find_var_files_flex_ts_type(self, var_name, ts_type_init,
                                    start_time=None, stop_time=None):
        """Find available files for a variable in a time period 
        
        Like :func:`find_var_files_in_timeperiod` but this method also checks
        other available ts_types in case, no files can be found for the 
        desired temporal resolution
        
        Parameters
        -----------
        var_name : str
            variable name
        ts_type_init : str
            desired temporal resolution of data
        start_time : :obj:`Timestamp` or :obj:`str`, optional
            start time of data. If None, then the first available time stamp 
            in this data object is used (i.e. :attr:`start_time`)
        stop_time : :obj:`Timestamp` or :obj:`str`, optional
            stop time of data. If None, then the last available time stamp 
            in this data object is used (i.e. :attr:`stop_time`)
            
        Returns
        --------
        tuple
            2-element tuple, containing
            
            -list of filepaths matching variable name, ts_type and either of \
            the years specified by years_to_load
            - str specifying ts_type of files
            
        Raises
        ------
        IOError 
            if not files could be found
        """
        try:
            files = self.find_var_files_in_timeperiod(var_name, ts_type_init,
                                                      start_time, stop_time)
            return (files, ts_type_init)
        except DataCoverageError as e:
            self.logger.warning('No file match for ts_type {}. Error: {}\n\n '
                                'Trying other available ts_types {}'
                                .format(ts_type_init, repr(e), self.ts_types))
            for ts_type in self.ts_types:
                if not ts_type == ts_type_init: #this already did not work
                    try:
                        files = self.find_var_files_in_timeperiod(var_name, 
                                                                  ts_type,
                                                                  start_time,
                                                                  stop_time)
                        return (files, ts_type)
                    
                    except DataCoverageError as e:
                        self.logger.warning(repr(e))
        raise DataCoverageError("No files could be found for dataset {}, "
                                "variable {}, ts_types {}".format(self.name, 
                                                                  var_name, 
                                                                  self.ts_types))
                        
    def find_var_files_in_timeperiod(self, var_name, ts_type,
                                     start_time=None, stop_time=None):
        """Find all files that match variable, time period and temporal res.
        
        Parameters
        ----------
        var_name : str
            variable name
        ts_type : str
            temporal resolution of data
        start_time : :obj:`Timestamp` or :obj:`str`, optional
            start time of data. If None, then the first available time stamp 
            in this data object is used (i.e. :attr:`start_time`)
        stop_time : :obj:`Timestamp` or :obj:`str`, optional
            stop time of data. If None, then the last available time stamp 
            in this data object is used (i.e. :attr:`stop_time`)
            
        Returns
        --------
        list
            list of filepaths matching variable name, ts_type and either of the
            years specified by years_to_load
            
        Raises
        ------
        IOError 
            if no files could be found
        """
        match_files = []
        
        years_to_load = self.get_years_to_load(start_time, stop_time)
        for year in years_to_load:
            if CONST.MIN_YEAR <= year <= CONST.MAX_YEAR:
                # search for filename in self.files using ts_type as default ts size
                for _file in self.files:
                    #new file naming convention (aerocom3)
                    match_mask = self.file_convention.string_mask(var_name,
                                                                  year, 
                                                                  ts_type)
                    
                    if re.match(match_mask, _file):
                        match_files.append(_file)
                        self.logger.debug("FOUND MATCH: {}".format(basename(_file)))

            else:
                self.logger.warning('Ignoring data from year {}. Year is out of '
                                    'allowed bounds ({:d} - {:d})'
                                    .format(year, CONST.MIN_YEAR, CONST.MAX_YEAR))
           
        if len(match_files) == 0:
            raise DataCoverageError("No files could be found for dataset {}, "
                                    "variable {}, ts_type {} and years {}"
                                    .format(self.name, 
                                            var_name, ts_type, years_to_load))
                
        self.match_files = match_files
        return match_files
    
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
            if concatenation of all cubes failed (catch this error using 
            :func:`concatenate_possible_cubes` which returns an instance 
            of :class:`CubeList` with results)
        """
# =============================================================================
#         for cube in cubes:
#             name = cube.standard_name or cube.long_name
#             if name is None:
#                 cube.long_name = 'UNDEFINED'
#                 self.logger.warn('Cube {} does not contain standard_name or '
#                                  'long_name attribute. Setting to UNDEFINED '
#                                  'so that iris.concatenate wont get confused'
#                                  .format(cube))
# =============================================================================
# =============================================================================
#                 raise NetcdfError('Either standard_name or long_name must be '
#                                   'defined in all cubes for iris.concatenate '
#                                   'to work')
# =============================================================================
        
        return concatenate_iris_cubes(cubes, error_on_mismatch=True)
    
    def concatenate_possible_cubes(self, cubes):
        """Concatenate list of cubes into one cube
        
        Note
        ----
        Warns, if all input cubes could be merged into single cube (because
        in this case, :func:`concatenate_cubes` should be used)
        
        Parameters
        ----------
        CubeList
            list of individual cubes
        
        Returns
        -------
        CubeList
            list of cubes that could be concatenated
        
        Raises
        ------
        iris.exceptions.ConcatenateError
            if call or :func:`iris._concatenate.concatenate` did not return
            instance of :class:`iris.cube.CubeList` or of 
            :class:`iris.cube.Cube`
        """
        cubes_concat = concatenate_iris_cubes(cubes, error_on_mismatch=False)
        if isinstance(cubes_concat, iris.cube.Cube):
            self.logger.warning('Successfully concatenated all input cubes into '
                           'single Cube, returning single cube as CubeList. '
                           'Please use method concatenate_cubes')
            cubes_concat = iris.cube.CubeList(cubes_concat)
        if not isinstance(cubes_concat, iris.cube.CubeList):
            raise iris.exceptions.ConcatenateError('Unexpected error please '
                                                   'debug')
        return cubes_concat
    
    
    
    def read_var(self, var_name, start_time=None, stop_time=None, 
                 ts_type=None, flex_ts_type=True):
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
        start_time : :obj:`Timestamp` or :obj:`str`, optional
            start time of data import (if valid input, then the current 
            :attr:`start_time` will be overwritten)
        stop_time : :obj:`Timestamp` or :obj:`str`, optional
            stop time of data import (if valid input, then the current 
            :attr:`start_time` will be overwritten)
        ts_type : str
            string specifying temporal resolution (choose from 
            "hourly", "3hourly", "daily", "monthly"). If None, prioritised 
            of the available resolutions is used
        flex_ts_type : bool
            if True and if applicable, then another ts_type is used in case 
            the input ts_type is not available for this variable
            
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
        ts_type = self._check_ts_type(ts_type)
        
        if var_name not in self.vars:
            raise VarNotAvailableError("Error: variable {} not found in files "
                                       "contained in model directory: {}"
                                       .format(var_name, self.data_dir))
        
        data = self._load_var(var_name, ts_type, start_time, stop_time,
                              flex_ts_type)
        
        # crop cube in time (if applicable)
        crop_time = False
        crop_time_range = [self.start_time, self.stop_time]
        if start_time is not None:
            crop_time = True
            crop_time_range[0] = to_pandas_timestamp(start_time)
        elif self._start_time is not None:
            crop_time = True
            crop_time_range[0] = self._start_time
        if stop_time is not None:
            crop_time = True
            crop_time_range[1] = to_pandas_timestamp(stop_time)
        elif self._stop_time is not None:
            crop_time = True
            crop_time_range[1] = self._stop_time
            
        if crop_time:
            self.logger.info("Applying temporal cropping of result cube")
            data = data.crop(time_range=crop_time_range)
        
        if var_name in self.data:
            self.logger.warning("Warning: Data for variable {} already exists "
                           "and will be overwritten".format(var_name))
        self.data[var_name] = data
        
        return data
        
                
    def read(self, var_names=None, start_time=None, stop_time=None, 
             ts_type=None, flex_ts_type=True, 
             require_all_vars_avail=False):
        """Read all variables that could be found 
        
        Reads all variables that are available (i.e. in :attr:`vars`)
        
        Parameters
        ----------
        var_names : :obj:`list` or :obj:`str`
            variables that are supposed to be read
        start_time : :obj:`Timestamp` or :obj:`str`, optional
            start time of data import (if valid input, then the current 
            :attr:`start_time` will be overwritten)
        stop_time : :obj:`Timestamp` or :obj:`str`, optional
            stop time of data import (if valid input, then the current 
            :attr:`start_time` will be overwritten)
        ts_type : str
            string specifying temporal resolution (choose from 
            "hourly", "3hourly", "daily", "monthly"). If None, prioritised 
            of the available resolutions is used
        flex_ts_type : bool
            if True and if applicable, then another ts_type is used in case 
            the input ts_type is not available for this variable
        require_all_vars_avail : bool
            if True, it is strictly required that all input variables are 
            available. 
        
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

        if var_names is None:
            var_names = self.vars
        elif isinstance(var_names, str):
            var_names = [var_names]
        elif not isinstance(var_names, list):
            raise IOError("Invalid input for var_names {}. Need string or list "
                          "of strings specifying var_names to load. You may "
                          "also leave it empty (None) in which case all "
                          "available variables are loaded".format(var_names))
        if require_all_vars_avail:
            if not all([var in self.vars for var in var_names]):
                raise VarNotAvailableError('One or more of the specified vars '
                                        '({}) is not available in {} database. '
                                        'Available vars: {}'.format(
                                        var_names, self.name, 
                                        self.vars))
        var_names = list(np.intersect1d(self.vars, var_names))
        if len(var_names) == 0:
            raise VarNotAvailableError('None of the desired variables is '
                                        'available in {}'.format(self.name))
        data = []
        for var in var_names:
            try:
                data.append(self.read_var(var, start_time, stop_time, ts_type,
                                          flex_ts_type))
            except (VarNotAvailableError, DataCoverageError) as e:
                self.logger.warning(repr(e))
        return tuple(data)
# =============================================================================
#             except Exception as e:
#                 self.logger.exception('Failed to read variable {} ({})\n'
#                                       'Error message: {}'.format(var,
#                                                       self.name, 
#                                                       repr(e)))
# =============================================================================
        
    
# =============================================================================
#     def read_individual_years(self, var_names, years_to_load, 
#                               ts_type=None, 
#                               require_all_years_avail=False,
#                               require_all_vars_avail=False,
#                               flex_ts_type=True):
#         """Read individual years into instances of :class:`GriddedData`
#         
#         Note
#         ----
#         Other than methods :func:`read_var` and :func:`read`, this method does
#         not write into :attr:`data` but into :attr:`data_yearly`. Since for 
#         each provided variable, multiple years are loaded, the structure of
#         :attr:`data_yearly` is a nested dictionary and the yearly data may
#         be accessed as shown in the below example.
#         
#         Parameters
#         ----------
#         var_names : :obj:`list` or :obj:`str`
#             variables that are supposed to be read
#         years_to_load : list
#             list specifying the years to be loaded
#         ts_type : str
#             string specifying temporal resolution (choose from 
#             "hourly", "3hourly", "daily", "monthly"). If None, prioritised 
#             of the available resolutions is used
#         require_all_years_avail : bool
#             if True, it is strictly required that all input years are 
#             available. 
#         require_all_vars_avail : bool
#             if True, it is strictly required that all input variables are 
#             available. 
#         
#         Returns
#         -------
#         dict
#             nested dictionary dictionary containing the results for each 
#             variable and for each year
#             
#         Raises 
#         ------
#         YearNotAvailableError
#             1. if ``require_all_years_avail=True`` and one or more of the provided 
#             years is not available in this class
#             2. if none of the required years is available in this object
#         VarNotAvailableError
#             1. if ``require_all_vars_avail=True`` and one or more of the 
#             desired variables is not available in this class
#             2. if ``require_all_vars_avail=True`` and if none of the input 
#             variables is available in this object
#         """
#         ts_type = self._check_ts_type(ts_type)
#         if not isinstance(years_to_load, (list, np.ndarray)):
#             year = int(years_to_load)
#             if not CONST.MIN_YEAR <= year <= CONST.MAX_YEAR:
#                 raise IOError('Invalid input for years_to_load')
#             years_to_load = [year]
#         if require_all_years_avail:
#             if not all([year in self.years for year in years_to_load]):
#                 raise YearNotAvailableError('One or more of the specified years '
#                                         '({}) is not available in {} database. '
#                                         'Available years: {}'.format(
#                                         years_to_load, self.name, 
#                                         self.years))
#         years_to_load = np.intersect1d(self.years, years_to_load)
#         if len(years_to_load) == 0:
#             raise YearNotAvailableError('None of the provided years is '
#                                         'available in {}'.format(self.name))
#         
#         if require_all_vars_avail:
#             if not all([var in self.vars for var in var_names]):
#                 raise VarNotAvailableError('One or more of the specified vars '
#                                         '({}) is not available in {} database. '
#                                         'Available vars: {}'.format(
#                                         var_names, self.name, 
#                                         self.vars))
#         var_names = np.intersect1d(self.vars, var_names)
#         if len(var_names) == 0:
#             raise VarNotAvailableError('None of the desired variables is '
#                                         'available in {}'.format(self.name))
#             
#         for var in var_names:
#             if not var in self.data_yearly:
#                 self.data_yearly[var] = od()
#                 
#             for year in years_to_load:
#                 try:
#                     data = self._load_var(var, ts_type, year, flex_ts_type)
#                     if year in self.data_yearly[var]:
#                         self.logger.warning('Individual data of year {} and var {} '
#                                             'already exists and will be '
#                                             'overwritten'.format(year, var))
#                     self.data_yearly[var][year] = data
#                 except Exception as e:
#                     self.logger.exception(repr(e))
#         return self.data_yearly
# =============================================================================
    
    def _load_files(self, files, var_name, quality_check=True):
        """Load list of files containing variable to read into Cube instances
        
        Parameters
        ----------
        var_name : str
            name of variable to read
        files : list
            list of netcdf files that contain this variable
        
        Returns
        -------
        CubeList
            list of loaded Cube instances
        """
        # read files using iris
        cubes = iris.cube.CubeList()
        loaded_files = []
        for _file in files:
            try:
                cube = load_cube_custom(_file, var_name,
                                        file_convention=self.file_convention)
                cubes.append(cube)
                loaded_files.append(_file)
            except Exception as e:
                msg = ("Failed to load {} as Iris cube. Error: {}"
                       .format(_file, repr(e)))
                self.logger.warning(msg)
                self.read_errors[datetime.now()] = msg
                if CONST.WRITE_FILEIO_ERR_LOG:
                    add_file_to_log(_file, msg)
                    
                    
        
        if len(loaded_files) == 0:
            err_str = ''
            for error in self.read_errors.values():
                err_str += '\n{}'.format(msg)
            raise IOError("None of the files found for variable {} "
                          "could be loaded. Errors: {}".format(self.name,
                                                               err_str))
    
        self.cubes[var_name] = cubes
        self.loaded_files[var_name] = loaded_files
        return cubes
    
    def _load_var(self, var_name, ts_type, start_time=None, stop_time=None,
                  flex_ts_type=True):
        """Find files corresponding to input specs and load into GriddedData
        
        Parameters
        ----------
        var_name : str
            variable to load
        """
        
        if flex_ts_type:
            match_files, ts_type = self.find_var_files_flex_ts_type(var_name, 
                                                                    ts_type,
                                                                    start_time,
                                                                    stop_time)
        else:
            match_files = self.find_var_files_in_timeperiod(var_name, 
                                                            ts_type, 
                                                            start_time,
                                                            stop_time)
        
        cube_list = self._load_files(match_files, var_name)
    
        if len(cube_list) > 1:
            try:
                cube = self.concatenate_cubes(cube_list)
            except iris.exceptions.ConcatenateError:
                raise NotImplementedError('Can not yet handle partial '
                                          'concatenation in pyaerocom')
        else:
            cube = cube_list[0]
        
        from_files = [f for f in self.loaded_files[var_name]]    
        return GriddedData(input=cube, 
                           from_files=from_files,
                           name=self.name, 
                           ts_type=ts_type)
    
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
            raise ValueError("No data found for variable %s" %var_name)
        return self.data[var_name]
    
    def __str__(self):
        head = "Pyaerocom {}".format(type(self).__name__)
        s = ("\n{}\n{}\n"
             "Model ID: {}\n"
             "Data directory: {}\n"
             "Available variables: {}\n"
             "Available years: {}\n"
             "Available time resolutions {}\n".format(head, 
                                                      len(head)*"-",
                                                      self.name,
                                                      self.data_dir,
                                                      self.vars, 
                                                      self.years,
                                                      self.ts_types))
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
    names : list
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
    >>> print(read.names)
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
    # "private attributes (defined with one underscore). These may be 
    # controlled using getter and setter methods (@property operator, see 
    # e.g. definition of def start_time below)
    _start_time = None
    _stop_time = None
    def __init__(self, names, start_time=None, stop_time=None):
        
        if isinstance(names, str):
            names = [names]
        if not isinstance(names, list) or not all([isinstance(x, str) for x in names]):
            raise IllegalArgumentError("Please provide string or list of strings")
    
        self.names = names
        #: dictionary containing instances of :class:`ReadGridded` for each
        #: datset
        self.results = od()
        
        # only overwrite if there is input, note that the attributes
        # start_time and stop_time are defined below as @property getter and
        # setter methods, that ensure that the input is convertible to 
        # pandas.Timestamp
        if start_time:
            self.start_time = start_time
        if stop_time:
            self.stop_time = stop_time
        
        self.init_results()
        
    @property
    def start_time(self):
        """Start time for the data import
        
        Note      
        ----
        If input is not :class:`pandas.Timestamp`, it must be convertible 
        into :class:`pandas.Timestamp` (e.g. "2012-1-1")
        """
        return self._start_time
    
    @start_time.setter
    def start_time(self, value):
        if not isinstance(value, str):
            try:
                value = str(value)
            except:
                raise ValueError("Failed to convert non-string input for "
                                 "time stamp into string")
        if not isinstance(value, pd.Timestamp):    
            try:
                value = pd.Timestamp(value)
            except:
                raise ValueError("Failed to convert input value to pandas "
                                  "Timestamp: %s" %value)
        self._start_time = value
            
    @property
    def stop_time(self):
        """Stop time for the data import
        
        Note      
        ----
        If input is not :class:`pandas.Timestamp`, it must be convertible 
        into :class:`pandas.Timestamp` (e.g. "2012-1-1")
        
        """
        return self._stop_time

    @stop_time.setter
    def stop_time(self, value):
        if not isinstance(value, str):
            try:
                value = str(value)
            except:
                raise ValueError("Failed to convert non-string input for "
                                 "time stamp into string")
        if not isinstance(value, pd.Timestamp):  
            try:
                value = pd.Timestamp(value)
            except:
                raise ValueError("Failed to convert input value to pandas "
                                  "Timestamp: %s" %value)
        self._stop_time = value
    
    def init_results(self):
        """Initiate the reading classes for each dataset
        
        Creates and initates instance of :class:`ReadGridded` for each 
        dataset name specified in attr. :attr:`names`.
        
        Raises
        ------
        Exception 
            if one of the reading classes cannot be instantiated properly. The
            type of Exception 
        """
        self.results = od()
        for name in self.names:
            self.results[name] = ReadGridded(name, 
                                             self.start_time, 
                                             self.stop_time)
    
        
    def read(self, var_names, start_time=None, stop_time=None,
             ts_type=None):
        """High level method to import data for multiple variables and models
        
        Parameters
        ----------
        var_names : :obj:`str` or :obj:`list`
            string IDs of all variables that are supposed to be imported
        start_time : :obj:`Timestamp` or :obj:`str`, optional
            start time of data import (if valid input, then the current 
            :attr:`start_time` will be overwritten)
        stop_time : :obj:`Timestamp` or :obj:`str`, optional
            stop time of data import (if valid input, then the current 
            :attr:`start_time` will be overwritten)
        ts_type : str
            string specifying temporal resolution (choose from 
            "hourly", "3hourly", "daily", "monthly").If None, prioritised 
            of the available resolutions is used
            
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
        if start_time:
            self.start_time = start_time
        if stop_time:
            self.stop_time = stop_time
    
        for name, reader in self.results.items():
            try:
                reader.read(var_names, start_time, stop_time, ts_type)
            except Exception as e:
                reader.logger.exception('Failed to read data of {}\n'
                                        'Error message: {}'.format(name,
                                                                   repr(e)))
        return self.results
    
    def read_individual_years(self, var_names, years_to_load, 
                              ts_type=None, require_all_years_avail=False,
                              require_all_vars_avail=False):
        """Read individual years into instances of :class:`GriddedData`
        
        Calls :func:`read_individual_years` from :class:`ReadGridded` for each
        of the datasets in this object.
        
        Parameters
        ----------
        var_names : :obj:`list` or :obj:`str`
            variables that are supposed to be read
        years_to_load : list
            list specifying the years to be loaded
        ts_type : str
            string specifying temporal resolution (choose from 
            "hourly", "3hourly", "daily", "monthly"). If None, prioritised 
            of the available resolutions is used
        require_all_years_avail : bool
            if True, it is strictly required that all input years are 
            available. 
        require_all_vars_avail : bool
            if True, it is strictly required that all input variables are 
            available.
            
        
        Returns
        -------
        dict
            nested dictionary dictionary containing the results for each 
            variable and for each year
            
        Raises 
        ------
        YearNotAvailableError
            1. if ``require_all_years_avail=True`` and one or more of the provided 
            years is not available in this class
            2. if none of the required years is available in either of the 
            reading classes for the individual models
        VarNotAvailableError
            1. if ``require_all_vars_avail=True`` and one or more of the 
            desired variables is not available in this class
            2. if ``require_all_vars_avail=True`` and if none of the input 
            variables is available in this object
        
        """
        for name, reader in self.results.items():
            reader.read_individual_years(var_names, years_to_load, ts_type,
                                         require_all_years_avail,
                                         require_all_vars_avail)
            
        return self.results
    
    def __getitem__(self, name):
        """Try access import result for one of the models
        
        Parameters
        ----------
        name : str
            string specifying model that is supposed to be extracted
        
        Returns
        -------
        ReadGridded
            the corresponding read class for this model
            
        Raises
        -------
        ValueError
            if results for ``name`` are not available
        """
        if isinstance(name, int):
            name = self.names[name]
        if not name in self.results:
            raise ValueError("No data found for name %s" %name)
        return self.results[name]
    
    def __str__(self):
        head = "Pyaerocom %s" %type(self).__name__
        s = ("\n%s\n%s\n"
             "Model IDs: %s\n" %(head, len(head)*"-", self.names))
        if self.results:
            s += "\nLoaded data:"
            for name, read in self.results.items():
                s += "\n%s" %read
        return s
    
if __name__=="__main__":
    r = ReadGridded('ECMWF_CAMS_REAN')
    data = r.read_var('od550aer')
    
    
    read = ReadGridded("ECHAM6-SALSA_AP3-CTRL2015")
    
    
    data = read.read_var("od550aer", "2009", "2011", ts_type="monthly")
    
    read_caliop = ReadGridded('CALIOP3')
    alt = read_caliop.read_var('z3d', ts_type='monthly')
    ec532aer = read_caliop.read_var('ec5323Daer', ts_type='monthly')

    

