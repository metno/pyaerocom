# -*- coding: utf-8 -*-
import pytest
from pyaerocom import const
from pyaerocom.conftest import does_not_raise_exception
from pyaerocom.io.readungriddedbase import ReadUngriddedBase

class DummyReader(ReadUngriddedBase):
    _FILEMASK = ".txt"
    DATA_ID = "Blaaa"
    __version__ = "0.01"
    PROVIDES_VARIABLES = ["od550aer"]
    REVISION_FILE = const.REVISION_FILE


    def __init__(self, data_id=None, data_dir=None):
        super(DummyReader, self).__init__(
                data_id, data_dir)

    @property
    def DEFAULT_VARS(self):
        return self.PROVIDES_VARIABLES

    @property
    def SUPPORTED_DATASETS(self):
        return [self.DATA_ID]

    @property
    def TS_TYPE(self):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError

    def read_file(self):
        raise NotImplementedError

@pytest.fixture(scope='module')
def dummy_reader():
    return DummyReader()

def test___init__template():
    with pytest.raises(TypeError):
        ReadUngriddedBase()

def test___init__dummy():
    dummy = DummyReader()
    assert dummy.data_id == 'Blaaa'

@pytest.mark.parametrize('key,val,raises', [
    ('_FILEMASK', '.txt', does_not_raise_exception()),
    ('TS_TYPE', None, pytest.raises(NotImplementedError)),
    ('__version__', '0.01', does_not_raise_exception()),
    ('DATA_ID', 'Blaaa', does_not_raise_exception()),
    ('SUPPORTED_DATASETS', ['Blaaa'], does_not_raise_exception()),
    ('PROVIDES_VARIABLES', ['od550aer'], does_not_raise_exception()),
    ('DEFAULT_VARS', ['od550aer'], does_not_raise_exception()),
    ('data_dir', None, pytest.raises(ValueError)),
    ('data_id', 'Blaaa', does_not_raise_exception()),
    ('REVISION_FILE', 'Revision.txt', does_not_raise_exception()),
    ('AUX_VARS', [], does_not_raise_exception()),
    ('data_id', 'Blaaa', does_not_raise_exception()),
    ])
def test_DummyReader_attrs(dummy_reader, key, val, raises):
    with raises:
        assert getattr(dummy_reader, key) == val

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)

