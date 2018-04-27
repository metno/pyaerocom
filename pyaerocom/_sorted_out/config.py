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
Provides access to aerocom_pt specific configuration values
"""


import numpy as np
import os
from pyaerocom import __dir__
try:
    from ConfigParser import ConfigParser
except: 
    from configparser import ConfigParser

###############################################################
# stat config start
#GCOS requirements
GCOSPERCENTCRIT =   np.float(0.1)
GCOSABSCRIT     =   np.float(0.04)
# stat config end
###############################################################

###############################################################
# read config start
#obs reading information

#names of the different obs networks
OBSNET_NONE = 'NONE'
NOMODELNAME = 'OBSERVATIONS-ONLY'

# Name of the test file containing the revision string of the obs data
# in the 1st file
REVISION_FILE = 'Revision.txt'

#default names of the different obs networks
#might get overwritten from paths.ini
#Aeronet V2
AERONET_SUN_V2L15_AOD_DAILY_NAME = 'AeronetSunV2Lev1.5.daily'
AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME = 'AeronetSun_2.0_NRT'
AERONET_SUN_V2L2_AOD_DAILY_NAME = 'AeronetSunV2Lev2.daily'
AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME = 'AeronetSunV2Lev2.AP'
AERONET_SUN_V2L2_SDA_DAILY_NAME = 'AeronetSDAV2Lev2.daily'
AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME = 'AeronetSDAV2Lev2.AP'
#Aeronet V3
AERONET_SUN_V3L15_AOD_DAILY_NAME = 'AeronetSunV3Lev1.5.daily'
AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME = 'AeronetSunV3Lev1.5.AP'
AERONET_SUN_V3L2_AOD_DAILY_NAME = 'AeronetSunV3Lev2.daily'
AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME = 'AeronetSunV3Lev2.AP'
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

OBSDATACACHEDIR = '/lustre/storeA/users/jang/cache/'
DONOTCACHEFILE = os.path.join(OBSDATACACHEDIR, 'DONOTCACHE')

#read paths.ini
#IniFileName = os.path.realpath(__file__)),'paths.ini'
_config_ini = os.path.join(__dir__, 'data', 'paths.ini')
if not os.path.exists(_config_ini):
    raise IOError("Configuration file paths.ini could not be found at %s"
                  %_config_ini)
conf_reader = ConfigParser()
if os.path.isfile(_config_ini):
    conf_reader.read(_config_ini)
    #Model
    #model data paths
    MODELBASEDIR = conf_reader['modelfolders']['BASEDIR']
    MODELDIRS = conf_reader['modelfolders']['dir'].\
        replace('${BASEDIR}',MODELBASEDIR).replace('\n','').split(',')

    # read obs network names from ini file
    # Aeronet V2
    AERONET_SUN_V2L15_AOD_DAILY_NAME = \
        conf_reader['obsnames']['AERONET_SUN_V2L15_AOD_DAILY']
    AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME = \
        conf_reader['obsnames']['AERONET_SUN_V2L15_AOD_ALL_POINTS']
    AERONET_SUN_V2L2_AOD_DAILY_NAME =\
        conf_reader['obsnames']['AERONET_SUN_V2L2_AOD_DAILY']
    AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME =\
        conf_reader['obsnames']['AERONET_SUN_V2L2_AOD_ALL_POINTS']
    AERONET_SUN_V2L2_SDA_DAILY_NAME =\
        conf_reader['obsnames']['AERONET_SUN_V2L2_SDA_DAILY']
    AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME =\
        conf_reader['obsnames']['AERONET_SUN_V2L2_SDA_ALL_POINTS']
        
    # Aeronet V3
    AERONET_SUN_V3L15_AOD_DAILY_NAME =\
        conf_reader['obsnames']['AERONET_SUN_V3L15_AOD_DAILY']
    AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME =\
        conf_reader['obsnames']['AERONET_SUN_V3L15_AOD_ALL_POINTS']
    AERONET_SUN_V3L2_AOD_DAILY_NAME =\
        conf_reader['obsnames']['AERONET_SUN_V3L2_AOD_DAILY']
    AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME =\
        conf_reader['obsnames']['AERONET_SUN_V3L2_AOD_ALL_POINTS']
    AERONET_SUN_V3L2_SDA_DAILY_NAME =\
        conf_reader['obsnames']['AERONET_SUN_V3L2_SDA_DAILY']
    AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME =\
     conf_reader['obsnames']['AERONET_SUN_V3L2_SDA_ALL_POINTS']
    
    # inversions
    AERONET_INV_V2L15_DAILY_NAME =\
        conf_reader['obsnames']['AERONET_INV_V2L15_DAILY']
    AERONET_INV_V2L15_ALL_POINTS_NAME =\
        conf_reader['obsnames']['AERONET_INV_V2L15_ALL_POINTS']
    AERONET_INV_V2L2_DAILY_NAME =\
        conf_reader['obsnames']['AERONET_INV_V2L2_DAILY']
    AERONET_INV_V2L2_ALL_POINTS_NAME = \
        conf_reader['obsnames']['AERONET_INV_V2L2_ALL_POINTS']
    #
    EBAS_MULTICOLUMN_NAME = conf_reader['obsnames']['EBAS_MULTICOLUMN']
    EEA_NAME = conf_reader['obsnames']['EEA']


    #observations
    #Folders
    OBSBASEDIR = conf_reader['obsfolders']['BASEDIR']
    OBSCONFIG = {}
    OBSCONFIG[AERONET_SUN_V2L15_AOD_DAILY_NAME] = {}
    OBSCONFIG[AERONET_SUN_V2L15_AOD_DAILY_NAME]['PATH'] =\
        conf_reader['obsfolders']['AERONET_SUN_V2L15_AOD_DAILY'].\
        replace('${BASEDIR}',OBSBASEDIR)
    OBSCONFIG[AERONET_SUN_V2L15_AOD_DAILY_NAME]['START_YEAR'] =\
        conf_reader['obsstartyears']['AERONET_SUN_V2L15_AOD_DAILY']

    OBSCONFIG[AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME] = {}
    OBSCONFIG[AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME]['PATH'] =\
        conf_reader['obsfolders']['AERONET_SUN_V2L15_AOD_ALL_POINTS'].\
        replace('${BASEDIR}',OBSBASEDIR)
    OBSCONFIG[AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME]['START_YEAR'] =\
        conf_reader['obsstartyears']['AERONET_SUN_V2L15_AOD_ALL_POINTS']

    OBSCONFIG[AERONET_SUN_V2L2_AOD_DAILY_NAME] = {}
    OBSCONFIG[AERONET_SUN_V2L2_AOD_DAILY_NAME]['PATH'] =\
        conf_reader['obsfolders']['AERONET_SUN_V2L2_AOD_DAILY'].\
        replace('${BASEDIR}',OBSBASEDIR)
    OBSCONFIG[AERONET_SUN_V2L2_AOD_DAILY_NAME]['START_YEAR'] =\
        conf_reader['obsstartyears']['AERONET_SUN_V2L2_AOD_DAILY']

    OBSCONFIG[AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME] = {}
    OBSCONFIG[AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME]['PATH'] =\
        conf_reader['obsfolders']['AERONET_SUN_V2L2_AOD_ALL_POINTS'].\
        replace('${BASEDIR}',OBSBASEDIR)
    OBSCONFIG[AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME]['START_YEAR'] =\
        conf_reader['obsstartyears']['AERONET_SUN_V2L2_AOD_ALL_POINTS']

    OBSCONFIG[AERONET_SUN_V2L2_SDA_DAILY_NAME] = {}
    OBSCONFIG[AERONET_SUN_V2L2_SDA_DAILY_NAME]['PATH'] =\
        conf_reader['obsfolders']['AERONET_SUN_V2L2_SDA_DAILY'].\
        replace('${BASEDIR}',OBSBASEDIR)
    OBSCONFIG[AERONET_SUN_V2L2_SDA_DAILY_NAME]['START_YEAR'] =\
        conf_reader['obsstartyears']['AERONET_SUN_V2L2_SDA_DAILY']

    OBSCONFIG[AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME] = {}
    OBSCONFIG[AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME]['PATH'] =\
        conf_reader['obsfolders']['AERONET_SUN_V2L2_SDA_ALL_POINTS'].\
        replace('${BASEDIR}',OBSBASEDIR)
    OBSCONFIG[AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_SUN_V2L2_SDA_ALL_POINTS']

    OBSCONFIG[AERONET_SUN_V3L15_AOD_DAILY_NAME] = {}
    OBSCONFIG[AERONET_SUN_V3L15_AOD_DAILY_NAME]['PATH'] = conf_reader['obsfolders']['AERONET_SUN_V3L15_AOD_DAILY'].replace('${BASEDIR}',OBSBASEDIR)
    OBSCONFIG[AERONET_SUN_V3L15_AOD_DAILY_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_SUN_V3L15_AOD_DAILY']

    OBSCONFIG[AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME] = {}
    OBSCONFIG[AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME]['PATH'] = conf_reader['obsfolders']['AERONET_SUN_V3L15_AOD_ALL_POINTS'].replace('${BASEDIR}',OBSBASEDIR)
    OBSCONFIG[AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_SUN_V3L15_AOD_ALL_POINTS']

    OBSCONFIG[AERONET_SUN_V3L2_AOD_DAILY_NAME] = {}
    OBSCONFIG[AERONET_SUN_V3L2_AOD_DAILY_NAME]['PATH'] = conf_reader['obsfolders']['AERONET_SUN_V3L2_AOD_DAILY'].replace('${BASEDIR}',OBSBASEDIR)
    OBSCONFIG[AERONET_SUN_V3L2_AOD_DAILY_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_SUN_V3L2_AOD_DAILY']

    OBSCONFIG[AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME] = {}
    OBSCONFIG[AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME]['PATH'] = conf_reader['obsfolders']['AERONET_SUN_V3L2_AOD_ALL_POINTS'].replace('${BASEDIR}',OBSBASEDIR)
    OBSCONFIG[AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_SUN_V3L2_AOD_ALL_POINTS']

    OBSCONFIG[AERONET_SUN_V3L2_SDA_DAILY_NAME] = {}
    OBSCONFIG[AERONET_SUN_V3L2_SDA_DAILY_NAME]['PATH'] = conf_reader['obsfolders']['AERONET_SUN_V3L2_SDA_DAILY'].replace('${BASEDIR}',OBSBASEDIR)
    OBSCONFIG[AERONET_SUN_V3L2_SDA_DAILY_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_SUN_V3L2_SDA_DAILY']

    OBSCONFIG[AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME] = {}
    OBSCONFIG[AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME]['PATH'] = conf_reader['obsfolders']['AERONET_SUN_V3L2_SDA_ALL_POINTS'].replace('${BASEDIR}',OBSBASEDIR)
    OBSCONFIG[AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_SUN_V3L2_SDA_ALL_POINTS']

    OBSCONFIG[AERONET_INV_V2L15_DAILY_NAME] = {}
    OBSCONFIG[AERONET_INV_V2L15_DAILY_NAME]['PATH'] = conf_reader['obsfolders']['AERONET_INV_V2L15_DAILY'].replace('${BASEDIR}',OBSBASEDIR)
    OBSCONFIG[AERONET_INV_V2L15_DAILY_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_INV_V2L15_DAILY']

    OBSCONFIG[AERONET_INV_V2L15_ALL_POINTS_NAME] = {}
    OBSCONFIG[AERONET_INV_V2L15_ALL_POINTS_NAME]['PATH'] = conf_reader['obsfolders']['AERONET_INV_V2L15_ALL_POINTS'].replace('${BASEDIR}',OBSBASEDIR)
    OBSCONFIG[AERONET_INV_V2L15_ALL_POINTS_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_INV_V2L15_ALL_POINTS']

    OBSCONFIG[AERONET_INV_V2L2_DAILY_NAME] = {}
    OBSCONFIG[AERONET_INV_V2L2_DAILY_NAME]['PATH'] = conf_reader['obsfolders']['AERONET_INV_V2L2_DAILY'].replace('${BASEDIR}',OBSBASEDIR)
    OBSCONFIG[AERONET_INV_V2L2_DAILY_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_INV_V2L2_DAILY']

    OBSCONFIG[AERONET_INV_V2L2_ALL_POINTS_NAME] = {}
    OBSCONFIG[AERONET_INV_V2L2_ALL_POINTS_NAME]['PATH'] = conf_reader['obsfolders']['AERONET_INV_V2L2_ALL_POINTS'].replace('${BASEDIR}',OBSBASEDIR)
    OBSCONFIG[AERONET_INV_V2L2_ALL_POINTS_NAME]['START_YEAR'] = conf_reader['obsstartyears']['AERONET_INV_V2L2_ALL_POINTS']

    OBSCONFIG[EBAS_MULTICOLUMN_NAME] = {}
    OBSCONFIG[EBAS_MULTICOLUMN_NAME]['PATH'] = conf_reader['obsfolders']['EBAS_MULTICOLUMN'].replace('${BASEDIR}',OBSBASEDIR)
    OBSCONFIG[EBAS_MULTICOLUMN_NAME]['START_YEAR'] = conf_reader['obsstartyears']['EBAS_MULTICOLUMN']

    OBSCONFIG[EEA_NAME] = {}
    OBSCONFIG[EEA_NAME]['PATH'] = conf_reader['obsfolders']['EEA'].replace('${BASEDIR}',OBSBASEDIR)
    OBSCONFIG[EEA_NAME]['START_YEAR'] = conf_reader['obsstartyears']['EEA']

conf_reader.clear()

del conf_reader, _config_ini
