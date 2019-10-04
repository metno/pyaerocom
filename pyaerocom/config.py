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
                                         check_fun_timeout_multiproc)
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
    
    #names of the different obs networks
    OBSNET_NONE = 'NONE'
    NOMODELNAME = 'OBSERVATIONS-ONLY'

    # names for the satellite data sets
    SENTINEL5P_NAME = 'Sentinel5P'
    AEOLUS_NAME = 'AeolusL2A'
    
    RM_CACHE_OUTDATED = True

    #: Name of the file containing the revision string of an obs data network
    REVISION_FILE = 'Revision.txt'

    
    BASEDIR_PPI = os.path.join('/lustre', 'storeA', 'project', 'aerocom') 
    BASEDIR_USER_SERVER = os.path.join('/metno', 'aerocom-users-database')
    
    #: timeout to check if one of the supported server locations can be 
    #: accessed
    SERVER_CHECK_TIMEOUT = 5 #0.1 #s
    
    from pyaerocom import __dir__
    _config_ini = os.path.join(__dir__, 'data', 'paths.ini')
    _config_ini_user_server = os.path.join(__dir__, 'data', 'paths_user_server.ini')
    _config_ini_testdata = os.path.join(__dir__, 'data', 'paths_testdata.ini')
    
    _config_files = {'metno'                  : _config_ini,
                     'aerocom-users-database' : _config_ini_user_server,
                     'pyaerocom-testdata'     : _config_ini_testdata}
    
    _var_info_file = os.path.join(__dir__, 'data', 'variables.ini')
    _coords_info_file = os.path.join(__dir__, 'data', 'coords.ini')
    _outhomename = 'MyPyaerocom'
    
    DONOTCACHEFILE = None
    def __init__(self, model_base_dir=None, obs_base_dir=None, 
                 output_dir=None, config_file=None, 
                 cache_dir=None, colocateddata_dir=None,
                 write_fileio_err_log=True, 
                 activate_caching=True):
        
        # Loggers
        from pyaerocom import print_log, logger
        self.print_log = print_log
        self.logger = logger
        
        # Directories
        self._modelbasedir = model_base_dir
        self._obsbasedir = obs_base_dir
        self._cachedir = cache_dir
        self._outputdir = output_dir
        self._testdatadir = os.path.join(self.HOMEDIR, 'pyaerocom-testdata')
        self._colocateddatadir = colocateddata_dir
        
        # Options
        self._caching_active = activate_caching
        
        #: Settings for reading and writing of gridded data
        self.GRID_IO = GridIO()
        print_log.info('Initating pyaerocom configuration')
        
        
        if not isinstance(config_file, str) or not os.path.exists(config_file):
            from time import time
            print_log.info('Checking database access...')
            t0 = time()
            config_file = self._infer_config_file()
            print_log.info('Expired time: {:.3f} s'.format(time() - t0))
        
        
        self._var_param = None
        self._coords = None
        
        # Attributes that are used to store search directories
        self.OBSCONFIG = od()
        self.SUPPLDIRS = od()
        self.MODELDIRS = []
        
        self.WRITE_FILEIO_ERR_LOG = write_fileio_err_log
        
        
        self._ebas_flag_info = None
        
        if config_file is not None:
            
            keep_basedirs = False
            if self.dir_exists(model_base_dir) and self.dir_exists(obs_base_dir):
                keep_basedirs=True
            try:
                self.read_config(config_file, keep_basedirs)
                
            except Exception as e:
                from traceback import format_exc
                self.init_outputdirs()
                self.print_log.warning(format_exc())
                self.print_log.warning("Failed to init config. Error: %s" %repr(e))
        else:
            self.init_outputdirs()
    
    def _check_access(self, loc):
        """Uses multiprocessing approach to check if location can be accessed
        
        Wrapper for :func:`check_fun_timeout_multiproc`. Uses method 
        :func:`os.listdir` to validate accessibility at input location
        (without the timeout and for mounted remote locations, this could 
        otherwise take ages)
        
        Parameters
        ----------
        loc : str
            path that is supposed to be checked
        
        Returns
        -------
        bool
            True, if location is accessible, else False
        """
