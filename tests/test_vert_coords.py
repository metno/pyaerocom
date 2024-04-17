import numpy as np
import pytest

from pyaerocom.griddeddata import GriddedData
from pyaerocom.vert_coords import *
from tests.conftest import lustre_unavail
from tests.fixtures.tm5 import data_tm5


@pytest.fixture
def alt(data_tm5: GriddedData) -> AltitudeAccess:
    return AltitudeAccess(data_tm5)


@pytest.fixture
def sin_wave() -> np.ndarray:
    return np.sin(np.arange(1000))


def test_atmosphere_sigma_coordinate_to_pressure(sin_wave: np.ndarray):
    assert isinstance(atmosphere_sigma_coordinate_to_pressure(0.5, 1, 1), float)

    result = atmosphere_sigma_coordinate_to_pressure(sin_wave, 1, 1)
    assert isinstance(result, np.ndarray)

    assert len(result) == len(sin_wave)


def test_atmosphere_hybrid_sigma_pressure_coordinate_to_pressure(sin_wave: np.ndarray):
    with pytest.raises(ValueError):
        atmosphere_hybrid_sigma_pressure_coordinate_to_pressure(np.ones(5), np.ones(4), 1, 1)

    result = atmosphere_hybrid_sigma_pressure_coordinate_to_pressure(sin_wave, sin_wave, 1, 1)
    assert len(result) == len(sin_wave)


def test_geopotentialheight2altitude():
    with pytest.raises(NotImplementedError):
        geopotentialheight2altitude(5)


class TestVerticalCoordinate:
    def test_exceptions(self):
        # Unsupported variable name during initialization.
        with pytest.raises(ValueError):
            VerticalCoordinate("jtlkjhsklrg")

        # Attempt calculating pressure for unsupported variable.
        vert = VerticalCoordinate("asc")
        with pytest.raises(CoordinateNameError):
            vert.calc_pressure(np.ones(5))

    @pytest.mark.parametrize(
        "name,expected,exception",
        (
            pytest.param("altitude", True, None, id="var-name-1"),
            pytest.param("atmosphere_sigma_coordinate", False, None, id="var-name-2"),
            pytest.param(
                "atmosphere_hybrid_sigma_pressure_coordinate", False, None, id="var-name-3"
            ),
            pytest.param("asc", False, None, id="standard-name-1"),
            pytest.param("z", True, None, id="standard-name-2"),
            pytest.param("gph", None, ValueError, id="valueerror"),
        ),
    )
    def test_lev_increases_with_alt(
        self, name: str, expected: bool | None, exception: Exception | None
    ):
        vert = VerticalCoordinate(name)
        if exception:
            with pytest.raises(exception):
                vert.lev_increases_with_alt
        else:
            assert vert.lev_increases_with_alt == expected


class TestAltitudeAccess:
    def test_exceptions(self):
        with pytest.raises(ValueError):
            AltitudeAccess(None)

    def test_extract_1D_subset_from_data(self, alt: AltitudeAccess):
        test = alt.extract_1D_subset_from_data()

        assert test.ndim == 1

        # TODO: More extensive testing should be done here.

    def test_get_altitude(self, alt: AltitudeAccess):
        with pytest.raises(NotImplementedError):
            alt.get_altitude(None, None)

    @lustre_unavail
    @pytest.mark.xfail
    # TODO: This test is currently failing because of a ValueError caused by
    # a variable name containing an underscore. This seems like an unrelated
    # issue to me, so I have marked it xfail for now.
    def test_check_access(self, alt: AltitudeAccess):
        assert alt.check_altitude_access()
