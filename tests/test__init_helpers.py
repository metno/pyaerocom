from __future__ import annotations

import logging
from contextlib import nullcontext as does_not_raise_exception

import pytest

from pyaerocom import _init_helpers as mod
from pyaerocom import logger, print_log


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


def test__init_logger():
    logger, print_log = mod._init_logger()
    check_loggger_level(logger, 50)
    check_loggger_level(print_log, 20)


@pytest.mark.parametrize(
    "new_level,log,raises",
    [
        ("debug", logger, does_not_raise_exception()),
        ("info", logger, does_not_raise_exception()),
        ("warning", logger, does_not_raise_exception()),
        ("error", logger, does_not_raise_exception()),
        ("critical", logger, does_not_raise_exception()),
        ("debug", print_log, does_not_raise_exception()),
        ("info", print_log, does_not_raise_exception()),
        ("warning", print_log, does_not_raise_exception()),
        ("error", print_log, does_not_raise_exception()),
        ("critical", print_log, does_not_raise_exception()),
        (10, print_log, does_not_raise_exception()),
        (20, print_log, does_not_raise_exception()),
        (30, print_log, does_not_raise_exception()),
        (40, print_log, does_not_raise_exception()),
        (50, print_log, does_not_raise_exception()),
        (60, print_log, pytest.raises(ValueError)),
        ("blaaa", print_log, pytest.raises(ValueError)),
    ],
)
def test_change_verbosity(new_level, log, raises):
    with raises:
        mod.change_verbosity(new_level, log)
        check_loggger_level(log, new_level)
        # revoke changes
        mod.change_verbosity(logging.CRITICAL, log)
        check_loggger_level(log, "critical")


### Functions for package initialisation
def test__init_supplemental():
    import os

    from pkg_resources import get_distribution

    version, fpath = mod._init_supplemental()
    assert version == get_distribution("pyaerocom").version
    assert os.path.normpath(fpath).endswith("/pyaerocom")
