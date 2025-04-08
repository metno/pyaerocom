from __future__ import annotations

import logging
import re
from collections.abc import Iterator
from datetime import date, datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
from tqdm import tqdm

from pyaerocom.griddeddata import GriddedData
from pyaerocom.io.cams2_83.models import ModelData, ModelName, RunType
from pyaerocom.io.gridded_reader import GriddedReader

"""
TODO:

As it is now, with e.g. leap = 3 and start date 01.12, 01.12 might not be used, since the leap shifts the date three days forward
This might have to be componsated for, with the filepath being for 3 days before 01.12 (the start date)(?)
"""

AEROCOM_NAMES = dict(
    co_conc="concco",
    no2_conc="concno2",
    o3_conc="conco3",
    pm10_conc="concpm10",
    pm2p5_conc="concpm25",
    so2_conc="concso2",
)

FULL_NAMES = dict(
    co_conc="Carbon Monoxide",
    no2_conc="Nitrogen Dioxide",
    o3_conc="Ozone",
    pm10_conc="PM10 Aerosol",
    pm2p5_conc="PM2.5 Aerosol",
    so2_conc="Sulphur Dioxide",
)

STANDARD_NAMES = dict(
    co_conc="mass_concentration_of_carbon_monoxide_in_air",
    no2_conc="mass_concentration_of_nitrogen_dioxide_in_air",
    o3_conc="mass_concentration_of_ozone_in_air",
    pm10_conc="mass_concentration_of_pm10_ambient_aerosol_in_air",
    pm2p5_conc="mass_concentration_of_pm2p5_ambient_aerosol_in_air",
    so2_conc="mass_concentration_of_sulfur_dioxide_in_air",
)


DATA_FOLDER_PATH = Path("/lustre/storeB/project/fou/kl/CAMS2_83/model")


DEBUG = True


logger = logging.getLogger(__name__)


def __model_path(
    name: str | ModelName,
    date: str | date | datetime,
    *,
    root_path: Path | str,
    run: str | RunType,
) -> Path:
    if not isinstance(name, ModelName):
        name = ModelName[name]
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y%m%d").date()
    if isinstance(date, datetime):
        date = date.date()
    if isinstance(root_path, str):
        root_path = Path(root_path)
    if not isinstance(run, RunType):
        run = RunType[run]
    return ModelData(name, run, date, root_path).path


def model_paths(
    model: str | ModelName,
    *dates: datetime | date | str,
    root_path: Path | str = DATA_FOLDER_PATH,
    run: str | RunType = RunType.FC,
) -> Iterator[Path]:
    for date in dates:  # noqa: F402
        path = __model_path(model, date, run=run, root_path=root_path)
        if not path.is_file():
            logger.warning(f"Could not find {path.name}. Skipping {date}")
            continue
        yield path


def parse_daterange(
    dates: pd.DatetimeIndex | list[datetime] | tuple[datetime, datetime],
) -> pd.DatetimeIndex:
    if isinstance(dates, pd.DatetimeIndex):
        return dates
    if len(dates) != 2:
        raise ValueError("need 2 datetime objects to define a date_range")
    return pd.date_range(*dates, freq="d")


def forecast_day(ds: xr.Dataset, *, day: int) -> xr.Dataset:
    data = ModelData.frompath(ds.encoding["source"])
    if not (0 <= day <= data.run.days):
        raise ValueError(f"{data} has no day #{day}")
    date = data.date + timedelta(days=day)
    first_date = data.date

    select_date = datetime(date.year, date.month, date.day, 0, 0, 0)

    dateselect = pd.date_range(select_date, select_date + timedelta(hours=23), freq="h")

    if isinstance(ds.time.data[0], np.timedelta64):
        logger.debug(f"Changing time dimension for {ds.encoding['source']}")
        ds = ds.assign_coords(time=np.datetime64(first_date) + ds.time.data)

    if len(set(np.array(ds.time))) != len(np.array(ds.time)):
        logger.debug(f"Changing time dimension for {ds.encoding['source']}")
        ds = ds.assign_coords(time=dateselect)

    # if len(ds.time.data) < 2:
    #     return xr.Dataset()
    try:
        ds = ds.sel(time=dateselect)
    except Exception as e:
        logger.debug(f"{e}")
        logger.debug(f"Interpolating NaNs for {ds.encoding['source']}")
        ds = ds.interp(time=dateselect)
        ds = ds.sel(time=dateselect)

    ds = ds.sel(level=0.0)
    ds.time.attrs["long_name"] = "time"
    ds.time.attrs["standard_name"] = "time"

    for var_name in ds.data_vars:
        ds[var_name].attrs["forecast_day"] = day
    return ds


