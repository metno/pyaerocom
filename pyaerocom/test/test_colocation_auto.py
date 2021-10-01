import os
import pytest

from pyaerocom.conftest import tda, does_not_raise_exception, testdata_unavail
from pyaerocom.colocation_auto import ColocationSetup, Colocator
from pyaerocom import ColocatedData, GriddedData, UngriddedData
from pyaerocom.io import ReadGridded, ReadMscwCtm
from pyaerocom.exceptions import ColocationError, DataCoverageError
from pyaerocom.io.aux_read_cubes import add_cubes

HOME = os.path.expanduser('~')
COL_OUT_DEFAULT = os.path.join(HOME, 'MyPyaerocom/colocated_data')

default_setup = {'save_coldata': True, '_obs_cache_only': False,
                 'obs_vars': None, 'obs_vert_type': None,
                 'model_vert_type_alt': None, 'read_opts_ungridded': None,
                 'obs_ts_type_read': None, 'model_use_vars': None,
                 'model_add_vars': None, 'model_to_stp': False,
                 'model_id': None, 'model_name': None, 'model_data_dir': None,
                 'obs_id': None, 'obs_name': None, 'obs_data_dir': None,
                 'obs_use_climatology': False, 'obs_add_meta': [],
                 'gridded_reader_id': {'model': 'ReadGridded', 'obs': 'ReadGridded'},
                 'start': None, 'stop': None, 'ts_type': None,
                 'filter_name': None, 'apply_time_resampling_constraints': None,
                 'min_num_obs': None, 'resample_how': None,
                 'remove_outliers': False, 'model_remove_outliers': False,
                 'obs_outlier_ranges': None, 'model_outlier_ranges': None,
                 'harmonise_units': False, 'vert_scheme': None,
                 'regrid_res_deg': None, 'ignore_station_names': None,
                 'basedir_coldata': COL_OUT_DEFAULT,
                 'model_ts_type_read': None, 'model_read_aux': None,
                 'model_use_climatology': False, 'colocate_time': False,
                 'flex_ts_type_gridded': True, 'reanalyse_existing': False,
                 'raise_exceptions': False,
                 'model_read_opts':None, 'model_rename_vars':{}
                 }

@testdata_unavail
@pytest.fixture(scope='function')
def tm5_aero_stp():
    return dict(
        model_id='TM5-met2010_CTRL-TEST',
        obs_id='AeronetSunV3L2Subset.daily',
        obs_vars='od550aer',
        start = 2010,
        raise_exceptions = True,
        reanalyse_existing = True
        )


@pytest.fixture(scope='function')
def col():
    return Colocator(raise_exceptions=True, reanalyze_existing=True)

@pytest.mark.parametrize('stp,should_be', [
    (ColocationSetup(), default_setup)
    ])
def test_colocation_setup(stp, should_be):
    for key, val in should_be.items():
        assert key in stp
        if key == 'basedir_coldata':
            assert os.path.samefile(val, stp['basedir_coldata'])
        else:
            assert val == stp[key], key

def test_colocator(col):
    assert isinstance(col, Colocator)
    col.obs_vars = 'var'
    assert isinstance(col.obs_vars, str)

@pytest.mark.parametrize('ts_type_desired, ts_type, flex, raises', [
    ('minutely', 'daily', False, pytest.raises(ColocationError)),
    ('daily', 'monthly', False, does_not_raise_exception()),
    ])
def test_colocator_model_ts_type_read(tm5_aero_stp,ts_type_desired,
                                      ts_type, flex, raises):
    col = Colocator(**tm5_aero_stp)
    obs_var = 'od550aer'
    assert tm5_aero_stp['obs_vars'] == obs_var
    col.save_coldata = False
    col.flex_ts_type_gridded = flex
    col.ts_type = ts_type
    # Problem with saving since obs_id is different
    # from obs_data.contains_dataset[0]...
    col.model_ts_type_read = {obs_var : ts_type_desired}
    with raises:
        data = col._run_gridded_ungridded()
        assert isinstance(data, dict)
        assert obs_var in data
        coldata = data[obs_var]
        assert coldata.ts_type == ts_type
        assert coldata.meta['ts_type_src'][0] == 'daily'
        if not flex:
            assert coldata.meta['ts_type_src'][1] == ts_type_desired

