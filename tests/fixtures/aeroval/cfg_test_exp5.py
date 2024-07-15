from __future__ import annotations

from pathlib import Path

from pyaerocom.config import ALL_REGION_NAME

from .common import add_dummy_model_data

START = 2000
STOP = 2020
lat_range = (30, 60)
lon_range = (10, 40)


def fake_model_data(tmp_path: str | Path) -> dict:
    for i, year in enumerate(range(START, STOP), start=1):
        model_data_dir = add_dummy_model_data(
            "prmm",
            "mm",
            "monthly",
            "Surface",
            name="DUMMY-MOD-TRENDS",
            year=year,
            lat_range=lat_range,
            lon_range=lon_range,
            value=i,
            tmp_path=tmp_path,
        )
    return dict(
        DUMMY=dict(
            model_id="DUMMY-MODEL",
            model_data_dir=model_data_dir,
        )
    )


def fake_obs_data(tmp_path: str | Path) -> dict:
    for i, year in enumerate(range(START, STOP), start=1):
        obs_data_dir = add_dummy_model_data(
            "prmm",
            "mm d-1",
            "monthly",
            "Surface",
            name="DUMMY-OBS-TRENDS",
            year=year,
            lat_range=lat_range,
            lon_range=lon_range,
            value=i,
            tmp_path=tmp_path,
        )

    return dict(
        DUMMY=dict(
            obs_id="DUMMY-OBS",
            obs_vars=("prmm",),
            obs_data_dir=obs_data_dir,
            obs_vert_type="Surface",
        )
    )


CFG = dict(
    model_cfg=dir(),  # fake_model_data("PATH_TO_MODEL_DATA"),
    obs_cfg=dir(),  # fake_obs_data("PATH_TO_MODEL_DATA"),
    json_basedir="PATH_TO_AEROVAL_OUT/data",
    coldata_basedir="PATH_TO_AEROVAL_OUT/coldata",
    # if True, existing colocated data files will be deleted
    reanalyse_existing=True,
    raise_exceptions=True,
    only_json=False,
    add_model_maps=False,
    only_model_maps=False,
    clear_existing_json=False,
    # Regional filter for analysis
    filter_name=f"{ALL_REGION_NAME}-wMOUNTAINS",
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
