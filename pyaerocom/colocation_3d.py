"""
Methods and / or classes to perform colocation
"""
import logging
import os

import numpy as np
import pandas as pd
import xarray as xr
from geonum.atmosphere import pressure

from pyaerocom import __version__ as pya_ver
from pyaerocom import const
from pyaerocom.colocateddata import ColocatedData
from pyaerocom.exceptions import (
    DataUnitError,
    DimensionOrderError,
    MetaDataError,
    TemporalResolutionError,
    TimeMatchError,
    VariableDefinitionError,
    VarNotAvailableError,
)
from pyaerocom.filter import Filter
from pyaerocom.helpers import (
    get_lowest_resolution,
    isnumeric,
    make_datetime_index,
    to_pandas_timestamp,
)
from pyaerocom.time_resampler import TimeResampler
from pyaerocom.tstype import TsType
from pyaerocom.variable import Variable

logger = logging.getLogger(__name__)


def colocate_vertical_profile_gridded(
    data,
    data_ref,
    ts_type=None,
    start=None,
    stop=None,
    filter_name=None,
    regrid_res_deg=None,
    harmonise_units=True,
    regrid_scheme="areaweighted",
    var_ref=None,
    update_baseyear_gridded=None,
    min_num_obs=None,
    colocate_time=False,
    use_climatology_ref=False,
    resample_how=None,
    **kwargs,
):
    breakpoint()
