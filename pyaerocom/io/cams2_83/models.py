from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import NamedTuple


class ModelName(str, Enum):
    ENSEMBLE = "ensemble"
    CHIMERE = "chimere"
    DEHM = "dehm"
    EMEP = "emep"
    EURAD = "euradim"
    GEMAQ = "gemaq"
    LOTOS = "lotos"
    MATCH = "match"
    MINNI = "minni"
    MOCAGE = "mocage"
    MONARCH = "monarch"
    SILAM = "silam"
    IFS = "ifs"

    def __str__(self) -> str:
        return self.value


class RunType(str, Enum):
    FC = "forecast"
    AN = "analysis"

    def __str__(self) -> str:
        return self.value

    @property
    def days(self) -> int:
        return dict(FC=3, AN=0)[self.name]


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
