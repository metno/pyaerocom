import os

import numpy as np

from ._outbase import ADD_MODELS_DIR, AEROVAL_OUT

START = 2000
STOP = 2020
YEARS = [str(x) for x in np.arange(START, STOP)]
lat_range = (30, 60)
lon_range = (10, 40)

from .._conftest_helpers import add_dummy_model_data

# create some fake model data
for i, year in enumerate(YEARS):
    MODEL_DIR = add_dummy_model_data(
        "prmm",
        "mm",
        "monthly",
        "Surface",
        name="DUMMY-MOD-TRENDS",
        year=year,
        lat_range=lat_range,
        lon_range=lon_range,
        value=i + 1,
        tmpdir=ADD_MODELS_DIR,
    )

    OBS_DIR = add_dummy_model_data(
        "prmm",
        "mm d-1",
        "monthly",
        "Surface",
        name="DUMMY-OBS-TRENDS",
        year=year,
        lat_range=lat_range,
        lon_range=lon_range,
        value=i + 1,
        tmpdir=ADD_MODELS_DIR,
    )

MODELS = {"DUMMY-MOD": dict(model_id="DUMMY-MODEL", model_data_dir=MODEL_DIR)}

OBS_GROUNDBASED = {
    "DUMMY-OBS": dict(
        obs_id="DUMMY-OBS-TRENDS", obs_vars=["prmm"], obs_data_dir=OBS_DIR, obs_vert_type="Surface"
    )
}

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
    periods=[f"{START}-{STOP}"],
    add_trends=True,
    main_freq="monthly",
    harmonise_units=True,
    proj_id="test",
    exp_id="exp5",
    exp_name="AeroVal test experiment 5",
    exp_descr=("Test setup for more trends evaluation (FAKE PRECIP DATA)"),
    exp_pi="Jonas Gliss",
    public=True,
    # directory where colocated data files are supposed to be stored
    weighted_stats=True,
)
