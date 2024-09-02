"""
Global config for CAMEO reporting pyaeroval runs
based on the memp config in the emep sub folder
"""

import copy
import functools
import logging
import os

import yaml
from pyaerocom.data import resources

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

OC_EC_RESAMPLE_CONSTRAINTS = dict(
    yearly=dict(monthly=4),
    monthly=dict(daily=4, weekly=1),
    daily=dict(hourly=18),
    hourly=dict(minutely=45),
)

OC_EC_RESAMPLE_CONSTRAINTS_DAILY = dict(
    # monthly=dict(daily=4, weekly=1),
    daily=dict(hourly=18),
    hourly=dict(minutely=45),
)


@functools.cache
def _get_ignore_stations_from_file():
    if os.path.exists("./omit_stations.yaml"):
        filename = os.path.abspath("./omit_stations.yaml")
        logger.info(f"reading omit_stations.yaml from {filename}")
        with open(filename) as fh:
            stations = yaml.safe_load(fh)
    else:
        with resources.path(__package__, "omit_stations.yaml") as filename:
            logger.info(f"reading omit_stations.yaml from {filename}")
            with filename.open() as fh:
                stations = yaml.safe_load(fh)

    rows = []
    for year, comps in stations.items():
        if year == "variables":
            continue
        year = int(year)
        for comp, stats in comps.items():
            for stat in stats:
                for var in stations["variables"][comp]:
                    rows.append((year, year, var.strip(), stat.strip()))
    return rows


def _get_ignore_stations(specy, year):
    """
    Read the ignore stations from either omit_stations.tsv in the local eller in the lib-folder

    specy: specy for this measurement network (ALL are translated to all specy)
    year: only select the stations for the specified year

    return: list of stations
    """
    retvals = []
    year = int(year)
    stations = _get_ignore_stations_from_file()
    for yearstart, yearend, comp, station in stations:
        if comp == "ALL" or comp == specy:
            if yearstart <= year <= yearend:
                retvals.append(station)
    return retvals


