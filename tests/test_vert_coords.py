import numpy as np
import pytest

from pyaerocom.exceptions import CoordinateNameError
from pyaerocom.griddeddata import GriddedData
from pyaerocom.vert_coords import (
    AltitudeAccess,
    VerticalCoordinate,
    atmosphere_hybrid_sigma_pressure_coordinate_to_pressure,
    atmosphere_sigma_coordinate_to_pressure,
)


@pytest.fixture
def alt(data_tm5: GriddedData) -> AltitudeAccess:
    return AltitudeAccess(data_tm5)


@pytest.fixture
def sin_wave() -> np.ndarray:
    return np.sin(np.arange(20))


def test_atmosphere_sigma_coordinate_to_pressure_exceptions():
    with pytest.raises(ValueError):
        atmosphere_sigma_coordinate_to_pressure(1.0, 0, "")


@pytest.mark.parametrize(
    "sigma,ps,ptop,expected",
    (
        pytest.param(1.0, 0, 0.0, 0.0, id="ptop-is-float"),
        pytest.param(1.0, 0, np.ones(10), np.zeros(10), id="ptop-is-ndarray"),
        pytest.param(
            0.5,
            0.2,
            np.sin(np.arange(10)),
            np.asarray(
                [
                    0.1,
                    0.52073549,
                    0.55464871,
                    0.17056,
                    -0.27840125,
                    -0.37946214,
                    -0.03970775,
                    0.4284933,
                    0.59467912,
                    0.30605924,
                ]
            ),
            id="sin",
        ),
    ),
)
def test_atmosphere_sigma_coordinate_to_pressure(sigma, ps, ptop, expected):
    result = atmosphere_sigma_coordinate_to_pressure(sigma, ps, ptop)

    assert type(result) is type(ptop)
    if isinstance(result, np.ndarray):
        assert len(result) == len(ptop)

    assert result == pytest.approx(expected)


def test_atmosphere_hybrid_sigma_pressure_coordinate_to_pressure_exceptions():
    with pytest.raises(ValueError):
        atmosphere_hybrid_sigma_pressure_coordinate_to_pressure(np.ones(10), np.ones(5), 1, 0)


@pytest.mark.parametrize(
    "a,b,ps,p0,expected",
    (
        pytest.param(np.ones(10), np.ones(10), 1, None, 2, id="test-p0-is-none"),
        pytest.param(np.ones(10), np.ones(10), 1, 1, 2, id="test-p0-is-not-none"),
        pytest.param(
            np.sin(np.arange(10)),
            np.sin(np.arange(10)),
            0.5,
            0.5,
            np.asarray(
                [
                    0.0,
                    0.84147098,
                    0.90929743,
                    0.14112001,
                    -0.7568025,
                    -0.95892427,
                    -0.2794155,
                    0.6569866,
                    0.98935825,
                    0.41211849,
                ]
            ),
            id="sin",
        ),
    ),
)
def test_atmosphere_hybrid_sigma_pressure_coordinate_to_pressure(
    a: np.ndarray, b: np.ndarray, ps: float, p0: float | None, expected: np.ndarray
):
    result = atmosphere_hybrid_sigma_pressure_coordinate_to_pressure(a, b, ps, p0)

    assert len(a) == len(b) == len(result)
    assert result == pytest.approx(expected)


def test_VerticalCoordinate_exceptions():
    # Unsupported variable name during initialization.
    with pytest.raises(ValueError):
        VerticalCoordinate("jtlkjhsklrg")


def test_VerticalCoordinate_calc_pressure_exceptions():
    # Attempt calculating pressure for unsupported variable.
    vert = VerticalCoordinate("asc")
    with pytest.raises(CoordinateNameError):
        vert.calc_pressure(np.ones(5))


def test_VerticalCoordinate_lev_increases_with_alt_exception():
    vert = VerticalCoordinate("gph")
    with pytest.raises(ValueError, match="Failed to access information"):
        vert.lev_increases_with_alt


@pytest.mark.parametrize(
    "name,expected",
    (
        pytest.param("altitude", True, id="var-name-1"),
        pytest.param("atmosphere_sigma_coordinate", False, id="var-name-2"),
        pytest.param("atmosphere_hybrid_sigma_pressure_coordinate", False, id="var-name-3"),
        pytest.param("asc", False, id="standard-name-1"),
        pytest.param("z", True, id="standard-name-2"),
    ),
)
def test_VerticalCoordinate_lev_increases_with_alt(name: str, expected: bool):
    vert = VerticalCoordinate(name)

    assert vert.lev_increases_with_alt == expected


def test_AltitudeAccess_exceptions():
    with pytest.raises(ValueError):
        AltitudeAccess(None)


def test_AltitudeAccess_search_aux_coords(alt: AltitudeAccess):
    assert alt.search_aux_coords(["lat"])
    assert alt.search_aux_coords("lon")
    assert not alt.search_aux_coords("z")
    assert alt.search_aux_coords(["lat", "lon", "time"])
    assert not alt.search_aux_coords(["lat", "lon", "time", "z"])


def test_AltitudeAccess_search_aux_coords_exception(alt: AltitudeAccess):
    with pytest.raises(CoordinateNameError, match=r"Coordinate .* is not supported"):
        alt.search_aux_coords(["gkjfdshglk"])
