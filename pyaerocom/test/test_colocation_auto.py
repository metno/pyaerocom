import pytest

from pyaerocom.conftest import testdata_unavail
from pyaerocom.colocation_auto import Colocator
from pyaerocom.io.read_emep import ReadEMEP

@testdata_unavail
def test_colocator_instantiate_gridded_reader(path_emep):
    col = Colocator(gridded_reader_id={'model':'ReadEMEP', 'obs':'ReadGridded'})
    col.filepath = path_emep['daily']
    model_id = 'model'
    col.model_id = model_id
    r = col.instantiate_gridded_reader(what='model')
    assert isinstance(r, ReadEMEP)
    assert r.filepath == col.filepath
    assert r.data_id == model_id

def test_colocator__get_gridded_reader_class():
    gridded_reader_id = {'model': 'ReadEMEP', 'obs': 'ReadEMEP'}
    col = Colocator(gridded_reader_id=gridded_reader_id)
    for what in ['model', 'obs']:
        assert col._get_gridded_reader_class(what=what) == ReadEMEP

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
