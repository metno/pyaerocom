from __future__ import annotations
import datetime
import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from collections.abc import Iterable


import cf_units
import numpy as np
import pandas as pd

from .exceptions import UnitConversionError
from .datetime import TsType
from .datetime.time_config import SI_TO_TS_TYPE
from pyaerocom.variable_helpers import get_variable

from .constants import HA_TO_SQM, M_SO2, M_S, M_NO2, M_N, M_NH3, M_SO4

from typing import TypeVar, overload, NamedTuple
from collections.abc import Callable
from .typing import SupportsMul

__all__ = ["Unit"]

T = TypeVar("T", bound=SupportsMul)


class UnitConversionCallbackInfo(NamedTuple):
    factor: float
    from_aerocom_var: str | None
    from_ts_type: TsType | None
    from_cf_unit: cf_units.Unit
    to_cf_unit: cf_units.Unit


UnitConversionCallbackHandler = Callable[[UnitConversionCallbackInfo], None]


class Unit:
    """Pyaerocom specific encapsulation of cf_units.Unit that extends it
    with additional needed behaviour.

    The first additional behaviour is to handle variables that measure only
    a portion of the real mass. Eg. if concso4 is provided as "ug S/m3", we
    want the mass in terms of SO4, so the values must be scaled up by a
    constant factor MolecularMass("SO4")/MolecularMass("S"). This is
    currently enabled using the lookup tables UCONV_MUL_FACS and UALIASES,
    combined with a scalar factor in the unit.

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
    _UCONV_MUL_FACS = pd.DataFrame(
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
            ["drynh3", "kg ha-1 yr-1", "kg m-2 s-2", 1 / (HA_TO_SQM * (365 * 24 * 60 * 60))],
            [
                "drynh3",
                "kg N ha-1 yr-1",
                "kg m-2 s-1",
                (M_NH3 / M_N) / (1 / (HA_TO_SQM * (365 * 24 * 60 * 60))),
            ],
        ],
        columns=["var_name", "from", "to", "fac"],
    ).set_index(["var_name", "from"])

    _UALIASES = {
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
        # attenuated backscatter
        "Mm-1.sr-1": "Mm-1 sr-1",
    }

    def __init__(
        self,
        unit: str,
        calendar: str | None = None,
        *,
        aerocom_var: str | None = None,
        ts_type: str | TsType | None = None,
    ) -> None:
        self._origin = str(unit)
        unit = Unit._UALIASES.get(str(unit), str(unit))

        try:
            info = Unit._UCONV_MUL_FACS.loc[(aerocom_var, str(unit)), :]
            if not isinstance(info, pd.Series):
                raise UnitConversionError(
                    "FATAL: Could not find unique conversion factor in table PyaerocomUnit._UCONV_MUL_FACS."
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
        self._ts_type = None
        if ts_type is not None:
            self._ts_type = TsType(ts_type)
        self._cfunit = cf_units.Unit(new_unit, calendar=calendar)

    @property
    def origin(self) -> str:
        """
        The original string used to create this Unit.
        """
        return self._origin

    def is_convertible(self, other: str | Unit) -> bool:
        """
        Return whether this unit is convertible to other.

        :param other: Other Unit.
        """
        return self._cfunit.is_convertible(other)

    def is_dimensionless(self) -> bool:
        """
        Return whether the unit is dimensionless.
        """
        return self._cfunit.is_dimensionless()

    def is_unknown(self) -> bool:
        """
        Return whether the unit is defined to be an unknown unit.
        """
        return self._cfunit.is_unknown()

    def __str__(self) -> str:
        return self._cfunit.__str__()

    def __repr__(self) -> str:
        return self._cfunit.__repr__()

    def __add__(self, other: float) -> Unit:
        return Unit.from_cf_units(self._cfunit.__add__(other))

    def __sub__(self, other: float) -> Unit:
        return Unit.from_cf_units(self._cfunit.__sub__(other))

    def __mul__(self, other: float | str | Unit) -> Unit:
        return Unit.from_cf_units(self._cfunit.__mul__(other))

    def __truediv__(self, other: float | str | Unit) -> Unit:
        return Unit.from_cf_units(self._cfunit.__truediv__(other))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Unit):
            try:
                other = Unit(str(other))
            except ValueError:
                return False

        return self._cfunit.__eq__(other._cfunit)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    @overload
    def convert(
        self,
        value: int,
        other: str | Self,
        inplace: bool = False,
        *,
        callback: None | UnitConversionCallbackHandler = None,
        **kwargs,
    ) -> float: ...

    @overload
    def convert(
        self,
        value: T,
        other: str | Self,
        inplace: bool = False,
        *,
        callback: None | UnitConversionCallbackHandler = None,
        **kwargs,
    ) -> T: ...

    def convert(
        self,
        value: T,
        other: str | Self,
        inplace: bool = False,
        *,
        callback: None | UnitConversionCallbackHandler = None,
        **kwargs,
    ) -> T:
        """Implements unit conversion to a different unit that should work
        with any data structure that supports __mul__ and / or __imul__.

        :param value: The value to be converted.
        :param other: The unit to which to convert (will be passed to PyaerocomUnit.__init__())
        :param callback: Callback function for eg. logging, defaults to None
            The callback function will receive a NamedTuple with the following keys:
                "factor" - float: The numerical conversion factor used.
                "from_aerocom_var" - str: The aerocom var name.
                "from_ts_type" - str: The ts_type of the from units.
                "from_cf_unit" - str: The base cf_unit converted from.
                "to_cf_unit" - str: The base cf_unit converted to.
        :param kwargs: Will be passed as additional keyword args to PyaerocomUnit.__init__() for 'other'.
        :return: Unit converted data.
        """
        to_unit = Unit(str(other), **kwargs)._cfunit
        factor = float(self._cfunit.convert(1, to_unit, inplace=False))

        if inplace:
            value *= factor
            result = value
        else:
            result = factor * value

        if isinstance(value, int):
            assert isinstance(result, float)
        else:
            assert type(result) is type(value)

        assert (result is value) == inplace

        if callback is not None:
            info = UnitConversionCallbackInfo(
                factor=factor,
                from_aerocom_var=self._aerocom_var,
                from_ts_type=self._ts_type,
                from_cf_unit=str(self._cfunit),
                to_cf_unit=str(to_unit),
            )
            callback(info)

        return result

    def date2num(
        self, date: datetime.datetime | Iterable[datetime.datetime]
    ) -> float | np.ndarray:
        """Returns the numeric time value calculated from the datetime object using the current calendar and unit time reference.

        :param date: Date to be converted.
        :return:

        See also: https://cf-units.readthedocs.io/en/latest/unit.html#cf_units.Unit.date2num
        """
        return self._cfunit.date2num(date)

    def num2date(
        self,
        time_value: float | np.ndarray,
        only_use_cftime_datetimes: bool = True,
        only_use_python_datetimes: bool = False,
    ) -> datetime.datetime | np.ndarray:
        """
        Returns a datetime-like object calculated from the numeric time value using the current calendar and the unit time reference.

        :param time_value: Time value(s)
        :param only_use_cftime_datetimes:
            If True, will always return cftime datetime objects, regardless of calendar. If False, returns datetime.datetime instances where possible. Defaults to True.
        :param only_use_python_datetimes:
            If True, will always return datetime.datetime instances where possible, and raise an exception if not. Ignored if only_use_cftime_datetimes is True. Defaults to False.
        :return: Datetime or ndarray of datetime.

        See also: https://cf-units.readthedocs.io/en/latest/unit.html#cf_units.Unit.num2date
        """
        return self._cfunit.num2date(
            time_value, only_use_cftime_datetimes, only_use_python_datetimes
        )

    @classmethod
    def from_cf_units(cls, unit: cf_units.Unit) -> Self:
        """
        Initialize from a cf_units.Unit instance.

        :param unit: The input unit.

        :return: The output unit.
        """
        return cls(unit)
