#!/usr/bin/env python3
"""
Create minimal testdataset for GHOST reader
"""
from itertools import product
from pathlib import Path

import xarray as xr

import pyaerocom as pya
from tests.fixtures.data_access import TestData

path_in = Path(pya.const.OUTPUTDIR) / "data/obsdata/GHOST/data"
path_out = TestData("obsdata/GHOST/data").path

assert path_in.is_dir(), f"missing {path_in}"
assert path_out.is_dir(), f"missing {path_out}"

datasets = ["EEA_AQ_eReporting", "EBAS"]

freqs = ["hourly", "daily"]

varis = ["pm10", "sconco3"]
datesfiles = ["201810", "201911", "201912"]

for dsname, freq, var in product(datasets, freqs, varis):
    if var == "pm10":
        dates = datesfiles
        numst = 3
        numts = None if freq == "daily" else 3
    else:
        dates = datesfiles[0:1]
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
