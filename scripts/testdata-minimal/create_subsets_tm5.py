#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import xarray as xr

from tests.fixtures.tm5 import TM5_DATA_PATH

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


def atomic_write(ds: xr.Dataset, path: Path, **kwargs) -> None:
    """write dataset to a netcdf file atomically"""
    tmp = path.with_suffix(".tmp")
    try:
        ds.to_netcdf(tmp, **kwargs)
        tmp.rename(path)
    finally:
        tmp.unlink(missing_ok=True)


def main():
    for path in PATHS:
        ds = xr.open_dataset(SRC_DATA_PATH / path.name).pipe(reduce_dims)
        atomic_write(ds, path)


if __name__ == "__main__":
    main()
