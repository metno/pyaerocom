#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 15:27:28 2019

@author: jonasg
"""
import pytest
import os
from pyaerocom import conftest
from pyaerocom import const as DEFAULT_CFG
import getpass

USER = getpass.getuser()

import pyaerocom.config as testmod

@pytest.fixture(scope='module')
def empty_cfg():
    cfg = testmod.Config(try_infer_environment=False)
    return cfg

def test_empty_class_header(empty_cfg):
    cfg = empty_cfg
    assert cfg.AERONET_SUN_V2L15_AOD_DAILY_NAME == 'AeronetSunV2Lev1.5.daily'
    assert cfg.AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME == 'AeronetSun_2.0_NRT'
    assert cfg.AERONET_SUN_V2L2_AOD_DAILY_NAME == 'AeronetSunV2Lev2.daily'
    assert cfg.AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME == 'AeronetSunV2Lev2.AP'
    assert cfg.AERONET_SUN_V2L2_SDA_DAILY_NAME == 'AeronetSDAV2Lev2.daily'
    assert cfg.AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME == 'AeronetSDAV2Lev2.AP'
    assert cfg.AERONET_INV_V2L15_DAILY_NAME == 'AeronetInvV2Lev1.5.daily'
    assert cfg.AERONET_INV_V2L15_ALL_POINTS_NAME == 'AeronetInvV2Lev1.5.AP'
    assert cfg.AERONET_INV_V2L2_DAILY_NAME == 'AeronetInvV2Lev2.daily'
    assert cfg.AERONET_INV_V2L2_ALL_POINTS_NAME == 'AeronetInvV2Lev2.AP'
    assert cfg.AERONET_SUN_V3L15_AOD_DAILY_NAME == 'AeronetSunV3Lev1.5.daily'
    assert cfg.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME == 'AeronetSunV3Lev1.5.AP'
    assert cfg.AERONET_SUN_V3L2_AOD_DAILY_NAME == 'AeronetSunV3Lev2.daily'
    assert cfg.AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME == 'AeronetSunV3Lev2.AP'
    assert cfg.AERONET_SUN_V3L15_SDA_DAILY_NAME == 'AeronetSDAV3Lev1.5.daily'
    assert cfg.AERONET_SUN_V3L15_SDA_ALL_POINTS_NAME == 'AeronetSDAV3Lev1.5.AP'
    assert cfg.AERONET_SUN_V3L2_SDA_DAILY_NAME == 'AeronetSDAV3Lev2.daily'
    assert cfg.AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME == 'AeronetSDAV3Lev2.AP'
    assert cfg.AERONET_INV_V3L15_DAILY_NAME == 'AeronetInvV3Lev1.5.daily'
    assert cfg.AERONET_INV_V3L2_DAILY_NAME == 'AeronetInvV3Lev2.daily'
    assert cfg.EBAS_MULTICOLUMN_NAME == 'EBASMC'
    assert cfg.EEA_NAME == 'EEAAQeRep'
    assert cfg.EARLINET_NAME == 'EARLINET'
    assert cfg.GAWTADSUBSETAASETAL_NAME == 'GAWTADsubsetAasEtAl'
    assert cfg.DMS_AMS_CVO_NAME == 'DMS_AMS_CVO'
    assert cfg.EBAS_DB_LOCAL_CACHE
    assert cfg.MIN_YEAR == 0
    assert cfg.MAX_YEAR == 20000
    assert cfg.STANDARD_COORD_NAMES == ['latitude',
                                        'longitude',
                                        'altitude']
    assert cfg.DEFAULT_VERT_GRID_DEF == dict(
        lower = 0,
        upper = 15000,
        step  = 250)
    assert cfg.RH_MAX_PERCENT_DRY == 40
    assert cfg.DEFAULT_REG_FILTER == 'WORLD-noMOUNTAINS'
    assert cfg.OBS_APPLY_TIME_RESAMPLE_CONSTRAINTS
    assert cfg.OBS_MIN_NUM_RESAMPLE == dict(
        yearly      =   dict(monthly    = 3),
        monthly     =   dict(daily      = 7),
        daily       =   dict(hourly     = 6),
        hourly      =   dict(minutely   = 15))
    from pyaerocom import obs_io
    assert cfg.OBS_ALLOW_ALT_WAVELENGTHS == obs_io.OBS_ALLOW_ALT_WAVELENGTHS

    assert cfg.OBS_WAVELENGTH_TOL_NM == obs_io.OBS_WAVELENGTH_TOL_NM

    assert cfg.CLIM_START ==2005
    assert cfg.CLIM_STOP == 2015
    assert cfg.CLIM_FREQ == 'daily'
    assert cfg.CLIM_RESAMPLE_HOW == 'mean'
    assert cfg.CLIM_MIN_COUNT == dict(daily = 30,
                                     monthly = 5)

    #names of the different obs networks
    assert cfg.OBSNET_NONE == 'NONE'
    assert cfg.NOMODELNAME == 'OBSERVATIONS-ONLY'

    # names for the satellite data sets
    assert cfg.SENTINEL5P_NAME == 'Sentinel5P'
    assert cfg.AEOLUS_NAME == 'AeolusL2A'

    assert cfg.OLD_AEROCOM_REGIONS == ['WORLD', 'ASIA', 'AUSTRALIA', 'CHINA',
                           'EUROPE', 'INDIA', 'NAFRICA', 'SAFRICA', 'SAMERICA',
                           'NAMERICA']

    assert cfg.URL_HTAP_MASKS == 'https://pyaerocom.met.no/pyaerocom-suppl/htap_masks/'

    assert cfg.HTAP_REGIONS == ['PAN', 'EAS', 'NAF', 'MDE', 'LAND',
                    'SAS', 'SPO', 'OCN',  'SEA', 'RBU',
                    'EEUROPE', 'NAM', 'WEUROPE', 'SAF',
                    'USA', 'SAM', 'EUR', 'NPO', 'MCA']

    assert cfg.RM_CACHE_OUTDATED

    #: Name of the file containing the revision string of an obs data network
    assert cfg.REVISION_FILE == 'Revision.txt'

    #: timeout to check if one of the supported server locations can be
    #: accessed
    assert cfg.SERVER_CHECK_TIMEOUT == 1 #s

    assert cfg._outhomename == 'MyPyaerocom'
    from pyaerocom import __dir__
    config_files = {
        'lustre'        : os.path.join(__dir__, 'data', 'paths.ini'),
        'user_server'   : os.path.join(__dir__, 'data', 'paths_user_server.ini'),
        'testdata'      : os.path.join(__dir__, 'data', 'paths_testdata.ini'),
        'local-db'      : os.path.join(__dir__, 'data', 'paths_local_database.ini')
        }

    assert cfg._config_ini_lustre == config_files['lustre']
    assert cfg._config_ini_user_server == config_files['user_server']
    assert cfg._config_ini_testdata == config_files['testdata']
    assert cfg._config_ini_localdb == config_files['local-db']

    assert cfg._config_files == {
            'metno'            : config_files['lustre'],
            'users-db'         : config_files['user_server'],
            'testdata'         : config_files['testdata'],
            'local-db'         : config_files['local-db']
    }
    assert cfg._check_subdirs_cfg == {
            'metno'       : 'aerocom',
            'users-db'    : 'AMAP',
            'testdata'    : 'modeldata',
            'local-db'    : 'modeldata'
    }

    assert cfg._var_info_file == os.path.join(__dir__, 'data', 'variables.ini')
    assert cfg._coords_info_file == os.path.join(__dir__, 'data', 'coords.ini')
    dbdirs = {'lustre/storeA/project': 'metno',
              'metno/aerocom_users_database': 'users-db',
              'pyaerocom-testdata/': 'testdata',
              'MyPyaerocom/pyaerocom-testdata': 'testdata',
              'MyPyaerocom/data': 'local-db'}
    for sd, name in dbdirs.items():
        assert sd in cfg._DB_SEARCH_SUBDIRS
        assert cfg._DB_SEARCH_SUBDIRS[sd] == name

    assert cfg.DONOTCACHEFILE == None

    assert cfg.ERA5_SURFTEMP_FILENAME == 'era5.msl.t2m.201001-201012.nc'

    assert cfg._LUSTRE_CHECK_PATH == '/project/aerocom/aerocom1/'

def test_empty_init(empty_cfg):
    cfg = empty_cfg
    assert cfg._cache_basedir is None
    assert cfg._outputdir is None
    assert cfg._colocateddatadir is None
    assert cfg._filtermaskdir is None
    assert cfg._local_tmp_dir is None
    assert cfg._downloaddatadir is None
    assert cfg._confirmed_access == []
    assert cfg._rejected_access == []

    # Options
    assert cfg._caching_active is True

    assert cfg._var_param is None
    assert cfg._coords is None

    # Attributes that are used to store search directories
    assert cfg.OBSLOCS_UNGRIDDED == {}
    assert cfg.OBS_UNGRIDDED_POST == {}
    assert cfg.SUPPLDIRS == {}
    assert cfg._search_dirs == []

    assert cfg.WRITE_FILEIO_ERR_LOG is True

    assert cfg.last_config_file is None
    assert cfg._ebas_flag_info is None
    from pyaerocom.grid_io import GridIO
    #: Settings for reading and writing of gridded data
    assert isinstance(cfg.GRID_IO, GridIO)

def test_default_config_HOMEDIR():
    assert DEFAULT_CFG.HOMEDIR == os.path.expanduser("~") + '/'

def test_default_config():
    cfg = DEFAULT_CFG
    home = os.path.abspath(cfg.HOMEDIR)

    mkpath = lambda basepath, relpath : os.path.abspath(os.path.join(basepath,
                                                                     relpath))

    mypydir = mkpath(home, 'MyPyaerocom')
    assert cfg._outputdir == mypydir
    assert cfg.OUTPUTDIR == mypydir

    assert cfg._cache_basedir == mkpath(mypydir, '_cache')
    assert cfg.CACHEDIR == mkpath(mypydir, f'_cache/{USER}')

    check = mkpath(mypydir, 'colocated_data')
    assert cfg.COLOCATEDDATADIR == check
    # now this should be assigned
    assert cfg._colocateddatadir == check

    check = mkpath(mypydir, 'filtermasks')
    assert cfg.FILTERMASKKDIR == check
    # now this should be assigned
    assert cfg._filtermaskdir == check

    check = mkpath(mypydir, 'tmp')
    assert cfg.LOCAL_TMP_DIR == check
    # now this should be assigned
    assert cfg._local_tmp_dir == check

    check = mkpath(mypydir, 'data')
    assert cfg.DOWNLOAD_DATADIR == check
    # now this should be assigned
    assert cfg._downloaddatadir == check

    from pyaerocom.testdata_access import TestDataAccess
    testdatadirname = TestDataAccess.TESTDATADIRNAME
    checkdir = testdatadirname + '/obsdata'
    assert mkpath(mypydir, checkdir) in cfg._confirmed_access

    assert cfg._caching_active
    assert cfg.CACHING

    from pyaerocom.variable import VarCollection
    assert isinstance(cfg._var_param, VarCollection)
    assert isinstance(cfg.VARS, VarCollection)
    assert cfg.VARS is cfg.VAR_PARAM

    assert isinstance(cfg.COORDINFO, VarCollection)
    assert cfg._coords is cfg.COORDINFO

    # Attributes that are used to store search directories
    for obs_id in TestDataAccess._UNGRIDDED_READERS:
        assert obs_id in cfg.OBSLOCS_UNGRIDDED
    assert cfg.OBS_UNGRIDDED_POST == {}
    if not cfg.has_access_lustre:
        assert cfg.SUPPLDIRS == {}

    search_dirs = [f'{mypydir}/{testdatadirname}/modeldata',
                   f'{mypydir}/{testdatadirname}/obsdata',
                   f'{mypydir}/{testdatadirname}/config']

    for sd in search_dirs:
        assert os.path.abspath(sd) in cfg._search_dirs

    assert cfg.DATA_SEARCH_DIRS is cfg._search_dirs

    assert cfg.WRITE_FILEIO_ERR_LOG

    from pyaerocom.grid_io import GridIO
    assert isinstance(cfg.GRID_IO, GridIO)

### NEED TO TEST MORE CLASS METHODS...
if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
