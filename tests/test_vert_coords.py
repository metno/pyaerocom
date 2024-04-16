import numpy as np
import pytest

from pyaerocom.griddeddata import GriddedData
from pyaerocom.vert_coords import *
from tests.fixtures.tm5 import data_tm5


@pytest.fixture
def alt(data_tm5: GriddedData):
    return AltitudeAccess(data_tm5)


def test_VerticalCoordinate_exceptions():
    # Unsupported variable name during initialization.
    with pytest.raises(ValueError):
        VerticalCoordinate("jtlkjhsklrg")

    # Attempt calculating pressure for unsupported variable.
    vert = VerticalCoordinate("asc")
    with pytest.raises(CoordinateNameError):
        vert.calc_pressure(np.ones(5))


def test_AltitudeAccess_exceptions():
    with pytest.raises(ValueError):
        AltitudeAccess(None)


def test_AltitudeAccess(alt: AltitudeAccess):
    assert True
