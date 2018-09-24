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
from warnings import warn
from collections import OrderedDict as od
import pyaerocom.obs_io as obs_io
from pyaerocom._lowlevel_helpers import list_to_shortstr, dict_to_str
from pyaerocom.variable import AllVariables
try:
    from ConfigParser import ConfigParser
except: 
    from configparser import ConfigParser
    
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
    

class Config(object):
    """Class containing relevant paths for read and write routines"""
    
    def __init__(self, model_base_dir=None, obs_base_dir=None, 
                 out_base_dir=None, config_file=None, 
                 obs_cache_dir=None, write_fileio_err_log=True):
        
        #: Lowest possible year in data
        self.MIN_YEAR = 0
        #: Highest possible year in data
        self.MAX_YEAR = 20000
        
        #: Settings for reading and writing of gridded data
        self.GRID_IO = GridIO()
        
        #: Wavelength tolerance for observations if data for required wavelength
        #: is not available
        self.OBS_WAVELENGTH_TOL_NM = obs_io.OBS_WAVELENGTH_TOL_NM
        
        #: This boolean can be used to enable / disable the former (i.e. use
        #: available wavelengths of variable in a certain range around variable
        #: wavelength).
        self.OBS_ALLOW_ALT_WAVELENGTHS = obs_io.OBS_ALLOW_ALT_WAVELENGTHS
        
        self.GCOSPERCENTCRIT =   np.float(0.1)
        self.GCOSABSCRIT     =   np.float(0.04)
        
        #names of the different obs networks
        self.OBSNET_NONE = 'NONE'
        self.NOMODELNAME = 'OBSERVATIONS-ONLY'

        # Name of the file containing the revision string of an obs data network
        self.REVISION_FILE = 'Revision.txt'
        
        ### NAMES
        #default names of the different obs networks
        #might get overwritten from paths.ini see func read_config
        #Aeronet V2
        self.AERONET_SUN_V2L15_AOD_DAILY_NAME = 'AeronetSunV2Lev1.5.daily'
        self.AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME = 'AeronetSun_2.0_NRT'
        self.AERONET_SUN_V2L2_AOD_DAILY_NAME = 'AeronetSunV2Lev2.daily'
        self.AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME = 'AeronetSunV2Lev2.AP'
        self.AERONET_SUN_V2L2_SDA_DAILY_NAME = 'AeronetSDAV2Lev2.daily'
        self.AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME = 'AeronetSDAV2Lev2.AP'
        
        #Aeronet V3
        self.AERONET_SUN_V3L15_AOD_DAILY_NAME = 'AeronetSunV3Lev1.5.daily'
        self.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME = 'AeronetSunV3Lev1.5.AP'
        self.AERONET_SUN_V3L2_AOD_DAILY_NAME = 'AeronetSunV3Lev2.daily'
        self.AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME = 'AeronetSunV3Lev2.AP'
        self.AERONET_SUN_V3L15_SDA_DAILY_NAME = 'AeronetSDAV3Lev1.5.daily'
        self.AERONET_SUN_V3L15_SDA_ALL_POINTS_NAME = 'AeronetSDAV3Lev1.5.AP'
        self.AERONET_SUN_V3L2_SDA_DAILY_NAME = 'AeronetSDAV3Lev2.daily'
        self.AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME = 'AeronetSDAV3Lev2.AP'

        # inversions
        self.AERONET_INV_V2L15_DAILY_NAME = 'AeronetInvV2Lev1.5.daily'
        self.AERONET_INV_V2L15_ALL_POINTS_NAME = 'AeronetInvV2Lev1.5.AP'
        self.AERONET_INV_V2L2_DAILY_NAME = 'AeronetInvV2Lev2.daily'
        self.AERONET_INV_V2L2_ALL_POINTS_NAME = 'AeronetInvV2Lev2.AP'
        #
        self.EBAS_MULTICOLUMN_NAME = 'EBASMC'
        self.EEA_NAME = 'EEAAQeRep'

        # Earlinet;
        self.EARLINET_NAME = 'EARLINET'
        
        # Attributes that are used to store import results
        self.OBSCONFIG = od()
        self.MODELDIRS = []
        
        # Directories
        self.MODELBASEDIR = None
        self.OBSBASEDIR = None
        
        self.OBSDATACACHEDIR = None
        self.LOGFILESDIR = None
        self.OUT_BASEDIR = None
        
        self.WRITE_FILEIO_ERR_LOG = write_fileio_err_log
        if isinstance(config_file, str) and os.path.exists(config_file):
            self._config_ini = config_file
        else:
            from pyaerocom import __dir__
            self._config_ini = os.path.join(__dir__, 'data', 'paths.ini')
        
        if self.check_dir(model_base_dir):
            self.MODELBASEDIR = model_base_dir
        if self.check_dir(obs_base_dir):
            self.OBSBASEDIR = obs_base_dir
        if self.check_dir(out_base_dir):
            self.OUT_BASEDIR = out_base_dir
        if self.check_dir(obs_cache_dir):
            self.OBSDATACACHEDIR = obs_cache_dir
         
        try:
            self.read_config(config_file)
        except Exception as e:
            print("Failed to read config file. Error: %s" %repr(e))
        
        if not self.check_dir(self.OUT_BASEDIR):
            self.OUT_BASEDIR = os.path.join(os.path.expanduser("~"), "pyaerocom")
            if not os.path.exists(self.OUT_BASEDIR):
                os.mkdir(self.OUT_BASEDIR)
        if not self.check_dir(self.OBSDATACACHEDIR):
            self.OBSDATACACHEDIR = os.path.join(self.OUT_BASEDIR, "_cache")
            if not os.path.exists(self.OBSDATACACHEDIR):
                os.mkdir(self.OBSDATACACHEDIR)
        if not self.check_dir(self.LOGFILESDIR):
            self.LOGFILESDIR = os.path.join(self.OUT_BASEDIR, "_log")
            if not os.path.exists(self.LOGFILESDIR):
                os.mkdir(self.LOGFILESDIR)
        
        # if this file exists no cache file is read
        # used to ease debugging
        self.DONOTCACHEFILE = os.path.join(self.OBSDATACACHEDIR, 'DONOTCACHE')
        self.PLOT_DIR = os.path.join(self.OUT_BASEDIR, "plots")
        if not self.check_dir(self.PLOT_DIR):
            os.mkdir(self.PLOT_DIR)
        from time import time
        t0=time()
        self.VAR_PARAM = AllVariables()
        print('Elapsed time init all variables: {} s'.format(time()-t0))
        self.READY
    
      
    @property 
    def BASEDIR(self):
        """Base directory of data"""
        return self.MODELBASEDIR
    
    @property
    def COLLOCATED_DATA_DIR(self):
        path = os.path.join(self.BASEDIR, 'aerocom2/pyaerocom/colocated-output')
        if not os.path.exists(path):
            path = os.path.join(self.OUT_BASEDIR + 'colocated-output')
            if not os.path.exists(path):
                os.mkdir(path)
        return path
            
    @property
    def READY(self):
        """Checks if relevant directories exist, returns True or False"""
        ok =True
        if not self.check_dir(self.MODELBASEDIR):
            warn("Model base directory %s does not exist")
            ok=False
        if not self.check_dir(self.OBSBASEDIR):
            warn("Observations base directory %s does not exist")
            ok=False
        if not self.check_dir(self.OBSDATACACHEDIR):
            warn("Observations cache directory %s does not exist")
        return ok 
    
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
    
    @property
    def CACHEDIR(self):
        """Directory for storing cached files"""
        return self.OBSDATACACHEDIR
    
    def check_dir(self, path):
        """Checks if directory exists"""
        if isinstance(path, str) and os.path.isdir(path):
            return True
        return False
    
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
        #init base directories for Model data
        if not keep_basedirs or not self.check_dir(self.MODELBASEDIR):
            self.MODELBASEDIR = cr['modelfolders']['BASEDIR']
        
        self.MODELDIRS = (cr['modelfolders']['dir'].
                          replace('${BASEDIR}', self.MODELBASEDIR).
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
        if not keep_basedirs or not self.check_dir(self.OBSBASEDIR):
            self.OBSBASEDIR = cr['obsfolders']['BASEDIR']
            
        OBSCONFIG = self.OBSCONFIG
        OBSCONFIG[self.AERONET_SUN_V2L15_AOD_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V2L15_AOD_DAILY_NAME]['PATH'] =\
        cr['obsfolders']['AERONET_SUN_V2L15_AOD_DAILY'].\
        replace('${BASEDIR}', self.OBSBASEDIR)
        
        OBSCONFIG[self.AERONET_SUN_V2L15_AOD_DAILY_NAME]['START_YEAR'] =\
            cr['obsstartyears']['AERONET_SUN_V2L15_AOD_DAILY']
    
        OBSCONFIG[self.AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME]['PATH'] =\
            cr['obsfolders']['AERONET_SUN_V2L15_AOD_ALL_POINTS'].\
            replace('${BASEDIR}', self.OBSBASEDIR)
        OBSCONFIG[self.AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME]['START_YEAR'] =\
            cr['obsstartyears']['AERONET_SUN_V2L15_AOD_ALL_POINTS']
    
        OBSCONFIG[self.AERONET_SUN_V2L2_AOD_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V2L2_AOD_DAILY_NAME]['PATH'] =\
            cr['obsfolders']['AERONET_SUN_V2L2_AOD_DAILY'].\
            replace('${BASEDIR}', self.OBSBASEDIR)
        OBSCONFIG[self.AERONET_SUN_V2L2_AOD_DAILY_NAME]['START_YEAR'] =\
            cr['obsstartyears']['AERONET_SUN_V2L2_AOD_DAILY']
    
        OBSCONFIG[self.AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME]['PATH'] =\
            cr['obsfolders']['AERONET_SUN_V2L2_AOD_ALL_POINTS'].\
            replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME]['START_YEAR'] =\
            cr['obsstartyears']['AERONET_SUN_V2L2_AOD_ALL_POINTS']
    
        OBSCONFIG[self.AERONET_SUN_V2L2_SDA_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V2L2_SDA_DAILY_NAME]['PATH'] =\
            cr['obsfolders']['AERONET_SUN_V2L2_SDA_DAILY'].\
            replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.AERONET_SUN_V2L2_SDA_DAILY_NAME]['START_YEAR'] =\
            cr['obsstartyears']['AERONET_SUN_V2L2_SDA_DAILY']
    
        OBSCONFIG[self.AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME]['PATH'] =\
            cr['obsfolders']['AERONET_SUN_V2L2_SDA_ALL_POINTS'].\
            replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_SUN_V2L2_SDA_ALL_POINTS']
    
        OBSCONFIG[self.AERONET_SUN_V3L15_AOD_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V3L15_AOD_DAILY_NAME]['PATH'] = cr['obsfolders']['AERONET_SUN_V3L15_AOD_DAILY'].replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.AERONET_SUN_V3L15_AOD_DAILY_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_SUN_V3L15_AOD_DAILY']
    
        OBSCONFIG[self.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME]['PATH'] = cr['obsfolders']['AERONET_SUN_V3L15_AOD_ALL_POINTS'].replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_SUN_V3L15_AOD_ALL_POINTS']
    
        OBSCONFIG[self.AERONET_SUN_V3L2_AOD_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V3L2_AOD_DAILY_NAME]['PATH'] = cr['obsfolders']['AERONET_SUN_V3L2_AOD_DAILY'].replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.AERONET_SUN_V3L2_AOD_DAILY_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_SUN_V3L2_AOD_DAILY']
    
        OBSCONFIG[self.AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME]['PATH'] = cr['obsfolders']['AERONET_SUN_V3L2_AOD_ALL_POINTS'].replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_SUN_V3L2_AOD_ALL_POINTS']
    
        OBSCONFIG[self.AERONET_SUN_V3L15_SDA_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V3L15_SDA_DAILY_NAME]['PATH'] = \
            cr['obsfolders']['AERONET_SUN_V3L15_SDA_DAILY'].replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.AERONET_SUN_V3L15_SDA_DAILY_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_SUN_V3L15_SDA_DAILY']
    
        OBSCONFIG[self.AERONET_SUN_V3L2_SDA_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V3L2_SDA_DAILY_NAME]['PATH'] = cr['obsfolders']['AERONET_SUN_V3L2_SDA_DAILY'].replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.AERONET_SUN_V3L2_SDA_DAILY_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_SUN_V3L2_SDA_DAILY']

        OBSCONFIG[self.AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME] = {}
        OBSCONFIG[self.AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME]['PATH'] = cr['obsfolders']['AERONET_SUN_V3L2_SDA_ALL_POINTS'].replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_SUN_V3L2_SDA_ALL_POINTS']
    
        OBSCONFIG[self.AERONET_INV_V2L15_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_INV_V2L15_DAILY_NAME]['PATH'] = cr['obsfolders']['AERONET_INV_V2L15_DAILY'].replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.AERONET_INV_V2L15_DAILY_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_INV_V2L15_DAILY']
    
        OBSCONFIG[self.AERONET_INV_V2L15_ALL_POINTS_NAME] = {}
        OBSCONFIG[self.AERONET_INV_V2L15_ALL_POINTS_NAME]['PATH'] = cr['obsfolders']['AERONET_INV_V2L15_ALL_POINTS'].replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.AERONET_INV_V2L15_ALL_POINTS_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_INV_V2L15_ALL_POINTS']
    
        OBSCONFIG[self.AERONET_INV_V2L2_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_INV_V2L2_DAILY_NAME]['PATH'] = cr['obsfolders']['AERONET_INV_V2L2_DAILY'].replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.AERONET_INV_V2L2_DAILY_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_INV_V2L2_DAILY']
    
        OBSCONFIG[self.AERONET_INV_V2L2_ALL_POINTS_NAME] = {}
        OBSCONFIG[self.AERONET_INV_V2L2_ALL_POINTS_NAME]['PATH'] = cr['obsfolders']['AERONET_INV_V2L2_ALL_POINTS'].replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.AERONET_INV_V2L2_ALL_POINTS_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_INV_V2L2_ALL_POINTS']
    
        # Aeronet v3 inversions
        OBSCONFIG[self.AERONET_INV_V3L15_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_INV_V3L15_DAILY_NAME]['PATH'] = cr['obsfolders']['AERONET_INV_V3L15_DAILY'].replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.AERONET_INV_V3L15_DAILY_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_INV_V2L15_DAILY']
        
        OBSCONFIG[self.AERONET_INV_V3L2_DAILY_NAME] = {}
        OBSCONFIG[self.AERONET_INV_V3L2_DAILY_NAME]['PATH'] = cr['obsfolders']['AERONET_INV_V3L2_DAILY'].replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.AERONET_INV_V3L2_DAILY_NAME]['START_YEAR'] = cr['obsstartyears']['AERONET_INV_V2L15_DAILY']
        
        OBSCONFIG[self.EBAS_MULTICOLUMN_NAME] = {}
        OBSCONFIG[self.EBAS_MULTICOLUMN_NAME]['PATH'] = cr['obsfolders']['EBAS_MULTICOLUMN'].replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.EBAS_MULTICOLUMN_NAME]['START_YEAR'] = cr['obsstartyears']['EBAS_MULTICOLUMN']
    
        OBSCONFIG[self.EEA_NAME] = {}
        OBSCONFIG[self.EEA_NAME]['PATH'] = cr['obsfolders']['EEA'].replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.EEA_NAME]['START_YEAR'] = cr['obsstartyears']['EEA']

        OBSCONFIG[self.EARLINET_NAME] = {}
        OBSCONFIG[self.EARLINET_NAME]['PATH'] = cr['obsfolders']['EARLINET'].replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.EARLINET_NAME]['START_YEAR'] = cr['obsstartyears']['EARLINET']
        
        cr.clear()
    
    def short_str(self):
        head = "Pyaerocom {}".format(type(self).__name__)
        s = "\n{}\n{}\n".format(head, len(head)*"-")
        for k, v in self.__dict__.items():
            if isinstance(v, dict):
                s += "\n%s (dict)" %k
            elif isinstance(v, list):
                s += "\n%s (list)" %k
                s += list_to_shortstr(v)
            else:
                s += "\n%s: %s" %(k, v)
        return s
    
    def __str__(self):
        head = "Pyaerocom {}".format(type(self).__name__)
        s = "\n{}\n{}\n".format(head, len(head)*"-")
        for k, v in self.__dict__.items():
            if isinstance(v, dict):
                s += "\n%s (dict)" %k
                s = dict_to_str(v, s)
            else:
                s += "\n%s: %s" %(k,v)
        return s

if __name__=="__main__":
    config = Config()
    
    print(config.short_str())
    io = GridIO()
    print(dict_to_str(io.to_dict()))
    
    io1 = GridIO()
    io1.from_dict(INCLUDE_SUBDIRS=True)
    print(io1)
    
    var_info = VarInfo()
    print(var_info)