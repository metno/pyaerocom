from pydantic import BaseModel, RootModel, ConfigDict


# Pydantic models for menu.json


class MenuModelEntry(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    model_id: str
    model_var: str
    obs_var: str
    longname: str = ""


class MenuModel(RootModel[dict[str, MenuModelEntry]]):
    pass


class MenuLevel(RootModel[dict[str, MenuModel]]):
    pass


class MenuEntry(BaseModel):
    type: str
    cat: str
    name: str
    obs_longnames: dict[str, str] | None = None
    obs: dict[str, MenuLevel]


class Menu(RootModel[dict[str, MenuEntry]]):
    def return_validated(self, val: dict) -> dict:
        return self.model_validate(val).model_dump()
