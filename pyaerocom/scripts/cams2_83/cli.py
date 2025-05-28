from __future__ import annotations

import logging
import multiprocessing as mp
from copy import deepcopy
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

import typer

from pyaerocom import change_verbosity, const
from pyaerocom.io.cams2_83.models import ModelName, RunType
from pyaerocom.io.cams2_83.read_obs import DATA_FOLDER_PATH as DEFAULT_OBS_PATH
from pyaerocom.io.cams2_83.read_obs import obs_paths
from pyaerocom.io.cams2_83.reader import DATA_FOLDER_PATH as DEFAULT_MODEL_PATH
from pyaerocom.scripts.cams2_83.config import CFG
from pyaerocom.scripts.cams2_83.evaluation import EvalType, date_range, runner, runnermedianscores

app = typer.Typer(add_completion=False, no_args_is_help=True)
logger = logging.getLogger(__name__)


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
    add_seasons: bool,
    fairmode: bool,
    medianscores: bool,
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
    if run_type != RunType.AN and medianscores:
        obs_dates = date_range(start_date - timedelta(days=1), end_date + timedelta(days=extra_obs_days))
    else:
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

    if add_seasons:
        cfg.update(add_seasons=True)    

    if fairmode:
        if eval_type in ["season", "long"]:
            cfg.update(use_cams2_83_fairmode=True)
        else:
            cfg.update(use_fairmode=True)

    return cfg


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
    model: list[ModelName] = typer.Option(
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
    add_seasons: bool = typer.Option(False, "--addseasons", help="set add_seasons"),
    fairmode: bool = typer.Option(False, "--fairmode", help="set use_fairmode"),
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
        1,
        "--pool",
        "-p",
        min=1,
        help="CPUs for reading OBS and running median scores",
    ),
):
    if dry_run:
        change_verbosity(logging.INFO)

    if pool > mp.cpu_count():
        logger.warning(
            f"The given pool {pool} is larger than the maximum CPU count {mp.cpu_count()}."
        )

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
        add_seasons,
        fairmode,
        medianscores
    )
    
    # we do not want the cache produced in previous runs to be silently cleared
    const.RM_CACHE_OUTDATED = False

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
            runnermedianscores(cfg, cache, analysis=analysis, dry_run=dry_run, pool=pool)
    else:
        logger.info("Standard run")
        runner(cfg, cache, dry_run=dry_run, pool=pool)


if __name__ == "__main__":
    main()
