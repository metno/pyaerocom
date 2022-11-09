from __future__ import annotations

from pathlib import Path

import typer
import xarray as xr

from tests.fixtures.tm5 import TM5_DATA_PATH

from .emep import atomic_write

SRC_DATA_PATH = Path("/lustre/storeA/project/aerocom/aerocom-users-database")
SRC_DATA_PATH /= "AEROCOM-PHASE-III-2019/TM5-met2010_AP3-CTRL2019/renamed"

LON, LAT = slice(20, 30), slice(20, 30)

PATHS = {
    TM5_DATA_PATH / "aerocom3_TM5-met2010_AP3-CTRL2019_abs550aer_Column_2010_daily.nc",
    TM5_DATA_PATH / "aerocom3_TM5-met2010_AP3-CTRL2019_od550aer_Column_2010_daily.nc",
}


def reduce_dims(ds: xr.Dataset) -> xr.Dataset:
    """crop domain"""
    return ds.isel(lon=LON, lat=LAT)


def main(tm5_path: Path = typer.Argument(SRC_DATA_PATH, exists=True, dir_okay=True)):
    """minimal TM5 dataset"""
    for path in PATHS:
        ds = xr.open_dataset(tm5_path / path.name).pipe(reduce_dims)
        atomic_write(ds, path)
