from __future__ import annotations
import datetime
from typing import Any
from collections.abc import Iterable


import cf_units
import numpy as np


class PyaerocomUnit:
    """Pyaerocom specific encapsulation of cf_units.Unit that
    extends it with additional needed behaviour.
    """

    @property
    def category(self):
        return self._cfunit.category

    @property
    def ut_unit(self):
        return self._cfunit.ut_unit

    @property
    def calendar(self):
        return self._cfunit.calendar

    @property
    def origin(self):
        return self._cfunit.origin

    def __init__(self, unit: str, calendar: str | None = None) -> None:
        self._cfunit = cf_units.Unit(unit, calendar=calendar)

    def is_time(self) -> bool:
        return self._cfunit.is_time()

    def is_vertical(self) -> bool:
        return self._cfunit.is_time()

    def is_udunits(self) -> bool:
        return self._cfunit.is_udunits()

    def is_time_reference(self) -> bool:
        return self._cfunit.is_time_reference()

    def is_long_time_interval(self) -> bool:
        return self._cfunit.is_long_time_interval()

    def title(self, value: float) -> str:
        return self._cfunit.title(value)

    @property
    def modulus(self) -> float | None:
        return self._cfunit.modulus

    def is_convertible(self, other: str | PyaerocomUnit) -> bool:
        return self._cfunit.is_convertible(other)

    def is_dimensionless(self) -> bool:
        return self._cfunit.is_dimensionless()

    def is_unknown(self) -> bool:
        return self._cfunit.is_unknown()

    def is_no_unit(self) -> bool:
        return self._cfunit.is_no_unit()

    def format(self, option: int | list[int] | None = None) -> str:
        return self._cfunit.format(option)

    @property
    def name(self) -> str:
        return self._cfunit.name

    @property
    def symbol(self) -> str:
        return self._cfunit.symbol

    @property
    def definition(self) -> str:
        return self._cfunit.definition

    def offset_by_time(self, origin: float) -> PyaerocomUnit:
        return self._cfunit.offset_by_time(origin)

    def invert(self) -> PyaerocomUnit:
        return self._cfunit.invert()

    def root(self, root: int) -> PyaerocomUnit:
        return self._cfunit.root(root)

    def log(self, base: float) -> PyaerocomUnit:
        return self._cfunit.log(base)

    def __str__(self) -> str:
        return self._cfunit.__str__()

    def __repr__(self) -> str:
        return self._cfunit.__repr__()

    def __add__(self, other: float) -> PyaerocomUnit:
        return self._cfunit.__add__(other)

    def __sub__(self, other: float) -> PyaerocomUnit:
        return self._cfunit.__sub__(other)

    def __mul__(self, other: float | str | PyaerocomUnit) -> PyaerocomUnit:
        return self._cfunit.__mul__(other)

    def __div__(self, other: float | str | PyaerocomUnit) -> PyaerocomUnit:
        return self._cfunit.__div__(other)

    def __truediv__(self, other: float | str | PyaerocomUnit) -> PyaerocomUnit:
        return self._cfunit.__truediv__(other)

    def __pow__(self, power: float) -> PyaerocomUnit:
        return self._cfunit.__pow__(power)

    def __eq__(self, other: object) -> bool:
        return self._cfunit.__eq__(other)

    def __ne__(self, other: object) -> bool:
        return self._cfunit.__ne__(other)

    def change_calendar(self, calendar: str) -> PyaerocomUnit:
        return self._cfunit.change_calendar(calendar)

    def convert(
        self,
        value: float | np.ndarray,
        other: str | PyaerocomUnit,
        ctype: Any = np.float64,
        inplace: bool = False,
    ) -> float | np.ndarray:
        return self._cfunit.convert(value, other, ctype, inplace)

    @property
    def cftime_unit(self) -> str:
        return self._cfunit.cftime_unit

    def date2num(self, date: Any) -> float | np.ndarray:
        return self._cfunit.date2num(date)

    def num2date(
        self,
        time_value: float | np.ndarray,
        only_use_cftime_datetimes: bool = True,
        only_use_python_datetimes: bool = False,
    ) -> Any | np.ndarray:
        return self._cfunit.num2date(
            time_value, only_use_cftime_datetimes, only_use_python_datetimes
        )

    def num2pydate(
        self, time_value: float | Iterable[float]
    ) -> datetime.datetime | Iterable[datetime.datetime]:
        return self._cfunit.num2pydate(time_value)
