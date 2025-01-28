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

with xr.open_dataset(TEST_FILE_PATH, engine="netcdf4") as dt:
    gridded_data: dict[str, pya.griddeddata.GriddedData] = {}
    for var in dt.keys():
        try:
            aerocomvar = var_lookup[var]
        except KeyError:
            print(f"Unable to translate '{var}' to aerocom name.")
            continue
        
        data = dt[var].expand_dims("data_source").transpose("data_source", "time", "station_id")
        
        # TODO: Check if data can be read once, and filtered instead.
        obsdata = reader.read(vars_to_retrieve=aerocomvar)        

        for station in data.station_name:
            station_name = str(station.values.astype(str))
            print(station_name)
            try:
                obsdata_station = obsdata.filter_by_meta(ts_type="hourly", station_id=station_name)
            except pya.exceptions.DataExtractionError:
                print("Empty filtered object")
                continue

            print(obsdata_station)
    
        
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