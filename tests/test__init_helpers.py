import logging
from contextlib import nullcontext as does_not_raise_exception

import pytest

from pyaerocom import _init_helpers as mod
from pyaerocom import logger, print_log


def test__init_logger():
    logger, print_log = mod._init_logger()
    assert logger.getEffectiveLevel() == 50
    assert print_log.getEffectiveLevel() == 20


@pytest.mark.parametrize(
    "new_level,log,raises",
    [
        ("debug", None, does_not_raise_exception()),
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
    if log is None:
        _log = logger
    else:
        _log = log
    lvl = _log.getEffectiveLevel()
    with raises:
        mod.change_verbosity(new_level, log)
        log_level = _log.getEffectiveLevel()
        if isinstance(new_level, str):
            new_level = new_level.upper()
            log_level = logging.getLevelName(log_level)
        assert log_level == new_level
        # revoke changes
        _log.setLevel(lvl)
        assert _log.getEffectiveLevel() == lvl


### Functions for package initialisation
def test__init_supplemental():
    import os

    from pkg_resources import get_distribution

    version, fpath = mod._init_supplemental()
    assert version == get_distribution("pyaerocom").version
    assert os.path.normpath(fpath).endswith("/pyaerocom")
