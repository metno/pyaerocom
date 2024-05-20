from __future__ import annotations

import os
from pathlib import Path

import pytest
from typer.testing import CliRunner

from pyaerocom.scripts.cams2_83.cli_mos import app

runner = CliRunner()


@pytest.fixture()
def fake_config(monkeypatch, patched_config_mos):
    def fake_make_config(*args, **kwargs):
        return patched_config_mos

    monkeypatch.setattr("pyaerocom.scripts.cams2_83.cli_mos.make_config_mos", fake_make_config)


def test_eval_mos_dummy(
    fake_cache_path: Path,
    tmp_path: Path,
    caplog,
):
    assert list(fake_cache_path.glob("*.pkl"))

    options = f"season 2024-03-01 2024-05-12 --data-path {tmp_path} --coldata-path {tmp_path} --cache {fake_cache_path} --name 'Test'"
    result = runner.invoke(app, options.split())
    assert result.exit_code == 0
    assert "no output available" in caplog.text


def test_eval_mos_standard(
    fake_cache_path: Path,
    tmp_path,
    dataDir,
    caplog,
    monkeypatch,
):
    def do_not_run(
        self,
        model_name=None,
        obs_name=None,
        var_list=None,
        update_interface=True,
        analysis=False,
    ):
        assert model_name is None
        assert obs_name is None
        assert var_list is None
        assert analysis is False
        assert update_interface is True

    monkeypatch.setattr("pyaerocom.scripts.cams2_83.evaluation.CAMS2_83_Processer.run", do_not_run)
    options = f"day 2024-03-01 2024-03-01 --data-path {tmp_path} --coldata-path {dataDir} --cache {fake_cache_path} --id mos-colocated-data --name 'Test'"
    result = runner.invoke(app, options.split())
    assert result.exit_code == 0
    map_dir = os.path.join(tmp_path, "cams2-83/mos-colocated-data/map")
    ts_st1 = os.path.join(
        tmp_path, "cams2-83/mos-colocated-data/ts/AT0ENK1_EEA-NRT-concno2_Surface.json"
    )
    ts_st2 = os.path.join(
        tmp_path, "cams2-83/mos-colocated-data/ts/AT0ILL1_EEA-NRT-concno2_Surface.json"
    )
    ts_st3 = os.path.join(
        tmp_path, "cams2-83/mos-colocated-data/ts/XK0012A_EEA-NRT-concno2_Surface.json"
    )
    hm_dir = os.path.join(tmp_path, "cams2-83/mos-colocated-data/hm")
    scat_dir = os.path.join(tmp_path, "cams2-83/mos-colocated-data/scat")
    contour_dir = os.path.join(tmp_path, "cams2-83/mos-colocated-data/contour")
    fc_dir = os.path.join(tmp_path, "cams2-83/mos-colocated-data/forecast")
    cfg_out = os.path.join(
        tmp_path, "cams2-83/mos-colocated-data/cfg_cams2-83_mos-colocated-data.json"
    )
    assert Path(map_dir).is_dir()
    assert Path(ts_st1).is_file()
    assert Path(ts_st2).is_file()
    assert Path(ts_st3).is_file()
    assert Path(hm_dir).is_dir()
    assert Path(scat_dir).is_dir()
    assert Path(contour_dir).is_dir()
    assert Path(fc_dir).is_dir()
    assert Path(cfg_out).is_file()
    colfileE = os.path.join(
        dataDir,
        "cams2-83/mos-colocated-data/ENS/concno2_concno2_MOD-ENS_REF-EEA-NRT_20240301_20240301_hourly_ALL-wMOUNTAINS.nc",
    )
    colfileM = os.path.join(
        dataDir,
        "cams2-83/mos-colocated-data/MOS/concno2_concno2_MOD-MOS_REF-EEA-NRT_20240301_20240301_hourly_ALL-wMOUNTAINS.nc",
    )
    assert "Running Statistics (MOS)" in caplog.text
    assert f"Processing: {colfileE}" in caplog.text
    assert f"Processing: {colfileM}" in caplog.text
    assert "Finished processing" in caplog.text


def test_eval_mos_medianscores(
    fake_cache_path: Path,
    tmp_path,
    dataDir,
    caplog,
    monkeypatch,
):
    def do_not_run(self, model_name=None, obs_name=None, var_list=None, update_interface=True):
        assert model_name is None
        assert obs_name is None
        assert var_list is None
        assert update_interface is True

    monkeypatch.setattr(
        "pyaerocom.scripts.cams2_83.evaluation.ExperimentProcessor.run", do_not_run
    )
    options = f"season 2024-03-01 2024-03-05 --data-path {tmp_path} --coldata-path {dataDir} --cache {fake_cache_path} --id mos-colocated-data --name 'Test'"
    result = runner.invoke(app, options.split())
    assert result.exit_code == 0
    fc_out = os.path.join(
        tmp_path, "cams2-83/mos-colocated-data/forecast/ALL_EEA-NRT-concno2_Surface.json"
    )
    assert Path(fc_out).is_file()
    assert "Running CAMS2_83 Specific Statistics" in caplog.text
    assert "Processing Component: concno2"
    assert "Making subset for ALL, 2024/03/01-2024/03/05 and all" in caplog.text
    assert "Finished processing" in caplog.text
