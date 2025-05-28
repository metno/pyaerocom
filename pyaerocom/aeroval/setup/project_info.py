from pydantic import BaseModel


class ProjectInfo(BaseModel):
    proj_id: str
