from pyaerocom.units.logging import LoggingCallback
from pyaerocom.units import Unit
import logging


def test_callback_1(caplog):
    caplog.set_level(logging.INFO)

    Unit("1").convert(1, "1", callback=LoggingCallback())

    assert "Successfully converted unit of variable" not in caplog.text


def test_callback_2(caplog):
    caplog.set_level(logging.DEBUG)

    Unit("1").convert(1, "1", callback=LoggingCallback())

    assert "Successfully converted unit of variable" in caplog.text


def test_callback_3(caplog):
    caplog.set_level(logging.INFO)

    Unit("1").convert(1, "2", callback=LoggingCallback())

    assert "Successfully converted unit of variable" in caplog.text
