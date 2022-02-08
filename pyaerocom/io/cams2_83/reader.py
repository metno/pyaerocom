from __future__ import annotations

import os
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from time import time

import iris
import numpy as np
import xarray as xr
from pandas import DatetimeIndex, date_range

from pyaerocom import const
from pyaerocom.griddeddata import GriddedData
from pyaerocom.io.cams2_83.models import ModelName
from pyaerocom.units_helpers import UALIASES

from .models import ModelName

"""
TODO:

As it is now, with e.g. leap = 3 and start date 01.12, 01.12 might not be used, since the leap shifts the date three days forward
This might have to be componsated for, with the filepath being for 3 days before 01.12 (the start date)(?)
"""

CAMS2_83_vars = dict(
    concco="co_conc",
    concno2="no2_conc",
    conco3="o3_conc",
    concpm10="pm10_conc",
    concpm25="pm2p5_conc",
    concso2="so2_conc",
)


DATA_FOLDER_PATH = Path("/lustre/storeB/project/fou/kl/CAMS2_83/test_data")
# DATA_FOLDER_PATH = Path("/lustre/storeB/project/fou/kl/CAMS2_83/model")


def find_model_path(
    model: str | ModelName,
    date: str | date | datetime,
    root_path: Path | str,
) -> Path:
    if not isinstance(model, ModelName):
        model = ModelName[model]
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y%m%d")

    if isinstance(root_path, str):
        root_path = Path(root_path)
    # if os.path.isdir(DATA_FOLDER_PATH / f"{date:%Y%m}"):
    #     return DATA_FOLDER_PATH / f"{date:%Y%m}/{date:%Y%m%d}_{model}_forecast.nc"
    # else:
    #     return DATA_FOLDER_PATH / f"{date:%Y%m%d}_{model}_forecast.nc"

    return DATA_FOLDER_PATH / f"{date:%Y-%m-%d}-{model}-all-species.nc"


def get_cams2_83_vars(var_name):
    if not var_name in CAMS2_83_vars.keys():
        raise ValueError(f"{var_name} is not a valide variable for CAMS2-83")
    return CAMS2_83_vars[var_name]


