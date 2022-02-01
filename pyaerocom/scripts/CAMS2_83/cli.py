from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import typer

from pyaerocom import change_verbosity
from pyaerocom.aeroval import EvalSetup
from pyaerocom.io.cams2_83.models import ModelName
from pyaerocom.io.cams2_83.reader import DATA_FOLDER_PATH

from .config import CFG
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


def make_period(
    start_date: datetime,
    end_date: datetime,
) -> str:
    start_yr = start_date.year
    end_yr = end_date.year

    if start_yr == end_yr:
        return f"{start_yr}"
    else:
        return f"{start_yr}-{end_yr}"


def make_model_entry(
    start_date: datetime,
    end_date: datetime,
    leap: int,
    path: Path,
    model: ModelName,
) -> dict:

    return dict(
        model_id=f"CAMS2-83.{model.upper()}.day{leap}",
        model_data_dir=str(path.absolute()),
        gridded_reader_id={"model": "ReadCAMS2_83"},
        model_kwargs=dict(
            daterange=(f"{start_date:%Y%m%d}", f"{end_date:%Y%m%d}"),
        ),
    )


def make_config(
    start_date: datetime,
    end_date: datetime,
    leap: int,
    path: Path,
    data_path: Path,
    coldata_path: Path,
    models: list[ModelName],
    id: str | None,
    name: str | None,
) -> dict:

    logger.info("Making the configuration")

    cfg = CFG

    if not models:
        models = list(ModelName)

    cfg["model_cfg"] = {
        f"CAMS2-83-{model}": make_model_entry(start_date, end_date, leap, path, model)
        for model in models
    }

    cfg["periods"] = [make_period(start_date, end_date)]

    cfg["json_basedir"] = str(data_path.absolute())
    cfg["coldata_basedir"] = str(coldata_path.absolute())

    if id is not None:
        cfg["exp_id"] = id
    if name is not None:
        cfg["exp_name"] = name

    return CFG


def runner(cfg):
    logger.info(f"Running the evaluation for the config\n{cfg}")

    stp = EvalSetup(**CFG)
    ana = CAMS2_83_Processer(stp)
    ana.run()


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
    path: Path = typer.Option(
        DATA_FOLDER_PATH,
        exists=True,
        readable=True,
        help="Path where the model data is found",
    ),
    data_path: Path = typer.Option(
        Path("../../data"),
        exists=True,
        readable=True,
        writable=True,
        help="Path where the results are stored",
    ),
    coldata_path: Path = typer.Option(
        Path("../../coldata"),
        exists=True,
        readable=True,
        writable=True,
        help="Path where the coldata are stored",
    ),
    model: List[ModelName] = typer.Option(
        [],
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
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-n",
        help="Will only make and print the config without running the evaluation",
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):

    if verbose:
        change_verbosity(logging.INFO)

    cfg = make_config(
        start_date,
        end_date,
        leap,
        path,
        data_path,
        coldata_path,
        model,
        id,
        name,
    )

    if not dry_run:
        runner(cfg)
    else:
        typer.echo(cfg)
