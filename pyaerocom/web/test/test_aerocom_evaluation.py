import os
import pytest
from pandas import DataFrame

from pyaerocom import Colocator, ColocatedData, GriddedData, UngriddedData
from pyaerocom.conftest import tda
from pyaerocom.web import AerocomEvaluation
from pyaerocom.io.aux_read_cubes import add_cubes

PROJ_ID = 'project'
EXP_ID = 'exp'

OBS_ID = 'AeronetSunV3L2Subset.daily'
OBS_NAME = 'AeronetSun'
OBS_VARS = 'od550aer'
OBS_VERT_TYPE = 'Column'

MODEL_NAME = 'TM5'
MODEL_ID = 'TM5-met2010_CTRL-TEST'
TS_TYPE = 'monthly'
START = 2010


CONFIG = tda.testdatadir.joinpath(tda.ADD_PATHS['CONFIG'])
METHODS_FILE = CONFIG.joinpath('cube_read_methods.py')

@pytest.fixture(scope='function')
def model_config():
    config = {MODEL_NAME : dict(model_id=MODEL_ID,
                                model_ts_type_read=TS_TYPE,
                                vert_which=OBS_VERT_TYPE
                                )}
    return config

@pytest.fixture(scope='function')
def obs_config():
    config = {OBS_NAME : dict(obs_id=OBS_ID,
                              obs_vars=OBS_VARS,
                              obs_vert_type=OBS_VERT_TYPE)}
    return config

@pytest.fixture(scope='function')
def model_config_aux(model_config):
    config = model_config.copy()
    config[MODEL_NAME]['model_read_aux'] = {'od550aer' : dict(
        vars_required=['od550aer', 'od550aer'],
        fun='add_cubes')}
    return config

@pytest.fixture(scope='function')
def stp(model_config, obs_config,tmpdir):
    return AerocomEvaluation(proj_id=PROJ_ID, exp_id=EXP_ID,
                             model_config=model_config,
                             obs_config=obs_config, start=START, ts_type=TS_TYPE,
                             raise_exceptions=True, reanalyse_existing=True,
                             out_basedir=str(tmpdir))

@pytest.fixture(scope='function')
def stp_min(tmpdir):
    return AerocomEvaluation(proj_id=PROJ_ID, exp_id=EXP_ID,
                             reanalyse_existing=True,
                             raise_exceptions=True,
                             out_basedir=str(tmpdir))


def test_aerocom_evaluation(stp_min):
    assert isinstance(stp_min, AerocomEvaluation)

def test_aerocom_evaluation_run_colocation(stp):

    mid = 'TM5-met2010_CTRL-TEST'
    var_name = 'od550aer'
    col = stp.run_colocation(model_name='TM5',
                             obs_name='AeronetSun',
                             var_name=var_name)


    assert isinstance(col, Colocator)
    assert mid in col.data
    assert var_name in col.data[mid]
    coldata = col.data[mid][var_name]
    assert isinstance(coldata, ColocatedData)
    assert coldata.shape == (2, 12, 8)


def test_aerocom_evaluation_run_evaluation(stp):
    col_paths = stp.run_evaluation(update_interface=False,
                                   reanalyse_existing=False) #reuse model colocated data from prev. test
    assert len(col_paths) == 1
    assert os.path.isfile(col_paths[0])

def test_aerocom_evaluation_get_web_overview_table(stp, tmpdir):
    stp.update()
    stp.run_evaluation(update_interface=False)
    table = stp.get_web_overview_table()
    assert isinstance(table, DataFrame)
    assert len(table) > 0

def test_aerocom_evaluation_get_custom_read_method_model_file(stp,
                                                              model_config_aux):
    stp.add_methods_file = METHODS_FILE
    stp.model_config = model_config_aux
    fun = stp.get_custom_read_method_model('add_cubes')
    assert fun == add_cubes

def test_aerocom_evaluation_get_custom_read_method_model_parameter(stp,
                                                                   model_config_aux):
    stp.add_methods={'add_cubes':add_cubes}
    fun = stp.get_custom_read_method_model('add_cubes')
    assert fun == add_cubes

