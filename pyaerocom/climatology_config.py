from pydantic import BaseModel, ValidationError, model_validator

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
    min_count : dict, optional
        Number of values should be present for the data to be used in the climatology.
        Dict where freqs are the keys and the count is the values

    """

    start: int = const.CLIM_START
    stop: int = const.CLIM_STOP

    set_year: int | None = None

    resample_how: Literal["mean", "median"] = const.CLIM_RESAMPLE_HOW
    freq: str = const.CLIM_FREQ
    min_count: dict = const.CLIM_MIN_COUNT

    @model_validator(mode="after")
    def validate_set_year(self):
        if self.set_year is None:
            self.set_year = int((self.stop - self.start) // 2 + self.start) + 1

        if self.set_year > 2100:
            raise ValidationError
        return self
