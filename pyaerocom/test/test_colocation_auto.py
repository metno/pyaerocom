import os
import pytest

from pyaerocom.conftest import TESTDATADIR, does_not_raise_exception, testdata_unavail

from pyaerocom import Colocator, ColocatedData, GriddedData, UngriddedData
from pyaerocom.io import ReadGridded, ReadEMEP
from pyaerocom.exceptions import DataCoverageError
from pyaerocom.io.aux_read_cubes import add_cubes

@pytest.fixture(scope='function')
def col_tm5_aero(model_id='TM5-met2010_CTRL-TEST', obs_id='AeronetSunV3L2Subset.daily',
                 obs_vars='od550aer'):
    coloc = Colocator(model_id=model_id, obs_id=obs_id, obs_vars=obs_vars)
    coloc.raise_exceptions = True
    coloc.reanalyse_existing = True
    coloc.start = 2010
    return coloc

@pytest.fixture(scope='function')
def col():
    return Colocator(raise_exceptions=True, reanalyze_existing=True)


def test_colocator(col):
    assert isinstance(col, Colocator)
    col.obs_vars = 'var'
    assert isinstance(col.obs_vars, str)

def test_colocator_init_basedir_coldata(tmpdir):
    basedir = os.path.join(tmpdir, 'basedir')
    col = Colocator(raise_exceptions=True, basedir_coldata=basedir)
    assert os.path.isdir(basedir)

def test_colocator__check_add_model_read_aux():
    coloc = Colocator(raise_exceptions=True)
    r = ReadGridded('TM5-met2010_CTRL-TEST')

    assert not coloc._check_add_model_read_aux('od550aer', r)

    coloc.model_read_aux = {
        'od550aer' : dict(
            vars_required=['od550aer', 'od550aer'],
            fun=add_cubes)}
    assert coloc._check_add_model_read_aux('od550aer', r)

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
        col = Colocator(filter_name='WORLD')
    with pytest.raises(Exception):
        col = Colocator(filter_name='invalid')

def test_colocator_basedir_coldata(tmpdir):
    basedir = os.path.join(tmpdir, 'test')
    col = Colocator(raise_exceptions=True)
    col.basedir_coldata = basedir
    assert not os.path.isdir(basedir)

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

def test_colocator_read_ungridded():
    col = Colocator(raise_exceptions=True)
    obs_id = 'AeronetSunV3L2Subset.daily'
    obs_var = 'od550aer'
    col.obs_filters = {'longitude' : [-30, 30]}
    col.obs_id = obs_id
    col.read_opts_ungridded = {'last_file' : 10}
    with pytest.raises(DataCoverageError):
        data = col.read_ungridded(obs_var) # Why is this raised?
        # read_ungridded expects a list of one or more variables!
        # Should check for str and convert to list?
        # Should read_ungridded and read_model_data have same arguments?
    data = col.read_ungridded([obs_var])
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

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
