from pydantic import BaseModel
from typing import Optional
from pyaro.timeseries import Engine


class PyaroConfig(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    engine: Engine  # Entrypoint name instead
    data_id: str
    filename_or_obj_or_url: str
    filters: list[str]
    name_map: Optional[dict[str, str]] = None  # no Unit conversion option
