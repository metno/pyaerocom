import pyaerocom as pya
import pathlib
import xarray as xr

from pyaerocom.io.uemep.model_variables import uemep_variables
UEMEP_PATH = pathlib.Path(
    "/lustre/storeB/project/fou/kl/emep/ModelRuns/uEMEP/uEMEP_norway/rerun/2023/stations"
)

TEST_FILE_PATH = UEMEP_PATH / "uEMEP_Norway_station_20231021_00.nc"


emep_var_map = uemep_variables()
var_lookup = {v: k for k, v in emep_var_map.items()}

data = {}
reader = pya.io.readungridded.ReadUngridded("EBASMC")

with xr.open_dataset(TEST_FILE_PATH) as dt:
    for x in dt.keys():
        try:
            aerocomvar = var_lookup[x]
        except KeyError:
            print(f"Unable to translate '{x}' to aerocom name.")
            continue

        data[aerocomvar] = dt[x].expand_dims("data_source").transpose("data_source", "time", "station_id")
        data[aerocomvar].name = aerocomvar

        obsdata = reader.read(vars_to_retrieve=aerocomvar)
        print("test")
    #data = (
    #    dt.expand_dims("data_source")
    #    .transpose("data_source", "time", "station_id")
    #    .swap_dims({"station_id": "station_name"})[
    #        "no2_EMEP_additional_nonlocal_contribution"
    #    ]
    #)

#cdata = pya.colocation.colocated_data.ColocatedData(data=data)

print("Test")