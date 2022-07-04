#!/usr/bin/env python3
"""
Create minimal testdataset for GHOST reader
"""
from pathlib import Path

import matplotlib.pyplot as plt
import xarray as xr

import pyaerocom as pya
from tests.fixtures.data_access import TestData

plt.close("all")

path_in = Path(pya.const.OUTPUTDIR) / "data/obsdata/GHOST/data"
path_out = TestData("obsdata/GHOST/data").path

assert path_in.is_dir(), f"missing {path_in}"
assert path_out.is_dir(), f"missing {path_out}"

datasets = ["EEA_AQ_eReporting", "EBAS"]

freqs = ["hourly", "daily"]

varis = ["pm10", "sconco3"]
datesfiles = ["201810", "201911", "201912"]

filename = lambda var, date: f"{var}_{date}.nc"

for dsname in datasets:
    for freq in freqs:
        indir = path_in / dsname / freq
        assert indir.is_dir(), f"missing {indir}"

        outdir = path_out / dsname / freq
        outdir.mkdir(exist_ok=True)
        for var in varis:
            if var == "pm10":
                dates = datesfiles
                numst = 3
                numts = None if freq == "daily" else 3
            else:
                dates = datesfiles[0:1]
                numst = 1
                numts = 3
            for date in dates:
                dir_in = indir / var
                assert dir_in.is_dir(), f"missing {dir_in}"

                dir_out = outdir / var
                dir_out.mkdir(exist_ok=True)

                fname = filename(var, date)
                file_in = dir_in / fname
                file_out = dir_out / fname
                print(file_in)
                print(file_out)
                assert file_in.exists, f"missing {file_in}"

                ds = xr.open_dataset(file_in)
                subset = ds.isel(station=slice(0, numst))
                if numts is not None:
                    subset = subset.isel(time=slice(0, numts))

                subset.to_netcdf(file_out)
                print("Saved")
