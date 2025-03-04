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
            [
                "20211201-20220228",
                "20220301-20220531",
                "20220601-20220831",
                "20220901-20221130",
                "20221201-20230228",
                "20230301-20230531",
                "20230601-20230831",
                "20230901-20231130",
                "20231201-20240229",
                "20240301-20240531",
                "20211201-20240531",
            ],
            id="long",
        ),
        pytest.param(
            "long",
            datetime(2024, 6, 1),
            datetime(2024, 8, 15),
            ["20240601-20240815"],
            id="long2",
        ),
        pytest.param(
            "week",
            datetime(2023, 12, 28),
            datetime(2024, 1, 12),
            ["20231228-20240112"],
            id="week",
        ),
        pytest.param("day", datetime(2024, 1, 12), datetime(2024, 1, 12), ["20240112"], id="day"),
    ],
)
def test_periods(eval_type: str, start_date: datetime, end_date: datetime, result: tuple):
    eval = EvalType(eval_type)
    print(eval.periods(start_date, end_date))
    assert eval.periods(start_date, end_date) == result


@pytest.mark.parametrize(
    "eval_type,start_date,end_date,error",
    [
        pytest.param(
            "week",
            datetime(2023, 12, 28),
            datetime(2024, 1, 1),
            "Evaluation type 'week' should have",
            id="week",
        ),
        pytest.param(
            "day",
            datetime(2024, 1, 12),
            datetime(2022, 1, 12),
            "Evaluation type 'day' should have the same",
            id="day",
        ),
    ],
)
def test_check_dates(eval_type: str, start_date: datetime, end_date: datetime, error: str):
    eval = EvalType(eval_type)
    with pytest.raises(ValueError) as excinfo:
        eval.check_dates(start_date, end_date)
    assert error in str(excinfo.value)
