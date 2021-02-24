import os
import pytest

from pyaerocom.conftest import tda, does_not_raise_exception, testdata_unavail

from pyaerocom import Colocator, ColocatedData, GriddedData, UngriddedData
from pyaerocom.io import ReadGridded, ReadMscwCtm
from pyaerocom.exceptions import DataCoverageError
from pyaerocom.io.aux_read_cubes import add_cubes

@testdata_unavail
@pytest.fixture(scope='function')
def col_tm5_aero(model_id='TM5-met2010_CTRL-TEST',
                 obs_id='AeronetSunV3L2Subset.daily',
                 obs_vars='od550aer'):
    coloc = Colocator(model_id=model_id, obs_id=obs_id, obs_vars=obs_vars)
    coloc.raise_exceptions = True
    coloc.reanalyse_existing = True
    coloc.start = 2010
    return coloc

@pytest.fixture(scope='function')
def col():
    return Colocator(raise_exceptions=True, reanalyze_existing=True)

def test_model_ts_type_read(col_tm5_aero):
    model_var = 'abs550aer'
    obs_var = 'od550aer'
    col_tm5_aero.save_coldata = False
    # Problem with saving since obs_id is different
    # from obs_data.contains_dataset[0]...
    col_tm5_aero.model_add_vars = {obs_var:model_var}
    col_tm5_aero.model_ts_type_read = {model_var:'daily', obs_var:'monthly'}
    data = col_tm5_aero._run_gridded_ungridded()
    assert (data[model_var].data.ts_type_src.values == ['daily', 'daily']).all()
    assert (data[obs_var].data.ts_type_src.values == ['daily', 'monthly']).all()

def test_colocator(col):
    assert isinstance(col, Colocator)
    col.obs_vars = 'var'
    assert isinstance(col.obs_vars, str)

def test_colocator_init_basedir_coldata(tmpdir):
    basedir = os.path.join(tmpdir, 'basedir')
    Colocator(raise_exceptions=True, basedir_coldata=basedir)
    assert os.path.isdir(basedir)

@testdata_unavail
def test_colocator__coldata_savename(data_tm5):
    col = Colocator(raise_exceptions=True)
    col.obs_name = 'obs'
    col.model_name = 'model'
    col.ts_type = 'monthly'
    col.filter_name = 'WORLD'
    savename = col._coldata_savename(data_tm5)
    assert isinstance(savename, str)
    assert savename == 'od550aer_REF-obs_MOD-model_20100101_20101231_monthly_WORLD.nc'

def test_colocator_update(tmpdir):
    col = Colocator(raise_exceptions=True)
    col.update(test="test")
    assert col.test == 'test'

    obs_id = 'test'
    col.update(obs_id=obs_id)
    assert col.obs_id == obs_id

    basedir = os.path.join(tmpdir, 'basedir')
    assert not os.path.isdir(basedir)
    col.update(basedir_coldata=basedir)
    assert os.path.isdir(basedir)

@pytest.mark.parametrize('gridded_gridded',[False, True])
def test_colocator_run(col_tm5_aero, gridded_gridded):
    if gridded_gridded:
        col_tm5_aero.obs_id = col_tm5_aero.model_id
    col_tm5_aero.run()
    coldata = col_tm5_aero.data[col_tm5_aero.model_id][col_tm5_aero.obs_vars[0]]
    assert isinstance(coldata, ColocatedData)

def test__run_gridded_ungridded(col_tm5_aero):
    obs_vars = col_tm5_aero.obs_vars[0]
    colocated_dict = col_tm5_aero._run_gridded_ungridded()
    assert isinstance(colocated_dict[obs_vars], ColocatedData)

def test__run_gridded_gridded(col_tm5_aero):
    obs_vars = col_tm5_aero.obs_vars[0]
    col_tm5_aero.obs_id = col_tm5_aero.model_id
    colocated = col_tm5_aero._run_gridded_gridded(obs_vars)
    assert isinstance(colocated[obs_vars], ColocatedData)
    assert isinstance(col_tm5_aero.data, dict)
    assert col_tm5_aero.data == {}

