from __future__ import annotations

import json
import logging
import multiprocessing as mp
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from datetime import date, datetime, timedelta
from enum import Enum
from pathlib import Path
from pprint import pformat
from typing import Optional

import pandas as pd
import typer
from dateutil.relativedelta import relativedelta

from pyaerocom import change_verbosity, const
from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
from pyaerocom.io import ReadUngridded
from pyaerocom.io.cams2_83.models import ModelName
from pyaerocom.io.cams2_83.read_obs import DATA_FOLDER_PATH as DEFAULT_OBS_PATH
from pyaerocom.io.cams2_83.read_obs import obs_paths
from pyaerocom.io.cams2_83.reader import DATA_FOLDER_PATH as DEFAULT_MODEL_PATH
from pyaerocom.scripts.cams2_83.config import CFG, species_list
from pyaerocom.scripts.cams2_83.processer import CAMS2_83_Processer
from pyaerocom.tools import clear_cache

"""
TODO:
    - Add option for species
    - Add option for periods [Done]
    - Add option for running only som observations/models/species
    - Add options with defaults for the different folders (data/coldata/cache)
"""


app = typer.Typer(add_completion=False)
logger = logging.getLogger(__name__)


class Eval_Type(str, Enum):
    LONG = "long"
    SEASON = "season"
    WEEK = "week"
    DAY = "day"

    def __str__(self) -> str:
        return self.value

    def check_dates(self, start_date: datetime, end_date: datetime) -> None:
        if self == "day" and start_date != end_date:
            raise ValueError(
                f"For single day, start and stop must be the same and not {start_date}-{end_date}"
            )

        if self == "week" and (end_date - start_date).days < 7:
            raise ValueError(
                f"For week, more than 7 days must be given. Only {(end_date-start_date).days} days were given"
            )

    def freqs_config(self) -> dict:
        if self == "long":
            return dict(
                freqs=["daily", "monthly"],
                ts_type="hourly",
                main_freq="daily",
                forecast_evaluation=True,
            )

        if self == "season":
            return dict(
                freqs=["hourly", "daily", "monthly"],
                ts_type="hourly",
                main_freq="hourly",
                forecast_evaluation=True,
            )

        if self == "week":
            return dict(
                freqs=["hourly", "daily"],
                ts_type="hourly",
                main_freq="hourly",
                forecast_evaluation=False,
            )
        if self == "day":
            return dict(
                freqs=["hourly"],
                ts_type="hourly",
                main_freq="hourly",
                forecast_evaluation=False,
            )

        raise NotImplementedError(f"Unsupported {self}")


def get_seasons_in_period(start_date: datetime, end_date: datetime) -> list[str]:
    seasons = ["DJF", "DJF", "MAM", "MAM", "MAM", "JJA", "JJA", "JJA", "SON", "SON", "SON", "DJF"]

    def get_season(date: pd.Timestamp):
        return seasons[date.month - 1]

    date_range = pd.date_range(start_date, end_date, freq="d")
    periods = []
    prev_date = start_period = date_range[0]
    prev_season = get_season(prev_date)
    for current_date in date_range[1:]:
        if get_season(current_date) == prev_season:
            prev_date = current_date
        else:
            periods.append(f"{start_period:%Y%m%d}-{prev_date:%Y%m%d}")
            prev_date = current_date
            prev_season = get_season(current_date)
            start_period = current_date

    else:
        if start_period == date_range[-1]:
            periods.append(f"{start_period:%Y%m%d}")
        else:
            periods.append(f"{start_period:%Y%m%d}-{date_range[-1]:%Y%m%d}")

    return periods


def get_years_starting_in_november(start_date: datetime, end_date: datetime) -> list[str]:
    periods = []
    prev_date = start_date
    new_yr = datetime(start_date.year, 12, 1)

    if new_yr > start_date:
        periods.append(f"{start_date:%Y%m%d}-{new_yr-timedelta(days=1):%Y%m%d}")
        prev_date = new_yr
        new_yr += relativedelta(years=1)
    else:
        if end_date < new_yr + relativedelta(years=1):
            return []
        periods.append(
            f"{start_date:%Y%m%d}-{new_yr+relativedelta(years=1)-timedelta(days=1):%Y%m%d}"
        )

        prev_date = new_yr + relativedelta(years=1)
        new_yr += relativedelta(years=2)

    for _ in range(end_date.year - start_date.year):
        if new_yr < end_date:
            periods.append(f"{prev_date:%Y%m%d}-{new_yr-timedelta(days=1):%Y%m%d}")
            prev_date = new_yr
            new_yr += relativedelta(years=1)
        else:
            periods.append(f"{prev_date:%Y%m%d}-{end_date:%Y%m%d}")
            break

    return periods


def make_period(start_date: datetime, end_date: datetime) -> list[str]:
    season_periods = get_seasons_in_period(start_date, end_date)
    nov_periods = get_years_starting_in_november(start_date, end_date)

    if start_date.date() == end_date.date():
        return [f"{start_date:%Y%m%d}"]

    periods = [f"{start_date:%Y%m%d}-{end_date:%Y%m%d}"]
    if periods != season_periods:
        periods += nov_periods  # season_periods

    return periods


