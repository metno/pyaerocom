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
from time import time
import numpy as np
import os
import getpass
from collections import OrderedDict as od
from pathlib import Path

import pyaerocom.obs_io as obs_io
from pyaerocom.grid_io import GridIO
from pyaerocom._lowlevel_helpers import (list_to_shortstr,
                                         chk_make_subdir,
                                         check_dir_access,
                                         check_write_access)

from pyaerocom.exceptions import DeprecationError, DataSourceError
from pyaerocom.variable import VarCollection
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

    #: name of EBAS sqlite database
    #EBAS_SQL_DB_NAME = 'ebas_file_index.sqlite3'

    #: boolean specifying wheter EBAS DB is copied to local cache for faster
    #: access, defaults to True
    EBAS_DB_LOCAL_CACHE = True

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

    OLD_AEROCOM_REGIONS = ['WORLD', 'ASIA', 'AUSTRALIA', 'CHINA',
                           'EUROPE', 'INDIA', 'NAFRICA', 'SAFRICA', 'SAMERICA',
                           'NAMERICA']

    URL_HTAP_MASKS = 'https://pyaerocom.met.no/pyaerocom-suppl/htap_masks/'

    HTAP_REGIONS = ['PAN', 'EAS', 'NAF', 'MDE', 'LAND',
                    'SAS', 'SPO', 'OCN',  'SEA', 'RBU',
                    'EEUROPE', 'NAM', 'WEUROPE', 'SAF',
                    'USA', 'SAM', 'EUR', 'NPO', 'MCA']

    RM_CACHE_OUTDATED = True

    #: Name of the file containing the revision string of an obs data network
    REVISION_FILE = 'Revision.txt'

    #: timeout to check if one of the supported server locations can be
    #: accessed
    SERVER_CHECK_TIMEOUT = 2 #0.1 #s

    _outhomename = 'MyPyaerocom'
    _testdatadirname = 'testdata-minimal'

    from pyaerocom import __dir__
    _config_ini_lustre = os.path.join(__dir__, 'data', 'paths.ini')
    _config_ini_user_server = os.path.join(__dir__, 'data', 'paths_user_server.ini')
    _config_ini_testdata = os.path.join(__dir__, 'data', 'paths_testdata.ini')
    _config_ini_localdb = os.path.join(__dir__, 'data', 'paths_local_database.ini')

    # this dictionary links environment ID's with corresponding ini files
    _config_files = {
            'metno'            : _config_ini_lustre,
            'users-db'         : _config_ini_user_server,
            'testdata'         : _config_ini_testdata,
            'local-db'         : _config_ini_localdb
    }

    # this dictionary links environment ID's with corresponding subdirectory
    # names that are required to exist in order to load this environment
    _check_subdirs_cfg = {
            'metno'       : 'aerocom',
            'users-db'    : 'AMAP',
            'testdata'    : 'modeldata',
            'local-db'    : 'modeldata'
    }

    _var_info_file = os.path.join(__dir__, 'data', 'variables.ini')
    _coords_info_file = os.path.join(__dir__, 'data', 'coords.ini')

    #_mask_location = '/home/hannas/Desktop/htap/'
    # todo update to ~/MyPyaerocom/htap_masks/' ask jonas

    # these are searched in preferred order both in root and home
    _DB_SEARCH_SUBDIRS = od()
    _DB_SEARCH_SUBDIRS['lustre/storeA/project'] = 'metno'
    #_DB_SEARCH_SUBDIRS['lustre/storeB/project/aerocom'] = 'metno'
    _DB_SEARCH_SUBDIRS['metno/aerocom_users_database'] = 'users-db'
    _DB_SEARCH_SUBDIRS['pyaerocom-testdata/'] = 'testdata'
    _DB_SEARCH_SUBDIRS['MyPyaerocom/pyaerocom-testdata'] = 'testdata'
    _DB_SEARCH_SUBDIRS['MyPyaerocom/data'] = 'local-db'

    DONOTCACHEFILE = None

    ERA5_SURFTEMP_FILENAME = 'era5.msl.t2m.201001-201012.nc'

    _LUSTRE_CHECK_PATH = '/project/aerocom/aerocom1/'

    def __init__(self, basedir=None,
                 output_dir=None, config_file=None,
                 cache_dir=None, colocateddata_dir=None,
                 write_fileio_err_log=True,
                 activate_caching=True):
        t0 = time()
        # Loggers
        from pyaerocom import print_log, logger
        self.print_log = print_log
        self.logger = logger

        # Directories
        self._cachedir = cache_dir
        self._outputdir = output_dir

        self._colocateddatadir = colocateddata_dir
        self._filtermaskdir = None
        self._local_tmp_dir = None
        self._downloaddatadir = None
        self._confirmed_access = []
        self._rejected_access = []

        # Options
        self._caching_active = activate_caching

        self._var_param = None
        self._coords = None

        # Attributes that are used to store search directories
        self.OBSLOCS_UNGRIDDED = od()
        self.SUPPLDIRS = od()
        self._search_dirs = []

        self.WRITE_FILEIO_ERR_LOG = write_fileio_err_log

        self.last_config_file = None
        self._ebas_flag_info = None

        #: Settings for reading and writing of gridded data
        self.GRID_IO = GridIO()
        self.logger.info('Initiating pyaerocom configuration')

        # checks and validates / invalidates input basedir and config_file
        # if both are provided
        (basedir,
         config_file) = self._check_input_basedir_and_config_file(basedir,
                                                                  config_file)

        if not isinstance(config_file, str) or not os.path.exists(config_file):
            self.logger.info('Checking database access...')
            try:
                basedir, config_file = self.infer_basedir_and_config()
            except FileNotFoundError:
                pass

        if config_file is not None:
            try:
                self.read_config(config_file, basedir=basedir)
            except Exception as e:
                self.print_log.warning("Failed to read config. Error: {}"
                                       .format(repr(e)))
        # create MyPyaerocom directory
        chk_make_subdir(self.HOMEDIR, self._outhomename)
        self.logger.info("ELAPSED TIME Config.__init__: {:.5f} s".format(time()-t0))

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

    def _check_access(self, loc, timeout=None):
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
        if loc is None:
            return False
        loc = str(Path(loc)) # make sure the path is set correctly
        if loc in self._confirmed_access:
            return True
        elif loc in self._rejected_access:
            return False
