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

import os, re
from datetime import datetime
import fnmatch
import numpy as np
from collections import OrderedDict as od
from pyaerocom import const
from pyaerocom.mathutils import (compute_scatc550dryaer, 
                                 compute_scatc440dryaer,
                                 compute_scatc700dryaer,
                                 compute_absc550dryaer,
                                 compute_ang4470dryaer_from_dry_scat)
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.io.helpers import _print_read_info
from pyaerocom import StationData
from pyaerocom import UngriddedData
from pyaerocom.io.ebas_varinfo import EbasVarInfo
from pyaerocom.io.ebas_file_index import EbasFileIndex, EbasSQLRequest
from pyaerocom.io.ebas_nasa_ames import EbasNasaAmesFile
from pyaerocom.exceptions import NotInFileError, EbasFileError
from pyaerocom._lowlevel_helpers import BrowseDict

class ReadEbasOptions(BrowseDict):
    """Options for EBAS reading routine
    
    Attributes
    ----------
    prefer_statistics : list
        preferred order of data statistics. Some files may contain multiple 
        columns for one variable, where each column corresponds to one of the
        here defined statistics that where applied to the data. This attribute
        is only considered for ebas variables, that have not explicitely defined
        what statistics to use (and in which preferred order, if applicable).
        Reading preferences for all Ebas variables are specified in the file
        ebas_config.ini in the data directory of pyaerocom.
    ignore_statistics : list
        columns that have either of these statistics applied are ignored for 
        variable data reading.
    wavelength_tol_nm : int
        Wavelength tolerance in nm for reading of (wavelength dependent) 
        variables. If multiple matches occur (e.g. query -> variable at 550nm
        but file contains 3 columns of that variable, e.g. at 520, 530 and 
        540 nm), then the closest wavelength to the queried wavelength is used
        within the specified tolerance level.
    eval_flags : bool
        If True, the flag columns in the NASA Ames files are read and decoded 
        (using :func:`EbasFlagCol.decode`) and the (up to 3 flags for each 
        measurement) are evaluated as valid / invalid using the information 
        in the flags CSV file. The evaluated flags are stored in the 
        data files returned by the reading methods :func:`ReadEbas.read` 
        and :func:`ReadEbas.read_file`.
    keep_aux_vars : bool
        if True, auxiliary variables required for computed variables will be 
        written to the :class:`UngriddedData` object created in 
        :func:`ReadEbas.read` (e.g. if scatc550dryaer is requested, this 
        requires reading of scatc550aer and scatcrh. The latter 2 will be 
        written to the data object if this parameter evaluates to True)
    log_read_stats : bool
        It True, the number of data points that is removed per station (
        dependent on other constraints) is logged in the attribute 
        _read_stats_log
    merge_meta : bool
        if True, then :func:`UngriddedData.merge_common_meta` will be called
        at the end of :func:`ReadEbas.read` (merges common metadata blocks
        together)
    """
    #: Names of options that correspond to reading filter constraints
    _FILTER_IDS = ['prefer_statistics',
                   'wavelength_tol_nm']
    
    def __init__(self):
        
        self.prefer_statistics = ['arithmetic mean', 'median']
        self.ignore_statistics = ['percentile:15.87',
                                  'percentile:84.13']
        
        self.wavelength_tol_nm = 50
        
        self.eval_flags = True
        
        self.keep_aux_vars = False
        
        self.log_read_stats = False
        
        self.merge_meta = False
        
        self.convert_units = True
    
    @property
    def filter_dict(self):
        d = {}
        for n in self._FILTER_IDS:
            d[n] = self[n]
        return d
    