# def get_CFG(reportyear, year, ) -> dict:
def get_CFG(
    anayear,
) -> dict:
    """Get a configuration usable for emep reporting

    :param anayear: year of analysis

    The current working directory of the experiment should have the following files/directories by default:
        - `data` output directory
        - `coldata` output directory
        - `user_var_scale_colmap.ini` optional user-defined colormaps for pyaerocom variables
        - `omit_stations.yaml` optional user-defined yaml file of stations to omit

    The default values can be changed in your program. If you want to permanently change the defaults,
    please agree upon these changes with the modellers and contact the pyaerocom-developers.

    Example runs with this config look like::

        import os
        import pyaerocom as pya
        from pyaerocom import const
        from pyaerocom.aeroval import EvalSetup, ExperimentProcessor

        from pyaerocom.aeroval.config.emep.reporting_base import get_CFG

        # Setup for models used in analysis
        CFG = get_CFG(reportyear=2024,
                    year=2021,
                    model_dir="/lustre/storeB/project/fou/kl/emep/ModelRuns/2024_REPORTING/EMEP01_rv5.3_metyear2021_emis2022")

        CFG.update(dict(
            # proj_id="status-2024",
            exp_id="test-2021met_2022emis",
            exp_name="Test runs for 2024 EMEP reporting",
            exp_descr=(
                "Test run from Agnes for 2024_REPORTING/EMEP01_rv5.3_metyear2021_emis2022, i.e. 2021met and 2022emis"
            ),
            exp_pi="S. Tsyro, A. Nyiri, H. Klein",
        ))

        # remove EEA
        # for obs in list(CFG["obs_cfg"].keys()):
        #     if obs.startswith("EEA"):
        #         del CFG["obs_cfg"][obs]
        #         print(f"removed {obs}")

        # remove "concCocpm10", not in model-output
        for obs in CFG["obs_cfg"]:
            if "concCocpm10" in CFG["obs_cfg"][obs]["obs_vars"]:
                CFG["obs_cfg"][obs]["obs_vars"].remove("concCocpm10")

        # remove "no, pm10, pm25" from EBAS-hourly
        CFG["obs_cfg"]["EBAS-h-diurnal"]["obs_vars"].remove("concNno")
        CFG["obs_cfg"]["EBAS-h-diurnal"]["obs_vars"].remove("concpm10")
        CFG["obs_cfg"]["EBAS-h-diurnal"]["obs_vars"].remove("concpm25")


        # CFG["raise_exceptions"] = False
        # CFG["add_model_maps"] = False
        # CFG["only_model_maps"] = True


        stp = EvalSetup(**CFG)
        cdir = "./cache/"
        os.makedirs(cdir, exist_ok=True)
        const.CACHEDIR = cdir

        ana = ExperimentProcessor(stp)
        ana.update_interface()

        res = ana.run()

    Another example for multiple model-evaluation::

        import os
        import pyaerocom as pya
        from pyaerocom import const
        from pyaerocom.aeroval import EvalSetup, ExperimentProcessor

        from pyaerocom.aeroval.config.emep.reporting_base import get_CFG

        # Setup for models used in analysis
        CFG = get_CFG(
            reportyear=2024,
            year=2022,
            model_dir=f"/lustre/storeB/project/fou/kl/emep/ModelRuns/2024_REPORTING/EMEP01_rv5.3_year2022_Status_Rep2024",
        )

        dir_versions = {
            "FFmod": "/lustre/storeB/project/fou/kl/emep/ModelRuns/2024_REPORTING/EMEP01_rv5.3_year2022_Status_Rep2024_FFmod/",
            "MARS5.3": "/lustre/storeB/project/fou/kl/emep/ModelRuns/2024_REPORTING/EMEP01_rv5.3_year2022_Status_Rep2024_MARS/",
            "MARS5.0": "/lustre/storeB/project/fou/kl/emep/ModelRuns/2024_REPORTING/EMEP01_rv5.0_year2022_Status_Rep2023_emis2022/",
            "NoCations": "/lustre/storeB/project/fou/kl/emep/ModelRuns/2024_REPORTING/EMEP01_rv5.3_year2022_Status_Rep2024_noCation/",
        }

        # Comparison of several models
        MODEL = CFG["model_cfg"]["EMEP"]
        for mid, fpath in dir_versions.items():
            CFG["model_cfg"][mid] = MODEL.copy()
            CFG["model_cfg"][mid]["model_data_dir"] = fpath
            CFG["model_cfg"][mid]["model_id"] = mid
        del CFG["model_cfg"]["EMEP"]

        # change some config settings, usually not needed
        CFG.update(
            dict(
                proj_id="emepX",
                exp_id=f"2024-XXX_2022_ebas2",
                # exp_name="Evaluation of EMEP runs for 2023 EMEP reporting",
                exp_descr=(
                    f"Evaluation of EMEP runs for 2024 EMEP reporting, MARS vs ISOROPIA. /lustre/storeB/project/fou/kl/emep/ModelRuns/2024_REPORTING/EMEP01_rv5.?_year2022_Status_Rep2024_*/, is compared against observations from EBAS."
                ),
                # periods=["2021"],
                # exp_pi="S. Tsyro, H. Klein",
                # add_model_maps=False,
            )
        )

        # remove "concCocpm10", not in model-output
        for obs in CFG["obs_cfg"]:
            if "concCocpm10" in CFG["obs_cfg"][obs]["obs_vars"]:
                CFG["obs_cfg"][obs]["obs_vars"].remove("concCocpm10")

        # remove "no, pm10, pm25" from EBAS-hourly
        CFG["obs_cfg"]["EBAS-h-diurnal"]["obs_vars"].remove("concNno")
        CFG["obs_cfg"]["EBAS-h-diurnal"]["obs_vars"].remove("concpm10")
        CFG["obs_cfg"]["EBAS-h-diurnal"]["obs_vars"].remove("concpm25")

        # remove EEA
        for obs in list(CFG["obs_cfg"].keys()):
            if obs.startswith("EEA"):
                del CFG["obs_cfg"][obs]
                print(f"removed {obs}")


        # try to run anything, but don't fail on error
        # CFG["raise_exceptions"] = False


        stp = EvalSetup(**CFG)

        cdir = "./cache"
        os.makedirs(cdir, exist_ok=True)
        const.CACHEDIR = cdir

        ana = ExperimentProcessor(stp)
        ana.update_interface()

        # run everything
        res = ana.run()

    and the example for trends::

        import os
        import pyaerocom as pya
        from pyaerocom import const
        from pyaerocom.aeroval import EvalSetup, ExperimentProcessor

        from pyaerocom.aeroval.config.emep.reporting_base import get_CFG

        # Setup for models used in analysis
        CFG = get_CFG(reportyear=2023,
                    year=2021,
                    model_dir=f"/lustre/storeB/project/fou/kl/emep/ModelRuns/2023_REPORTING/TRENDS/pyaerocom_trends/")


        CFG.update(dict(
            proj_id="emep",
            exp_id=f"2023-trends",
            # exp_name="Evaluation of EMEP runs for 2023 EMEP reporting",
            exp_descr=(
                f"Evaluation of EMEP runs for 2023 EMEP reporting trend runs. 7 year obs-data availability per period. /lustre/storeB/project/fou/kl/emep/ModelRuns/2023_REPORTING/TRENDS/pyaerocom_trends is compared against observations fro
        m EBAS."
            ),
            periods=["1990-2021", "1990-1999", "2000-2009", "2010-2019", "2012-2021"], #range(1990,2022)],
            # exp_pi="S. Tsyro, H. Klein",
            add_model_maps=False,
            #only_model_maps=True,
            # trend parameters
            freqs=["yearly", "monthly"], # "weekly"],"daily"], # can't be hourly for trends, daily is too slow weekly hardly ever needed
            main_freq="monthly",
            add_trends=True,
            avg_over_trends=True,
            obs_min_yrs=7, # kun stasjoner med minst 14yr
            stats_min_yrs=7, # kun stasjoner med minst 14yr
            sequential_yrs=False,
        ))


        # remove "no, pm10, pm25" from EBAS-hourly
        CFG["obs_cfg"]["EBAS-h-diurnal"]["obs_vars"].remove("concNno")
        CFG["obs_cfg"]["EBAS-h-diurnal"]["obs_vars"].remove("concpm10")
        CFG["obs_cfg"]["EBAS-h-diurnal"]["obs_vars"].remove("concpm25")


        # remove EEA
        for obs in list(CFG["obs_cfg"].keys()):
            if obs.startswith("EEA"):
                del CFG["obs_cfg"][obs]

        # remove all hourly obs, f.e. for trends
        for obs in list(CFG["obs_cfg"].keys()):
            if "ts_type" in CFG["obs_cfg"][obs] and CFG["obs_cfg"][obs]["ts_type"] == "hourly":
                del CFG["obs_cfg"][obs]
                print(f"removed hourly {obs}")

        # remove all daily obs, f.e. for trends
        for obs in list(CFG["obs_cfg"].keys()):
            if "ts_type" in CFG["obs_cfg"][obs] and CFG["obs_cfg"][obs]["ts_type"] == "daily":
                del CFG["obs_cfg"][obs]
                print(f"removed daily {obs}")


        # remove "concCocpm10", not in model-output
        for obs in CFG["obs_cfg"]:
            if "concCocpm10" in CFG["obs_cfg"][obs]["obs_vars"]:
                CFG["obs_cfg"][obs]["obs_vars"].remove("concCocpm10")

                # try to run anything, but don't fail on error
        # CFG["raise_exceptions"] = False


        stp = EvalSetup(**CFG)

        cdir = "./cache"
        os.makedirs(cdir, exist_ok=True)
        const.CACHEDIR = cdir

        ana = ExperimentProcessor(stp)
        ana.update_interface()

        # run everything
        res = ana.run()

    :returns: a dict of a model configuration usable for EvalSetup
    """

    CFG = dict(
        json_basedir=os.path.abspath("/home/jang/data/aeroval-local-web/data"),
        coldata_basedir=os.path.abspath("/home/jang/data/aeroval-local-web/coldata"),
        # io_aux_file=os.path.abspath("./gridded_io_aux.py"), not needed for ReadMscwCtm
        var_scale_colmap_file=os.path.abspath(
            "/home/jang/data/aeroval-local-web/user_var_scale_colmap.ini"
        ),
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
        periods=[f"{anayear}"],
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
        proj_id="CAMEO",
        exp_id=f"CAMEO-{anayear}-reporting",
        exp_name=f"Evaluation of EMEP runs for {anayear} for the CAMEO project",
        exp_descr=(
            f"Evaluation of EMEP runs for {anayear} CAMEO. The EMEP model, is compared against observations from EBAS."
        ),
        exp_pi="jan.griesfeller@met.no",
        public=True,
        # directory where colocated data files are supposed to be stored
        weighted_stats=True,
        var_order_menu=[
            "concno2",
            "vmro3max",
            "vmro3",
            "conco3",
            "vmrox",
            "concso2",
            "vmrco",
            "vmrno",
            "vmrno2",
            "vmrso2",
            "concCoc25",
            "concom25",
            "concpm25",
            "concpm10",
            "concso4",
            "concNtno3",
            "concNtnh",
            "concNnh3",
            "concNnh4",
            "concNhno3",
            "concNno3pm25",
            "concNno3pm10",
            "concsspm25",
            "concsspm10",
            "concCecpm25",
            "concCocpm25",
            "wetoxs",
            "wetrdn",
            "wetoxn",
            "pr",
            "drysox",
            "dryrdn",
            "dryoxn",
            "dryo3",
            "dryvelo3",
            "proxydryoxs",
            "proxydryoxn",
            "proxydryrdn",
            "proxydryo3",
            "proxydrypm10",
            "proxydrypm25",
            "proxydryno2",
            "proxydryno2no2",
            "proxydryhono",
            "proxydryn2o5",
            "proxydryhno3",
            "proxydryno3c",
            "proxydryno3f",
            "proxydrynh3",
            "proxydrynh4",
            "proxydryso2",
            "proxydryso4",
            "proxywetoxs",
            "proxywetoxn",
            "proxywetrdn",
            "proxyweto3",
            "proxywetpm10",
            "proxywetpm25",
            "proxywethno3",
            "proxywethono",
            "proxywetn2o5",
            "proxywetno2no2",
            "proxywetnh3",
            "proxywetnh4",
            "proxywetno2",
            "proxywetso2",
            "proxywetso4",
            "proxywetno3c",
            "proxywetno3f",
            "depoxs",
            "deprdn",
            "depoxn",
            "depoxsf",
            "depoxnf",
            "deprdnf",
        ],
    )

    CFG["model_cfg"] = {
        "EMEP": dict(
            model_id="EMEP.cameo",
            # model_data_dir=model_dir,
            # gridded_reader_id={"model": "ReadMscwCtm"},
            model_read_aux={},
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

    # AERONET_FILTER = {
    #     **BASE_FILTER,  # Forandring fra Daniel
    #     "altitude": [-20, 1000],
    # }

    OC_EC_RESAMPLE_CONSTRAINTS = dict(
        yearly=dict(monthly=4),
        monthly=dict(daily=4, weekly=1),
        daily=dict(hourly=18),
        hourly=dict(minutely=45),
    )

    RESAMPLE_CONSTRAINTS_LESS_STRICT = dict(
        yearly=dict(monthly=9),
        monthly=dict(daily=4, weekly=1),
        daily=dict(hourly=18),
        hourly=dict(minutely=45),
    )

    # Station filters

    eea_species = [
        "concpm10",
        "concpm25",
        "concSso2",
        "concNno2",
        "concNno",
        "vmro3max",
        "vmro3",
        "concNno2",
        "vmrox",
        "concno2",
    ]

    ebas_species = [
        "concNhno3",
        "concNtno3",
        "concNtnh",
        "concNnh3",
        "concnh4",
        "prmm",
        "concpm10",
        "concpm25",
        "concSso2",
        "concNno2",
        "vmrco",
        "vmro3max",
        "vmro3",
        "concNno",
        "concCecpm25",
        "concCocpm25",
        "concCecpm10",
        "concCocpm10",
        #        "concnh4pm10", # no output in the model
        "concnh4pm25",
        #        "concso4pm10", # no output in the model
        "concso4pm25",
        "concno3pm10",
        "concno3pm25",
        "concsspm10",
        "concsspm25",
        "concso4t",
        "concso4c",
        "wetoxs",
        "wetoxn",
        "wetrdn",
        "vmrox",
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

    EBAS_FILTER = {
        key: dict(
            **EBAS_FILTER,
            station_id=_get_ignore_stations(key, anayear) + height_ignore_ebas,
            negate="station_id",
        )
        for key in ebas_species
    }

    EEA_FILTER = {
        key: dict(
            **EEA_FILTER,
            station_name=height_ignore_eea,
            negate="station_name",
        )
        for key in eea_species
    }

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
        ### HOURLY
        "EBAS-gases-h": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-h",
            ts_type="hourly",
            obs_vars=[
                "vmro3",
                "vmrno2",
                "vmrno",
                "vmrso2",
            ],
            obs_vert_type="Surface",
            colocate_time=True,
            obs_filters=EBAS_FILTER,
        ),
        ### DAILY
        # Gases
        "EBAS-gases-d": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-d",
            ts_type="daily",
            obs_vars=[
                # "vmrhno3",
                # "vmrhcho",
                "vmro3max",
                # "vmrc2h6",
                # "vmrc2h4",
                # "vmrisop",
                # "vmrtp",
                # "concno3",
                "concNhno3",
                "concNnh3",
                "vmro3",
                "vmrno2",
                "vmrno",
                "vmrso2",
            ],
            obs_vert_type="Surface",
            colocate_time=True,
            obs_filters=EBAS_FILTER,
        ),
        # PM
        "EBAS-pm-d": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-d",
            ts_type="daily",
            obs_vars=[
                "concpm25",
                "concpm10",
                "concso4",
                # "vmrc2h4",
                "concsspm25",
                "concsspm10",
                "concNno3pm10",
                "concNno3pm25",
                "concNtno3",
                "concNnh4",
                "concNtnh",
            ],
            obs_vert_type="Surface",
            colocate_time=True,
            obs_filters=EBAS_FILTER,
        ),
        # OC
        "EBAS-oc-d": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-d",
            ts_type="daily",
            obs_vars=[
                "concCoc25",
                "concom25",
            ],
            obs_vert_type="Surface",
            colocate_time=True,
            obs_filters=EBAS_FILTER,
            min_num_obs=OC_EC_RESAMPLE_CONSTRAINTS,
        ),
        ### MONTHLY
        # Gases
        "EBAS-gases-m": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-m",
            ts_type="monthly",
            obs_vars=[
                # "vmrhcho",
                "vmro3max",
                # "vmrc2h6",
                # "vmrc2h4",
                # "vmrisop",
                # "vmrtp",
                "concNhno3",
                "concNnh3",
            ],
            obs_vert_type="Surface",
            colocate_time=True,
            obs_filters=EBAS_FILTER,
        ),
        # PM
        "EBAS-pm-m": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-m",
            ts_type="monthly",
            obs_vars=[
                "concpm25",
                "concpm10",
                "concso4",
                # "vmrc2h4",
                "concsspm25",
                "concsspm10",
                "concNno3pm10",
                "concNno3pm25",
                "concNtno3",
                "concNnh4",
                "concNtnh",
            ],
            obs_vert_type="Surface",
            colocate_time=True,
            obs_filters=EBAS_FILTER,
        ),
        # OC
        "EBAS-oc-m": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-m",
            ts_type="monthly",
            obs_vars=[
                "concCoc25",
                "concom25",
            ],
            obs_vert_type="Surface",
            colocate_time=True,
            obs_filters=EBAS_FILTER,
            min_num_obs=OC_EC_RESAMPLE_CONSTRAINTS,
        ),
        ##################
        #    EBAS Less Strict
        ##################
        ### HOURLY
        "EBAS-gases-LS-h": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-Less-Strict-h",
            ts_type="hourly",
            obs_vars=[
                "vmro3",
                "vmrno2",
                "vmrno",
                "vmrso2",
            ],
            obs_vert_type="Surface",
            colocate_time=True,
            obs_filters=EBAS_FILTER,
            min_num_obs=RESAMPLE_CONSTRAINTS_LESS_STRICT,
        ),
        ### DAILY
        # Gases
        "EBAS-gases-LS-d": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-Less-Strict-d",
            ts_type="daily",
            obs_vars=[
                # "vmrhno3",
                "vmro3max",
                # "vmrhcho",
                # "vmrc2h6",
                # "vmrc2h4",
                # "vmrisop",
                # "vmrtp",
                # "concno3",
                "concNhno3",
                "concNnh3",
                "vmro3",
                "vmrno2",
                "vmrno",
                "vmrso2",
            ],
            obs_vert_type="Surface",
            colocate_time=True,
            obs_filters=EBAS_FILTER,
            min_num_obs=RESAMPLE_CONSTRAINTS_LESS_STRICT,
        ),
        # PM
        "EBAS-pm-LS-d": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-Less-Strict-d",
            ts_type="daily",
            obs_vars=[
                "concpm25",
                "concpm10",
                "concso4",
                # "vmrc2h4",
                "concsspm25",
                "concsspm10",
                "concNno3pm10",
                "concNno3pm25",
                "concNtno3",
                "concNnh4",
                "concNtnh",
            ],
            obs_vert_type="Surface",
            colocate_time=True,
            obs_filters=EBAS_FILTER,
            min_num_obs=RESAMPLE_CONSTRAINTS_LESS_STRICT,
        ),
        ### MONTHLY
        # Gases
        "EBAS-gases-LS-m": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-Less-Strict-m",
            ts_type="monthly",
            obs_vars=[
                "vmro3max",
                # "vmrhcho",
                # "vmrc2h6",
                # "vmrc2h4",
                # "vmrisop",
                # "vmrtp",
                "concNhno3",
                "concNnh3",
            ],
            obs_vert_type="Surface",
            colocate_time=True,
            obs_filters=EBAS_FILTER,
            min_num_obs=RESAMPLE_CONSTRAINTS_LESS_STRICT,
        ),
        # PM
        "EBAS-pm-LS-m": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-Less-Strict-m",
            ts_type="monthly",
            obs_vars=[
                "concpm25",
                "concpm10",
                "concso4",
                # "vmrc2h4",
                "concsspm25",
                "concsspm10",
                "concNno3pm10",
                "concNno3pm25",
                "concNtno3",
                "concNnh4",
                "concNtnh",
            ],
            obs_vert_type="Surface",
            colocate_time=True,
            obs_filters=EBAS_FILTER,
            min_num_obs=RESAMPLE_CONSTRAINTS_LESS_STRICT,
        ),
    }
    # Setup for supported satellite evaluations
    OBS_SAT = {}

    OBS_CFG = {**OBS_GROUNDBASED, **OBS_SAT}

    CFG["obs_cfg"] = OBS_CFG

    return copy.deepcopy(CFG)
