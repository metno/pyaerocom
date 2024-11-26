from __future__ import annotations

from pathlib import Path

import pytest

from pyaerocom.io.pyaro.pyaro_config import PyaroConfig


def get_test_config() -> PyaroConfig:
    config = PyaroConfig(
        name="test",
        reader_id="test",
        filename_or_obj_or_url="test",
        filters={},
        name_map={},
    )
    return config


def get_existing_config() -> PyaroConfig:
    config = PyaroConfig(
        name="aeronetsun_test",
        reader_id="test",
        filename_or_obj_or_url="test",
        filters={},
        name_map={},
    )
    return config


def test_default_path_exist():
    assert PyaroConfig._DEFAULT_CATALOG.exists()


def test_kwargs(pyaro_testconfig_kwargs, pyaro_kwargs):
    kwargs = pyaro_testconfig_kwargs.model_extra["columns"]
    assert kwargs == pyaro_kwargs


def test_save(tmp_path):
    config = get_test_config()
    config.save(path=Path(tmp_path))


def test_list_configs(tmp_path):
    config = get_test_config()
    config.save(path=Path(tmp_path))

    private_configs = list(PyaroConfig.load_catalog(tmp_path / "catalog.yaml").keys())
    default_configs = list(PyaroConfig.load_catalog().keys())

    configs = default_configs + private_configs

    assert configs == PyaroConfig.list_configs(tmp_path / "catalog.yaml")


def test_load(tmp_path):
    config = get_test_config()
    config.save(path=Path(tmp_path))

    new_config = PyaroConfig.load("test", filepath=tmp_path / "catalog.yaml")

    assert config == new_config


#########################################################
#   Tests for expected exceptions
#########################################################
def test_save_path_error(tmp_path):
    config = get_test_config()
    with pytest.raises(ValueError, match="must be a directory"):
        config.save(path=Path(tmp_path) / "catalog.yaml")


def test_save_duplicate_name_error(tmp_path):
    config = get_test_config()
    config.save(path=Path(tmp_path))
    with pytest.raises(ValueError, match="already exists in catalog"):
        config.save(path=Path(tmp_path))


def test_save_name_in_default_error(tmp_path):
    config = get_existing_config()
    with pytest.raises(ValueError, match="already exists in default"):
        config.save(path=Path(tmp_path))


def test_load_filepath_error(tmp_path):
    config = get_test_config()
    with pytest.raises(ValueError, match="is a directory not a file"):
        config.load("test", tmp_path)


def test_load_no_catalog_error(tmp_path):
    config = get_test_config()
    with pytest.raises(ValueError, match="No catalog with this name exists"):
        config.load("test", tmp_path / "catalog.yaml")


def test_load_no_config_error(tmp_path):
    config = get_test_config()
    config.save(path=Path(tmp_path))
    with pytest.raises(ValueError, match="was not found in any catalogs"):
        config.load("test2", tmp_path / "catalog.yaml")
