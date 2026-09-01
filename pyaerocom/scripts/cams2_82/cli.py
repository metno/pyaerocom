from __future__ import annotations

import logging
import multiprocessing as mp
from collections.abc import Iterator
from copy import deepcopy
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

import typer

import pyaerocom.scripts.cams2_82.converter as converter
from pyaerocom import ConfigReader, change_verbosity
from pyaerocom.io.cams2_82.reader import DATA_FOLDER_PATH
from pyaerocom.scripts.cams2_82.config import (
    CFG,
    make_Aeronet_entry,
    make_EEA_entry,
    make_EPROFILE_entry,
    make_ICOS_entry,
    make_model_entry,
    make_openAQ_entry,
)
from pyaerocom.scripts.cams2_82.evaluation import runner

app = typer.Typer(add_completion=False, no_args_is_help=True)
app.add_typer(converter.app, name="convert")
logger = logging.getLogger(__name__)

const = ConfigReader.get_instance()

DEFAULT_EEA_PATH = Path("/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/EEA-AQDS/download")
DEFAULT_AERONET_PATH = Path("/lustre/storeB/users/danielh/cams282/src/")
DEFAULT_OPENAQ_PATH = Path("/lustre/storeB/users/danielh/cams282/src/openaq/")
DEFAULT_VPROFILES_PATH = Path("/lustre/storeB/project/fou/kl/v-profiles")
DEFAULT_ICOS_PATH = Path("/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/ICOS/NRT/")
VPROFILES_EXCLUDE_LIST = ["AP_0-20000-0-03808-C","AP_0-20000-0-07014-A","AP_0-20000-0-07110-A","AP_0-20000-0-07145-A","AP_0-20000-0-07606-A","AP_0-20000-0-07617-A","AP_0-20000-0-07774-A","AP_0-20000-0-78990-A","AP_0-20008-0-LAU-A","AP_0-203-10-LNG-A"]
DEFAULT_MODEL_PATH = DATA_FOLDER_PATH


def date_range(start_date: date, end_date: date) -> tuple[date, ...]:
    days = (end_date - start_date) // timedelta(days=1)
    assert days >= 0
    return tuple(start_date + timedelta(days=day) for day in range(days + 1))

def make_period(start_date: date, end_date: date) -> list[str]:
    if start_date == end_date:
        return [f"{start_date:%Y%m%d}"]
    periods = [f"{start_date:%Y%m%d}-{end_date:%Y%m%d}"]

    return periods

def vpro_subpaths(
    *dates: datetime | date | str,
    root_path: Path | str = DEFAULT_VPROFILES_PATH,
) -> Iterator[Path]:
    for date in dates:  # noqa: F402
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y%m%d").date()
        if isinstance(date, datetime):
            date = date.date()
        if isinstance(root_path, str):
            root_path = Path(root_path)
        subpath = "%Y/%m/%d/"
        pattern = "AP*-%Y-%m-%d.nc"
        path = root_path / date.strftime(subpath)
        fpaths = path.glob(date.strftime(pattern))
        for p in fpaths: 
            # exclude wigos IDs that belong to Mini-MPL and CL61 instruments, aka wrong wavelength
            if any(wigosid in str(p) for wigosid in VPROFILES_EXCLUDE_LIST):
                continue
            yield p.resolve()

def make_config(
    start_date: date,
    end_date: date,
    model_path: Path,
    eea_path: Path,
    icos_path: Path,
    aeronet_path: Path,
    openaq_path: Path,
    vprofiles_path: Path,
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
    cfg["obs_cfg"]["EPROFILE"] = make_EPROFILE_entry(start_date, end_date, vprofiles_path)
    cfg["obs_cfg"]["EPROFILE"]["read_opts_ungridded"]["files"] = [  # type:ignore[index]
        str(p)
        for p in vpro_subpaths(
            *obs_dates, root_path=vprofiles_path,
        )
    ]
    cfg["obs_cfg"]["ICOS"] = make_ICOS_entry(start_date, end_date, icos_path)
    #cfg["obs_cfg"]["openAQ"] = make_openAQ_entry(start_date, end_date, openaq_path)
    cfg["obs_cfg"]["Aeronet"] = make_Aeronet_entry(start_date, end_date, aeronet_path)
    cfg["obs_cfg"]["EEA"] = make_EEA_entry(start_date, end_date, eea_path)
    cfg["model_cfg"]["IFS-OSUITE"] = make_model_entry(start_date, end_date, model_path)

    cfg.update(exp_id=id, exp_name=name, exp_descr=description)

    if add_map:
        cfg.update(add_model_maps=True)

    if only_map:
        cfg.update(add_model_maps=True, only_model_maps=True)

    if add_seasons:
        cfg.update(add_seasons=True)

    return cfg


@app.command()
def run(
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
    icos_obs_path: Path = typer.Option(
        DEFAULT_ICOS_PATH, exists=True, readable=True, help="path to observation data"
    ),
    aeronet_obs_path: Path = typer.Option(
        DEFAULT_AERONET_PATH, exists=True, readable=True, help="path to observation data"
    ),
    openaq_obs_path: Path = typer.Option(
        DEFAULT_OPENAQ_PATH, exists=True, readable=True, help="path to observation data"
    ),
    vprofiles_path: Path = typer.Option(
        DEFAULT_VPROFILES_PATH, exists=True, readable=True, help="path to v-profiles data"
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
        icos_obs_path,
        aeronet_obs_path,
        openaq_obs_path,
        vprofiles_path,
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


    const.OBSLOCS_UNGRIDDED["EPROFILE"] = str(vprofiles_path)

   
    logger.info("Standard run")
    runner(cfg, cache, dry_run=dry_run, pool=pool)




if __name__ == "__main__":
    app()