def make_period_ys(start_date: datetime, end_date: datetime) -> list[str]:
    periods = [f"{start_date.year}-{end_date.year}"]
    periods.extend(str(yr) for yr in range(start_date.year, end_date.year + 1))
    return periods


def date_range(start_date: datetime | date, end_date: datetime | date) -> tuple[date, ...]:
    if isinstance(start_date, datetime):
        start_date = start_date.date()
    if isinstance(end_date, datetime):
        end_date = end_date.date()
    days = (end_date - start_date) // timedelta(days=1)
    assert days >= 0
    return tuple(start_date + timedelta(days=day) for day in range(days + 1))


def make_model_entry(
    start_date: datetime,
    end_date: datetime,
    leap: int,
    model_path: Path,
    obs_path: Path,
    model: ModelName,
    runtype: str,
) -> dict:
    return dict(
        model_id=f"CAMS2-83.{model.name}.day{leap}.{runtype}",
        model_data_dir=str(model_path.resolve()),
        gridded_reader_id={"model": "ReadCAMS2_83"},
        model_kwargs=dict(
            daterange=[f"{start_date:%F}", f"{end_date:%F}"],
        ),
    )


def make_config(
    start_date: datetime,
    end_date: datetime,
    leap: int,
    model_path: Path,
    obs_path: Path,
    data_path: Path,
    coldata_path: Path,
    models: list[ModelName],
    id: str,
    name: str,
    description: str,
    eval_type: Eval_Type | None,
    analysis: bool,
    only_map: bool,
    add_map: bool,
) -> dict:
    logger.info("Making the configuration")

    if not models:
        models = list(ModelName)

    if eval_type == "long":
        periods = make_period_ys(start_date, end_date)
    else:
        periods = make_period(start_date, end_date)

    cfg = deepcopy(CFG)
    cfg.update(
        model_cfg={
            f"{model.name}": make_model_entry(
                start_date,
                end_date,
                leap,
                model_path,
                obs_path,
                model,
                runtype="AN" if analysis else "FC",
            )
            for model in models
        },
        periods=periods,
        json_basedir=str(data_path),
        coldata_basedir=str(coldata_path),
    )

    if eval_type is not None:
        eval_type.check_dates(start_date, end_date)
        cfg.update(eval_type.freqs_config())

    extra_obs_days = 4 if eval_type in {"season", "long"} else 0
    cfg["obs_cfg"]["EEA"]["read_opts_ungridded"]["files"] = [  # type:ignore[index]
        str(p)
        for p in obs_paths(
            *date_range(start_date, end_date + timedelta(days=extra_obs_days)),
            root_path=obs_path,
            analysis=analysis,
        )
    ]

    if analysis:
        cfg.update(forecast_days=1)

    cfg.update(exp_id=id, exp_name=name, exp_descr=description)

    if add_map:
        cfg.update(add_model_maps=True)

    if only_map:
        cfg.update(add_model_maps=True, only_model_maps=True)

    return cfg


def read_observations(specie: str, *, files: list[str], cache: str | Path | None) -> None:
    logger.info(f"Running {specie}")
    if cache is not None:
        const.CACHEDIR = str(cache)

    reader = ReadUngridded()
    reader.read(data_ids="CAMS2_83.NRT", vars_to_retrieve=specie, files=files, force_caching=True)
    logger.info(f"Finished {specie}")


def run_forecast(specie: str, *, stp: EvalSetup, analysis: bool) -> None:
    ana_cams2_83 = CAMS2_83_Processer(stp)
    ana_cams2_83.run(analysis=analysis, var_list=specie)


def runner(
    cfg: dict,
    cache: str | Path | None,
    eval_type: Eval_Type | None,
    *,
    analysis: bool = False,
    dry_run: bool = False,
    quiet: bool = False,
    pool: int = 1,
):
    logger.info(f"Running the evaluation for the config\n{pformat(cfg)}")
    if dry_run:
        return

    if cache is not None:
        const.CACHEDIR = str(cache)

    if quiet:
        const.QUIET = True

    stp = EvalSetup(**cfg)
    logging.info(f"Clearing cache at {const.CACHEDIR}")
    clear_cache()

    if pool > 1:
        logger.info(f"Running observation reading with pool {pool}")
        files = cfg["obs_cfg"]["EEA"]["read_opts_ungridded"]["files"]
        with ProcessPoolExecutor(max_workers=pool) as executor:
            futures = [
                executor.submit(read_observations, specie, files=files, cache=cache)
                for specie in species_list
            ]
        for future in as_completed(futures):
            future.result()

    logger.info("Running Statistics")
    ExperimentProcessor(stp).run()
    logger.info("Done Running Statistics")


