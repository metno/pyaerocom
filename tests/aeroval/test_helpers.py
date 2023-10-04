from __future__ import annotations

import pytest

from pyaerocom.aeroval.helpers import (
    _check_statistics_periods,
    _get_min_max_year_periods,
    _period_str_to_timeslice,
    check_var_ranges_avail,
    make_dummy_model,
)
from pyaerocom.aeroval.setupclasses import EvalSetup
from pyaerocom.exceptions import VariableDefinitionError
from pyaerocom.griddeddata import GriddedData


@pytest.mark.parametrize(
    "dvar,var",
    [
        ("od550aer", "od550aer"),
        ("od550aer", "od550gt1aer"),
        ("pr", "prmm"),
        ("prmm", "prmm"),
    ],
)
def test_check_var_ranges_avail(data_tm5: GriddedData, dvar: str, var: str):
    data = data_tm5.copy()
    data.var_name = dvar
    check_var_ranges_avail(data, var)


def test_check_var_ranges_avail_error(data_tm5: GriddedData):
    with pytest.raises(VariableDefinitionError) as e:
        check_var_ranges_avail(data_tm5, "bla")
    assert str(e.value) == "Error (VarCollection): input variable bla is not supported"


def test__check_statistics_periods():
    assert _check_statistics_periods(["2010-2010", "2005"]) == ["2010-2010", "2005"]


@pytest.mark.parametrize(
    "periods,error",
    [
        pytest.param(
            42,
            "statistics_periods needs to be a list",
            id="not list",
        ),
        pytest.param(
            [42],
            "All periods need to be strings",
            id="not list[str]",
        ),
        pytest.param(
            ["2010-2010-20"],
            "Invalid value for period (2010-2010-20), can be either single years or period of years (e.g. 2000-2010).",
            id="wrong period",
        ),
    ],
)
def test__check_statistics_periods_error(periods: list[str], error: str):
    with pytest.raises(ValueError) as e:
        _check_statistics_periods(periods)
    assert str(e.value) == error


@pytest.mark.parametrize(
    "period,result",
    [
        ("2005", slice("2005", "2005")),
        ("2005-2019", slice("2005", "2019")),
    ],
)
def test__period_str_to_timeslice(period: str, result: slice):
    assert _period_str_to_timeslice(period) == result


def test__period_str_to_timeslice_error():
    with pytest.raises(ValueError) as e:
        _period_str_to_timeslice("2005-2019-2000")
    assert str(e.value) == "2005-2019-2000"


@pytest.mark.parametrize(
    "periods,result",
    [
        (["2005", "2000"], (2000, 2005)),
        (["2005", "2000", "1999-2021"], (1999, 2021)),
    ],
)
def test__get_min_max_year_periods(periods: list[str], result: tuple[int, int]):
    assert _get_min_max_year_periods(periods) == result


def test__get_min_max_year_periods_error():
    with pytest.raises(ValueError) as e:
        _get_min_max_year_periods(["2005-2004-23", "2000", "1999-2021"])
    assert str(e.value) == "2005-2004-23"


@pytest.mark.parametrize("cfg", ["cfgexp1"])
def test_make_dummy_model(eval_config: dict):
    cfg = EvalSetup(**eval_config)
    assert cfg.obs_cfg["AERONET-Sun"]
    model_id = make_dummy_model(["AERONET-Sun"], cfg)
    assert model_id == "dummy_model"
