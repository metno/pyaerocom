from pyaerocom.config import ALL_REGION_NAME

MODELS = {
    "TM5-AP3-CTRL": dict(
        model_id="TM5-met2010_CTRL-TEST",
        model_add_vars=dict(od550csaer=["od550aer"]),
        model_ts_type_read="monthly",
        flex_ts_type=False,
    )
}

ODCSFUN = "AeronetSDAV3L2Subset.daily;od550lt1aer+AeronetSDAV3L2Subset.daily;od550gt1aer"
OBS_GROUNDBASED = {
    "AERONET-Sun": dict(
        obs_id="AeronetSunV3L2Subset.daily", obs_vars=("od550aer",), obs_vert_type="Column"
    ),
    "AERONET-SDA": dict(
        obs_id="AERONET-SDA",
        obs_vars=["od550csaer"],
        obs_type="ungridded",
        obs_vert_type="Column",
        obs_merge_how={
            "od550csaer": "eval",
        },
        obs_aux_requires={
            "od550csaer": {
                "AeronetSDAV3L2Subset.daily": ["od550lt1aer", "od550gt1aer"],
            }
        },
        obs_aux_funs={"od550csaer": ODCSFUN},
        obs_aux_units={"od550csaer": "1"},
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
    main_freq="monthly",
    zeros_to_nan=False,
    min_num_obs=None,
    colocate_time=False,
    obs_remove_outliers=False,
    add_seasons=False,
    model_remove_outliers=False,
    harmonise_units=True,
    regions_how="country",  #'default',#'country',
    annual_stats_constrained=False,
    proj_id="test",
    exp_id="exp2",
    exp_name="AeroVal test experiment 2",
    exp_descr=("Test setup for more complex evaluation configurations"),
    exp_pi="Jonas Gliss",
    public=True,
    # directory where colocated data files are supposed to be stored
    weighted_stats=True,
)
