from pydantic import BaseModel
from typing import Optional
from pyaro.timeseries import Filter


class PyaroConfig(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    data_id: str
    filename_or_obj_or_url: str
    filters: list[Filter]
    name_map: Optional[dict[str, str]] = None  # no Unit conversion option

    def json_repr(self):
        return self.model_dump()
