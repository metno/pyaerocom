import pytest

from pyaerocom.region import Region


@pytest.mark.parametrize(
    "region_name, lat, lon",
    [
        ("ALL", 0, 0),
        ("NAM", 39.7555, -105.2211),
        ("NAM", 19.5364, -155.5765),
        ("PAN", -37.8136, 144.9631),
        ("RBU", 50.4501, 30.5234),
        ("EUR", 59.9139, 10.7522),
    ],
)
def test_contains_coordinate(region_name, lat, lon):
    reg = Region(region_name)
    assert reg.contains_coordinate(lat, lon)


@pytest.mark.parametrize(
    "region_name, lat, lon",
    [
        ("EAS", 0, 0),
        ("MCA", 51.5072, 0.1276),
        ("MDE", 10.4806, -66.9036),
        ("SEA", 33.9249, 18.4241),
    ],
)
def test_does_not_contain_coordinate(region_name, lat, lon):
    reg = Region(region_name)
    assert not reg.contains_coordinate(lat, lon)
