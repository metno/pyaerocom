from pathlib import Path

import iris
import xarray as xr

import pyaerocom.helpers_landsea_masks as lsm
from pyaerocom import const
from tests.conftest import lustre_avail

TEST_REGIONS = const.HTAP_REGIONS[:2]


def test_available_region_masks():
    assert lsm.available_htap_masks() == [
        "PAN",
        "EAS",
        "NAF",
        "MDE",
        "LAND",
        "SAS",
        "SPO",
        "OCN",
        "SEA",
        "RBU",
        "EEUROPE",
        "NAM",
        "WEUROPE",
        "SAF",
        "USA",
        "SAM",
        "EUR",
        "NPO",
        "MCA",
    ]


@lustre_avail
def test_download_htap_masks():
    paths = [Path(mask) for mask in lsm.download_htap_masks(TEST_REGIONS)]
    assert bool(paths)
    assert all(path.exists() for path in paths)
    assert {path.parts[-3] for path in paths} == {"MyPyaerocom"}
    assert {path.parts[-2] for path in paths} == {"filtermasks"}
    assert [path.name for path in paths] == ["PANhtap.0.1x0.1deg.nc", "EAShtap.0.1x0.1deg.nc"]


def test_get_htap_mask_files():
    paths = [Path(mask) for mask in lsm.get_htap_mask_files(*TEST_REGIONS)]
    assert [path.name for path in paths] == ["PANhtap.0.1x0.1deg.nc", "EAShtap.0.1x0.1deg.nc"]


def test_load_region_mask_xr():
    mask = lsm.load_region_mask_xr(*TEST_REGIONS)
    assert isinstance(mask, xr.DataArray)
    pixels = int(mask.sum())
    assert pixels == 193355


def test_load_region_mask_iris():
    mask = lsm.load_region_mask_iris(*TEST_REGIONS)
    assert isinstance(mask, iris.cube.Cube)
    pixels = int(mask.data.sum())
    assert pixels == 193355


def test_get_mask_value():
    mask = lsm.load_region_mask_xr("WEUROPE")

    assert lsm.get_mask_value(50, 5, mask)
    assert not lsm.get_mask_value(50, 15, mask)


def test_check_all_htap_available():
    should_be = [
        "EAShtap.0.1x0.1deg.nc",
        "EEUROPEhtap.0.1x0.1deg.nc",
        "EURhtap.0.1x0.1deg.nc",
        "LANDhtap.0.1x0.1deg.nc",
        "MCAhtap.0.1x0.1deg.nc",
        "MDEhtap.0.1x0.1deg.nc",
        "NAFhtap.0.1x0.1deg.nc",
        "NAMhtap.0.1x0.1deg.nc",
        "NPOhtap.0.1x0.1deg.nc",
        "OCNhtap.0.1x0.1deg.nc",
        "PANhtap.0.1x0.1deg.nc",
        "RBUhtap.0.1x0.1deg.nc",
        "SAFhtap.0.1x0.1deg.nc",
        "SAMhtap.0.1x0.1deg.nc",
        "SAShtap.0.1x0.1deg.nc",
        "SEAhtap.0.1x0.1deg.nc",
        "SPOhtap.0.1x0.1deg.nc",
        "USAhtap.0.1x0.1deg.nc",
        "WEUROPEhtap.0.1x0.1deg.nc",
    ]

    files = lsm.check_all_htap_available()
    assert sorted(Path(file).name for file in files) == should_be
