from __future__ import annotations

import logging
import multiprocessing as mp
from copy import deepcopy
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

import typer

from pyaerocom import change_verbosity, const
from pyaerocom.scripts.cams2_82.config import CFG
from pyaerocom.io.cams2_82.reader import DATA_FOLDER_PATH
from pyaerocom.scripts.cams2_82.evaluation import (
    date_range,
    runner,
)
from pyaerocom.scripts.cams2_82.config import obs_filters, species_list, EEA_FILTER

from pyaerocom.io import PyaroConfig

app = typer.Typer(add_completion=False, no_args_is_help=True)
logger = logging.getLogger(__name__)


DEFAULT_EEA_PATH = Path("/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/EEA-AQDS/download")
DEFAULT_MODEL_PATH = DATA_FOLDER_PATH

def make_model_entry(
    start_date: datetime,
    end_date: datetime,
    model_path: Path,

) -> dict:
    return dict(
        model_id = "IFS",
        model_data_dir=str(model_path.resolve()),
        gridded_reader_id={"model": "ReadCAMS2_82"},
        model_kwargs=dict(
            daterange=[f"{start_date:%F}", f"{end_date:%F}"],
        ),
    )

def make_EEA_entry(
    start_date: datetime,
    end_date: datetime,
    obs_path: Path,
) -> dict:
    filters={
                "time_bounds": {
                "startend_include": [[start_date.strftime("%Y-%m-%d %H:%M:%S"), end_date.strftime("%Y-%m-%d %H:%M:%S")]]
            },

        }
    data_id = "eeareader"
    config_eea = PyaroConfig(
        name="eea",
        reader_id=data_id,
        filename_or_obj_or_url=obs_path,
        filters=filters,
        dataset= "unverified",
        name_map={
            "PM2.5": "concpm25",
            "PM10": "concpm10",
            
        },
    )

    return  dict(
        obs_id=config_eea.name,
        pyaro_config=config_eea,
        web_interface_name="EEA",
        obs_vars=species_list,
        obs_vert_type="Surface",
        ts_type="hourly",
        obs_filters=EEA_FILTER,   
    )


def make_period(start_date: date, end_date: date) -> list[str]:
    if start_date == end_date:
        return [f"{start_date:%Y%m%d}"]
    periods = [f"{start_date:%Y%m%d}-{end_date:%Y%m%d}"]

    return periods


def make_config(
    start_date: date,
    end_date: date,
    model_path: Path,
    obs_path: Path,
    data_path: Path,
    coldata_path: Path,
    
    id: str,
    name: str,
    description: str,
    only_map: bool,
    add_map: bool,
    add_seasons: bool,
) -> dict:
    logger.info("Making the configuration")

    

    cfg = deepcopy(CFG)
    cfg.update(
        periods=make_period(start_date, end_date),
        json_basedir=str(data_path),
        coldata_basedir=str(coldata_path),
    )




    obs_dates = date_range(start_date, end_date)
    cfg["obs_cfg"]["EEA"] = make_EEA_entry(start_date, end_date, obs_path)
    cfg["model_cfg"]["IFS"] = make_model_entry(start_date, end_date, model_path)

    
    cfg.update(exp_id=id, exp_name=name, exp_descr=description)

    if add_map:
        cfg.update(add_model_maps=True)

    if only_map:
        cfg.update(add_model_maps=True, only_model_maps=True)

    if add_seasons:
        cfg.update(add_seasons=True)

    return cfg


@app.command()
def main(
    
    start_date: datetime = typer.Argument(
        ..., formats=["%Y-%m-%d", "%Y%m%d"], help="evaluation start date"
    ),
    end_date: datetime = typer.Argument(
        ..., formats=["%Y-%m-%d", "%Y%m%d"], help="evaluation end date"
    ),
    
    model_path: Path = typer.Option(
        DEFAULT_MODEL_PATH, exists=True, readable=True, help="path to model data"
    ),
    eea_obs_path: Path = typer.Option(
        DEFAULT_EEA_PATH, exists=True, readable=True, help="path to observation data"
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
    add_seasons: bool = typer.Option(False, "--addseasons", help="set add_seasons"),
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
        
        model_path,
        eea_obs_path,
        data_path,
        coldata_path,
        
        id,
        name,
        description,
        
        only_map,
        add_map,
        add_seasons,
        
    )

    # we do not want the cache produced in previous runs to be silently cleared
    const.RM_CACHE_OUTDATED = False

   
    logger.info("Standard run")
    runner(cfg, cache, dry_run=dry_run, pool=pool)


if __name__ == "__main__":
    main()
