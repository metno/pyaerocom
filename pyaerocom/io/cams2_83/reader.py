from __future__ import annotations

import logging
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterator

import numpy as np
import pandas as pd
import xarray as xr

from pyaerocom.griddeddata import GriddedData
from pyaerocom.io.cams2_83.models import ModelData, ModelName, RunType
from pyaerocom.units_helpers import UALIASES

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


DATA_FOLDER_PATH = Path("/lustre/storeB/project/fou/kl/CAMS2_83/model")


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


# def _model_path(
#     name: str | ModelName,
#     date: str | date | datetime,
#     *,
#     run: str | RunType = RunType.FC,
#     root_path: str | Path = DATA_FOLDER_PATH,
# ) -> Path:
#     if not isinstance(name, ModelName):
#         name = ModelName[name]
#     if isinstance(date, str):
#         date = datetime.strptime(date, "%Y%m%d").date()

#     if isinstance(root_path, str):
#         root_path = Path(root_path)
#     if isinstance(date, datetime):
#         date = date.date()
#     if not isinstance(run, RunType):
#         run = RunType[run]
#     return ModelData(name, run, date, root_path).path


# def get_cams2_83_vars(var_name):
#     if not var_name in CAMS2_83_vars.keys():
#         raise ValueError(f"{var_name} is not a valide variable for CAMS2-83")
#     return CAMS2_83_vars[var_name]


def model_paths(
    model: str | ModelName,
    *dates: datetime | date | str,
    root_path: Path | str = DATA_FOLDER_PATH,
    run: str | RunType = RunType.FC,
) -> Iterator[Path]:
    for date in dates:
        path = __model_path(model, date, run=run, root_path=root_path)
        if not path.is_file():
            logger.warning(f"Could not find {path.name}. Skipping {date}")
            continue
        yield path


def parse_daterange(
    dates: pd.DatetimeIndex | list[datetime] | tuple[datetime, datetime]
) -> pd.DatetimeIndex:
    if isinstance(dates, pd.DatetimeIndex):
        return dates
    if len(dates) != 2:
        raise ValueError("need 2 datetime objets to define a date_range")
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
        ds = ds.assign_coords(time=np.datetime64(first_date) + ds.time.data)

    try:
        ds = ds.sel(time=dateselect)
    except:
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


def read_dataset(paths: list[Path], *, day: int) -> xr.Dataset:
    def preprocess(ds: xr.Dataset) -> xr.Dataset:
        return ds.pipe(forecast_day, day=day)

    ds = xr.open_mfdataset(paths, preprocess=preprocess, parallel=False)
    return ds.pipe(fix_coord).pipe(fix_names)


