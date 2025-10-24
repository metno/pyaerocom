from __future__ import annotations

import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import date, timedelta
from enum import Enum
from pathlib import Path
from pprint import pformat

from pyaerocom import ConfigReader
from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
from pyaerocom.io import ReadUngridded
from pyaerocom.io.cachehandler_ungridded import list_cache_files

logger = logging.getLogger(__name__)

const = ConfigReader.get_instance()


def clear_cache():
    """Delete cached data objects"""
    for path in list_cache_files():
        path.unlink()


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

    logger.info("Running Statistics")
    ExperimentProcessor(stp).run()
    logger.info("Done Running Statistics")
