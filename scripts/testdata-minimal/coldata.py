from pathlib import Path

import typer

import pyaerocom as pya
from tests.fixtures.data_access import DataForTests
from tests.fixtures.tm5 import CHECK_PATHS

MOD_PATH = DataForTests(CHECK_PATHS.tm5aod).path
OUT_PATH = DataForTests("coldata").path


def main(
    mod_path: Path = typer.Argument(MOD_PATH, exists=True, dir_okay=True),
    out_path: Path = typer.Argument(OUT_PATH, exists=True, dir_okay=True),
):
    """collocated data example"""

    mod = pya.GriddedData(mod_path)
    obs = pya.io.ReadAeronetSunV3("AeronetSunV3L2Subset.daily").read("od550aer")

    coldata = pya.colocation.colocate_gridded_ungridded(mod, obs)
    coldata.to_netcdf(out_path)
    print(coldata.calc_statistics())

    coldata.plot_coordinates()

    mod = mod.sel(latitude=(0, 3), longitude=(0, 4))
    cgg = pya.colocation.colocate_gridded_gridded(mod, mod)
    cgg.data = cgg.data[:, :3]

    cgg.plot_scatter()
    cgg.to_netcdf(out_path)

    pya.plot.mapping.plot_nmb_map_colocateddata(cgg)
