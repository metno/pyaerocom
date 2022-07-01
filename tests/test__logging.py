from __future__ import annotations

import logging

import pytest

from pyaerocom._logging import LOGGING_CONFIG, change_verbosity


def get_level_value(logger: logging.Logger | None) -> int:
    """logging level of the first applicable StreamHandler"""

    while logger is not None:
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
    assert logging.getLevelName(handler.level) == LOGGING_CONFIG["file_level"]


def test_pya_logger():
    logger = logging.getLogger("pyaerocom")
    assert len(logger.handlers) == 1
    handler = logger.handlers[0]
    assert type(handler) == logging.StreamHandler
    assert logging.getLevelName(handler.level) == LOGGING_CONFIG["console_level"]


@pytest.mark.parametrize(
    "name,level",
    [
        ("pyaerocom.test", LOGGING_CONFIG["console_level"]),
        ("pyaerocom.deep.nested.module", LOGGING_CONFIG["console_level"]),
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
