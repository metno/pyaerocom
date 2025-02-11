"""
Global config for ratio pm10 vs pm25
"""

import copy
import logging
import os

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


def get_CFG(reportyear, year, model_dir) -> dict:
    """create aeroval configuration dict to run the variable
    ratpm10pm25 (ratio pm10 vspm25)

    :returns: a dict of a model configuration usable for EvalSetup
    """
    # get current path for reference to local gridded_io_aux.py

    CFG = dict(
        json_basedir=os.path.abspath("/home/jang/data/aeroval-local-web/data"),
        coldata_basedir=os.path.abspath("/home/jang/data/aeroval-local-web/coldata"),
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
        ts_type="daily",
        map_zoom="Europe",
        freqs=[
            "yearly",
            "monthly",
            "daily",
        ],
        periods=[f"{year}"],
        main_freq="monthly",
        zeros_to_nan=False,
        use_diurnal=True,
        min_num_obs=DEFAULT_RESAMPLE_CONSTRAINTS,
        colocate_time=True,
        obs_remove_outliers=False,
        model_remove_outliers=False,
        harmonise_units=True,
        regions_how="country",
        annual_stats_constrained=True,
        proj_id="emep",
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
        "EMEPcameo": dict(
            model_id="EMEP,",
            model_data_dir=model_dir,
            gridded_reader_id={"model": "ReadMscwCtm"},
            # model_read_aux={},
            model_ts_type_read="daily",
        ),
    }

    """
    Filters
    """

    BASE_FILTER = {
        "latitude": [30, 82],
        "longitude": [-30, 90],
    }

    EBAS_FILTER = {
        **BASE_FILTER,
        "data_level": [None, 2],
        "set_flags_nan": True,
    }

    OBS_GROUNDBASED = {
        ##################
        #    EBAS
        ##################
        "EBAS-d-10": dict(
            obs_id="EBASratd10",
            web_interface_name="EBAS-d",
            obs_vars=["ratpm10pm25"],
            obs_vert_type="Surface",
            colocate_time=True,
            min_num_obs=DEFAULT_RESAMPLE_CONSTRAINTS,
            ts_type="daily",
            obs_filters=EBAS_FILTER,
            obs_type="ungridded",
            obs_merge_how={
                "ratpm10pm25": "eval",
            },
            obs_aux_requires={
                "ratpm10pm25": {
                    "EBASMC": [
                        "concpm10",
                        "concpm25",
                    ],
                }
            },
            obs_aux_funs={
                "ratpm10pm25":
                # variables used in computation method need to be based on AeroCom
                # units, since the colocated StationData objects (from which the
                # new UngriddedData is computed, will perform AeroCom unit check
                # and conversion)
                "(EBASMC;concpm10/EBASMC;concpm25)"
            },
            obs_aux_units={"ratpm10pm25": "1"},
        ),
        "EBAS-d-25": dict(
            obs_id="EBASratd25",
            web_interface_name="EBAS-d",
            obs_vars=["ratpm25pm10"],
            obs_vert_type="Surface",
            colocate_time=True,
            min_num_obs=DEFAULT_RESAMPLE_CONSTRAINTS,
            ts_type="daily",
            obs_filters=EBAS_FILTER,
            obs_type="ungridded",
            obs_merge_how={
                "ratpm25pm10": "eval",
            },
            obs_aux_requires={
                "ratpm25pm10": {
                    "EBASMC": [
                        "concpm10",
                        "concpm25",
                    ],
                }
            },
            obs_aux_funs={
                "ratpm25pm10":
                # variables used in computation method need to be based on AeroCom
                # units, since the colocated StationData objects (from which the
                # new UngriddedData is computed, will perform AeroCom unit check
                # and conversion)
                "(EBASMC;concpm25/EBASMC;concpm10)"
            },
            obs_aux_units={"ratpm25pm10": "1"},
        ),
        "EBAS-d-tc": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-d",
            obs_vars=[
                "concpm10",
                "concpm25",
            ],
            obs_vert_type="Surface",
            colocate_time=True,
            min_num_obs=DEFAULT_RESAMPLE_CONSTRAINTS,
            ts_type="daily",
            obs_filters=EBAS_FILTER,
        ),
    }

    # Setup for supported satellite evaluations
    OBS_SAT = {}

    OBS_CFG = {**OBS_GROUNDBASED, **OBS_SAT}

    CFG["obs_cfg"] = OBS_CFG

    return copy.deepcopy(CFG)
