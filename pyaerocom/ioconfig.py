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
try:
    from ConfigParser import ConfigParser
except: 
    from configparser import ConfigParser

class IOConfig(object):
    """Class containing relevant paths for read and write routines"""
    
    def __init__(self, model_base_dir=None, obs_base_dir=None, 
                 config_file=None, 
                 obs_cache_dir='/lustre/storeA/users/jang/cache/'):
        
        self.GCOSPERCENTCRIT =   np.float(0.1)
        self.GCOSABSCRIT     =   np.float(0.04)
        
        #names of the different obs networks
        self.OBSNET_NONE = 'NONE'
        self.NOMODELNAME = 'OBSERVATIONS-ONLY'

        # if this file exists no cache file is read
        # used to ease debugging
        self.DONOTCACHEFILE = os.path.join(obs_cache_dir, 'DONOTCACHE')

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
        
        # Attributes that are used to store import results
        self.OBSCONFIG = {}
        self.MODELDIRS = []
        
        # Directories
        self.MODELBASEDIR = None
        self.OBSBASEDIR = None
        self.OBSDATACACHEDIR = None
        
        if isinstance(config_file, str) and os.path.exists(config_file):
            self._config_ini = config_file
        else:
            from pyaerocom import __dir__
            self._config_ini = os.path.join(__dir__, 'data', 'paths.ini')
        
        if self.check_dir(model_base_dir):
            self.MODELBASEDIR = model_base_dir
        if self.check_dir(obs_base_dir):
            self.OBSBASEDIR = obs_base_dir
        if self.check_dir(obs_cache_dir):
            self.OBSDATACACHEDIR = obs_cache_dir
        self.read_config(config_file)
        try:
            self.read_config(config_file)
        except Exception as e:
            print("Failed to read config file. Error: %s" %repr(e))
        self.READY
        
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
    
    def check_dir(self, path):
        """Checks if directory exists"""
        if isinstance(path, str) and os.path.isdir(path):
            return True
        return False
    
    def reload(self):
        self.read_config(self._config_ini)
        
    def read_config(self, config_file):
        """Read and import form paths.ini"""
        _config_ini = self._config_ini
        if not os.path.isfile(_config_ini):
            raise IOError("Configuration file paths.ini at %s does not exist "
                          "or is not a file"
                          %_config_ini)
        cr = ConfigParser()
        cr.read(_config_ini)
        #init base directories for Model data
        if not self.check_dir(self.MODELBASEDIR):
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
            
        # Aeronet V3
        self.AERONET_SUN_V3L15_AOD_DAILY_NAME = cr['obsnames']['AERONET_SUN_V3L15_AOD_DAILY']
        self.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME = cr['obsnames']['AERONET_SUN_V3L15_AOD_ALL_POINTS']
        self.AERONET_SUN_V3L2_AOD_DAILY_NAME = cr['obsnames']['AERONET_SUN_V3L2_AOD_DAILY']
        self.AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME = cr['obsnames']['AERONET_SUN_V3L2_AOD_ALL_POINTS']
        self.AERONET_SUN_V3L2_SDA_DAILY_NAME = cr['obsnames']['AERONET_SUN_V3L2_SDA_DAILY']
        self.AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME = cr['obsnames']['AERONET_SUN_V3L2_SDA_ALL_POINTS']
        
        # inversions
        self.AERONET_INV_V2L15_DAILY_NAME = cr['obsnames']['AERONET_INV_V2L15_DAILY']
        self.AERONET_INV_V2L15_ALL_POINTS_NAME = cr['obsnames']['AERONET_INV_V2L15_ALL_POINTS']
        self.AERONET_INV_V2L2_DAILY_NAME = cr['obsnames']['AERONET_INV_V2L2_DAILY']
        self.AERONET_INV_V2L2_ALL_POINTS_NAME = cr['obsnames']['AERONET_INV_V2L2_ALL_POINTS']
        
        self.EBAS_MULTICOLUMN_NAME = cr['obsnames']['EBAS_MULTICOLUMN']
        self.EEA_NAME = cr['obsnames']['EEA']
    
    
        #Read directories for observation location
        if not self.check_dir(self.OBSBASEDIR):
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
    
        OBSCONFIG[self.EBAS_MULTICOLUMN_NAME] = {}
        OBSCONFIG[self.EBAS_MULTICOLUMN_NAME]['PATH'] = cr['obsfolders']['EBAS_MULTICOLUMN'].replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.EBAS_MULTICOLUMN_NAME]['START_YEAR'] = cr['obsstartyears']['EBAS_MULTICOLUMN']
    
        OBSCONFIG[self.EEA_NAME] = {}
        OBSCONFIG[self.EEA_NAME]['PATH'] = cr['obsfolders']['EEA'].replace('${BASEDIR}',self.OBSBASEDIR)
        OBSCONFIG[self.EEA_NAME]['START_YEAR'] = cr['obsstartyears']['EEA']
    
        cr.clear()
    
    def short_str(self):
        s = 'Pyaerocom IOConfig'
        for k, v in self.__dict__.items():
            if isinstance(v, dict):
                s += "\n%s (dict)" %k
            elif isinstance(v, list):
                s += "\n%s (list)" %k
                s += list_to_shortstr(v)
            else:
                s += "\n%s: %s" %(k,v)
        return s
    
    def __str__(self):
        s = 'Pyaerocom IOConfig'
        for k, v in self.__dict__.items():
            if isinstance(v, dict):
                s += "\n%s (dict)" %k
                s = dict_to_str(v, s)
            else:
                s += "\n%s: %s" %(k,v)
        return s

