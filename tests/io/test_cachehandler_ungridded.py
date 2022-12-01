from pathlib import Path

import pytest

from pyaerocom import UngriddedData
from pyaerocom.io import ReadAeronetSunV3
from pyaerocom.io.cachehandler_ungridded import CacheHandlerUngridded
from tests.conftest import lustre_avail


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
