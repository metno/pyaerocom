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
        add_model_maps=True,
        only_model_maps=False,
        modelmaps_opts=dict(maps_freq="yearly", maps_res_deg=5),
        clear_existing_json=False,
        # if True, the analysis will stop whenever an error occurs (else, errors that
        # occurred will be written into the logfiles)
        raise_exceptions=True,
        # Regional filter for analysis
        filter_name="ALL-wMOUNTAINS",
        # colocation frequency (no statistics in higher resolution can be computed)
        ts_type="daily",
        map_zoom="Europe",
        freqs=["yearly", "monthly", "weekly", "daily", "hourly"],
        periods=[f"{year}"],
        main_freq="daily",
        zeros_to_nan=False,
        use_diurnal=True,
        min_num_obs=DEFAULT_RESAMPLE_CONSTRAINTS,
        colocate_time=True,
        resample_how={"vmro3max": {"daily": {"hourly": "max"}}},
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
        "EMEP.cameo": dict(
            model_id="EMEP,",
            model_data_dir=model_dir,
            # gridded_reader_id={"model": "ReadMscwCtm"},
            # model_read_aux={},
            # model_ts_type_read="daily",
        ),
    }

    """
    Filters
    """

    # OBS SPECIFIC FILTERS (combination of the above and more)
    EEA_RURAL_FILTER = {
        "station_classification": ["background"],
        "area_classification": [
            "rural",
            "rural-nearcity",
            "rural-regional",
            "rural-remote",
        ],
    }

    BASE_FILTER = {
        "latitude": [30, 82],
        "longitude": [-30, 90],
    }

    EBAS_FILTER = {
        **BASE_FILTER,
        "data_level": [None, 2],
        "set_flags_nan": True,
    }

    EEA_FILTER = {
        **BASE_FILTER,
        **EEA_RURAL_FILTER,
    }

    EEA_FILTER_ALL = {
        **BASE_FILTER,
    }

    AERONET_FILTER = {
        **BASE_FILTER,  # Forandring fra Daniel
        "altitude": [-20, 1000],
    }

    # Station filters

    eea_species = [
        "concpm10",
        "concpm25",
        "ratpm10pm25",
    ]

    ebas_species = [
        "concpm10",
        "concpm25",
        "ratpm10pm25",
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

    height_ignore_eea = [
        "FR33220",
        "TR0047A",
        "AT72619",
        "ES1982A",
        "IT0983A",
        "IS0040A",
        "IT2099A",
        "BG0080A",
        "IT2159A",
        "IT0906A",
        "AT72821",
        "IT1190A",
        "IT1976A",
        "AT56072",
        "IT2178A",
        "IS0044A",
        "IT1335A",
        "AT0SON1",
        "IT0703A",
        "AT72227",
        "DEUB044",
        "AT55032",
        "HR0013A",
        "FR33120",
        "AT60182",
        "IT0908A",
        "ES1673A",
        "AT55019",
        "SK0042A",
        "SI0032R",
        "ES0005R",
        "FR33720",
        "DEBY196",
        "AT60177",
        "IT2128A",
        "AT2SP18",
        "FR15045",
        "R160421",
        "IT2234A",
        "TR0118A",
        "DEST039",
        "E165168",
        "AT72110",
        "FR15013",
        "ES1348A",
        "E165169",
        "AL0206A",
        "AT72822",
        "DEBY123",
        "FR15031",
        "AT72538",
        "IS0042A",
        "FR33114",
        "AT52300",
        "IT1859A",
        "FR33232",
        "IT2239A",
        "IS0043A",
        "PL0003R",
        "FR31027",
        "FR33113",
        "FR15048",
        "AT54057",
        "TR0046A",
        "FR33111",
        "IT2284A",
        "AT72550",
        "IT1037A",
        "FR33121",
        "E165167",
        "IT1847A",
        "AT72912",
        "RS0047A",
        "R610613",
        "TR0110A",
        "R160512",
        "IT1191A",
        "IT1963A",
        "FR15053",
        "RO0009R",
        "IT0508A",
        "IT2233A",
        "MK0041A",
        "AT72519",
        "BG0079A",
        "IT1696A",
        "IT1619A",
        "IT2267A",
        "TR0107A",
        "AT56071",
        "FR29440",
        "AT4S235",
        "AD0945A",
        "IS0038A",
        "E165166",
        "PT01047",
        "AT55018",
        "SK0002R",
        "IT0499A",
        "HR0014A",
        "IT0591A",
        "IT0507A",
        "AT72315",
        "E165170",
        "ES1432A",
        "IT1166A",
        "AT4S254",
        "IT1967A",
        "AT2VL52",
        "IT1930A",
        "AT72115",
        "AT82708",
        "IT0988A",
        "FR15038",
        "AT82801",
        "IT2285A",
        "NO0039R",
        "TR0020A",
        "IT2096A",
        "AD0942A",
        "TR0071A",
        "E165165",
        "ES0354A",
        "AT72910",
        "ES1882A",
        "IT1725A",
        "AT60150",
        "CH0024A",
        "IT1114A",
        "AT72113",
        "IT1852A",
        "IS0048A",
        "FR15017",
        "FR15039",
        "IT0980A",
        "IT0502A",
        "IT1678A",
        "IT1334A",
        "IT0978A",
        "FR15043",
        "IT2279A",
        "IT0775A",
        "IT1539A",
        "AT72123",
        "IT2014A",
        "XK0005A",
        "AT2WO15",
        "FR33122",
        "XK0007A",
        "AT60196",
        "CH0033A",
        "IT1385A",
        "GR0405A",
        "AT52000",
        "IT2266A",
        "FR15046",
        "AT72223",
        "FR24024",
        "IT0979A",
        "AT2SP10",
        "IT2179A",
        "IT0977A",
        "AT72530",
        "ES1248A",
        "AT72106",
        "IT0753A",
    ]

    EEA_FILTER_ALL = {
        key: dict(
            **EEA_FILTER_ALL,
            station_name=height_ignore_eea,
            negate="station_name",
        )
        for key in eea_species
    }

    OBS_GROUNDBASED = {
        ##################
        #    EBAS
        ##################
        "EBAS-m": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-m",
            obs_vars=ebas_species,
            obs_vert_type="Surface",
            colocate_time=True,
            ts_type="monthly",
            obs_filters=EBAS_FILTER,
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
                "vmrox":
                # variables used in computation method need to be based on AeroCom
                # units, since the colocated StationData objects (from which the
                # new UngriddedData is computed, will perform AeroCom unit check
                # and conversion)
                "(EBASMC;concpm10/EBASMC;concpm25)"
            },
            obs_aux_units={"ratpm10pm25": "1"},
        ),
        "EBAS-d": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-d",
            obs_vars=ebas_species,
            obs_vert_type="Surface",
            colocate_time=True,
            min_num_obs=DEFAULT_RESAMPLE_CONSTRAINTS,
            ts_type="daily",
            obs_filters=EBAS_FILTER,
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
                "vmrox":
                # variables used in computation method need to be based on AeroCom
                # units, since the colocated StationData objects (from which the
                # new UngriddedData is computed, will perform AeroCom unit check
                # and conversion)
                "(EBASMC;concpm10/EBASMC;concpm25)"
            },
            obs_aux_units={"ratpm10pm25": "1"},
        ),
        # Diurnal
        # "EBAS-h-diurnal": dict(
        #     obs_id="EBASMC",
        #     web_interface_name="EBAS-h",
        #     obs_vars=[
        #         "concNno2",
        #         "concNno",
        #         "vmro3",
        #         "concpm10",
        #         "concpm25",
        #     ],
        #     obs_vert_type="Surface",
        #     ts_type="hourly",
        #     # diurnal_only=True,
        #     resample_how="mean",
        #     obs_filters={**EBAS_FILTER, "ts_type": "hourly"},
        # ),
        # OX
        ################
        #    EEA-rural
        ################
        "EEA-d-rural": dict(
            obs_id="EEAAQeRep.v2",
            obs_vars=[
                "concpm10",
                "concpm25",
                "ratpm10pm25",
            ],
            web_interface_name="EEA-rural",
            obs_vert_type="Surface",
            obs_filters=EEA_FILTER,
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
                "vmrox":
                # variables used in computation method need to be based on AeroCom
                # units, since the colocated StationData objects (from which the
                # new UngriddedData is computed, will perform AeroCom unit check
                # and conversion)
                "(EBASMC;concpm10/EBASMC;concpm25)"
            },
            obs_aux_units={"ratpm10pm25": "1"},
        ),
        ################
        #    EEA-all
        ################
        "EEA-d-all": dict(
            obs_id="EEAAQeRep.v2",
            obs_vars=[
                "concpm10",
                "concpm25",
                "ratpm10pm25",
            ],
            web_interface_name="EEA-all",
            obs_vert_type="Surface",
            obs_filters=EEA_FILTER_ALL,
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
                "vmrox":
                # variables used in computation method need to be based on AeroCom
                # units, since the colocated StationData objects (from which the
                # new UngriddedData is computed, will perform AeroCom unit check
                # and conversion)
                "(EBASMC;concpm10/EBASMC;concpm25)"
            },
            obs_aux_units={"ratpm10pm25": "1"},
        ),
    }

    # Setup for supported satellite evaluations
    OBS_SAT = {}

    OBS_CFG = {**OBS_GROUNDBASED, **OBS_SAT}

    CFG["obs_cfg"] = OBS_CFG

    return copy.deepcopy(CFG)
