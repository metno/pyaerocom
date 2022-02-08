import getpass
import os
import tempfile
from importlib import resources
from pathlib import Path

import pytest

import pyaerocom.config as testmod
from pyaerocom import const
from pyaerocom.config import Config

from .conftest import lustre_avail

USER = getpass.getuser()

_TEMPDIR = tempfile.mkdtemp()
CFG_FILE_WRONG = os.path.join(_TEMPDIR, "paths.txt")

LOCAL_DB_DIR = os.path.join(_TEMPDIR, "data")
os.makedirs(os.path.join(LOCAL_DB_DIR, "modeldata"))
os.makedirs(os.path.join(LOCAL_DB_DIR, "obsdata"))
open(CFG_FILE_WRONG, "w").close()


def test_CFG_FILE_EXISTS():
    assert resources.is_resource("pyaerocom.data", "paths.ini")
    assert os.path.exists(CFG_FILE)


with resources.path("pyaerocom.data", "paths.ini") as path:
    CFG_FILE = str(path)


def test_CFG_FILE_EXISTS():
    assert os.path.exists(CFG_FILE)


def test_CFG_FILE_WRONG_EXISTS():
    assert os.path.exists(CFG_FILE_WRONG)


def test_LOCAL_DB_DIR_EXISTS():
    assert os.path.exists(LOCAL_DB_DIR)


@pytest.fixture(scope="module")
def empty_cfg():
    cfg = testmod.Config(try_infer_environment=False)
    return cfg


def test_Config_ALL_DATABASE_IDS(empty_cfg):
    assert empty_cfg.ALL_DATABASE_IDS == ["metno", "users-db", "local-db"]


@pytest.mark.parametrize(
    "config_file,try_infer_environment",
    [
        (None, False),
        (None, True),
        (CFG_FILE, False),
    ],
)
def test_Config___init__(config_file, try_infer_environment):
    testmod.Config(config_file, try_infer_environment)


@pytest.mark.parametrize(
    "config_file,exception",
    [
        (CFG_FILE_WRONG, ValueError),
        (f"/home/{USER}/blaaaa.ini", FileNotFoundError),
    ],
)
def test_Config___init___error(config_file, exception):
    with pytest.raises(exception):
        testmod.Config(config_file, False)


def test_Config__infer_config_from_basedir():
    cfg = testmod.Config(try_infer_environment=False)
    res = cfg._infer_config_from_basedir(LOCAL_DB_DIR)
    assert res[1] == "local-db"


def test_Config__infer_config_from_basedir_error():
    cfg = testmod.Config(try_infer_environment=False)
    with pytest.raises(FileNotFoundError):
        cfg._infer_config_from_basedir("/blaaa")


def test_Config_has_access_lustre():
    cfg = testmod.Config(try_infer_environment=False)
    assert not cfg.has_access_lustre


def test_Config_has_access_users_database():
    cfg = testmod.Config(try_infer_environment=False)
    assert not cfg.has_access_users_database


@lustre_avail
@pytest.mark.parametrize(
    "cfg_id,basedir,init_obslocs_ungridded,init_data_search_dirs",
    [
        ("metno", None, False, False),
        ("metno", None, True, False),
        ("metno", None, True, True),
        ("metno", f"/home/{USER}", True, True),
        ("users-db", None, False, False),
    ],
)
def test_Config_read_config(cfg_id, basedir, init_obslocs_ungridded, init_data_search_dirs):
    cfg = testmod.Config(try_infer_environment=False)
    cfg_file = cfg._config_files[cfg_id]
    assert Path(cfg_file).exists()
    cfg.read_config(cfg_file, basedir, init_obslocs_ungridded, init_data_search_dirs)
    assert len(cfg.DATA_SEARCH_DIRS) == 0
    assert len(cfg.OBSLOCS_UNGRIDDED) == 0
    assert Path(cfg.OUTPUTDIR).exists()
    assert Path(cfg.COLOCATEDDATADIR).exists()
    assert Path(cfg.CACHEDIR).exists()


