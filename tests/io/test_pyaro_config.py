import pytest
from pathlib import Path

from pyaerocom.io.pyaro.pyaro_config import PyaroConfig



def test_default_path_exist():
    assert PyaroConfig._DEFAULT_CATALOG.exists()

def test_save(tmp_path):
    config = PyaroConfig(
        data_id = "test",
        filename_or_obj_or_url="test",
        filters=[],
        name_map={}
    )

    config.save("test", path=Path(tmp_path))
