from pydantic import BaseModel
from typing import Optional, ClassVar, Self
from pyaro.timeseries import Filter
import pyaro.timeseries
import yaml
import os
from pathlib import Path
from importlib import resources
import pyaerocom as pya




class PyaroConfig(BaseModel):
    _DEFAULT_CATALOG: ClassVar[Path] = resources.files(pya) / Path("data/pyaro_catalogs/default.yaml")
    class Config:
        arbitrary_types_allowed = True

    data_id: str
    filename_or_obj_or_url: str
    #filters: list[Filter]
    filters: dict[str, dict[str, str | list[str]]]
    name_map: Optional[dict[str, str]] = None  # no Unit conversion option

    def json_repr(self):
        return self.model_dump()
    
    def save(self, name: str, path: Optional[Path] = None) -> None:
        filename = path / "catalog.yaml" if path is not None else "catalog.yaml"
        body = {name: self.json_repr()}
        with open(filename, "w") as f:
            yaml.safe_dump(body, f)
        

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return PyaroConfig.model_validate(data)


    @classmethod
    def load(cls, name: str, filepath: Optional[Path] = None) -> Self:
        data = cls.load_all(filepath)

        if name in data:
            return PyaroConfig.from_dict(data[name])
        else:
            raise ValueError(f"Config {name} was not find in catalog found at {filepath}")
        
        

    
    @classmethod
    def list_configs(cls, filepath: Optional[Path] = None) -> list[str]:
        data = cls.load_all()
        if filepath is not None:
            print(f"Updating with private catalog {filepath}")
            data.update(cls.load_all(filepath))

        return list(data.keys())

    
    @classmethod
    def load_all(cls, filepath: Optional[Path] = None) -> dict:
        if filepath is None:
            filepath = cls._DEFAULT_CATALOG
        
        if not filepath.exists():
            raise ValueError(f"File {filepath} does not exist")

        with open(filepath, "r") as f:
            data = yaml.safe_load(f)

        return data



    
        

    

if __name__=="__main__":
    data_id = "aeronetsunreader"
    url = "https://pyaerocom.met.no/pyaro-suppl/testdata/aeronetsun_testdata.csv"

    config = PyaroConfig(
        data_id=data_id,
        filename_or_obj_or_url=url,
        #filters=[pyaro.timeseries.filters.get("variables", include=["AOD_550nm"])],
        filters={"variables": {"include": ["AOD_550nm"]}},
        name_map={"AOD_550nm": "od550aer"},
    )

    #config.save("test_config")
    print(config.list_configs(Path("./catalog.yaml")))
    print(config.load("test_config"))