def test_empty_class_header(empty_cfg):
    cfg = empty_cfg
    assert cfg.AERONET_SUN_V2L15_AOD_DAILY_NAME == "AeronetSunV2Lev1.5.daily"
    assert cfg.AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME == "AeronetSun_2.0_NRT"
    assert cfg.AERONET_SUN_V2L2_AOD_DAILY_NAME == "AeronetSunV2Lev2.daily"
    assert cfg.AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME == "AeronetSunV2Lev2.AP"
    assert cfg.AERONET_SUN_V2L2_SDA_DAILY_NAME == "AeronetSDAV2Lev2.daily"
    assert cfg.AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME == "AeronetSDAV2Lev2.AP"
    assert cfg.AERONET_INV_V2L15_DAILY_NAME == "AeronetInvV2Lev1.5.daily"
    assert cfg.AERONET_INV_V2L15_ALL_POINTS_NAME == "AeronetInvV2Lev1.5.AP"
    assert cfg.AERONET_INV_V2L2_DAILY_NAME == "AeronetInvV2Lev2.daily"
    assert cfg.AERONET_INV_V2L2_ALL_POINTS_NAME == "AeronetInvV2Lev2.AP"
    assert cfg.AERONET_SUN_V3L15_AOD_DAILY_NAME == "AeronetSunV3Lev1.5.daily"
    assert cfg.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME == "AeronetSunV3Lev1.5.AP"
    assert cfg.AERONET_SUN_V3L2_AOD_DAILY_NAME == "AeronetSunV3Lev2.daily"
    assert cfg.AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME == "AeronetSunV3Lev2.AP"
    assert cfg.AERONET_SUN_V3L15_SDA_DAILY_NAME == "AeronetSDAV3Lev1.5.daily"
    assert cfg.AERONET_SUN_V3L15_SDA_ALL_POINTS_NAME == "AeronetSDAV3Lev1.5.AP"
    assert cfg.AERONET_SUN_V3L2_SDA_DAILY_NAME == "AeronetSDAV3Lev2.daily"
    assert cfg.AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME == "AeronetSDAV3Lev2.AP"
    assert cfg.AERONET_INV_V3L15_DAILY_NAME == "AeronetInvV3Lev1.5.daily"
    assert cfg.AERONET_INV_V3L2_DAILY_NAME == "AeronetInvV3Lev2.daily"
    assert cfg.EBAS_MULTICOLUMN_NAME == "EBASMC"
    assert cfg.EEA_NAME == "EEAAQeRep"
    assert cfg.EARLINET_NAME == "EARLINET"
    assert cfg.GAWTADSUBSETAASETAL_NAME == "GAWTADsubsetAasEtAl"
    assert cfg.DMS_AMS_CVO_NAME == "DMS_AMS_CVO"
    assert cfg.EBAS_DB_LOCAL_CACHE
    assert cfg.MIN_YEAR == 0
    assert cfg.MAX_YEAR == 20000
    assert cfg.STANDARD_COORD_NAMES == ["latitude", "longitude", "altitude"]
    assert cfg.DEFAULT_VERT_GRID_DEF == dict(lower=0, upper=15000, step=250)
    assert cfg.RH_MAX_PERCENT_DRY == 40
    assert cfg.DEFAULT_REG_FILTER == "WORLD-wMOUNTAINS"
    assert cfg.OBS_MIN_NUM_RESAMPLE == dict(
        yearly=dict(monthly=3),
        monthly=dict(daily=7),
        daily=dict(hourly=6),
        hourly=dict(minutely=15),
    )
    from pyaerocom import obs_io

    assert cfg.OBS_ALLOW_ALT_WAVELENGTHS == obs_io.OBS_ALLOW_ALT_WAVELENGTHS

    assert cfg.OBS_WAVELENGTH_TOL_NM == obs_io.OBS_WAVELENGTH_TOL_NM

    assert cfg.CLIM_START == 2005
    assert cfg.CLIM_STOP == 2015
    assert cfg.CLIM_FREQ == "daily"
    assert cfg.CLIM_RESAMPLE_HOW == "mean"
    assert cfg.CLIM_MIN_COUNT == dict(daily=30, monthly=5)

    # names for the satellite data sets
    assert cfg.SENTINEL5P_NAME == "Sentinel5P"
    assert cfg.AEOLUS_NAME == "AeolusL2A"

    assert cfg.OLD_AEROCOM_REGIONS == [
        "WORLD",
        "ASIA",
        "AUSTRALIA",
        "CHINA",
        "EUROPE",
        "INDIA",
        "NAFRICA",
        "SAFRICA",
        "SAMERICA",
        "NAMERICA",
    ]

    assert cfg.URL_HTAP_MASKS == "https://pyaerocom.met.no/pyaerocom-suppl/htap_masks/"

    assert cfg.HTAP_REGIONS == [
        "PAN",
        "EAS",
        "NAF",
        "MDE",
        "LAND",
        "SAS",
        "SPO",
        "OCN",
        "SEA",
        "RBU",
        "EEUROPE",
        "NAM",
        "WEUROPE",
        "SAF",
        "USA",
        "SAM",
        "EUR",
        "NPO",
        "MCA",
    ]

    assert cfg.RM_CACHE_OUTDATED

    #: Name of the file containing the revision string of an obs data network
    assert cfg.REVISION_FILE == "Revision.txt"

    #: timeout to check if one of the supported server locations can be
    #: accessed
    assert cfg.SERVER_CHECK_TIMEOUT == 1  # s

    assert cfg._outhomename == "MyPyaerocom"

    with resources.path("pyaerocom.data", "paths.ini") as path:
        assert cfg._config_files["metno"] == cfg._config_ini_lustre == str(path)

    with resources.path("pyaerocom.data", "paths_user_server.ini") as path:
        assert cfg._config_files["users-db"] == cfg._config_ini_user_server == str(path)

    with resources.path("pyaerocom.data", "paths_local_database.ini") as path:
        assert cfg._config_files["local-db"] == cfg._config_ini_localdb == str(path)

    assert cfg._check_subdirs_cfg == {
        "metno": "aerocom",
        "users-db": "AMAP",
        "local-db": "modeldata",
    }

    with resources.path("pyaerocom.data", "variables.ini") as path:
        assert cfg._var_info_file == str(path)
    with resources.path("pyaerocom.data", "coords.ini") as path:
        assert cfg._coords_info_file == str(path)

    dbdirs = {
        "lustre/storeA/project": "metno",
        "metno/aerocom_users_database": "users-db",
        "MyPyaerocom/data": "local-db",
    }
    for sd, name in dbdirs.items():
        assert sd in cfg._DB_SEARCH_SUBDIRS
        assert cfg._DB_SEARCH_SUBDIRS[sd] == name

    assert cfg.DONOTCACHEFILE == None

    assert cfg.ERA5_SURFTEMP_FILENAME == "era5.msl.t2m.201001-201012.nc"

    assert cfg._LUSTRE_CHECK_PATH == "/project/aerocom/aerocom1/"


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
    assert const.HOMEDIR == os.path.expanduser("~") + "/"


