#!/usr/bin/env python3

import matplotlib.pyplot as plt

import pyaerocom as pya

plt.close("all")

from pathlib import Path

import pyaerocom.testdata_access as td
from pyaerocom.conftest import CHECK_PATHS

tda = td.TestDataAccess()

TESTDATADIR = Path(tda.testdatadir)

OUTBASE = TESTDATADIR.joinpath("coldata")

if not OUTBASE.exists():
    OUTBASE.mkdir()

fpath = TESTDATADIR.joinpath(CHECK_PATHS["tm5aod"])
if not fpath.exists():
    raise Exception("Unexpected error, please debug")
mod = pya.GriddedData(fpath)

obs = pya.io.ReadAeronetSunV3("AeronetSunV3L2Subset.daily").read("od550aer")

coldata = pya.colocation.colocate_gridded_ungridded(mod, obs)

coldata.to_netcdf(OUTBASE)

print(coldata.calc_statistics())

coldata.plot_coordinates()

mod = mod.sel(latitude=(0, 3), longitude=(0, 4))
cgg = pya.colocation.colocate_gridded_gridded(mod, mod)
cgg.data = cgg.data[:, :3]

cgg.plot_scatter()

cgg.to_netcdf(OUTBASE)

pya.plot.mapping.plot_nmb_map_colocateddata(cgg)