class ReadEbas(ReadUngriddedBase):
    """Interface for reading EBAS data

    Parameters
    ----------
    dataset_to_read
        string specifying either of the supported datasets that are defined 
        in ``SUPPORTED_DATASETS``
        
    TODO
    ----
    - Check for negative values vs. detection limit
    - Read uncertainties from percentiles (where available)
    """
    
    #: version log of this class (for caching)
    __version__ = "0.25_" + ReadUngriddedBase.__baseversion__
    
    #: Name of dataset (OBS_ID)
    DATA_ID = const.EBAS_MULTICOLUMN_NAME
    
    
    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [const.EBAS_MULTICOLUMN_NAME]
    
    TS_TYPE = 'undefined'
    
    MERGE_STATIONS = {'Birkenes' : 'Birkenes II'}
                      #'Trollhaugen'    : 'Troll'}
    # TODO: check and redefine 
    #: default variables for read method
    DEFAULT_VARS = ['absc550aer', # light absorption coefficient
                    'scatc550aer'] # light scattering coefficient
    
    #: Temporal resolution codes that (so far) can be understood by pyaerocom
    TS_TYPE_CODES = {'1mn'  :   'minutely',
                     '1h'   :   'hourly',
                     '1d'   :   'daily',
                     '1w'   :   'weekly',
                     '1mo'  :   'monthly',
                     'mn'   :   'minutely',
                     'h'    :   'hourly',
                     'd'    :   'daily',
                     'w'    :   'weekly',
                     'mo'   :   'monthly'}
    
    
    AUX_REQUIRES = {'scatc550dryaer'    :   ['scatc550aer',
                                             'scatcrh'],
                    'scatc440dryaer'    :   ['scatc440aer',
                                             'scatcrh'],
                    'scatc700dryaer'    :   ['scatc700aer',
                                             'scatcrh'],
                    'absc550dryaer'     :   ['absc550aer',
                                             'abscrh'],
                    'ang4470dryaer'     :   ['scatc440dryaer',
                                             'scatc700dryaer']}
    
    # Specifies which metainformation is supposed to be migrated to computed
    # variable
    AUX_USE_META = {'scatc550dryaer'    :   'scatc550aer',
                    'scatc440dryaer'    :   'scatc440aer',
                    'scatc700dryaer'    :   'scatc700aer',
                    'absc550dryaer'     :   'absc550aer'}
    
    AUX_FUNS = {'scatc440dryaer'    :   compute_scatc440dryaer,
                'scatc550dryaer'    :   compute_scatc550dryaer,
                'scatc700dryaer'    :   compute_scatc700dryaer,
                'absc550dryaer'     :   compute_absc550dryaer,
                'ang4470dryaer'     :   compute_ang4470dryaer_from_dry_scat}
    
    
    IGNORE_WAVELENGTH = ['conceqbc']
    # list of all available resolution codes (extracted from SQLite database)
    # 1d 1h 1mo 1w 4w 30mn 2w 3mo 2d 3d 4d 12h 10mn 2h 5mn 6d 3h 15mn
    
    #: List of variables that are provided by this dataset (will be extended 
    #: by auxiliary variables on class init, for details see __init__ method of
    #: base class ReadUngriddedBase)
    def __init__(self, dataset_to_read=None):
    
        super(ReadEbas, self).__init__(dataset_to_read)
        
        #ReadUngriddedBase.__init__(self, dataset_to_read)
        self.opts = ReadEbasOptions()
        
        #self.opts = ReadEbasOptions()
        #: loaded instances of aerocom variables (instances of 
        #: :class:`Variable` object, is written in get_file_list
        self.loaded_aerocom_vars = {}
        
        #: loaded instances of variables in EBAS namespace (instances of 
        #: :class:`EbasVarInfo` object, is updated in read_file
        self.loaded_ebas_vars = {}
        
        self._filelog = None
        
        self.files_failed = []
        self._read_stats_log = BrowseDict()
        
        #: SQL database interface class used to retrieve file paths for vars
        self.file_index = EbasFileIndex()
        self.sql_requests = []
        
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
        
        self._all_stats = None
    
    @property
    def filelog(self):
        """File logger"""
        if self._filelog is None:
            import logging
            logdir = const.LOGFILESDIR
            logfile = os.path.join(logdir, 'ReadEbas_{}.log'.format(self.__version__))
            fh = logging.FileHandler(logfile)
            logger = logging.getLogger('ebas_io')
            logger.setLevel(logging.DEBUG)
            logger.addHandler(fh)
            self._filelog = logger
        return self._filelog
    
    @property
    def FILE_REQUEST_OPTS(self):
        """List of options for file retrieval"""
        return list(EbasSQLRequest().keys())
    
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
        return EbasVarInfo.PROVIDES_VARIABLES()
    
    @property
    def prefer_statistics(self):
        """List containing preferred statistics columns"""
        return self.opts.prefer_statistics
    
    @property
    def ignore_statistics(self):
        """List containing column statistics keys to be ignored"""
        return self.opts.ignore_statistics
    
    @property
    def wavelength_tol_nm(self):
        """Wavelength tolerance in nm for columns"""
        return self.opts.wavelength_tol_nm
    
    @property
    def log_read_stats(self):
        """Option: if True, then reading info will be logged during read"""
        return self.opts.log_read_stats
    
    @property
    def keep_aux_vars(self):
        """Option: Keep auxiliary variables during reading"""
        return self.opts.keep_aux_vars
    
    @property
    def merge_meta(self):
        """Option: if True, then common meta-data blocks are merged on reading"""
        return self.opts.merge_meta
    
    @property
    def eval_flags(self):
        """Boolean specifying whether to use EBAS flag columns"""
        return self.opts.eval_flags

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
        #lists = deepcopy(lists_per_var)
        lists = lists_per_var
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
    
    @property
    def all_station_names(self):
        """List of all available station names in EBAS database"""
        if self._all_stats is None:
            self._all_stats = self.file_index.ALL_STATION_NAMES
        return self._all_stats
    
    def find_station_matches(self, stats_or_patterns):
        val = stats_or_patterns
        all_stats = self.all_station_names
        stats = []
        if isinstance(val, str):
            val = [val]
        elif isinstance(val, tuple):
            val = [x for x in val]
        
        for name in val:
            if '*' in name: 
                #handle wildcard
                for stat in all_stats:
                    if fnmatch.fnmatch(stat, name):
                        stats.append(stat)
            elif name in all_stats:
                stats.append(name)
            else:
                const.print_log.warning('Ignoring station_names input {}. '
                                        'No match could be found'.format(name))
                
        if not bool(stats):
            raise FileNotFoundError('No EBAS data files could be found for '
                                    'stations {}'.format(stats_or_patterns))
        return list(dict.fromkeys(stats).keys())
    
    def get_file_list(self, vars_to_retrieve=None, **constraints):
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
        **constraints
            further EBAS request constraints deviating from default (default 
            info for each AEROCOM variable can be found in `ebas_config.ini <
            https://github.com/metno/pyaerocom/blob/master/pyaerocom/data/
            ebas_config.ini>`__). For details on possible input parameters 
            see :class:`EbasSQLRequest` (or `this tutorial <http://aerocom.met.no
            /pyaerocom/tutorials.html#ebas-file-query-and-database-browser>`__)
            
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
        const.print_log.info('Retrieving EBAS files for variables\n{}'
                             .format(vars_to_retrieve))
        for var in vars_to_retrieve:
            if not var in self.PROVIDES_VARIABLES:
                raise AttributeError('No such variable {}'.format(var))
            info = EbasVarInfo(var)
            self.loaded_ebas_vars[var] = info

            if 'station_names' in constraints:
                stat_matches = self.find_station_matches(constraints['station_names'])
                constraints['station_names'] = stat_matches
