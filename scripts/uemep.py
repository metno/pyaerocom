import pyaerocom as pya
import pathlib
import xarray as xr

import numpy as np
import pandas as pd

from pyaerocom.io.uemep import uemep_variables
from pyaerocom.colocation.colocated_data import validate_structure


UEMEP_PATH = pathlib.Path(
    "/lustre/storeB/project/fou/kl/emep/ModelRuns/uEMEP/uEMEP_norway/rerun/2023/stations"
)

TEST_FILE_PATH = UEMEP_PATH / "uEMEP_Norway_station_20230101_00.nc"


emep_var_map = uemep_variables()
var_lookup = {v: k for k, v in emep_var_map.items()}

reader = pya.io.readungridded.ReadUngridded("EBASMC")

#with xr.open_dataset(TEST_FILE_PATH, engine="netcdf4", decode_timedelta=True) as dt:
with xr.open_mfdataset(list(UEMEP_PATH.glob("*.nc")), engine="netcdf4", decode_timedelta=True) as dt:
    gridded_data: dict[str, pya.griddeddata.GriddedData] = {}
    for var in dt.keys():
        try:
            aerocomvar = var_lookup[var]
        except KeyError:
            print(f"Unable to translate '{var}' to aerocom name.")
            continue
        
        data = dt[var].swap_dims({"station_id": "station_name"})

        data = data.assign_coords({"station_name": data.station_name.astype(str)})
        # Pyaerocom uses the mid-time for its values, while model data is start time, so need
        # to shift.
        data = data.assign_coords(time = data.time + pd.Timedelta(minutes=30))
        station_ids = data["station_name"].values.astype(str)

        # TODO: Filterpost?
        obsdata = reader.read(vars_to_retrieve=[aerocomvar])

        fobsdata = obsdata.filter_by_meta(
            ts_type = "hourly",
        )

        start_date = str(data.time.min().values)
        end_date = str(data.time.max().values)
        print(f"Time span: {start_date}, {end_date}")

        sdata: dict[str, pya.stationdata.StationData] = {}
        stations = fobsdata.to_station_data_all()
        for station_name, station in zip(stations["station_name"], stations["stats"]):
            station: pya.stationdata.StationData
            if station.station_id not in station_ids:
                print(f"No matching station_id for {station.station_id}. Skipping...")
                continue
            sdata[station.station_id] = station

        if len(sdata.keys()) == 0:
            print(f"No valid station data found for period.")
            continue

        darrays = [
            xr.DataArray(
                (ts := station.to_timeseries(aerocomvar).loc[start_date:end_date]), dims=['time'], coords={'time': ts.index}, name=aerocomvar
            ) for _, station in sdata.items()
        ]

        combined = xr.concat(darrays, dim=pd.Index([x for x in sdata.keys()], name="station_name"))
        data = data.expand_dims(data_source=["uemep"])
        combined = combined.expand_dims(data_source=["EBASMC"])
        combined = combined.assign_coords({"station_name": [x for x in combined.station_name.values]})
        
        coldataarray = xr.concat([combined, data], dim="data_source")
        #coldataarray = xr.concat([combined, data], dim=pd.Index([x for x in ["EBASMC", "uemep"]], name="data_source"))
        coldataarray = coldataarray.transpose("data_source", "time", "station_name").rename(
            {
                "lat": "latitude",
                "lon": "longitude"
            }
        )
        
        coldat = pya.colocation.colocated_data.ColocatedData(coldataarray)
        coldat.data.attrs = {
            "obs_vars": aerocomvar,
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
            "data_source": ["EBASMC", "uemep"],
            "var_name": [aerocomvar, aerocomvar]
        }
        validate_structure(coldat.data)
        coldat.to_netcdf(".")

print("Test")