from __future__ import annotations

import logging
from datetime import date, datetime
from pathlib import Path
from typing import Iterator

from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.ungriddeddata import UngriddedData

from .obs import read_csv

AEROCOM_NAMES = dict(
    CO="concco",
    NO2="concno2",
    O3="conco3",
    PM10="concpm10",
    PM25="concpm25",
    SO2="concso2",
)
DATA_FOLDER_PATH = Path("/lustre/storeB/project/fou/kl/CAMS2_83/obs")


logger = logging.getLogger(__name__)


def obs_paths(*dates: datetime | date | str) -> Iterator[Path]:
    for date in dates:
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y%m%d").date()
        if isinstance(date, datetime):
            date = date.date()

        path = DATA_FOLDER_PATH / date.strftime("%Y%m/obsmacc4verif_%Y%m%d.csv")
        if not path.is_file():
            logger.warning(f"Could not find {path.name}. Skipping {date}")
            continue
        yield path


class ReadCAMS2_83(ReadUngriddedBase):

    __version__ = "0.0.0"
    _FILEMASK = ""
    DATA_ID = "cams2_83"
    DEFAULT_VARS = list(AEROCOM_NAMES.values())
    PROVIDES_VARIABLES = DEFAULT_VARS
    SUPPORTED_DATASETS = [DATA_ID]
    TS_TYPE = "hourly"

    def read(
        self,
        vars_to_retrieve: str | list[str] | None = None,
        files: list[str | Path] | None = None,
        first_file=None,
        last_file=None,
    ) -> UngriddedData:
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        if isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        if not isinstance(vars_to_retrieve, list):
            raise TypeError(
                f"Unsupoerted type {type(vars_to_retrieve)}, "
                "vars_to_retrieve supported types are: str | list[str] | None"
            )
        assert all(
            var in self.PROVIDES_VARIABLES for var in vars_to_retrieve
        ), f"this dataset only has {self.PROVIDES_VARIABLES}"

        if files is None:
            files = list(obs_paths(date.today()))

        return UngriddedData.from_station_data(list(self.__reader(vars_to_retrieve, files)))

    @classmethod
    def __reader(cls, vars_to_retrieve: list[str], files: list[str | Path]) -> Iterator[dict]:
        for path in files:
            data = read_csv(path)
            for (station, poll), df in data.groupby(["station", "poll"]):
                if poll not in vars_to_retrieve:
                    continue
                conc = df["conc"]
                conc.name = AEROCOM_NAMES[poll]
                site = df.iloc[0]
                yield dict(
                    station_id=station,
                    station_name=site["Station name"],
                    latitude=df["lon"].iloc[0],
                    longitude=df["lat"].iloc[0],
                    altitude=df["alt"].iloc[0],
                    concch=conc,
                    var_info={conc.name: dict(units="ug m-3", ts_type=cls.TS_TYPE)},
                )
