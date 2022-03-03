import os

from ._outbase import ADD_MODELS_DIR, AEROVAL_OUT

YEAR = "2007"
from .._conftest_helpers import add_dummy_model_data

# create some fake model data
add_dummy_model_data(
    "vmrno2",
    "nmole mole-1",
    "monthly",
    "Surface",
    year=YEAR,
    lat_range=(-90, 90),
    lon_range=(-180, 180),
    tmpdir=ADD_MODELS_DIR,
)
MODEL_DIR = add_dummy_model_data(
    "vmro3",
    "nmole mole-1",
    "monthly",
    "Surface",
    year=YEAR,
    lat_range=(-90, 90),
    lon_range=(-180, 180),
    tmpdir=ADD_MODELS_DIR,
)

MODELS = {"DUMMY": dict(model_id="DUMMY-MODEL", model_data_dir=MODEL_DIR)}

OBS_GROUNDBASED = {"EBAS": dict(obs_id="EBASSubset", obs_vars=["vmro3"], obs_vert_type="Surface")}

CFG = dict(
    model_cfg=MODELS,
    obs_cfg=OBS_GROUNDBASED,
    json_basedir=os.path.join(AEROVAL_OUT, "data"),
    coldata_basedir=os.path.join(AEROVAL_OUT, "coldata"),
    # if True, existing colocated data files will be deleted
    reanalyse_existing=True,
    raise_exceptions=True,
    only_json=False,
    add_model_maps=False,
    only_model_maps=False,
    clear_existing_json=False,
    # Regional filter for analysis
    filter_name="WORLD-wMOUNTAINS",
    # colocation frequency (no statistics in higher resolution can be computed)
    ts_type="monthly",
    map_zoom="World",
    freqs=["monthly"],
    periods=[YEAR],
    main_freq="monthly",
    harmonise_units=True,
    proj_id="test",
    exp_id="exp3",
    exp_name="AeroVal test experiment 3",
    exp_descr=("Test setup for more complex evaluation configurations"),
    exp_pi="Jonas Gliss",
    public=True,
    # directory where colocated data files are supposed to be stored
    weighted_stats=True,
)
