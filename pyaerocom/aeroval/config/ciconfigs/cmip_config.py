"""
this module contains basic aeroval configurations for running on CI
"""

import copy
import logging
from pathlib import Path

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

HOMEDIR = Path.home()
MYPYAEROCOM_DIR = Path.home() / "MyPyaerocom"
TMP_DIR = MYPYAEROCOM_DIR / "tmp"
JSON_DIR = MYPYAEROCOM_DIR / "tmp" / "data"
COLDATA_DIR = MYPYAEROCOM_DIR / "tmp" / "coldata"

# data directory for test data
TEST_DATA_DIR = MYPYAEROCOM_DIR / "testdata-minimal" / "obsdata" / "diurnal_test_data"

IO_AUX_FILE = MYPYAEROCOM_DIR / "testdata-minimal" / "config" / "gridded_io_aux.py"
MODELDIR = MYPYAEROCOM_DIR / "testdata-minimal" / "modeldata" / "CMIP6"
START_TIME = "2013-06-01"
STOP_TIME = "2014-06-01"
PERIODS = ["2014", "2015"]


def get_CFG(
    start=START_TIME,
    stop=STOP_TIME,
) -> dict:
    """create aeroval configuration dict to run the variable

    :returns: a dict of a model configuration usable for EvalSetup
    """
    MYPYAEROCOM_DIR.mkdir(exist_ok=True)
    TMP_DIR.mkdir(exist_ok=True)
    JSON_DIR.mkdir(exist_ok=True)
    COLDATA_DIR.mkdir(exist_ok=True)
    # reportyear = year

    CFG = dict(
        json_basedir=JSON_DIR,
        coldata_basedir=COLDATA_DIR,
        io_aux_file=IO_AUX_FILE,
        # if True, existing colocated data files will be deleted and contours will be overwritten
        reanalyse_existing=True,
        only_json=False,
        add_model_maps=False,
        only_model_maps=False,
        # modelmaps_opts=dict(maps_freq="monthly", maps_res_deg=5),
        clear_existing_json=False,
        # if True, the analysis will stop whenever an error occurs (else, errors that
        # occurred will be written into the logfiles)
        raise_exceptions=True,
        # Regional filter for analysis
        filter_name="ALL-wMOUNTAINS",
        # colocation frequency (no statistics in higher resolution can be computed)
        ts_type="monthly",
        # map_zoom="Europe",
        freqs=[
            "monthly",
            "daily",
        ],
        periods=PERIODS,
        main_freq="monthly",
        zeros_to_nan=False,
        use_diurnal=False,
        min_num_obs=DEFAULT_RESAMPLE_CONSTRAINTS,
        colocate_time=False,
        obs_remove_outliers=False,
        model_remove_outliers=False,
        harmonise_units=True,
        regions_how="default",
        # annual_stats_constrained=True,
        proj_id="CMIPCI",
        exp_id="CMIP testing reporting",
        exp_name="Evaluation of CMIP data ",
        exp_descr="Evaluation of CMIP runs",
        exp_pi="jan.griesfeller@met.no",
        public=True,
        # directory where colocated data files are supposed to be stored
        weighted_stats=True,
        var_order_menu=[
            # Gases
            "od550aer",
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
        "CMIPCI": dict(
            model_id="MPI-ESM-1-2-HAM",
            model_ts_type_read="monthly",
            model_data_dir=str(MODELDIR),
            gridded_reader_id={"model": "ReadCmipCtm"},
            start=start,
            stop=stop,
        ),
    }

    """
    Filters
    """

    OBS_GROUNDBASED = {
        "AeronetSubset": dict(
            # obs_id="AeronetSunV3L2Subset.daily",
            obs_id="AeronetSunV3Lev2.daily",
            obs_vars=["od550aer"],
            obs_vert_type="Column",
            min_num_obs={"monthly": {"daily": 3}},
        ),
    }

    # Setup for supported satellite evaluations
    OBS_SAT = {}

    OBS_CFG = {**OBS_GROUNDBASED, **OBS_SAT}

    CFG["obs_cfg"] = OBS_CFG

    return copy.deepcopy(CFG)