def test_colocator_model_add_vars(tm5_aero_stp):
    col = Colocator(**tm5_aero_stp)
    model_var = 'abs550aer'
    obs_var = 'od550aer'
    col.save_coldata = False
    # Problem with saving since obs_id is different

    col.model_add_vars = {obs_var : model_var}
    data = col._run_gridded_ungridded(var_name=model_var)
    assert isinstance(data, dict)
    assert model_var in data
    coldata = data[model_var]
    assert coldata.var_name == ['od550aer', 'abs550aer']

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


def test_colocator_update_basedir_coldata(tmpdir):
    col = Colocator(raise_exceptions=True)

    basedir = os.path.join(tmpdir, 'basedir')
    assert not os.path.isdir(basedir)
    col.update(basedir_coldata=basedir)
    assert os.path.isdir(basedir)

@pytest.mark.parametrize('what,raises', [
    (dict(blaa=42), does_not_raise_exception()),
    (dict(obs_id='test', model_id='test'), does_not_raise_exception()),
    (dict(gridded_reader_id='test'), pytest.raises(ValueError)),
    (dict(gridded_reader_id={'test' : 42}), does_not_raise_exception()),
    ])
def test_colocator_update(what,raises):
    colref = Colocator(raise_exceptions=True)
    col = Colocator(raise_exceptions=True)
    with raises:
        col.update(**what)
        for key, val in what.items():
            if key in colref and isinstance(colref[key], dict):
                colref[key].update(val)
                assert col[key] == colref[key]
            else:
                assert col[key] == val


@pytest.mark.parametrize('gridded_gridded', [False, True])
def test_colocator_run(tm5_aero_stp, gridded_gridded):
    col = Colocator(**tm5_aero_stp)
    if gridded_gridded:
        col.obs_id = col.model_id
    col.run()
    coldata = col.data[col.model_id][col.obs_vars[0]]
    assert isinstance(coldata, ColocatedData)

def test_colocator__run_gridded_ungridded(tm5_aero_stp):
    col = Colocator(**tm5_aero_stp)
    data = col._run_gridded_ungridded()
    for ovar in col.obs_vars:
        assert ovar in data
        assert isinstance(data[ovar], ColocatedData)

def test_colocator__run_gridded_gridded(tm5_aero_stp):
    col = Colocator(**tm5_aero_stp)
    col.obs_id = col.model_id
    ovar = col.obs_vars[0]
    data = col._run_gridded_gridded(ovar)
    assert ovar in data
    assert isinstance(data[ovar], ColocatedData)
    assert isinstance(col.data, dict)
    assert col.data == {}

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
    assert col.stop == 9999

def test_colocator_with_obs_data_dir_ungridded():
    col = Colocator(save_coldata=False)
    col.model_id='TM5-met2010_CTRL-TEST'
    col.obs_id='AeronetSunV3L2Subset.daily'
    col.obs_vars='od550aer'
    col.ts_type='monthly'
    col.start = 2010
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
    col.start=2010
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
    col.start=2010
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

def test_model_add_vars(tm5_aero_stp):
    col = Colocator(**tm5_aero_stp)
    model_var = 'abs550aer'
    obs_var = 'od550aer'
    col.model_add_vars = {obs_var:model_var}
    model_reader = ReadGridded(col.model_id)
    var_matches = col._check_model_add_var(obs_var, model_reader, {})
    assert var_matches == {model_var: obs_var}
    var_matches = col._find_var_matches([obs_var], model_reader)
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
