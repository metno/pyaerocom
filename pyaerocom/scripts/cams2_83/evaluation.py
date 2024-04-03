from __future__ import annotations

from datetime import date, datetime, timedelta
from enum import Enum
from typing import Literal

from dateutil.relativedelta import relativedelta


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
                freqs=["hourly", "daily", "monthly"],
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


def season(date: date) -> Literal["DJF", "MAM", "JJA", "SON"]:
    return ("DJF", "MAM", "JJA", "SON")[date.month % 12 // 3]


def seasons_in_period(start_date: date, end_date: date) -> list[str]:
    dates = date_range(start_date, end_date)
    periods = []
    prev_date = start_period = dates[0]
    prev_season = season(prev_date)
    for current_date in dates[1:]:
        if season(current_date) == prev_season:
            prev_date = current_date
        else:
            periods.append(f"{start_period:%Y%m%d}-{prev_date:%Y%m%d}")
            prev_date = current_date
            prev_season = season(current_date)
            start_period = current_date

    else:
        if start_period == dates[-1]:
            periods.append(f"{start_period:%Y%m%d}")
        else:
            periods.append(f"{start_period:%Y%m%d}-{dates[-1]:%Y%m%d}")

    return periods


def years_starting_in_november(start_date: date, end_date: date) -> list[str]:
    periods = []
    prev_date = start_date
    new_yr = datetime(start_date.year, 12, 1, 00, 00, 00)

    if new_yr > start_date:
        periods.append(f"{start_date:%Y%m%d}-{new_yr-timedelta(days=1):%Y%m%d}")
        prev_date = new_yr
        new_yr += relativedelta(years=1)
    else:
        if end_date < new_yr + relativedelta(years=1):
            return []
        periods.append(
            f"{start_date:%Y%m%d}-{new_yr+relativedelta(years=1)-timedelta(days=1):%Y%m%d}"
        )

        prev_date = new_yr + relativedelta(years=1)
        new_yr += relativedelta(years=2)

    for _ in range(end_date.year - start_date.year):
        if new_yr < end_date:
            periods.append(f"{prev_date:%Y%m%d}-{new_yr-timedelta(days=1):%Y%m%d}")
            prev_date = new_yr
            new_yr += relativedelta(years=1)
        else:
            periods.append(f"{prev_date:%Y%m%d}-{end_date:%Y%m%d}")
            break

    return periods


def make_period(start_date: date, end_date: date) -> list[str]:
    season_periods = seasons_in_period(start_date, end_date)
    nov_periods = years_starting_in_november(start_date, end_date)

    if start_date == end_date:
        return [f"{start_date:%Y%m%d}"]

    periods = [f"{start_date:%Y%m%d}-{end_date:%Y%m%d}"]
    if periods != season_periods:
        periods += nov_periods  # season_periods

    return periods


def make_period_ys(start_date: date, end_date: date) -> list[str]:
    periods = [f"{start_date.year}-{end_date.year}"]
    periods.extend(str(yr) for yr in range(start_date.year, end_date.year + 1))
    return periods
