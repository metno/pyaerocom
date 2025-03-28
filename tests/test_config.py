from __future__ import annotations

import getpass
import logging
import os.path
from pathlib import Path

import pytest

import pyaerocom.config as testmod
from pyaerocom import const
from pyaerocom.config import ALL_REGION_NAME, Config
from pyaerocom.data import resources
from pyaerocom.grid_io import GridIO
from pyaerocom.varcollection import VarCollection
from pyaerocom.variable import Variable
from tests.conftest import lustre_avail

USER = getpass.getuser()

with resources.path("pyaerocom.data", "paths.ini") as path:
    DEFAULT_PATHS_INI = str(path)

logger = logging.getLogger(__name__)


@pytest.fixture()
def config_file(file: str | None, tmp_path: Path) -> str | None:
    if file is None:
        return None

    if file.casefold() == "default":
        assert resources.is_resource("pyaerocom.data", "paths.ini")
        with resources.path("pyaerocom.data", "paths.ini") as path:
            return str(path)

    if file.casefold() == "wrong_suffix":
        path = tmp_path / "paths.txt"
        path.write_text("")
        assert path.exists()
        return str(path)

    return file


@pytest.fixture()
def local_db(tmp_path: Path) -> Path:
    """temporary path to DB file structure"""
    path = tmp_path / "data"
    (path / "modeldata").mkdir(parents=True)
    (path / "obsdata").mkdir()
    assert path.is_dir()
    return path


@pytest.fixture(scope="module")
def empty_cfg():
    cfg = testmod.Config(try_infer_environment=False)
    return cfg


@pytest.mark.parametrize(
    "file,try_infer_environment",
    [
        (None, False),
        (None, True),
        ("default", False),
    ],
)
def test_Config___init__(config_file: str, try_infer_environment: bool):
    testmod.Config(config_file, try_infer_environment)


@pytest.mark.parametrize(
    "file,exception,error",
    [
        pytest.param(
            "wrong_suffix",
            ValueError,
            "Need path to an ini file for input config_file",
            id="wrong file extension",
        ),
        pytest.param(
            f"/home/{USER}/blaaaa.ini",
            FileNotFoundError,
            f"input config file does not exist /home/{USER}/blaaaa.ini",
            id="no such file",
        ),
    ],
)
def test_Config___init___error(config_file: str, exception: type[Exception], error: str):
    with pytest.raises(exception) as e:
        testmod.Config(config_file, False)
    assert str(e.value) == error


def test_Config_has_access_lustre():
    cfg = testmod.Config(try_infer_environment=False)
    assert not cfg.has_access_lustre


def test_user_specific_paths_ini():
    # test if user specific paths.ini file is read
    CHANGE_NAME = "NAME_CHANGED_FOR_TESTING"
    CHECK_NAME = "GAWTADSUBSETAASETAL"
    user_file = os.path.join(const.my_pyaerocom_dir, const.PATHS_INI_NAME)
    # only create user_file if it doesn't exist
    del_flag = False
    if not os.path.exists(user_file):
        with open(DEFAULT_PATHS_INI) as infile, open(user_file, "w") as outfile:
            for line in infile:
                if CHECK_NAME in line:
                    line = f"{CHECK_NAME} = {CHANGE_NAME}\n"
                else:
                    line = line.replace("/lustre/storeB/project", "${HOME}")
                outfile.write(line)
        del_flag = True

    assert os.path.exists(user_file)
    # no real test here for now since we would need to get rid of the already loaded const module
    # and recreate that The following does not work due to caching
    # cfg = testmod.Config(try_infer_environment=False)
    # assert cfg.GAWTADSUBSETAASETAL == CHANGE_NAME

    if del_flag:
        os.remove(user_file)


def test_Config_read_config():
    cfg = testmod.Config(try_infer_environment=False)
    cfg_file = DEFAULT_PATHS_INI
    assert Path(cfg_file).exists()
    cfg.read_config(cfg_file)
    # not all paths from the default paths.ini are present on CI
    # Just test a few of them
    assert Path(cfg.OUTPUTDIR).exists()
    assert Path(cfg.COLOCATEDDATADIR).exists()
    assert Path(cfg.CACHEDIR).exists()


