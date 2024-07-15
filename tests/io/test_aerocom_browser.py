import pytest

from pyaerocom.io.aerocom_browser import AerocomBrowser


@pytest.mark.parametrize(
    "searchstr,endswith",
    [
        ("TM5*TEST", "modeldata/TM5-met2010_CTRL-TEST/renamed"),
        ("AeronetSunV3L2Subset.daily", "obsdata/AeronetSunV3Lev2.daily/renamed"),
    ],
)
def test_find_data_dir(searchstr, endswith):
    browser = AerocomBrowser()

    data_dir = browser.find_data_dir(searchstr)
    assert data_dir.endswith(endswith)
