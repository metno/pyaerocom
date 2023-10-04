from __future__ import annotations

import logging
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterator

import numpy as np
import pandas as pd

from pyaerocom import const
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


def obs_paths(
    *dates: datetime | date | str,
    root_path: Path | str = DATA_FOLDER_PATH,
    analysis: bool = False,
) -> Iterator[Path]:
    for date in dates:
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y%m%d").date()
        if isinstance(date, datetime):
            date = date.date()
        if isinstance(root_path, str):
            root_path = Path(root_path)
        if analysis:
            filename = "%Y%m/obsmacc4verifana_%Y%m%d.csv"
        else:
            filename = "%Y%m/obsmacc4verif_%Y%m%d.csv"
        path = root_path / date.strftime(filename)
        if not path.is_file():
            logger.warning(f"Could not find {path.name}. Skipping {date}")
            continue
        yield path.resolve()


class ReadCAMS2_83(ReadUngriddedBase):
    __version__ = "0.0.0"
    _FILEMASK = ""
    DATA_ID = const.CAMS2_83_NRT_NAME
    DEFAULT_VARS = list(AEROCOM_NAMES.values())
    PROVIDES_VARIABLES = DEFAULT_VARS
    SUPPORTED_DATASETS = [DATA_ID]
    TS_TYPE = "hourly"

    def read(
        self,
        vars_to_retrieve: str | list[str] | None = None,
        files: list[str | Path] | None = None,
        first_file: int | None = None,
        last_file: int | None = None,
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
            files = list(obs_paths(date.today() - timedelta(days=1)))
        if first_file is not None:
            files = files[first_file:]
        if last_file is not None:
            files = files[:last_file]

        start = time.time()
        data = list(self.__reader(vars_to_retrieve, files))
        end = time.time()
        print(end - start)

        ungriddeddata = UngriddedData.from_station_data(data)
        print(time.time() - end, (time.time() - end) / 60.0)
        return ungriddeddata

    def read_file(self, filename, vars_to_retrieve=None):
        return self.read(vars_to_retrieve, [filename])

    @classmethod
    def __reader(cls, vars_to_retrieve: list[str], files: list[str | Path]) -> Iterator[dict]:
        logger.debug(f"reading {cls.DATA_ID} {vars_to_retrieve=} from {files=}")
        data = pd.concat(read_csv(path) for path in files).drop_duplicates(
            subset=["station", "poll", "time"]
        )
        df: pd.DataFrame
        for station, df in data.groupby("station"):
            logging.info(f"Reading obs for station {station} and variables {vars_to_retrieve}")
            output = dict(
                station_id=station,
                station_name=station,
                latitude=df["lat"].iloc[0],
                longitude=df["lon"].iloc[0],
                altitude=df["alt"].iloc[0],
                variables=cls.DEFAULT_VARS,
                var_info=dict.fromkeys(cls.DEFAULT_VARS, dict(units="ug m-3")),
                data_id=cls.DATA_ID,
                ts_type=cls.TS_TYPE,
            )
            df = df.pivot(index="time", columns="poll", values="conc")
            missing = {poll for poll in AEROCOM_NAMES if poll not in df}
            if missing.issubset(vars_to_retrieve):
                logger.debug(f"no relevant data on {station=}, skip")
                continue
            for poll in missing:
                df[poll] = np.nan
            df = df.rename(AEROCOM_NAMES, axis="columns")
            for poll in cls.DEFAULT_VARS:
                output[poll] = df[poll]
            yield output