import pytest

from pyaerocom import const
from pyaerocom.io.readungriddedbase import ReadUngriddedBase


class DummyReader(ReadUngriddedBase):
    _FILEMASK = ".txt"
    DATA_ID = "Blaaa"
    __version__ = "0.01"
    PROVIDES_VARIABLES = ["od550aer"]
    REVISION_FILE = const.REVISION_FILE

    def __init__(self, data_id=None, data_dir=None):
        super().__init__(data_id, data_dir)

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


@pytest.fixture(scope="module")
def dummy_reader():
    return DummyReader()


def test___init__template():
    with pytest.raises(TypeError):
        ReadUngriddedBase()


def test___init__dummy():
    dummy = DummyReader()
    assert dummy.data_id == "Blaaa"


@pytest.mark.parametrize(
    "key,val",
    [
        ("_FILEMASK", ".txt"),
        ("__version__", "0.01"),
        ("DATA_ID", "Blaaa"),
        ("SUPPORTED_DATASETS", ["Blaaa"]),
        ("PROVIDES_VARIABLES", ["od550aer"]),
        ("DEFAULT_VARS", ["od550aer"]),
        ("data_id", "Blaaa"),
        ("REVISION_FILE", "Revision.txt"),
        ("AUX_VARS", []),
        ("data_id", "Blaaa"),
    ],
)
def test_DummyReader_attrs(dummy_reader, key, val):
    assert getattr(dummy_reader, key) == val


@pytest.mark.parametrize(
    "key,exception,error",
    [
        pytest.param("TS_TYPE", NotImplementedError, "", id="NotImplementedError"),
        pytest.param(
            "data_dir", ValueError, "Observation network ID Blaaa does not exist", id="ValueError"
        ),
    ],
)
def test_DummyReader_attrs_error(dummy_reader, key, exception, error: str):
    with pytest.raises(exception) as e:
        getattr(dummy_reader, key)
    assert str(e.value) == error
