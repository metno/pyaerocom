import pytest

from pyaerocom.conftest import testdata_unavail
from pyaerocom.colocation_auto import Colocator
from pyaerocom.io.read_emep import ReadEMEP
from pyaerocom.io.readgridded import ReadGridded

@pytest.mark.parametrize('reader_id,reader_class', [
    ('ReadEMEP', ReadEMEP),
    ('ReadGridded', ReadGridded)
    ])
def test_colocator_reader(reader_id, reader_class):
    col = Colocator(gridded_reader_id=reader_id)
    reader = col.get_gridded_reader()
    assert reader == reader_class

@testdata_unavail
def test_colocator_instantiate_model_reader(path_emep):
    col = Colocator(gridded_reader_id='ReadEMEP')
    col.filepath = path_emep['daily']
    r = col.instantiate_model_reader()
    assert isinstance(r, ReadEMEP)
    assert r.filepath == col.filepath

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
