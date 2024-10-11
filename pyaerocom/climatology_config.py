from pydantic import BaseModel, ValidationError, field_validator

from typing import Literal

from pyaerocom import const


class ClimatologyConfig(BaseModel):
    """
    Holds the configuration for the climatology

    Attributes
    -------------
    start : int, optional
        Start year of the climatology
    stop : int, optional
        Stop year of the climatology
    resample_how : str, optional
        How to resample the climatology. Must be mean or median.
    freq : str, optional
        Which frequency the climatology should have
    mincount : dict, optional
        Number of values should be present for the data to be used in the climatology.
        Dict where freqs are the keys and the count is the values

    """

    start: int = const.CLIM_START
    stop: int = const.CLIM_STOP

    set_year: int | None = None

    @field_validator("set_year")
    @classmethod
    def validate_set_year(cls, v):
        if v is None:
            return int((cls.stop - cls.start) // 2 + cls.start) + 1

        if v > cls.stop or v < cls.start:
            raise ValidationError

        return v

    resample_how: Literal["mean", "median"] = const.CLIM_RESAMPLE_HOW
    freq: str = const.CLIM_FREQ
    mincount: dict = const.CLIM_MIN_COUNT
