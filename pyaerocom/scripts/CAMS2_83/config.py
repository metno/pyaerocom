##################################################
#        The global configs
##################################################
import os

from pyaerocom.io.cams2_83.models import ModelName

GLOBAL_CONFIG = dict(
    # Description of the experiment
    proj_id="CAMS2-83",
    exp_id="cams2-83-examples",
    exp_name="CAMS2-83 test",
    exp_descr=(
        "This is an example config of how to evaluate EMEP. It is meant as an educational experiment only, but can be used freely as a starting point to other experiments."
    ),
    exp_pi="Daniel Heinesen",
    # Whether or not the experiment is visible in the web interface
    public=True,
    # Locations where to place the results
    # These can be set as the user want, but as here written to use the folder structures we made
    json_basedir=os.path.abspath("../../data"),
    coldata_basedir=os.path.abspath("../../coldata"),
    # io_aux_file=os.path.abspath("../eval_py/gridded_io_aux.py"),
    # Some infor about the output
    reanalyse_existing=True,
    only_json=False,
    add_model_maps=False,
    only_model_maps=False,
    clear_existing_json=False,
    # if True, the analysis will stop whenever an error occurs (else, errors that
    # occurred will be written into the logfiles)
    raise_exceptions=True,
    # options for CAMS2-83
    use_cams2_83=True,
    # cams2_83_model=ModelName.EMEP,
    # cams2_83_dateshift=0,
    # Regional filter for analysis
    filter_name="WORLD-wMOUNTAINS",
    # colocation frequency (no statistics in higher resolution can be computed)
    ts_type="hourly",
    # The size of map used to display the results
    map_zoom="Europe",
    # Options for time
    freqs=["yearly", "monthly", "daily", "hourly"],  # Possible frequencies
    periods=[
        "2019"
    ],  # Periodes, can be single years or range, e.g. 2010-2015. EMEP only supports single years as of now
    main_freq="hourly",  # default frequency to use. This will be overwritten in most of the observation options (see below)
    # This has to be true for the web interface to show diurnal evaluation
    use_diurnal=False,
    # O3 is special, since we want to look at daily max
    # Here we say that we when O3(vmro3) is evaluated, the daily results will be the maximum for that day
    resample_how={"vmro3": {"daily": {"hourly": "max"}}},
    # Assorted options, more info can be found in 'cfg_examples_examples1.py'
    zeros_to_nan=False,
    colocate_time=False,
    obs_remove_outliers=False,
    model_remove_outliers=False,
    harmonise_units=True,
    regions_how="country",
    annual_stats_constrained=False,
    weighted_stats=False,
    # This is just the order at which the different species will be shown in the web interface
    # Species that are not evaluated can still be in this list. The web interface will not show them if they are not evaluated
    var_order_menu=[
        "vmrno2",
        "vmro3max",
        "vmro3",
        "conco3",
        "vmrox",
        "concso2",
        "vmrco",
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
    ],
)

GLOBAL_CONFIG["min_num_obs"] = dict(
    yearly=dict(monthly=9), monthly=dict(daily=21, weekly=3), daily=dict(hourly=18)
)


##################################################
#        The model configs
##################################################
# folder_CAMS2_83 = f'/home/danielh/lustre/storeB/project/fou/kl/CAMS2_83/test_data'
folder_CAMS2_83 = f"/lustre/storeB/project/fou/kl/CAMS2_83/test_data"


MODELS_CONFIG = {
    "CAMS2-83": dict(
        model_id="CAMS2-83.EMEP.day0",  # ID of the model
        model_data_dir=folder_CAMS2_83,  # Where (on PPI) the netCDF file is found
        gridded_reader_id={"model": "ReadCAMS2_83"},  #
        # model_kwargs=dict(
        #     cams2_83_daterange=["20190601", "20190603"]#list(pd.date_range(start="20190601", end="20190703")),
        # )
    ),
}


##################################################
#        The observation configs
##################################################
# Station filters
ignore_id_dict = dict(
    concso2="GR0001*",
    vmro3="RS0005*",
    concNnh4="EE0009*",
    concso4="EE0009*",
)

BASE_FILTER = {
    "latitude": [30, 82],
    "longitude": [-30, 90],
    "station_id": ["NO0042*"],
    "negate": "station_id",
}

EEA_RURAL_FILTER = {
    "station_classification": ["background"],
    "area_classification": [
        "rural",
        "rural-nearcity",
        "rural-regional",
        "rural-remote",
    ],
}
EBAS_FILTER = {
    "data_level": [None, 2],
    **BASE_FILTER,
    "altitude": [-20, 1000],
    "set_flags_nan": True,
}

EEA_FILTER = {
    **BASE_FILTER,
    **EEA_RURAL_FILTER,
    "altitude": [-20, 1000],
}

# Empty observation config
OBS_CONFIG = {}

# EEA observatio
OBS_CONFIG["EEA"] = dict(
    # obs_id="EEAAQeRep.v2",
    obs_id="EEAAQeRep.NRT",
    obs_vars=["concno2"],
    web_interface_name="EEA-rural",
    obs_vert_type="Surface",
    # ignore_station_ids=ignore_id_dict, #One station needs to be ignored
    obs_filters=EEA_FILTER,
)

##################################################
#        Putting it all together
##################################################
CFG = {**GLOBAL_CONFIG}

CFG["model_cfg"] = MODELS_CONFIG
CFG["obs_cfg"] = OBS_CONFIG