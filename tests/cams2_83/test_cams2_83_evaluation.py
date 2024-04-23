from __future__ import annotations

from datetime import datetime

import pytest

from pyaerocom.scripts.cams2_83.evaluation import EvalType


@pytest.mark.parametrize(
    "eval_type,start_date,end_date,result",
    [
        pytest.param(
            "long",
            datetime(2021, 12, 1),
            datetime(2024, 5, 31),
            ["2021-2024", "2021", "2022", "2023", "2024"],
            id="long",
        ),
        pytest.param(
            "week", datetime(2023, 12, 28), datetime(2024, 1, 12), ["20231228-20240112"], id="week"
        ),
        pytest.param("week", datetime(2024, 1, 12), datetime(2024, 1, 12), ["20240112"], id="day"),
    ],
)
def test_periods(eval_type: str, start_date: datetime, end_date: datetime, result: tuple):
    eval = EvalType(eval_type)
    assert eval.periods(start_date, end_date) == result