# =============================================================================
#         try:
#             os.listdir(loc)
#             return True
#         except:
#             return False
# =============================================================================
        self.print_log.info('Checking access to: {}'.format(loc))
        return check_fun_timeout_multiproc(os.listdir, fun_args=(loc, ),
                                           timeout_secs=self.SERVER_CHECK_TIMEOUT)
    
    @property
    def has_access_lustre(self):
        """Boolean specifying whether the lustre database can be accessed"""
        ok = False
        p = os.path.join(self.ROOTDIR, 'lustre/')
        if os.path.exists(p):
            ok = self._check_access(os.path.join(p, 'storeA'))
        self.print_log.info('Access to lustre database: {}'.format(ok))
        return ok
    
    @property
    def has_access_users_database(self):
        """Boolean specifying whether the users database can be accessed"""
        ok = False
        p = os.path.join(self.ROOTDIR, 'metno/')
        if os.path.exists(p):
            test_loc = os.path.join(p, 'aerocom-users-database')
            ok = self._check_access(test_loc)
                
        self.print_log.info("Access to aerocom-users-database: {}".format(ok))
        return ok
    
    @property
    def has_access_testdata(self):
        """Boolean specifying whether the testdataset can be accessed"""
        ok = False
        if self.dir_exists(self._testdatadir) and 'modeldata' in os.listdir(self.TESTDATADIR):
            ok = True
            
        self.print_log.info("Access to pyaerocom-testdata: {}".format(ok))
        return ok
    
    def _infer_config_file(self):
        """Infer the database configuration to be loaded"""
        if self.has_access_lustre:
            self.print_log.info("Init data paths for lustre")
            self.GRID_IO.load_aerocom_default()
            return self._config_files['metno']
        elif self.has_access_users_database:
            self.print_log.info("Init data paths for users database")
            self.GRID_IO.load_aerocom_default()
            return self._config_files['aerocom-users-database']
        elif self.has_access_testdata:
            self.print_log.info("Init data paths for pyaerocom testdata")
            self.GRID_IO.load_aerocom_default()
            return self._config_files['pyaerocom-testdata']
        
        self.GRID_IO.load_default()
        return None
    
    @property
    def ALL_DATABASE_IDS(self):
        '''ID's of available database configurations'''
        return list(self._config_files.keys())
    
    @property
    def ROOTDIR(self):
        return os.path.abspath(os.sep)
    
    @property
    def HOMEDIR(self):
        """Home directory of user"""
        return os.path.expanduser("~") + '/'
    
    @property
    def TESTDATADIR(self):
        return self._testdatadir
    
    @TESTDATADIR.setter
    def TESTDATADIR(self, val):
        if not self.dir_exists(val):
            raise ValueError('Cannot set pyaerocom-testdata directory {}.'
                             'Directory does not exist')
        self._testdatadir = val
        if not self.has_access_testdata:
            self._testdatadir = None
            raise IOError('Input path {} could not be identified as official '
                          'pyaerocom testdata directory (requires that a sub '
                          'directory modeldata exists)'.format(val))
        self.read_config(self._config_files['pyaerocom-testdata'], keep_basedirs=False)
    
    @property
    def OUTPUTDIR(self):
        """Default output directory"""
        return self._outputdir
    
    @property
    def COLOCATEDDATADIR(self):
        """Directory for accessing and saving colocated data objects"""
        return self._colocateddatadir
    
    @property
    def OUT_BASEDIR(self):
        msg = 'Attribute OUT_BASEDIR is deprecated. Please use OUTPUTDIR instead'
        self.print_log.warning(DeprecationWarning(msg))
        return self.OUTPUTDIR
    
    @property
    def CACHING(self):
        """Activate writing of and reading from cache files"""
        return self._caching_active
    
    @CACHING.setter
    def CACHING(self, val):
        self._caching_active = bool(val)
        
    @property
    def OBSDATACACHEDIR(self):
        """Cache directory for UngriddedData objects (deprecated)"""
        msg=('Attr. was renamed (but still works). Please us CACHEDIR instead')
        self.print_log.warning(DeprecationWarning(msg))
        return self.CACHEDIR
    
    @property
    def CACHEDIR(self):
        """Cache directory for UngriddedData objects"""
        if self._cachedir is None:
            raise IOError('Cache directory is not defined')
        try:
            return chk_make_subdir(self._cachedir, getpass.getuser())
        except Exception as e:
            from pyaerocom import print_log
            print_log.info('Failed to access CACHEDIR: {}\n'
                           'Deactivating caching'.format(repr(e)))
            self._caching_active = False
            
    @CACHEDIR.setter
    def CACHEDIR(self, val):
        """Cache directory"""
        if not os.path.exists(val):
            raise ValueError('Input directory does not exist {}'.format(val))
        elif not self._write_access(val):
            raise ValueError('Cannot write to {}'.format(val))
        self._cachedir = val
        
    @property
    def VAR_PARAM(self):
        """Deprecated name, please use :attr:`VARS` instead"""
        self.print_log.warning('Deprecated (but still functional) name '
                               'VARS. Please use VARS')
        return self.VARS
    
    @property
    def VARS(self):
        """Instance of class VarCollection (for default variable information)"""
        if self._var_param is None: #has not been accessed before
            self._var_param = VarCollection(self._var_info_file)
        return self._var_param
    
    @property
    def COORDINFO(self):
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
            from pyaerocom import print_log
            print_log.info('Failed to access LOGFILESDIR: {}'
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
        self.check_data_dirs()
    
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
        self.check_data_dirs()
    
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
        if not os.path.exists(value):
            raise IOError('Cannot change data base directory. Input directory '
                          'does not exist')
            
        self._obsbasedir = value
        self._modelbasedir = value
        
        subdirs = os.listdir(value)
        from pyaerocom import print_log
        if 'aerocom0' in subdirs:
            print_log.info('Initiating directories for lustre')
            self.read_config(self._config_ini, 
                             keep_basedirs=True)
        elif 'obsdata' in subdirs: #test dataset
            
            print_log.info('Initiating directories for pyaerocom testdataset')
            self.read_config(self._config_ini_testdata, 
                             keep_basedirs=True)
            self._cachedir = os.path.join('..', '_cache')
        elif 'AMAP' in subdirs:
            print_log.info('Initiating directories for AEROCOM users database')
            self.read_config(self._config_ini_user_server, 
                             keep_basedirs=True)
        else:
            self.reload()    
        
         
    @property
    def READY(self):
        """Checks if relevant directories exist, returns True or False"""
        return bool(self.check_directories())
    
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
        
    def dir_exists(self, path):
        """Checks if directory exists"""
        if isinstance(path, str) and os.path.isdir(path):
            return True
        return False
    
    @staticmethod
    def _write_access(path):
        test = os.path.join(path, '_tmp')
        try:
            os.mkdir(test)
            os.rmdir(test)
            return True
        except:
            return False
        return os.access(path, os.W_OK)
    
    @staticmethod
    def _read_access(path):
        return os.access(path, os.R_OK)
    
    def check_directories(self):
        """Checks all predefined data directories for availability
        
        Prints each directory that is not available
        """
        self.logger.info('Checking data directories')
        ok =True
        #model_dirs = []
        # CHECK BASIC DATA READING DIRECTORIES
        if not self.dir_exists(self._modelbasedir):
            self.logger.warning("Model base directory {} does not exist"
                                .format(self._modelbasedir))
            ok=False
        if not self.dir_exists(self._obsbasedir):
            self.logger.warning("Observations base directory {} does not "
                                "exist".format(self._obsbasedir))
            ok=False
        
        return self.init_outputdirs() * ok
    
    def init_outputdirs(self):
        """Initiate output directories based on current configuration
        
        Checks, and if applicable, writes / creates required output directories
        (i.e. :attrs:`OUTPUTDIR, CACHEDIR, COLOCATEDDATADIR`).
        
        Returns
        -------
        bool
            True, if everything is okay, False if not
        """
        out_ok = True
        if not self.dir_exists(self._outputdir) or not self._write_access(self._outputdir):
            out_ok = False
            try:
                self._outputdir = chk_make_subdir(self.HOMEDIR, self._outhomename)
                out_ok = True
            except:
                self.logger.warning('Failed to create {} directory in home '
                                    'directory'.format(self._outhomename))
        
        if not out_ok or not self._write_access(self._outputdir):
            self.log.info('Cannot establish write access to output directory {}'
                           .format(self._outputdir))
            return False

        if (not self.dir_exists(self._colocateddatadir) or not 
                self._read_access(self._colocateddatadir)):
            self._colocateddatadir = os.path.join(self._outputdir,
                                                  'colocated_data')
        if not self.dir_exists(self._cachedir) or not self._write_access(self._cachedir):
            self._cachedir = chk_make_subdir(self._outputdir, '_cache')
        
        
        # if this file exists no cache file is read
        # used to ease debugging
        if self.dir_exists(self.CACHEDIR):
            self.DONOTCACHEFILE = os.path.join(self.CACHEDIR, 'DONOTCACHE')
            if os.path.exists(self.DONOTCACHEFILE):
                self._caching_active = False
        
        if not self._write_access(self._cachedir):
            self.logger.info('Cannot establish write access to cache '
                             'directory {}. Deactivating caching of files'
                             .format(self._cachedir))
            self._caching_active = False
        return out_ok
    
    def add_model_dir(self, dirname):
        """Add new model directory"""
        self.MODELDIRS.append(os.path.join(self.MODELBASEDIR, 'dirname'))
        
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
        
    def reload(self, keep_basedirs=True):
        """Reload config file (for details see :func:`read_config`)"""
        self.read_config(self._config_ini, keep_basedirs)

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
    
    def load_default_config(self):
        """Read AeroCom default config file"""
        self.read_config(self._config_files['metno'])
        
    def read_config(self, config_file, keep_basedirs=True):
        """Read and import form paths.ini"""
        if not os.path.isfile(config_file):
            raise IOError("Configuration file paths.ini at %s does not exist "
                          "or is not a file"
                          %config_file)
        self.OBSCONFIG = od()
        cr = ConfigParser()
        cr.read(config_file)
        if cr.has_section('outputfolders'):
            if not keep_basedirs or not self.dir_exists(self._cachedir):
                try:
                    cachedir = cr['outputfolders']['CACHEDIR']
                    if not self._write_access(cachedir):
                        raise PermissionError('Cannot write to {}'.format(cachedir))
                    self._cachedir = cr['outputfolders']['CACHEDIR']
                except Exception as e:
                    self.logger.warning('Failed to init cache directory from '
                                        'config file. Error: {}'
                                        .format(repr(e)))
                
            if not keep_basedirs or not self.dir_exists(self._outputdir):
                try:
                    outdir = cr['outputfolders']['OUTPUTDIR']
                    if not self._write_access(outdir):
                        raise PermissionError('Cannot write to {}'.format(outdir))
                        
                    self._outputdir = outdir
                    self._colocateddatadir = os.path.join(outdir, 
                                                          'colocated_data')
                except Exception as e:
                    self.logger.warning('Failed to init output and colocated data '
                                        'directory from config file. Error: {}'
                                        .format(repr(e)))

            try:
                _dir = cr['outputfolders']['LOCALTMPDIR']
                # expand $HOME
                if '$HOME' in _dir:
                    _dir = _dir.replace('$HOME', os.path.expanduser('~'))
                if '${USER}' in _dir:
                    _dir = _dir.replace('${USER}', getpass.getuser())
                local_tmp_dir = _dir

                if not self._write_access(local_tmp_dir):
                    raise PermissionError('Cannot write to {}'.format(local_tmp_dir))
                self.LOCAL_TMP_DIR = local_tmp_dir

            except Exception as e:
                    self.logger.warning('Failed to init local tmp directory from '
                                        'config file. Error: {}'
                                        .format(repr(e)))
                    
        if cr.has_section('supplfolders'):
            for name, path in cr['supplfolders'].items():
                if not os.path.exists(path):
                    self.print_log.warning('Supplementary data directory for '
                                        '{} does not exist:\n{}'.format(name, path))
                self.SUPPLDIRS[name] = path
                
        #init base directories for Model data
        if not keep_basedirs or not self.dir_exists(self._modelbasedir):
            _dir = cr['modelfolders']['BASEDIR']
            if '$HOME' in _dir:
                _dir = _dir.replace('$HOME', os.path.expanduser('~'))
            self._modelbasedir = _dir
        
        self.MODELDIRS = (cr['modelfolders']['dir'].
                          replace('${BASEDIR}', self._modelbasedir).
                          replace('\n','').split(','))

        #Read directories for observation location
        if not keep_basedirs or not self.dir_exists(self._obsbasedir):
            _dir = cr['obsfolders']['BASEDIR']
            if '$HOME' in _dir:
                _dir = _dir.replace('$HOME', os.path.expanduser('~'))
            self._obsbasedir = _dir
        
        try:
            self._init_obsconfig(cr)
        except Exception as e:
            from pyaerocom import print_log
            print_log.exception('Failed to initiate obs config. Error: {}'
                                .format(repr(e)))
        cr.clear()
        self.check_directories()
    
    def _add_obsname(self, name):
        name_str = '{}_NAME'.format(name.upper())
        self[name_str] =  name
        return name_str
        
    def _add_obsnames_config(self, cr):
        names_cfg = []
        for obsname, ID in cr['obsnames'].items():
            name_str = '{}_NAME'.format(obsname.upper())
            self[name_str] =  ID
            names_cfg.append(name_str)
        return names_cfg
            
    def _init_obsconfig(self, cr):
        
        names_cfg = self._add_obsnames_config(cr)
        
        OBSCONFIG = self.OBSCONFIG
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
        
if __name__=="__main__":
    import pyaerocom as pya
    
    pya.const.COORDINFO.a
# =============================================================================
#     pya.const.BASEDIR = '/home/jonasg/aerocom-users-database'
#     
#     pya.browse_database('Aeronet*')
# =============================================================================
