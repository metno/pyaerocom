import logging
import os
import warnings
from ast import literal_eval
from pathlib import Path

import numpy as np
import pandas as pd
import xarray

from pyaerocom import const
from pyaerocom.colocateddata import ColocatedData
from pyaerocom.exceptions import (
    CoordinateError,
    DataCoverageError,
    DataDimensionError,
    DataSourceError,
    MetaDataError,
    NetcdfError,
    UnknownRegion,
    VarNotAvailableError,
)
from pyaerocom.geodesy import get_country_info_coords
from pyaerocom.helpers import to_datestring_YYYYMMDD
from pyaerocom.helpers_landsea_masks import get_mask_value, load_region_mask_xr
from pyaerocom.mathutils import calc_statistics
from pyaerocom.plot.plotscatter import plot_scatter
from pyaerocom.region import Region
from pyaerocom.region_defs import REGION_DEFS
from pyaerocom.time_resampler import TimeResampler

logger = logging.getLogger(__name__)


class ColocatedData3D(ColocatedData):
    """Class representing 3d colocated data which will be used for vertical profiles"""

    def __init__(self, data=None, **kwargs):
        super().__init__(data, **kwargs)

    @property
    def altitude(self):
        """Array of altitude coordinates"""
        if not "altitude" in self.data.coords:
            raise AttributeError("ColocatedData#D does not include altitutde coordinate")
        return self.data.altitude

    @property
    def alt_range(self):
        """Altitude range covered by this data object"""
        alts = self.altitude.values
        return (np.nanmin(alts), np.nanmax(alts))
