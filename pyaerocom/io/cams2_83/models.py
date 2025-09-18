from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import NamedTuple


class ModelName(str, Enum):
    member00 = "member00"
    member01 = "member01"
    member02 = "member02"
    member03 = "member03"
    member04 = "member04"
    member05 = "member05"
    member06 = "member06"
    member07 = "member07"
    member08 = "member08"
    member09 = "member09"
    member10 = "member10"
    member11 = "member11"
    member12 = "member12"
    member13 = "member13"
    member14 = "member14"
    member15 = "member15"
    member16 = "member16"
    member17 = "member17"
    member18 = "member18"
    member19 = "member19"
    member20 = "member20"
    member21 = "member21"
    member22 = "member22"
    member23 = "member23"
    member24 = "member24"
    member25 = "member25"
    member26 = "member26"
    member27 = "member27"
    member28 = "member28"
    member29 = "member29"
    member30 = "member30"
    member31 = "member31"
    member32 = "member32"
    member33 = "member33"
    member34 = "member34"
    member35 = "member35"
    member36 = "member36"
    member37 = "member37"
    member38 = "member38"
    member39 = "member39"
    member40 = "member40"
    member41 = "member41"
    member42 = "member42"
    member43 = "member43"
    member44 = "member44"
    member45 = "member45"
    member46 = "member46"
    member47 = "member47"
    member48 = "member48"
    member49 = "member49"
    member50 = "member50"

    def __str__(self) -> str:
        return self.value

    @property
    def webname(self) -> str:
        return dict(
            member00="mbr00",
            member01="mbr01",
            member02="mbr02",
            member03="mbr03",
            member04="mbr04",
            member05="mbr05",
            member06="mbr06",
            member07="mbr07",
            member08="mbr08",
            member09="mbr09",
            member10="mbr10",
            member11="mbr11",
            member12="mbr12",
            member13="mbr13",
            member14="mbr14",
            member15="mbr15",
            member16="mbr16",
            member17="mbr17",
            member18="mbr18",
            member19="mbr19",
            member20="mbr20",
            member21="mbr21",
            member22="mbr22",
            member23="mbr23",
            member24="mbr24",
            member25="mbr25",
            member26="mbr26",
            member27="mbr27",
            member28="mbr28",
            member29="mbr29",
            member30="mbr30",
            member31="mbr31",
            member32="mbr32",
            member33="mbr33",
            member34="mbr34",
            member35="mbr35",
            member36="mbr36",
            member37="mbr37",
            member38="mbr38",
            member39="mbr39",
            member40="mbr40",
            member41="mbr41",
            member42="mbr42",
            member43="mbr43",
            member44="mbr44",
            member45="mbr45",
            member46="mbr46",
            member47="mbr47",
            member48="mbr48",
            member49="mbr49",
            member50="mbr50",
        )[self.name]


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