def test_empty_class_header(empty_cfg):
    cfg = empty_cfg
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
    assert cfg.CNEMC_NAME == "CNEMC"
    assert cfg.EBAS_DB_LOCAL_CACHE
    assert cfg.MIN_YEAR == 0
    assert cfg.MAX_YEAR == 20000
    assert cfg.STANDARD_COORD_NAMES == ["latitude", "longitude", "altitude"]
    assert cfg.DEFAULT_VERT_GRID_DEF == dict(lower=0, upper=15000, step=250)
    assert cfg.RH_MAX_PERCENT_DRY == 40
    assert cfg.DEFAULT_REG_FILTER == f"{ALL_REGION_NAME}-wMOUNTAINS"
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
    assert cfg.CLIM_FREQ == "monthly"
    assert cfg.CLIM_RESAMPLE_HOW == "mean"
    assert cfg.CLIM_MIN_COUNT == dict(daily=30, monthly=5)

    # names for the satellite data sets
    assert cfg.SENTINEL5P_NAME == "Sentinel5P"
    assert cfg.AEOLUS_NAME == "AeolusL2A"

    assert cfg.OLD_AEROCOM_REGIONS == [
        ALL_REGION_NAME,
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

    assert cfg._outhomename == "MyPyaerocom"

    with resources.path("pyaerocom.data", "variables.ini") as path:
        assert cfg._var_info_file == str(path)
    with resources.path("pyaerocom.data", "coords.ini") as path:
        assert cfg._coords_info_file == str(path)

    assert cfg.DO_NOT_CACHE_FILE is None

    assert cfg.ERA5_SURFTEMP_FILENAME == "era5.msl.t2m.201001-201012.nc"

    assert cfg._LUSTRE_CHECK_PATH == "/"


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
    assert Path(const.HOMEDIR) == Path("~").expanduser()
    assert const.HOMEDIR.endswith("/")


@lustre_avail
def test_default_config():
    cfg = Config()

    mypydir = Path(cfg.HOMEDIR).resolve() / "MyPyaerocom"
    assert Path(cfg.OUTPUTDIR) == Path(cfg._outputdir) == mypydir
    assert Path(cfg.CACHEDIR) == mypydir / f"_cache/{USER}"
    assert Path(cfg.COLOCATEDDATADIR) == Path(cfg._colocateddatadir) == mypydir / "colocated_data"
    assert Path(cfg.FILTERMASKKDIR) == Path(cfg._filtermaskdir) == mypydir / "filtermasks"
    assert Path(cfg.LOCAL_TMP_DIR) == Path(cfg._local_tmp_dir) == mypydir / "tmp"
    assert Path(cfg.DOWNLOAD_DATADIR) == Path(cfg._downloaddatadir) == mypydir / "data"

    assert cfg._caching_active
    assert cfg.CACHING

    assert isinstance(cfg.VARS, VarCollection)
    assert cfg.VARS is cfg.VAR_PARAM
    assert isinstance(cfg._var_param, VarCollection)

    assert isinstance(cfg.COORDINFO, VarCollection)
    assert cfg._coords is cfg.COORDINFO

    assert cfg.DATA_SEARCH_DIRS is cfg._search_dirs

    assert cfg.WRITE_FILEIO_ERR_LOG

    assert isinstance(cfg.GRID_IO, GridIO)


def test_register_variable_with_dict():
    test_var_name = "conctestvariabledict"
    variables = {
        test_var_name: {
            "var_name": test_var_name,
            "units": "ug m-3",
        }
    }
    const.register_custom_variables(variables)

    vars = const.VARS

    assert test_var_name in vars.find(test_var_name)


def test_register_variable_with_Variable():
    test_var_name = "testvariableVariable"
    variables = {
        test_var_name: Variable(
            var_name=test_var_name,
            units="ug m-3",
        ),
    }
    const.register_custom_variables(variables)

    vars = const.VARS

    assert test_var_name in vars.all_vars
