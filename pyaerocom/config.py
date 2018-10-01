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
from warnings import warn
from collections import OrderedDict as od
import pyaerocom.obs_io as obs_io
from pyaerocom._lowlevel_helpers import (list_to_shortstr, dict_to_str,
                                         chk_make_subdir)
from pyaerocom.variable import AllVariables
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
    
    #: Aeronet V2 access names
    AERONET_SUN_V2L15_AOD_DAILY_NAME = 'AeronetSunV2Lev1.5.daily'
    AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME = 'AeronetSun_2.0_NRT'
    AERONET_SUN_V2L2_AOD_DAILY_NAME = 'AeronetSunV2Lev2.daily'
    AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME = 'AeronetSunV2Lev2.AP'
    AERONET_SUN_V2L2_SDA_DAILY_NAME = 'AeronetSDAV2Lev2.daily'
    AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME = 'AeronetSDAV2Lev2.AP'
    
    #Aeronet V3 access names
    AERONET_SUN_V3L15_AOD_DAILY_NAME = 'AeronetSunV3Lev1.5.daily'
    AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME = 'AeronetSunV3Lev1.5.AP'
    AERONET_SUN_V3L2_AOD_DAILY_NAME = 'AeronetSunV3Lev2.daily'
    AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME = 'AeronetSunV3Lev2.AP'
    AERONET_SUN_V3L15_SDA_DAILY_NAME = 'AeronetSDAV3Lev1.5.daily'
    AERONET_SUN_V3L15_SDA_ALL_POINTS_NAME = 'AeronetSDAV3Lev1.5.AP'
    AERONET_SUN_V3L2_SDA_DAILY_NAME = 'AeronetSDAV3Lev2.daily'
    AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME = 'AeronetSDAV3Lev2.AP'

    # inversions
    AERONET_INV_V2L15_DAILY_NAME = 'AeronetInvV2Lev1.5.daily'
    AERONET_INV_V2L15_ALL_POINTS_NAME = 'AeronetInvV2Lev1.5.AP'
    AERONET_INV_V2L2_DAILY_NAME = 'AeronetInvV2Lev2.daily'
    AERONET_INV_V2L2_ALL_POINTS_NAME = 'AeronetInvV2Lev2.AP'
    #
    EBAS_MULTICOLUMN_NAME = 'EBASMC'
    EEA_NAME = 'EEAAQeRep'

    #: Earlinet access name;
    EARLINET_NAME = 'EARLINET'
    
    #: Lowest possible year in data
    MIN_YEAR = 0
    #: Highest possible year in data
    MAX_YEAR = 20000
    
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

    #: Name of the file containing the revision string of an obs data network
    REVISION_FILE = 'Revision.txt'
    
    _config_ini = os.path.join('.', 'data', 'paths.ini')
    _outhomename = 'pyaerocom'
    def __init__(self, model_base_dir=None, obs_base_dir=None, 
                 output_dir=None, config_file=None, 
                 cache_dir=None, write_fileio_err_log=True, 
                 activate_caching=True):
        
        if isinstance(config_file, str) and os.path.exists(config_file):
            self._config_ini = config_file
        
        # Directories
        self._modelbasedir = model_base_dir
        self._obsbasedir = obs_base_dir
        self._cachedir = cache_dir
        self._outputdir = output_dir
        self._caching_active = activate_caching
        
        self._var_param = None
        #: Settings for reading and writing of gridded data
        self.GRID_IO = GridIO()
        
        # Attributes that are used to store import results
        self.OBSCONFIG = od()
        self.MODELDIRS = []
        
        self.WRITE_FILEIO_ERR_LOG = write_fileio_err_log
                 
        try:
            # only overwrites above defined directories if they do not exist
            # (which is the default case, since they are None on default input)
            self.read_config(config_file)
        except Exception as e:
            print("Failed to read config file. Error: %s" %repr(e))
        
        self.check_output_dirs()
        self.check_data_dirs()
        
        # if this file exists no cache file is read
        # used to ease debugging
        self.DONOTCACHEFILE = os.path.join(self.OBSDATACACHEDIR, 'DONOTCACHE')
        if os.path.exists(self.DONOTCACHEFILE):
            self._caching_active=False
    
    @property
    def HOMEDIR(self):
        """Home directory of user"""
        return os.path.expanduser("~")
    
    @property
    def OUTPUTDIR(self):
        return self._outputdir
    
    @property
    def OUT_BASEDIR(self):
        warn(DeprecationWarning('Attribute OUT_BASEDIR is deprecated. Please '
                                'use OUTPUTDIR instead'))
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
        from warnings import warn
        warn(DeprecationWarning('Attr. was renamed (but still works). '
                                'Please us CACHEDIR instead'))
        return self.CACHEDIR
    
    @property
    def CACHEDIR(self):
        """Cache directory"""
        return chk_make_subdir(self._cachedir, getpass.getuser())
    
    @property
    def VAR_PARAM(self):
        """Instance of class AllVariables (for default variable information)"""
        if self._var_param is None: #has not been accessed before
            self._var_param = AllVariables()
        return self._var_param
    
    @property
    def LOGFILESDIR(self):
        """Directory where logfiles are stored"""
        logdir=chk_make_subdir(self.OUTPUTDIR, '_log')
        return logdir
       
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
        self.reload()    
        self.check_data_dirs()
            
    @property
    def READY(self):
        """Checks if relevant directories exist, returns True or False"""
        return bool(self.check_data_dirs() * self.check_output_dirs())
    
    @property
    def EBASMC_SQL_DATABASE(self):
        """Path to EBAS SQL database"""
        return os.path.join(self.OBSCONFIG["EBASMC"]["PATH"], 
                                'ebas_file_index.sqlite3')
        
    @property
    def EBASMC_DATA_DIR(self):
        """Data directory of EBAS multicolumn files"""
        return os.path.join(self.OBSCONFIG["EBASMC"]["PATH"], 'data')
                            
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
    
    def dir_exists(self, path):
        """Checks if directory exists"""
        if isinstance(path, str) and os.path.isdir(path):
            return True
        return False
    
    @staticmethod
    def _write_access(path):
        return os.access(path, os.W_OK)
    
    def check_output_dirs(self):
        """Checks if output directories are available and have write-access"""
        
        if not self.dir_exists(self._outputdir) or not self._write_access(self._outputdir):
            self._outputdir = chk_make_subdir(self.HOMEDIR, self._outhomename)
        if not self._write_access(self._outputdir):
            print('Cannot establish write access to output directory {}'
                  .format(self._outputdir))
            return False
        if not self.dir_exists(self._cachedir) or not self._write_access(self._cachedir):
            self._cachedir = chk_make_subdir(self._outputdir, '_cache')
        if not self._write_access(self._cachedir):
            print('Cannot establish write access to cache directory {}.'
                  'Deactivating caching of files'.format(self._cachedir))
            self._caching_active = False
            return False
        return True
    
    def check_data_dirs(self):
        """Checks all predefined data directories for availability
        
        Prints each directory that is not available
        """
        from logging import getLogger
        logger = getLogger()
        logger.info('Checking data directories')
        ok =True
        model_dirs = []
        if not self.dir_exists(self._modelbasedir):
            logger.warning("Model base directory %s does not exist")
            ok=False
        if not self.dir_exists(self._obsbasedir):
            logger.warning("Observations base directory %s does not exist")
            ok=False
        if not self.dir_exists(self._cachedir):
            logger.warning("Observations cache directory %s does not exist. "
                           "Turning off caching")
            self.CACHING = False            
        for subdir in self.MODELDIRS:
            if not os.path.exists(subdir):
                logger.warning('Model directory base path does not exist and '
                               'will be removed from search tree: {}'.format(subdir))
            else:
                model_dirs.append(subdir)
        for subdir in self.OBSDIRS:
            if not os.path.exists(subdir):
                logger.warning('OBS directory path {} does not exist'.format(subdir))
     
        self.MODELDIRS = model_dirs
        return ok
    
    def add_model_dir(self, dirname):
        """Add new model directory"""
        self.MODELDIRS.append(os.path.join(self.MODELBASEDIR, 'dirname'))
        
    def reload(self, keep_basedirs=True):
        """Reload file"""
        self.read_config(self._config_ini, keep_basedirs)
        
    def read_config(self, config_file, keep_basedirs=True):
        """Read and import form paths.ini"""
        _config_ini = self._config_ini
        if not os.path.isfile(_config_ini):
            raise IOError("Configuration file paths.ini at %s does not exist "
                          "or is not a file"
                          %_config_ini)
        cr = ConfigParser()
        cr.read(_config_ini)
        if cr.has_section('outputfolders'):
            if not keep_basedirs or not self.dir_exists(self._cachedir):
                self._cachedir = cr['outputfolders']['CACHEDIR']
            if not keep_basedirs or not self.dir_exists(self._outputdir):
                self._outputdir = cr['outputfolders']['OUTPUTDIR']
        #init base directories for Model data
        if not keep_basedirs or not self.dir_exists(self._modelbasedir):
            self._modelbasedir = cr['modelfolders']['BASEDIR']
        
        self.MODELDIRS = (cr['modelfolders']['dir'].
                          replace('${BASEDIR}', self._modelbasedir).
                          replace('\n','').split(','))

        # read obs network names from ini file
        # Aeronet V2
        self.AERONET_SUN_V2L15_AOD_DAILY_NAME = cr['obsnames']['AERONET_SUN_V2L15_AOD_DAILY']
        self.AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME = cr['obsnames']['AERONET_SUN_V2L15_AOD_ALL_POINTS']
        self.AERONET_SUN_V2L2_AOD_DAILY_NAME = cr['obsnames']['AERONET_SUN_V2L2_AOD_DAILY']
        self.AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME = cr['obsnames']['AERONET_SUN_V2L2_AOD_ALL_POINTS']
        self.AERONET_SUN_V2L2_SDA_DAILY_NAME = cr['obsnames']['AERONET_SUN_V2L2_SDA_DAILY']
        self.AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME = cr['obsnames']['AERONET_SUN_V2L2_SDA_ALL_POINTS']
        # inversions
        self.AERONET_INV_V2L15_DAILY_NAME = cr['obsnames']['AERONET_INV_V2L15_DAILY']
        self.AERONET_INV_V2L15_ALL_POINTS_NAME = cr['obsnames']['AERONET_INV_V2L15_ALL_POINTS']
        self.AERONET_INV_V2L2_DAILY_NAME = cr['obsnames']['AERONET_INV_V2L2_DAILY']
        self.AERONET_INV_V2L2_ALL_POINTS_NAME = cr['obsnames']['AERONET_INV_V2L2_ALL_POINTS']
        
        # Aeronet V3
        self.AERONET_SUN_V3L15_AOD_DAILY_NAME = cr['obsnames']['AERONET_SUN_V3L15_AOD_DAILY']
        self.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME = cr['obsnames']['AERONET_SUN_V3L15_AOD_ALL_POINTS']
        self.AERONET_SUN_V3L2_AOD_DAILY_NAME = cr['obsnames']['AERONET_SUN_V3L2_AOD_DAILY']
        self.AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME = cr['obsnames']['AERONET_SUN_V3L2_AOD_ALL_POINTS']
        self.AERONET_SUN_V3L2_SDA_DAILY_NAME = cr['obsnames']['AERONET_SUN_V3L2_SDA_DAILY']
        self.AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME = cr['obsnames']['AERONET_SUN_V3L2_SDA_ALL_POINTS']
        # inversions
        self.AERONET_INV_V3L15_DAILY_NAME = cr['obsnames']['AERONET_INV_V3L15_DAILY']
        self.AERONET_INV_V3L2_DAILY_NAME = cr['obsnames']['AERONET_INV_V3L2_DAILY']
        
        
        self.EBAS_MULTICOLUMN_NAME = cr['obsnames']['EBAS_MULTICOLUMN']
        self.EEA_NAME = cr['obsnames']['EEA']
        self.EARLINET_NAME = cr['obsnames']['EARLINET']
    
    
        #Read directories for observation location
        if not keep_basedirs or not self.dir_exists(self._obsbasedir):
            self._obsbasedir = cr['obsfolders']['BASEDIR']
            
        OBSCONFIG = self.OBSCONFIG
        OBSCONFIG[self.AERONET_SUN_V2L15_AOD_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V2L15_AOD_DAILY_NAME]['PATH'] =\
        cr['obsfolders']['AERONET_SUN_V2L15_AOD_DAILY'].\
        replace('${BASEDIR}', self._obsbasedir)
        
        OBSCONFIG[self.AERONET_SUN_V2L15_AOD_DAILY_NAME]['START_YEAR'] =\
            cr['obsstartyears']['AERONET_SUN_V2L15_AOD_DAILY']
    
        OBSCONFIG[self.AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME]['PATH'] =\
            cr['obsfolders']['AERONET_SUN_V2L15_AOD_ALL_POINTS'].\
            replace('${BASEDIR}', self._obsbasedir)
        OBSCONFIG[self.AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME]['START_YEAR'] =\
            cr['obsstartyears']['AERONET_SUN_V2L15_AOD_ALL_POINTS']
    
        OBSCONFIG[self.AERONET_SUN_V2L2_AOD_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V2L2_AOD_DAILY_NAME]['PATH'] =\
            cr['obsfolders']['AERONET_SUN_V2L2_AOD_DAILY'].\
            replace('${BASEDIR}', self._obsbasedir)
        OBSCONFIG[self.AERONET_SUN_V2L2_AOD_DAILY_NAME]['START_YEAR'] =\
            cr['obsstartyears']['AERONET_SUN_V2L2_AOD_DAILY']
    
        OBSCONFIG[self.AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME]['PATH'] =\
            cr['obsfolders']['AERONET_SUN_V2L2_AOD_ALL_POINTS'].\
            replace('${BASEDIR}',self._obsbasedir)
        OBSCONFIG[self.AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME]['START_YEAR'] =\
            cr['obsstartyears']['AERONET_SUN_V2L2_AOD_ALL_POINTS']
    
        OBSCONFIG[self.AERONET_SUN_V2L2_SDA_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V2L2_SDA_DAILY_NAME]['PATH'] =\
            cr['obsfolders']['AERONET_SUN_V2L2_SDA_DAILY'].\
            replace('${BASEDIR}',self._obsbasedir)
        OBSCONFIG[self.AERONET_SUN_V2L2_SDA_DAILY_NAME]['START_YEAR'] =\
            cr['obsstartyears']['AERONET_SUN_V2L2_SDA_DAILY']
    
        OBSCONFIG[self.AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME]['PATH'] =\
            cr['obsfolders']['AERONET_SUN_V2L2_SDA_ALL_POINTS'].\
            replace('${BASEDIR}',self._obsbasedir)
        OBSCONFIG[self.AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_SUN_V2L2_SDA_ALL_POINTS']
    
        OBSCONFIG[self.AERONET_SUN_V3L15_AOD_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V3L15_AOD_DAILY_NAME]['PATH'] = cr['obsfolders']['AERONET_SUN_V3L15_AOD_DAILY'].replace('${BASEDIR}',self._obsbasedir)
        OBSCONFIG[self.AERONET_SUN_V3L15_AOD_DAILY_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_SUN_V3L15_AOD_DAILY']
    
        OBSCONFIG[self.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME]['PATH'] = cr['obsfolders']['AERONET_SUN_V3L15_AOD_ALL_POINTS'].replace('${BASEDIR}',self._obsbasedir)
        OBSCONFIG[self.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_SUN_V3L15_AOD_ALL_POINTS']
    
        OBSCONFIG[self.AERONET_SUN_V3L2_AOD_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V3L2_AOD_DAILY_NAME]['PATH'] = cr['obsfolders']['AERONET_SUN_V3L2_AOD_DAILY'].replace('${BASEDIR}',self._obsbasedir)
        OBSCONFIG[self.AERONET_SUN_V3L2_AOD_DAILY_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_SUN_V3L2_AOD_DAILY']
    
        OBSCONFIG[self.AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME]['PATH'] = cr['obsfolders']['AERONET_SUN_V3L2_AOD_ALL_POINTS'].replace('${BASEDIR}',self._obsbasedir)
        OBSCONFIG[self.AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_SUN_V3L2_AOD_ALL_POINTS']
    
        OBSCONFIG[self.AERONET_SUN_V3L15_SDA_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V3L15_SDA_DAILY_NAME]['PATH'] = \
            cr['obsfolders']['AERONET_SUN_V3L15_SDA_DAILY'].replace('${BASEDIR}',self._obsbasedir)
        OBSCONFIG[self.AERONET_SUN_V3L15_SDA_DAILY_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_SUN_V3L15_SDA_DAILY']
    
        OBSCONFIG[self.AERONET_SUN_V3L2_SDA_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V3L2_SDA_DAILY_NAME]['PATH'] = cr['obsfolders']['AERONET_SUN_V3L2_SDA_DAILY'].replace('${BASEDIR}',self._obsbasedir)
        OBSCONFIG[self.AERONET_SUN_V3L2_SDA_DAILY_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_SUN_V3L2_SDA_DAILY']

        OBSCONFIG[self.AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME]['PATH'] = cr['obsfolders']['AERONET_SUN_V3L2_SDA_ALL_POINTS'].replace('${BASEDIR}',self._obsbasedir)
        OBSCONFIG[self.AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_SUN_V3L2_SDA_ALL_POINTS']
    
        OBSCONFIG[self.AERONET_INV_V2L15_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_INV_V2L15_DAILY_NAME]['PATH'] = cr['obsfolders']['AERONET_INV_V2L15_DAILY'].replace('${BASEDIR}',self._obsbasedir)
        OBSCONFIG[self.AERONET_INV_V2L15_DAILY_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_INV_V2L15_DAILY']
    
        OBSCONFIG[self.AERONET_INV_V2L15_ALL_POINTS_NAME] = {}
        OBSCONFIG[self.AERONET_INV_V2L15_ALL_POINTS_NAME]['PATH'] = cr['obsfolders']['AERONET_INV_V2L15_ALL_POINTS'].replace('${BASEDIR}',self._obsbasedir)
        OBSCONFIG[self.AERONET_INV_V2L15_ALL_POINTS_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_INV_V2L15_ALL_POINTS']
    
        OBSCONFIG[self.AERONET_INV_V2L2_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_INV_V2L2_DAILY_NAME]['PATH'] = cr['obsfolders']['AERONET_INV_V2L2_DAILY'].replace('${BASEDIR}',self._obsbasedir)
        OBSCONFIG[self.AERONET_INV_V2L2_DAILY_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_INV_V2L2_DAILY']
    
        OBSCONFIG[self.AERONET_INV_V2L2_ALL_POINTS_NAME] = {}
        OBSCONFIG[self.AERONET_INV_V2L2_ALL_POINTS_NAME]['PATH'] = cr['obsfolders']['AERONET_INV_V2L2_ALL_POINTS'].replace('${BASEDIR}',self._obsbasedir)
        OBSCONFIG[self.AERONET_INV_V2L2_ALL_POINTS_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_INV_V2L2_ALL_POINTS']
    
        # Aeronet v3 inversions
        OBSCONFIG[self.AERONET_INV_V3L15_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_INV_V3L15_DAILY_NAME]['PATH'] = cr['obsfolders']['AERONET_INV_V3L15_DAILY'].replace('${BASEDIR}',self._obsbasedir)
        OBSCONFIG[self.AERONET_INV_V3L15_DAILY_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_INV_V2L15_DAILY']
        
        OBSCONFIG[self.AERONET_INV_V3L2_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_INV_V3L2_DAILY_NAME]['PATH'] = cr['obsfolders']['AERONET_INV_V3L2_DAILY'].replace('${BASEDIR}',self._obsbasedir)
        OBSCONFIG[self.AERONET_INV_V3L2_DAILY_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_INV_V2L15_DAILY']
        
        OBSCONFIG[self.EBAS_MULTICOLUMN_NAME] = {}
        OBSCONFIG[self.EBAS_MULTICOLUMN_NAME]['PATH'] = cr['obsfolders']['EBAS_MULTICOLUMN'].replace('${BASEDIR}',self._obsbasedir)
        OBSCONFIG[self.EBAS_MULTICOLUMN_NAME]['START_YEAR'] = cr['obsstartyears']['EBAS_MULTICOLUMN']
    
        OBSCONFIG[self.EEA_NAME] = {}
        OBSCONFIG[self.EEA_NAME]['PATH'] = cr['obsfolders']['EEA'].replace('${BASEDIR}',self._obsbasedir)
        OBSCONFIG[self.EEA_NAME]['START_YEAR'] = cr['obsstartyears']['EEA']

        OBSCONFIG[self.EARLINET_NAME] = {}
        OBSCONFIG[self.EARLINET_NAME]['PATH'] = cr['obsfolders']['EARLINET'].replace('${BASEDIR}',self._obsbasedir)
        OBSCONFIG[self.EARLINET_NAME]['START_YEAR'] = cr['obsstartyears']['EARLINET']
        
        cr.clear()
    
    def short_str(self):
        """Deprecated method"""
        return self.__str__()    
    
    def __str__(self):
        head = "Pyaerocom {}".format(type(self).__name__)
        s = "\n{}\n{}\n".format(head, len(head)*"-")
        for k, v in self.__dict__.items():
            if k.startswith('_'):
                pass
            if k=='VAR_PARAM':
                s += '\n{}\n{}'.format(k, list_to_shortstr(v.all_vars))
            elif isinstance(v, dict):
                s += "\n%s (dict)" %k
            elif isinstance(v, list):
                s += "\n%s (list)" %k
                s += list_to_shortstr(v)
            else:
                s += "\n%s: %s" %(k, v)
        return s

class GridIO(object):
    """Settings class for managing IO settings
    
    This class includes options related to the import of grid data. This 
    includes both options related to file search as well as preprocessing 
    options.
    
    Attributes
    ----------
    FILE_TYPE : str
        file type of data files. Defaults to .nc
    TS_TYPES : list
        list of strings specifying temporal resolution options encrypted in
        file names.
    DEL_TIME_BOUNDS : bool
        if True, preexisting bounds on time are deleted when grid data is 
        loaded. Else, nothing is done. Aerocom default is True
    SHIFT_LONS : bool
        if True, longitudes are shifted to 
        -180 <= lon <= 180 when data is loaded (in case they are defined 
        0 <= lon <= 360. Aerocom default is True.
    CHECK_TIME_FILENAME : bool
        the times stored in NetCDF files may be wrong or not stored according
        to the CF conventions. If True, the times are checked and if 
        :attr:`CORRECT_TIME_FILENAME`, corrected for on data import based what
        is encrypted in the 
        file name. In case of Aerocom models, it is ensured that the filename 
        contains both the year and the temporal resolution in the filenames 
        (for details see :class:`pyaerocom.io.FileConventionRead`).
        Aerocom default is True
    CORRECT_TIME_FILENAME : bool
        if True and time dimension in data is found to be different from 
        filename, it is attempted to be corrected
    EQUALISE_METADATA : bool
        if True (and if metadata varies between different NetCDF files that are
        supposed to be merged in time), the metadata in all loaded objects is 
        unified based on the metadata of the first grid (otherwise, 
        concatenating them in time might not work using the Iris interface).
        This might need to be reviewed and should be used with care if 
        specific metadata aspects of individual files need to be accessed.
        Aerocom default is True
    USE_RENAMED_DIR : bool
        if True, data files are searched within a subdirectory named "renamed" 
        that needs to exist withing the data directory of a certain model or
        obs data type. Aerocom default is True.
    USE_FILECONVENTION : bool
        if True, file names are strictly required to follow one of the file
        naming conventions that can be specified in the file 
        `file_conventions.ini <https://github.com/metno/pyaerocom/tree/master/
        pyaerocom/data>`__. Aerocom default is True.
    INCLUDE_SUBDIRS : bool
        if True, search for files is expanded to all subdirecories included in
        data directory. Aerocom default is False.
    """
    def __init__(self, **kwargs):
        self.FILE_TYPE = ".nc"
        # it is important to keep them in the order from highest to lowest
        # resolution
        self.TS_TYPES = ["hourly", "3hourly", "daily", "monthly", "yearly"]
        #delete time bounds if they exist in netCDF files
        self.DEL_TIME_BOUNDS = True
        #shift longitudes to -180 -> 180 repr (if applicable)
        self.SHIFT_LONS = True 
        
        self.CHECK_TIME_FILENAME = True
        self.CORRECT_TIME_FILENAME = True
        
        self.CHECK_DIM_COORDS = False
         # check and update metadata dictionary on Cube load since 
         # iris concatenate of Cubes only works if metadata is equal
        self.EQUALISE_METADATA = True
        
        self.USE_RENAMED_DIR = True
        
        self.INCLUDE_SUBDIRS = False
        
    def to_dict(self):
        """Convert object to dictionary
        
        Returns
        -------
        dict
            settings dictionary
        """
        return self.__dict__
    
    def from_dict(self, dictionary=None, **settings):
        """Import settings from dictionary"""
        if not dictionary:
            dictionary = {}
        dictionary.update(settings)
        for key, val in dictionary.items():
            self[key] = val

    def __setitem__(self, key, value):
        """Set item
        
        GridIO["<key>"] = value <=> GridIO.<key> = value
        <=> GridIO.__setitem__(<key>, value)
        
        Raises
        ------
        IOError 
            if key is not a valid setting
        """
        if not key in self.__dict__.keys():
            raise IOError("Could not update IO setting: Invalid key")
        self.__dict__[key] = value
        
    def __getitem__(self, key):
        """Get item using curly brackets
        
        GridIO["<key>"] => value
        
        """
        if not key in self.__dict__.keys():
            raise IOError("Invalid attribute")
        return self.__dict__[key]
    
    def __str__(self):
        head = "Pyaerocom {}".format(type(self).__name__)
        return ("\n{}\n{}\n{}".format(head, 
                                      len(head)*"-",
                                      dict_to_str(self.to_dict())))
        
if __name__=="__main__":
    config = Config()
    
    print(config.short_str())
    
    #config.BASEDIR = '/home/'
    print(config.short_str())