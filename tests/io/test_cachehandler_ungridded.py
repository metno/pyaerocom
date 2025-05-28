from pathlib import Path

import pytest

from pyaerocom import UngriddedData
from pyaerocom.io import ReadAeronetSunV3
from pyaerocom.io.cachehandler_ungridded import CacheHandlerUngridded
from tests.conftest import lustre_avail
from pyaerocom.io.pyaro.pyaro_config import PyaroConfig
from pyaerocom.io.pyaro.read_pyaro import ReadPyaro


@pytest.fixture(scope="module")
def cache_handler():
    return CacheHandlerUngridded()


@lustre_avail
def test_cache_dir(cache_handler: CacheHandlerUngridded):
    cache_path = Path(cache_handler.cache_dir)
    comps = cache_path.parts
    assert comps[-2] == "_cache"
    assert comps[-3] == "MyPyaerocom"


def test_reload_custom(
    cache_handler: CacheHandlerUngridded, aeronetsunv3lev2_subset: UngriddedData, tmp_path: Path
):
    path = tmp_path / "test_manual_caching.pkl"
    cache_handler.write(aeronetsunv3lev2_subset, var_or_file_name=path.name, cache_dir=path.parent)
    assert path.exists()
    cache_handler.check_and_load(var_or_file_name=path.name, cache_dir=path.parent)
    assert cache_handler.loaded_data[path.name].shape == aeronetsunv3lev2_subset.shape


@pytest.mark.dependency
def test_reload(
    cache_handler: CacheHandlerUngridded,
    aeronetsunv3lev2_subset: UngriddedData,
    aeronet_sun_subset_reader: ReadAeronetSunV3,
):
    cache_handler.reader = aeronet_sun_subset_reader
    cache_handler.write(aeronetsunv3lev2_subset, var_or_file_name="od550aer")
    assert Path(cache_handler.file_path("od550aer")).exists()

    cache_handler.check_and_load(var_or_file_name="od550aer")
    subset = aeronetsunv3lev2_subset.extract_var("od550aer")
    assert "od550aer" in cache_handler.loaded_data

    reloaded = cache_handler.loaded_data["od550aer"]
    assert isinstance(reloaded, UngriddedData)
    assert reloaded.shape == subset.shape


def test_reload_pyaro(cache_handler: CacheHandlerUngridded, pyaro_test_data_file):
    config0 = PyaroConfig(
        reader_id="csv_timeseries",
        filename_or_obj_or_url=str(pyaro_test_data_file),
        name="test",
        name_map={
            "NO": "concno",
        },
        post_processing=[
            "concNno_from_concno",
        ],
        filters=dict(),
    )

    reader0 = ReadPyaro(config0)
    cache_handler.reader = reader0
    has_data = cache_handler.check_and_load("concno")
    assert not has_data, "Data was present"

    data = reader0.read("concno")
    _outpath = cache_handler.write(data, var_or_file_name="concno")

    has_data = cache_handler.check_and_load("concno")
    assert has_data, "Data should not be present"
    assert cache_handler.loaded_data.get("concno") is not None

    reader1 = ReadPyaro(config0)
    cache_handler.reader = reader1
    has_data = cache_handler.check_and_load("concno")
    assert has_data, "Data should be present"

    # Enable a filter which should invalidate the cache
    config2 = config0.model_copy()
    config2.filters["countries"] = {"include": "DE"}

    reader2 = ReadPyaro(config2)
    cache_handler.reader = reader2
    has_data = cache_handler.check_and_load("concno")
    assert not has_data, "Data should not be present"

    data = reader2.read("concno")
    _outpath = cache_handler.write(data, var_or_file_name="concno")
    has_data = cache_handler.check_and_load("concno")
    assert has_data, "Data should be present"
