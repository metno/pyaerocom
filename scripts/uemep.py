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
        
        data = dt[var].expand_dims("data_source").transpose("data_source", "time", "station_id").assign_coords(data_source=["uemep"])
        #swap_dims({"station_id": "station_name"})
        data2 = xr.DataArray(
            0,
            coords = {
                "station_name": data.station_name,
                "time": data.time,
                "lat": data.lat,
                "lon": data.lon, 
            },
            dims=["time", "station_id"]
        ).expand_dims("data_source").assign_coords(data_source=["ebas"])



        merged = xr.concat([data, data2], dim='data_source') 
        #obsdata = reader.read(vars_to_retrieve=aerocomvar)        
        merged.transpose("data_source", "time", "station_name")
        coldat = pya.colocation.colocated_data.ColocatedData(merged)
        coldat.data.attrs = {
            "obsvar": aerocomvar,
            "ts_type": "hourly",
            "filter_name": "ALL-wMOUNTAINS",
            "ts_type_src": ["hourly", "hourly"],
            "var_units": [data.attrs["units"], data.attrs["units"]],
            "data_level": 3, #?
            "revision_ref": "20250128", #?
            "from_files": [], #?
            "from_files_ref": [],
            "colocate_time": 0, #?
            "obs_is_clim": 0,
            "pyaerocom": pya.__version__,
            "CONV!min_num_obs": str(dict(monthly=dict(daily=3))),
            "resample_how": "mean",
            "obs_name": "EBASMC",
            "vert_code": "Surface",
            "diurnal_only": 0,
            "zeros_to_nan": 0,
            "data_source": ["uemep", "EBASMC"],
            "var_name": [aerocomvar, aerocomvar]
        }
        #coldat.to_netcdf(".")
        for station in data.station_name:
            station_name = str(station.values.astype(str))            
            print(station_name)
            try:
                obsdata_station = obsdata.filter_by_meta(ts_type="hourly")
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