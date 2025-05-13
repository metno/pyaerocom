from pydantic import BaseModel


class UnitsSetup(BaseModel):
    units: dict[str, str] = {}
