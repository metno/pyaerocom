#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import xarray as xr

from tests.fixtures.mscw_ctm import EMEP_DATA_PATH

SRC_DATA_PATH = Path("/lustre/storeB/project/fou/kl/emep/ModelRuns")
SRC_DATA_PATH /= "2019_REPORTING/EMEP01_L20EC_rv4_33.2017"

VARIABLES = ["SURF_ug_O3", "SURF_ppb_O3", "SURF_ug_PM10_rh50", "SURF_ug_PM25_rh50", "SURF_ug_NO2"]
LAT, LON = slice(50, 52), slice(10, 12)

PATHS = (
    EMEP_DATA_PATH / "Base_day.nc",
    EMEP_DATA_PATH / "Base_month.nc",
    EMEP_DATA_PATH / "Base_fullrun.nc",
)


def reduce_dims(ds: xr.Dataset) -> xr.Dataset:
    """crop domain and remove "unlimited" from time coordinate"""
    del ds.encoding["unlimited_dims"]
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
        ds = xr.open_dataset(SRC_DATA_PATH / path.name)[VARIABLES].pipe(reduce_dims)
        atomic_write(ds, path)


if __name__ == "__main__":
    main()