def test_default_config():
    cfg = Config()
    home = os.path.abspath(cfg.HOMEDIR)

    mkpath = lambda basepath, relpath: os.path.abspath(os.path.join(basepath, relpath))

    mypydir = mkpath(home, "MyPyaerocom")
    assert cfg.OUTPUTDIR == mypydir
    assert cfg._outputdir == mypydir

    assert cfg.CACHEDIR == mkpath(mypydir, f"_cache/{USER}")

    check = mkpath(mypydir, "colocated_data")
    assert cfg.COLOCATEDDATADIR == check
    # now this should be assigned
    assert cfg._colocateddatadir == check

    check = mkpath(mypydir, "filtermasks")
    assert cfg.FILTERMASKKDIR == check
    # now this should be assigned
    assert cfg._filtermaskdir == check

    check = mkpath(mypydir, "tmp")
    assert cfg.LOCAL_TMP_DIR == check
    # now this should be assigned
    assert cfg._local_tmp_dir == check

    check = mkpath(mypydir, "data")
    assert cfg.DOWNLOAD_DATADIR == check
    # now this should be assigned
    assert cfg._downloaddatadir == check

    assert cfg._caching_active
    assert cfg.CACHING

    from pyaerocom.varcollection import VarCollection

    assert isinstance(cfg.VARS, VarCollection)
    assert cfg.VARS is cfg.VAR_PARAM
    assert isinstance(cfg._var_param, VarCollection)

    assert isinstance(cfg.COORDINFO, VarCollection)
    assert cfg._coords is cfg.COORDINFO

    assert cfg.DATA_SEARCH_DIRS is cfg._search_dirs

    assert cfg.WRITE_FILEIO_ERR_LOG

    from pyaerocom.grid_io import GridIO

    assert isinstance(cfg.GRID_IO, GridIO)
