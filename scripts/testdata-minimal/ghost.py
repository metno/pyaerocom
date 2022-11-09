"""
Create minimal testdataset for GHOST reader
"""
from itertools import product
from pathlib import Path

import typer
import xarray as xr

import pyaerocom as pya
from tests.fixtures.data_access import DataForTests

PATH_IN = Path(pya.const.OUTPUTDIR) / "data/obsdata/GHOST/data"
PATH_OUT = DataForTests("obsdata/GHOST/data").path
DATASETS = ["EBAS"]
FREQS = ["hourly", "daily"]
VARS = ["pm10", "sconco3"]
DATES = ["201810", "201911", "201912"]


def main(
    path_in: Path = typer.Argument(PATH_IN, exists=True, dir_okay=True),
    path_out: Path = typer.Argument(PATH_OUT, exists=True, dir_okay=True),
):
    """minimal GHOST dataset"""
    for dsname, freq, var in product(DATASETS, FREQS, VARS):
        if var == "pm10":
            dates = DATES
            numst = 3
            numts = None if freq == "daily" else 3
        else:
            dates = DATES[0:1]
            numst = 1
            numts = 3
        for date in dates:
            file_in = path_in / dsname / freq / var / f"{var}_{date}.nc"
            assert file_in.exists(), f"missing {file_in}"

            file_out = path_out / file_in.relative_to(path_in)
            file_out.parent.mkdir(exist_ok=True, parents=True)
            print(file_in)
            print(file_out)

            ds = xr.open_dataset(file_in)
            ds = ds.isel(station=slice(0, numst))
            if numts is not None:
                ds = ds.isel(time=slice(0, numts))

            ds.to_netcdf(file_out)
            print("Saved")
