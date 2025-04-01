"""
Global config for emep reporting pyaeroval runs
"""

import pathlib

import copy
import functools
import logging
import os
from typing import SupportsInt

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
    omit_file = pathlib.Path(__file__).parent / "omit_stations_actris_ebas.yaml"
    if omit_file.exists():
        logger.info(f"reading omit_stations_actris_ebas.yaml from {omit_file}")
        with open(omit_file) as fh:
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


def _get_ignore_stations(specy, year: SupportsInt) -> list[str]:
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


def get_actrisebase_CFG(reportyear, year, model_dir) -> dict:
    """Get a configuration usable for emep reporting

    :param reportyear: year of reporting
    :param year: year of data
    :param model_dir: directory containing Base_hour.nc,Base_day.nc,Base_month.nc and Base_fullrun.nc
        or for trends directory containing years like 2005,2010,2015 again containing above files


    :returns: a dict of a model configuration usable for EvalSetup
    """

    ebas_test_vars = [
        # "concso4t",
        # "wetoxs",
        "prmm",
        "concso4c",
        "vmro3",
    ]
    # Will be used later
    ebas_test_vars_diurnal = [
        "vmro3",
    ]

    CFG = dict(
        json_basedir=os.path.abspath("./data"),
        coldata_basedir=os.path.abspath("./coldata"),
        # io_aux_file=os.path.abspath("./gridded_io_aux.py"), not needed for ReadMscwCtm
        # var_scale_colmap_file=os.path.abspath("./user_var_scale_colmap.ini"),
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
            "wetso4",
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

    OBS_GROUNDBASED = {
        # actrisebas
        "ACTRIS-EBAS-h-diurnal": dict(
            obs_id="ACTRIS-EBAS-h-diurnal",
            web_interface_name="ACTRIS-EBAS-h",
            obs_vars=ebas_test_vars_diurnal,
            obs_vert_type="Surface",
            # colocate_time=True,
            min_num_obs=DEFAULT_RESAMPLE_CONSTRAINTS,
            ts_type="hourly",
            resample_how="mean",
            # obs_filters=EBAS_FILTER,
            pyaro_config={
                "name": "ACTRIS-EBAS-h-diurnal",
                "reader_id": "actrisebas",
                "filename_or_obj_or_url": "",
                "filters": {
                    "time_bounds": {
                        "startend_include": [
                            (f"{year}-01-01 00:00:00", f"{year + 1}-01-01 00:00:00")
                        ],
                    },
                    "variables": {"include": ebas_test_vars_diurnal},
                },
            },
        ),
        "ACTRIS-EBAS-d-tc": dict(
            obs_id="ACTRIS-EBAS-d-tc",
            web_interface_name="ACTRIS-EBAS-d",
            obs_vars=ebas_test_vars,
            obs_vert_type="Surface",
            colocate_time=True,
            min_num_obs=DEFAULT_RESAMPLE_CONSTRAINTS,
            ts_type="daily",
            # obs_filters=EBAS_FILTER,
            pyaro_config={
                "name": "ACTRIS-EBAS-d-tc",
                "reader_id": "actrisebas",
                "filename_or_obj_or_url": "",
                "filters": {
                    "time_bounds": {
                        "startend_include": [
                            (f"{year}-01-01 00:00:00", f"{year + 1}-01-01 00:00:00")
                        ],
                    },
                    "variables": {"include": ebas_test_vars},
                },
            },
        ),
        "EBAS-d-tc": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-d",
            obs_vars=ebas_test_vars,
            obs_vert_type="Surface",
            colocate_time=True,
            min_num_obs=DEFAULT_RESAMPLE_CONSTRAINTS,
            ts_type="daily",
            # obs_filters=EBAS_FILTER,
        ),
        # # Diurnal
        "EBAS-h-diurnal": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-h",
            obs_vars=ebas_test_vars_diurnal,
            obs_vert_type="Surface",
            ts_type="hourly",
            # diurnal_only=True,
            resample_how="mean",
            # obs_filters={**EBAS_FILTER, "ts_type": "hourly"},
        ),
    }

    # Setup for supported satellite evaluations
    OBS_SAT = {}

    OBS_CFG = {**OBS_GROUNDBASED, **OBS_SAT}

    CFG["obs_cfg"] = OBS_CFG

    return copy.deepcopy(CFG)
