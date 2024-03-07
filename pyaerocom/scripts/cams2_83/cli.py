from __future__ import annotations

import json
import logging
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from datetime import date, datetime, timedelta
from enum import Enum
from multiprocessing import cpu_count
from pathlib import Path

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

import typer

from pyaerocom import change_verbosity, const
from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
from pyaerocom.io import ReadUngridded
from pyaerocom.io.cams2_83.models import ModelName, RunType
from pyaerocom.io.cams2_83.read_obs import DATA_FOLDER_PATH as DEFAULT_OBS_PATH
from pyaerocom.io.cams2_83.read_obs import obs_paths
from pyaerocom.io.cams2_83.reader import DATA_FOLDER_PATH as DEFAULT_MODEL_PATH
from pyaerocom.tools import clear_cache

from .config import CFG, species_list
from .evaluation import EvalType, date_range
from .processer import CAMS2_83_Processer

"""
TODO:
    - Add option for species
    - Add option for periods [Done]
    - Add option for running only som observations/models/species
    - Add options with defaults for the different folders (data/coldata/cache)
"""


app = typer.Typer(add_completion=False, no_args_is_help=True)
logger = logging.getLogger(__name__)


def make_model_entry(
    start_date: date,
    end_date: date,
    leap: int,
    model_path: Path,
    model: ModelName,
    run_type: RunType,
) -> dict:
    return dict(
        model_id=f"CAMS2-83.{model.name}.day{leap}.{run_type}",
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


@app.callback()
def callback(
    cache: Path = typer.Option(const.CACHEDIR, help="cache path"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """evaluate CAMS2_83 models against surface observations"""
    change_verbosity(logging.INFO if verbose else logging.ERROR)
    const.QUIET = not verbose
    const.CACHEDIR = str(cache)


@app.command(no_args_is_help=True)
def conf(
    run_type: RunType = typer.Argument(...),
    eval_type: EvalType = typer.Argument(...),
    config: Path = typer.Argument(..., writable=True, help="experiment configuration"),
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
    id: str = typer.Option(CFG["exp_id"], help="experiment ID"),
    name: str = typer.Option(CFG["exp_name"], help="experiment name"),
    description: str = typer.Option(CFG["exp_descr"], help="experiment description"),
    add_map: bool = typer.Option(False, "--addmap", help="set add_model_maps"),
    only_map: bool = typer.Option(
        False, "--onlymap", help="set add_model_maps and only_model_maps"
    ),
):
    """write experiment configuration as JSON"""
    cfg = make_config(
        start_date.date(),
        end_date.date(),
        leap,
        model_path,
        obs_path,
        data_path,
        coldata_path,
        list(ModelName),
        id,
        name,
        description,
        eval_type,
        run_type,
        only_map,
        add_map,
    )
    config.write_text(json.dumps(cfg, indent=2))


@app.command(no_args_is_help=True)
def pre_cache_obs(
    config: Path = typer.Argument(
        ..., exists=True, readable=True, help="experiment configuration"
    ),
    pool: int = typer.Option(
        1, "--pool", "-p", min=1, max=cpu_count(), help="CPUs for reading OBS"
    ),
):
    """read observations to update cache"""
    logging.info(f"clearing cache at {const.CACHEDIR}")
    clear_cache()

    logger.info(f"reading observations on {pool} processes")
    cfg = json.loads(config.read_text())
    files = cfg["obs_cfg"]["EEA"]["read_opts_ungridded"]["files"]
    with ProcessPoolExecutor(max_workers=pool) as executor:
        futures = {
            executor.submit(read_observations, specie, files, const.CACHEDIR): specie
            for specie in species_list
        }

        # re-raise exception as soon as the task fails
        for future in as_completed(futures):
            specie = futures[future]
            try:
                future.result()
            except Exception as e:
                logger.error(f"{specie} raised {e}")
                raise


def read_observations(specie: str, files: list[str], cache: str | Path) -> None:
    const.CACHEDIR = str(cache)
    reader = ReadUngridded()
    reader.read(data_ids="CAMS2_83.NRT", vars_to_retrieve=specie, files=files, force_caching=True)


def model_task_id(task_id: str | None = os.getenv("SGE_TASK_ID")) -> ModelName | None:
    if task_id is None or not task_id.isnumeric():
        return None

    return tuple(ModelName)[int(task_id) % len(ModelName)]


@app.command(no_args_is_help=True)
def evaluation(
    config: Path = typer.Argument(
        ..., exists=True, readable=True, help="experiment configuration"
    ),
    model: ModelName = typer.Argument(
        model_task_id(), case_sensitive=False, help="model to evaluate"
    ),
):
    """run standard evaluation as described on experiment configuration"""
    logger.info(f"Standard Evaluation\n{config}")
    cfg = json.loads(config.read_text())
    stp = EvalSetup(**cfg)
    ExperimentProcessor(stp).run(model_name=model.name)


class Species(str, Enum):
    _ignore_ = "spc Species"

    Species = vars()
    for spc in species_list:
        Species[spc] = spc

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_task_id(cls, task_id: str | None = os.getenv("SGE_TASK_ID")) -> Self | None:
        if task_id is None or not task_id.isnumeric():
            return None

        return tuple(cls)[int(task_id) % len(cls)]


@app.command(no_args_is_help=True)
def median_scores(
    config: Path = typer.Argument(
        ..., exists=True, readable=True, help="experiment configuration"
    ),
    spc: Species = typer.Argument(Species.from_task_id()),
    analysis: bool = typer.Option(
        False,
        "--analysis/--forecast",
        help="analysis or forecast model and observations",
    ),
):
    """special evaluation for experiment as described on experiment configuration"""
    logger.info("CAMS2_83 Specific Statistics\n{config}")
    logger.warning(
        "cache is not cleared, "
        "collocated data is assumed in place, "
        "regular statistics are assumed to have been run"
    )
    cfg = json.loads(config.read_text())
    stp = EvalSetup(**cfg)

    logger.info(f"Median scores plot for {spc=} and {analysis=}")
    CAMS2_83_Processer(stp).run(analysis=analysis, var_list=spc)
