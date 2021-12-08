from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
import os
import re
from pyaerocom.griddeddata import GriddedData

import xarray as xr
from pandas import date_range, DatetimeIndex
import numpy as np

from pyaerocom.io.cams2_83.models import ModelName
from pyaerocom.units_helpers import UALIASES


DATA_FOLDER_PATH = Path("/home/danielh/lustre/storeB/project/fou/kl/CAMS2_83/test_data")

def find_model_path(model: str | ModelName, date: str | date | datetime) -> Path:
    if not isinstance(model, ModelName):
        model = ModelName[model]
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y%m%d")
    return DATA_FOLDER_PATH / f"{date:%Y-%m-%d}-{model}-all-species.nc"





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


    def __init__(self, data_id: str | None = None, data_dir: str | Path | None = None, daterange: DatetimeIndex | None = None) -> None:
        self._filedata = None
        self._filepaths = None
        self._data_dir = None
        self._model = None

        if data_dir is not None:
            if (not isinstance(data_dir, str) and not isinstance(data_dir, Path)) or not os.path.exists(data_dir):
                raise FileNotFoundError(f"{data_dir}")

            self.data_dir = data_dir

        self.data_id = data_id

        self._daterange = daterange



    @property
    def data_dir(self) -> list[str | Path]:
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
    def filepaths(self) -> list[str | Path]:
        """
        Path to data file
        """
        if self.data_dir is None and self._filepaths is None:
            raise AttributeError("data_dir or filepaths needs to be set before accessing")
        #if self._filepaths is None:
        #self._filepaths = find_model_path()
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
            if val not in ModelName:
                raise ValueError(f"{val} not a valid model")
            self._model = val
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
    def daterange(self, val: DatetimeIndex):
        if not isinstance(val, DatetimeIndex):
            raise TypeError(f"Date range {val} need to be a pandas DatetimeIndex")
        self._daterange = val
        self._filedata = None
        

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
        raise NotImplementedError

    def _find_all_files(self):
        model = self.model
        daterange = self.daterange

        filepaths = []

        for date in daterange:
            filepaths.append(find_model_path(model, date))
        
        self.filepaths = filepaths

    def _select_date(self, ds):

        forecast_date = ds.attrs["FORECAST"]

        forecast_date = re.search(r"Europe, (\d*)\+\[0H_96H\]", forecast_date).group(1)

        dt = datetime.strptime(forecast_date, "%Y%m%d")

        dateselect = [f"1 days {i:02d}:00:00" for i in range(24)]
        
        ds = ds.sel(time=dateselect)

        return ds

    def open_file(self) -> xr.Dataset:
        """
        Opens the data set for the current model

        Returns
        -------
        dict(xarray.Dataset)
            Dict with years as keys and Datasets as items

        """
        ds = xr.open_mfdataset(self.filepaths)
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
        raise NotImplementedError


if __name__=="__main__":
    data_dir = DATA_FOLDER_PATH
    reader = ReadCAMS2_83(data_dir=data_dir)

    reader.daterange = date_range(start="20210602", end="20210602")
    reader.model = ModelName.EMEP

    reader._find_all_files()

    print(reader.filepaths)
    
    ds = reader.open_file()
    #dateselect = date_range(start="T0000", end="T2300", freq="h")
    dateselect = [f"1 days {i:02d}:00:00" for i in range(24)]
    #print(dateselect)
    #ds = ds.sel(time=dateselect)

    forecast_date = ds.attrs["FORECAST"]

    forecast_date = re.search(r"Europe, (\d*)\+\[0H_96H\]", forecast_date).group(1)

    dt = datetime.strptime(forecast_date, "%Y%m%d")

    print(dt)