def list_to_shortstr(lst, indent=3):
    """Custom function to convert a list into a short string representation"""
    s = "\n" + indent*" " + "[%s\n" %lst[0]
    if len(lst) > 4:
        s += (indent+1)*" " + "%s\n" %lst[1]
        s += (indent+1)*" " + "...\n"
        s += (indent+1)*" " + "%s\n" %lst[-2]
    else: 
        for item in lst[1:-1]:
            s += (indent+1)*" " + "%s" %item
    s += (indent+1)*" " + "%s]\n" %lst[-1]
    return s
        
def dict_to_str(dictionary, s="", indent=3):
    """Custom function to convert dictionary into string (e.g. for print)
    
    Parameters
    ----------
    dictionary : dict
        the dictionary
    s : str
        the input string
    indent : int
        indent of dictionary content
    
    Returns
    -------
    str
        the modified input string
        
    Example
    -------
    
    >>> string = "Printing dictionary d"
    >>> d = dict(Bla=1, Blub=dict(BlaBlub=2))
    >>> print(dict_to_str(d, string))
    Printing dictionary d
       Bla: 1
       Blub (dict)
        BlaBlub: 2
    
    """
    for k, v in dictionary.items():
        if isinstance(v, dict):
            s += "\n" + indent*" " + "%s (dict)" %k
            s = dict_to_str(v, s, indent+1)
        else:
            s += "\n" + indent*" " + "%s: %s" %(k,v)
    return s

if __name__=="__main__":
    import doctest
    doctest.testmod()
        
