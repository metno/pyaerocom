from __future__ import annotations

from datetime import date, timedelta
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import xarray as xr

from pyaerocom import const

from . import cfg_test, cfg_test_mos


@pytest.fixture()
def fake_cache_path(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(
        "pyaerocom.io.cachehandler_ungridded.CacheHandlerUngridded.cache_dir", tmp_path
    )
    cache_file = tmp_path / "tmp.pkl"
    cache_file.write_bytes(b"")
    assert cache_file.exists()
    return tmp_path


@pytest.fixture
def reset_cachedir():
    cache = const.CACHEDIR
    yield
    const.CACHEDIR = cache


@pytest.fixture
def patched_config(tmp_path):
    cfg = cfg_test.CFG
    assert cfg["proj_id"] == "cams2-83"
    cfg.update({"json_basedir": tmp_path, "coldata_basedir": tmp_path})
    return cfg


@pytest.fixture
def patched_config_mos():
    cfg = cfg_test_mos.CFG
    assert cfg["exp_id"] == "mos-colocated-data"
    return cfg


@pytest.fixture
def fake_CAMS2_83_Processer(monkeypatch):
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


@pytest.fixture
def fake_ExperimentProcessor(monkeypatch):
    def do_not_run(self, model_name=None, obs_name=None, var_list=None, update_interface=True):
        assert model_name is None
        assert obs_name is None
        assert var_list is None
        assert update_interface is True

    monkeypatch.setattr(
        "pyaerocom.scripts.cams2_83.evaluation.ExperimentProcessor.run", do_not_run
    )


@pytest.fixture(scope="module")
def coldata_mos(tmp_path_factory) -> Path:
    root: Path = tmp_path_factory.mktemp("data")

    def dataset(model: str, day: int, start: date, end: date, persistence: bool) -> xr.Dataset:
        if persistence:
            start = start - timedelta(days=1)
        else:
            start = start + timedelta(days=day)

        hours = (end - start) // timedelta(hours=1) + 1

        ds = xr.Dataset(
            data_vars=dict(
                concno2=xr.Variable(
                    ("data_source", "time", "station_name"),
                    np.zeros((2, hours, 3)),
                    {
                        "ts_type": "hourly",
                        "filter_name": "ALL-wMOUNTAINS",
                        "ts_type_src": ["hourly", "hourly"],
                        "var_units": ["ug m-3", "ug m-3"],
                        "data_level": 3,
                        "revision_ref": "n/a",
                        "from_files": "",
                        "from_files_ref": "None",
                        "colocate_time": 0,
                        "obs_is_clim": 0,
                        "pyaerocom": "0.18.dev0",
                        "CONV!min_num_obs": str(dict(daily=dict(hourly=18))),
                        "resample_how": "None",
                        "obs_name": "EEA-UTD",
                        "vert_code": "Surface",
                        "diurnal_only": 0,
                        "zeros_to_nan": 1,
                    },
                )
            ),
            coords=dict(
                data_source=xr.Variable(
                    "data_source", ["CAMS2_83.NRT", f"CAMS2-83.{model}.day{day}.FC"]
                ),
                station_name=xr.Variable("station_name", ["AT0ENK1", "AT0ILL1", "XK0012A"]),
                station_type=xr.Variable("station_name", ["bla", "bla", "bla"]),
                latitude=xr.Variable("station_name", [48.39, 47.77, 42.66]),
                longitude=xr.Variable("station_name", [13.67, 16.77, 21.08]),
                altitude=xr.Variable("station_name", [525, 117, 529]),
                time=xr.Variable("time", pd.date_range(start, end, freq="1h")),
            ),
        )

        ds["concno2"].attrs.update(
            data_source=ds["data_source"].values.tolist(),
            var_name=["concno2", "concno2"],
            var_name_input=["concno2", "concno2"],
            model_name=f"CAMS2-83-{model}-day{day}-FC",
        )

        return ds

    start, end = date(2024, 3, 1), date(2024, 3, 5)
    for model, day in product(("ENS", "MOS"), range(4)):
        path = (
            root
            / f"cams2-83/mos-colocated-data/CAMS2-83-{model}-day{day}-FC/concno2_concno2_MOD-CAMS2-83-{model}-day{day}-FC_REF-EEA-UTD_{start:%Y%m%d}_{end:%Y%m%d}_hourly_ALL-wMOUNTAINS.nc"
        )
        path.parent.mkdir(exist_ok=True, parents=True)
        dataset(model, day, start, end, False).to_netcdf(path)

    for model in ("ENS", "MOS"):
        path = (
            root
            / f"cams2-83/mos-colocated-data/CAMS2-83-{model}-persistence-FC/concno2_concno2_MOD-CAMS2-83-{model}-persistence-FC_REF-EEA-UTD_{start:%Y%m%d}_{end:%Y%m%d}_hourly_ALL-wMOUNTAINS.nc"
        )
        path.parent.mkdir(exist_ok=True, parents=True)
        ds = dataset(model, 0, start, end, True)
        ds["concno2"].attrs.update(model_name=f"CAMS2-83-{model}-persistence-FC")
        ds.to_netcdf(path)

    start, end = date(2024, 3, 1), date(2024, 3, 2)
    for model in ("ENS", "MOS"):
        path = (
            root
            / f"cams2-83/mos-colocated-data/{model}/concno2_concno2_MOD-{model}_REF-EEA-UTD_{start:%Y%m%d}_{start:%Y%m%d}_hourly_ALL-wMOUNTAINS.nc"
        )
        path.parent.mkdir(exist_ok=True, parents=True)
        ds = dataset(model, 0, start, end, False)
        ds["concno2"].attrs.update(model_name=model)
        ds.to_netcdf(path)

    return root