# =============================================================================
#             if not 'data_level' in constraints:
#                 constraints['data_level'] = self.opts.data_level
# =============================================================================

            req = info.make_sql_request(**constraints)
            
            const.logger.info('Retrieving EBAS file list for request:\n{}'
                              .format(req))
            filenames = db.get_file_names(req)
            self.sql_requests.append(req)
            
            paths = []
            for file in filenames:
                paths.append(os.path.join(const.EBASMC_DATA_DIR, file))
            files_vars[var] = sorted(paths)
            num = len(paths)
            totnum += num
            self.logger.info('{} files found for variable {}'.format(num, var))
        if len(files_vars) == 0:
            raise IOError('No file could be retrieved for either of the '
                          'specified input variables: {}'
                          .format(vars_to_retrieve))
        
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
        list
            list specifying column matches
        
        Raises
        ------
        NotInFileError
            if no column in file matches variable specifications
        """
        if ebas_var_info.component is None:
            raise NotInFileError
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
                    # ignore_statistics
                    if col_info['statistics'] in self.ignore_statistics:
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
        
        preferred_statistics = self.prefer_statistics
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
    
    def _add_meta(self, data_out, file):
        meta = file.meta
        name = meta['station_name'].replace('/', ';')
        
        data_out['filename'] = os.path.basename(file.file)
        data_out['data_id'] = self.DATA_ID
        data_out['PI'] = file['data_originator']
        data_out['station_id'] = meta['station_code']
        
        data_out['station_name'] = name
        if name in self.MERGE_STATIONS:
            data_out['station_name'] = self.MERGE_STATIONS[name]
            data_out['station_name_orig'] = name
        else:
            data_out['station_name'] = name
        
        
        # write meta information
        tres_code = meta['resolution_code']
        try:
            ts_type = self.TS_TYPE_CODES[tres_code]
        except KeyError:
            ival = re.findall('\d+', tres_code)[0]
            code = tres_code.split(ival)[-1]
            if not code in self.TS_TYPE_CODES:
                raise NotImplementedError('Cannot handle EBAS resolution code '
                                          '{}'.format(tres_code))
            ts_type = ival + self.TS_TYPE_CODES[code]
            self.TS_TYPE_CODES[tres_code] = ts_type

        data_out['ts_type'] = ts_type
        # altitude of station
        try:
            altitude = float(meta['station_altitude'].split(' ')[0])
        except:
            altitude = np.nan
        try:
            meas_height = float(meta['measurement_height'].split(' ')[0])
        except KeyError:
            meas_height = 0.0
        
        data_alt = altitude + meas_height
            
        # file specific meta information
        #data_out.update(meta)
        data_out['latitude'] = float(meta['station_latitude'])
        data_out['longitude'] = float(meta['station_longitude'])
        data_out['altitude'] = data_alt
        data_out['meas_height'] = meas_height
        data_out['station_altitude'] = altitude
        
        data_out['instrument_name'] = meta['instrument_name']
        data_out['instrument_type'] = meta['instrument_type']
        
        data_out['matrix'] = meta['matrix']
        data_out['revision_date'] = file['revision_date']
        
        setting, land_use, gaw_type, lev =  None, None, None, None
        if 'station_setting' in meta:
            setting = meta['station_setting']
        
        if 'station_land_use' in meta:
            land_use = meta['station_land_use']
            
        if 'station_gaw_type' in meta:
            gaw_type = meta['station_gaw_type']
    
        if 'data_level' in meta:
            try:
                lev = int(meta['data_level'])
            except:
                pass
        
        data_out['station_setting'] = setting
        data_out['station_land_use'] = land_use
        data_out['station_gaw_type'] = gaw_type
        
        # NOTE: may be also defined per column in attr. var_defs
        
        data_out['data_level'] = lev
        
        
        return data_out
     
    def _find_wavelength_matches(self, col_matches, file, var_info):
        """
        """
        min_diff_wvl = 1e6
        matches = []
        # get wavelength of column and tolerance
        wvl = var_info.wavelength_nm
        wvl_low = wvl - self.wavelength_tol_nm
        wvl_high = wvl + self.wavelength_tol_nm
        
        for colnum in col_matches:
            colinfo = file.var_defs[colnum]
            if not 'wavelength' in colinfo:
                const.print_log.warn('Ignoring column {} ({}) in EBAS file for '
                                     'reading var {}: column misses wavelength '
                                     'specification'
                                     .format(colnum, colinfo, var_info))
        
            wvl_col = colinfo.get_wavelength_nm()
            # wavelength is in tolerance range
            if wvl_low <= wvl_col <= wvl_high:
                wvl_diff = wvl_col - wvl
                if abs(wvl_diff) < abs(min_diff_wvl):
                    # the wavelength difference of this column to
                    # the desired wavelength of the variable is 
                    # smaller than any of the detected before, so
                    # ignore those from earlier columns by reinit
                    # of the matches list
                    min_diff_wvl = wvl_diff
                    matches = []
                    matches.append(colnum)
                elif wvl_diff == min_diff_wvl:
                    matches.append(colnum)
        return matches
    
    def find_var_cols(self, vars_to_read, loaded_nasa_ames):
        """Find best-match variable columns in loaded NASA Ames file
        
        For each of the input variables, try to find one or more matches in the 
        input NASA Ames file (loaded data object). If more than one match 
        occurs, identify the best one (an example here is: user wants 
        scatc550aer and file contains scattering coefficients at 530 nm and 
        580 nm: in this case the 530 nm column will be used, cf. also accepted
        wavelength tolerance for reading of wavelength dependent variables
        :attr:`wavelength_tol_nm`).
        
        Parameters
        ----------
        vars_to_read : list
            list of variables that are supposed to be read
        loaded_nasa_ames : EbasNasaAmesFile
            loaded data object
        
        Returns
        -------
        dict
            dictionary specifying the best-match variable column for each 
            of the input variables.
        """
        file = loaded_nasa_ames
        var_cols = {}
        # Loop over all variables that are supposed to be read
        for var in vars_to_read:
            # get corresponding EBAS variable info ...
            ebas_var_info = self.loaded_ebas_vars[var]
            # ... and AeroCom variable definition
            if not var in self.loaded_aerocom_vars:
                self.loaded_aerocom_vars[var] = var_info = const.VARS[var]
            else:
                var_info = self.loaded_aerocom_vars[var]
            # Find all columns in file that match the current variable 
            # There may be multiple matches, e.g. because the variable may
            # be sampled at different wavelenghts or there may be different 
            # statistics applied, or there may be different matrices
            # available (e.g. aerosol, pm10, pm25)
            try:
                col_matches = self._get_var_cols(ebas_var_info, file)
            except NotInFileError:
                const.logger.warning('Variable {} (EBAS name(s): {}) is '
                                     'missing in file {} (start: {})'
                                     .format(var, ebas_var_info.component, 
                                             os.path.basename(file.file),
                                             file.base_date))
                continue
            
            # if AeroCom variable has a wavelength specified, find the column (s)
            # that are closest to this wavelength. There may be multiple column
            # matches, e.g. due to different statistics or matrix columns, these
            # will be sorted out below. 
            if var_info.wavelength_nm is not None and len(col_matches) > 1:
                col_matches = self._find_wavelength_matches(col_matches,
                                                            file, var_info)

            if bool(col_matches):
                # loop was interrupted since exact wavelength match was found
                var_cols[var] = col_matches
        
        if not len(var_cols) > 0:
            raise NotInFileError('None of the specified variables {} could be '
                                 'found in file {}'.format(vars_to_read,
                                                os.path.basename(file.file)))
        
        for var, cols in var_cols.items():
            if len(cols) > 1:
                col = self._find_best_data_column(cols, 
                                                  self.loaded_ebas_vars[var],
                                                  file)
                var_cols[var] = col
        return var_cols
    
    def read_file(self, filename, vars_to_retrieve=None, _vars_to_read=None, 
                  _vars_to_compute=None):
        """Read EBAS NASA Ames file
        
        Parameters
        ----------
        filename : str
            absolute path to filename to read
        vars_to_retrieve : :obj:`list`, optional
            list of str with variable names to read, if None (and if not 
            both of the alternative possible parameters ``_vars_to_read`` and
            ``_vars_to_compute`` are specified explicitely) then the default
            settings are used
            
        Returns
        -------
        StationData
            dict-like object containing results
        """
        # implemented in base class
        if _vars_to_read is None or _vars_to_compute is None:
            (vars_to_read, 
             vars_to_compute) = self.check_vars_to_retrieve(vars_to_retrieve)
        else:
            vars_to_read, vars_to_compute = _vars_to_read, _vars_to_compute
        
        for var in vars_to_read:
            if not var in self.loaded_ebas_vars:
                self.loaded_ebas_vars[var] = EbasVarInfo(var)
            
            if self.loaded_ebas_vars[var].requires is not None:
                for aux_var in self.loaded_ebas_vars[var].requires:
                    if not aux_var in self.loaded_ebas_vars:
                        self.loaded_ebas_vars[aux_var] = EbasVarInfo(aux_var)  
            
        file = EbasNasaAmesFile(filename)
        
        # find columns in NASA Ames file for variables that are to be read
        var_cols = self.find_var_cols(vars_to_read=vars_to_read,
                                      loaded_nasa_ames=file)
        #create empty data object (is dictionary with extended functionality)
        data_out = StationData()
        
        data_out = self._add_meta(data_out, file)
        # store the raw EBAS meta dictionary (who knows what for later ;P )
        #data_out['ebas_meta'] = meta
        data_out['var_info'] = {}
        #totnum = file.data.shape[0]
        for var, colnums  in var_cols.items():
            data_out['var_info'][var] = {}
            if len(colnums) != 1:
                raise Exception('Something went wrong...please debug')
            colnum = colnums[0]
            _col = file.var_defs[colnum]
            data = file.data[:, colnum]
            
            if self.eval_flags:
                invalid = ~file.flag_col_info[_col.flag_col].valid
                data_out.data_flagged[var] = invalid
            sf = self.loaded_ebas_vars[var].scale_factor
            if sf != 1:
                data *= sf
                data_out['var_info'][var]['scale_factor'] = sf
            data_out[var] = data
            
            meta = file.meta
            
            if not 'unit' in _col: #make sure a unit is assigned to data column
                _col['unit']= file.unit
            if 'wavelength' in _col:
                _col['wavelength_nm'] = _col.get_wavelength_nm() 
            # TODO: double-check with NILU if this can be assumed
            if not 'matrix' in _col:
                _col['matrix'] = meta['matrix']
            if not 'statistics' in _col:
                stats = None
                if 'statistics' in meta:
                    stats = meta['statistics']
                _col['statistics'] = stats
            
            
                
            var_info = _col.to_dict()
            data_out['var_info'][var].update(var_info)
            
            if self.opts.convert_units:
                try:
                    data_out = self._convert_varunit_stationdata(data_out, var)
                except:
                    raise
            if self.log_read_stats:
                info = data_out['var_info'][var]
                info['numtot'] = len(data)
                info['numnans'] = np.isnan(data).sum()
            
            
        if len(data_out['var_info']) == 0:
            raise EbasFileError('All data columns of specified input variables '
                                'are NaN in {}'.format(filename))
        data_out['dtime'] = file.time_stamps
        
        # compute additional variables (if applicable)
        data_out = self.compute_additional_vars(data_out, vars_to_compute)
        
            
        return data_out
    
    def _convert_varunit_stationdata(self, sd, var):
        from_unit = sd.var_info[var]['units']
        to_unit = self.loaded_aerocom_vars[var]['units']
        if from_unit != to_unit:
            sd.convert_unit(var, to_unit)    
        return sd
            
                
    def compute_additional_vars(self, data, vars_to_compute):
        """Compute additional variables and put into station data
        
        Note
        ----
        Extended version of :func:`ReadUngriddedBase.compute_additional_vars`
        
        Parameters
        ----------
        data : dict-like
            data object containing data vectors for variables that are required
            for computation (cf. input param ``vars_to_compute``)
        vars_to_compute : list
            list of variable names that are supposed to be computed. 
            Variables that are required for the computation of the variables
            need to be specified in :attr:`AUX_VARS` and need to be 
            available as data vectors in the provided data dictionary (key is
            the corresponding variable name of the required variable).
        
        Returns
        -------
        dict
            updated data object now containing also computed variables
        """
        data = super(ReadEbas, self).compute_additional_vars(data, 
                                                             vars_to_compute)
        for var in vars_to_compute:
            if not var in data: # variable could not be computed -> ignore
                continue
            
            if not var in self.loaded_ebas_vars:
                self.loaded_ebas_vars[var] = EbasVarInfo(var)
            
            data.var_info[var] = self.loaded_ebas_vars[var]

            if var in self.AUX_USE_META:
                to_dict = data['var_info'][var]
                from_var = self.AUX_USE_META[var]
                if from_var in data:
                    from_dict = data['var_info'][from_var]
                    for k, v in from_dict.items():
                        if not k in to_dict or to_dict[k] is None:
                            to_dict[k] = v
                    if self.log_read_stats:
                        # determines the additional number of points that were set 
                        # to NaN while computing the variable. If
                        nandiff = (np.isnan(data[var]).sum() - 
                                   np.isnan(data[from_var]).sum())
                        
                        to_dict['num_nan_diff'] = nandiff
                if from_var in data.data_flagged:
                    data.data_flagged[var] = data.data_flagged[from_var]
                if from_var in data.data_err:
                    data.data_err[var] = data.data_err[from_var]
            if not 'units' in data['var_info'][var]:
                data['var_info'][var]['units'] = self.var_info(var)['units']
        return data
    
    def var_info(self, var_name):
        """Aerocom variable info for input var_name"""
        if not var_name in self.loaded_aerocom_vars:
            self.loaded_aerocom_vars[var_name] = const.VARS[var_name]
        return self.loaded_aerocom_vars[var_name]
    
    def read(self, vars_to_retrieve=None, first_file=None, 
             last_file=None, multiproc=False, files=None, **constraints):
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
        **constraints
            further reading constraints deviating from default (default 
            info for each AEROCOM variable can be found in `ebas_config.ini <
            https://github.com/metno/pyaerocom/blob/master/pyaerocom/data/
            ebas_config.ini>`__). For details on possible input parameters 
            see :class:`EbasSQLRequest` (or `this tutorial <http://aerocom.met.no
            /pyaerocom/tutorials.html#ebas-file-query-and-database-browser>`__)
            
        Returns
        -------
        UngriddedData
            data object
        """    
        
        
        #data_obj.filter_hist.update(constraints)
        for k in list(constraints):
            if k.isupper() and k.lower() in self.opts:
                msg = ('All uppercase reading option for EBAS {} is deprecated '
                       '(but still works). Please use new name of option '
                       'from now on (all lowercase)'.format(k))
                const.print_log.warning(DeprecationWarning(msg))
                self.opts[k.lower()] = constraints.pop(k)
            elif k in self.opts:
                self.opts[k] = constraints.pop(k)
        
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        
        if self.keep_aux_vars:
            (vars_to_read, 
             vars_to_compute) = self.check_vars_to_retrieve(vars_to_retrieve)
            for var in vars_to_read:
                if not var in vars_to_retrieve:
                    vars_to_retrieve.append(var)
        
        if files is None:
            self.get_file_list(vars_to_retrieve, **constraints)
            files = self.files
            files_contain = self.files_contain
        else:
            files_contain = [vars_to_retrieve]*len(files)
            
    
        if first_file is None:
            first_file = 0
        if last_file is None:
            last_file = len(files)
        files = files[first_file:last_file]
        files_contain = files_contain[first_file:last_file]
        
        
        if not multiproc:
            data = self._read_files(files, vars_to_retrieve,
                                    files_contain, constraints)
        else:
            raise NotImplementedError('Coming soon...')
        data.clear_meta_no_data()
