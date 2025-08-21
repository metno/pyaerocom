from __future__ import annotations

import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import date, timedelta
from enum import Enum
from pathlib import Path
from pprint import pformat

from pyaerocom import const
from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
from pyaerocom.io import ReadUngridded
from pyaerocom.io.cachehandler_ungridded import list_cache_files
#from pyaerocom.scripts.cams2_83.config import species_list
#from pyaerocom.scripts.cams2_82.cli import make_period


logger = logging.getLogger(__name__)


# class EvalType(str, Enum):
#     LONG = "long"
#     SEASON = "season"
#     WEEK = "week"
#     DAY = "day"

#     def __str__(self) -> str:
#         return self.value

#     def check_dates(self, start_date: date, end_date: date) -> None:
#         if end_date < start_date:
#             raise ValueError("End date should be ⩾ start_date")
#         if self == "day" and start_date != end_date:
#             raise ValueError(
#                 f"Evaluation type 'day' should have the same {start_date=} and {end_date=}"
#             )

#         if self == "week" and (days := (end_date - start_date) // timedelta(days=1)) < 7:
#             raise ValueError(f"Evaluation type 'week' should have {days=} >= 7")

#     def freqs_config(self) -> dict:
#         if self == "long":
#             return dict(
#                 freqs=["daily", "monthly"],
#                 ts_type="hourly",
#                 main_freq="daily",
#                 forecast_evaluation=True,
#             )

#         if self == "season":
#             return dict(
#                 freqs=["hourly", "daily"],
#                 ts_type="hourly",
#                 main_freq="hourly",
#                 forecast_evaluation=True,
#             )

#         if self == "week":
#             return dict(
#                 freqs=["hourly", "daily"],
#                 ts_type="hourly",
#                 main_freq="hourly",
#                 forecast_evaluation=False,
#             )
#         if self == "day":
#             return dict(
#                 freqs=["hourly"],
#                 ts_type="hourly",
#                 main_freq="hourly",
#                 forecast_evaluation=False,
#             )

#         raise NotImplementedError(f"Unsupported {self}")

#     def periods(self, start_date: date, end_date: date) -> list[str]:
#         if self == "long":
#             if (start_date.year != end_date.year):
#                 return make_period_ys(start_date, end_date)
#         return make_period(start_date, end_date)


# def make_period_ys(start_date: date, end_date: date) -> list[str]:
#     periods = [f"{start_date.year}-{end_date.year}"]
#     periods.extend(str(yr) for yr in range(start_date.year, end_date.year + 1))
#     return periods


def clear_cache():
    """Delete cached data objects"""
    for path in list_cache_files():
        path.unlink()


# def read_observations(specie: str, *, files: list, cache: str | Path | None) -> None:
#     logger.info(f"Running {specie}")

#     if cache is not None:
#         const.CACHEDIR = str(cache)

#     reader = ReadUngridded()

#     reader.read(
#         data_ids="CAMS2_83.NRT",
#         vars_to_retrieve=specie,
#         files=files,
#         force_caching=True,
#     )

#     logger.info(f"Finished {specie}")




def runner(
    cfg: dict,
    cache: str | Path | None,
    dry_run: bool = False,
    pool: int = 1,
):
    logger.info(f"Running the evaluation for the config\n{pformat(cfg)}")
    if dry_run:
        return

    if cache is not None:
        const.CACHEDIR = str(cache)

    stp = EvalSetup(**cfg)

    logger.info(f"Clearing cache at {const.CACHEDIR}")
    clear_cache()

    #if pool > 1:
    #    logger.info(f"Running observation reading with pool {pool}")
    #    files = cfg["obs_cfg"]["EEA"]["read_opts_ungridded"]["files"]
    #    with ProcessPoolExecutor(max_workers=pool) as executor:
    #        futures = [
    #            executor.submit(read_observations, specie, files=files, cache=cache)
    #            for specie in species_list
    #        ]
    #    for future in as_completed(futures):
    #        future.result()

    logger.info("Running Statistics")
    ExperimentProcessor(stp).run()
    logger.info("Done Running Statistics")
