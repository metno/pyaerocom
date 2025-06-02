from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from pyaerocom._warnings import ignore_warnings
from pyaerocom.scripts.cams2_83.cli_mos import app

runner = CliRunner()


@pytest.fixture()
def fake_config(monkeypatch, patched_config_mos):
    def fake_make_config(*args, **kwargs):
        return patched_config_mos

    monkeypatch.setattr("pyaerocom.scripts.cams2_83.cli_mos.make_config_mos", fake_make_config)


def test_eval_mos_dummy(
    tmp_path: Path,
    caplog,
):
    options = f"season 2024-03-01 2024-05-12 --data-path {tmp_path} --coldata-path {tmp_path} --name 'Test' --addseasons"
    result = runner.invoke(app, options.split())
    assert result.exit_code == 0
    assert "'add_seasons': True," in caplog.text
    assert "'use_cams2_83_fairmode': True," in caplog.text
    assert "no output available" in caplog.text


@pytest.mark.usefixtures("fake_CAMS2_83_Processer", "reset_cachedir")
def test_eval_mos_standard(tmp_path: Path, coldata_mos: Path, caplog):
    options = f"day 2024-03-01 2024-03-01 --data-path {tmp_path} --coldata-path {coldata_mos} --cache {tmp_path} --id mos-colocated-data --name 'Test'"
    result = runner.invoke(app, options.split())
    assert result.exit_code == 0

    map_dir = tmp_path / "cams2-83/mos-colocated-data/map"
    assert map_dir.is_dir()

    ts_st1 = tmp_path / "cams2-83/mos-colocated-data/ts/AT0ENK1_EEA-UTD_concno2_Surface.json"
    assert ts_st1.is_file()

    ts_st2 = tmp_path / "cams2-83/mos-colocated-data/ts/AT0ILL1_EEA-UTD_concno2_Surface.json"
    assert ts_st2.is_file()

    ts_st3 = tmp_path / "cams2-83/mos-colocated-data/ts/XK0012A_EEA-UTD_concno2_Surface.json"
    assert ts_st3.is_file()

    hm_dir = tmp_path / "cams2-83/mos-colocated-data/hm"
    assert hm_dir.is_dir()

    scat_dir = tmp_path / "cams2-83/mos-colocated-data/scat"
    assert scat_dir.is_dir()

    cfg_out = tmp_path / "cams2-83/mos-colocated-data/cfg_cams2-83_mos-colocated-data.json"
    assert cfg_out.is_file()

    colfileE = f"{coldata_mos}/cams2-83/mos-colocated-data/ENS/concno2_concno2_MOD-ENS_REF-EEA-UTD_20240301_20240301_hourly_ALL-wMOUNTAINS.nc"
    colfileM = f"{coldata_mos}/cams2-83/mos-colocated-data/MOS/concno2_concno2_MOD-MOS_REF-EEA-UTD_20240301_20240301_hourly_ALL-wMOUNTAINS.nc"

    assert "Running Statistics (MOS)" in caplog.text
    assert f"Processing: {colfileE}" in caplog.text
    assert f"Processing: {colfileM}" in caplog.text
    assert "Finished processing" in caplog.text
    assert "Done Running Statistics (MOS)" in caplog.text


@ignore_warnings(RuntimeWarning, "invalid value encountered in divide")
@ignore_warnings(RuntimeWarning, "Mean of empty slice")
@ignore_warnings(RuntimeWarning, "All-NaN slice encountered")
@pytest.mark.usefixtures("fake_ExperimentProcessor", "reset_cachedir")
def test_eval_mos_medianscores(tmp_path: Path, coldata_mos: Path, caplog):
    options = f"season 2024-03-01 2024-03-05 --data-path {tmp_path} --coldata-path {coldata_mos} --cache {tmp_path} --id mos-colocated-data --name 'Test'"
    result = runner.invoke(app, options.split())
    assert result.exit_code == 0
    fc_out = tmp_path / "cams2-83/mos-colocated-data/forecast/ALL_EEA-UTD_concno2_Surface.json"
    assert fc_out.is_file()
    assert "Running CAMS2_83 Specific Statistics" in caplog.text
    assert "Processing Component: concno2"
    assert "Making subset for ALL, 2024/03/01-2024/03/05 and all" in caplog.text
    assert "Finished processing" in caplog.text
    assert "Median scores run finished" in caplog.text
