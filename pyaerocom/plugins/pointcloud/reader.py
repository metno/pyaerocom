import glob
import logging
import os
import warnings

# import dask.array as da
import dask
import numpy as np
import xarray as xr

# import polars as pl
import pyaerocom as pya

logger = logging.getLogger(__name__)

# from pyaerocom.exceptions import DataDimensionError

# defines the interface of what we want to fill. here we fill
from pointclouddata import PointCloudData
from tropomi_variables import tropomi_variables


class ReadPointCloud:

    """
    Class to read PointCloudData.
    This is thought to be be a more general case than data which is collected at stations.
    Inspired for use by L2 satellite data, it may also cover cases in which stations move, for example.


    """

    #: Version log of this class (for caching)
    __version__ = "0.01"

    _FILEMASK = "*.nc"  # use eventually to just read in nc files in data_dir

    def __init__(self, data_id: str = None, data_dir: str = None, num_files_to_read_in=1):
        self._data_dir = None
        self._filename = None
        self._filepath = None
        self._group = None
        self.var_map = (
            tropomi_variables()
        )  # putting this here for now. In future can think of a TropomiData class which is either derived or this is a protocol which defines

        self.FILE_TYPE = ".nc"

        if data_dir is not None:
            if not isinstance(data_dir, str) or not os.path.exists(data_dir):
                raise FileNotFoundError(f"{data_dir}")
            self._data_dir = data_dir  # correct way to doing this? What about the setter?

        self.data_id = data_id
        self.num_files_to_read_in = num_files_to_read_in  # Because we can have million of data points a day, we need to be able the number of files we handle at once.

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "ReadPointCloud"

    @property
    def data_dir(self) -> str:
        """
        Directory where data files are located
        """
        if self._data_dir is None:
            raise AttributeError(f"data_dir needs to be set before accessing")
        return self._data_dir

    @data_dir.setter
    def data_dir(self, val: str):
        if val is None:
            raise ValueError(f"Data dir {val} needs to be a dictionary or a file")
        if not os.path.isdir(val):
            raise FileNotFoundError(val)
        # self._file_mask = self.FILE_MASKS[0] # What is this?
        self._data_dir = val
        # self.reinit()
        # self._filedata = None
        # self.search_all_files() # What about this?
        # self._files = self.filepaths

    @property
    def filename(self):
        """
        Name of netcdf file
        """
        return self._filename

    @filename.setter
    def filename(self, val: str):
        """
        Name of netcdf file
        """
        if not isinstance(val, str):  # pragma: no cover
            raise ValueError("needs str")
        elif val == self._filename:
            return
        self._filename = val
        self._filedata = None

    @property
    def filepath(self):
        """
        Path to data file
        """
        if self.data_dir is None and self._filepaths is None:  # pragma: no cover
            raise AttributeError("data_dir or filepaths needs to be set before accessing")
        return self._filepath

    @filepath.setter
    def filepath(self, value: str):
        if not isinstance(value, str):
            raise TypeError("needs to be a string")

        self._filepath = value
        ddir, fname = os.path.split(value)
        self.data_dir = ddir
        self.filename = fname

    @property
    def file_type(self):
        """File type of data files"""
        return (
            self.FILE_TYPE
        )  # For ReadGridded, this is coming from the class in gridio.py, eventually move?

    # @property
    # def group(self):
    #     return self._group

    # @group.setter
    # def group(self, value : str):
    #     if not isinstance(value, str):
    #         raise ValueError("needs to be a string")
    #     self._group = value

    @property
    def obs_name(self):
        return self.var_map[self.data_id]

    @property
    def columns_ordered(self):
        """Order of the columns in the in final data array"""
        return ["time_utc", "longitude", "latitude", "altitude", self.obs_name, "qa_value"]

    @property
    def data_files_in_data_dir(self):
        """Return a list of all the files in the data_dir which mathcing the FILETYPE"""
        return glob.glob(f"{self.data_dir}{self._FILEMASK}")

    @property
    def files_to_read_in(self):
        # need to think about this and how the data directory will be structured. Can we assume data will be split up by day into different dirs, or will it all be dumped into one dir , or will it be e.g., all data gfiles from 1 year in a data dir
        # funamental Q to resolve: What is a PointCloudData suppose to represent? Or can it be flexible? Can we leverage dask so that we potentially can iterate through all the chunks sequentially even though they won't all fit in memory at once?
        pass

    def open_file(self):
        return self.read_netcdf_file(self.filename, self.group)

    def read_netcdf_file(self, filename: str = None, group: str = None):
        # providing chunks will mean product is filled with dask arrays
        # product = xr.open_dataset(file_path + file_name, group='PRODUCT', chunks = {"time_utc": 10}) # {"latitude": chunk_size, "longitude": chunk_size}

        # possible idea: amke time a dimension? https://docs.xarray.dev/en/stable/generated/xarray.Dataset.swap_dims.html
        if group == None:
            return xr.open_dataset(filename)
        if group == "PRODUCT":
            return xr.open_dataset(filename, group=group)

    def read_directory_netcdf_files(self, filepath: str):
        pass

    def read_netcdf_product_attributes(self, filename: str = None, var: str = None):
        product = xr.open_dataset(filename, group="PRODUCT")
        return product[var].attrs

    def _get_meta(self):
        meta = {}
        for col in self.columns_ordered:
            meta[col] = self.read_netcdf_product_attributes(self.filename, var=col)
        return meta
