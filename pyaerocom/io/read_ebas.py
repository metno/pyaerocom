################################################################
# read_aeronet_invv2.py
#
# read Aeronet inversion V2 data
#
# this file is part of the pyaerocom package
#
#################################################################
# Created 20180629 by Jan Griesfeller for Met Norway
#
# Last changed: See git log
#################################################################

# Copyright (C) 2018 met.no
# Contact information:
# Norwegian Meteorological Institute
# Box 43 Blindern
# 0313 OSLO
# NORWAY
# E-mail: jan.griesfeller@met.no
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA

import os
from copy import deepcopy
import numpy as np
from collections import OrderedDict as od
from pyaerocom import const
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom import StationData
from pyaerocom import UngriddedData
from pyaerocom.io.ebas_varinfo import EbasVarInfo
from pyaerocom.io.ebas_file_index import EbasFileIndex
from pyaerocom.io import EbasNasaAmesFile
from pyaerocom.exceptions import (VariableDefinitionError, NotInFileError,
                                  EbasFileError, DataUnitError)

class ReadEbas(ReadUngriddedBase):
    """Interface for reading EBAS data

    Parameters
    ----------
    dataset_to_read
        string specifying either of the supported datasets that are defined 
        in ``SUPPORTED_DATASETS``
        
    TODO
    ----
    Check for negative values vs. detection limit
    """
    
    #: version log of this class (for caching)
    __version__ = "0.07_" + ReadUngriddedBase.__baseversion__
    
    #: preferred order of data statistics. Some files may contain multiple 
    #: columns for one variable, where each column corresponds to one of the
    #: here defined statistics that where applied to the data. This attribute
    #: is only considered for ebas variables, that have not explicitely defined
    #: what statistics to use (and in which preferred order, if appicable).
    #: Reading preferences for all Ebas variables are specified in the file
    #: ebas_config.ini in the data directory of pyaerocom
    PREFER_STATISTICS = ['arithmetic mean',
                         'median']
    
    IGNORE_STATISTICS = ['percentile:15.87',
                         'percentile:84.13']
    #: Wavelength tolerance in nm for reading of variables. If multiple matches
    #: occure, the closest wavelength to the desired wavelength is chosen
    #: e.g. if 50 and for variable at 550nm, accept everything in interval
    #: {500, 600}
    WAVELENGTH_TOL_NM = 50
    
    #: Name of dataset (OBS_ID)
    DATASET_NAME = const.EBAS_MULTICOLUMN_NAME
    
    
    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [const.EBAS_MULTICOLUMN_NAME]
    
    TS_TYPE = 'undefined'
    
    # TODO: check and redefine 
    #: default variables for read method
    DEFAULT_VARS = ['absc550aer', # light absorption coefficient
                    'absc550lt1aer',
                    'scatc550aer',
                    'scatc550lt1aer',
                    ] # light scattering coefficient
    
    #: Temporal resolution codes that (so far) can be understood by pyaerocom
    TS_TYPE_CODES = {'1h'   :   'hourly',
                     '1d'   :   'daily',
                     '1mo'  :   'monthly'}
    
    # list of all available resolution codes (extracted from SQL database)
    # 1d 1h 1mo 1w 4w 30mn 2w 3mo 2d 3d 4d 12h 10mn 2h 5mn 6d 3h 15mn
    
    #: List of variables that are provided by this dataset (will be extended 
    #: by auxiliary variables on class init, for details see __init__ method of
    #: base class ReadUngriddedBase)
    def __init__(self, dataset_to_read=None):
        super(ReadEbas, self).__init__(dataset_to_read)
        #: loaded instances of aerocom variables (instances of 
        #: :class:`Variable` object, is written in get_file_list
        self.loaded_aerocom_vars = {}
        
        #: original file lists retrieved for each variable individually using
        #: SQL request. Since some of the files in the lists for each variable
        #: might occur in multiple lists, these are merged into a single list 
        #: self.files and information about which variables are to be extracted 
        #: for each file is stored in attribute files_contain
        
        #: Originally retrieved file lists from SQL database, for each variable
        #: individually
        self._lists_orig = {}
        
        #: this is filled in method get_file_list and specifies variables 
        #: to be read from each file
        self.files_contain = []
        
        #: Interface to access aerocom variable information (instance of class
        #: AllVariables)
        self.aerocom_vars = const.VAR_PARAM
        
        #: EBAS I/O variable information
        self._ebas_vars = EbasVarInfo.PROVIDES_VARIABLES()
        
        #: SQL database interface class used to retrieve file paths for vars
        self.file_index = EbasFileIndex()
        
    @property
    def _FILEMASK(self):
        raise AttributeError("Irrelevant for EBAS implementation, since SQL "
                             "database is used for finding valid files")
    @property
    def NAN_VAL(self):
        """Irrelevant for implementation of EBAS I/O"""
        raise AttributeError("Irrelevant for EBAS implementation: Info about "
                             "invalid measurements is extracted from header of "
                             "NASA Ames files for each variable individually ")
    @property
    def PROVIDES_VARIABLES(self):
        """List of variables provided by the interface"""
        return self._ebas_vars

    def _merge_lists(self, lists_per_var):
        """Merge dictionary of lists for each variable into one list
        
        Note
        ----
        In addition to writing the retrieved file list into :attr:`files`, this 
        method also fills the list :attr:`files_contain` which (by index)
        defines variables to read for each file path in :attr:`files`
        
        Parameters
        ----------
        lists_per_var : dict
            dictionary containing file lists (values) for a set of variables
            (keys)
        
        Returns
        -------
        list
            merged file list (is also written into :attr:`files`)
        """
        # original lists are modified, so make a copy of them
        lists = deepcopy(lists_per_var)
        mapping = {}
        for var, lst in lists.items():
            for fpath in lst:
                if fpath in mapping:
                    raise Exception('FATAL: logical error -> this should not occur...')
                mapping[fpath] = [var]
                for other_var, other_lst in lists.items():
                    if not var == other_var:
                        try:
                            other_lst.pop(other_lst.index(fpath))
                            mapping[fpath].append(other_var)
                        except ValueError:
                            pass
        self.logger.info('Number of files to read reduced to {}'.format(len(mapping)))
        files, files_contain = [], []
        for path, contains_vars in mapping.items():
            files.append(path)
            files_contain.append(contains_vars)
        self.files = files
        self.files_contain = files_contain
        return files
    
    def get_file_list(self, vars_to_retrieve=None):
        """Get list of files for all variables to retrieve
        
        Note
        ----
        Other than in other implementations of the base class, this 
        implementation returns a dictionary containing file lists for each 
        of the specified variables. This is because in EBAS, some of the 
        variables require additional specifications to the variable name, such
        as the EBAS matrix or the instrument used. For instance, the EBAS
        variable *sulphate_total* specifies either sulfate concentrations in
        precipitable water (EBAS matrix: precip) or in air (e.g. matrix aerosol,
        pm1, pm10 ...)
        
        
        Parameters
        ----------
        vars_to_retrieve : list
            list of variables that are supposed to be loaded
            
        Returns
        -------
        list 
            unified list of file paths each containing either of the specified 
            variables
        """
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
            
        self.logger.info('Fetching data files. This might take a while...')
        
        db = self.file_index
        files_vars = {}
        totnum = 0
        for var in vars_to_retrieve:
            if not var in self.PROVIDES_VARIABLES:
                raise AttributeError('No such variable {}'.format(var))
            info = EbasVarInfo(var)
            if info.requires is not None:
                raise NotImplementedError('Auxiliary variables can not yet '
                                          'be handled / retrieved')
            
            filenames = db.get_file_names(info.make_sql_request())
            
            paths = []
            for file in filenames:
                paths.append(os.path.join(const.EBASMC_DATA_DIR, file))
            files_vars[var] = sorted(paths)
            num = len(paths)
            totnum += num
            self.logger.info('{} files found for variable {}'.format(num, var))
        if len(files_vars) == 0:
            raise IOError('No file could be retrieved for either of the '
                          'specified input variables: {}'.format(vars_to_retrieve))
        
        self._lists_orig = files_vars
        files = self._merge_lists(files_vars)
        return files
    
    def _get_var_cols(self, ebas_var_info, data):
        """Get all columns in NASA Ames file matching input Aerocom variable
        
        Note
        ----
        For developers: All Aerocom variable definitions should go into file
        *variables.ini* in pyaerocom data directory. All Ebas variable 
        definitions for each Aerocom variable should go into file 
        *ebas_config.ini* where section names are Aerocom namespace and 
        contain import constraints.
        
        Parameters
        -----------
        ebas_var_info : EbasVarInfo
            EBAS variable information (e.g. for absc550aer)
        data : EbasNasaAmesFile
            loaded EBAS file data
        
        Returns
        -------
        dict
            key value pairs specifying all matches of input variable, where 
            keys are the column index and values are instances of
            :class:`EbasColDef` specifying further information such as unit, 
            or sampling wavelength.
        
        Raises
        ------
        NotInFileError
            if no column in file matches variable specifications
        """
        
        col_matches = []
        
        check_matrix = False if ebas_var_info['matrix'] is None else True
        check_stats = False if ebas_var_info['statistics'] is None else True
        
        for colnum, col_info in enumerate(data.var_defs):
            if col_info.name in ebas_var_info.component: #candidate (name match)
                ok = True 
                if check_matrix:
                    if 'matrix' in col_info:
                        matrix = col_info['matrix']
                    else:
                        matrix = data.matrix
                    if not matrix in ebas_var_info['matrix']:
                        ok = False
                if ok and 'statistics' in col_info:
                    # ALWAYS ignore columns containing statistics flagged in
                    # IGNORE_STATISTICS
                    if col_info['statistics'] in self.IGNORE_STATISTICS:
                        ok = False
                    elif check_stats:
                        if not col_info['statistics'] in ebas_var_info['statistics']:
                            ok=False
                
                if ok:
                    col_matches.append(colnum)
        if len(col_matches) == 0:
            raise NotInFileError("Variable {} could not be found in "
                                 "file".format(ebas_var_info.var_name))
        return col_matches
        
    def _find_best_data_column(self, cols, ebas_var_info, file):
        """Find best match of data column for variable in multiple columns
        
        This method is supposed to be used in case no unique match can be 
        found for a given variable. For instance, if ``absc550aer``
        
        """
        var = ebas_var_info.var_name
        preferred_matrix = None
        idx_best_matrix_found = 9999
        
        matrix_matches = []
        #first find best column match with 
        if ebas_var_info['matrix'] is not None:
            preferred_matrix = ebas_var_info['matrix']
        
        for colnum in cols:
            col_info = file.var_defs[colnum]
            if 'matrix' in col_info:
                if preferred_matrix is None:
                    raise IOError('Data file contains multiple column matches '
                                  'for variable {}, some of which specify '
                                  'different data type matrices. Aerocom '
                                  'import information for this variable, '
                                  'however, does not contain information '
                                  'about preferred matrix. Please resolve '
                                  'by adding preferred matrix information for '
                                  '{} in corresponding section of '
                                  'ebas_config.ini file'.format(var, var))
                matrix = col_info['matrix']
                if matrix in preferred_matrix:
                    idx = preferred_matrix.index(matrix)
                    if idx < idx_best_matrix_found:
                        idx_best_matrix_found = idx
                        matrix_matches = []
                        matrix_matches.append(colnum)
                    elif idx == idx_best_matrix_found:
                        matrix_matches.append(colnum)
                    
        if idx_best_matrix_found == 9999:
            matrix_matches = cols
        
        if len(matrix_matches) == 1:
            return matrix_matches
        
        preferred_statistics = self.PREFER_STATISTICS
        idx_best_statistics_found = 9999
        result_col = []
        if ebas_var_info['statistics'] is not None:
            preferred_statistics = ebas_var_info['statistics']
        for colnum in matrix_matches:
            col_info = file.var_defs[colnum]
            if 'statistics' in col_info:
                stats = col_info['statistics']
            elif 'statistics' in file.meta:
                stats = file.meta['statistics']
            else:
                raise EbasFileError('Cannot infer data statistics for data '
                                    'column {}. Neither column nor file meta '
                                    'specifications include information about '
                                    'data statistics'.format(col_info))
                
            if stats in preferred_statistics:
                idx = preferred_statistics.index(stats)
                if idx < idx_best_statistics_found:
                    idx_best_statistics_found = idx
                    result_col = []
                    result_col.append(colnum)
                elif idx == idx_best_statistics_found:
                    result_col.append(colnum)
        num_matches = len(result_col)
        if num_matches != 1:
            if num_matches == 0:
                raise ValueError('Note for developers: this should not happen, '
                                 'please debug')
            # multiple column matches were found, use the one that contains 
            # less NaNs
            num_invalid = []
            for colnum in result_col:
                num_invalid.append(np.isnan(file.data[:, colnum]).sum())
            result_col = [result_col[np.argmin(num_invalid)]]
