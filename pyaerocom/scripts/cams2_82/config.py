##################################################
#        The global configs
##################################################
from datetime import datetime
from pathlib import Path

import pandas as pd

from pyaerocom.io import PyaroConfig

GLOBAL_CONFIG = dict(
    # Description of the experiment
    proj_id="cams2-82",  # cannot be changed because it has a role in determining the output subfolders
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
    # Regional filter for analysis
    filter_name="ALL-wMOUNTAINS",
    # colocation frequency (no statistics in higher resolution can be computed)
    ts_type="hourly",
    # The size of map used to display the results
    map_zoom="World",
    # Options for time
    freqs=["daily", "hourly"],  # Possible frequencies
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
    obs_remove_outliers=True,
    model_remove_outliers=False,
    harmonise_units=True,
    regions_how="htap",
    annual_stats_constrained=False,
    weighted_stats=False,
    
    use_fairmode=False,
    
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
        "od550aer",
        "ec1064aer",
    ],
    min_num_obs=dict(
        # yearly=dict(monthly=9),
        # monthly=dict(daily=21, weekly=3),
        daily=dict(hourly=6),
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
    # concso2="GR0001*",
    # vmro3="RS0005*",
    # concNnh4="EE0009*",
    # concso4="EE0009*",
    # concco=["BETN*"],
)

BASE_FILTER = {
    # "latitude": [30, 82],
    # "longitude": [-30, 90],
}

