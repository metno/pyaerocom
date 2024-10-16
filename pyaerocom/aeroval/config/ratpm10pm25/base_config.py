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
    base_conf_path = os.path.dirname(__file__)

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
        # "EMEP": dict(
        #     model_id="EMEP.ratpm25pm10.testing",
        #     # model_read_aux={
        #
        #     #     "ratpm10pm25": dict(
        #     #         vars_required=["sconcpm10", "sconcpm25"], fun="calc_ratpm10pm25"
        #     #     )
        #     # },
        # ),
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

    AERONET_FILTER = {
        **BASE_FILTER,  # Forandring fra Daniel
        "altitude": [-20, 1000],
    }

    # Station filters

    ebas_species = [
        "concpm10",
        "concpm25",
        "ratpm10pm25",
        "ratpm25pm10",
    ]

    # no new sites with 2021 observations (comment Svetlana T.)
    height_ignore_ebas = [
        "AT0034G",
        "AT0038R",
        "AT0049R",
        "BG0001R",
        "CH0001G",
        "CH0018R",
        "CH0024R",
        "CH0031R",
        "CH0033R",
        "DE0054R",
        "DE0057G",
        "DE0075R",
        "ES0005R",
        "ES0022R",
        "FR0019R",
        "FR0030R",
        "FR0031R",
        "FR0038U",
        "FR0039U",
        "FR0100G",
        "GR0003R",
        "GR0101R",
        "HR0002R",
        "HR0004R",
        "IT0002R",
        "IT0009R",
        "IT0019R",
        "IT0020U",
        "IT0021U",
        "IT0024R",
        "KG0001R",
        "KG0002U",
        "NO0036R",
        "NO0039R",
        "NO0211R",
        "NO0214R",
        "NO0225R",
        "NO0226R",
        "NO0227R",
        "NO0229R",
        "NO0796R",
        "NO0802R",
        "NO0907R",
        "NO2073R",
        "NO2079R",
        "NO2085R",
        "NO2096R",
        "NO2156R",
        "NO2210R",
        "NO2216R",
        "NO2219R",
        "NO2233R",
        "NO2239R",
        "NO2257R",
        "NO2263R",
        "NO2274R",
        "NO2280R",
        "NO2288R",
        "NO2362R",
        "NO2380R",
        "NO2397R",
        "NO2411R",
        "PL0003R",
        "PT0005R",
        "PT0007R",
        "PT0012R",
        "RO0002R",
        "RO0003R",
        "SE0093R",
        "SE0094R",
        "SI0032R",
        "SK0002R",
    ]

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