def fix_coord(ds: xr.Dataset) -> xr.Dataset:
    lon = ds.longitude.data
    ds["longitude"] = np.where(lon > 180, lon - 360, lon)
    ds.longitude.attrs.update(
        long_name="longitude", standard_name="longitude", units="degrees_east"
    )
    ds.latitude.attrs.update(long_name="latitude", standard_name="latitude", units="degrees_north")
    return ds


def fix_names(ds: xr.Dataset) -> xr.Dataset:
    for var_name, aerocom_name in AEROCOM_NAMES.items():
        ds[var_name].attrs.update(long_name=aerocom_name)
    return ds.rename(AEROCOM_NAMES)


def fix_missing_vars(ds: xr.Dataset) -> xr.Dataset:
    """
    TODO: Check if all variables are there. If not:
    make the rest of the variables, filled with nans.
    Log an error when this is done

    Might not be possible...
    """
    vars_list = [i for i in ds.data_vars]
    nb_vars = len(vars_list)
    if nb_vars < 6:
        logger.warning(f"Found only {vars_list}. Filling the rest with NaNs")

        dummy_var = ds[vars_list[0]]
        dummy_var_name = vars_list[0]
        for species in AEROCOM_NAMES:
            if species not in vars_list:
                ds = ds.assign(**{species: dummy_var * np.nan})
                attrs = ds[dummy_var_name].attrs
                attrs["species"] = FULL_NAMES[species]
                attrs["standard_name"] = STANDARD_NAMES[species]
                ds[species] = ds[species].assign_attrs(attrs)
    return ds


def read_dataset(paths: list[Path], *, day: int) -> xr.Dataset:
    paths = check_files(paths)

    def preprocess(ds: xr.Dataset) -> xr.Dataset:
        return ds.pipe(forecast_day, day=day).pipe(fix_missing_vars)

    ds = xr.open_mfdataset(paths, preprocess=preprocess, parallel=False, chunks={"time": 24})
    return ds.pipe(fix_coord).pipe(fix_names)


def check_files(paths: list[Path]) -> list[Path]:
    if not DEBUG:
        return paths

    new_paths: list[Path] = []

    for p in tqdm(paths, disable=None):
        try:
            with xr.open_dataset(p, decode_timedelta=True) as ds:
                if len(ds.time.data) < 2:
                    logger.warning(f"To few timestamps in {p}. Skipping file")
                    continue
                if len(set(np.array(ds.time))) != len(np.array(ds.time)):
                    if len(np.array(ds.time)) != 24:
                        logger.warning(
                            f"Ambiguous time dimension: Duplicate timestamps in {p}, with less that 24 step. Skipping file"
                        )
                        continue

            new_paths.append(p)
        except Exception as ex:
            logger.warning(f"Error when opening {p}: {ex}. Skipping file")

    return new_paths