class ReadCAMS2_83:
    FREQ_CODES = {
        "hour": "hourly",
        "day": "daily",
        "month": "monthly",
        "fullrun": "yearly",
    }

    REVERSE_FREQ_CODES = {
        "hourly": "hour",
        "daily": "day",
        "monthly": "month",
        "yearly": "fullrun",
    }

    def __init__(
        self,
        data_id: str | None = None,
        data_dir: str | Path | None = None,
    ) -> None:

        self._filedata = None
        self._filepaths = None
        self._data_dir = None
        self._model = None
        self._date = None
        self._data_id = None
        self._daterange = None

        self.data_id = data_id

        if data_dir is not None:
            if (
                not isinstance(data_dir, str) and not isinstance(data_dir, Path)
            ) or not os.path.exists(data_dir):
                raise FileNotFoundError(f"{data_dir}")

            self.data_dir = data_dir

        self.data_id = data_id

    @property
    def data_dir(self) -> str | Path:
        """
        Directory containing netcdf files
        """
        if self._data_dir is None:
            raise AttributeError(f"data_dir needs to be set before accessing")
        return self._data_dir

    @data_dir.setter
    def data_dir(self, val):
        if val is None:
            raise ValueError(f"Data dir {val} needs to be a dictionary or a file")
        if not os.path.isdir(val):
            raise FileNotFoundError(val)
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

        self._get_model_dateshift_from_id(val)
        self._data_id = val

    @property
    def filepaths(self) -> list[str | Path]:
        """
        Path to data file
        """
        if self.data_dir is None and self._filepaths is None:
            raise AttributeError("data_dir or filepaths needs to be set before accessing")
        if self._filepaths is None:
            self._filepaths = self._find_all_files()
        return self._filepaths

    @filepaths.setter
    def filepaths(self, value: list[str | Path]):
        if not isinstance(value, list) and not isinstance(value, Path):
            raise ValueError("needs to be list of strings")
        self._filepaths = value

    @property
    def filedata(self) -> list[xr.Dataset]:
        """
        Loaded netcdf file (:class:`xarray.Dataset`)
        """
        if self._filedata is None:
            self.open_file()
        return self._filedata

    @property
    def model(self) -> str:
        if self._model is None:
            raise ValueError(f"Model not set")
        return self._model

    @model.setter
    def model(self, val: str | ModelName):
        if isinstance(val, str):
            if val not in [m.value for m in ModelName]:
                raise ValueError(f"{val} not a valid model")

            for m in ModelName:

                if m.value == val:

                    self._model = m
                    break
            else:
                raise ValueError(f"{val} is not a valide model name")
            self._filedata = None
        elif isinstance(val, ModelName):
            if val not in ModelName.name:
                raise ValueError(f"{val} not a valid model")
            self._model = ModelName[val]
            self._filedata = None
            # Read new file paths(?)
        else:
            raise TypeError(f"{val} needs to be string of ModelName")

    @property
    def daterange(self) -> DatetimeIndex:
        if self._daterange is None:
            raise ValueError("The date range is not set yet")
        return self._daterange

    @daterange.setter
    def daterange(self, val: DatetimeIndex | list[datetime]):
        if (not isinstance(val, DatetimeIndex)) and (not isinstance(val, list)):
            raise TypeError(f"Date range {val} need to be a pandas DatetimeIndex or a list")

        self._daterange = self._parse_daterange(val)
        self._filedata = None

    @property
    def date(self) -> int:
        if self._date is None:
            raise ValueError("Date is not set")
        return self._date

    @date.setter
    def date(self, val: int):
        if not isinstance(val, int) or val < 0 or val > 3:
            raise TypeError(f"Date {val} is not a int between 0 and 3")
        self._date = val

    def _parse_daterange(self, val):
        if isinstance(val, DatetimeIndex):
            return val
        daterange = date_range(val[0], val[-1], freq="d")
        return daterange

    def _get_model_dateshift_from_id(self, id):
        words = id.split(".")

        if len(words) != 3:
            raise ValueError(f"The id {id} is not on the correct format")

        model = words[1]
        if not words[2].startswith("day"):
            raise ValueError(f"The day {words[2]} needs to be on the format 'day[0-3]'")
        dateshift = int(re.search(r"day(\d)", words[2]).group(1))

        self.model = str(model.casefold())
        self.date = dateshift

    def _load_var(self, var_name_aerocom: str, ts_type: str) -> xr.DataArray:
        """
        Load variable data as :class:`xarray.DataArray`.

        This combines both, variables that can be read directly and auxiliary
        variables that are computed.

        Parameters
        ----------
        var_name_aerocom : str
            variable name
        ts_type : str
            desired frequency

        Raises
        ------
        VarNotAvailableError
            if input variable is not available

        Returns
        -------
        xarray.DataArray
            loaded data

        """
        data = self.filedata[var_name_aerocom]

        old_lon = data.longitude.data
        old_lon = np.where(old_lon > 180, old_lon - 360, old_lon)
        data["longitude"] = old_lon

        data.attrs["long_name"] = var_name_aerocom
        data.time.attrs["long_name"] = "time"
        data.time.attrs["standard_name"] = "time"

        data.longitude.attrs["long_name"] = "longitude"
        data.longitude.attrs["standard_name"] = "longitude"
        data.longitude.attrs["units"] = "degrees_east"

        data.latitude.attrs["long_name"] = "latitude"
        data.latitude.attrs["standard_name"] = "latitude"
        data.latitude.attrs["units"] = "degrees_north"
        return data

    def _find_all_files(self):
        model = self.model
        daterange = self.daterange

        filepaths = []

        for date in daterange:
            location = find_model_path(model, date, self.data_dir)
            if not os.path.isfile(location):
                print(f"Could not find {location} . Skipping file")
            else:
                filepaths.append(location)

        if len(filepaths) == 0:
            raise ValueError(f"Could not find any data to read for {self.model}")

        self.filepaths = filepaths
        return filepaths

    def _select_date(self, ds: xr.Dataset) -> xr.Dataset:

        forecast_date = ds.attrs["FORECAST"]
        forecast_date = re.search(r"Europe, (\d*)\+\[0H_96H\]", forecast_date).group(1)
        forecast_date = datetime.strptime(forecast_date, "%Y%m%d")

        # select_date = forecast_date + timedelta(days=self.date)

        # dateselect = date_range(select_date, select_date + timedelta(hours=23), freq="h")
        # ds = ds.sel(time=dateselect)
        # ds = ds.sel(level=0.0)
        # ds.time.attrs["long_name"] = "time"
        # ds.time.attrs["standard_name"] = "time"
        # return ds

        day_prefix = " " if abs(self.date) == 0 else f"{int(self.date)} days "
        dateselect = [f"{day_prefix}{i:02d}:00:00" for i in range(24)]

        ds = ds.sel(time=dateselect)
        ds = ds.sel(level=0.0)

        forecast_hour = (forecast_date - datetime(1900, 1, 1)).days * 24
        # new_dates = [forecast_hour+i for i in range(24)]

        new_dates = date_range(forecast_date, forecast_date + timedelta(hours=23), freq="h")
        ds["time"] = new_dates
        # ds.time.attrs["units"] = "hours since 1900-01-01"
        ds.time.attrs["long_name"] = "time"
        ds.time.attrs["standard_name"] = "time"
        return ds

    def has_var(self, var_name):
        """Check if variable is supported

        Parameters
        ----------
        var_name : str
            variable to be checked

        Returns
        -------
        bool
        """
        if var_name in CAMS2_83_vars.keys():
            return True
        return False

    def open_file(self) -> xr.Dataset:
        """
        Opens the data set for the current model

        Returns
        -------
        dict(xarray.Dataset)
            Dict with years as keys and Datasets as items

        """
        self._find_all_files()
        ds = xr.open_mfdataset(self.filepaths, preprocess=self._select_date)  # , parallel=True)

        self._filedata = ds

        return ds

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
        # var_name have to be made into the correct PollutantName
        var = const.VARS[var_name]
        var_name_aerocom = var.var_name_aerocom

        cams_var = get_cams2_83_vars(var_name)

        # ts_type can be ignored
        for key in kwargs.keys():
            if "daterange" in key:
                self.daterange = kwargs[key]
                break
        else:
            if self._daterange is None:
                raise ValueError(f"The date range needs to be defined in the kwargs {kwargs}")

        # ts_type = "hourly"

        if ts_type != "hourly":
            raise ValueError(f"CAMS2-83 is not readable using hourly data, and not {ts_type}")
        var_name_aerocom = var_name
        ds = self._load_var(cams_var, ts_type)

        ds.attrs["Simulation date"] = self.date

        cube = ds.to_iris()

        # if ts_type == "hourly":
        #     cube.coord("time").convert_units("hours since 1900-01-01")
        gridded = GriddedData(
            cube,
            var_name=var_name_aerocom,
            ts_type=ts_type,
            check_unit=True,
            convert_unit_on_init=True,
        )

        gridded.metadata["data_id"] = self.data_id

        return gridded


if __name__ == "__main__":
    data_dir = DATA_FOLDER_PATH
    data_id = "CAMS2-83.EMEP.day0"
    reader = ReadCAMS2_83(data_dir=data_dir, data_id=data_id)

    t0 = time()
    daterange = list(date_range(start="20190601", end="20190613"))

    # print(reader.open_file())
    print(reader.read_var("concno2", ts_type="hourly", daterange=daterange))

    print(time() - t0)
