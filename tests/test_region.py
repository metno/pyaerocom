import pytest

from pyaerocom.region import Region, get_regions_coord


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
        ("SEA", -33.9249, 18.4241),
    ],
)
def test_does_not_contain_coordinate(region_name, lat, lon):
    reg = Region(region_name)
    assert not reg.contains_coordinate(lat, lon)


# This test needs work because Region() can accept almost any key in region_defs.py and they are not consistent.
# NAF, NAFRICA, N Africa, for example. Running in a debugger exposes the inconsistencies
@pytest.mark.parametrize(
    "region_name, lat, lon",
    [
        ("EUROPE", 48.864716, 2.349014),
        ("NAFRICA", 30.033333, 31.233334),
        ("ALL", 0.0, 0.0),
    ],
)
def test_get_regions_coord(region_name, lat, lon):
    reg = Region(region_name)
    assert reg.region_id in get_regions_coord(lat, lon)


@pytest.mark.parametrize(
    "region_name, lat, lon",
    [
        ("SAM", -33.447487, -70.673676),
        ("ASIA", 39.916668, 116.383331),
        ("OCN", 0.0, 0.0),
    ],
)
def test_get_regions_coord_with_supplied_regions_dict(region_name, lat, lon):
    oceans, sam, asia = Region("OCN"), Region("SAM"), Region("ASIA")
    candidate_regions = {"OCN": oceans, "SAM": sam, "ASIA": asia}
    reg = Region(region_name)
    assert reg.region_id in get_regions_coord(lat, lon, candidate_regions)
