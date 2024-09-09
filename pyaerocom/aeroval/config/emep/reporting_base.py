"""
Global config for emep reporting pyaeroval runs
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


def get_CFG(reportyear, year, model_dir) -> dict:
    """Get a configuration usable for emep reporting

    :param reportyear: year of reporting
    :param year: year of data
    :param model_dir: directory containing Base_hour.nc,Base_day.nc,Base_month.nc and Base_fullrun.nc
        or for trends directory containing years like 2005,2010,2015 again containing above files

    The current working directory of the experiment should have the following files/directories by default:
        - `data` output directory
        - `coldata` output directory
        - `user_var_scale_colmap.ini` optional user-defined colormaps for pyaerocom variables
        - `omit_stations.yaml` optional user-defined yaml file of stations to omit

    The default values can be changed in your program. If you want to permanently change the defaults,
    please agree upon these changes with the emep-modellers and contact the pyaerocom-developers.

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
        json_basedir=os.path.abspath("./data"),
        coldata_basedir=os.path.abspath("./coldata"),
        # io_aux_file=os.path.abspath("./gridded_io_aux.py"), not needed for ReadMscwCtm
        var_scale_colmap_file=os.path.abspath("./user_var_scale_colmap.ini"),
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
            "concno3pm1",
            "concnh4pm25",
            "concnh4pm1",
            "concso4pm25",
            "concso4pm1",
            "concCecpm10",
            "concCecpm25",
            "concCocpm10",  # SURF_ugC_PM_OMCOARSE missing in model-output
            "concCocpm25",
            "concom1",
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
        "EMEP": dict(
            model_id="EMEP",
            model_data_dir=model_dir,
            gridded_reader_id={"model": "ReadMscwCtm"},
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

    AERONET_FILTER = {
        **BASE_FILTER,  # Forandring fra Daniel
        "altitude": [-20, 1000],
    }

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
        "concom1",
        "concCecpm10",
        "concCocpm10",
        #        "concnh4pm10", # no output in the model
        "concnh4pm25",
        "concnh4pm1",
        #        "concso4pm10", # no output in the model
        "concso4pm25",
        "concso4pm1",
        "concno3pm10",
        "concno3pm25",
        "concno3pm1",
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
            station_id=_get_ignore_stations(key, year) + height_ignore_ebas,
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
        "EBAS-m-tc": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-m",
            obs_vars=[
                "concNhno3",
                "concNtno3",
                "concNtnh",
                "concNnh3",
                "concnh4",
                # "prmm",
                "concpm10",
                "concpm25",
                "concSso2",
                "concNno2",
                "vmrco",
                "vmro3max",
                "vmro3",
                "concNno",
                "concso4t",
                "concso4c",
            ],
            obs_vert_type="Surface",
            colocate_time=True,
            ts_type="monthly",
            obs_filters=EBAS_FILTER,
        ),
        "EBAS-d-tc": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-d",
            obs_vars=[
                "concNhno3",
                "concNtno3",
                "concNtnh",
                "concNnh3",
                "concnh4",
                "concpm10",
                "concpm25",
                "concSso2",
                "concNno2",
                "vmrco",
                "vmro3max",
                "vmro3",
                "concNno",
                "concso4t",
                "concso4c",
            ],
            obs_vert_type="Surface",
            colocate_time=True,
            min_num_obs=DEFAULT_RESAMPLE_CONSTRAINTS,
            ts_type="daily",
            obs_filters=EBAS_FILTER,
        ),
        "EBAS-m-tc-ecoc": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-m",
            obs_vars=[
                "concCecpm25",
                "concCocpm25",
                "concom1",
                "concCecpm10",
                "concCocpm10",
                #                "concnh4pm10",
                "concnh4pm25",
                "concnh4pm1",
                #                "concso4pm10",
                "concso4pm25",
                "concso4pm1",
                "concno3pm10",
                "concno3pm25",
                "concno3pm1",
                "concsspm10",
                "concsspm25",
            ],
            obs_vert_type="Surface",
            colocate_time=True,
            ts_type="monthly",
            min_num_obs=OC_EC_RESAMPLE_CONSTRAINTS,
            obs_filters=EBAS_FILTER,
        ),
        "EBAS-d-tc-ecoc": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-d",
            obs_vars=[
                "concCecpm25",
                "concCocpm25",
                "concom1",
                "concCecpm10",
                "concCocpm10",
                # "concnh4pm10",
                "concnh4pm25",
                "concnh4pm1",
                #                "concso4pm10",
                "concso4pm25",
                "concso4pm1",
                "concno3pm10",
                "concno3pm25",
                "concno3pm1",
                "concsspm10",
                "concsspm25",
            ],
            obs_vert_type="Surface",
            colocate_time=True,
            ts_type="daily",
            min_num_obs=OC_EC_RESAMPLE_CONSTRAINTS,
            obs_filters=EBAS_FILTER,
        ),
        # Diurnal
        "EBAS-h-diurnal": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-h",
            obs_vars=[
                "concNno2",
                "concNno",
                "vmro3",
                "concpm10",
                "concpm25",
            ],
            obs_vert_type="Surface",
            ts_type="hourly",
            # diurnal_only=True,
            resample_how="mean",
            obs_filters={**EBAS_FILTER, "ts_type": "hourly"},
        ),
        # OX
        "EBAS-d-ox": dict(
            obs_id="EBAS-ox",
            obs_vars=["vmrox"],
            obs_type="ungridded",
            obs_vert_type="Surface",
            web_interface_name="EBAS",
            ts_type="daily",
            obs_merge_how={
                "vmrox": "eval",
            },
            obs_aux_requires={
                "vmrox": {
                    "EBASMC": [
                        "vmro3",
                        "vmrno2",
                    ],
                }
            },
            obs_aux_funs={
                "vmrox":
                # variables used in computation method need to be based on AeroCom
                # units, since the colocated StationData objects (from which the
                # new UngriddedData is computed, will perform AeroCom unit check
                # and conversion)
                "(EBASMC;vmro3+EBASMC;vmrno2)"
            },
            obs_aux_units={"vmrox": "nmol mol-1"},
            min_num_obs=DEFAULT_RESAMPLE_CONSTRAINTS,
            obs_filters=EBAS_FILTER,
        ),
        "EBAS-h-ox-diurnal": dict(
            obs_id="EBAS-ox-diurnal",
            obs_vars=["vmrox"],
            obs_type="ungridded",
            obs_vert_type="Surface",
            web_interface_name="EBAS-h",
            ts_type="hourly",
            # diurnal_only=True,
            obs_merge_how={
                "vmrox": "eval",
            },
            obs_aux_requires={
                "vmrox": {
                    "EBASMC": ["vmro3", "vmrno2"],
                }
            },
            obs_aux_funs={
                "vmrox":
                # variables used in computation method need to be based on AeroCom
                # units, since the colocated StationData objects (from which the
                # new UngriddedData is computed, will perform AeroCom unit check
                # and conversion)
                "(EBASMC;vmro3+EBASMC;vmrno2)"
            },
            obs_aux_units={"vmrox": "nmol mol-1"},
            obs_filters={**EBAS_FILTER, "ts_type": "hourly"},
        ),
        # Wet Dep
        "EBAS-d-wet": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-d",
            ts_type="daily",
            obs_remove_outliers=True,
            obs_vars=[
                "wetoxs",
                "wetoxn",
                "wetrdn",
                "prmm",
            ],
            obs_vert_type="Surface",
            min_num_obs=DEFAULT_RESAMPLE_CONSTRAINTS,
            colocate_time=True,
            obs_filters=EBAS_FILTER,
        ),
        "EBAS-m-wet": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-m",
            ts_type="monthly",
            obs_remove_outliers=True,
            colocate_time=True,
            obs_vars=[
                "wetoxs",
                "wetoxn",
                "wetrdn",
                "prmm",
            ],
            obs_vert_type="Surface",
            obs_filters=EBAS_FILTER,
        ),
        ################
        #    EEA-rural
        ################
        "EEA-d-rural": dict(
            obs_id="EEAAQeRep.v2",
            obs_vars=[
                "concpm10",
                "concpm25",
                "concSso2",
                "concNno2",
                "vmro3max",
                # "concno2",
            ],
            web_interface_name="EEA-rural",
            obs_vert_type="Surface",
            obs_filters=EEA_FILTER,
        ),
        "EEA-d-rural-no": dict(
            obs_id="EEAAQeRep.v2",
            obs_vars=[
                "concNno",
            ],
            web_interface_name="EEA-rural",
            obs_vert_type="Surface",
            obs_filters=EEA_FILTER,
        ),
        "EEA-h-diurnal-rural": dict(
            obs_id="EEAAQeRep.v2",
            obs_vars=["vmro3", "concNno2"],
            obs_vert_type="Surface",
            web_interface_name="EEA-h-rural",
            ts_type="hourly",
            # diurnal_only=True,
            harmonise_units=False,
            resample_how="mean",
            obs_filters={**EEA_FILTER, "ts_type": "hourly"},
        ),
        "EEA-d-ox-rural": dict(
            obs_id="EEA-ox-rural",
            obs_vars=["vmrox"],
            obs_type="ungridded",
            obs_vert_type="Surface",
            web_interface_name="EEA-rural",
            ts_type="daily",
            # min_num_obs=None,
            obs_merge_how={
                "vmrox": "eval",
            },
            obs_aux_requires={
                "vmrox": {
                    "EEAAQeRep.v2": ["vmro3", "vmrno2"],
                }
            },
            obs_aux_funs={
                "vmrox":
                # variables used in computation method need to be based on AeroCom
                # units, since the colocated StationData objects (from which the
                # new UngriddedData is computed, will perform AeroCom unit check
                # and conversion)
                "(EEAAQeRep.v2;vmro3+EEAAQeRep.v2;vmrno2)"
            },
            obs_aux_units={"vmrox": "nmol mol-1"},
            obs_filters={**EEA_FILTER},
        ),
        "EEA-h-ox-rural-diu": dict(
            obs_id="EEA-ox-rural-diu",
            obs_vars=["vmrox"],
            obs_type="ungridded",
            obs_vert_type="Surface",
            web_interface_name="EEA-h-rural",
            ts_type="hourly",
            # diurnal_only=True,
            obs_merge_how={
                "vmrox": "eval",
            },
            obs_aux_requires={
                "vmrox": {
                    "EEAAQeRep.v2": ["vmro3", "vmrno2"],
                }
            },
            obs_aux_funs={
                "vmrox":
                # variables used in computation method need to be based on AeroCom
                # units, since the colocated StationData objects (from which the
                # new UngriddedData is computed, will perform AeroCom unit check
                # and conversion)
                "(EEAAQeRep.v2;vmro3+EEAAQeRep.v2;vmrno2)"
            },
            obs_aux_units={"vmrox": "nmol mol-1"},
            obs_filters={**EEA_FILTER, "ts_type": "hourly"},
        ),
        ################
        #    EEA-all
        ################
        "EEA-d-all": dict(
            obs_id="EEAAQeRep.v2",
            obs_vars=[
                "concpm10",
                "concpm25",
                "concSso2",
                "concNno2",
                "vmro3max",
                # "concno2",
            ],
            web_interface_name="EEA-all",
            obs_vert_type="Surface",
            obs_filters=EEA_FILTER_ALL,
        ),
        "EEA-d-all-no": dict(
            obs_id="EEAAQeRep.v2",
            obs_vars=[
                "concNno",
            ],
            web_interface_name="EEA-all",
            obs_vert_type="Surface",
            obs_filters=EEA_FILTER_ALL,
        ),
        "EEA-h-diurnal-all": dict(
            obs_id="EEAAQeRep.v2",
            obs_vars=["vmro3", "concNno2"],
            obs_vert_type="Surface",
            web_interface_name="EEA-h-all",
            ts_type="hourly",
            # diurnal_only=True,
            harmonise_units=False,
            resample_how="mean",
            obs_filters={**EEA_FILTER_ALL, "ts_type": "hourly"},
        ),
        "EEA-d-ox-all": dict(
            obs_id="EEA-ox-all",
            obs_vars=["vmrox"],
            obs_type="ungridded",
            obs_vert_type="Surface",
            web_interface_name="EEA-all",
            ts_type="daily",
            # min_num_obs=None,
            obs_merge_how={
                "vmrox": "eval",
            },
            obs_aux_requires={
                "vmrox": {
                    "EEAAQeRep.v2": ["vmro3", "vmrno2"],
                }
            },
            obs_aux_funs={
                "vmrox":
                # variables used in computation method need to be based on AeroCom
                # units, since the colocated StationData objects (from which the
                # new UngriddedData is computed, will perform AeroCom unit check
                # and conversion)
                "(EEAAQeRep.v2;vmro3+EEAAQeRep.v2;vmrno2)"
            },
            obs_aux_units={"vmrox": "nmol mol-1"},
            obs_filters={**EEA_FILTER_ALL},
        ),
        "EEA-h-ox-all-diu": dict(
            obs_id="EEA-ox-all-diu",
            obs_vars=["vmrox"],
            obs_type="ungridded",
            obs_vert_type="Surface",
            web_interface_name="EEA-h-all",
            ts_type="hourly",
            # diurnal_only=True,
            obs_merge_how={
                "vmrox": "eval",
            },
            obs_aux_requires={
                "vmrox": {
                    "EEAAQeRep.v2": ["vmro3", "vmrno2"],
                }
            },
            obs_aux_funs={
                "vmrox":
                # variables used in computation method need to be based on AeroCom
                # units, since the colocated StationData objects (from which the
                # new UngriddedData is computed, will perform AeroCom unit check
                # and conversion)
                "(EEAAQeRep.v2;vmro3+EEAAQeRep.v2;vmrno2)"
            },
            obs_aux_units={"vmrox": "nmol mol-1"},
            obs_filters={**EEA_FILTER_ALL, "ts_type": "hourly"},
        ),
        ##################
        #    AERONET
        ##################
        "AERONET": dict(
            obs_id="AeronetSunV3Lev1.5.daily",
            obs_vars=["od550aer"],
            web_interface_name="AERONET",
            obs_vert_type="Column",
            ignore_station_names="DRAGON*",
            ts_type="daily",
            colocate_time=True,
            min_num_obs=dict(
                yearly=dict(
                    daily=90,
                ),
                monthly=dict(
                    weekly=1,
                ),
            ),
            obs_filters=AERONET_FILTER,
        ),
    }

    # Setup for supported satellite evaluations
    OBS_SAT = {}

    OBS_CFG = {**OBS_GROUNDBASED, **OBS_SAT}

    CFG["obs_cfg"] = OBS_CFG

    return copy.deepcopy(CFG)
