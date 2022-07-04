#!/usr/bin/env python3

import pyaerocom as pya
from tests.fixtures.data_access import TestData
from tests.fixtures.tm5 import CHECK_PATHS

OUTBASE = TestData("coldata").path
OUTBASE.mkdir(exist_ok=True)


def main():

    path = TestData(CHECK_PATHS.tm5aod).path
    assert path.exists(), f"missing {path}"

    mod = pya.GriddedData(path)
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


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    plt.close("all")
    main()
