from __future__ import annotations

import logging
from contextlib import nullcontext as does_not_raise_exception

import pytest

from pyaerocom import _init_helpers as mod


def get_level_value(logger: logging.Logger) -> int:
    """logging level of the first applicable StreamHandler"""

    while logger:
        if not logger.hasHandlers():
            return logger.getEffectiveLevel()
        for handler in logger.handlers:
            if type(handler) == logging.StreamHandler:
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


def test_root_logger():
    logger = logging.getLogger()
    assert any(isinstance(h, logging.FileHandler) for h in logger.handlers)
    handler = next(h for h in logger.handlers if isinstance(h, logging.FileHandler))
    assert logging.getLevelName(handler.level) == mod.LOGGING_CONFIG["file_level"]


def test_pya_logger():
    logger = logging.getLogger("pyaerocom")
    assert len(logger.handlers) == 1
    handler = logger.handlers[0]
    assert type(handler) == logging.StreamHandler
    assert logging.getLevelName(handler.level) == mod.LOGGING_CONFIG["console_level"]


@pytest.mark.parametrize(
    "name,level",
    [
        ("pyaerocom.test", mod.LOGGING_CONFIG["console_level"]),
        ("pyaerocom.deep.nested.module", mod.LOGGING_CONFIG["console_level"]),
        ("other.module", logging.NOTSET),
        (None, logging.NOTSET),
    ],
)
def test_logger_level(test_logger: logging.Logger, level: int | str):
    if isinstance(level, int):
        assert get_level_value(test_logger) == level
    if isinstance(level, str):
        assert get_level_name(test_logger) == level.upper()


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
@pytest.mark.parametrize("name", ["pyaerocom.test", "pyaerocom.deep.nested.module"])
def test_change_verbosity(level: str | int, test_logger: logging.Logger, raises):
    with raises:
        mod.change_verbosity(level)
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
