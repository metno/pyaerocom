from pydantic import BaseModel
from typing import Optional


class PyaroConfig(BaseModel):
    data_id: str
    filename_or_obj_or_url: str
    filters: list[str]
    name_map: Optional[dict[str, str]] = None
