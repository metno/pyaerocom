from pydantic import BaseModel, RootModel


# Pydantic models for menu.json


class MenuModelEntry(BaseModel):
    model_id: str
    model_var: str
    obs_var: str
    longname: str


class MenuModel(RootModel[dict[str, MenuModelEntry]]):
    pass


class MenuLevel(RootModel[dict[str, MenuModel]]):
    pass


class MenuEntry(BaseModel):
    type: str
    cat: str
    name: str
    obs_longnames: dict[str, str]
    obs: dict[str, MenuLevel]


class Menu(RootModel[dict[str, MenuEntry]]):
    pass