# =============================================================================
#             self.print_log.warning('Attempting access to location {}, which '
#                                    'has been checked before and failed. This '
#                                    'may slow things down.'.format(loc))
# =============================================================================

        if timeout is None:
            timeout = self.SERVER_CHECK_TIMEOUT

        self.logger.info('Checking access to: {}'.format(loc))
        if check_dir_access(loc, timeout=timeout):
            self._confirmed_access.append(loc)
            return True
        self._rejected_access.append(loc)
        return False

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

    def _check_basedir_environment(self, basedir):
        """Check if input basedir can be linked with one of the supported databases

        Note
        ----
        Does not check if the path actually exists.
        """
        basedir = os.path.normpath(basedir)
        import pathlib
        new = pathlib.Path(basedir)
        last = new.parts[-1]
        for search_dir, env_id in self._DB_SEARCH_SUBDIRS.items():
            if pathlib.Path(search_dir).parts[0] == last:
                check = os.path.join(*new.parts[:-1], search_dir)
                if self._check_access(check):
                    self.print_log.info('Input path {} was identified to be '
                                   'connected with database {} and will be '
                                   'updated to {}'.format(basedir, env_id, check))
                    return check
        return basedir

    def _infer_config_from_basedir(self, basedir):

        basedir = os.path.normpath(basedir)
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
        raise FileNotFoundError('Could not find access to any registered '
                                'database')

    @property
    def has_access_users_database(self):
        chk_dir = self._check_subdirs_cfg['users-db']
        chk_paths = [os.path.join('/metno/aerocom_users_database/', chk_dir),
                     os.path.join(self.HOMEDIR, '/aerocom_users_database/', chk_dir)]
        for p in chk_paths:
            if self._check_access(p):
                return True
        return False

    @property
    def has_access_lustre(self):
        """Boolean specifying whether MetNO AeroCom server is accessible"""
        for path in self._search_dirs:
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
    def DATA_SEARCH_DIRS(self):
        """
        Directories which pyaerocom will consider for data access

        Note
        ----
        This corresponds to directories considered for searching gridded
        data (e.g. models and level 3 satellite products).  Please
        see :attr:`OBSLOCS_UNGRIDDED` for available data directories
        for reading of ungridded data.

        Returns
        -------
        list
            list of directories

        """
        return self._search_dirs

    @property
    def _TESTDATADIR(self):
        """Directory where testdata is stored (only for automated testing)"""
        return os.path.join(self.OUTPUTDIR, self._testdatadirname)

    @property
    def FILTERMASKKDIR(self):
        if not check_write_access(self._filtermaskdir):
            outdir = self.OUTPUTDIR
            self._filtermaskdir = chk_make_subdir(outdir, 'filtermasks')
        return self._filtermaskdir

    @property
    def COLOCATEDDATADIR(self):
        """Directory for accessing and saving colocated data objects"""
        if not check_write_access(self._colocateddatadir):
            outdir = self.OUTPUTDIR
            self._colocateddatadir = chk_make_subdir(outdir, 'colocated_data')
        return self._colocateddatadir

    @property
    def LOCAL_TMP_DIR(self):
        """Local TEMP directory"""
        if self._local_tmp_dir is None:
            self._local_tmp_dir = '{}/tmp'.format(self.OUTPUTDIR)
        if not self._check_access(self._local_tmp_dir):
            try:
                os.mkdir(self._local_tmp_dir)
            except Exception:
                raise FileNotFoundError('const.LOCAL_TMP_DIR {} is not set or '
                                        'does not exist and cannot be created')
        return self._local_tmp_dir

    @LOCAL_TMP_DIR.setter
    def LOCAL_TMP_DIR(self, val):
        self._local_tmp_dir = val

    @property
    def DOWNLOAD_DATADIR(self):
        """Directory where data is downloaded into"""
        if self._downloaddatadir is None:
            self._downloaddatadir = chk_make_subdir(self.OUTPUTDIR, 'data')
        return self._downloaddatadir

    @DOWNLOAD_DATADIR.setter
    def DOWNLOAD_DATADIR(self, val):
        if not isinstance(val, str):
            raise ValueError('Please provide str')
        elif not os.path.exists(val):
            try:
                os.mkdir(val)
            except Exception:
                raise IOError('Input directory {} does not exist and can '
                              'also not be created'.format(val))
        self._downloaddatadir =  val

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
    def BASEDIR(self):
        """DEPRECATED since v0.9.0: Base directory of data
        """
        msg=('BASEDIR attribute is deprecated, please see attrs. '
             'DATA_SEARCH_DIRS for available search directories and '
             'method add_data_search_dir for adding new locations. You can '
             'still use the setter method for adding a database location')
        raise DeprecationError(msg)
        #return self._modelbasedir

