from pyaerocom import const
import os
TMPDIR = const.LOCAL_TMP_DIR
BASEOUT = os.path.join(TMPDIR, 'aeroval')
os.makedirs(BASEOUT, exist_ok=True)

YEAR = '2007'
from .._conftest_helpers import add_dummy_model_data, TMPDIR

add_dummy_model_data('vmrno2', 'nmole mole-1', 'monthly', 'Surface',
                     year=YEAR, lat_range=(-90,90), lon_range=(-180,180))
MODEL_DIR = add_dummy_model_data('vmro3', 'nmole mole-1', 'monthly', 'Surface',
                        year=YEAR, lat_range=(-90,90), lon_range=(-180,180))

MODELS = {
    'DUMMY' : dict(model_id='DUMMY-MODEL',
                   model_data_dir=MODEL_DIR)

}

OBS_GROUNDBASED = {
    'EBAS' : dict(obs_id='EBASSubset',
                  obs_vars = ['vmro3'],
                  obs_vert_type='Surface')
}

CFG = dict(

    model_cfg = MODELS,
    obs_cfg = OBS_GROUNDBASED,

    json_basedir = os.path.join(BASEOUT, 'data'),
    coldata_basedir = os.path.join(BASEOUT, 'coldata'),

    # if True, existing colocated data files will be deleted
    reanalyse_existing = True,
    raise_exceptions = True,
    only_json = False,
    add_model_maps = False,
    only_model_maps = False,

    clear_existing_json = False,

    # Regional filter for analysis
    filter_name = 'WORLD-wMOUNTAINS',

    # colocation frequency (no statistics in higher resolution can be computed)
    ts_type = 'monthly',

    map_zoom = 'World',

    freqs = ['monthly'],
    periods = [YEAR],
    main_freq = 'monthly',

    harmonise_units=True,

    proj_id = 'test',
    exp_id = 'exp3',
    exp_name = 'AeroVal test experiment 3',
    exp_descr = ('Test setup for more complex evaluation configurations'),
    exp_pi = 'Jonas Gliss',

    public = True,
    # directory where colocated data files are supposed to be stored
    weighted_stats = True,
)

if __name__=='__main__':
    from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
    from pyaerocom.access_testdata import initialise
    tda = initialise()
    stp = EvalSetup(**CFG)
    ana = ExperimentProcessor(stp)
    ana.run()
    print(ana.exp_output)