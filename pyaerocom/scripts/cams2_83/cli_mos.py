from __future__ import annotations

import logging
import multiprocessing as mp
from copy import deepcopy
from datetime import date, datetime
from pathlib import Path
from typing import Optional

import typer

from pyaerocom import const
from pyaerocom.scripts.cams2_83.config import CFG
from pyaerocom.scripts.cams2_83.evaluation import (
    EvalType,
    runnermedianscores,
    runnermos,
)

app = typer.Typer(add_completion=False, no_args_is_help=True)
logger = logging.getLogger(__name__)


def make_config_mos(
    start_date: date,
    end_date: date,
    data_path: Path,
    coldata_path: Path,
    eval_type: EvalType,
    id: str,
    name: str,
    description: str,
    add_seasons: bool,
) -> dict:
    logger.info("Making the configuration")

    models = ["ENS", "MOS"]

    cfg = deepcopy(CFG)
    cfg.update(
        model_cfg={
            f"{model}": dict(
                model_id=f"CAMS2-83.{model}.day0.FC",
                model_kwargs=dict(
                    daterange=[f"{start_date}", f"{end_date}"],
                ),
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

    cfg.update(only_json=True)

    cfg.update(exp_id=id, exp_name=name, exp_descr=description)

    cfg.update(use_cams2_83_fairmode=True)

    if add_seasons:
        cfg.update(add_seasons=True)

    return cfg


@app.command()
def main(
    eval_type: EvalType = typer.Argument(...),
    start_date: datetime = typer.Argument(
        ..., formats=["%Y-%m-%d", "%Y%m%d"], help="evaluation start date"
    ),
    end_date: datetime = typer.Argument(
        ..., formats=["%Y-%m-%d", "%Y%m%d"], help="evaluation end date"
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
        help="where colocated data are stored, this is useless here but this path needs to exist",
    ),
    cache: Optional[Path] = typer.Option(
        None,
        help="Optional path to cache. If nothing is given, the default pyaerocom cache is used",
    ),
    id: str = typer.Option(CFG["exp_id"], help="experiment ID"),
    name: str = typer.Option(CFG["exp_name"], help="experiment name"),
    description: str = typer.Option(CFG["exp_descr"], help="experiment description"),
    add_seasons: bool = typer.Option(False, "--addseasons", help="set add_seasons"),
    pool: int = typer.Option(
        1,
        "--pool",
        "-p",
        min=1,
        help="CPUs for running the median scores",
    ),
):
    if pool > mp.cpu_count():
        logger.warning(
            f"The given pool {pool} is larger than the maximum CPU count {mp.cpu_count()}. Using that instead"
        )
        pool = 1

    cfg = make_config_mos(
        start_date,
        end_date,
        data_path,
        coldata_path,
        eval_type,
        id,
        name,
        description,
        add_seasons,
    )

    # we do not want the cache produced in previous runs to be silently cleared
    const.RM_CACHE_OUTDATED = False

    logger.info("Standard run")
    runnermos(cfg, cache, dry_run=False)
    logger.info("Special run for median scores only")
    runnermedianscores(cfg, cache, dry_run=False, analysis=False, pool=pool)


if __name__ == "__main__":
    main()
