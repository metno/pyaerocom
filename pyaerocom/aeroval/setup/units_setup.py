from pydantic import BaseModel


class UnitsSetup(BaseModel):
    """
    Unit setup options

    Attributes
    ----------
    units : dict[str, str]
        A dictionary specifying a mapping from variable name (eg. concno2) to unit. All unit conversion
        by pyaerocom will use this unit for harmonisation if provided. If not provided, the unit specified
        in variables.ini will be used.
    """

    units: dict[str, str] = {}
