import logging
import os
import warnings

import dask
import numpy as np
import pandas as pd


class PointCloudData:

    # Columns of the eventual numpy array
    TIME_IDX = 0
    LONGITUDE_IDX = 1
    LATITUDE_IDX = 2
    ALTITUDE_IDX = 3
    OBSERVATION_IDX = 4
    QA_FLAG_IDX = 5

    # Just make qa_value threshold a constant for now
    QA_THRESHOLD = 0.8

    def __init__(self, input=None, var_name=None):
        self._reader = None
        self._var_name = var_name
        self._core_columns_name_order = None
        if input:
            pass

    @property
    def var_name(self):
        """Name of variable"""
        return self.var_name

    @var_name.setter
    def var_name(self, val):
        """Name of variable"""
        if not isinstance(val, str):
            raise ValueError(f"Invalid input for var_name, need str, got {val}")
        self.var_name = val
        if "var_name" in self.metadata:
            self.metadata["var_name"] = val

    # LB: Not sure if / why both are needed
    @property
    def reader(self):
        """Instance of reader class from which this object was created

        Note
        ----
        Currently only supports instances of :class:`ReadPoinrCloud`.
        """
        # LB: If I don't put this here, get a circular import error
        from pyaerocom.plugins.pointcloud.reader import ReadPointCloud

        if not isinstance(self._reader, ReadPointCloud):
            self._reader = ReadPointCloud  # previous argument: self.data_id
        return self._reader

    @reader.setter
    def reader(self, val):

        # LB: If I don't put this here, get a circular import error
        from pyaerocom.plugins.pointcloud.reader import ReadPointCloud

        if not isinstance(val, ReadPointCloud):
            raise ValueError(
                "cannot set reader in ReadPointCloud: need instance of class ReadPointCloud"
            )
        self._reader = val

    @property
    def metadata(self):
        pass

    ##########################
    # Data formats for testing
    ##########################

    # single core cases
    def data_numpy(
        self, filename: str = None, vars_to_read_in: str = None, core_columns_name_order=None
    ) -> np.array:
        """
        Data array (n-dimensional numpy array)
        """
        reader = self.reader()
        xarray_data = reader.read_netcdf_file(filename=filename, group="PRODUCT")
        return self.convert_data_xarray_numpy(
            xarray_data=xarray_data,
            vars_to_read_in=vars_to_read_in,
            core_columns_name_order=core_columns_name_order,
        )

    def data_df(
        self, filename: str = None, vars_to_read_in: str = None, core_columns_name_order=None
    ) -> pd.DataFrame:
        reader = self.reader()
        xarray_data = reader.read_netcdf_file(filename=filename, group="PRODUCT")
        return self.convert_data_xarray_to_pandas_df(
            xarray_data=xarray_data,
            vars_to_read_in=vars_to_read_in,
            core_columns_name_order=core_columns_name_order,
        )

    # multi-processor cases
    def data_distributed_array(
        self, filename: str = None, vars_to_read_in: str = None, core_columns_name_order=None
    ):
        reader = self.reader()
        xarray_data = reader.read_netcdf_file_product(filename=filename)
        return self.convert_xarray_to_dask_array(
            xarray_data=xarray_data,
            vars_to_read_in=vars_to_read_in,
            core_columns_name_order=core_columns_name_order,
        )

    def data_distributed_df(
        self, filename: str = None, vars_to_read_in: str = None, core_columns_name_order=None
    ):
        reader = self.reader()
        xarray_data = reader.read_netcdf_file(filename=filename, group="PRODUCT")
        return self.convert_xarray_to_dask_df(
            xarray_data=xarray_data,
            vars_to_read_in=vars_to_read_in,
            core_columns_name_order=core_columns_name_order,
        )

    def data_xarray(
        self, filename: str = None, vars_to_read_in: str = None, core_columns_name_order=None
    ):
        reader = self.reader()
        return reader.read_netcdf_file(filename=filename, group="PRODUCT")

    ###########################
    # Methods to convert formats
    ###########################
    def convert_xarray_to_dask_df(
        self, xarray_data=None, vars_to_read_in: list = None, core_columns_name_order: list = None
    ):
        assert hasattr(xarray_data, "qa_value") and hasattr(xarray_data, "time_utc")
        obs = xarray_data[vars_to_read_in]
        # LB: these data types may be causeing issues later on when computing distances. They are with altitude. turn up as float 64???
        obs_df = obs.to_dask_dataframe()[core_columns_name_order].astype(
            {
                "time_utc": "str",
                "longitude": "float32",
                "latitude": "float32",
                "altitude": "float32",
                "ozone_profile": "float16",
                "qa_value": "float16",
            }
        )
        del obs  # maybe not needed, depends how big obs gets
        obs_df = obs_df.dropna()  # drop na's first to sorting goes through less
        obs_df = obs_df[obs_df["qa_value"] > self.QA_THRESHOLD - 0.01]
        return obs_df

    def convert_data_xarray_to_pandas_df(
        self, xarray_data=None, vars_to_read_in: list = None, core_columns_name_order: list = None
    ) -> pd.DataFrame:
        assert hasattr(xarray_data, "qa_value") and hasattr(xarray_data, "time_utc")
        obs = xarray_data[vars_to_read_in]
        # these data types may be causeing issues later on when computing distances
        obs_df = obs.to_dataframe()[core_columns_name_order].astype(
            {
                "longitude": "float16",
                "latitude": "float16",
                "altitude": "float16",
                "ozone_profile": "float16",
                "qa_value": "float16",
            }
        )
        obs_df = obs_df.assign(
            time_utc=pd.to_datetime(obs_df["time_utc"]).astype("datetime64[ns]")
        )
        del obs  # maybe not needed, depends how big obs gets
        obs_df = obs_df.dropna()  # drop na's first to sorting goes through less
        obs_df = obs_df[obs_df["qa_value"] > self.QA_THRESHOLD - 0.01]
        return obs_df

    def convert_data_xarray_numpy(
        self, xarray_data=None, vars_to_read_in: list = None, core_columns_name_order: list = None
    ):
        obs_df = self.convert_data_xarray_to_pandas_df(
            xarray_data=xarray_data,
            vars_to_read_in=vars_to_read_in,
            core_columns_name_order=core_columns_name_order,
        )
        obs_df = obs_df[core_columns_name_order]
        # return numpy array
        return obs_df.to_numpy()

    # @dask.delayed # would only be run when dask needs the result
    def convert_xarray_to_dask_array(
        self, xarray_data=None, vars_to_read_in: list = None, core_columns_name_order: list = None
    ):
        obs_df = self.convert_xarray_to_dask_df(
            xarray_data=xarray_data,
            vars_to_read_in=vars_to_read_in,
            core_columns_name_order=core_columns_name_order,
        )
        # set the index to be with respect to time_utc and sort in that order
        obs_df = obs_df.set_index(
            "time_utc", sorted=True, drop=False
        )  # drop = False is important. lose time otherwise
        # lengths = True here so we can do rechunking later on
        # earliest opportunity I've seen to start splitting up the observation array
        return obs_df.to_dask_array(lengths=True)