class ReadCAMS2_83(GriddedReader):
    FREQ_CODES = dict(hour="hourly")
    REVERSE_FREQ_CODES = {val: key for key, val in FREQ_CODES.items()}

    def __init__(
        self,
        data_id: str | None = None,
        data_dir: str | Path | None = None,
    ) -> None:
        self._filedata: xr.Dataset | None = None
        self._filepaths: list[Path] | None = None
        self._data_dir: Path | None = None
        self._model: ModelName | None = None
        self._forecast_day: int | None = None
        self._data_id: str | None = None
        self._daterange: pd.DatetimeIndex | None = None

        self._run_type: RunType = RunType.FC

        if data_dir is not None:
            if isinstance(data_dir, str):
                data_dir = Path(data_dir)
            self.data_dir = data_dir

        if data_id is not None:
            self.data_id = data_id

    @property
    def data_dir(self) -> Path:
        """
        Directory containing netcdf files
        """
        if self._data_dir is None:
            raise AttributeError("data_dir needs to be set before accessing")
        return self._data_dir

    @data_dir.setter
    def data_dir(self, val: str | Path | None):
        if val is None:
            raise ValueError(f"Data dir {val} needs to be a dictionary or a file")
        if isinstance(val, str):
            val = Path(val)
        if not val.is_dir():
            raise NotADirectoryError(val)
        self._data_dir = val
        self._filedata = None

    @property
    def data_id(self):
        if self._data_id is None:
            raise AttributeError("data_id needs to be set before accessing")
        return self._data_id

    @data_id.setter
    def data_id(self, val):
        if val is None:
            raise ValueError(f"The data_id {val} can't be None")
        elif not isinstance(val, str):
            raise TypeError(f"The data_id {val} needs to be a string")

        self._data_id = val

        match = re.match(r"^CAMS2-83\.(.*)\.day(\d)\.(FC|AN)$", val)
        if match is None:
            raise ValueError(f"The id {val} is not on the correct format")

        model, day, run_type = match.groups()
        self.run_type = RunType[run_type]
        self.model = ModelName[model]
        self.forecast_day = int(day)

    @property
    def years_avail(self):
        return np.unique(
            self.daterange.values.astype("datetime64[Y]").astype("int") + 1970
        ).astype("str")

    @property
    def ts_types(self):
        return self.REVERSE_FREQ_CODES.keys()

    @property
    def vars_provided(self):
        return AEROCOM_NAMES.values()

    @property
    def run_type(self):
        if self._run_type is None:
            raise AttributeError("run_type needs to be set before accessing")
        return self._run_type

    @run_type.setter
    def run_type(self, val):
        if val is None:
            raise AttributeError("run_type cannot be set as None")
        elif not isinstance(val, RunType):
            raise AttributeError(f"run_type cannot be set as {type(val)}, but must be a RunType")

        self._run_type = val

    @property
    def filepaths(self) -> list[Path]:
        """
        Path to data file
        """
        if self.data_dir is None and self._filepaths is None:  # type:ignore[unreachable]
            raise AttributeError("data_dir or filepaths needs to be set before accessing")
        if self._filepaths is None:
            paths = list(
                model_paths(
                    self.model,
                    *self.daterange,
                    root_path=self.data_dir,
                    run=self.run_type,
                )
            )
            if not paths:
                raise ValueError(f"no files found for {self.model}")
            self._filepaths = paths
        return self._filepaths

    @filepaths.setter
    def filepaths(self, value: list[Path]):
        if not bool(list):
            raise ValueError("needs to be list of paths")
        if not isinstance(value, list):
            raise ValueError("needs to be list of paths")
        if all(isinstance(path, Path) for path in value):
            raise ValueError("needs to be list of paths")
        self._filepaths = value

    @property
    def filedata(self) -> xr.Dataset:
        """
        Loaded netcdf file (:class:`xarray.Dataset`)
        """
        if self._filedata is None:
            self._filedata = read_dataset(self.filepaths, day=self.forecast_day)
        return self._filedata

    @property
    def model(self) -> str:
        if self._model is None:
            raise ValueError("Model not set")
        return self._model

    @model.setter
    def model(self, val: str | ModelName):
        if not isinstance(val, ModelName):
            val = ModelName(val)
        self._model = val
        self._filedata = None

    @property
    def daterange(self) -> pd.DatetimeIndex:
        if self._daterange is None:
            raise ValueError("The date range is not set yet")
        return self._daterange

    @daterange.setter
    def daterange(self, dates: pd.DatetimeIndex | list[datetime] | tuple[datetime]):
        if not isinstance(dates, pd.DatetimeIndex | list | tuple):
            raise TypeError(f"{dates} need to be a pandas DatetimeIndex or 2 datetimes")

        self._daterange = parse_daterange(dates)
        self._filedata = None

    @property
    def forecast_day(self) -> int:
        if self._forecast_day is None:
            raise ValueError("forecast_day is not set")
        return self._forecast_day

    @forecast_day.setter
    def forecast_day(self, val: int):
        if not isinstance(val, int) or not (0 <= val <= 3):
            raise TypeError(f"forecast_day {val} is not a int between 0 and 3")
        self._forecast_day = val

    @staticmethod
    def has_var(var_name):
        """Check if variable is supported

        Parameters
        ----------
        var_name : str
            variable to be checked

        Returns
        -------
        bool
        """
        return var_name in AEROCOM_NAMES.values()

    def read_var(self, var_name: str, ts_type: str | None = None, **kwargs) -> GriddedData:
        """Load data for given variable.

        Parameters
        ----------
        var_name : str
            Variable to be read
        ts_type : str
            Temporal resolution of data to read. Supported are
            "hourly", "daily", "monthly" , "yearly".

        Returns
        -------
        GriddedData
        """
        if "daterange" in kwargs:
            self.daterange = kwargs["daterange"]
        if self._daterange is None:
            raise ValueError(f"No 'daterange' in kwargs={kwargs}")

        if ts_type != "hourly":
            raise ValueError("Only hourly ts_type is supported")

        cube = self.filedata[var_name].to_iris()

        gridded = GriddedData(
            cube,
            var_name=var_name,
            ts_type=ts_type,
            check_unit=True,
            convert_unit_on_init=True,
        )
        gridded.metadata["data_id"] = self.data_id
        return gridded


if __name__ == "__main__":
    # from time import perf_counter

    data_dir = str(DATA_FOLDER_PATH)
    data_id = "CAMS2-83.EMEP.day0.AN"
    reader = ReadCAMS2_83(data_dir=data_dir, data_id=data_id)
    reader.daterange = ("2021-12-01", "2021-12-04")
    print(
        np.unique(reader.daterange.values.astype("datetime64[Y]").astype("int") + 1970).astype(
            "str"
        )
    )
    print(reader.filepaths)
    # dates = ("2021-12-01", "2021-12-04")

    # seconds = -perf_counter()
    # print(reader.read_var("concno2", ts_type="hourly", daterange=dates))

    # seconds += perf_counter()
    # print(timedelta(seconds=int(seconds)))
