import pathlib
import xarray as xr
import os
import logging
from pyaerocom.units import Unit
from pyaerocom.io.uemep import uemep_variables
from pyaerocom.colocation.colocated_data import validate_structure
from pyaerocom.io.readungridded import ReadUngridded
import pyaerocom
import time
import pandas as pd
import datetime


from pyaerocom.units.units_helpers import get_unit_conversion_fac


logger = logging.getLogger(__name__)


class UEMEPColocator:
    """
    Helper class for colcating uEMEP station data with observation
    data.

    Limitations:

    - Only colocates hourly model data with hourly obs data. No temporal
    resampling occurs.
    - Only works for EBAS data currently.

    :param uemep_station_data : Path to folder containing uemep_station_data, or list of files. Files
    must be readable using xarray's open_mfdataset().
    :param obs : dict or list with observations to be colocated against. If list, must be
    data_ids understood by ReadUngridded. If dict, must be a mapping from identifier to data_id
    understood by ReadUngridded. The identifier can be chosen freely and is only used for metadata
    (which is shown on Aeroval).
    :var_names : A list of variables. If not provided, all variables defined in uemep_variables.toml
    will be tried.
    :out_dir : Directory where colocated data objects will be written. Note that output will be one
    file per variable/observation combination. Variables will be stored as files following aerocom
    convention.
    """

    # Maps an aerocom variable name to it's equivalent uemep variable name.
    VAR_LOOKUP = uemep_variables()

    def __init__(
        self,
        uemep_station_data: os.PathLike | str | list[os.PathLike | str],
        *,
        obs: dict[str, str] | list[str],
        var_names: str | list[str] | None = None,
        out_dir: os.PathLike | None = None,
    ):
        """
        :param uemep_station_data: Folder with .nc UEMEP station data.
        :param var_names: List of aerocom variable names to colocate.
        :param obs: Either list of obs_ids passed to ReadUngridded, or dict with mapping
        of identifier to obs_id passed to ReadUngridded.
        :param out_dir: Path to output directory where colocated data objects will be stored.
        Defaults to '.'.
        """
        if isinstance(var_names, str):
            var_names = [var_names]

        if not isinstance(uemep_station_data, list):
            logger.info("Looking for station data in '%s'.", uemep_station_data)
            self._file_path = list(pathlib.Path(uemep_station_data).glob("*.nc"))
        else:
            logger.info("Using the following files as station data: '%s'", uemep_station_data)
            self._file_path = [pathlib.Path(p) for p in uemep_station_data]

        self._uemep_station_data = None

        if var_names is None:
            var_names = list(UEMEPColocator.VAR_LOOKUP.keys())
            logger.info(
                "No variable list configured. Defaulting to all configured uemep variables: %s",
                var_names,
            )

        aerocom_vars = []
        for var in var_names:
            if var not in UEMEPColocator.VAR_LOOKUP.keys():
                logger.warning(
                    "Variable '%s' not found in configured uEMEP variables. It will be ignored.",
                    var,
                )
                continue

            aerocom_vars.append(var)

        self._vars = sorted(set(aerocom_vars))

        if isinstance(obs, list):
            self._obs = {v: ReadUngridded(v) for v in obs}
        elif isinstance(obs, dict):
            self._obs = {k: ReadUngridded(v) for k, v in obs.items()}
        else:
            raise TypeError

        if out_dir is None:
            out_dir = pathlib.Path(".")

        self._out_dir = out_dir

    def _load_station_data(self) -> None:
        logger.info("Reading uEMEP station data. This may take a while.")
        start_time = time.perf_counter()
        with xr.open_mfdataset(self._file_path, engine="netcdf4", decode_timedelta=True) as dt:
            self._uemep_station_data = dt
        logger.info(f"Finished reading data in {time.perf_counter() - start_time:.3f} seconds.")

    @property
    def uemep_station_data(self) -> xr.Dataset:
        if self._uemep_station_data is None:
            self._load_station_data()

        return self._uemep_station_data

    def _run_single_variable(self, var: str) -> None:
        uemep_name = UEMEPColocator.VAR_LOOKUP[var]
        logger.info("Using uemep variable '%s' for aerocom variable '%s'", uemep_name, var)

        uemep_data = self.uemep_station_data[uemep_name].swap_dims({"station_id": "station_name"})
        model_unit = Unit(uemep_data.attrs["units"])
        uemep_data = uemep_data.assign_coords(
            {"station_name": uemep_data.station_name.astype(str)}
        ).assign_coords({"time": uemep_data.time + pd.Timedelta(minutes=30)})
        station_ids = uemep_data["station_name"].values.astype(str)

        for obs_id, obs_reader in self._obs.items():
            logger.info("Running colocation against obs_id '%s'.", obs_id)

            obsdata = obs_reader.read(vars_to_retrieve=[var])

            fobsdata = obsdata.filter_by_meta(ts_type="hourly")

            start_date = str(uemep_data.time.min().values)
            end_date = str(uemep_data.time.max().values)

            logger.info("uEMEP data spans %s-%s", start_date, end_date)

            sdata: dict[str, pyaerocom.stationdata.StationData] = {}
            stations = fobsdata.to_station_data_all()
            for _, station in zip(stations["station_name"], stations["stats"]):
                ids = station.station_id.split(";")
                if not any([id in station_ids for id in ids]):
                    logger.info(
                        "Station '%s' not found in uemep data. Skipping.",
                        station.station_id,
                    )
                    continue

                sdata[station.station_id] = station

            if len(sdata.keys()) == 0:
                logger.error(
                    "No matching stations found in '%s'. Aborting colocation of '%s'.",
                    obs_id,
                    var,
                )
                continue

            for s in station_ids:  # Remove timeseries for stations not present in model data.
                if s not in sdata.keys():
                    uemep_data = uemep_data.drop(s, dim="station_name")

            darrays: list[xr.DataArray] = []
            sids = []
            for sid, station in sdata.items():
                ts = station.to_timeseries(var).loc[start_date:end_date]
                if len(ts) == 0:
                    logger.warning("Length of timeseries for '%s' is 0.", station.station_id)
                    continue

                unit = Unit(station.var_info[var]["units"])

                conversion_factor = get_unit_conversion_fac(unit, model_unit)
                if conversion_factor != 1:
                    logger.info(
                        f"Transforming timeseries from '{unit}' to '{model_unit}' using conversion factor {float(conversion_factor):.2}."
                    )
                    ts *= conversion_factor

                darrays.append(
                    xr.DataArray(ts, dims=["time"], coords={"time": ts.index}, name=var)
                )
                sids.append(sid)

            if len(darrays) == 0:
                logger.error("No stations with data for the given time range.")
                return

            combined = xr.concat(darrays, dim=pd.Index(sids, name="station_name"))
            uemep_data = uemep_data.expand_dims(data_source=["uemep"])
            combined = combined.expand_dims(data_source=[obs_id])
            combined = combined.assign_coords(
                {"station_name": [x for x in combined.station_name.values]}
            )

            coldataarray = xr.concat([combined, uemep_data], dim="data_source")

            coldataarray = coldataarray.transpose("data_source", "time", "station_name").rename(
                {"lat": "latitude", "lon": "longitude"}
            )
            coldataarray = coldataarray.drop_vars("station_id")
            coldat = pyaerocom.colocation.colocated_data.ColocatedData(coldataarray)
            coldat.data.attrs = {
                "obs_vars": var,
                "ts_type": "hourly",
                "filter_name": "ALL-wMOUNTAINS",
                "ts_type_src": ["hourly", "hourly"],
                "var_units": [
                    uemep_data.attrs["units"],
                    uemep_data.attrs["units"],
                ],
                "data_level": 2,
                "revision_ref": datetime.datetime.strftime(datetime.date.today(), "%Y%m%d"),
                "from_files": [str(p) for p in self._file_path],
                "from_files_ref": [],
                "colocate_time": 0,  # ?
                "obs_is_clim": 0,
                "pyaerocom": pyaerocom.__version__,
                "CONV!min_num_obs": str(dict(monthly=dict(daily=3))),
                "resample_how": "mean",
                "obs_name": obs_id,
                "vert_code": "Surface",
                "diurnal_only": 0,
                "zeros_to_nan": 0,
                "data_source": [obs_id, "uemep"],
                "var_name": [var, var],
            }
            validate_structure(coldat.data)
            logger.info("Writing colocated data object to file in dir '%s'.", self._out_dir)
            coldat.to_netcdf(self._out_dir)

    def run(self) -> None:
        logger.info("Starting colocation.")
        for i, var in enumerate(self._vars, start=1):
            logger.info("Processing variable %d of %d: %s", i, len(self._vars), var)
            self._run_single_variable(var)

        logger.info("Finished.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])
    colocator = UEMEPColocator(
        uemep_station_data=pathlib.Path(
            "/lustre/storeB/project/fou/kl/emep/ModelRuns/uEMEP/uEMEP_norway/rerun/2023/stations"
        ),
        obs=["EBASMC"],
        var_names=["conco3"],
    )
    colocator.run()
