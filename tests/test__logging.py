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
