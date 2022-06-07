"""
CAMS84 configuration
AeroCom PhaseIII optical properties experiment
"""

from collections import ChainMap

from pyaerocom.config import ALL_REGION_NAME

# Used below in some of the obsconfig entries to speed up when ran locally
OBS_ACCESS: dict = {}

# BASE FILTERS
ALTITUDE_FILTER = {"altitude": [0, 1000]}

GHOST_RURAL_FILTER = {
    "station_classification": ["background"],
    "area_classification": ["rural", "rural-near_city", "rural-regional", "rural-remote"],
}

EEA_NRT_RURAL_FILTER = {
    "station_classification": ["background"],
    "area_classification": ["rural", "rural-nearcity", "rural-regional", "rural-remote"],
}

# options station_classification: ['rural', 'urban', 'urban_bound']
# options area_classification: ['Agricultural', 'Commercial', 'Forested',
#               'Industrial', 'Residential', 'Undeveloped Rural', 'Unknown']
AIRNOW_RURAL_FILTER = {
    "station_classification": ["rural"]
    #'area_classification'     :   ['Agricultural', 'Forested', 'Undeveloped Rural']
}

# OBS SPECIFIC FILTERS (combination of the above and more)
GHOST_BASE_FILTER = {
    "set_flags_nan": True,
}

# How to read auxiliary model variables (that cannot be read but need to be
# computed). Entry under "fun" needs to be defined in ../eval_py/cube_read_methods.py
MODEL_AUX_VARS = {
    "vmro3": dict(vars_required=["mmro3"], fun="mmr_to_vmr"),
    "vmrno2": dict(vars_required=["mmrno2"], fun="mmr_to_vmr"),
}

# Setup for models used in analysis
MODELS = {
    "IFS-OSUITE": dict(model_id="ECMWF_OSUITE", model_read_aux=MODEL_AUX_VARS),
    "IFS-OSUITE-96h": dict(model_id="ECMWF_OSUITE_96H", model_read_aux=MODEL_AUX_VARS),
    "IFS-CTRL": dict(model_id="ECMWF_CNTRL", model_read_aux=MODEL_AUX_VARS),
    "IFS-CTRL-96h": dict(model_id="ECMWF_CNTRL_96H", model_read_aux=MODEL_AUX_VARS),
}

# Setup for available ground based observations (ungridded)

VAR_OUTLIER_RANGES = {
    "concpm10": [-1, 5000],  # ug m-3
    "concpm25": [-1, 5000],  # ug m-3
    "vmrno2": [-1, 5000],  # ppb
    "vmro3": [-1, 5000],  # ppb
}

AERONET_SITE_FILTER = dict(station_name="DRAGON*", negate="station_name")
OBS_GROUNDBASED = {
    "AeronetL1.5-d": dict(
        obs_id="AeronetSunV3Lev1.5.daily",
        obs_vars=["ang4487aer", "od550aer"],
        obs_vert_type="Column",
        obs_filters=ChainMap(ALTITUDE_FILTER, AERONET_SITE_FILTER),
        min_num_obs={"monthly": {"daily": 3}},
    ),
    "EEA-NRT-rural": dict(
        obs_id="EEAAQeRep.NRT",
        obs_data_dir=OBS_ACCESS.get("EEA_NRT_LOCAL"),
        obs_vars=["concpm10", "concpm25", "vmro3", "vmrno2"],
        obs_vert_type="Surface",
        obs_outlier_ranges=VAR_OUTLIER_RANGES,
        obs_filters=ChainMap(ALTITUDE_FILTER, EEA_NRT_RURAL_FILTER),
    ),
    "G-EEA-rural": dict(
        obs_id="GHOST.EEA.daily",
        obs_data_dir=OBS_ACCESS.get("GHOST_LOCAL_EEA_DAILY"),
        obs_vars=["concpm10", "concpm25", "vmro3", "vmrno2"],
        obs_vert_type="Surface",
        obs_outlier_ranges=VAR_OUTLIER_RANGES,
        obs_filters=ChainMap(ALTITUDE_FILTER, GHOST_BASE_FILTER, GHOST_RURAL_FILTER),
    ),
    "AirNow-rural": dict(
        obs_id="AirNow",
        obs_data_dir=None,
        obs_vars=["concpm10", "concpm25", "vmro3", "vmrno2"],
        obs_outlier_ranges=VAR_OUTLIER_RANGES,
        obs_filters=ChainMap(ALTITUDE_FILTER, AIRNOW_RURAL_FILTER),
        obs_vert_type="Surface",
    ),
    "AirNow": dict(
        obs_id="AirNow",
        obs_data_dir=OBS_ACCESS.get("AIRNOW_LOCAL"),
        obs_vars=["concpm10", "concpm25", "vmro3", "vmrno2"],
        obs_outlier_ranges=VAR_OUTLIER_RANGES,
        obs_filters={**ALTITUDE_FILTER},
        obs_vert_type="Surface",
    ),
    "MarcoPolo": dict(
        obs_id="MarcoPolo",
        obs_data_dir=OBS_ACCESS.get("MARCOPOLO_LOCAL"),
        obs_vars=["concpm10", "concpm25", "vmro3", "vmrno2"],
        obs_outlier_ranges=VAR_OUTLIER_RANGES,
        obs_vert_type="Surface",
    ),
}


# Setup for supported satellite evaluations
OBS_SAT: dict = {}

OBS_CFG = ChainMap(OBS_GROUNDBASED, OBS_SAT)


DEFAULT_RESAMPLE_CONSTRAINTS = dict(monthly=dict(daily=21), daily=dict(hourly=18))

CAMS84_CONFIG = dict(
    model_cfg=MODELS,
    obs_cfg=OBS_CFG,
    json_basedir="../../data",
    coldata_basedir="../../coldata",
    io_aux_file="../eval_py/gridded_io_aux.py",
    # if True, existing colocated data files will be deleted
    reanalyse_existing=True,
    only_json=False,
    add_model_maps=False,
    only_model_maps=False,
    clear_existing_json=False,
    # if True, the analysis will stop whenever an error occurs (else, errors that
    # occurred will be written into the logfiles)
    raise_exceptions=False,
    # Regional filter for analysis
    filter_name=f"{ALL_REGION_NAME}-wMOUNTAINS",
    # colocation frequency (no statistics in higher resolution can be computed)
    ts_type="daily",
    map_zoom="World",
    freqs=["daily", "monthly"],
    periods=["2018-2021", "2018", "2019", "2020", "2021"],
    main_freq="monthly",
    zeros_to_nan=False,
    min_num_obs=DEFAULT_RESAMPLE_CONSTRAINTS,
    colocate_time=False,
    obs_remove_outliers=True,
    model_remove_outliers=False,
    harmonise_units=True,
    regions_how="htap",
    annual_stats_constrained=False,
    proj_id="cams84",
    exp_id="eval",
    exp_name="Evaluation of CAMS forecast and reanalysis models",
    exp_descr=(
        "Both OSUITE and CNTRL are evaluated against multiple "
        "observation records including AOD from AERONET and "
        "PM, O3 and NO2 measurements."
    ),
    exp_pi="Jonas Gliß (jonasg@met.no)",
    public=True,
    # directory where colocated data files are supposed to be stored
    weighted_stats=True,
    var_order_menu=["od550aer", "ang4487aer", "concpm10", "concpm25", "vmrno2", "vmro3"],
)