# =============================================================================
#             from multiprocessing import Pool, Manager, cpu_count
#             from functools import partial
#             num_proc = cpu_count()
#             func = partial(self._append_read_files, 
#                            vars_to_retrieve=vars_to_retrieve,
#                            files_contain=files_contain,
#                            constraints=constraints)
#             lists = np.array_split(files, num_proc)
#             with Manager() as manager:
#                 result = manager.list()
#                 p = Pool(processes=num_proc)
#                 for sub in lists:
#                     p.apply_async(func, (sub, result))
#                 p.close()
#                 p.join()
#             
#             data = result
# =============================================================================
        return data
    
    def _read_files(self, files, vars_to_retrieve, files_contain, constraints):
        """Helper that reads list of files into UngriddedData
        
        Note
        ----
        This method is not supposed to be called directly but is used in 
        :func:`read` and serves the purpose of parallel loading of data
        """
        data_obj = UngriddedData()
        
        # Add reading options
        filters = self.opts.filter_dict
        filters.update(constraints)
        data_obj._add_to_filter_history(filters)
        
        meta_key = 0.0
        idx = 0
        
        #assign metadata object
        metadata = data_obj.metadata
        meta_idx = data_obj.meta_idx
    
        num_files = len(files)
        disp_each = int(num_files*0.1)
        if disp_each < 1:
            disp_each = 1
         
        # counter that is updated whenever a new variable appears during read
        # (is used for attr. var_idx in UngriddedData object)
        var_count_glob = -1
        last_t = datetime.now()
        for i, _file in enumerate(files):
            if i%disp_each == 0:
                last_t = _print_read_info(i, disp_each, num_files, 
                                          last_t, type(self).__name__,
                                          const.print_log)
            try:
                station_data = self.read_file(_file, 
                                              vars_to_retrieve=files_contain[i])
                
            except (NotInFileError, EbasFileError) as e:
                self.files_failed.append(_file)
                self.logger.warning('Skipping reading of EBAS NASA Ames '
                                    'file: {}. Reason: {}'
                                    .format(_file, repr(e)))
                continue
            except Exception as e:
                const.print_log.warning('Skipping reading of EBAS NASA Ames '
                                        'file: {}. Reason: {}'
                                        .format(_file, repr(e)))

                continue
            
            # Fill the metatdata dict
            # the location in the data set is time step dependent!
            # use the lat location here since we have to choose one location
            # in the time series plot
            metadata[meta_key] = od()
            metadata[meta_key].update(station_data.get_meta(add_none_vals=True))

            if 'station_name_orig' in station_data:
                metadata[meta_key]['station_name_orig'] = station_data['station_name_orig']     
            
            metadata[meta_key]['data_revision'] = self.data_revision
            metadata[meta_key]['var_info'] = od()
            # this is a list with indices of this station for each variable
            # not sure yet, if we really need that or if it speeds up things
            meta_idx[meta_key] = {}
            
            num_times = len(station_data['dtime'])
            
            contains_vars = list(station_data.var_info.keys())
            #access array containing time stamps
            # TODO: check using index instead (even though not a problem here 
            # since all Aerocom data files are of type timeseries)
            times = np.float64(station_data['dtime'])
            
            append_vars = [x for x in np.intersect1d(vars_to_retrieve, 
                                                     contains_vars)]
            
            totnum = num_times * len(append_vars)
            
            #check if size of data object needs to be extended
            if (idx + totnum) >= data_obj._ROWNO:
                #if totnum < data_obj._CHUNKSIZE, then the latter is used
                data_obj.add_chunk(totnum)
                
            for var_count, var in enumerate(append_vars):
                # data values
                values = station_data[var]
                
                # get start / stop index for this data vector
                start = idx + var_count * num_times
                stop = start + num_times
                
                
                if not var in data_obj.var_idx:
                    var_count_glob += 1
                    var_idx = var_count_glob
                else:
                    var_idx = data_obj.var_idx[var]
                
                #write common meta info for this station (data lon, lat and 
                #altitude are set to station locations)
                data_obj._data[start:stop, 
                               data_obj._LATINDEX] = station_data['latitude']
                data_obj._data[start:stop, 
                               data_obj._LONINDEX] = station_data['longitude']
                data_obj._data[start:stop, 
                               data_obj._ALTITUDEINDEX] = station_data['altitude']
                data_obj._data[start:stop, 
                               data_obj._METADATAKEYINDEX] = meta_key
                               
                # write data to data object
                data_obj._data[start:stop, data_obj._TIMEINDEX] = times

                data_obj._data[start:stop, data_obj._DATAINDEX] = values

                data_obj._data[start:stop, data_obj._VARINDEX] = var_idx
                
                if var in station_data.data_flagged:
                    invalid = station_data.data_flagged[var]
                    data_obj._data[start:stop, data_obj._DATAFLAGINDEX] = invalid
                if var in station_data.data_err:
                    errs = station_data.data_err[var]
                    data_obj._data[start:stop, data_obj._DATAERRINDEX] = errs
                    
                var_info = station_data['var_info'][var]
                metadata[meta_key]['var_info'][var] = od()
                metadata[meta_key]['var_info'][var].update(var_info)
                meta_idx[meta_key][var] = np.arange(start, stop)

                if not var in data_obj.var_idx:
                    data_obj.var_idx[var] = var_idx
                    
            metadata[meta_key]['variables'] = append_vars
            idx += totnum  
            meta_key = meta_key + 1.
        
        # shorten data_obj._data to the right number of points
        data_obj._data = data_obj._data[:idx]
        if self.merge_meta:
            data_obj = data_obj.merge_common_meta(ignore_keys=['filename', 
                                                               'PI'])
        #data_obj.data_revision[self.DATA_ID] = self.data_revision
        self.data = data_obj
        
        return data_obj
    
if __name__=="__main__":

    r = ReadEbas()
    

    

    
    
