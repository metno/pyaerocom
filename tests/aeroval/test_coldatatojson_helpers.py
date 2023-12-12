from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from pytest import mark, param

from pyaerocom.aeroval.coldatatojson_helpers import (
    _add_heatmap_entry_json,
    _init_stats_dummy,
    _prepare_aerocom_regions_json,
    _prepare_country_regions,
    _prepare_default_regions_json,
    _prepare_htap_regions_json,
    _prepare_regions_json_helper,
    _write_diurnal_week_stationdata_json,
    _write_site_data,
    _write_stationdata_json,
    get_stationfile_name,
)
from pyaerocom.region import get_all_default_region_ids
from pyaerocom.region_defs import (
    HTAP_REGIONS,
    HTAP_REGIONS_DEFAULT,
    OLD_AEROCOM_REGIONS,
    OTHER_REGIONS,
)


def test__write_stationdata_json(tmp_path: Path):
    data = dict(station_name="stat1", obs_name="obs1", var_name_web="var1", vert_code="Column")
    path: Path = tmp_path / get_stationfile_name(**data)
    assert not path.exists()

    data["model_name"] = "model1"
    _write_stationdata_json(data, path.parent)
    assert path.exists()

    data["model_name"] = "model2"
    _write_stationdata_json(data, path.parent)
    assert path.exists()

    data = json.loads(path.read_text())
    assert data["model1"].pop("model_name") == "model1"
    assert data["model2"].pop("model_name") == "model2"
    assert data["model1"] == data["model2"]


def test__write_site_data(tmp_path: Path):
    data = [
        dict(
            model_name=f"model{n}",
            station_name=f"stat{n}",
            obs_name=f"obs{n}",
            var_name_web=f"var{n}",
            vert_code="Column",
        )
        for n in range(3)
    ]
    assert not list(tmp_path.glob("*.json"))
    _write_site_data(data, str(tmp_path))
    assert len(list(tmp_path.glob("*.json"))) == len(data)


def test__write_diurnal_week_stationdata_json(tmp_path: Path):
    data = dict(station_name="stat1", obs_name="obs1", var_name_web="var1", vert_code="Column")
    dirs = {"ts/diurnal": tmp_path}
    path: Path = tmp_path / get_stationfile_name(**data)
    assert not path.exists()

    data["model_name"] = "model1"
    _write_diurnal_week_stationdata_json(data, dirs)
    assert path.exists()

    data["model_name"] = "model2"
    _write_diurnal_week_stationdata_json(data, dirs)
    assert path.exists()

    data = json.loads(path.read_text())
    assert data["model1"].pop("model_name") == "model1"
    assert data["model2"].pop("model_name") == "model2"
    assert data["model1"] == data["model2"]


def test__add_heatmap_entry_json(tmp_path: Path):
    path = tmp_path / "add_entry.json"
    assert not path.exists()

    result = dict(value=None)
    obs, obs_var, vert, model, model_var = "obs", "obs_var", "Column", "model", "model_var"
    _add_heatmap_entry_json(path, result, obs, obs_var, vert, model, model_var)
    assert path.exists()

    data = json.loads(path.read_text())
    assert data[obs_var][obs][vert][model][model_var] == result

    result.update(value=42.0)
    _add_heatmap_entry_json(path, result, obs, obs_var, vert, model, model_var)

    data = json.loads(path.read_text())
    assert data[obs_var][obs][vert][model][model_var] == result


def test__init_stats_dummy():
    dummy = _init_stats_dummy()
    assert dummy
    assert all(np.isnan(value) for value in dummy.values())


@mark.parametrize(
    "region_ids",
    [
        param(OLD_AEROCOM_REGIONS, id="old AeroCom"),
        param(HTAP_REGIONS_DEFAULT, id="HTAP default"),
        param(HTAP_REGIONS, id="HTAP"),
        param(OTHER_REGIONS, id="other"),
    ],
)
def test__prepare_regions_json_helper(region_ids: list[str]):
    helper = _prepare_regions_json_helper(region_ids)
    assert len(helper) == 2
    assert len(helper[0]) == len(helper[1]) == len(region_ids)

    for region_name, borders in helper[0].items():
        assert region_name in helper[1]
        assert type(borders) == dict
        assert "minLat" in borders and -90 <= borders["minLat"] <= 90
        assert "maxLat" in borders and -90 <= borders["maxLat"] <= 90
        assert "minLon" in borders and -180 <= borders["minLon"] <= 180
        assert "maxLon" in borders and -180 <= borders["maxLon"] <= 180
        assert borders["minLat"] < borders["maxLat"]

    for region_name, region in helper[1].items():
        assert region_name in helper[0]
        assert region.region_id in region_ids
        assert region.name == region_name


def test__prepare_default_regions_json():
    borders, regions = _prepare_default_regions_json()
    region_ids = get_all_default_region_ids()
    assert bool(borders) and bool(regions) and bool(region_ids)
    assert list(borders) == list(regions)
    assert [reg.region_id for reg in regions.values()] == region_ids


def test__prepare_aerocom_regions_json():
    borders, regions = _prepare_aerocom_regions_json()
    region_ids = OLD_AEROCOM_REGIONS
    assert bool(borders) and bool(regions) and bool(region_ids)
    assert list(borders) == list(regions)
    assert [reg.region_id for reg in regions.values()] == region_ids


def test__prepare_htap_regions_json():
    borders, regions = _prepare_htap_regions_json()
    region_ids = HTAP_REGIONS_DEFAULT
    assert bool(borders) and bool(regions) and bool(region_ids)
    assert list(borders) == list(regions)
    assert [reg.region_id for reg in regions.values()] == region_ids


@mark.parametrize(
    "region_ids",
    [
        param(OLD_AEROCOM_REGIONS, id="old AeroCom"),
        param(HTAP_REGIONS_DEFAULT, id="HTAP default"),
        param(HTAP_REGIONS, id="HTAP"),
        param(OTHER_REGIONS, id="other"),
    ],
)
def test__prepare_country_regions(region_ids: list[str]):
    regions = _prepare_country_regions(region_ids)
    assert type(regions) is dict
    assert bool(regions)
    assert [reg.region_id for reg in regions.values()] == region_ids
