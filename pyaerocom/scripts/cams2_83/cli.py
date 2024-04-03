from __future__ import annotations

import logging
import multiprocessing as mp
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from datetime import date, datetime, timedelta
from multiprocessing import cpu_count
from pathlib import Path
from pprint import pformat
from typing import List, Optional

import typer

from pyaerocom import change_verbosity, const
from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
from pyaerocom.io import ReadUngridded
from pyaerocom.io.cachehandler_ungridded import list_cache_files
from pyaerocom.io.cams2_83.models import ModelName, RunType
from pyaerocom.io.cams2_83.read_obs import DATA_FOLDER_PATH as DEFAULT_OBS_PATH
from pyaerocom.io.cams2_83.read_obs import obs_paths
from pyaerocom.io.cams2_83.reader import DATA_FOLDER_PATH as DEFAULT_MODEL_PATH
from pyaerocom.scripts.cams2_83.config import CFG, species_list  # , obs_filters
from pyaerocom.scripts.cams2_83.evaluation import EvalType, date_range
from pyaerocom.scripts.cams2_83.processer import CAMS2_83_Processer

"""
TODO:
    - Add option for species
    - Add option for periodes [Done]
    - Add option for running only som observations/models/species
    - Add options with defaults for the different folders (data/coldata/cache)
"""


app = typer.Typer(add_completion=False, no_args_is_help=True)
logger = logging.getLogger(__name__)


def clear_cache():
    """Delete cached data objects"""
    for path in list_cache_files():
        path.unlink()


def make_model_entry(
    start_date: datetime,
    end_date: datetime,
    leap: int,
    model_path: Path,
    model: ModelName,
    run_type: RunType,
) -> dict:
    return dict(
        model_id=f"CAMS2-83.{model.name}.day{leap}.{run_type.name}",
        model_data_dir=str(model_path.resolve()),
        gridded_reader_id={"model": "ReadCAMS2_83"},
        model_kwargs=dict(
            daterange=[f"{start_date:%F}", f"{end_date:%F}"],
        ),
    )


def make_config(
    start_date: date,
    end_date: date,
    leap: int,
    model_path: Path,
    obs_path: Path,
    data_path: Path,
    coldata_path: Path,
    models: list[ModelName],
    id: str,
    name: str,
    description: str,
    eval_type: EvalType,
    run_type: RunType,
    only_map: bool,
    add_map: bool,
) -> dict:
    logger.info("Making the configuration")

    if not models:
        models = list(ModelName)

    cfg = deepcopy(CFG)
    cfg.update(
        model_cfg={
            f"{model.name}": make_model_entry(
                start_date,
                end_date,
                leap,
                model_path,
                model,
                run_type=run_type,
            )
            for model in models
        },
        periods=eval_type.periods(start_date, end_date),
        json_basedir=str(data_path),
        coldata_basedir=str(coldata_path),
    )

    if eval_type is not None:
        eval_type.check_dates(start_date, end_date)
        cfg.update(eval_type.freqs_config())

    extra_obs_days = 4 if eval_type in {"season", "long"} else 0
    obs_dates = date_range(start_date, end_date + timedelta(days=extra_obs_days))
    cfg["obs_cfg"]["EEA"]["read_opts_ungridded"]["files"] = [  # type:ignore[index]
        str(p) for p in obs_paths(*obs_dates, root_path=obs_path, analysis=run_type == RunType.AN)
    ]

    if run_type == RunType.AN:
        cfg.update(forecast_days=1)

    cfg.update(exp_id=id, exp_name=name, exp_descr=description)

    if add_map:
        cfg.update(add_model_maps=True)

    if only_map:
        cfg.update(add_model_maps=True, only_model_maps=True)

    return cfg


def read_observations(specie: str, *, files: List, cache: str | Path | None) -> None:
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

    logger.info(f"Clearing cache at {const.CACHEDIR}")
    clear_cache()

    if pool > 1:
        logger.info(f"Running observation reading with pool {pool}")
        files = cfg["obs_cfg"]["EEA"]["read_opts_ungridded"]["files"]
        # pool_data = [[s, files, cache] for s in species_list]
        with ProcessPoolExecutor(max_workers=pool) as executor:
            futures = [
                executor.submit(read_observations, specie, files=files, cache=cache)
                for specie in species_list
            ]
            # executor.map(read_observations, pool_data)
        for future in as_completed(futures):
            future.result()

    logger.info("Running Statistics")
    ExperimentProcessor(stp).run()
    print("Done Running Statistics")


def runnermedianscores(
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
        "Running CAMS2_83 Specific Statistics, cache is not cleared, colocated data is assumed in place, regular statistics are assumed to have been run"
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
    run_type: RunType = typer.Argument(...),
    eval_type: EvalType = typer.Argument(...),
    start_date: datetime = typer.Argument(
        ..., formats=["%Y-%m-%d", "%Y%m%d"], help="evaluation start date"
    ),
    end_date: datetime = typer.Argument(
        ..., formats=["%Y-%m-%d", "%Y%m%d"], help="evaluation end date"
    ),
    leap: int = typer.Argument(0, min=RunType.AN.days, max=RunType.FC.days, help="forecast day"),
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
        writable=True,
        help="where results are stored",
    ),
    coldata_path: Path = typer.Option(
        Path("../../coldata").resolve(),
        exists=True,
        readable=True,
        writable=True,
        help="where collocated data are stored",
    ),
    model: List[ModelName] = typer.Option(
        [],
        "--model",
        "-m",
        case_sensitive=False,
        help="Which model to use. All is used if none is given",
    ),
    id: str = typer.Option(CFG["exp_id"], help="experiment ID"),
    name: str = typer.Option(CFG["exp_name"], help="experiment name"),
    description: str = typer.Option(CFG["exp_descr"], help="experiment description"),
    add_map: bool = typer.Option(False, "--addmap", help="set add_model_maps"),
    only_map: bool = typer.Option(
        False, "--onlymap", help="set add_model_maps and only_model_maps"
    ),
    medianscores: bool = typer.Option(
        False,
        "--medianscores",
        help="If true just the cams2_83-specific statistics are computed, a.k.a. the median scores plots or 'weird' plots, the cache is not cleared and it's assumed that the colocated data is already in place and the regular statistics have already been run",
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
    pool: int = typer.Option(
        1, "--pool", "-p", min=1, max=cpu_count(), help="CPUs for reading OBS"
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
        run_type,
        only_map,
        add_map,
    )

    quiet = not verbose

    analysis = False
    if run_type == RunType.AN:
        analysis = True

    if medianscores:
        if eval_type not in {"season", "long"}:
            logger.error(
                "Median scores calculations are only consistent with a season/long kind of evaluation"
            )
            raise Exception(
                "Median scores calculations are only consistent with a season/long kind of evaluation"
            )
        else:
            logger.info("Special run for median scores only")
            runnermedianscores(
                cfg, cache, analysis=analysis, dry_run=dry_run, quiet=quiet, pool=pool
            )
    else:
        logger.info("Standard run")
        runner(cfg, cache, dry_run=dry_run, quiet=quiet, pool=pool)
