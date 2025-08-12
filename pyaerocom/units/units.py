from __future__ import annotations
import datetime
import sys

from pyaerocom.units.molecular_mass import MolecularMass, UnknownSpeciesError, _get_species

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from collections.abc import Iterable


import cf_units
import numpy as np

from .datetime import TsType
from .datetime.time_config import SI_TO_TS_TYPE
from pyaerocom.variable_helpers import get_variable

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
    constant factor MolecularMass("SO4")/MolecularMass("S").

    The second behaviour is adding implicit frequency for rate variables
    and a ts_type. If tstype and aerocom_var are provided in __init__, units
    of the form "mg m-2" will automatically have the temporal frequency
    appended. For instance, assuming tstype='daily', it becomes "mg m-2 d-1"

    Third, cf_units.Unit does not natively support conversion of eg. pd.Series.
    This wrapper allows conversion of any data structure that supports __mul__.
    """

    # If found in the nominator, these are treated as elements for scaling units.
    _TREAT_AS_ELEMENT = ["C", "N", "S"]

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
        **kwargs,
    ) -> None:
        self._origin = str(unit)
        unit = Unit._UALIASES.get(str(unit), str(unit))

        self._species = kwargs.pop("species", None)
        if self._species is None:
            try:
                sp = _get_species(aerocom_var).upper()
            except (UnknownSpeciesError, AttributeError):
                pass
            else:
                self._species = sp

        self._element = None
        if self._species is not None:
            for e in Unit._TREAT_AS_ELEMENT:
                if e in self._origin_nominator:
                    unit = unit.replace(e, "", 1)
                    self._element = e
                    break

        if self._species is not None:
            try:
                MolecularMass(self._species)
            except ValueError:
                self._species = None
        if self._element is not None and self._species is not None:
            factor = MolecularMass(self._species) / MolecularMass(self._element)

        else:
            factor = 1

        if factor != 1:
            new_unit = f"{factor} {unit}"
        else:
            new_unit = unit

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

    @property
    def _origin_nominator(self) -> str:
        """
        The nominator of the original string used to initialize this Unit instance.
        """
        if "/" in self.origin:
            return self.origin.split("/")[0].strip()

        if "-" in self.origin:
            idx = self.origin.index("-")
            try:
                while self.origin[idx] not in [" ", "."]:
                    idx -= 1
            except IndexError:
                pass
            return self.origin[:idx].strip()

        return self.origin.strip()

    @property
    def _origin_denominator(self) -> str:
        """
        The denominator of the original string used to initialize this Unit instance.
        """
        if "/" in self.origin:
            return self.origin.split("/")[1].strip()

        if "-" in self.origin:
            idx = self.origin.index("-")
            while self.origin[idx] != " ":
                idx -= 1

            return self.origin[idx:].strip()

        return ""

    def _validate_convertible(self, other: str | Unit) -> None:
        """
        Validates whether the unit is convertible to another by raising an exception
        if not convertible:

        - Units that contain elements (eg. kg N m-2) need to have compatible mass ratios:
           - This is assumed to be the case if element and species are the same, the aerocom
           variable is the same (to account for variables that don't have a clear mass ratio —
           eg. wetrdn.)

        :param other: Other Unit.

        :raises ValueError: If unit is not convertible.
        """
        if isinstance(other, str):
            other = Unit(other)

        cf_units_only = self._element is None and other._element is None
        compatible_element = (
            (self._element is None)
            or (other._element is None)
            or (self._element == other._element)
        )
        same_species = (self._species is not None and other._species is not None) and (
            self._species == other._species
        )
        same_variable = (self._aerocom_var is None and other._aerocom_var is None) or (
            self._aerocom_var == other._aerocom_var
        )

        if cf_units_only:
            if not self._cfunit.is_convertible(other._cfunit):
                raise ValueError(
                    f"cfunit '{self._cfunit}' is not convertible to cfunit '{other._cfunit}'."
                )
        elif not compatible_element:
            raise ValueError(
                f"Element '{self._element}' is not compatible with '{other._element}'."
            )
        elif same_species and same_variable:
            if not self._cfunit.is_convertible(other._cfunit):
                raise ValueError(
                    f"cfunit '{self._cfunit}' is not convertible to cfunit '{other._cfunit}'."
                )
        elif (self._element == other._element) and same_variable:
            if not self._cfunit.is_convertible(other._cfunit):
                raise ValueError(
                    f"cfunit '{self._cfunit}' is not convertible to cfunit '{other._cfunit}'."
                )
        else:
            raise ValueError(
                f"Units {self} not convertible to {other}. If you believe this to be a bug, please raise an issue at https://github.com/metno/pyaerocom"
            )

    def is_convertible(self, other: str | Unit) -> bool:
        """
        Return whether this unit is convertible to other. It handles a couple of
        additional cases when checking convertibility, namely:

        - Units that contain elements (eg. kg N m-2) need to have compatible mass ratios:
           - This is assumed to be the case if element and species are the same, the aerocom
           variable is the same (to account for variables that don't have a clear mass ratio —
           eg. wetrdn.)

        :param other: Other Unit.
        """
        try:
            self._validate_convertible(other)
        except ValueError:
            return False

        return True

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
        result = f"Unit('{self.origin}'"
        if self._aerocom_var is not None:
            result += f", aerocom_var='{self._aerocom_var}'"
        if self._species is not None:
            result += f", species='{self._species}'"
        if self._ts_type is not None:
            result += f", ts_type='{self._ts_type}'"

        result += ")"
        return result

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
        if isinstance(other, Unit):
            to_unit = other
        elif isinstance(other, str):
            to_unit = Unit(str(other), **kwargs)
        else:
            raise TypeError(f"'other' must be of type str | Unit. Got {other}.")

        self._validate_convertible(to_unit)

        to_unit_cf = to_unit._cfunit
        factor = float(self._cfunit.convert(1, to_unit_cf, inplace=False))

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