def test_aerocom_evaluation_all_obs_vars(stp):
    assert stp.all_obs_vars == [OBS_VARS]

def test_aerocom_evaluation_get_model_name(stp):
    assert stp.get_model_name(MODEL_ID) == MODEL_NAME

def test_aerocom_evaluation___str__(stp):
    assert isinstance(str(stp), str)

def test_aerocom_evaluation_to_from_json(stp, tmpdir):
    stp.to_json(tmpdir)
    config_filename = 'cfg_{}_{}.json'.format(PROJ_ID, EXP_ID)
    stp_new = AerocomEvaluation(proj_id='project2', exp_id='exp2', raise_exceptions=True)
    stp_new.from_json(os.path.join(tmpdir, config_filename))
    for old, new in zip(dir(stp), dir(stp_new)):
        assert stp[old] == stp_new[new]

    stp_new = AerocomEvaluation(proj_id='project2', exp_id='exp2', raise_exceptions=True)
    stp_new.config_dir = tmpdir
    stp_new.load_config(PROJ_ID, EXP_ID)
    for old, new in zip(dir(stp), dir(stp_new)):
        assert stp[old] == stp_new[new]

def test_aerocom_evaluation_read_model_data(stp):
    data = stp.read_model_data(MODEL_NAME, OBS_VARS)
    assert isinstance(data, GriddedData)
    with pytest.raises(ValueError):
        stp.read_model_data('model_name', 'od550aer')

def test_aerocom_evaluation_read_ungridded_obsdata(stp):
    data = stp.read_ungridded_obsdata(OBS_NAME, vars_to_read=[OBS_VARS])
    assert isinstance(data, UngriddedData)

@pytest.mark.parametrize('search,expected,fun_name',[
    ('TM*', [MODEL_NAME], 'find_model_matches'),
    ('Aero*', [OBS_NAME], 'find_obs_matches'),
])
def test_aerocom_evaluation_find_matches(stp, search, expected, fun_name):
    search_fun = getattr(AerocomEvaluation, fun_name)
    assert search_fun(stp, search) == expected

# @ejgal: keep these tests until deciding if test_aerocom_evaluation_find_matches is ok
# def test_aerocom_evaluation_find_model_matches(stp):
#     matches = stp.find_model_matches('TM*')
#     assert matches == [MODEL_NAME]
#
# def test_aerocom_evaluation_find_obs_matches(stp):
#     matches = stp.find_obs_matches('Aero*')
#     assert matches == [OBS_NAME]

@pytest.mark.parametrize('expected,property',[
    ([MODEL_NAME], 'all_model_names'),
    ([OBS_NAME], 'all_obs_names'),
])
def test_aerocom_evaluation_all_names(stp, expected, property):
    assert getattr(stp, property) == expected

# @ejgal: keep these tests until deciding if test_aerocom_evaluation_all_names is ok.
# def test_aerocom_evaluation_all_model_names(stp):
#     assert stp.all_model_names == [MODEL_NAME]
#
# def test_aerocom_evaluation_all_obs_names(stp):
#     assert stp.all_obs_names == [OBS_NAME]

def test_aerocom_evaluation_find_obs_name(stp):
    obs_name = stp.find_obs_name(OBS_ID, OBS_VARS)
    assert obs_name == OBS_NAME

def test_aerocom_evaluation_find_model_name(stp):
    model_name = stp.find_model_name(MODEL_ID)
    assert model_name == MODEL_NAME

@pytest.mark.parametrize('key,val,expected',[
    ('proj_id', ['project'], AttributeError),
    ('exp_id', ['exp'], AttributeError)
])
def test_aerocom_evaluation_check_config(stp_min, key, val, expected):
    stp_min[key] = val
    with pytest.raises(expected):
        stp_min.check_config()

@pytest.mark.parametrize('config_name,name,id',[
    ('model_config', MODEL_NAME, 'model_id'),
    ('obs_config', OBS_NAME, 'obs_id')
])
def test_aerocom_evaluation_check_config_model_obs(stp, config_name, name, id):
    del stp[config_name][name][id]
    with pytest.raises(KeyError):
        stp.check_config()

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
