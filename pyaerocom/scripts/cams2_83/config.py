##################################################
#        The global configs
##################################################
from pathlib import Path

GLOBAL_CONFIG = dict(
    # Description of the experiment
    proj_id="cams2-83",  # cannot be changed because it has a role in determining the output subfolders
    exp_id="prototype",
    exp_name="Prototype-daily",
    exp_descr=("Evaluation using EEA-MF NRT obs."),
    exp_pi="<a href='https://atmosphere.copernicus.eu/help-and-support'>CAMS user support</a>",
    # Whether or not the experiment is visible in the web interface
    public=True,
    # Locations where to place the results
    # These can be set as the user want, but as here written to use the folder structures we made
    json_basedir=str(Path("../../data").absolute()),
    coldata_basedir=str(Path("../../coldata").absolute()),
    # io_aux_file=os.path.abspath("../eval_py/gridded_io_aux.py"),
    # Some info about the output
    reanalyse_existing=True,
    only_json=False,
    add_model_maps=False,
    # maps_res_deg=5,
    only_model_maps=False,
    clear_existing_json=False,
    # if True, the analysis will stop whenever an error occurs (else, errors that
    # occurred will be written into the logfiles)
    raise_exceptions=False,
    # options for CAMS2-83
    use_cams2_83=True,
    # cams2_83_model=ModelName.EMEP,
    # cams2_83_dateshift=0,
    # Regional filter for analysis
    filter_name="ALL-wMOUNTAINS",
    # colocation frequency (no statistics in higher resolution can be computed)
    ts_type="hourly",
    # The size of map used to display the results
    map_zoom="Europe",
    # Options for time
    freqs=["hourly", "daily"],  # Possible frequencies
    periods=[
        "2021-2022"
    ],  # Periods, can be single years or range, e.g. 2010-2015. EMEP only supports single years as of now
    main_freq="hourly",  # default frequency to use. This will be overwritten in most of the observation options (see below)
    add_seasons=False,
    use_meteorological_seasons=True,
    # This has to be true for the web interface to show diurnal evaluation
    use_diurnal=False,
    # O3 is special, since we want to look at daily max
    # Here we say that we when O3(vmro3) is evaluated, the daily results will be the maximum for that day
    resample_how={"vmro3": {"daily": {"hourly": "max"}}},
    # Assorted options, more info can be found in 'cfg_examples_examples1.py'
    # zeros_to_nan=False,
    zeros_to_nan=True,
    colocate_time=False,
    obs_remove_outliers=False,
    model_remove_outliers=False,
    harmonise_units=True,
    regions_how="country",
    annual_stats_constrained=False,
    weighted_stats=False,
    forecast_evaluation=True,
    forecast_days=4,
    use_fairmode=False,
    use_cams2_83_fairmode=False,
    drop_stats=("mb", "mab"),
    # This is just the order at which the different species will be shown in the web interface
    # Species that are not evaluated can still be in this list. The web interface will not show them if they are not evaluated
    var_order_menu=[
        "conco3",
        "conco3mda8",
        "concno2",
        "concpm10",
        "concpm25",
        "concso2",
        "concco",
    ],
    min_num_obs=dict(
        # yearly=dict(monthly=9),
        # monthly=dict(daily=21, weekly=3),
        daily=dict(hourly=18),
    ),
)


##################################################
#        The model configs
##################################################

MODELS_CONFIG = {}


##################################################
#        The observation configs
##################################################
# Station filters
ignore_id_dict = dict(
    concso2="GR0001*",
    vmro3="RS0005*",
    concNnh4="EE0009*",
    concso4="EE0009*",
    concco=["BETN*"],
)

BASE_FILTER = {
    "latitude": [30, 82],
    "longitude": [-30, 90],
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

species_list = [
    "concno2",
    "concco",
    "conco3",
    "concso2",
    "concpm10",
    "concpm25",
]


def get_ignore_list(species):
    return ignore_id_dict[species] if species in ignore_id_dict else ["NO0042*"]


obs_filters = {
    key: dict(
        **BASE_FILTER,
        station_id=get_ignore_list(key),
        negate="station_id",
    )
    for key in species_list
}

# Empty observation config
OBS_CONFIG = {}

# EEA observatio
OBS_CONFIG["EEA"] = dict(
    obs_id="CAMS2_83.NRT",
    # obs_id="EEAAQeRep.NRT",
    obs_vars=species_list,
    web_interface_name="EEA-UTD",
    obs_vert_type="Surface",
    read_opts_ungridded=dict(files=[], force_caching=True),
    obs_filters=obs_filters,
)

##################################################
#        Putting it all together
##################################################
CFG = dict(
    model_cfg=MODELS_CONFIG,
    obs_cfg=OBS_CONFIG,
    **GLOBAL_CONFIG,
)
