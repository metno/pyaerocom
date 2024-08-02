from __future__ import annotations

import logging

import pytest

from pyaerocom._logging import change_verbosity


def get_level_value(logger: logging.Logger | None) -> int:
    """logging level of the first applicable StreamHandler"""

    while logger is not None:
        if not logger.hasHandlers():
            return logger.getEffectiveLevel()
        for handler in logger.handlers:
            if type(handler) is logging.StreamHandler:
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
    "level", ["debug", "info", "warning", "error", "critical", 10, 20, 30, 40, 50]
)
@pytest.mark.parametrize("name", ["pyaerocom.test", "pyaerocom.deep.nested.module"])
def test_change_verbosity(level: str | int, test_logger: logging.Logger):
    change_verbosity(level)
    if isinstance(level, int):
        assert get_level_value(test_logger) == level
    if isinstance(level, str):
        assert get_level_name(test_logger) == level.upper()


@pytest.mark.parametrize(
    "level,error",
    [
        (60, "invalid logging level 60"),
        ("blaaa", "Unknown level: 'BLAAA'"),
    ],
)
@pytest.mark.parametrize("name", ["pyaerocom.test", "pyaerocom.deep.nested.module"])
def test_change_verbosity_error(level: str | int, error: str, test_logger: logging.Logger):
    with pytest.raises(ValueError) as e:
        change_verbosity(level)
    assert str(e.value).startswith(error)
