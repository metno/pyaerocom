from pyaerocom.config import ALL_REGION_NAME

MODELS = {
    "TM5-AP3-CTRL": dict(
        model_id="TM5-met2010_CTRL-TEST", model_ts_type_read="monthly", flex_ts_type=False
    )
}

OBS_GROUNDBASED = {
    "AERONET-Sun": dict(
        obs_id="AeronetSunV3L2Subset.daily",
        obs_vars=("od550aer",),
        only_superobs=True,
        obs_vert_type="Column",
    ),
    "AERONET-SDA": dict(
        obs_id="AeronetSDAV3L2Subset.daily",
        obs_vars=("od550aer",),
        only_superobs=True,
        obs_vert_type="Column",
    ),
    "SDA-and-Sun": dict(
        is_superobs=True,
        obs_id=("AERONET-Sun", "AERONET-SDA"),
        obs_vars=("od550aer",),
        obs_vert_type="Column",
    ),
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
    add_model_maps=False,
    only_model_maps=False,
    clear_existing_json=False,
    # Regional filter for analysis
    filter_name=f"{ALL_REGION_NAME}-wMOUNTAINS",
    # colocation frequency (no statistics in higher resolution can be computed)
    ts_type="monthly",
    map_zoom="World",
    freqs=["monthly"],
    periods=["2010"],
    add_seasons=False,
    main_freq="monthly",
    zeros_to_nan=False,
    min_num_obs=None,
    colocate_time=False,
    obs_remove_outliers=False,
    model_remove_outliers=False,
    harmonise_units=True,
    regions_how="default",
    annual_stats_constrained=False,
    proj_id="test",
    exp_id="exp4",
    exp_name="AeroVal test experiment 4",
    exp_descr=("Test superobs processing"),
    exp_pi="Jonas Gliss",
    public=True,
)
