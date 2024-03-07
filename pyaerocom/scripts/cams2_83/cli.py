from __future__ import annotations

import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from datetime import date, datetime, timedelta
from enum import Enum
from multiprocessing import cpu_count
from pathlib import Path
from pprint import pformat
from typing import List, Optional

import pandas as pd
import typer
from dateutil.relativedelta import relativedelta

from pyaerocom import change_verbosity, const
from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
from pyaerocom.io import ReadUngridded
from pyaerocom.io.cams2_83.models import ModelName, RunType
from pyaerocom.io.cams2_83.read_obs import DATA_FOLDER_PATH as DEFAULT_OBS_PATH
from pyaerocom.io.cams2_83.read_obs import obs_paths
from pyaerocom.io.cams2_83.reader import DATA_FOLDER_PATH as DEFAULT_MODEL_PATH
from pyaerocom.tools import clear_cache

from .config import CFG, obs_filters, species_list
from .processer import CAMS2_83_Processer

"""
TODO:
    - Add option for species
    - Add option for periodes [Done]
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


def check_dates_from_eval(
    eval_type: Eval_Type | None, start_date: datetime, end_date: datetime
) -> None:
    if eval_type == "day" and start_date != end_date:
        raise ValueError(
            f"For single day, start and stop must be the same and not {start_date}-{end_date}"
        )
    elif eval_type == "week" and (end_date - start_date).days < 7:
        raise ValueError(
            f"For week, more than 7 days must be given. Only {(end_date-start_date).days} days were given"
        )


def update_freqs_from_eval_type(eval_type: Eval_Type | None) -> dict:
    if eval_type is None:
        return {}

    if eval_type == "long":
        return dict(
            freqs=["daily", "monthly"],
            ts_type="hourly",
            main_freq="daily",
            forecast_evaluation=True,
        )
    elif eval_type == "season":
        return dict(
            freqs=["hourly","daily", "monthly"],
            ts_type="hourly",
            main_freq="hourly",
            forecast_evaluation=True,
        )
    elif eval_type == "week":
        return dict(
            freqs=["hourly", "daily"],
            ts_type="hourly",
            main_freq="hourly",
            forecast_evaluation=False,
        )
    elif eval_type == "day":
        return dict(
            freqs=["hourly"],
            ts_type="hourly",
            main_freq="hourly",
            forecast_evaluation=False,
        )
    else:
        return {}


def get_seasons_in_period(start_date: datetime, end_date: datetime) -> List[str]:
    seasons = ["DJF", "DJF", "MAM", "MAM", "MAM", "JJA", "JJA", "JJA", "SON", "SON", "SON", "DJF"]
    get_season = lambda date: seasons[date.month - 1]
    daterange = pd.date_range(start_date, end_date, freq="d")

    periods = []
    prev_date = daterange[0]
    start_period = daterange[0]
    prev_season = get_season(prev_date)
    for date in daterange[1:]:
        if get_season(date) == prev_season:
            prev_date = date
        else:
            periods.append(
                f"{pd.to_datetime(str(start_period)).strftime('%Y%m%d')}-{pd.to_datetime(str(prev_date)).strftime('%Y%m%d')}"
            )
            prev_date = date
            prev_season = get_season(date)
            start_period = date

    else:

        if start_period == daterange[-1]:
            periods.append(f"{pd.to_datetime(str(start_period)).strftime('%Y%m%d')}")
        else:
            periods.append(
                f"{pd.to_datetime(str(start_period)).strftime('%Y%m%d')}-{pd.to_datetime(str(daterange[-1])).strftime('%Y%m%d')}"
            )

    return periods


def get_years_starting_in_november(start_date: datetime, end_date: datetime) -> List[str]:
    periods = []

    start_yr = start_date.year
    end_yr = end_date.year

    found_last_yr = False

    prev_date = start_date
    new_yr = datetime(start_yr, 12, 1, 00, 00, 00)

    if new_yr > start_date:
        periods.append(
            f"{start_date.strftime('%Y%m%d')}-{(new_yr-timedelta(days=1)).strftime('%Y%m%d')}"
        )
        prev_date = new_yr
        new_yr += relativedelta(years=1)
    else:
        if end_date < new_yr + relativedelta(years=1):
            return []
        periods.append(
            f"{start_date.strftime('%Y%m%d')}-{(new_yr+relativedelta(years=1)-timedelta(days=1)).strftime('%Y%m%d')}"
        )

        prev_date = new_yr + relativedelta(years=1)
        new_yr += relativedelta(years=2)

    for i in range(end_yr - start_yr):
        if new_yr < end_date:
            periods.append(
                f"{prev_date.strftime('%Y%m%d')}-{(new_yr-timedelta(days=1)).strftime('%Y%m%d')}"
            )
            prev_date = new_yr
            new_yr += relativedelta(years=1)
        else:
            periods.append(f"{prev_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}")
            break

    return periods


def make_period(
    start_date: datetime,
    end_date: datetime,
) -> List[str]:
    start_yr = start_date.year
    end_yr = end_date.year
    start_dt = start_date.strftime("%Y%m%d")  # .year
    end_dt = end_date.strftime("%Y%m%d")  # .year

    season_periods = get_seasons_in_period(start_date, end_date)

    nov_periods = get_years_starting_in_november(start_date, end_date)

    if start_dt == end_dt:
        return [f"{start_dt}"]

    periods = [f"{start_dt}-{end_dt}"]

    if periods != season_periods:
        periods += nov_periods  # season_periods

    # if end_yr == start_yr:
    #     return periods

    # periods.append(f"{start_dt}-{start_yr}1231")  # append first year portion

    # if (end_yr - start_yr) >= 2:  # append full years in between if any
    #     for y in range(start_yr + 1, end_yr):
    #         periods.append(f"{y}0101-{y}1231")

    # periods.append(f"{end_yr}0101-{end_dt}")  # append last year portion
    return periods


def make_period_ys(
    start_date: datetime,
    end_date: datetime,
) -> List[str]:
    start_yr = start_date.year
    end_yr = end_date.year
    periods = [f"{start_yr}-{end_yr}"]
    periods += [str(yr) for yr in range(start_yr, end_yr + 1)]
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
    models: List[ModelName],
    id: str | None,
    name: str | None,
    description: str | None,
    eval_type: Eval_Type | None,
    analysis: bool,
    onlymap: bool,
    addmap: bool, 
) -> dict:

    logger.info("Making the configuration")

    if not models:
        models = list(ModelName)

    if analysis:
        runtype = "AN"
    else:
        runtype = "FC"

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
                runtype=runtype,
            )
            for model in models
        },
        periods=periods,
        json_basedir=str(data_path),
        coldata_basedir=str(coldata_path),
    )
    check_dates_from_eval(eval_type, start_date, end_date)
    cfg.update(update_freqs_from_eval_type(eval_type))
    if eval_type == "season" or eval_type == "long":
        extra_obs_days = 4
    else:
        extra_obs_days = 0
    cfg["obs_cfg"]["EEA"]["read_opts_ungridded"]["files"] = [
        str(p)
        for p in obs_paths(
            *date_range(start_date, end_date + timedelta(days=extra_obs_days)),
            root_path=obs_path,
            analysis=analysis,
        )
    ]  # type:ignore[index]

    if analysis:
        cfg["forecast_days"] = 1

    if id is not None:
        cfg["exp_id"] = id
    if name is not None:
        cfg["exp_name"] = name
    if description is not None:
        cfg["exp_descr"] = description
    if addmap:
        cfg["add_model_maps"]=True
    if onlymap:
        cfg["add_model_maps"]=True
        cfg["only_model_maps"]=True

    return cfg


#def read_observations(data: list) -> None:
def read_observations(specie: str, *, files: List, cache: str | Path | None) -> None:
    #logger.info(f"Running {data[0]}")
    #cache = data[2]
    #if cache is not None:
    #    const.CACHEDIR = str(cache)

    #reader = ReadUngridded()

    #reader.read(
    #    data_ids="CAMS2_83.NRT",
    #    vars_to_retrieve=data[0],
    #    files=data[1],
    #    force_caching=True,
    #)

    #logger.info(f"Finished {data[0]}")
    logger.info(f"Running {specie}")
    if cache is not None:
        const.CACHEDIR = str(cache)

    reader = ReadUngridded()

    reader.read(
        data_ids="CAMS2_83.NRT",
        vars_to_retrieve=specie,
        files=files,
        force_caching=True,
    )

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

    import time

    start = time.time()

    logging.info(f"Clearing cache at {const.CACHEDIR}")
    clear_cache()

    if pool > 1:
        logger.info(f"Running observation reading with pool {pool}")
        files = cfg["obs_cfg"]["EEA"]["read_opts_ungridded"]["files"]
        #pool_data = [[s, files, cache] for s in species_list]
        with ProcessPoolExecutor(max_workers=pool) as executor:
            futures = [
                executor.submit(read_observations,specie,files=files,cache=cache)
                for specie in species_list
            ]
            #executor.map(read_observations, pool_data)
        for future in as_completed(futures):
            future.result()


    logger.info(f"Running Rest of Statistics")
    ExperimentProcessor(stp).run()
    print("Done Running Rest of Statistics")
    if eval_type in {"season", "long"}:
        logger.info(f"Running CAMS2_83 Spesific Statistics")
        if pool > 1:
            logger.info(f"Making forecast plot with pool {pool}")
            with ProcessPoolExecutor(max_workers=pool) as executor:
                futures = [
                    executor.submit(run_forecast, specie, stp=stp, analysis=analysis)
                    for specie in species_list
                ]
            for future in as_completed(futures):
                future.result()
        else:
            CAMS2_83_Processer(stp).run(analysis=analysis)
    print(f"Long run: {time.time() - start} sec")


@app.command()
def main(
    start_date: datetime = typer.Argument(
        f"{datetime.today():%F}",
        formats=["%Y-%m-%d", "%Y%m%d"],
        help="Start date for the evaluation",
    ),
    end_date: datetime = typer.Argument(
        f"{datetime.today():%F}",
        formats=["%Y-%m-%d", "%Y%m%d"],
        help="End date for the evaluation",
    ),
    leap: int = typer.Argument(
        0,
        min=0,
        max=3,
        help="Which forecast day to use",
    ),
    model_path: Path = typer.Option(
        DEFAULT_MODEL_PATH,
        exists=True,
        readable=True,
        help="Path where the model data is found",
    ),
    obs_path: Path = typer.Option(
        DEFAULT_OBS_PATH,
        exists=True,
        readable=True,
        help="Path where the obs data is found",
    ),
    data_path: Path = typer.Option(
        Path("../../data").resolve(),
        exists=True,
        readable=True,
        writable=True,
        help="Path where the results are stored",
    ),
    coldata_path: Path = typer.Option(
        Path("../../coldata").resolve(),
        exists=True,
        readable=True,
        writable=True,
        help="Path where the coldata are stored",
    ),
    model: List[ModelName] = typer.Option(
        [],
        "--model",
        "-m",
        case_sensitive=False,
        help="Which model to use. All is used if none is given",
    ),
    id: Optional[str] = typer.Option(
        None,
        help="Experiment name. If none are given, the id from the default config is used",
    ),
    name: Optional[str] = typer.Option(
        None,
        help="Experiment name. If none are given, the name from the default config is used",
    ),
    description: Optional[str] = typer.Option(
        None,
        help="Experiment description. If none given, the description from the default config is used",
    ),
    analysis: bool = typer.Option(
        False,
        help="Sets the flag which tells the code to use the analysis model data. If false, the forecast model data is used",
    ),
    addmap: bool = typer.Option(
        False,
        help="Sets the flag which tells the code to set add_model_maps=True. Option is set to False otherwise",
    ),
    onlymap: bool = typer.Option(
         False,
         help="Sets the flag which tells the code to set add_model_maps=True and only_model_maps=True. Option is set to False otherwise",
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

    if pool > cpu_count():
        logger.warning(
            f"The given pool {pool} is larger than the maximum CPU count {cpu_count()}. Using that instead"
        )
        pool = cpu_count()

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
        onlymap,
        addmap,
    )

    quiet = not verbose
    runner(cfg, cache, eval_type, analysis=analysis, dry_run=dry_run, quiet=quiet, pool=pool)