def test_colocator_filter_name():
    with does_not_raise_exception():
        Colocator(filter_name='WORLD')
    with pytest.raises(Exception):
        Colocator(filter_name='invalid')

def test_colocator_basedir_coldata(tmpdir):
    basedir = os.path.join(tmpdir, 'test')
    col = Colocator(raise_exceptions=True)
    col.basedir_coldata = basedir
    assert not os.path.isdir(basedir)

def test_colocator_read_ungridded():
    col = Colocator(raise_exceptions=True)
    obs_id = 'AeronetSunV3L2Subset.daily'
    obs_var = 'od550aer'
    col.obs_filters = {'longitude' : [-30, 30]}
    col.obs_id = obs_id
    col.read_opts_ungridded = {'last_file' : 10}

    data = col.read_ungridded(obs_var)
    assert isinstance(data, UngriddedData)

    col.read_opts_ungridded = None
    col.obs_vars = ['od550aer']
    with does_not_raise_exception():
        data = col.read_ungridded()
    col.obs_vars = ['invalid']
    with pytest.raises(DataCoverageError):
        data = col.read_ungridded()

def test_colocator_read_model_data():
    col = Colocator(raise_exceptions=True)
    model_id = 'TM5-met2010_CTRL-TEST'
    col.model_id = model_id
    data = col.read_model_data('od550aer')
    assert isinstance(data, GriddedData)

def test_colocator_call():
    col = Colocator(raise_exceptions=True)
    with pytest.raises(NotImplementedError):
        col()

def test_colocator__infer_start_stop():
    col = Colocator()
    reader = ReadGridded('TM5-met2010_CTRL-TEST')
    col._infer_start_stop(reader)
    assert col.start == 2010
    assert col.stop == None

def test_colocator_with_obs_data_dir_ungridded():
    col = Colocator(save_coldata=False)
    col.model_id='TM5-met2010_CTRL-TEST'
    col.obs_id='AeronetSunV3L2Subset.daily'
    col.obs_vars='od550aer'
    col.ts_type='monthly'
    col.apply_time_resampling_constraints = False

    aeronet_loc = tda.ADD_PATHS['AeronetSunV3L2Subset.daily']
    col.obs_data_dir = tda.testdatadir.joinpath(aeronet_loc)

    data = col._run_gridded_ungridded()
    assert len(data) == 1
    cd = data['od550aer']
    assert isinstance(cd, ColocatedData)
    assert cd.ts_type=='monthly'
    assert str(cd.start) == '2010-01-15T00:00:00.000000000'
    assert str(cd.stop) == '2010-12-15T00:00:00.000000000'

def test_colocator_with_model_data_dir_ungridded():
    col = Colocator(save_coldata=False)
    col.model_id='TM5-met2010_CTRL-TEST'
    col.obs_id='AeronetSunV3L2Subset.daily'
    col.obs_vars='od550aer'
    col.ts_type='monthly'
    col.apply_time_resampling_constraints = False

    model_dir = 'modeldata/TM5-met2010_CTRL-TEST/renamed'
    col.model_data_dir = tda.testdatadir.joinpath(model_dir)

    data = col._run_gridded_ungridded()
    assert len(data) == 1
    cd = data['od550aer']
    assert isinstance(cd, ColocatedData)
    assert cd.ts_type=='monthly'
    assert str(cd.start) == '2010-01-15T00:00:00.000000000'
    assert str(cd.stop) == '2010-12-15T00:00:00.000000000'