# =============================================================================
#     @BASEDIR.setter
#     def BASEDIR(self, value):
#         if not self._check_access(value):
#             raise FileNotFoundError('Cannot change data base directory. '
#                                     'Input directory does not exist')
#
#         value = self._check_basedir_environment(value)
#
#         self._obsbasedir = value
#         self._modelbasedir = value
#
#         try:
#             config_file, env_id = self._infer_config_from_basedir(value)
#             self.print_log.info('Adding paths for {} with root at {}'
#                                 .format(env_id, value))
#             self.read_config(config_file, keep_basedirs=True)
#         except FileNotFoundError:
#             self.print_log.warning('Failed to infer path environment for '
#                                    'input dir {}. No search paths will be added'
#                                    .format(value))
# =============================================================================

    @property
    def DIR_INI_FILES(self):
        """Directory containing configuration files"""
        from pyaerocom import __dir__
        return os.path.join(__dir__, 'data')

    @property
    def ETOPO1_AVAILABLE(self):
        """
        Boolean specifying if access to ETOPO1 dataset is provided

        Returns
        -------
        bool
        """
        if 'etopo1' in self.SUPPLDIRS and os.path.exists(self.SUPPLDIRS['etopo1']):
            return True
        return False

    @property
    def GEONUM_AVAILABLE(self):
        """
        Boolean specifying if geonum library is installed

        Returns
        -------
        bool

        """
        try:
            import geonum
            return True
        except ModuleNotFoundError:
            return False

    @property
    def BASEMAP_AVAILABLE(self):
        """
        Boolean specifying if basemap library is installed

        Returns
        -------
        bool

        """
        try:
            from mpl_toolkits.basemap import Basemap
            return True
        except ModuleNotFoundError:
            return False

    def connect_database(self, location):
        if not self._check_access(location):
            raise FileNotFoundError('Cannot add {}: location does not exist')

        raise NotImplementedError

