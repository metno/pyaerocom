from pydantic import BaseModel
from typing import Optional
from pyaerocom_readers import TimeseriesReader


class PyaroConfig(BaseModel):
    engine: TimeseriesReader
    data_id: str
    filename_or_obj_or_url: str
    filters: list[str]
    name_map: Optional[dict[str, str]] = None
