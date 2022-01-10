from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import NamedTuple


class ModelName(str, Enum):
    EMEP = "emep"
    DEHM = "dehm"
    EURAD = "euradim"
    GEMAQ = "gemaq"
    LOTOS = "lotos"
    MATCH = "match"
    SILAM = "silam"
    MOCAGE = "mocage"
    CHIMERE = "chimere"
    ENSEMBLE = "ensemble"

    def __str__(self) -> str:
        return self.value


class RunType(str, Enum):
    FC = "forecast"
    AN = "analysis"

    def __str__(self) -> str:
        return self.value


class ModelData(NamedTuple):
    name: ModelName
    run: RunType
    date: date = date.today()
    root: Path = Path.cwd()

    def __str__(self) -> str:
        return f"{self.name.name} {self.date:%F} {self.run.name}"

    @property
    def path(self) -> Path:
        return self.root / self.date.strftime(f"%Y%m/%Y%m%d_{self.name}_{self.run}.nc")

    @classmethod
    def frompath(cls, path: str | Path) -> ModelData:
        if isinstance(path, str):
            path = Path(path)
        date, name, run = path.stem.split("_")
        return cls(
            ModelName(name),
            RunType(run),
            datetime.strptime(date, "%Y%m%d").date(),
            path.parents[1],
        )
