import pyaerocom as pya
import pathlib
import xarray as xr

from pyaerocom.io.uemep.model_variables import uemep_variables

import tempfile
UEMEP_PATH = pathlib.Path(
    "/lustre/storeB/project/fou/kl/emep/ModelRuns/uEMEP/uEMEP_norway/rerun/2023/stations"
)

TEST_FILE_PATH = UEMEP_PATH / "uEMEP_Norway_station_20231021_00.nc"


emep_var_map = uemep_variables()
var_lookup = {v: k for k, v in emep_var_map.items()}

reader = pya.io.readungridded.ReadUngridded("EBASMC")

with xr.open_mfdataset(list(UEMEP_PATH.glob("*.nc")), engine="netcdf4") as dt:
    gridded_data: dict[str, pya.griddeddata.GriddedData] = {}
    for x in dt.keys():
        try:
            aerocomvar = var_lookup[x]
        except KeyError:
            print(f"Unable to translate '{x}' to aerocom name.")
            continue
        
        data = dt[x].expand_dims("data_source").transpose("data_source", "time", "station_id")
        data = pya.griddeddata.GriddedData(TEST_FILE_PATH, var_name=x)

        with tempfile.TemporaryDirectory() as dir:
            dir = pathlib.Path(dir)
            print(dir)
            # data_id=None, var_name=None, vert_code=None, year=None, ts_type=None
            data.to_netcdf(dir, var_name = x, vert_code = "Surface", year=2023, ts_type="hourly")
            
            uemepdata = pya.GriddedData(list(dir.glob("*"))[0], var_name=x)

            print("Test")
        
        #data[aerocomvar] = dt[x].expand_dims("data_source").transpose("data_source", "time", "station_id")
        #data[aerocomvar].name = aerocomvar

        #obsdata = reader.read(vars_to_retrieve=aerocomvar)
        #print("test")
    #data = (
    #    dt.expand_dims("data_source")
    #    .transpose("data_source", "time", "station_id")
    #    .swap_dims({"station_id": "station_name"})[
    #        "no2_EMEP_additional_nonlocal_contribution"
    #    ]
    #)

#cdata = pya.colocation.colocated_data.ColocatedData(data=data)

print("Test")