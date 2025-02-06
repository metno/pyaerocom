#!/usr/bin/env python3
"""
Create minimal testdataset for GHOST reader

Created on Fri Feb 26 09:17:09 2021

@author: jonasg
"""

import os

import matplotlib.pyplot as plt

plt.close("all")
import xarray as xr

import pyaerocom as pya

path_in = os.path.join(pya.const.OUTPUTDIR, "data/obsdata/GHOST/data")

path_out = os.path.join(pya.const.OUTPUTDIR, "testdata-minimal/obsdata/GHOST/data")

assert os.path.exists(path_in)
assert os.path.exists(path_out)

datasets = ["EEA_AQ_eReporting", "EBAS"]

freqs = ["hourly", "daily"]

varis = ["pm10", "sconco3"]
datesfiles = ["201810", "201911", "201912"]


def filename(var: str, date: str) -> str:
    return f"{var}_{date}.nc"


files_out = []
for dsname in datasets:
    for freq in freqs:
        indir = os.path.join(path_in, dsname, freq)
        assert os.path.exists(indir)
        outdir = os.path.join(path_out, dsname, freq)
        os.makedirs(outdir, exist_ok=True)
        assert os.path.exists(outdir)
        for var in varis:
            if var == "pm10":
                dates = datesfiles
                numst = 3

                numts = None if freq == "daily" else 3

            else:
                dates = [datesfiles[0]]
                numst = 1
                numts = 3
            for date in dates:
                dir_in = os.path.join(indir, var)
                dir_out = os.path.join(outdir, var)
                os.makedirs(dir_out, exist_ok=True)
                assert os.path.exists(dir_in)
                fname = filename(var, date)
                file_in = os.path.join(dir_in, fname)
                file_out = os.path.join(dir_out, fname)
                print(file_in)
                print(file_out)
                assert os.path.exists(file_in)

                with xr.open_dataset(file_in, decode_timedelta=True) as ds:
                    subset = ds.isel(station=slice(0, numst))
                    if numts is not None:
                        subset = subset.isel(time=slice(0, numts))

                    subset.to_netcdf(file_out)
                print("Saved")
