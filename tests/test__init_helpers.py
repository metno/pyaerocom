import pytest

from pyaerocom import _init_helpers as mod
from pyaerocom import logger, print_log


def test_LOGLEVELS():
    assert mod.LOGLEVELS == {"debug": 10, "info": 20, "warning": 30, "error": 40, "critical": 50}


def test__init_logger():
    logger, print_log = mod._init_logger()
    assert logger.getEffectiveLevel() == 50
    assert print_log.getEffectiveLevel() == 20


@pytest.mark.parametrize(
    "new_level", ["debug", "info", "warning", "error", "critical", 10, 20, 30, 40, 50]
)
@pytest.mark.parametrize("log", [logger, print_log])
def test_change_verbosity(new_level, log):
    old_level = log.getEffectiveLevel()

    mod.change_verbosity(new_level, log)
    assert log.getEffectiveLevel() == mod.LOGLEVELS.get(new_level, new_level)

    # revoke changes
    log.setLevel(old_level)
    assert log.getEffectiveLevel() == old_level


@pytest.mark.parametrize("new_level", [60, "blaaa"])
@pytest.mark.parametrize("log", [logger, print_log])
def test_change_verbosity_error(new_level, log):
    with pytest.raises(ValueError):
        mod.change_verbosity(new_level, log)
