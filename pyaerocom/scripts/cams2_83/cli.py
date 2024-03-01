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
from pyaerocom.io.cams2_83.models import ModelName
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
    analysis: bool,
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
                runtype="AN" if analysis else "FC",
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
        str(p) for p in obs_paths(*obs_dates, root_path=obs_path, analysis=analysis)
    ]

    if analysis:
        cfg.update(forecast_days=1)

    cfg.update(exp_id=id, exp_name=name, exp_descr=description)

    if add_map:
        cfg.update(add_model_maps=True)

    if only_map:
        cfg.update(add_model_maps=True, only_model_maps=True)

    return cfg


def read_observations(specie: str, *, files: list[str], cache: str | Path) -> None:
    logger.info(f"Running {specie}")
    const.CACHEDIR = str(cache)

    reader = ReadUngridded()
    reader.read(data_ids="CAMS2_83.NRT", vars_to_retrieve=specie, files=files, force_caching=True)
    logger.info(f"Finished {specie}")


def standard_runner(config: Path, *, pool: int = 1):
    logger.info(f"Standard Evaluation\n{config}")
    cfg = json.loads(config.read_text())
    stp = EvalSetup(**cfg)

    logging.info(f"Clearing cache at {const.CACHEDIR}")
    clear_cache()

    if pool > 1:
        logger.info(f"Running observation reading with pool {pool}")
        files = cfg["obs_cfg"]["EEA"]["read_opts_ungridded"]["files"]
        with ProcessPoolExecutor(max_workers=pool) as executor:
            futures = [
                executor.submit(read_observations, specie, files=files, cache=const.CACHEDIR)
                for specie in species_list
            ]
        for future in as_completed(futures):
            future.result()

    logger.info("Running Statistics")
    ExperimentProcessor(stp).run()


def runner_median_scores(config: Path, specie: str, *, analysis: bool = False):
    logger.info("CAMS2_83 Specific Statistics\n{config}")
    logger.warning(
        "cache is not cleared, "
        "collocated data is assumed in place, "
        "regular statistics are assumed to have been run"
    )
    cfg = json.loads(config.read_text())
    stp = EvalSetup(**cfg)

    logger.info(f"Median scores plot for {specie=} and {analysis=}")
    CAMS2_83_Processer(stp).run(analysis=analysis, var_list=specie)


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
    config: Path = typer.Argument(..., writable=True, help="experiment configuration"),
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
        help="where collocated data are stored",
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
        help="analysis or forecast model and observations",
    ),
    add_map: bool = typer.Option(False, "--addmap", help="set add_model_maps"),
    only_map: bool = typer.Option(
        False, "--onlymap", help="set add_model_maps and only_model_maps"
    ),
    eval_type: EvalType = typer.Option(..., "--eval-type", "-e"),
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
        model,
        id,
        name,
        description,
        eval_type,
        analysis,
        only_map,
        add_map,
    )
    config.write_text(json.dumps(cfg, indent=2))


@app.command(no_args_is_help=True)
def evaluation(
    config: Path = typer.Argument(
        ..., exists=True, readable=True, help="experiment configuration"
    ),
    pool: int = typer.Option(
        1,
        "--pool",
        "-p",
        min=1,
        max=cpu_count(),
        help="Number of CPUs to be used for reading OBS and creating forecast plots",
    ),
):
    """run standard evaluation as described on experiment configuration"""
    standard_runner(config, pool=pool)


class Species(str, Enum):
    _ignore_ = "species Species"

    Species = vars()
    for species in species_list:
        Species[species] = species

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_task_id(cls, task_id: str | None = os.getenv("SGE_TASK_ID")) -> Self | None:
        if task_id is None or not task_id.isnumeric():
            return None

        try:
            return cls[species_list[int(task_id)]]
        except IndexError as e:
            raise ValueError(f"{task_id=} out of range") from e


@app.command(no_args_is_help=True)
def median_scores(
    config: Path = typer.Argument(
        ..., exists=True, readable=True, help="experiment configuration"
    ),
    species: Species = typer.Argument(Species.from_task_id()),
    analysis: bool = typer.Option(
        False,
        "--analysis/--forecast",
        help="analysis or forecast model and observations",
    ),
):
    """special evaluation for experiment as described on experiment configuration"""
    runner_median_scores(config, species, analysis=analysis)
