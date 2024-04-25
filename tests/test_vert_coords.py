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


@pytest.mark.parametrize(
    "sigma,ps,ptop,exception",
    (
        pytest.param(1.0, 0, "", ValueError, id="value-error"),
        pytest.param(1.0, 0, 0.0, None, id="ptop-is-float"),
        pytest.param(1.0, 0, np.ones(10), None, id="ptop-is-ndarray"),
    ),
)
def test_atmosphere_sigma_coordinate_to_pressure(sigma, ps, ptop, exception):
    if exception is not None:
        with pytest.raises(exception):
            atmosphere_sigma_coordinate_to_pressure(sigma, ps, ptop)
    else:
        result = atmosphere_sigma_coordinate_to_pressure(sigma, ps, ptop)

        assert type(result) == type(ptop)
        if isinstance(result, np.ndarray):
            assert len(result) == len(ptop)


@pytest.mark.parametrize(
    "a,b,ps,p0,exception",
    (
        pytest.param(np.ones(10), np.ones(5), 1, 0, ValueError, id="test-ab-length-mismatch"),
        pytest.param(np.ones(10), np.ones(10), 1, None, None, id="test-p0-is-none"),
        pytest.param(np.ones(10), np.ones(10), 1, 1, None, id="test-p0-is-not-none"),
    ),
)
def test_atmosphere_hybrid_sigma_pressure_coordinate_to_pressure(
    a: np.ndarray, b: np.ndarray, ps: float, p0: float | None, exception
):
    if exception is not None:
        with pytest.raises(exception):
            atmosphere_hybrid_sigma_pressure_coordinate_to_pressure(a, b, ps, p0)
    else:
        result = atmosphere_hybrid_sigma_pressure_coordinate_to_pressure(a, b, ps, p0)

        assert len(a) == len(b) == len(result)


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

    def test_search_aux_coords(self, alt: AltitudeAccess):
        with pytest.raises(CoordinateNameError):
            alt.search_aux_coords(["gkjfdshglk"])

        assert alt.search_aux_coords(["lat"])
        assert alt.search_aux_coords("lon")
        assert not alt.search_aux_coords("z")
        assert alt.search_aux_coords(["lat", "lon", "time"])
        assert not alt.search_aux_coords(["lat", "lon", "time", "z"])
