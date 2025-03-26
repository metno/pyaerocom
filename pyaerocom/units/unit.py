from __future__ import annotations
import datetime
from typing import Any
from collections.abc import Iterable


import cf_units
import numpy as np
import pandas as pd

from .exceptions import UnitConversionError
from .datetime import TsType
from .datetime.time_config import SI_TO_TS_TYPE
from .typing import UnitLike
from pyaerocom.variable_helpers import get_variable

from .constants import HA_TO_SQM, M_SO2, M_S, M_NO2, M_N, M_NH3, M_SO4

from typing import TypeVar

T = TypeVar("T")


class PyaerocomUnit:
    """Pyaerocom specific encapsulation of cf_units.Unit that extends it
    with additional needed behaviour.

    The first additional behaviour is to handle variables that measure only
    a portion of the real mass. Eg. if concso4 is provided as "ug S/m3", we
    want the mass in terms of SO2, so the values must be scaled up by a
    constant factor MolecularMass("SO2")/MolecularMass("S"). This is
    currently enabled using the lookup tables UCONV_MUL_FACS and UALIASES.

    The second behaviour is adding implicit frequency for rate variables
    and a ts_type. If tstype and aerocom_var are provided in __init__, units
    of the form "mg m-2" will automatically have the temporal frequency
    appended. For instance, assuming tstype='daily', it becomes "mg m-2 d-1"

    Third, cf_units.Unit does not natively support conversion of eg. pd.Series.
    This wrapper allows conversion of any data structure that supports __mul__.
    """

    #: Custom unit conversion factors for certain variables
    #: columns: variable -> from unit -> to_unit -> conversion
    #: factor
    UCONV_MUL_FACS = pd.DataFrame(
        [
            # ["dryso4", "mg/m2/d", "mgS m-2 d-1", M_S / M_SO4],
            # ["drynh4", "mg/m2/d", "mgN m-2 d-1", M_N/ M_NH4],
            # ["concso4", "ug S/m3", "ug m-3", M_SO4 / M_S],
            # ["SO4ugSm3", "ug/m3", "ug S m-3", M_S / M_SO4],
            # ["concso4pm25", "ug S/m3", "ug m-3", M_SO4 / M_S],
            # ["concso4pm10", "ug S/m3", "ug m-3", M_SO4 / M_S],
            ["concso2", "ug S/m3", "ug m-3", M_SO2 / M_S],
            ["concbc", "ug C/m3", "ug m-3", 1.0],
            ["concoa", "ug C/m3", "ug m-3", 1.0],
            ["concoc", "ug C/m3", "ug m-3", 1.0],
            ["conctc", "ug C/m3", "ug m-3", 1.0],
            # a little hacky for ratpm10pm25...
            # ["ratpm10pm25", "ug m-3", "1", 1.0],
            ["concpm25", "ug m-3", "ug m-3", 1.0],
            ["concpm10", "ug m-3", "ug m-3", 1.0],
            ["concno2", "ug N/m3", "ug m-3", M_NO2 / M_N],
            # ["concno3", "ug N/m3", "ug m-3", M_NO3 / M_N],
            ["concnh3", "ug N/m3", "ug m-3", M_NH3 / M_N],
            # ["concnh4", "ug N/m3", "ug m-3", M_NH4 / M_N],
            ["wetso4", "kg S/ha", "kg m-2", M_SO4 / M_S / HA_TO_SQM],
            ["concso4pr", "mg S/L", "g m-3", M_SO4 / M_S],
        ],
        columns=["var_name", "from", "to", "fac"],
    ).set_index(["var_name", "from"])

    UALIASES = {
        # mass concentrations
        "ug S m-3": "ug S/m3",
        "ug C m-3": "ug C/m3",
        "ug N m-3": "ug N/m3",
        "ugC/m3": "ug C m-3",
        # deposition rates (implicit)
        ## sulphur species
        "mgS/m2": "mg S m-2",
        "mgSm-2": "mg S m-2",
        ## nitrogen species
        "mgN/m2": "mg N m-2",
        "mgNm-2": "mg N m-2",
        # deposition rates (explicit)
        ## sulphur species
        "mgS/m2/h": "mg S m-2 h-1",
        "mg/m2/h": "mg m-2 h-1",
        "mgS/m**2/h": "mg S m-2 h-1",
        "mgSm-2h-1": "mg S m-2 h-1",
        "mgSm**-2h-1": "mg S m-2 h-1",
        "mgS/m2/d": "mg S m-2 d-1",
        ## nitrogen species
        "mgN/m2/h": "mg N m-2 h-1",
        "mgN/m**2/h": "mg N m-2 h-1",
        "mgNm-2h-1": "mg N m-2 h-1",
        "mgNm**-2h-1": "mg N m-2 h-1",
        "mgN/m2/d": "mg N m-2 d-1",
        ## others
        "MM/H": "mm h-1",
        # others
        "/m": "m-1",
    }

    def __init__(
        self,
        unit: str | UnitLike,
        calendar: str | None = None,
        *,
        aerocom_var: str | None = None,
        ts_type: str | TsType | None = None,
    ) -> None:
        unit = PyaerocomUnit.UALIASES.get(str(unit), str(unit))

        try:
            info = PyaerocomUnit.UCONV_MUL_FACS.loc[(aerocom_var, str(unit)), :]
            if not isinstance(info, pd.Series):
                raise UnitConversionError(
                    "FATAL: Could not find unique conversion factor in table  "
                    "UCONV_MUL_FACS in units_helpers.py. Please check for "
                    "dulplicate entries"
                )
            new_unit, factor = (info.to, info.fac)
        except KeyError:
            new_unit, factor = unit, 1

        if factor != 1:
            new_unit = f"{factor} {new_unit}"

        if ts_type is not None and aerocom_var is not None and get_variable(aerocom_var).is_rate:
            ends_with_freq = False
            for si_unit in SI_TO_TS_TYPE:
                if unit.endswith(f"/{si_unit}") or unit.endswith(f"{si_unit}-1"):
                    ends_with_freq = True
                    break

            if not ends_with_freq:
                new_unit = f"{new_unit} {TsType(ts_type).to_si()}-1"

        self._aerocom_var = aerocom_var
        self._ts_type = ts_type
        self._cfunit = cf_units.Unit(new_unit, calendar=calendar)

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
        return PyaerocomUnit(
            self._cfunit.offset_by_time(origin),
            calendar=self._cfunit.calendar,
            aerocom_var=self._aerocom_var,
        )

    def invert(self) -> PyaerocomUnit:
        return self._cfunit.invert()  # ?

    def root(self, root: int) -> PyaerocomUnit:
        return self._cfunit.root(root)  # ?

    def log(self, base: float) -> PyaerocomUnit:
        return self._cfunit.log(base)  # ?

    def __str__(self) -> str:
        return self._cfunit.__str__()

    def __repr__(self) -> str:
        return self._cfunit.__repr__()

    def __add__(self, other: float) -> PyaerocomUnit:
        return self._cfunit.__add__(other)  # ?

    def __sub__(self, other: float) -> PyaerocomUnit:
        return self._cfunit.__sub__(other)  # ?

    def __mul__(self, other: float | str | PyaerocomUnit) -> PyaerocomUnit:
        return self._cfunit.__mul__(other)  # ?

    def __div__(self, other: float | str | PyaerocomUnit) -> PyaerocomUnit:
        return self._cfunit.__div__(other)  # ?

    def __truediv__(self, other: float | str | PyaerocomUnit) -> PyaerocomUnit:
        return self._cfunit.__truediv__(other)  # ?

    def __pow__(self, power: float) -> PyaerocomUnit:
        return self._cfunit.__pow__(power)  # ?

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PyaerocomUnit):
            return self._cfunit.__eq__(other)

        other = cf_units.Unit(other)
        return self._cfunit.__eq__(other)

    def __ne__(self, other: object) -> bool:
        return self._cfunit.__ne__(other)

    def change_calendar(self, calendar: str) -> PyaerocomUnit:
        return self._cfunit.change_calendar(calendar)  # ?

    def convert(
        self,
        value: T,
        other: str | PyaerocomUnit,
        ctype: Any = np.float64,
        inplace: bool = False,
    ) -> T:
        if isinstance(value, int):
            value = float(value)

        factor = self._cfunit.convert(1, other, ctype, inplace)
        if factor == 1:
            return value

        result = factor * value
        assert type(value) is type(result)
        return result

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

    # def __repr__(self) -> str:
    #    return f"PyaerocomUnit('{self._cfunit.name}')"
