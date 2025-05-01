from typing import Literal
from pydantic import (
    BaseModel,
    field_validator,
)
from pyaerocom.aeroval.exceptions import ConfigError
from pyaerocom.aeroval.helpers import (
    BoundingBox,
)

from pyaerocom.aeroval.modelmaps_helpers import CONTOUR, OVERLAY


PLOT_TYPE_OPTIONS = ({OVERLAY}, {CONTOUR}, {OVERLAY, CONTOUR})


class ModelMapsSetup(BaseModel):
    maps_freq: Literal["hourly", "daily", "monthly", "yearly", "coarsest"] = "coarsest"
    plot_types: dict[str, str | set[str]] | set[str] = {CONTOUR}
    boundaries: BoundingBox = BoundingBox(west=-180, east=180, north=90, south=-90)
    right_menu: tuple[str, ...] | None = None
    overlay_save_format: Literal["webp", "png"] = "webp"

    @field_validator("plot_types")
    def validate_plot_types(cls, v):
        if isinstance(v, dict):
            for m in v:
                if not isinstance(v[m], set):
                    v[m] = set([v[m]])  # v[m] must be a string
                if v[m] not in PLOT_TYPE_OPTIONS:
                    raise ConfigError("Model maps set up given a non-valid plot type.")
            return v
        if isinstance(v, str):
            v = set([v])
        if isinstance(v, list):  # can occur when reading a serialized config
            v = set(v)
        if v not in PLOT_TYPE_OPTIONS:
            raise ConfigError("Model maps set up given a non-valid plot type.")
        return v
