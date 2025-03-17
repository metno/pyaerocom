import sys

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

_ELEMENT_MASS = {"H": 1.0079, "Be": 9.0122, "C": 12.0107, "N": 14.0067, "O": 15.9994, "S": 32.065}


class MolecularMass:
    """This class represents the mass of simple molecular formulas
    and permits arithmetic calculations on them.
    """

    def __init__(self, val: str | float, *, label: str | None = None):
        if isinstance(val, float):
            self._mass = val
        else:
            self._mass = self._mass_from_chemical_formula(val)

        if isinstance(val, str) and label is None:
            self._label: str | None = val
        else:
            self._label = label

    @property
    def mass(self) -> float:
        return self._mass

    @property
    def label(self) -> str:
        if self._label is None:
            return f"{self.mass:.4f} u"

        return self._label

    def _mass_from_chemical_formula(self, val: str) -> float:
        # Limitations
        # Does not support brackets (eg. Ca(OH)2).
        # Does not support multidigit numbers (eg. C6H12O6).
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

            mass += count * _ELEMENT_MASS[element]

            i += offset + 1

        return mass

    @override
    def __add__(self, other):
        if isinstance(other, MolecularMass):
            return MolecularMass(self.mass + other.mass)

        return MolecularMass(self.mass + other)

    @override
    def __sub__(self, other):
        if isinstance(other, MolecularMass):
            return MolecularMass(self.mass - other.mass)

        return MolecularMass(self.mass - other)

    @override
    def __mul__(self, other):
        if isinstance(other, MolecularMass):
            return MolecularMass(self.mass * other.mass)

        return MolecularMass(self.mass * other)

    @override
    def __rmul__(self, other):
        return self.__mul__(other)

    @override
    def __truediv__(self, other):
        if isinstance(other, MolecularMass):
            return self.mass / other.mass

        return self.mass / other
