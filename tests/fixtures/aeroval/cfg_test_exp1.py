from pyaerocom.config import ALL_REGION_NAME

MODELS = {"TM5-AP3-CTRL": dict(model_id="TM5-met2010_CTRL-TEST")}

OBS_GROUNDBASED = {
    "AERONET-Sun": dict(
        obs_id="AeronetSunV3L2Subset.daily",
        obs_vars=("od550aer",),
        obs_vert_type="Column",
    )
}

CFG = dict(
    model_cfg=MODELS,
    obs_cfg=OBS_GROUNDBASED,
    json_basedir="PATH_TO_AEROVAL_OUT/data",
    coldata_basedir="PATH_TO_AEROVAL_OUT/coldata",
    # if True, existing colocated data files will be deleted
    reanalyse_existing=True,
    raise_exceptions=True,
    only_json=False,
    add_model_maps=True,
    only_model_maps=False,
    clear_existing_json=False,
    # Regional filter for analysis
    filter_name=f"{ALL_REGION_NAME}-wMOUNTAINS",
    # colocation frequency (no statistics in higher resolution can be computed)
    ts_type="daily",
    map_zoom="World",
    freqs=["daily", "monthly", "yearly"],
    periods=["2010"],
    main_freq="monthly",
    zeros_to_nan=False,
    min_num_obs=None,
    colocate_time=False,
    obs_remove_outliers=False,
    add_seasons=False,
    model_remove_outliers=False,
    harmonise_units=True,
    regions_how="default",  #'default',#'country',
    annual_stats_constrained=True,
    proj_id="test",
    exp_id="exp1",
    exp_name="AeroVal test experiment 1",
    exp_descr=("Very simple setup to test basic stuff in AeroVal"),
    exp_pi="Jonas Gliss",
    public=True,
    # directory where colocated data files are supposed to be stored
    weighted_stats=True,
)
