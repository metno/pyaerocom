from __future__ import annotations

import logging
from contextlib import nullcontext as does_not_raise_exception

import pytest

from pyaerocom import _init_helpers as mod


def get_level_value(logger: logging.Logger) -> int:

    while logger:
        mod.logging.critical(f"{logger=}")
        if not logger.hasHandlers():
            return logger.getEffectiveLevel()
        for handler in logger.handlers:
            if type(handler) == logging.StreamHandler:
                mod.logging.critical(f"found {handler.name} {handler.level}")
                return handler.level
        if not logger.propagate:
            return logging.NOTSET
        logger = logger.parent

    return logging.NOTSET


def get_level_name(logger: logging.Logger) -> str:
    level = get_level_value(logger)
    return logging.getLevelName(level)


@pytest.fixture
def test_logger(name: str | None) -> logging.Logger:
    return logging.getLogger(name)


@pytest.mark.parametrize(
    "name,level",
    [
        ("pyaerocom.test", get_level_value(mod.logger)),
        ("pyaerocom.deep.nested.module", get_level_value(mod.logger)),
        ("other.module", logging.NOTSET),
        (None, logging.NOTSET),
    ],
)
def test_logger_level(test_logger: logging.Logger, level: int):
    assert get_level_value(test_logger) == level


@pytest.mark.parametrize(
    "level,raises",
    [
        ("debug", does_not_raise_exception()),
        ("info", does_not_raise_exception()),
        ("warning", does_not_raise_exception()),
        ("error", does_not_raise_exception()),
        ("critical", does_not_raise_exception()),
        (10, does_not_raise_exception()),
        (20, does_not_raise_exception()),
        (30, does_not_raise_exception()),
        (40, does_not_raise_exception()),
        (50, does_not_raise_exception()),
        (60, pytest.raises(ValueError)),
        ("blaaa", pytest.raises(ValueError)),
    ],
)
@pytest.mark.parametrize("name", ["pyaerocom", "pyaerocom.test"])
def test_change_verbosity(level: str | int, test_logger: logging.Logger, raises):
    with raises:
        mod.change_verbosity(level, test_logger)
        if isinstance(level, int):
            assert get_level_value(test_logger) == level
        if isinstance(level, str):
            assert get_level_name(test_logger) == level.upper()


### Functions for package initialisation
def test__init_supplemental():
    import os

    from pkg_resources import get_distribution

    version, fpath = mod._init_supplemental()
    assert version == get_distribution("pyaerocom").version
    assert os.path.normpath(fpath).endswith("/pyaerocom")
