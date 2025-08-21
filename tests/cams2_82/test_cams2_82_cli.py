from datetime import date

import pytest

from pyaerocom.scripts.cams2_82.cli import date_range, make_period, vpro_subpaths


@pytest.mark.parametrize(
    "date1,date2,result",
    [
        pytest.param(date(2025, 1, 1), date(2025, 12, 4), "20250101-20251204", id="different"),
        pytest.param(date(2025, 2, 2), date(2025, 2, 2), "20250202", id="same"),
    ],
)
def test_make_period(date1, date2, result):
    assert make_period(date1, date2) == [result]


def test_vpro_subpaths(tmp_path):
    dates = date_range(date(2025, 1, 1), date(2025, 1, 17))
    flist = []
    # create dummy files
    for d in dates:
        fpath1 = tmp_path / d.strftime("%Y/%m/%d/AP_TIC-%Y-%m-%d.nc")
        fpath2 = tmp_path / d.strftime("%Y/%m/%d/AP_TAC-%Y-%m-%d.nc")
        flist.append(fpath1)
        flist.append(fpath2)
        fpath1.mkdir(exist_ok=True, parents=True)
        fpath2.mkdir(exist_ok=True, parents=True)
    assert set(list(vpro_subpaths(*dates, root_path=tmp_path))) == set(flist)