EEA_RURAL_FILTER = {
    "station_type": ["background"],
    "station_area": [
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

EEA_SPECIES = [
    "concno2",
    # "concco",
    "conco3",
    # "concso2",
    "concpm10",
    "concpm25",
]

AERONET_SPECIES = [
    "od550aer"
]

OPENAQ_SPECIES = [
    "concpm10",
    "concpm25",
]

ICOS_SPECIES = [
    "vmrch4",
    "vmrco",
]

EPROFILE_SPECIES = ["ec1064aer"]


# def get_ignore_list(species):
#     return ignore_id_dict[species] if species in ignore_id_dict else ["NO0042*"]


# obs_filters = {
#     key: dict(
#         **BASE_FILTER,
#         station_id=get_ignore_list(key),
#         negate="station_id",
#     )
#     for key in species_list
# }

# Base observation config with EPROFILE only
OBS_CONFIG = {}


##################################################
#        Putting it all together
##################################################
CFG = dict(
    model_cfg=MODELS_CONFIG,
    obs_cfg=OBS_CONFIG,
    **GLOBAL_CONFIG,
)



def make_model_entry(
    start_date: datetime,
    end_date: datetime,
    model_path: Path,

) -> dict:
    return dict(
        model_id = "IFS",
        model_data_dir=str(model_path.resolve()),
        gridded_reader_id={"model": "ReadCAMS2_82"},
        model_kwargs=dict(
            daterange=[f"{start_date:%F}", f"{end_date:%F}"],
        ),
    )


def make_openAQ_entry(
    start_date: datetime,
    end_date: datetime,
    obs_path: Path,
) -> dict:
    filters={
                "time_bounds": {
                "startend_include": [[start_date.strftime("%Y-%m-%d %H:%M:%S"), end_date.strftime("%Y-%m-%d %H:%M:%S")]]
            },

        }
    data_id = "csv_timeseries"

    new_columns = {
        'variable': 7,
        'station': 1,
        'longitude': 2,
        'latitude': 3,
        'value': 4,
        "units": "ug m**-3",
        'end_time': 6,
        'start_time': 5,
        "altitude": "0",
        "country": "Norway",
        "station_type": "NaN",
        "standard_deviation": "NaN",
        "flag": "0",
        }
    config_eea = PyaroConfig(
        name="openAQ",
        reader_id=data_id,
        filename_or_obj_or_url=str(obs_path),
        filters=filters,
        name_map={
            
        },
        columns=new_columns,
    )

    return  dict(
        obs_id=config_eea.name,
        pyaro_config=config_eea,
        web_interface_name="openAQ",
        obs_vars=OPENAQ_SPECIES,
        obs_vert_type="Surface",
        ts_type="hourly",
        min_num_obs=dict(),
        
        # obs_filters=EEA_FILTER,   
    )
    
def make_EEA_entry(
    start_date: datetime,
    end_date: datetime,
    obs_path: Path,
) -> dict:
    filters={
                "time_bounds": {
                "startend_include": [[start_date.strftime("%Y-%m-%d %H:%M:%S"), end_date.strftime("%Y-%m-%d %H:%M:%S")]]
            },

        }
    data_id = "eeareader"
    config_eea = PyaroConfig(
        name="eea",
        reader_id=data_id,
        filename_or_obj_or_url=obs_path,
        filters=filters,
        dataset= "unverified",
        name_map={
            "PM2.5": "concpm25",
            "PM10": "concpm10",
            "NO2": "concno2",
            "O3": "conco3",
            
        },
    )

    return  dict(
        obs_id=config_eea.name,
        pyaro_config=config_eea,
        web_interface_name="EEA-rural",
        obs_vars=EEA_SPECIES,
        obs_vert_type="Surface",
        ts_type="hourly",
        obs_filters=EEA_FILTER,   
    )
def make_ICOS_entry(
    start_date: datetime,
    end_date: datetime,
    obs_path: Path,
) -> dict:

    return  dict(
        obs_id="ICOS",
        web_interface_name="ICOS",
        obs_data_dir=str(obs_path),
        obs_vars=ICOS_SPECIES,
        obs_vert_type="Surface",
        ts_type="hourly",
        obs_filters=BASE_FILTER,   
    )

def make_Aeronet_entry(
    start_date: datetime,
    end_date: datetime,
    obs_path: Path,
) -> dict:
    filters={
                "time_bounds": {
                "startend_include": [[start_date.strftime("%Y-%m-%d %H:%M:%S"), end_date.strftime("%Y-%m-%d %H:%M:%S")]]
            },

        }
    data_id = "csv_timeseries"
    columns = {
        "variable": 13,
        "station": 0,
        "longitude": 7,
        "latitude": 6,
        "value": 12,
        "units": 14,
        "start_time": 15,
        "end_time": 15,
        "altitude": 8,
        "country": "",
        "station_type": 10,
        "standard_deviation": "NaN",
        "flag": "0",
    }   
    config_eea = PyaroConfig(
        name="aeronet",
        reader_id=data_id,
        filename_or_obj_or_url=str(obs_path),
        filters=filters,
        name_map={
            "AOD_550nm": "od550aer"
            
        },
        columns=columns,
    )

    return  dict(
        obs_id=config_eea.name,
        pyaro_config=config_eea,
        web_interface_name="AeronetL1.5",
        obs_vars=AERONET_SPECIES,
        obs_vert_type="Surface",
        ts_type="hourly",
        # obs_filters=EEA_FILTER,   
    )


def make_EPROFILE_entry(
    start_date: datetime,
    end_date: datetime,
    obs_path: Path,
) -> dict:
    return dict( 
      obs_vars=EPROFILE_SPECIES,
      obs_id="EPROFILE",
      obs_name="EPROFILE",
      obs_ts_type_read=None,
      obs_vert_type="Column",
      obs_aux_requires={},
      instr_vert_loc=None,
      is_superobs=False,
      only_superobs=False,
      is_bulk=False,
      bulk_options={},
      colocation_layer_limts=None,
      profile_layer_limits=[
        {
          "start": 0,
          "end": 1000
        },  
        {
          "start": 1000,
          "end": 2000
        },
        {
          "start": 2000,
          "end": 3000
        },
        {
          "start": 3000,
          "end": 4000
        },
        {
          "start": 4000,
          "end": 5000
        },
        {
          "start": 5000,
          "end": 6000
        },
        {
          "start": 6000,
          "end": 7000
        },
        {
          "start": 7000,
          "end": 8000
        },
        {
          "start": 8000,
          "end": 9000
        },
        {
          "start": 9000,
          "end": 10000
        }
      ],
      web_interface_name="EPROFILE",
      diurnal_only=False,
      obs_type=None,
      read_opts_ungridded={},
      only_json=False,
      coldata_dir=None,
      obs_use_climatology=False,
      colocate_time=False,
      min_num_obs={
        "yearly": {
          "monthly": 1
        },
        "monthly": {
          "daily": 1
        },
        "daily": {
          "hourly": 1
        }
      },
      ts_type="daily",
      ignore_station_ids=None,
      colocation_layer_limits=[
        {
          "start": 0,
          "end": 2000
        },
        {
          "start": 2000,
          "end": 4000
        },
        {
          "start": 4000,
          "end": 6000
        }
      ],
      obs_filters={
        "latitude": [
          -90,
          90
        ],
        "longitude": [
          -180,
          180
        ]
      }
    )