def runner_medians_cores(
    cfg: dict,
    cache: str | Path | None,
    *,
    analysis: bool = False,
    dry_run: bool = False,
    quiet: bool = False,
    pool: int = 1,
):
    if dry_run:
        return

    if cache is not None:
        const.CACHEDIR = str(cache)

    if quiet:
        const.QUIET = True

    stp = EvalSetup(**cfg)

    start = time.time()

    logger.info(
        "Running CAMS2_83 Specific Statistics, "
        "cache is not cleared, "
        "collocated data is assumed in place, "
        "regular statistics are assumed to have been run"
    )
    if pool > 1:
        logger.info(f"Making median scores plot with pool {pool} and analysis {analysis}")
        with ProcessPoolExecutor(max_workers=pool) as executor:
            futures = [
                executor.submit(run_forecast, specie, stp=stp, analysis=analysis)
                for specie in species_list
            ]
        for future in as_completed(futures):
            future.result()
    else:
        logger.info(f"Making median scores plot with pool {pool} and analysis {analysis}")
        CAMS2_83_Processer(stp).run(analysis=analysis)

    print(f"Long run: {time.time() - start} sec")


@app.command()
def main(
    start_date: datetime = typer.Argument(
        ..., formats=["%Y-%m-%d", "%Y%m%d"], help="evaluation start date"
    ),
    end_date: datetime = typer.Argument(
        ..., formats=["%Y-%m-%d", "%Y%m%d"], help="evaluation end date"
    ),
    leap: int = typer.Argument(0, min=0, max=3, help="forecast day"),
    model_path: Path = typer.Option(
        DEFAULT_MODEL_PATH, exists=True, readable=True, help="path to model data"
    ),
    obs_path: Path = typer.Option(
        DEFAULT_OBS_PATH, exists=True, readable=True, help="path to observation data"
    ),
    data_path: Path = typer.Option(
        Path("../../data").resolve(),
        exists=True,
        readable=True,
        # writable=True,
        help="where results are stored",
    ),
    coldata_path: Path = typer.Option(
        Path("../../coldata").resolve(),
        exists=True,
        readable=True,
        # writable=True,
        help="where the collocated data are stored",
    ),
    model: list[ModelName] = typer.Option(
        list(ModelName), "--model", "-m", case_sensitive=False, help="model(s) to evaluate"
    ),
    id: str = typer.Option(CFG["exp_id"], help="experiment ID"),
    name: str = typer.Option(CFG["exp_name"], help="experiment name"),
    description: str = typer.Option(CFG["exp_descr"], help="experiment description"),
    analysis: bool = typer.Option(
        False,
        "--analysis/--forecast",
        help="Sets the flag which tells the code to use the analysis model data. If false, the forecast model data is used",
    ),
    add_map: bool = typer.Option(
        False,
        "--addmap",
        help="Sets the flag which tells the code to set add_model_maps=True. Option is set to False otherwise",
    ),
    only_map: bool = typer.Option(
        False,
        "--onlymap",
        help="Sets the flag which tells the code to set add_model_maps=True and only_model_maps=True. Option is set to False otherwise",
    ),
    median_scores: bool = typer.Option(
        False,
        "--medianscores",
        help="If true just the cams2_83-specific statistics are computed, a.k.a. the median scores plots or 'weird' plots, the cache is not cleared and it's assumed that the collocated data is already in place and the regular statistics have already been run",
    ),
    cache: Optional[Path] = typer.Option(
        None,
        help="Optional path to cache. If nothing is given, the default pyaerocom cache is used",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-n",
        help="Will only make and print the config without running the evaluation",
    ),
    eval_type: Optional[Eval_Type] = typer.Option(
        None,
        "--eval-type",
        "-e",
        help="Type of evaluation.",
    ),
    pool: int = typer.Option(
        1,
        "--pool",
        "-p",
        help="Number of CPUs to be used for reading OBS and creating forecast plots",
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    if verbose or dry_run:
        change_verbosity(logging.INFO)

    if pool > mp.cpu_count():
        logger.warning(
            f"The given pool {pool} is larger than the maximum CPU count {mp.cpu_count()}. Using that instead"
        )
        pool = mp.cpu_count()

    # mp.set_start_method('forkserver')

    cfg = make_config(
        start_date,
        end_date,
        leap,
        model_path,
        obs_path,
        data_path,
        coldata_path,
        model,
        id,
        name,
        description,
        eval_type,
        analysis,
        only_map,
        add_map,
    )
    if dry_run:
        path = Path(f"{date.today():%Y%m%d}_{id}.json")
        path.write_text(json.dumps(cfg, indent=2))
        return

    if median_scores:
        if eval_type not in {"season", "long"}:
            logger.error(
                "Median scores calculations are only consistent with a season/long kind of evaluation"
            )
            raise typer.Abort()
        else:
            logger.info("Special run for median scores only")
            runner_medians_cores(
                cfg, cache, analysis=analysis, dry_run=dry_run, quiet=not verbose, pool=pool
            )
    else:
        logger.info("Standard run")
        runner(
            cfg, cache, eval_type, analysis=analysis, dry_run=dry_run, quiet=not verbose, pool=pool
        )
