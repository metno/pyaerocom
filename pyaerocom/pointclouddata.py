import logging
import os
from typing import Protocol

import iris
import numpy as np
import pandas as pd
import xarray as xr

from pyaerocom import const
from pyaerocom._warnings import ignore_warnings
from pyaerocom.exceptions import (
    CoordinateError,
    DataDimensionError,
    DataExtractionError,
    DimensionOrderError,
    ResamplingError,
    TemporalResolutionError,
    VariableDefinitionError,
    VariableNotFoundError,
)

logger = logging.getLogger(__name__)


class PointCloudData(Protocol):
    """pyaerocom object representing point cloud data, such as 3-dimesional and 4-dimensional spatio-temporal fields"""

    # _META_ADD = dict(
    #     from_files =[],
    #     data_id="undefined",
    #     var_name_read="undefined",
    #     ts_type="undefined",
    #     vert_code=None,
    #     regridded=False,
    #     outliers_removed=False,
    #     computed=False,
    #     concatenated=False,
    #     region=None,
    #     reader=None,
    # )

    def __init__(
        self, input=None, var_name=None, check_unit=True, convert_unit_on_init=True, **meta
    ):

        __version__ = "0.1"
        if input is None:
            input = iris.cube.Cube([])

    @property
    def var_name(self):
        """Name of variable"""
        return self.grid.var_name

    @var_name.setter
    def var_name(self, val):
        """Name of variable"""
        if not isinstance(val, str):
            raise ValueError(f"Invalid input for var_name, need str, got {val}")
        self.grid.var_name = val
        if "var_name" in self.metadata:
            self.metadata["var_name"] = val

    @property
    def var_name_aerocom(self):
        """AeroCom variable name"""
        try:
            return const.VARS[self.var_name].var_name_aerocom
        except VariableDefinitionError:
            return None

    @property
    def var_info(self):
        """Print information about variable"""
        if self.var_name in const.VARS:
            return const.VARS[self.var_name]
        var_name = self.var_name_aerocom
        if var_name in const.VARS:
            return const.VARS[var_name]
        else:
            raise VariableDefinitionError(
                f"No default access available for variable {self.var_name}"
            )

    @property
    def ts_type(self):
        """
        Temporal resolution of data
        """
        if self.metadata["ts_type"] == "undefined":
            logger.warning("ts_type is not set in PointCloudData, trying to infer.")
            self.infer_ts_type()

        return self.metadata["ts_type"]

    @property
    def vert_code(self):
        """
        Vertical code of data (e.g. Column, Surface, ModelLevel)
        """
        return self.metadata["vert_code"]

    @property
    def standard_name(self):
        """
        Standard name of variable
        """
        return self.grid.standard_name

    @property
    def long_name(self):
        """Long name of variable"""
        return self.grid.long_name

    @long_name.setter
    def long_name(self, val):
        self.grid.long_name = val

    @property
    def unit_ok(self):
        """Boolean specifying if variable unit is AeroCom default"""
        return self.check_unit()

    @property
    def metadata(self):
        return self.cube.attributes

    @property
    def data_revision(self):
        """Revision string from file Revision.txt in the main data directory"""
        if self.from_files:
            data_dir = os.path.dirname(self.from_files[0])
            revision_file = os.path.join(data_dir, const.REVISION_FILE)
            if os.path.isfile(revision_file):
                with open(revision_file) as in_file:
                    revision = in_file.readline().strip()
                    in_file.close()

                return revision
        return "n/a"

    @property
    def reader(self):
        """ """
        return self._reader

    @reader.setter
    def reader(self, val):
        ...

    @property
    def concatenated(self):
        return self.metadata["concatenated"]

    @property
    def computed(self):
        return self.metadata["computed"]

    @property
    def units(self):
        """Unit of data"""
        return self.grid.units

    @units.setter
    def units(self, val):
        self.grid.units = val

    @property
    def data(self):
        """Data array (n-dimensional numpy array)

        Note
        ----
        This is a pointer to the data object of the underlying iris.Cube
        instance and will load the data into memory. Thus, in case of large
        datasets, this may lead to a memory error
        """
        return self.grid.data
