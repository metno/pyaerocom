import pytest
from numpy.testing import assert_allclose, assert_almost_equal

from pyaerocom import geodesy

from .conftest import etopo1_unavail, geonum_unavail, rg_unavail

TEST_LAT = 50.8
TEST_LON = 9


@rg_unavail
@pytest.mark.parametrize(
    "coords,countries",
    [((52, 12), ["Germany"]), ([(46.1956, 6.21125), (55.398, 10.3669)], ["France", "Denmark"])],
)
def test_get_country_info_coords(coords, countries):
    for i, res in enumerate(geodesy.get_country_info_coords(coords)):
        assert isinstance(res, dict)
        assert "country" in res
        assert res["country"] == countries[i]


def test_haversine():
    assert_allclose(geodesy.haversine(0, 15, 0, 16), 111.2, atol=0.1)


def test_is_within_radius_km():
    assert geodesy.is_within_radius_km(0, 15, 0, 16, 1000, 111.2)


# @pytest.mark.skip(reason='https://github.com/tkrajina/srtm.py/issues/51')
@geonum_unavail
def test_srtm_altitude():
    assert_almost_equal(geodesy.get_topo_altitude(TEST_LAT, TEST_LON), 207)


@geonum_unavail
@etopo1_unavail
def test_etopo_altitude():
    alt = geodesy.get_topo_altitude(TEST_LAT, TEST_LON, topo_dataset="etopo1")
    assert_almost_equal(alt, 217)
