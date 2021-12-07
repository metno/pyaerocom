from __future__ import annotations

import logging
from contextlib import nullcontext as does_not_raise_exception

import pytest

from pyaerocom import _init_helpers as mod


def check_loggger_level(logger: logging.Logger, level: int | str):
    assert logger.hasHandlers()
    assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)
    if isinstance(level, int):
        assert any(
            h.level == level for h in logger.handlers if isinstance(h, logging.StreamHandler)
        )
    if isinstance(level, str):
        assert any(
            logging.getLevelName(h.level) == level.upper()
            for h in logger.handlers
            if isinstance(h, logging.StreamHandler)
        )


@pytest.fixture
def test_logger() -> logging.Logger:
    return mod._init_logger(logging.getLogger("test"))


def test__init_logger(test_logger: logging.Logger):
    check_loggger_level(test_logger, logging.INFO)


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
def test_change_verbosity(level: str | int, test_logger: logging.Logger, raises):
    with raises:
        mod.change_verbosity(level, test_logger)
        check_loggger_level(test_logger, level)


### Functions for package initialisation
def test__init_supplemental():
    import os

    from pkg_resources import get_distribution

    version, fpath = mod._init_supplemental()
    assert version == get_distribution("pyaerocom").version
    assert os.path.normpath(fpath).endswith("/pyaerocom")