# =============================================================================
#         
# ###############################################################
# # stat config start
# #GCOS requirements
# GCOSPERCENTCRIT =   np.float(0.1)
# GCOSABSCRIT     =   np.float(0.04)
# # stat config end
# ###############################################################
# 
# ###############################################################
# # read config start
# #obs reading information
# 
# #names of the different obs networks
# OBSNET_NONE = 'NONE'
# NOMODELNAME = 'OBSERVATIONS-ONLY'
# 
# #default names of the different obs networks
# #might get overwritten from paths.ini
# #Aeronet V2
# AERONET_SUN_V2L15_AOD_DAILY_NAME = 'AeronetSunV2Lev1.5.daily'
# AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME = 'AeronetSun_2.0_NRT'
# AERONET_SUN_V2L2_AOD_DAILY_NAME = 'AeronetSunV2Lev2.daily'
# AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME = 'AeronetSunV2Lev2.AP'
# AERONET_SUN_V2L2_SDA_DAILY_NAME = 'AeronetSDAV2Lev2.daily'
# AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME = 'AeronetSDAV2Lev2.AP'
# 
# #Aeronet V3
# AERONET_SUN_V3L15_AOD_DAILY_NAME = 'AeronetSunV3Lev1.5.daily'
# AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME = 'AeronetSunV3Lev1.5.AP'
# AERONET_SUN_V3L2_AOD_DAILY_NAME = 'AeronetSunV3Lev2.daily'
# AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME = 'AeronetSunV3Lev2.AP'
# AERONET_SUN_V3L2_SDA_DAILY_NAME = 'AeronetSDAV3Lev2.daily'
# AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME = 'AeronetSDAV3Lev2.AP'
# 
# # inversions
# AERONET_INV_V2L15_DAILY_NAME = 'AeronetInvV2Lev1.5.daily'
# AERONET_INV_V2L15_ALL_POINTS_NAME = 'AeronetInvV2Lev1.5.AP'
# AERONET_INV_V2L2_DAILY_NAME = 'AeronetInvV2Lev2.daily'
# AERONET_INV_V2L2_ALL_POINTS_NAME = 'AeronetInvV2Lev2.AP'
# #
# EBAS_MULTICOLUMN_NAME = 'EBASMC'
# EEA_NAME = 'EEAAQeRep'
# 
# OBSDATACACHEDIR = '/lustre/storeA/users/jang/cache/'
# 
# #read paths.ini
# #IniFileName = os.path.realpath(__file__)),'paths.ini'
# _config_ini = os.path.join(__dir__, 'data', 'paths.ini')
# if not os.path.exists(_config_ini):
#     raise IOError("Configuration file paths.ini could not be found at %s"
#                   %_config_ini)
# conf_reader = ConfigParser()
# 
# if os.path.isfile(_config_ini):
#     conf_reader.read(_config_ini)
#     #Model
#     #model data paths
#     MODELBASEDIR = conf_reader['modelfolders']['BASEDIR']
#     MODELDIRS = conf_reader['modelfolders']['dir'].\
#         replace('${BASEDIR}',MODELBASEDIR).replace('\n','').split(',')
# 
#     # read obs network names from ini file
#     # Aeronet V2
#     AERONET_SUN_V2L15_AOD_DAILY_NAME = \
#         conf_reader['obsnames']['AERONET_SUN_V2L15_AOD_DAILY']
#     AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME = \
#         conf_reader['obsnames']['AERONET_SUN_V2L15_AOD_ALL_POINTS']
#     AERONET_SUN_V2L2_AOD_DAILY_NAME =\
#         conf_reader['obsnames']['AERONET_SUN_V2L2_AOD_DAILY']
#     AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME =\
#         conf_reader['obsnames']['AERONET_SUN_V2L2_AOD_ALL_POINTS']
#     AERONET_SUN_V2L2_SDA_DAILY_NAME =\
#         conf_reader['obsnames']['AERONET_SUN_V2L2_SDA_DAILY']
#     AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME =\
#         conf_reader['obsnames']['AERONET_SUN_V2L2_SDA_ALL_POINTS']
#         
#     # Aeronet V3
#     AERONET_SUN_V3L15_AOD_DAILY_NAME =\
#         conf_reader['obsnames']['AERONET_SUN_V3L15_AOD_DAILY']
#     AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME =\
#         conf_reader['obsnames']['AERONET_SUN_V3L15_AOD_ALL_POINTS']
#     AERONET_SUN_V3L2_AOD_DAILY_NAME =\
#         conf_reader['obsnames']['AERONET_SUN_V3L2_AOD_DAILY']
#     AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME =\
#         conf_reader['obsnames']['AERONET_SUN_V3L2_AOD_ALL_POINTS']
#     AERONET_SUN_V3L2_SDA_DAILY_NAME =\
#         conf_reader['obsnames']['AERONET_SUN_V3L2_SDA_DAILY']
#     AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME =\
#      conf_reader['obsnames']['AERONET_SUN_V3L2_SDA_ALL_POINTS']
#     
#     # inversions
#     AERONET_INV_V2L15_DAILY_NAME =\
#         conf_reader['obsnames']['AERONET_INV_V2L15_DAILY']
#     AERONET_INV_V2L15_ALL_POINTS_NAME =\
#         conf_reader['obsnames']['AERONET_INV_V2L15_ALL_POINTS']
#     AERONET_INV_V2L2_DAILY_NAME =\
#         conf_reader['obsnames']['AERONET_INV_V2L2_DAILY']
#     AERONET_INV_V2L2_ALL_POINTS_NAME = \
#         conf_reader['obsnames']['AERONET_INV_V2L2_ALL_POINTS']
#     #
#     EBAS_MULTICOLUMN_NAME = conf_reader['obsnames']['EBAS_MULTICOLUMN']
#     EEA_NAME = conf_reader['obsnames']['EEA']
# 
# 
#     #observations
#     #Folders
#     OBSBASEDIR = conf_reader['obsfolders']['BASEDIR']
#     OBSCONFIG = {}
#     OBSCONFIG[AERONET_SUN_V2L15_AOD_DAILY_NAME] = {}
#     OBSCONFIG[AERONET_SUN_V2L15_AOD_DAILY_NAME]['PATH'] =\
#         conf_reader['obsfolders']['AERONET_SUN_V2L15_AOD_DAILY'].\
#         replace('${BASEDIR}',OBSBASEDIR)
#     OBSCONFIG[AERONET_SUN_V2L15_AOD_DAILY_NAME]['START_YEAR'] =\
#         conf_reader['obsstartyears']['AERONET_SUN_V2L15_AOD_DAILY']
# 
#     OBSCONFIG[AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME] = {}
#     OBSCONFIG[AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME]['PATH'] =\
#         conf_reader['obsfolders']['AERONET_SUN_V2L15_AOD_ALL_POINTS'].\
#         replace('${BASEDIR}',OBSBASEDIR)
#     OBSCONFIG[AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME]['START_YEAR'] =\
#         conf_reader['obsstartyears']['AERONET_SUN_V2L15_AOD_ALL_POINTS']
# 
#     OBSCONFIG[AERONET_SUN_V2L2_AOD_DAILY_NAME] = {}
#     OBSCONFIG[AERONET_SUN_V2L2_AOD_DAILY_NAME]['PATH'] =\
#         conf_reader['obsfolders']['AERONET_SUN_V2L2_AOD_DAILY'].\
#         replace('${BASEDIR}',OBSBASEDIR)
#     OBSCONFIG[AERONET_SUN_V2L2_AOD_DAILY_NAME]['START_YEAR'] =\
#         conf_reader['obsstartyears']['AERONET_SUN_V2L2_AOD_DAILY']
# 
#     OBSCONFIG[AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME] = {}
#     OBSCONFIG[AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME]['PATH'] =\
#         conf_reader['obsfolders']['AERONET_SUN_V2L2_AOD_ALL_POINTS'].\
#         replace('${BASEDIR}',OBSBASEDIR)
#     OBSCONFIG[AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME]['START_YEAR'] =\
#         conf_reader['obsstartyears']['AERONET_SUN_V2L2_AOD_ALL_POINTS']
# 
#     OBSCONFIG[AERONET_SUN_V2L2_SDA_DAILY_NAME] = {}
#     OBSCONFIG[AERONET_SUN_V2L2_SDA_DAILY_NAME]['PATH'] =\
#         conf_reader['obsfolders']['AERONET_SUN_V2L2_SDA_DAILY'].\
#         replace('${BASEDIR}',OBSBASEDIR)
#     OBSCONFIG[AERONET_SUN_V2L2_SDA_DAILY_NAME]['START_YEAR'] =\
#         conf_reader['obsstartyears']['AERONET_SUN_V2L2_SDA_DAILY']
# 
#     OBSCONFIG[AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME] = {}
#     OBSCONFIG[AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME]['PATH'] =\
#         conf_reader['obsfolders']['AERONET_SUN_V2L2_SDA_ALL_POINTS'].\
#         replace('${BASEDIR}',OBSBASEDIR)
#     OBSCONFIG[AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_SUN_V2L2_SDA_ALL_POINTS']
# 
#     OBSCONFIG[AERONET_SUN_V3L15_AOD_DAILY_NAME] = {}
#     OBSCONFIG[AERONET_SUN_V3L15_AOD_DAILY_NAME]['PATH'] = conf_reader['obsfolders']['AERONET_SUN_V3L15_AOD_DAILY'].replace('${BASEDIR}',OBSBASEDIR)
#     OBSCONFIG[AERONET_SUN_V3L15_AOD_DAILY_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_SUN_V3L15_AOD_DAILY']
# 
#     OBSCONFIG[AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME] = {}
#     OBSCONFIG[AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME]['PATH'] = conf_reader['obsfolders']['AERONET_SUN_V3L15_AOD_ALL_POINTS'].replace('${BASEDIR}',OBSBASEDIR)
#     OBSCONFIG[AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_SUN_V3L15_AOD_ALL_POINTS']
# 
#     OBSCONFIG[AERONET_SUN_V3L2_AOD_DAILY_NAME] = {}
#     OBSCONFIG[AERONET_SUN_V3L2_AOD_DAILY_NAME]['PATH'] = conf_reader['obsfolders']['AERONET_SUN_V3L2_AOD_DAILY'].replace('${BASEDIR}',OBSBASEDIR)
#     OBSCONFIG[AERONET_SUN_V3L2_AOD_DAILY_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_SUN_V3L2_AOD_DAILY']
# 
#     OBSCONFIG[AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME] = {}
#     OBSCONFIG[AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME]['PATH'] = conf_reader['obsfolders']['AERONET_SUN_V3L2_AOD_ALL_POINTS'].replace('${BASEDIR}',OBSBASEDIR)
#     OBSCONFIG[AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_SUN_V3L2_AOD_ALL_POINTS']
# 
#     OBSCONFIG[AERONET_SUN_V3L2_SDA_DAILY_NAME] = {}
#     OBSCONFIG[AERONET_SUN_V3L2_SDA_DAILY_NAME]['PATH'] = conf_reader['obsfolders']['AERONET_SUN_V3L2_SDA_DAILY'].replace('${BASEDIR}',OBSBASEDIR)
#     OBSCONFIG[AERONET_SUN_V3L2_SDA_DAILY_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_SUN_V3L2_SDA_DAILY']
# 
#     OBSCONFIG[AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME] = {}
#     OBSCONFIG[AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME]['PATH'] = conf_reader['obsfolders']['AERONET_SUN_V3L2_SDA_ALL_POINTS'].replace('${BASEDIR}',OBSBASEDIR)
#     OBSCONFIG[AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_SUN_V3L2_SDA_ALL_POINTS']
# 
#     OBSCONFIG[AERONET_INV_V2L15_DAILY_NAME] = {}
#     OBSCONFIG[AERONET_INV_V2L15_DAILY_NAME]['PATH'] = conf_reader['obsfolders']['AERONET_INV_V2L15_DAILY'].replace('${BASEDIR}',OBSBASEDIR)
#     OBSCONFIG[AERONET_INV_V2L15_DAILY_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_INV_V2L15_DAILY']
# 
#     OBSCONFIG[AERONET_INV_V2L15_ALL_POINTS_NAME] = {}
#     OBSCONFIG[AERONET_INV_V2L15_ALL_POINTS_NAME]['PATH'] = conf_reader['obsfolders']['AERONET_INV_V2L15_ALL_POINTS'].replace('${BASEDIR}',OBSBASEDIR)
#     OBSCONFIG[AERONET_INV_V2L15_ALL_POINTS_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_INV_V2L15_ALL_POINTS']
# 
#     OBSCONFIG[AERONET_INV_V2L2_DAILY_NAME] = {}
#     OBSCONFIG[AERONET_INV_V2L2_DAILY_NAME]['PATH'] = conf_reader['obsfolders']['AERONET_INV_V2L2_DAILY'].replace('${BASEDIR}',OBSBASEDIR)
#     OBSCONFIG[AERONET_INV_V2L2_DAILY_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_INV_V2L2_DAILY']
# 
#     OBSCONFIG[AERONET_INV_V2L2_ALL_POINTS_NAME] = {}
#     OBSCONFIG[AERONET_INV_V2L2_ALL_POINTS_NAME]['PATH'] = conf_reader['obsfolders']['AERONET_INV_V2L2_ALL_POINTS'].replace('${BASEDIR}',OBSBASEDIR)
#     OBSCONFIG[AERONET_INV_V2L2_ALL_POINTS_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_INV_V2L2_ALL_POINTS']
# 
#     OBSCONFIG[EBAS_MULTICOLUMN_NAME] = {}
#     OBSCONFIG[EBAS_MULTICOLUMN_NAME]['PATH'] = conf_reader['obsfolders']['EBAS_MULTICOLUMN'].replace('${BASEDIR}',OBSBASEDIR)
#     OBSCONFIG[EBAS_MULTICOLUMN_NAME]['START_YEAR'] = conf_reader['obsstartyears']['EBAS_MULTICOLUMN']
# 
#     OBSCONFIG[EEA_NAME] = {}
#     OBSCONFIG[EEA_NAME]['PATH'] = conf_reader['obsfolders']['EEA'].replace('${BASEDIR}',OBSBASEDIR)
#     OBSCONFIG[EEA_NAME]['START_YEAR'] = conf_reader['obsstartyears']['EEA']
# 
# conf_reader.clear()
# 
# del conf_reader, _config_ini
# =============================================================================
