from getpass import getuser
from pathlib import Path

import pytest

from pyaerocom import const, tools
from pyaerocom.exceptions import DataSearchError


@pytest.fixture
def tmp_cache(tmp_path: Path) -> Path:  # type:ignore[misc]
    old_cache = const.CACHEDIR

    new_cache = tmp_path / "_cache" / getuser()
    new_cache.parent.mkdir()

    const.CACHEDIR = str(new_cache.parent)
    assert Path(const.CACHEDIR) == new_cache
    assert new_cache.is_dir()

    yield new_cache
    const.CACHEDIR = old_cache


def test_clear_cache(tmp_cache: Path):
    path = tmp_cache / "cache_dummy.pkl"
    path.write_bytes(b"")
    assert path.exists()

    tools.clear_cache()
    assert not path.exists()


def test_browse_database():
    with pytest.raises(DataSearchError):
        tools.browse_database("blaaa")
