from __future__ import annotations
import sys

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

_ELEMENT_MASS = {
    "H": 1.00794,
    "Be": 9.0122,
    "C": 12.0107,
    "N": 14.0067,
    "O": 15.9994,
    "Ca": 40.078,
    "S": 32.065,
}

_VAR_PREFIXES = [
    # These are checked in the order written, so should be ordered by most specific to least specific (eg. concN before conc).
    "vmr",
    "mmr",
    "sconc",
    "concNt",
    "concN",
    "concC",
    "conc",
    "wet",
    "dry",
    "proxydry",
    "proxywet",
    "dep",
]

_MOLMASSES = {
    # Override molecular masses used for species that do not constitute molecular
    # formulas with only single letter elements.
    "air_dry": 28.9647,
    "isop": 68.12,
    "glyoxal": 58.036,
    "glyox": 58.036,
}


class UnknownSpeciesError(ValueError):
    pass


def _get_species(aerocom_var: str) -> str:
    """
    Get species name from variable name

    Parameters
    ----------
    var_name : str
        pyaerocom variable name (cf. variables.ini)

    Raises
    ------
    UnknownSpeciesError
        if species cannot be inferred

    Returns
    -------
    str
        name of species

    """
    if aerocom_var in _MOLMASSES:
        return aerocom_var
    for prefix in _VAR_PREFIXES:
        if aerocom_var.startswith(prefix):
            species = aerocom_var.split(prefix)[-1]
            # if species in _MOLMASSES:
            return species

    raise UnknownSpeciesError(
        f"Could not infer atom / molecule/ species from var_name {aerocom_var}"
    )


class MolecularMass:
    """This class represents the mass of simple molecular formulas
    and permits arithmetic calculations on them.
    """

    def __init__(self, val: str | int | float, *, label: str | None = None):
        """
        :param val: Either a chemical formula (eg. H2O) or a numeric mass.
        :param label: Optional label. Defaults to the chemical formula / chemical mass.

        :raises ValueError: If val is negative.
        """
        if isinstance(val, float | int):
            if val < 0:
                raise ValueError("Molecular mass can not be less than zero.")
            self._mass = float(val)
        else:
            self._mass = self._mass_from_chemical_formula(val)

        if isinstance(val, str) and label is None:
            self._label: str | None = val
        else:
            self._label = label

    @property
    def mass(self) -> float:
        """
        :return: The mass value (in Dalton).
        """
        return self._mass

    @property
    def label(self) -> str:
        """
        :return: Human readable description of the mass (eg. '1 u' or 'H2O')
        """
        if self._label is None:
            return f"{self.mass:.4f} u"

        return self._label

    def _mass_from_chemical_formula(self, val: str) -> float:
        """Determines the mass of simple chemical formulas.

        :param val: Chemicala formula as string (see limitations below).
        :raises ValueError: If there are brackets in the formula.
        :raises ValueError: If element masses are not defined in _ELEMENT_MASSES dict.

        :return: Molecular mass (in daltons).

        Limitations:
        ------------
        - Elements must have their first character and only the first capitalized.
        - Numeric subscripts are limited to one digit.
        - No brackets.
        """
        # Limitations
        # Does not support brackets (eg. Ca(OH)2).
        # Does not support multidigit numbers (eg. C6H12O6).
        if "(" in val or ")" in val:
            raise ValueError("Brackets are not currently supported.")
        mass: float = 0
        i = 0
        while i < len(val):
            offset = 0
            element = val[i]
            if i + 1 < len(val):
                if val[i + 1].islower():
                    element += val[i + 1]
                    offset += 1
            if i + offset + 1 < len(val):
                if val[i + offset + 1].isdigit():
                    count = int(val[i + offset + 1])
                    offset += 1
                else:
                    count = 1
            else:
                count = 1

            try:
                mass += count * _ELEMENT_MASS[element]
            except KeyError as e:
                raise ValueError(f"Unable to parse chemical formula '{val}'") from e

            i += offset + 1

        return mass

    def __add__(self, other) -> MolecularMass:
        if isinstance(other, MolecularMass):
            return MolecularMass(self.mass + other.mass)

        return MolecularMass(self.mass + other)

    def __radd__(self, other) -> MolecularMass:
        return self.__add__(other)

    def __sub__(self, other) -> MolecularMass:
        if isinstance(other, MolecularMass):
            return MolecularMass(self.mass - other.mass)

        return MolecularMass(self.mass - other)

    def __mul__(self, other) -> float:
        if isinstance(other, MolecularMass):
            self.mass * other.mass

        return self.mass * other

    def __rmul__(self, other) -> float:
        return self.__mul__(other)

    def __truediv__(self, other) -> float:
        if isinstance(other, MolecularMass):
            return self.mass / other.mass

        return self.mass / other

    def __float__(self) -> float:
        return float(self.mass)

    @override
    def __repr__(self) -> str:
        return f"MolecularMass('{self.label}')"

    @override
    def __str__(self) -> str:
        return self.label

    @staticmethod
    def from_aerocom_var(aerocom_var: str) -> MolecularMass:
        """Produces a MolecularMass from an var_name. It will first check
        the override dict _MOLMASSES. If the var_name is not defined there
        it will try to extract the chemical formula from the name (eg. 'concso2'->'SO2').

        :param aerocom_var: string (See variables.ini).

        :return: MolecularMass of element.
        """
        species = _get_species(aerocom_var)
        if species in _MOLMASSES:
            return MolecularMass(_MOLMASSES[species], label=species)
        return MolecularMass(species.upper())


def get_molmass(aerocom_varname: str) -> float:
    """
    Get molar mass for input variable

    Parameters
    ----------
    var_name : str
        pyaerocom variable name (cf. variables.ini) or name of species

    Returns
    -------
    float
        molar mass of species in units of g/mol

    Note:
    Will break with molecular formulas that contain 2-letter elements (eg. Ca)
    since this relies on upper case conversion to make it understandable for
    MolecularMass.__init__(). For now such species should be defined manually
    in the override dict _MOLMASSES.
    """
    try:
        mass = MolecularMass.from_aerocom_var(aerocom_varname).mass
    except UnknownSpeciesError:
        # This function previously was used on pure formulas even though it is only
        # supposed to be used on var_names.
        # This maintains backward compatibility for those cases.
        mass = MolecularMass(aerocom_varname.upper()).mass

    return mass


def get_mmr_to_vmr_fac(aerocom_varname: str) -> float:
    """
    Get conversion factor for MMR -> VMR conversion for input variable

    Note
    ----
    Assumes dry air molar mass

    Parameters
    ----------
    var_name : str
        Name of variable to be converted

    Returns
    -------
    float
        multiplication factor to convert MMR -> VMR
    """
    return get_molmass("air_dry") / get_molmass(aerocom_varname)
