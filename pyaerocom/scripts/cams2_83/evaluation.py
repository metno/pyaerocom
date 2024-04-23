from __future__ import annotations

from datetime import date, timedelta
from enum import Enum


class EvalType(str, Enum):
    LONG = "long"
    SEASON = "season"
    WEEK = "week"
    DAY = "day"

    def __str__(self) -> str:
        return self.value

    def check_dates(self, start_date: date, end_date: date) -> None:
        if self == "day" and start_date != end_date:
            raise ValueError(f"For single day {start_date=} and {end_date=} should be the same")

        if self == "week" and (days := (end_date - start_date) // timedelta(days=1)) < 7:
            raise ValueError(f"For week needs {days=} >= 7")

    def freqs_config(self) -> dict:
        if self == "long":
            return dict(
                freqs=["daily", "monthly"],
                ts_type="hourly",
                main_freq="daily",
                forecast_evaluation=True,
            )

        if self == "season":
            return dict(
                freqs=["hourly", "daily"],
                ts_type="hourly",
                main_freq="hourly",
                forecast_evaluation=True,
            )

        if self == "week":
            return dict(
                freqs=["hourly", "daily"],
                ts_type="hourly",
                main_freq="hourly",
                forecast_evaluation=False,
            )
        if self == "day":
            return dict(
                freqs=["hourly"],
                ts_type="hourly",
                main_freq="hourly",
                forecast_evaluation=False,
            )

        raise NotImplementedError(f"Unsupported {self}")

    def periods(self, start_date: date, end_date: date) -> list[str]:
        if self == "long":
            return make_period_ys(start_date, end_date)
        return make_period(start_date, end_date)


def date_range(start_date: date, end_date: date) -> tuple[date, ...]:
    days = (end_date - start_date) // timedelta(days=1)
    assert days >= 0
    return tuple(start_date + timedelta(days=day) for day in range(days + 1))


def make_period(start_date: date, end_date: date) -> list[str]:
    if start_date == end_date:
        return [f"{start_date:%Y%m%d}"]
    periods = [f"{start_date:%Y%m%d}-{end_date:%Y%m%d}"]

    return periods


def make_period_ys(start_date: date, end_date: date) -> list[str]:
    periods = [f"{start_date.year}-{end_date.year}"]
    periods.extend(str(yr) for yr in range(start_date.year, end_date.year + 1))
    return periods
