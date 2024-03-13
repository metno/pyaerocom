from __future__ import annotations

import logging
from importlib import resources
from pathlib import Path
from typing import ClassVar, Optional

import yaml
from pydantic import BaseModel

import pyaerocom as pya

logger = logging.getLogger(__name__)


class PyaroConfig(BaseModel):
    _DEFAULT_CATALOG: ClassVar[Path] = resources.files(pya) / Path(
        "data/pyaro_catalogs/default.yaml"
    )

    class Config:
        arbitrary_types_allowed = True

    ##########################
    #   Model fields
    ##########################

    name: str
    data_id: str
    filename_or_obj_or_url: str
    filters: dict[str, dict[str, list[str]]]
    name_map: Optional[dict[str, str]] = None  # no Unit conversion option

    ##########################
    #   Save and load methods
    ##########################

    def json_repr(self):
        return self.model_dump()

    def save(self, path: Optional[Path] = None) -> None:
        name = self.name

        if not path.is_dir():
            raise ValueError(f"{path} must be a directory")
        filename = path / "catalog.yaml" if path is not None else "catalog.yaml"

        if name in self.load_catalog(filepath=filename):
            raise ValueError(f"{name} already exists in catalog {filename}")
        if name in self.load_catalog():
            raise ValueError(f"{name} already exists in default catalog")

        body = {name: self.json_repr()}
        with open(filename, "w") as f:
            yaml.safe_dump(body, f)

    @classmethod
    def from_dict(cls, data: dict):
        return PyaroConfig.model_validate(data)

    @classmethod
    def load(cls, name: str, filepath: Optional[Path] = None):
        if filepath is not None:
            if filepath.is_dir():
                raise ValueError(f"Filepath {filepath} is a directory not a file")
            elif not filepath.exists():
                raise ValueError(f"No catalog with this name exists {filepath}")

        data = cls.load_catalog(filepath)

        if name in data:
            return PyaroConfig.from_dict(data[name])
        else:
            raise ValueError(f"Config {name} was not found in any catalogs")

    @classmethod
    def list_configs(cls, filepath: Optional[Path] = None) -> list[str]:
        data = cls.load_catalog()
        if filepath is not None:
            logger.info(f"Updating with private catalog {filepath}")
            data.update(cls.load_catalog(filepath))

        return list(data.keys())

    @classmethod
    def load_catalog(cls, filepath: Optional[Path] = None) -> dict:
        if filepath is None:
            filepath = cls._DEFAULT_CATALOG

        if not filepath.exists():
            return {}

        with open(filepath, "r") as f:
            data = yaml.safe_load(f)

        return data