def test_colocator_with_obs_data_dir_gridded():
    col = Colocator(save_coldata=False)
    col.model_id='TM5-met2010_CTRL-TEST'
    col.obs_id='TM5-met2010_CTRL-TEST'
    col.obs_vars='od550aer'
    col.ts_type='monthly'
    col.apply_time_resampling_constraints = False

    obs_dir = 'modeldata/TM5-met2010_CTRL-TEST/renamed'
    col.obs_data_dir=str(tda.testdatadir.joinpath(obs_dir))

    data = col._run_gridded_gridded()
    assert len(data) == 1
    cd = data['od550aer']
    assert isinstance(cd, ColocatedData)
    assert cd.ts_type=='monthly'
    assert str(cd.start) == '2010-01-15T00:00:00.000000000'
    assert str(cd.stop) == '2010-12-15T00:00:00.000000000'

def test_colocator__find_var_matches(col):
    r = ReadGridded('TM5-met2010_CTRL-TEST')
    with pytest.raises(DataCoverageError):
        col._find_var_matches('invalid', r)
    var_matches = col._find_var_matches('od550aer', r)
    assert var_matches == {'od550aer': 'od550aer'}

    obs_vars = 'conco3'
    col.obs_vars = [obs_vars]
    col.model_use_vars = {obs_vars : 'od550aer'}
    var_matches = col._find_var_matches('conco3', r)
    assert var_matches == {'od550aer' : 'conco3'}

def test_colocator__find_var_matches_model_add_vars(col):
    r = ReadGridded('TM5-met2010_CTRL-TEST')
    model_var = 'abs550aer'
    obs_var = 'od550aer'
    col.model_add_vars = {obs_var:model_var}
    var_matches = col._find_var_matches(obs_var, r)
    assert var_matches == {model_var:obs_var, obs_var:obs_var}

def test_model_add_vars(col_tm5_aero):
    model_var = 'abs550aer'
    obs_var = 'od550aer'
    col_tm5_aero.model_add_vars = {obs_var:model_var}
    model_reader = ReadGridded(col_tm5_aero.model_id)
    var_matches = col_tm5_aero._check_model_add_var(obs_var, model_reader, {})
    assert var_matches == {model_var: obs_var}
    var_matches = col_tm5_aero._find_var_matches([obs_var], model_reader)
    assert len(var_matches) == 2
    assert (model_var in var_matches)
    assert (obs_var in var_matches)


@testdata_unavail
def test_colocator_instantiate_gridded_reader(path_emep):
    col = Colocator(gridded_reader_id={'model':'ReadMscwCtm', 'obs':'ReadGridded'})
    col.filepath = path_emep['daily']
    model_id = 'model'
    col.model_id = model_id
    r = col.instantiate_gridded_reader(what='model')
    assert isinstance(r, ReadMscwCtm)
    assert r.filepath == col.filepath
    assert r.data_id == model_id


@testdata_unavail
def test_colocator_instantiate_gridded_reader_model_data_dir(path_emep):
    col = Colocator(gridded_reader_id={'model':'ReadMscwCtm', 'obs':'ReadGridded'})
    model_data_dir = path_emep['data_dir']
    col.model_data_dir = path_emep['data_dir']
    model_id = 'model'
    col.model_id = model_id
    r = col.instantiate_gridded_reader(what='model')
    assert isinstance(r, ReadMscwCtm)
    assert r.data_dir == model_data_dir
    assert r.data_id == model_id


def test_colocator__get_gridded_reader_class():
    gridded_reader_id = {'model': 'ReadMscwCtm', 'obs': 'ReadMscwCtm'}
    col = Colocator(gridded_reader_id=gridded_reader_id)
    for what in ['model', 'obs']:
        assert col._get_gridded_reader_class(what=what) == ReadMscwCtm

def test_colocator__check_add_model_read_aux():
    coloc = Colocator(raise_exceptions=True)
    r = ReadGridded('TM5-met2010_CTRL-TEST')
    assert not coloc._check_add_model_read_aux('od550aer', r)
    coloc.model_read_aux = {
        'od550aer' : dict(
            vars_required=['od550aer', 'od550aer'],
            fun=add_cubes)}
    assert coloc._check_add_model_read_aux('od550aer', r)

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
