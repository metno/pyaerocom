from datetime import date

import pytest

from pyaerocom.scripts.cams2_82.cli import (
    date_range,
    make_config,
    make_period,
    vpro_subpaths,
)


@pytest.fixture
def dummy_vpro_files(tmp_path):
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
    return flist


@pytest.mark.parametrize(
    "date1,date2,result",
    [
        pytest.param(date(2025, 1, 1), date(2025, 12, 4), "20250101-20251204", id="different"),
        pytest.param(date(2025, 2, 2), date(2025, 2, 2), "20250202", id="same"),
    ],
)
def test_make_period(date1, date2, result):
    assert make_period(date1, date2) == [result]


def test_vpro_subpaths(dummy_vpro_files, tmp_path):
    dates = date_range(date(2025, 1, 1), date(2025, 1, 17))
    assert set(list(vpro_subpaths(*dates, root_path=tmp_path))) == set(dummy_vpro_files)


def test_make_config(dummy_vpro_files, tmp_path):
    start_date = date(2025, 1, 1)
    end_date = date(2025, 1, 17)
    id = "test"
    name = "test"
    description = "test"

    cfg = make_config(
        start_date=start_date,
        end_date=end_date,
        model_path=tmp_path,
        eea_path=tmp_path,
        icos_path=tmp_path,
        aeronet_path=tmp_path,
        openaq_path=tmp_path,
        vprofiles_path=tmp_path,
        data_path=tmp_path,
        coldata_path=tmp_path,
        id=id,
        name=name,
        description=description,
        add_map=True,
        only_map=True,
        add_seasons=True,
    )

    assert cfg["periods"] == ["20250101-20250117"]
    assert cfg["add_model_maps"]
    assert cfg["only_model_maps"]
    cfg["obs_cfg"]["EEA"]["pyaro_config"].filename_or_obj_or_url == tmp_path
    cfg["obs_cfg"]["EEA"]["pyaro_config"].filters["time_bounds"]["startend_include"][0][0] == cfg[
        "obs_cfg"
    ]["Aeronet"]["pyaro_config"].filters["time_bounds"]["startend_include"][0][
        0
    ] == start_date.strftime("%Y-%m-%d %M%H%S")
    cfg["obs_cfg"]["EEA"]["pyaro_config"].filters["time_bounds"]["startend_include"][0][1] == cfg[
        "obs_cfg"
    ]["Aeronet"]["pyaro_config"].filters["time_bounds"]["startend_include"][0][
        1
    ] == start_date.strftime("%Y-%m-%d %M%H%S")
    assert set(cfg["obs_cfg"]["EPROFILE"]["read_opts_ungridded"]["files"]) == set(
        [str(p) for p in dummy_vpro_files]
    )
    assert cfg["only_model_maps"]
    cfg["obs_cfg"]["EEA"]["pyaro_config"].filename_or_obj_or_url == tmp_path
    cfg["obs_cfg"]["EEA"]["pyaro_config"].filters["time_bounds"]["startend_include"][0][0] == cfg[
        "obs_cfg"
    ]["Aeronet"]["pyaro_config"].filters["time_bounds"]["startend_include"][0][
        0
    ] == start_date.strftime("%Y-%m-%d %M%H%S")
    cfg["obs_cfg"]["EEA"]["pyaro_config"].filters["time_bounds"]["startend_include"][0][1] == cfg[
        "obs_cfg"
    ]["Aeronet"]["pyaro_config"].filters["time_bounds"]["startend_include"][0][
        1
    ] == start_date.strftime("%Y-%m-%d %M%H%S")
    assert set(cfg["obs_cfg"]["EPROFILE"]["read_opts_ungridded"]["files"]) == set(
        [str(p) for p in dummy_vpro_files]
    )
