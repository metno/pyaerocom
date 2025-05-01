from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)
from typing import Literal


class WebDisplaySetup(BaseModel):
    # Pydantic ConfigDict
    model_config = ConfigDict(protected_namespaces=())
    # WebDisplaySetup attributes
    map_zoom: Literal["World", "Europe", "xEMEP"] = "World"
    regions_how: Literal["default", "aerocom", "htap", "country"] = "default"
    map_zoom: str = "World"
    add_model_maps: bool = False
    modelorder_from_config: bool = True
    obsorder_from_config: bool = True
    var_order_menu: tuple[str, ...] = ()
    obs_order_menu: tuple[str, ...] = ()
    stats_order_menu: tuple[str, ...] = ()
    model_order_menu: tuple[str, ...] = ()
    hide_charts: tuple[str, ...] = ()
    hide_pages: tuple[str, ...] = ()
    ts_annotations: dict[str, str] = Field(default_factory=dict)
    pages: tuple[str, ...] = ("maps", "evaluation", "intercomp", "overall", "infos")
