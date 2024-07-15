from __future__ import annotations

from pathlib import Path

from pyaerocom.config import ALL_REGION_NAME

from .common import add_dummy_model_data

YEAR = "2007"


def fake_model_data(tmp_path: str | Path) -> dict:
    add_dummy_model_data(
        "vmrno2",
        "nmole mole-1",
        "monthly",
        "Surface",
        year=YEAR,
        lat_range=(-90, 90),
        lon_range=(-180, 180),
        tmp_path=tmp_path,
    )
    model_data_dir = add_dummy_model_data(
        "vmro3",
        "nmole mole-1",
        "monthly",
        "Surface",
        year=YEAR,
        lat_range=(-90, 90),
        lon_range=(-180, 180),
        tmp_path=tmp_path,
    )
    return dict(
        DUMMY=dict(
            model_id="DUMMY-MODEL",
            model_data_dir=model_data_dir,
        )
    )


OBS_GROUNDBASED = {"EBAS": dict(obs_id="EBASSubset", obs_vars=("vmro3",), obs_vert_type="Surface")}

CFG = dict(
    model_cfg=dict(),  # fake_model_data("PATH_TO_MODEL_DATA"),
    obs_cfg=OBS_GROUNDBASED,
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
