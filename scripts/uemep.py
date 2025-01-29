import pyaerocom as pya
import pathlib
import xarray as xr

import numpy as np
import pandas as pd

from pyaerocom.io.uemep import uemep_variables

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
        
        data = dt[var].swap_dims({"station_id": "station_name"})
        # .expand_dims("data_source").transpose("data_source", "time", "station_id").assign_coords(data_source=["UEMEP"])
        #data2 = xr.DataArray(
        #    0,
        #    coords = {
        #        "station_name": data.station_name,
        #        "time": data.time,
        #        "lat": data.lat,
        #        "lon": data.lon, 
        #    },
        #    dims=["time", "station_id"]
        #).expand_dims("data_source").assign_coords(data_source=["ebas"])
#
        # TODO: Filterpost?
        obsdata = reader.read(vars_to_retrieve=[aerocomvar])

        # Filterbymeta, station, hourly, time, latlon

        fobsdata = obsdata.filter_by_meta(
            ts_type = "hourly",
        )
        
        #stations = fobsdata.to_station_data_all()
        # TODO Hardcoded date range for now.
        start_date = '2023-01-01'
        end_date = '2023-01-02'
        new_data = xr.DataArray(
            np.nan,
            dims=['time', 'station_name'],
            coords={
                #'data_source': ["obs"],
                'time': fobsdata.to_station_data_all()["stats"][0].to_timeseries(aerocomvar).loc[start_date:end_date].index,
                'station_name': [str(s.values.astype(str)) for s in data.station_name]
            }
        )
        for station in data.station_name:
            station_name = str(station.values.astype(str))
            try:
                sobsdata = fobsdata.filter_by_meta(station_id=station_name)
            except pya.exceptions.DataExtractionError:
                print(f"No data for variable '{aerocomvar}' and station '{station_name}'.")
                continue
            stations = sobsdata.to_station_data_all()

            assert len(stations["stats"]) == 1

            sdata = stations["stats"][0]

            timeseries: pd.Series = sdata.to_timeseries(aerocomvar).loc[start_date:end_date]

            
            darray = xr.DataArray(timeseries, dims=['time'], coords={'time': timeseries.index})
            #expanded_data_sources = np.array(data.data_source.values.tolist() + ["ebas"], dtype="bytes")

            #data = data.reindex({'data_source': expanded_data_sources}, fill_value = np.nan)

            #data = xr.concat([data, darray], dim="data_source")
            data.loc[dict(station_name=station_name)] = darray

        data = data.expand_dims({'data_source': ["uemep"]})
        new_data = new_data.expand_dims({'data_source': ["observations"]})

        data = xr.concat([data, new_data], dim = "data_source")
        coldat = pya.colocation.colocated_data.ColocatedData(data)
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
            "data_source": ["uemep", "observations"],
            "var_name": [aerocomvar, aerocomvar]
        }
        coldat.to_netcdf(".")
        print("Test")
        ## Colocate with uemep data.
        #merged = xr.concat([data, data2], dim='data_source') 
        ##obsdata = reader.read(vars_to_retrieve=aerocomvar)        
        #merged.transpose("data_source", "time", "station_name")
        #coldat = pya.colocation.colocated_data.ColocatedData(merged)
        #coldat.data.attrs = {
        #    "obsvar": aerocomvar,
        #    "ts_type": "hourly",
        #    "filter_name": "ALL-wMOUNTAINS",
        #    "ts_type_src": ["hourly", "hourly"],
        #    "var_units": [data.attrs["units"], data.attrs["units"]],
        #    "data_level": 3, #?
        #    "revision_ref": "20250128", #?
        #    "from_files": [], #?
        #    "from_files_ref": [],
        #    "colocate_time": 0, #?
        #    "obs_is_clim": 0,
        #    "pyaerocom": pya.__version__,
        #    "CONV!min_num_obs": str(dict(monthly=dict(daily=3))),
        #    "resample_how": "mean",
        #    "obs_name": "EBASMC",
        #    "vert_code": "Surface",
        #    "diurnal_only": 0,
        #    "zeros_to_nan": 0,
        #    "data_source": ["uemep", "EBASMC"],
        #    "var_name": [aerocomvar, aerocomvar]
        #}
        ##coldat.to_netcdf(".")
        #for station in data.station_name:
        #    station_name = str(station.values.astype(str))            
        #    print(station_name)
        #    try:
        #        obsdata_station = obsdata.filter_by_meta(ts_type="hourly")
        #    except pya.exceptions.DataExtractionError:
        #        print("Empty filtered object")
        #        continue
#
        #    print(obsdata_station)
    
        
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