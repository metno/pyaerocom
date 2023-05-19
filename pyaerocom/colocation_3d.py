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

from pyaerocom.colocation import _resolve_var_name

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
    
    """
    TODO: Fill in docstring
    """
    if filter_name is None:
        filter_name = const.DEFAULT_REG_FILTER
    try:
        data.check_dimcoords_tseries()
    except DimensionOrderError:
        data.reorder_dimensions_tseries()

    var, var_aerocom = _resolve_var_name(data)
    if var_ref is None:
        var_ref = var_aerocom
        var_ref_aerocom = var_aerocom
    else:
        var_ref_aerocom = const.VARS[var_ref].var_name_aerocom

    if not var_ref in data_ref.contains_vars:
        raise VarNotAvailableError(
            f"Variable {var_ref} is not available in ungridded "
            f"data (which contains {data_ref.contains_vars})"
        )
    elif len(data_ref.contains_datasets) > 1:
        raise AttributeError(
            f"Colocation can only be performed with ungridded data objects "
            f"that only contain a single dataset (input data contains: "
            f"{data_ref.contains_datasets}. Use method `extract_dataset` of "
            f"UngriddedData object to extract single datasets."
        )

    dataset_ref = data_ref.contains_datasets[0]

    if update_baseyear_gridded is not None:
        # update time dimension in gridded data
        data.base_year = update_baseyear_gridded

    # apply region filter to data
    regfilter = Filter(name=filter_name)
    data_ref = regfilter.apply(data_ref)
    data = regfilter.apply(data)

    # check time overlap and crop model data if needed
    start, stop = _check_time_ival(data, start, stop)
    data = data.crop(time_range=(start, stop))

    if regrid_res_deg is not None:
        data = _regrid_gridded(data, regrid_scheme, regrid_res_deg)

    # Special ts_typs for which all stations with ts_type< are removed
    reduce_station_data_ts_type = ts_type

    ts_type_src_data = data.ts_type
    ts_type, ts_type_data = _check_ts_type(data, ts_type)
    if not colocate_time and ts_type < ts_type_data:
        data = data.resample_time(str(ts_type), min_num_obs=min_num_obs, how=resample_how)
        ts_type_data = ts_type

    if use_climatology_ref:
        col_freq = "monthly"
        obs_start = const.CLIM_START
        obs_stop = const.CLIM_STOP
    else:
        col_freq = str(ts_type)
        obs_start = start
        obs_stop = stop

    # colocation frequency
    col_tst = TsType(col_freq)

    latitude = data.latitude.points
    longitude = data.longitude.points
    lat_range = [np.min(latitude), np.max(latitude)]
    lon_range = [np.min(longitude), np.max(longitude)]
    # use only sites that are within model domain
    
    # LB: filter_by_meta wipes is_vertical_profile
    data_ref = data_ref.filter_by_meta(latitude=lat_range, longitude=lon_range)

    # get timeseries from all stations in provided time resolution
    # (time resampling is done below in main loop)
    all_stats = data_ref.to_station_data_all(
        vars_to_convert=var_ref,
        start=obs_start,
        stop=obs_stop,
        by_station_name=True,
        ts_type_preferred=reduce_station_data_ts_type,
        **kwargs,
    )

    obs_stat_data = all_stats["stats"]
    ungridded_lons = all_stats["longitude"]
    ungridded_lats = all_stats["latitude"]

    if len(obs_stat_data) == 0:
        raise VarNotAvailableError(
            f"Variable {var_ref} is not available in specified time interval ({start}-{stop})"
        )

    grid_stat_data = data.to_time_series(longitude=ungridded_lons, latitude=ungridded_lats)

    pd_freq = col_tst.to_pandas_freq()
    time_idx = make_datetime_index(start, stop, pd_freq)

    time_num = len(time_idx)
    stat_num = len(obs_stat_data)

    arr = np.full((2, time_num, stat_num), np.nan)

    lons = [np.nan] * stat_num
    lats = [np.nan] * stat_num
    alts = [np.nan] * stat_num
    station_names = [""] * stat_num

    data_ref_unit = None
    ts_type_src_ref = None
    if not harmonise_units:
        data_unit = str(data.units)
    else:
        data_unit = None

    return
