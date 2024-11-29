"""
this module contains basic aeroval configurations for running on CI
"""

import copy
import logging
from pathlib import Path

from pyaerocom.io.pyaro.pyaro_config import PyaroConfig

logger = logging.getLogger(__name__)

# Constraints
DEFAULT_RESAMPLE_CONSTRAINTS = dict(
    yearly=dict(monthly=9),
    monthly=dict(
        daily=21,
        weekly=3,
    ),
    daily=dict(hourly=18),
)

DEFAULT_RESAMPLE_CONSTRAINTS_DAILY = dict(
    daily=dict(hourly=18),
)

# ODCSFUN_EEANRT = "EEAAQeRep.NRT;concpm10/EEAAQeRep.NRT;concpm25"
ODCSFUN_EEAV2 = "EEAAQeRep.v2;concpm10/EEAAQeRep.v2;concpm25"
ODCSFUN_EBAS = "EBASMC;concpm10/EBASMC;concpm25"

HOMEDIR = Path.home()
MYPEYAEROCOM_DIR = Path.home() / "MyPyaerocom"
MYPEYAEROCOM_DIR.mkdir(exist_ok=True)
TMP_DIR = Path.home() / "tmp"
TMP_DIR.mkdir(exist_ok=True)
JSON_DIR = Path.home() / "tmp" / "data"
JSON_DIR.mkdir(exist_ok=True)
COLDATA_DIR = Path.home() / "tmp" / "coldata"
COLDATA_DIR.mkdir(exist_ok=True)

# data directory for test data
TEST_DATA_DIR = MYPEYAEROCOM_DIR / "testdata-minimal" / "obsdata" / "diurnal_test_data"


def get_CFG(reportyear, year) -> dict:
    """create aeroval configuration dict to run the variable
    ratpm10pm25 (ratio pm10 vspm25)

    :returns: a dict of a model configuration usable for EvalSetup
    """
    # get current path for reference to local gridded_io_aux.py

    CFG = dict(
        json_basedir=JSON_DIR,
        coldata_basedir=COLDATA_DIR,
        # io_aux_file=os.path.abspath("/home/jang/data/aeroval-local-web/gridded_io_aux.py"), not needed for ReadMscwCtm
        # io_aux_file=os.path.join(base_conf_path, "gridded_io_aux.py"),
        # var_scale_colmap_file=os.path.abspath(
        #     "/home/jang/data/aeroval-local-web/pyaerocom-config/config_files/CAMEO/user_var_scale_colmap.ini"
        # ),
        # if True, existing colocated data files will be deleted and contours will be overwritten
        reanalyse_existing=True,
        only_json=False,
        add_model_maps=False,
        only_model_maps=False,
        modelmaps_opts=dict(maps_freq="monthly", maps_res_deg=5),
        clear_existing_json=False,
        # if True, the analysis will stop whenever an error occurs (else, errors that
        # occurred will be written into the logfiles)
        raise_exceptions=False,
        # Regional filter for analysis
        filter_name="ALL-wMOUNTAINS",
        # colocation frequency (no statistics in higher resolution can be computed)
        ts_type="hourly",
        map_zoom="Europe",
        freqs=[
            "monthly",
            "daily",
            "hourly",
        ],
        periods=[f"{year}"],
        main_freq="daily",
        zeros_to_nan=False,
        use_diurnal=True,
        min_num_obs=DEFAULT_RESAMPLE_CONSTRAINTS,
        colocate_time=False,
        obs_remove_outliers=False,
        model_remove_outliers=False,
        harmonise_units=True,
        regions_how="country",
        # annual_stats_constrained=True,
        proj_id="emepCI",
        exp_id=f"{reportyear}-reporting",
        exp_name=f"Evaluation of EMEP runs for {reportyear} EMEP reporting",
        exp_descr=(
            f"Evaluation of EMEP runs for {reportyear} EMEP reporting. The EMEP model, simulated for {year}, is compared against observations from EEA and EBAS."
        ),
        exp_pi="emep.mscw@met.no",
        public=True,
        # directory where colocated data files are supposed to be stored
        weighted_stats=True,
        var_order_menu=[
            # Gases
            "ratpm10pm25",
            "ratpm25pm10",
            "concNno",
            "concNno2",
            "concNtno3",
            "concNhno3",
            "concNtnh",
            "concNnh3",
            "concnh4",
            "concSso2",
            "concso4t",
            "concso4c",
            "vmro3",
            "vmro3max",
            "vmro3mda8",
            "vmrox",
            "vmrco",
            # PMs
            "concpm10",
            "concpm25",
            "concno3pm10",
            "concno3pm25",
            "concnh4pm25",
            "concso4pm25",
            "concCecpm10",
            "concCecpm25",
            "concCocpm10",  # SURF_ugC_PM_OMCOARSE missing in model-output
            "concCocpm25",
            "concsspm10",
            "concsspm25",
            # Depositions
            "wetrdn",
            "wetoxs",
            "wetoxn",
            "prmm",
        ],
    )

    CFG["model_cfg"] = {
        "EMEPCI": dict(
            model_id="EMEP.CI",
            model_ts_type_read="hourly",
        ),
    }

    """
    Filters
    """

    BASE_FILTER = {
        "latitude": [30, 82],
        "longitude": [-30, 90],
    }

    data_name = "CITestData"
    data_id = "harp"

    config = PyaroConfig(
        name=data_name,
        data_id=data_id,
        filename_or_obj_or_url=TEST_DATA_DIR,
        filters={"variables": {"include": ["O3_density"]}},
        name_map={"O3_density": "vmro3"},
    )

    EBAS_FILTER = {
        **BASE_FILTER,
        "data_level": [None, 2],
        "set_flags_nan": True,
    }

    OBS_GROUNDBASED = {
        ################
        #    Pyaro
        ################
        "Pyaro-h": dict(
            obs_id=config.name,
            obs_config=config,
            web_interface_name=data_name,
            obs_name=data_name,
            obs_vars=["vmro3"],
            # obs_vert_type="Column",
            obs_vert_type="Surface",
            # colocate_time=True,
            # min_num_obs={
            #     "yearly": {"monthly": 9},
            #     "monthly": {"daily": 4, "weekly": 1},
            #     "daily": {"hourly": 18},
            #     # "hourly": {"minutely": 45},
            # },
            ts_type="hourly",
            # obs_filters=Pyaro_FILTER,
        ),
    }

    # Setup for supported satellite evaluations
    OBS_SAT = {}

    OBS_CFG = {**OBS_GROUNDBASED, **OBS_SAT}

    CFG["obs_cfg"] = OBS_CFG

    return copy.deepcopy(CFG)
