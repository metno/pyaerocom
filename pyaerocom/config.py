################################################################
# config.py
#
# configuration class for the aerocom python tools 
#
# this file is part of the aerocom_pt package
#
#################################################################
# Created 20171106 by Jan Griesfeller for Met Norway
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

"""
Provides access to pyaerocom specific configuration values
"""

import numpy as np
import os
import getpass
from collections import OrderedDict as od
import pyaerocom.obs_io as obs_io
from pyaerocom.grid_io import GridIO
from pyaerocom._lowlevel_helpers import (list_to_shortstr, 
                                         chk_make_subdir,
                                         check_dir_access,
                                         check_write_access)
from pyaerocom.variable import VarCollection
try:
    from ConfigParser import ConfigParser
except: 
    from configparser import ConfigParser
    

class Config(object):
    """Class containing relevant paths for read and write routines
    
    TODO: write docstring
    """
    
    # NAMES
    # default names of the different obs networks
    # might get overwritten from paths.ini see func read_config
    
    #: Aeronet Sun V2 access names
    AERONET_SUN_V2L15_AOD_DAILY_NAME = 'AeronetSunV2Lev1.5.daily'
    AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME = 'AeronetSun_2.0_NRT'
    AERONET_SUN_V2L2_AOD_DAILY_NAME = 'AeronetSunV2Lev2.daily'
    AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME = 'AeronetSunV2Lev2.AP'
    
    #: Aeronet SDA V2 access names
    AERONET_SUN_V2L2_SDA_DAILY_NAME = 'AeronetSDAV2Lev2.daily'
    AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME = 'AeronetSDAV2Lev2.AP'
    
    # Aeronet V2 inversion products
    AERONET_INV_V2L15_DAILY_NAME = 'AeronetInvV2Lev1.5.daily'
    AERONET_INV_V2L15_ALL_POINTS_NAME = 'AeronetInvV2Lev1.5.AP'
    AERONET_INV_V2L2_DAILY_NAME = 'AeronetInvV2Lev2.daily'
    AERONET_INV_V2L2_ALL_POINTS_NAME = 'AeronetInvV2Lev2.AP'
    
    #: Aeronet Sun V3 access names
    AERONET_SUN_V3L15_AOD_DAILY_NAME = 'AeronetSunV3Lev1.5.daily'
    AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME = 'AeronetSunV3Lev1.5.AP'
    AERONET_SUN_V3L2_AOD_DAILY_NAME = 'AeronetSunV3Lev2.daily'
    AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME = 'AeronetSunV3Lev2.AP'
    
    #: Aeronet SDA V3 access names
    AERONET_SUN_V3L15_SDA_DAILY_NAME = 'AeronetSDAV3Lev1.5.daily'
    AERONET_SUN_V3L15_SDA_ALL_POINTS_NAME = 'AeronetSDAV3Lev1.5.AP'
    AERONET_SUN_V3L2_SDA_DAILY_NAME = 'AeronetSDAV3Lev2.daily'
    AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME = 'AeronetSDAV3Lev2.AP'

    #: Aeronet V3 inversions
    AERONET_INV_V3L15_DAILY_NAME = 'AeronetInvV3Lev1.5.daily'
    AERONET_INV_V3L2_DAILY_NAME = 'AeronetInvV3Lev2.daily'
    
    #: EBAS name
    EBAS_MULTICOLUMN_NAME = 'EBASMC'
    
    #: EEA nmea
    EEA_NAME = 'EEAAQeRep'

    #: Earlinet access name;
    EARLINET_NAME = 'EARLINET'

    #: GAW TAD subset aas et al paper
    GAWTADSUBSETAASETAL_NAME = 'GAWTADsubsetAasEtAl'

    #: DMS
    DMS_AMS_CVO_NAME = 'DMS_AMS_CVO'

    #: Lowest possible year in data
    MIN_YEAR = 0
    #: Highest possible year in data
    MAX_YEAR = 20000

    #: standard names for coordinates
    STANDARD_COORD_NAMES = ['latitude',
                            'longitude',
                            'altitude']
    #: Information specifying default vertical grid for post processing of
    #: profile data. The values are in units of m.
    DEFAULT_VERT_GRID_DEF = od(lower = 0,
                               upper = 15000,
                               step  = 250)
    #: maximum allowed RH to be considered dry
    RH_MAX_PERCENT_DRY = 40
    
    DEFAULT_REG_FILTER = 'WORLD-noMOUNTAINS'
    #: If True, then whenever applicable the time resampling constraints
    #: definted below (OBS_MIN_NUM_RESMAMPLE) are applied to observations when 
    #: resampling in StationData and thus colocation routines. Requires that 
    #: original obs_data is available in a certain regular resolution (or at
    #: least has ts_type assigned to it)
    OBS_APPLY_TIME_RESAMPLE_CONSTRAINTS = True
    
    #: Time resample strategies for certain cominations, first level refers
    #: to TO, second to FROM and values are minimum number of observations
    OBS_MIN_NUM_RESAMPLE = dict(yearly      =   dict(monthly    = 3),
                                monthly     =   dict(daily      = 7),
                                daily       =   dict(hourly     = 6),
                                hourly      =   dict(minutely   = 15))
    
    #: This boolean can be used to enable / disable the former (i.e. use
    #: available wavelengths of variable in a certain range around variable
    #: wavelength).
    OBS_ALLOW_ALT_WAVELENGTHS = obs_io.OBS_ALLOW_ALT_WAVELENGTHS
    
    #: Wavelength tolerance for observations imports
    OBS_WAVELENGTH_TOL_NM = obs_io.OBS_WAVELENGTH_TOL_NM
    
    #: not used at the moment
    GCOSPERCENTCRIT =   np.float(0.1)
    GCOSABSCRIT     =   np.float(0.04)
    
    
    CLIM_START =2005
    CLIM_STOP = 2015
    CLIM_FREQ = 'daily'
    CLIM_RESAMPLE_HOW = 'mean' # median, ...
    # as a function of climatological frequency
    CLIM_MIN_COUNT = dict(daily = 30, # at least 30 daily measurements in each month over whole period
                          monthly = 5) # analogue to daily ...
    
    #names of the different obs networks
    OBSNET_NONE = 'NONE'
    NOMODELNAME = 'OBSERVATIONS-ONLY'

    # names for the satellite data sets
    SENTINEL5P_NAME = 'Sentinel5P'
    AEOLUS_NAME = 'AeolusL2A'
    
    DEFAULT_REGIONS = ['EUROPE', 'WORLD', 'ASIA', 'AUSTRALIA', 'CHINA', 
                       'INDIA', 'NAFRICA', 'SAFRICA', 'SAMERICA', 'NAMERICA']
    
    HTAP_REGIONS = ['PANhtap', 'EAShtap', 'NAFhtap', 'MDEhtap', 'LANDhtap', 
                    'SAShtap', 'SPOhtap', 'OCNhtap',  'SEAhtap', 'RBUhtap', 
                    'EEUROPEhtap', 'NAMhtap', 'WEUROPEhtap', 'SAFhtap', 
                    'USAhtap', 'SAMhtap', 'EURhtap', 'NPOhtap', 'MCAhtap']
    
    RM_CACHE_OUTDATED = True

    #: Name of the file containing the revision string of an obs data network
    REVISION_FILE = 'Revision.txt'
    
    #: timeout to check if one of the supported server locations can be 
    #: accessed
    SERVER_CHECK_TIMEOUT = 1 #0.1 #s
    
    _outhomename = 'MyPyaerocom'
    
    from pyaerocom import __dir__
    _config_ini_lustre = os.path.join(__dir__, 'data', 'paths.ini')
    _config_ini_user_server = os.path.join(__dir__, 'data', 'paths_user_server.ini')
    _config_ini_testdata = os.path.join(__dir__, 'data', 'paths_testdata.ini')
    
    # this dictionary links environment ID's with corresponding ini files
    _config_files = {
            'metno'            : _config_ini_lustre,
            'users-db'         : _config_ini_user_server,
            'testdata'         : _config_ini_testdata
    }
    
    # this dictionary links environment ID's with corresponding subdirectory
    # names that are required to exist in order to load this environment
    _check_subdirs_cfg = {
            'metno'       : 'aerocom1',
            'users-db'    : 'AMAP',
            'testdata'    : 'modeldata',
    }
    
    
    _var_info_file = os.path.join(__dir__, 'data', 'variables.ini')
    _coords_info_file = os.path.join(__dir__, 'data', 'coords.ini')
    
    # these are searched in preferred order both in root and home
    _DB_SEARCH_SUBDIRS = od()
    _DB_SEARCH_SUBDIRS['lustre/storeA/project/aerocom'] = 'metno'
    #_DB_SEARCH_SUBDIRS['lustre/storeB/project/aerocom'] = 'metno'
    _DB_SEARCH_SUBDIRS['metno/aerocom_users_database'] = 'users-db'
    _DB_SEARCH_SUBDIRS['pyaerocom-testdata/'] = 'testdata'
    _DB_SEARCH_SUBDIRS['MyPyaerocom/pyaerocom-testdata'] = 'testdata'
                
    DONOTCACHEFILE = None
    
    _LUSTRE_CHECK_PATH = '/project/aerocom/aerocom1/'
    def __init__(self, basedir=None, 
                 output_dir=None, config_file=None, 
                 cache_dir=None, colocateddata_dir=None,
                 write_fileio_err_log=True, 
                 activate_caching=True):
        
        # Loggers
        from pyaerocom import print_log, logger
        self.print_log = print_log
        self.logger = logger
        
        # Directories
        self._modelbasedir = None
        self._obsbasedir = None
        self._cachedir = cache_dir
        self._outputdir = output_dir
        
        self._colocateddatadir = colocateddata_dir
        
        # Options
        self._caching_active = activate_caching
        
        self._var_param = None
        self._coords = None
        
        # Attributes that are used to store search directories
        self.OBSCONFIG = od()
        self.SUPPLDIRS = od()
        self.MODELDIRS = []
        
        self.WRITE_FILEIO_ERR_LOG = write_fileio_err_log
        
        self.last_config_file = None
        self._ebas_flag_info = None
        
        #: Settings for reading and writing of gridded data
        self.GRID_IO = GridIO()
        self.logger.info('Initiating pyaerocom configuration')
        
        # If this is False and a config_file is specified and / or can be 
        # inferred, then existing base directories are ignored, else they are
        # kept (cf. method read_config)
        keep_basedirs = False
        
        # checks and validates / invalidates input basedir and config_file
        # if both are 
        (basedir, 
         config_file) = self._check_input_basedir_and_config_file(basedir, 
                                                                  config_file)
        
        if not isinstance(config_file, str) or not os.path.exists(config_file):
            self.logger.info('Checking database access...')
            try:
                _basedir, config_file = self.infer_basedir_and_config()
            except FileNotFoundError:
                _basedir = None
            if basedir is None:
                basedir = _basedir
            
        if basedir is not None: # it passed the check and exists
            self._modelbasedir = basedir
            self._obsbasedir = basedir
            keep_basedirs = True
           
        
        if config_file is not None:
            try:
                self.read_config(config_file, keep_basedirs)
            except Exception as e:
                self.print_log.warning("Failed to read config. Error: {}"
                                       .format(repr(e)))
        # create MyPyaerocom directory
        chk_make_subdir(self.HOMEDIR, self._outhomename)
    
    def _check_input_basedir_and_config_file(self, basedir, config_file):
        if config_file is not None and not os.path.exists(config_file):
            self.print_log.warning('Ignoring input config_file {} since it '
                                   'does not exist'.format(config_file))
            config_file = None
            
        if basedir is not None:
            if not self._check_access(basedir):
                self.print_log.warning('Failed to establish access to input '
                                       'basedir={}'.format(basedir))
                basedir=None
            else:
                if config_file is None:
                    try:
                        config_file, _ = self._infer_config_from_basedir(basedir)
                    except FileNotFoundError:
                        basedir=None # config_file is None and basedir is None
        
        return basedir, config_file
                        
    @property 
    def _config_ini(self):
        # for backwards compatibility
        return self._config_ini_lustre
    
    def _check_access(self, loc):
        """Uses multiprocessing approach to check if location can be accessed
        
        Parameters
        ----------
        loc : str
            path that is supposed to be checked
        
        Returns
        -------
        bool
            True, if location is accessible, else False
        """
        
        
        self.logger.info('Checking access to: {}'.format(loc))
        return check_dir_access(loc, timeout=self.SERVER_CHECK_TIMEOUT)
    
    def _basedirs_search_db(self):
        return [self.ROOTDIR, self.HOMEDIR]
    
    def _check_env_access(self, basedir, env_id):
        if not os.path.exists(basedir):
            raise FileNotFoundError('Location not found: {}'.format(basedir))
        if not env_id in self._check_subdirs_cfg:
            raise ValueError('No such environment with ID {}. Choose from {}'
                             .format(env_id, 
                                     list(self._check_subdirs_cfg.keys())))
        return self._check_access(os.path.join(basedir, 
                                               self._check_subdirs_cfg[env_id]))
    
    def _infer_config_from_basedir(self, basedir):
        for env_id, chk_sub in self._check_subdirs_cfg.items():
            chkdir =  os.path.join(basedir, chk_sub)
            if self._check_access(chkdir):
                return (self._config_files[env_id], env_id)
        raise FileNotFoundError('Could not infer environment configuration '
                                'for input directory: {}'.format(basedir))
        
    def infer_basedir_and_config(self):
        """Boolean specifying whether the lustre database can be accessed"""
        for sub_envdir, cfg_id in self._DB_SEARCH_SUBDIRS.items():
            for sdir in self._basedirs_search_db():
                basedir = os.path.join(sdir, sub_envdir)
                if self._check_access(basedir):
                    _chk_dir = os.path.join(basedir, 
                                            self._check_subdirs_cfg[cfg_id])
                
                    if self._check_access(_chk_dir):
                        
                        return (basedir, self._config_files[cfg_id])
        raise FileNotFoundError('Could not find base directory for lustre')
        
    @property
    def has_access_lustre(self):
        """Boolean specifying whether MetNO AeroCom server is accessible"""
        for path in self.MODELDIRS:
            if self._LUSTRE_CHECK_PATH in path and self._check_access(path):
                return True
        return False
    @property
    def ALL_DATABASE_IDS(self):
        '''ID's of available database configurations'''
        return list(self._config_files.keys())
    
    @property
    def ROOTDIR(self):
        """Local root directory"""
        return os.path.abspath(os.sep)
    
    @property
    def HOMEDIR(self):
        """Home directory of user"""
        return os.path.expanduser("~") + '/'
    
    @property
    def OUTPUTDIR(self):
        """Default output directory"""
        if not check_write_access(self._outputdir):
            self._outputdir = chk_make_subdir(self.HOMEDIR, self._outhomename)
        return self._outputdir
    
    @property
    def COLOCATEDDATADIR(self):
        """Directory for accessing and saving colocated data objects"""
        if not check_write_access(self._colocateddatadir):
            outdir = self.OUTPUTDIR
            self._colocateddatadir = chk_make_subdir(outdir, 'colocated_data')
        return self._colocateddatadir
    
    @property
    def CACHEDIR(self):
        """Cache directory for UngriddedData objects"""
        if not check_write_access(self._cachedir):
            outdir = self.OUTPUTDIR
            self._cachedir = chk_make_subdir(outdir, '_cache')
        try:
            return chk_make_subdir(self._cachedir, getpass.getuser())
        except Exception as e:
            self.print_log.warning('Failed to access CACHEDIR: {}\n'
                                   'Deactivating caching'.format(repr(e)))
            self._caching_active = False
            
    @CACHEDIR.setter
    def CACHEDIR(self, val):
        """Cache directory"""
        if not check_write_access(val):
            raise ValueError('Cannot set cache directory. Input directory {} '
                             'does not exist or write '
                             'permission is not granted'.format(val))
        self._cachedir = val
        
    @property
    def CACHING(self):
        """Activate writing of and reading from cache files"""
        return self._caching_active
    
    @CACHING.setter
    def CACHING(self, val):
        self._caching_active = bool(val)
        
    @property
    def VAR_PARAM(self):
        """Deprecated name, please use :attr:`VARS` instead"""
        self.print_log.warning('Deprecated (but still functional) name '
                               'VAR_PARAM. Please use VARS')
        return self.VARS
    
    @property
    def VARS(self):
        """Instance of class VarCollection (for default variable information)"""
        if self._var_param is None: #has not been accessed before
            self._var_param = VarCollection(self._var_info_file)
        return self._var_param
    
    @property
    def COORDINFO(self):
        """Instance of :class:`VarCollection` containing coordinate info"""
        if self._coords is None:
            self._coords = VarCollection(self._coords_info_file)
        return self._coords
    
    @property
    def LOGFILESDIR(self):
        """Directory where logfiles are stored"""
        try:
            logdir = chk_make_subdir(self.OUTPUTDIR, '_log')
            return logdir
        except Exception as e:
            self.print_log.info('Failed to access LOGFILESDIR: {}'
                           'Deactivating file logging'.format(repr(e)))
            self.WRITE_FILEIO_ERR_LOG = False
            
       
    @property
    def MODELBASEDIR(self):
        """Base directory of model data
        
        If changed, all relevant subdirectories are updated as well.
        """
        return self._modelbasedir
    
    @MODELBASEDIR.setter
    def MODELBASEDIR(self, value):
        if not os.path.exists(value):
            raise IOError('Input directory does not exist')
        self._modelbasedir = value
        self.reload()
    
    @property
    def OBSBASEDIR(self):
        """Base directory of model data"""
        return self._obsbasedir
    
    @OBSBASEDIR.setter
    def OBSBASEDIR(self, value):
        if not os.path.exists(value):
            raise IOError('Input directory does not exist')
        self._obsbasedir = value
        self.reload() 
    
    @property 
    def BASEDIR(self):
        """Base directory of data
        
        Note
        ----
        If this attribute is changed it changes both, :attr:`MODELBASEDIR` and
        :attr:`OBSBASEDIR`.
        """
        return self._modelbasedir
    
    @BASEDIR.setter
    def BASEDIR(self, value):
        if not self._check_access(value):
            raise FileNotFoundError('Cannot change data base directory. '
                                    'Input directory does not exist')
            
        self._obsbasedir = value
        self._modelbasedir = value
        
        try:
            config_file, env_id = self._infer_config_from_basedir(value)
            self.print_log.info('Adding paths for {} with root at {}'
                                .format(env_id, value))
            self.read_config(config_file, keep_basedirs=True)
        except FileNotFoundError:
            self.print_log.warning('Failed to infer path environment for '
                                   'input dir {}. No search paths will be added'
                                   .format(value))
    @property
    def DIR_INI_FILES(self):
        """Directory containing configuration files"""
        from pyaerocom import __dir__
        return os.path.join(__dir__, 'data')
    
    @property
    def EBASMC_SQL_DATABASE(self):
        """Path to EBAS SQL database"""
        return os.path.join(self.OBSCONFIG["EBASMC"]["PATH"], 
                                'ebas_file_index.sqlite3')
        
    @property
    def EBASMC_DATA_DIR(self):
        """Data directory of EBAS multicolumn files"""
        return os.path.join(self.OBSCONFIG["EBASMC"]["PATH"], 'data/')
    
    @property
    def EBAS_FLAGS_FILE(self):
        from pyaerocom import __dir__
        return os.path.join(__dir__, 'data', 'ebas_flags.csv')
    
    @property
    def OBSDIRS(self):
        """Direcories of observation networks"""
        return [x["PATH"] for x in self.OBSCONFIG.values()]
    
    @property 
    def OBS_START_YEARS(self):
        """Start years of observation networks"""
        return [x["START_YEAR"] for x in self.OBSCONFIG.values()]
    
    @property
    def OBS_IDS(self):
        """List of all IDs of observations"""
        return [x for x in self.OBSCONFIG.keys()]
    
    def make_default_vert_grid(self):
        """Makes default vertical grid for resampling of profile data"""
        step = self.DEFAULT_VERT_GRID_DEF['step']
        offs = int(step/2)
        return np.arange(self.DEFAULT_VERT_GRID_DEF['lower'] + offs,
                         self.DEFAULT_VERT_GRID_DEF['upper'] - offs,
                         step)
        
    def add_data_search_dir(self, loc):
        """Add new search directory for database browsing"""
        if not self._check_access(loc):
            raise FileNotFoundError('Input location {} could not be accessed'
                                    .format(loc))
        self.MODELDIRS.append(loc)
        
    def change_database(self, database_name='metno', keep_root=False):
        '''Changes the path setup for a specific data environment
        
        Parameters
        ----------
        database_name : str
            name of path environment for database. To see available database
            ID's use :attr:`ALL_DATABASE_IDS`
        keep_root : bool
            if True, :attr:`BASEDIR` remains unchanged and paths in
            corresponding ini files are set relative to current :attr:`BASEDIR`.
            Else, :attr:`BASEDIR` is updated using the specifications 
            provided in the corresponding ini file.
        '''
        if not database_name in self.ALL_DATABASE_IDS:
            raise ValueError('Unkown database name {}. Please choose from '
                             '{}'.format(database_name, self.ALL_DATABASE_IDS))
        self.read_config(self._config_files[database_name], 
                         keep_basedirs=keep_root)
        
    

    @property    
    def EBAS_FLAG_INFO(self):
        """Information about EBAS flags
        
        Dictionary containing 3 dictionaries (keys: ```valid, values, info```) 
        that contain information about validity of each flag (```valid```), 
        their actual values (```values```, e.g. V, M, I)
        """
        if self._ebas_flag_info is None:
            from pyaerocom.io.helpers import read_ebas_flags_file
            self._ebas_flag_info = read_ebas_flags_file(self.EBAS_FLAGS_FILE)
        return self._ebas_flag_info
    
    def reload(self, keep_basedirs=True):
        """Reload config file (for details see :func:`read_config`)"""
        self.read_config(self.last_config_file, keep_basedirs)
        
    def read_config(self, config_file, keep_basedirs=True,
                    init_obs_locations=False,
                    init_model_locations=False):
        """Read and import paths from ini file"""
        if not os.path.isfile(config_file):
            raise IOError("Configuration file paths.ini at %s does not exist "
                          "or is not a file"
                          %config_file)
            
        if init_obs_locations:
            self.OBSCONFIG = od()
        if init_model_locations:
            self.MODELDIRS = []
            
        cr = ConfigParser()
        cr.read(config_file)
        #init base directories for Model data
        if cr.has_section('modelfolders'):
            mcfg = cr['modelfolders']
            # check and update model base directory if applicable
            if 'BASEDIR' in mcfg:
                if not keep_basedirs or not self._check_access(self._modelbasedir):
                    _dir = mcfg['BASEDIR']
                    if '$HOME' in _dir:
                        _dir = _dir.replace('$HOME', os.path.expanduser('~'))
                    
                    self._modelbasedir = _dir
                
            # load model paths if applicable
            if self._check_access(self._modelbasedir) and 'dir' in mcfg:
                mdirs = (mcfg['dir'].
                         replace('${BASEDIR}', self._modelbasedir).
                         replace('\n','').split(','))
                for mdir in mdirs:
                    # make sure to not add multiple times the same location
                    if not mdir in self.MODELDIRS:
                        self.MODELDIRS.append(mdir)
                
        if cr.has_section('outputfolders'):
            self._init_output_folders_from_cfg(cr['outputfolders'],
                                               keep_basedirs)
                    
        if cr.has_section('supplfolders'):
            for name, path in cr['supplfolders'].items():
                self.SUPPLDIRS[name] = path
        
        #Read directories for observation location
        if cr.has_section('obsfolders'):
            ocfg = cr['obsfolders']
            if 'BASEDIR' in ocfg:
                if not keep_basedirs or not self._check_access(self._obsbasedir):
                    _dir = cr['obsfolders']['BASEDIR']
                    if '$HOME' in _dir:
                        _dir = _dir.replace('$HOME', os.path.expanduser('~'))
                    self._obsbasedir = _dir
        try:
            self._init_obsconfig(cr)
        except Exception as e:
            self.print_log.exception('Failed to initiate obs config. '
                                     'Error: {}'.format(repr(e)))
        cr.clear()
        self.GRID_IO.load_aerocom_default()
        self.last_config_file = config_file
    
    def _init_output_folders_from_cfg(self, cfg, keep_basedirs):
        if 'CACHEDIR' in cfg: 
            if not keep_basedirs or not self._check_access(self._cachedir):
                self._cachedir = cfg['CACHEDIR']
        
        if 'OUTPUTDIR' in cfg:
            if not keep_basedirs or not self._check_access(self._outputdir):
                self._outputdir = cfg['OUTPUTDIR']
        
        if 'COLOCATEDDATADIR' in cfg: 
            if not keep_basedirs or not self._check_access(self._colocateddatadir):
                self._colocateddatadir = cfg['COLOCATEDDATADIR']
                
        if 'LOCALTMPDIR' in cfg:
            _dir = cfg['LOCALTMPDIR']
            # expand $HOME
            if '$HOME' in _dir:
                _dir = _dir.replace('$HOME', os.path.expanduser('~'))
            if '${USER}' in _dir:
                _dir = _dir.replace('${USER}', getpass.getuser())
            local_tmp_dir = _dir

            self.LOCAL_TMP_DIR = local_tmp_dir

    def _add_obsname(self, name):
        name_str = '{}_NAME'.format(name.upper())
        self[name_str] =  name
        return name_str
        
    def _add_obsnames_config(self, cr):
        names_cfg = []
        if cr.has_section('obsnames'):
            for obsname, ID in cr['obsnames'].items():
                name_str = '{}_NAME'.format(obsname.upper())
                self[name_str] =  ID
                names_cfg.append(name_str)
        return names_cfg
            
    def _init_obsconfig(self, cr):
        
        names_cfg = self._add_obsnames_config(cr)
        
        OBSCONFIG = self.OBSCONFIG
        if cr.has_section('obsfolders'):
            for obsname, path in cr['obsfolders'].items():
                if obsname.lower() == 'basedir':
                    continue
                name_str = '{}_NAME'.format(obsname.upper())
                if name_str in names_cfg:
                    ID = self.__dict__[name_str]    
                else:
                    ID = self._add_obsname(obsname)
                OBSCONFIG[ID] = {}
                p = path.replace('${BASEDIR}', self._obsbasedir)
                p = p.replace('$HOME', os.path.expanduser('~'))
                OBSCONFIG[ID]['PATH'] = p
        
        if cr.has_section('obsstartyears'):
            for obsname, year in cr['obsstartyears'].items():
                NAME = '{}_NAME'.format(obsname.upper())
                if NAME in self.__dict__:
                    ID = self.__dict__[NAME]
                    if ID in OBSCONFIG.keys():
                        OBSCONFIG[ID]['START_YEAR'] = year
            
        self.OBSCONFIG = OBSCONFIG
    
    def add_data_source(self, data_dir, name=None):
        """Add a network to the data search structure
        
        Parameters
        ----------
        name : str
            name of network 
        data_dir : str
            directory where data files are stored
        
        Raises
        ------
        AttributeError
            if the network name is already reserved 
        ValueError
            if the data directory does not exist
        """
        raise NotImplementedError('Coming soon... need some refactoring before')
        name_str = '{}_NAME'.format(name.upper())
        if name_str in self.__dict__.keys():
            raise AttributeError('Network with ID {} does already exist'.format(name_str))
        elif not os.path.exists(data_dir):
            raise ValueError('Input data directory does not exist')
        self[name_str] =  name
        self.OBSCONFIG[name] = {'PATH' : data_dir}
        
    def short_str(self):
        """Deprecated method"""
        return self.__str__()    
    
    def __setitem__(self, key, val):
        self.__dict__[key] = val
        
    def __str__(self):
        head = "Pyaerocom {}".format(type(self).__name__)
        s = "\n{}\n{}\n".format(head, len(head)*"-")
        for k, v in self.__dict__.items():
            if k.startswith('_'):
                pass
            if k=='VARS':
                s += '\n{}\n{}'.format(k, list_to_shortstr(v.all_vars))
            elif isinstance(v, dict):
                s += "\n%s (dict)" %k
            elif isinstance(v, list):
                s += "\n%s (list)" %k
                s += list_to_shortstr(v)
            else:
                s += "\n%s: %s" %(k, v)
        return s
    
    @property
    def OUT_BASEDIR(self):
        msg = 'Attribute OUT_BASEDIR is deprecated. Please use OUTPUTDIR instead'
        self.print_log.warning(DeprecationWarning(msg))
        return self.OUTPUTDIR
    
    @property
    def OBSDATACACHEDIR(self):
        """Cache directory for UngriddedData objects (deprecated)"""
        msg=('Attr. was renamed (but still works). Please us CACHEDIR instead')
        self.print_log.warning(DeprecationWarning(msg))
        return self.CACHEDIR
    
if __name__=="__main__":
    import pyaerocom as pya
    
    print(pya.const.OUTPUTDIR)
    print(pya.const.COLOCATEDDATADIR)
    print(pya.const.CACHEDIR)
    
    pya.const.BASEDIR = '/home/jonasg/'
    pya.const.BASEDIR = '/home/jonasg/MyPyaerocom/pyaerocom-testdata/'
    
    print(pya.const.has_access_lustre)
          