# =============================================================================
#     @property
#     def EBASMC_SQL_DATABASE(self):
#         """Path to EBAS SQL database"""
#         dbname = self.EBAS_SQL_DB_NAME
#         if not 'EBASMC' in self.OBSLOCS_UNGRIDDED:
#             return None
#         loc_remote = os.path.join(self.OBSLOCS_UNGRIDDED["EBASMC"], dbname)
#         if self.EBAS_DB_LOCAL_CACHE:
#             loc_local = os.path.join(self.CACHEDIR, dbname)
#             return self._check_ebas_db_local_vs_remote(loc_remote, loc_local)
#
#         return loc_remote
# =============================================================================

# =============================================================================
#     @property
#     def EBASMC_DATA_DIR(self):
#         """Data directory of EBAS multicolumn files"""
#         return os.path.join(self.OBSLOCS_UNGRIDDED["EBASMC"], 'data/')
# =============================================================================

    @property
    def EBAS_FLAGS_FILE(self):
        """Location of CSV file specifying meaning of EBAS flags"""
        from pyaerocom import __dir__
        return os.path.join(__dir__, 'data', 'ebas_flags.csv')

    @property
    def OBS_IDS_UNGRIDDED(self):
        """List of all IDs of observations"""
        return [x for x in self.OBSLOCS_UNGRIDDED.keys()]

    @property
    def OBSDIRS_UNGRIDDED(self):
        """List of all IDs of observations"""
        return [x for x in self.OBSLOCS_UNGRIDDED.values()]

    @property
    def ERA5_SURFTEMP_FILE(self):
        if 'era5' in self.SUPPLDIRS:
            sdir = self.SUPPLDIRS['era5']
            if os.path.exists(sdir) and self.ERA5_SURFTEMP_FILENAME in os.listdir(sdir):
                return os.path.join(sdir, self.ERA5_SURFTEMP_FILENAME)
        raise FileNotFoundError('ERA Interim surface temperature data cannot '
                                'be accessed (check lustre connection)')

    def make_default_vert_grid(self):
        """Makes default vertical grid for resampling of profile data"""
        step = self.DEFAULT_VERT_GRID_DEF['step']
        offs = int(step/2)
        return np.arange(self.DEFAULT_VERT_GRID_DEF['lower'] + offs,
                         self.DEFAULT_VERT_GRID_DEF['upper'] - offs,
                         step)

    def add_data_search_dir(self, *dirs):
        """Add data search directories for database browsing"""
        for loc in dirs:
            if not self._check_access(loc):
                raise FileNotFoundError('Input location {} could not be accessed'
                                        .format(loc))
            self._search_dirs.append(loc)

    def add_ungridded_obs(self, obs_id, data_dir, reader=None, check_read=False):
        """Add a network to the data search structure

        Parameters
        ----------
        obs_id : str
            name of network. E.g. MY_OBS or EBASMC
        data_dir : str
            directory where data files are stored
        reader : pyaerocom.io.ReadUngriddedBase, optional
            reading class used to import these data. If `obs_id` is known
            (e.g. EBASMC) this is not needed.

        Raises
        ------
        AttributeError
            if the network name is already reserved in :attr:`OBSLOCS_UNGRIDDED`
        ValueError
            if the data directory does not exist
        """
        if obs_id in self.OBSLOCS_UNGRIDDED:
            raise AttributeError('Network with ID {} is already registered at '
                                 '{}'.format(obs_id, self.OBSLOCS_UNGRIDDED[obs_id]))
        elif not self._check_access(data_dir):
            raise ValueError('Input data directory cannot be accessed')
        if reader is None:
            from pyaerocom.io.utils import get_ungridded_reader
            reader =  get_ungridded_reader(obs_id)

        if not obs_id in reader.SUPPORTED_DATASETS:
            reader.SUPPORTED_DATASETS.append(obs_id)
        self.OBSLOCS_UNGRIDDED[obs_id] = data_dir
        if check_read:
            self._check_obsreader(obs_id, data_dir, reader)

    def _check_obsreader(self, obs_id, data_dir, reader):
        """
        Check if files can be accessed when registering new dataset

        Parameters
        ----------
        obs_id : str
            name of obsnetwork
        data_dir : str
            directory containing data files
        reader : ReadUngriddedBase
            reading interface
        """
        check = reader(obs_id)
        path = check.DATASET_PATH
        assert path == data_dir
        try:
            check.get_file_list()
        except DataSourceError:
            if 'renamed' in os.listdir(data_dir):
                chk_dir = os.path.join(data_dir, 'renamed')
                self.OBSLOCS_UNGRIDDED.pop(obs_id)
                self.add_ungridded_obs(obs_id, chk_dir, reader,
                                       check_read=True)

    def change_database(self, database_name='metno', keep_root=False):
        """
        Changes the path setup for a specific data environment

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
        """
        raise NotImplementedError('This method is deprecated since v090 ...')
        if not database_name in self.ALL_DATABASE_IDS:
            raise ValueError('Unkown database name {}. Please choose from '
                             '{}'.format(database_name, self.ALL_DATABASE_IDS))
        self.read_config(self._config_files[database_name],
                         keep_basedirs=keep_root)

    @property
    def ebas_flag_info(self):
        """Information about EBAS flags

        Note
        ----
        Is loaded upon request -> cf.
        :attr:`pyaerocom.io.ebas_nasa_ames.EbasFlagCol.FLAG_INFO`

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

    def read_config(self, config_file, basedir=None,
                    init_obslocs_ungridded=False,
                    init_data_search_dirs=False):
        #Read and import paths from ini file

        if not os.path.isfile(config_file):
            raise IOError("Configuration file paths.ini at %s does not exist "
                          "or is not a file"
                          %config_file)

        if init_obslocs_ungridded:
            self.OBSLOCS_UNGRIDDED = od()
        if init_data_search_dirs:
            self._search_dirs = []

        cr = ConfigParser()
        cr.read(config_file)
        #init base directories for Model data
        if cr.has_section('modelfolders'):
           self._add_searchdirs(cr, basedir)

        if cr.has_section('obsfolders'):
            self._add_obsconfig(cr, basedir)

        if cr.has_section('outputfolders'):
            self._init_output_folders_from_cfg(cr)

        if cr.has_section('supplfolders'):
            if basedir is None and 'BASEDIR' in cr['supplfolders']:
                basedir = cr['supplfolders']['BASEDIR']

            for name, path in cr['supplfolders'].items():
                if '${BASEDIR}' in path:
                    path = path.replace('${BASEDIR}', basedir)
                self.SUPPLDIRS[name] = path

        cr.clear()
        self.GRID_IO.load_aerocom_default()
        self.last_config_file = config_file

    def _resolve_basedir(self, locs, chk_dirs):
        repl = '${BASEDIR}'
        for loc in locs:
            if repl in loc:
                for chk_dir in chk_dirs:
                    chk = Path(loc.replace(repl, chk_dir))
                    if self._check_access(chk):
                        return chk_dir
        raise FileNotFoundError('Could not confirm any directory...')

    def _add_searchdirs(self, cr, basedir=None):

        t0 = time()

        chk_dirs = []
        if basedir is not None and self._check_access(basedir):
            chk_dirs.append(basedir)

        mcfg = cr['modelfolders']

        # check and update model base directory if applicable
        if 'BASEDIR' in mcfg:
            _dir = mcfg['BASEDIR']
            if '${HOME}' in _dir:
                _dir = _dir.replace('${HOME}', os.path.expanduser('~'))
            if not _dir in chk_dirs and self._check_access(_dir):
                chk_dirs.append(_dir)
        if len(chk_dirs) == 0:
            return False

        # get all locations defined in config file as list
        locs = (mcfg['dir'].replace('\n','').split(','))

        # find first location that contains BASEDIR to determine
        try:
            basedir = str(self._resolve_basedir(locs, chk_dirs))
        except FileNotFoundError:
            basedir = None

        for loc in locs:
            candidate = loc.replace('${BASEDIR}', basedir)
            if not candidate in self._search_dirs:
                self._search_dirs.append(candidate)
        self.logger.info("ELAPSED TIME _add_searchdirs: {:.5f} s".format(time()-t0))
        return True

    def _add_obsconfig(self, cr, basedir=None):
        t0 = time()
        chk_dirs = []
        if basedir is not None and self._check_access(basedir):
            chk_dirs.append(basedir)

        cfg = cr['obsfolders']

        # check and update model base directory if applicable
        if 'BASEDIR' in cfg:
            _dir = cfg['BASEDIR']
            if '${HOME}' in _dir:
                _dir = _dir.replace('${HOME}', os.path.expanduser('~'))
            if not _dir in chk_dirs and self._check_access(_dir):
                chk_dirs.append(_dir)
        if len(chk_dirs) == 0:
            return False

        names_cfg = self._add_obsnames_config(cr)

        candidates = {}
        dirconfirmed = None
        repl = '${BASEDIR}'
        if cr.has_section('obsfolders'):
            for obsname, path in cr['obsfolders'].items():
                if obsname.lower() == 'basedir':
                    continue
                name_str = '{}_NAME'.format(obsname.upper())
                if name_str in names_cfg:
                    ID = self.__dict__[name_str]
                else:
                    ID = self._add_obsname(obsname)
                candidates[ID] = path
                # candidate for checking access
                if dirconfirmed is None and repl in path:
                    for chk_dir in chk_dirs:
                        chk = Path(path.replace(repl, chk_dir))
                        if self._check_access(chk):
                            dirconfirmed = str(chk_dir)

        for name, loc in candidates.items():
            if '${BASEDIR}' in loc and dirconfirmed is not None:
                loc = loc.replace('${BASEDIR}', dirconfirmed)
            if '${HOME}' in loc:
                loc = loc.replace('${HOME}', os.path.expanduser('~'))

            self.OBSLOCS_UNGRIDDED[name] = loc
        self.logger.info("ELAPSED TIME _add_obsconfig: {:.5f} s".format(time()-t0))

    def _init_output_folders_from_cfg(self, cr):
        t0 = time()
        cfg = cr['outputfolders']
        if 'CACHEDIR' in cfg and not self._check_access(self._cachedir):
            self._cachedir = cfg['CACHEDIR']

        if 'OUTPUTDIR' in cfg and not self._check_access(self._outputdir):
            self._outputdir = cfg['OUTPUTDIR']

        if 'COLOCATEDDATADIR' in cfg and not self._check_access(self._colocateddatadir):
            self._colocateddatadir = cfg['COLOCATEDDATADIR']

        if 'LOCALTMPDIR' in cfg:
            _dir = cfg['LOCALTMPDIR']
            # expand ${HOME}
            if '${HOME}' in _dir:
                _dir = _dir.replace('${HOME}', os.path.expanduser('~'))
            if '${USER}' in _dir:
                _dir = _dir.replace('${USER}', getpass.getuser())

            self._local_tmp_dir = _dir

        self.logger.info("ELAPSED TIME init outputdirs: {:.5f} s".format(time()-t0))

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

    ### DEPRECATED BUT STILL FUNCTIONAL CODE
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

    @property
    def OBSDIRS(self):
        msg = 'Attr. OBSDIRS is deprecated, use OBSDIRS_UNGRIDDED instead'
        self.print_log.warning(DeprecationWarning(msg))
        return self.OBSDIRS_UNGRIDDED

    @property
    def OBS_IDS(self):
        msg = 'Attr. OBS_IDS is deprecated, use OBS_IDS_UNGRIDDED instead'
        self.print_log.warning(DeprecationWarning(msg))
        return self.OBS_IDS_UNGRIDDED

    @property
    def OBSCONFIG(self):
        msg = ('Attr. OBSCONFIG is deprecated, use OBSLOCS_UNGRIDDED instead. '
               'Note that the latter maps ids with paths directly and has no '
               '{"PATH":<loc>} style entries')
        self.print_log.warning(DeprecationWarning(msg))
        cfg = {}
        for obsid, path in self.OBSLOCS_UNGRIDDED.items():
            cfg[obsid] = {'PATH':path}
        return cfg

    @property
    def MODELDIRS(self):
        msg = 'Attr. MODELDIRS is deprecated, use DATA_SEARCH_DIRS instead'
        self.print_log.warning(DeprecationWarning(msg))
        return self.DATA_SEARCH_DIRS

if __name__=="__main__":
    import pyaerocom as pya
    #print(pya.const)
    print(pya.const.has_access_lustre)