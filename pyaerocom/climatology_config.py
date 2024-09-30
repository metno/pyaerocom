from pydantic import (
    BaseModel,
    ValidationError,
    field_validator,
)

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

    resample_how: str = const.CLIM_RESAMPLE_HOW
    freq: str = const.CLIM_FREQ
    mincount: dict = const.CLIM_MIN_COUNT

    @field_validator("resample_how")
    @classmethod
    def validate_resample_how(cls, v):
        if v in ["mean", "median"]:
            return v

        raise ValidationError