# =============================================================================
#             raise EbasFileError('Could not identify unique column for var {}. '
#                                 'Detected multiple matches: {}'.format(
#                                         ebas_var_info.var_name,
#                                         result_col))
# =============================================================================
        return result_col
                    
    def read_file(self, filename, vars_to_retrieve=None, _vars_to_read=None, 
                  _vars_to_compute=None):
        """Read Aeronet file containing results from v2 inversion algorithm

        Todo
        ----
        - Introduce unit check
        
        Parameters
        ----------
        filename : str
            absolute path to filename to read
        vars_to_retrieve : :obj:`list`, optional
            list of str with variable names to read, if None (and if not 
            both of the alternative possible parameters ``_vars_to_read`` and
            ``_vars_to_compute`` are specified explicitely) then the default
            settings are used
        _vars_to_read : :obj:`list`, optional
            private (used in method :func:`read`). List of variables to read 
            (only considered if also ``_vars_to_compute`` is provided)
            
        Returns
        -------
        StationData
            dict-like object containing results
        """
        # implemented in base class
        if _vars_to_read is None or _vars_to_compute is None:
            vars_to_read, vars_to_compute = self.check_vars_to_retrieve(vars_to_retrieve)
        else:
            vars_to_read, vars_to_compute = _vars_to_read, _vars_to_compute
            
        file = EbasNasaAmesFile(filename)

        var_cols = {}
        all_vars = self.aerocom_vars
        ebas_var_info = {}
        for var in vars_to_read:
            if not var in self.loaded_aerocom_vars:
                self.loaded_aerocom_vars[var] = all_vars[var]
            var_info = self.loaded_aerocom_vars[var]
            var_info_ebas = EbasVarInfo(var)
            
            if var_info_ebas['matrix'] is not None:
                if not file.matrix in var_info_ebas['matrix']:
                    continue
            ebas_var_info[var] = var_info_ebas
            try:
                col_matches = self._get_var_cols(var_info_ebas, file)
            except NotInFileError:
                continue
            # init helper variable for finding closest wavelength (if 
            # no exact wavelength match can be found)
            min_diff_wvl = 1e6
            matches = []
            for colnum in col_matches:
                colinfo = file.var_defs[colnum]
                if 'wavelength' in colinfo:
                    wvl = var_info.wavelength_nm
                    if wvl is None:
                        raise VariableDefinitionError('Require wavelength '
                                                      'specification for '
                                                      'Aerocom variable {}'.format(var))
                    wvl_col = colinfo.get_wavelength_nm()
                    wvl_low = wvl - self.WAVELENGTH_TOL_NM
                    wvl_high = wvl + self.WAVELENGTH_TOL_NM
                    # wavelength is in tolerance range
                    if wvl_low <= wvl_col <= wvl_high:
                        wvl_diff = wvl_col - wvl
                        if abs(wvl_diff) < abs(min_diff_wvl):
                            # the wavelength difference of this column to
                            # the desired wavelength of the variable is 
                            # smaller than any of the detected before, so
                            # ignore those from earlier columns by reinit
                            # of the matches dictionary
                            min_diff_wvl = wvl_diff
                            matches = []
                            matches.append(colnum)
                        elif wvl_diff == min_diff_wvl:
                            matches.append(colnum)
                
                elif 'location' in colinfo:
                    raise NotImplementedError('For developers, please '
                                              'check!')
                else:
                    matches.append(colnum)
            if matches:
                # loop was interrupted since exact wavelength match was found
                var_cols[var] = matches
        
        if not len(var_cols) > 0:
            raise NotInFileError('None of the specified variables {} could be '
                                 'found in file {}'.format(vars_to_read,
                                                os.path.basename(filename)))
        
        for var, cols in var_cols.items():
            if len(cols) > 1:
                col = self._find_best_data_column(cols, ebas_var_info[var],
                                                  file)
                var_cols[var] = col
    
        #create empty data object (is dictionary with extended functionality)
        data_out = StationData()
        data_out['filename'] = filename
        data_out.dataset_name = self.DATASET_NAME
        
        
        meta = file.meta
        # write meta information
        tres_code = meta['resolution_code']
        try:
            ts_type = self.TS_TYPE_CODES[tres_code]
        except KeyError:
            self.logger.info('Unkown temporal resolution {}'.format(tres_code))
            ts_type = 'undefined'
        data_out['ts_type'] = ts_type
        # altitude of station
        stat_alt = float(meta['station_altitude'].split(' ')[0])
        try:
            meas_height = float(meta['measurement_height'].split(' ')[0])
        except KeyError:
            meas_height = 0.0
        data_alt = stat_alt + meas_height
            
        
        data_out['stat_lon'] = float(meta['station_longitude'])
        data_out['stat_lat'] = float(meta['station_latitude'])
        data_out['stat_alt'] = stat_alt
        data_out['station_name'] = meta['station_name']
        data_out['PI'] = meta['submitter']
        data_out['altitude'] = data_alt
        data_out['instrument_name'] = meta['instrument_type']
        
        # store the raw EBAS meta dictionary (who knows what for later ;P )
        #data_out['ebas_meta'] = meta
        data_out['var_info'] = {}
        contains_vars = []
        totnum = file.data.shape[0]
        for var, colnums  in var_cols.items():
            if len(colnums) != 1:
                raise Exception('Something went wrong...please debug')
            colnum = colnums[0]
            data = file.data[:, colnum]
            if np.isnan(data).sum() == totnum:
                self.logger.warning('Ignoring data column of variable {}. All '
                                    'values are NaN'.format(var))
                continue
            data_out[var] = data
            data_out['var_info'][var] = file.var_defs[colnum]
            if 'unit' in file.var_defs[colnum]:
                data_out.unit[var] = file.var_defs[colnum]['unit']
            else:
                data_out.unit[var]= file.unit
            contains_vars.append(var)
        
        if len(contains_vars) == 0:
            raise EbasFileError('All data columns of specified input variables '
                                'are NaN in {}'.format(filename))
        data_out['dtime'] = file.time_stamps
        # compute additional variables (if applicable)
        data_out = self.compute_additional_vars(data_out, vars_to_compute)
        contains_vars.extend(vars_to_compute)
        data_out['contains_vars'] = contains_vars
        
        return data_out
    
    def read(self, vars_to_retrieve=None, first_file=None, 
             last_file=None):
        """Method that reads list of files as instance of :class:`UngriddedData`
        
        Parameters
        ----------
        vars_to_retrieve : :obj:`list` or similar, optional,
            list containing variable IDs that are supposed to be read. If None, 
            all variables in :attr:`PROVIDES_VARIABLES` are loaded
        first_file : :obj:`int`, optional
            index of first file in file list to read. If None, the very first
            file in the list is used
        last_file : :obj:`int`, optional
            index of last file in list to read. If None, the very last file 
            in the list is used
            
        Returns
        -------
        UngriddedData
            data object
        """
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
           
        if len(self.files) == 0:
            self.get_file_list(vars_to_retrieve)
        files = self.files
    
        if first_file is None:
            first_file = 0
        if last_file is None:
            last_file = len(files)
        
        files = files[first_file:last_file]
        files_contain = self.files_contain[first_file:last_file]
        self.read_failed = []
        
        data_obj = UngriddedData()
        meta_key = 0.0
        idx = 0
        
        #assign metadata object
        metadata = data_obj.metadata
        meta_idx = data_obj.meta_idx
    
        num_files = len(files)
        disp_each = int(num_files*0.1)
        if disp_each < 1:
            disp_each = 1
            
        vars_to_read, vars_to_compute = self.check_vars_to_retrieve(vars_to_retrieve)
        
        self.files_failed = []
        for i, _file in enumerate(files):
            if i%disp_each == 0:
                print("Reading file {} of {} ({})".format(i, 
                                 num_files, type(self).__name__))
            vars_to_read = files_contain[i]
            
            try:
                station_data = self.read_file(_file, _vars_to_read=vars_to_read,
                                              _vars_to_compute=vars_to_compute)
            except (NotInFileError, EbasFileError) as e:
                self.files_failed.append(_file)
                self.logger.warning('Failed to read file {}. '
                                    'Error: {}'.format(os.path.basename(_file),
                                                       repr(e)))
                continue
                
            
            # Fill the metatdata dict
            # the location in the data set is time step dependent!
            # use the lat location here since we have to choose one location
            # in the time series plot
            metadata[meta_key] = od()
            metadata[meta_key].update(station_data.get_meta())
            metadata[meta_key].update(station_data.get_station_coords())
            metadata[meta_key]['dataset_name'] = self.DATASET_NAME
            metadata[meta_key]['ts_type'] = station_data['ts_type']
            metadata[meta_key]['instrument_name'] = station_data['instrument_name']
            metadata[meta_key]['var_info'] = od()
            # this is a list with indices of this station for each variable
            # not sure yet, if we really need that or if it speeds up things
            meta_idx[meta_key] = {}
            
            num_times = len(station_data['dtime'])
            
            #access array containing time stamps
            # TODO: check using index instead (even though not a problem here 
            # since all Aerocom data files are of type timeseries)
            times = np.float64(station_data['dtime'])
            
            totnum = num_times * len(station_data.contains_vars)
            
            #check if size of data object needs to be extended
            if (idx + totnum) >= data_obj._ROWNO:
                #if totnum < data_obj._CHUNKSIZE, then the latter is used
                data_obj.add_chunk(totnum)
                
            vars_avail = station_data.contains_vars
            for var_idx, var in enumerate(vars_avail):
                if not var in data_obj.unit:
                    data_obj.unit[var] = station_data.unit[var]
                elif station_data.unit[var] != data_obj.unit[var]:
                    raise DataUnitError("Unit mismatch")
                values = station_data[var]
                start = idx + var_idx * num_times
                stop = start + num_times
                
                
                #write common meta info for this station (data lon, lat and 
                #altitude are set to station locations)
                data_obj._data[start:stop, 
                               data_obj._LATINDEX] = station_data['stat_lat']
                data_obj._data[start:stop, 
                               data_obj._LONINDEX] = station_data['stat_lat']
                data_obj._data[start:stop, 
                               data_obj._ALTITUDEINDEX] = station_data['stat_alt']
                data_obj._data[start:stop, 
                               data_obj._METADATAKEYINDEX] = meta_key
                               
                # write data to data object
                data_obj._data[start:stop, data_obj._TIMEINDEX] = times
                data_obj._data[start:stop, data_obj._DATAINDEX] = values
                data_obj._data[start:stop, data_obj._VARINDEX] = var_idx
                
                meta_idx[meta_key][var] = np.arange(start, stop)
                
                var_info = station_data['var_info'][var]
                metadata[meta_key]['var_info'][var] = var_info.to_dict()
                if not var in data_obj.var_idx:
                    data_obj.var_idx[var] = var_idx
            metadata[meta_key]['variables'] = vars_avail
            idx += totnum  
            meta_key = meta_key + 1.
        
        # shorten data_obj._data to the right number of points
        data_obj._data = data_obj._data[:idx]
        data_obj = data_obj.merge_common_meta()
        data_obj.data_revision[self.DATASET_NAME] = self.data_revision
        self.data = data_obj
        return data_obj
    
