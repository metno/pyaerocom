from __future__ import annotations

from datetime import datetime

import pytest

from pyaerocom.scripts.cams2_83.evaluation import EvalType, date_range


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
            "long",
            datetime(2024, 3, 1),
            datetime(2024, 8, 31),
            ["20240301-20240831"],
            id="long",
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
    assert eval.periods(start_date, end_date) == result


@pytest.mark.parametrize(
    "eval_type,start_date,end_date,error",
    [
        pytest.param(
            "season",
            datetime(2023, 12, 28),
            datetime(2023, 12, 12),
            "End date should be ⩾ start_date",
            id="invalid",
        ),
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
            datetime(2024, 2, 12),
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


@pytest.mark.parametrize(
    "start_date,end_date,result",
    [
        pytest.param(
            datetime(2023, 12, 28),
            datetime(2023, 12, 28),
            (datetime(2023, 12, 28, 0, 0),),
            id="1d",
        ),
        pytest.param(
            datetime(2023, 12, 28),
            datetime(2023, 12, 30),
            (
                datetime(2023, 12, 28, 0, 0),
                datetime(2023, 12, 29, 0, 0),
                datetime(2023, 12, 30, 0, 0),
            ),
            id="3d",
        ),
    ],
)
def test_date_range(start_date: datetime, end_date: datetime, result: tuple[datetime, ...]):
    assert date_range(start_date=start_date, end_date=end_date) == result
