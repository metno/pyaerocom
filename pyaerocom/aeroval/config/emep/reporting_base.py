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
        PLTTYPES = CFG["plot_types"]["EMEP"]
        for mid, fpath in dir_versions.items():
            CFG["model_cfg"][mid] = MODEL.copy()
            CFG["plot_types"][mid] = PLTTYPES.copy()
            CFG["model_cfg"][mid]["model_data_dir"] = fpath
            CFG["model_cfg"][mid]["model_id"] = mid
        del CFG["model_cfg"]["EMEP"]
        del CFG["plot_types"]["EMEP"]

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
        boundaries={
            "west": -30,
            "east": 90,
            "north": 82,
            "south": 30,
        },
        maps_freq="yearly",
        plot_types={"EMEP": ["contour", "overlay"]},
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

    # This list of stations was generated using the script found here:
    # https://gist.github.com/thorbjoernl/b7946882f1696722742053406d056e12.
    # It excludes stations with a relative altitude (Elevation difference to the lowest
    # altitude in a 5km radius based on gtopo30) above 500m as well as stations that do not include
    # an altitude in the ebas file index.
    # Last updated: ~2025-01-03
    height_ignore_ebas = [
        "AM0001R",
        "AR0001R",
        "AT0033R",
        "AT0034G",
        "AT0037R",
        "AT0038R",
        "AT0040R",
        "AT0048R",
        "AT0049R",
        "BG0001R",
        "BG0053R",
        "BO0001R",
        "CA0100R",
        "CA0103R",
        "CH0001G",
        "CH0004R",
        "CH0005R",
        "CL0001R",
        "CN1003R",
        "DE0003R",
        "DE0005R",
        "DE0054R",
        "DE0057G",
        "DE0060G",
        "DE0075R",
        "DZ0001G",
        "ES0005R",
        "ES0018G",
        "ES0022R",
        "ES0025U",
        "FI0009R",
        "FR0012R",
        "FR0019R",
        "FR0026R",
        "FR0030R",
        "FR0031R",
        "FR0033R",
        "GB0035R",
        "GB0059G",
        "GR0003R",
        "GR0101R",
        "HR0002R",
        "HR0004R",
        "IT0002R",
        "IT0003R",
        "IT0005R",
        "IT0009R",
        "IT0019R",
        "IT0031U",
        "JP1021R",
        "KE0001G",
        "MK0007R",
        "MX0001R",
        "MY1030R",
        "NO0036R",
        "PL0003R",
        "PL0011R",
        "PT0005R",
        "PT0007R",
        "RO0001R",
        "RO0002R",
        "RO0003R",
        "RO0004R",
        "RO0005R",
        "RS0005R",
        "RU1038R",
        "SI0032R",
        "SK0002R",
        "TW0100R",
        "US0012R",
        "US0013R",
        "US0015R",
        "US0016R",
        "US0024R",
        "US0030R",
        "US0032R",
        "US0053R",
        "US0054R",
        "US0055R",
        "US0073R",
        "US0077R",
        "US0082R",
        "US0131R",
        "US0142R",
        "US0204R",
        "US0602R",
        "US1200R",
        "US4828R",
        "US9002R",
        "US9005R",
        "US9020R",
        "US9024R",
        "US9026R",
        "US9029R",
        "US9041R",
        "US9042R",
        "US9046R",
        "US9048R",
        "US9050R",
        "US9056R",
        "US9064R",
        "US9065R",
        "US9070R",
        "US9071R",
        "US9078R",
        "US9082U",
        "VN0001R",
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
        **BASE_FILTER,
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
            obs_id="EEA-d-rural",
            obs_vars=[
                "concpm10",
                "concpm25",
                "concSso2",
                "concNno2",
                "concNno",
                "vmro3max",
            ],
            pyaro_config={
                "name": "EEA-d-rural",
                "reader_id": "eeareader",
                "filename_or_obj_or_url": "/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/EEA-AQDS/download",
                "name_map": {
                    "PM2.5": "concpm25",
                    "PM10": "concpm10",
                    "NO": "concno",
                    "NO2": "concno2",
                    "SO2": "concso2",
                    "O3": "conco3",
                },
                "filters": {
                    "time_bounds": {
                        "startend_include": [
                            (f"{year}-01-01 00:00:00", f"{year + 1}-01-01 00:00:00")
                        ],
                    },
                    "valleyfloor_relaltitude": {
                        "topo": "/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/GTOPO30/merged",
                        "radius": 5000,
                        "topo_var": "Band1",
                        "lower": None,
                        "upper": 500,
                    },
                },
                "post_processing": [
                    "concNno_from_concno",
                    "concNno2_from_concno2",
                    "concSso2_from_concso2",
                    "vmro3max_from_conco3",
                ],
                "dataset": "verified",
                "station_area": [
                    "rural",
                    "rural-regional",
                    "rural-nearcity",
                    "rural-remote",
                ],
                "station_type": [
                    "background",
                ],
            },
            web_interface_name="EEA-rural",
            obs_vert_type="Surface",
            obs_filters=EEA_FILTER,
            ts_type="daily",
        ),
        "EEA-h-diurnal-rural": dict(
            obs_id="EEA-h-diurnal-rural",
            obs_vars=[
                "concNno2",
                "vmro3",
                "vmrox",
            ],
            pyaro_config={
                "name": "EEA-h-diurnal-rural",
                "reader_id": "eeareader",
                "filename_or_obj_or_url": "/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/EEA-AQDS/download",
                "name_map": {
                    "PM2.5": "concpm25",
                    "PM10": "concpm10",
                    "NO": "concno",
                    "NO2": "concno2",
                    "SO2": "concso2",
                    "O3": "conco3",
                },
                "filters": {
                    "time_bounds": {
                        "startend_include": [
                            (f"{year}-01-01 00:00:00", f"{year + 1}-01-01 00:00:00")
                        ],
                    },
                    "valleyfloor_relaltitude": {
                        "topo": "/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/GTOPO30/merged",
                        "radius": 5000,
                        "topo_var": "Band1",
                        "lower": None,
                        "upper": 500,
                    },
                },
                "post_processing": [
                    "concNno2_from_concno2",
                    "vmro3_from_conco3",
                    "vmrno2_from_concno2",
                    "vmrox_from_vmrno2_vmro3",
                ],
                "dataset": "verified",
                "station_area": [
                    "rural",
                    "rural-regional",
                    "rural-nearcity",
                    "rural-remote",
                ],
                "station_type": [
                    "background",
                ],
            },
            web_interface_name="EEA-h-rural",
            obs_vert_type="Surface",
            obs_filters={**EEA_FILTER, "ts_type": "hourly"},
            resample_how="mean",
            ts_type="hourly",
        ),
        ################
        #    EEA-all
        ################
        "EEA-d-all": dict(
            obs_id="EEA-d-all",
            obs_vars=[
                "concpm10",
                "concpm25",
                "concSso2",
                "concNno2",
                "concNno",
                "vmro3max",
            ],
            pyaro_config={
                "name": "EEA-d-all",
                "reader_id": "eeareader",
                "filename_or_obj_or_url": "/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/EEA-AQDS/download",
                "name_map": {
                    "PM2.5": "concpm25",
                    "PM10": "concpm10",
                    "NO": "concno",
                    "NO2": "concno2",
                    "SO2": "concso2",
                    "O3": "conco3",
                },
                "filters": {
                    "time_bounds": {
                        "startend_include": [
                            (f"{year}-01-01 00:00:00", f"{year + 1}-01-01 00:00:00")
                        ],
                    },
                    "valleyfloor_relaltitude": {
                        "topo": "/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/GTOPO30/merged",
                        "radius": 5000,
                        "topo_var": "Band1",
                        "lower": None,
                        "upper": 500,
                    },
                },
                "post_processing": [
                    "concNno_from_concno",
                    "concNno2_from_concno2",
                    "concSso2_from_concso2",
                    "vmro3max_from_conco3",
                ],
                "dataset": "verified",
            },
            web_interface_name="EEA-all",
            obs_vert_type="Surface",
            obs_filters=EEA_FILTER,
            ts_type="daily",
        ),
        "EEA-h-diurnal-all": dict(
            obs_id="EEA-h-diurnal-all",
            obs_vars=[
                "concNno2",
                "vmro3",
                "vmrox",
            ],
            pyaro_config={
                "name": "EEA-h-diurnal-all",
                "reader_id": "eeareader",
                "filename_or_obj_or_url": "/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/EEA-AQDS/download",
                "name_map": {
                    "PM2.5": "concpm25",
                    "PM10": "concpm10",
                    "NO": "concno",
                    "NO2": "concno2",
                    "SO2": "concso2",
                    "O3": "conco3",
                },
                "filters": {
                    "time_bounds": {
                        "startend_include": [
                            (f"{year}-01-01 00:00:00", f"{year + 1}-01-01 00:00:00")
                        ],
                    },
                    "valleyfloor_relaltitude": {
                        "topo": "/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/GTOPO30/merged",
                        "radius": 5000,
                        "topo_var": "Band1",
                        "lower": None,
                        "upper": 500,
                    },
                },
                "post_processing": [
                    "concNno2_from_concno2",
                    "vmro3_from_conco3",
                    "vmrno2_from_concno2",
                    "vmrox_from_vmrno2_vmro3",
                ],
                "dataset": "verified",
            },
            web_interface_name="EEA-h-all",
            obs_vert_type="Surface",
            obs_filters={**EEA_FILTER, "ts_type": "hourly"},
            resample_how="mean",
            ts_type="hourly",
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