if __name__=="__main__":
    from pyaerocom import change_verbosity
    change_verbosity('critical')

    reader = ReadEbas()
    
    vars_to_retrieve = ['absc550aer']
    
    files = reader.get_file_list(vars_to_retrieve)
    
    data = reader.read(vars_to_retrieve, last_file=10)
    
    stat_data = data.to_station_data(0)
    
    print(stat_data)    
    print(data)

    idx, meta = data._find_common_meta()
    
    dm = data.merge_common_meta()
    
    sd = dm.to_station_data(0, data_as_series=True)
    
    
    DO_META_TEST = False
    DO_TIME_SAMPLE_TEST = False
    if DO_TIME_SAMPLE_TEST:
        files_failed = []
        has_24h = []
        success = 0
        failed = 0
        file_info = {}
        for file in files[:200]:
            try:
                data = reader.read_file(file)
                days_vs_num = {}
                prev_date= 0 
                for t in data.dtime:
                    date = t.astype('datetime64[D]')
                    if not date == prev_date:
                        if prev_date != 0:
                            if days_vs_num[prev_date] == 24:
                                has_24h.append(True)
                            else:
                                has_24h.append(False)
                                
                        days_vs_num[date] = 1
                    else:
                        days_vs_num[date] += 1
                    prev_date = date
                file_info[file] = days_vs_num
                success += 1
            except NotInFileError:
                failed += 1
                files_failed.append(file)
        for file in files_failed:
            data = EbasNasaAmesFile(file, only_head=True)
            print("File {} contains:\n".format(file))
            for var in data.var_defs:
                if var.is_var:
                    print(repr(var))
            print()
            print()

                
    if DO_META_TEST:
        totnum = len(files)
        failed = 0
        mat_in_head = 0
        mat_in_coldef =  0
        mat_in_both = 0
        mat_in_none = 0
        stat_in_head = 0
        stat_in_coldef = 0
        stat_in_both = 0
        stat_in_none = 0
        for i, f in enumerate(read.files):
            if i%25 == 0:
                print('File {} of {}'.format(i, totnum))
            _mat_in_head = 0
            _mat_in_coldef =  0
            _mat_in_both = 0
            _stat_in_head = 0
            _stat_in_coldef = 0
            _stat_in_both = 0
            try:
                head = EbasNasaAmesFile(f, only_head=True)
                for col in head.var_defs:
                    if 'matrix' in col:
                        _mat_in_coldef = 1
                    if 'statistics' in col:
                        _stat_in_coldef = 1
                if 'matrix' in head.meta:
                    _mat_in_head = 1
                if 'statistics' in head.meta:
                    _stat_in_head = 1
                if _mat_in_coldef and _mat_in_head:
                    _mat_in_both = True
                if _stat_in_coldef and _stat_in_head:
                    _stat_in_both = True
                if not _mat_in_coldef and not _mat_in_head:
                    mat_in_none += 1
                if not _stat_in_coldef and not _stat_in_head:
                    stat_in_none += 1
                mat_in_both += _mat_in_both
                mat_in_coldef += _mat_in_coldef
                mat_in_head += _mat_in_head
                
                stat_in_both += _stat_in_both
                stat_in_coldef += _stat_in_coldef
                stat_in_head += _stat_in_head
                   
            except:
                failed += 1