class ReadCAMS2_83:
    FREQ_CODES = dict(hour="hourly", day="daily", month="monthly", fullrun="yearly")
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
            raise AttributeError(f"data_dir needs to be set before accessing")
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
            raise AttributeError(f"data_id needs to be set before accessing")
        return self._data_id

    @data_id.setter
    def data_id(self, val):
        if val is None:
            raise ValueError(f"The data_id {val} can't be None")
        elif not isinstance(val, str):
            raise TypeError(f"The data_id {val} needs to be a string")

        self._data_id = val

        match = re.match(r"^CAMS2-83\.(.*)\.day(\d)$", val)
        if match is None:
            raise ValueError(f"The id {id} is not on the correct format")

        model, day = match.groups()
        self.model = ModelName[model]
        self.forecast_day = int(day)

    @property
    def filepaths(self) -> list[Path]:
        """
        Path to data file
        """
        if self.data_dir is None and self._filepaths is None:  # type:ignore[unreachable]
            raise AttributeError("data_dir or filepaths needs to be set before accessing")
        if self._filepaths is None:
            paths = list(model_paths(self.model, *self.daterange, root_path=self.data_dir))
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
            raise ValueError(f"Model not set")
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
        if not isinstance(dates, (pd.DatetimeIndex, list, tuple)):
            raise TypeError(f"{dates} need to be a pandas DatetimeIndex or 2 datetimes")

        self._daterange = parse_daterange(dates)
        self._filedata = None

    # @property
    # def date(self) -> int:
    #     if self._date is None:
    #         raise ValueError("Date is not set")
    #     return self._date

    # @date.setter
    # def date(self, val: int):
    #     if not isinstance(val, int) or val < 0 or val > 3:
    #         raise TypeError(f"Date {val} is not a int between 0 and 3")
    #     self._date = val

    # def _parse_daterange(self, val):
    #     if isinstance(val, pd.DatetimeIndex):
    #         return val
    #     daterange = pd.date_range(val[0], val[-1], freq="d")
    #     return daterange

    # def _get_model_dateshift_from_id(self, id):
    #     words = id.split(".")

    #     if len(words) != 3:
    #         raise ValueError(f"The id {id} is not on the correct format")

    #     model = words[1]
    #     if not words[2].startswith("day"):
    #         raise ValueError(f"The day {words[2]} needs to be on the format 'day[0-3]'")
    #     dateshift = int(re.search(r"day(\d)", words[2]).group(1))

    #     self.model = ModelName[model]
    #     self.date = dateshift

    # def _load_var(self, var_name_aerocom: str, ts_type: str) -> xr.DataArray:
    #     """
    #     Load variable data as :class:`xarray.DataArray`.

    #     This combines both, variables that can be read directly and auxiliary
    #     variables that are computed.

    #     Parameters
    #     ----------
    #     var_name_aerocom : str
    #         variable name
    #     ts_type : str
    #         desired frequency

    #     Raises
    #     ------
    #     VarNotAvailableError
    #         if input variable is not available

    #     Returns
    #     -------
    #     xarray.DataArray
    #         loaded data

    #     """
    #     data = self.filedata[var_name_aerocom]

    #     old_lon = data.longitude.data
    #     old_lon = np.where(old_lon > 180, old_lon - 360, old_lon)
    #     data["longitude"] = old_lon

    #     data.attrs["long_name"] = var_name_aerocom
    #     data.time.attrs["long_name"] = "time"
    #     data.time.attrs["standard_name"] = "time"

    #     data.longitude.attrs["long_name"] = "longitude"
    #     data.longitude.attrs["standard_name"] = "longitude"
    #     data.longitude.attrs["units"] = "degrees_east"

    #     data.latitude.attrs["long_name"] = "latitude"
    #     data.latitude.attrs["standard_name"] = "latitude"
    #     data.latitude.attrs["units"] = "degrees_north"
    #     return data

    # def _find_all_files(self):
    #     model = self.model
    #     daterange = self.daterange

    #     filepaths = []

    #     for date in daterange:
    #         location = _model_path(model, date, root_path=self.data_dir)
    #         # location = find_model_path(model, date, self.data_dir)
    #         if not os.path.isfile(location):
    #             print(f"Could not find {location} . Skipping file")
    #         else:
    #             filepaths.append(location)

    #     if len(filepaths) == 0:
    #         raise ValueError(f"Could not find any data to read for {self.model}")

    #     self.filepaths = filepaths
    #     return filepaths

    # def _select_date(self, ds: xr.Dataset) -> xr.Dataset:

    #     # forecast_date = ds.attrs["FORECAST"]
    #     # forecast_date = re.search(r"Europe, (\d*)\+\[0H_96H\]", forecast_date).group(1)
    #     # forecast_date = datetime.strptime(forecast_date, "%Y%m%d")

    #     fd = ModelData.frompath(ds.encoding["source"]).date

    #     forecast_date = datetime(fd.year, fd.month, fd.day, 0, 0, 0)
    #     select_date = forecast_date + timedelta(days=self.date)

    #     dateselect = date_range(select_date, select_date + timedelta(hours=23), freq="h")
    #     try:
    #         ds = ds.sel(time=dateselect)
    #     except:
    #         ds = ds.interp(time=dateselect)
    #         ds = ds.sel(time=dateselect)

    #     ds = ds.sel(level=0.0)
    #     ds.time.attrs["long_name"] = "time"
    #     ds.time.attrs["standard_name"] = "time"
    #     return ds

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
            raise ValueError(f"Only hourly ts_type is supported")

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
    from time import perf_counter

    data_dir = DATA_FOLDER_PATH
    data_id = "CAMS2-83.EMEP.day0"
    reader = ReadCAMS2_83(data_dir=data_dir, data_id=data_id)
    dates = ("2021-12-01", "2021-12-04")

    seconds = -perf_counter()
    print(reader.read_var("concno2", ts_type="hourly", daterange=dates))

    seconds += perf_counter()
    print(timedelta(seconds=int(seconds)))
