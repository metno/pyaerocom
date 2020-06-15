import pytest
from pyaerocom.conftest import lustre_unavail, testdata_unavail
from pyaerocom.io.read_emep import ReadEMEP
from pyaerocom.griddeddata import GriddedData
from pyaerocom.colocation import colocate_gridded_gridded
from pyaerocom.colocation import ColocatedData

def test_read_emep():
    r = ReadEMEP()
    assert r.data_id == None
    assert r.vars_provided == []
    assert r.filepath == None


def test___str__():
    r = ReadEMEP()
    r_string = str(r)
    assert isinstance(r_string, str)

@testdata_unavail
def test_read_emep_data(path_emep):
    path = path_emep['daily']
    data_id = 'EMEP_v5'
    r = ReadEMEP(filepath=path, data_id=data_id)

    vars_provided = r.vars_provided
    assert isinstance(vars_provided, list)
    assert 'vmro3' in vars_provided

    data = r.read_var('vmro3', ts_type='daily')
    assert isinstance(data, GriddedData)
    assert data.time.long_name == 'time'
    assert data.time.standard_name == 'time'

    assert data.data_id == data_id
    assert data.from_files == path

# @testdata_unavail
# def test_read_emep_alias(path_emep):
#     filepath = path_emep['monthly']
#     r = ReadEMEP(path_emep['monthly'])
#     data_emep = r.read_var('sconcpm10', ts_type='monthly')

@testdata_unavail
def test_read_emep_directory(path_emep):
    data_dir = path_emep['data_dir']
    r = ReadEMEP(data_dir=data_dir)
    assert r.data_dir == data_dir
    vars_provided = r.vars_provided
    assert 'vmro3' in vars_provided
    assert 'concpm10' in vars_provided
    assert 'concno2' in vars_provided
    paths = r._get_paths()
    assert len(paths) == 3
    gridded = r.read_var('concno2',ts_type='monthly')

from contextlib import contextmanager

@contextmanager
def does_not_raise_exception():
    yield

@testdata_unavail
def test__infer_ts_type(path_emep):
    r = ReadEMEP(data_dir=path_emep['data_dir'])
    with pytest.raises(ValueError):
        # r._infer_ts_type()

        r.read_var('concno2')
    with does_not_raise_exception():

        r = ReadEMEP(filepath=path_emep['monthly'])
        ts_type = r._infer_ts_type()
        assert ts_type == 'monthly'
        # r.read_var('concno2')
        # assert gridded.ts_type == 'monthly'

@testdata_unavail
def test__load_gridded(path_emep):
    filepath = path_emep['monthly']
    r = ReadEMEP(filepath)
    gridded = r._load_gridded('concno2', filepath, 'monthly')
    assert isinstance(gridded, GriddedData)

@pytest.mark.parametrize('filename,ts_type', [
    ('Base_month.nc', 'monthly'),
    ('Base_day.nc', 'daily'),
    ('Base_fullrun', 'yearly')
    ])
def test__ts_type_from_filename(filename, ts_type):
    r = ReadEMEP()
    assert r._ts_type_from_filename(filename) == ts_type

def test__preprocess_units():
    units = ''
    prefix = 'AOD'
    assert ReadEMEP()._preprocess_units(units, prefix) == '1'

    units = 'mgS/m2'
    catch_error = False
    try:
        ReadEMEP()._preprocess_units(units)
    except NotImplementedError as e:
        catch_error = True
    assert catch_error == True

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
