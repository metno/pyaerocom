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
from pyaerocom._lowlevel_helpers import RegridResDeg
from pyaerocom.climatology_config import ClimatologyConfig
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
from pyaerocom.griddeddata import GriddedData
from pyaerocom.ungridded_data_container import UngriddedDataContainer
from pyaerocom.units.datetime import get_lowest_resolution, to_pandas_timestamp
from pyaerocom.helpers import (
    isnumeric,
    make_datetime_index,
)
from pyaerocom.time_resampler import TimeResampler
from pyaerocom.units.datetime import TsType
from pyaerocom.units.helpers import get_standard_unit

from .colocated_data import ColocatedData

logger = logging.getLogger(__name__)


def resolve_var_name(data: GriddedData) -> tuple[str, str]:
    """
    Check variable name of `GriddedData` against AeroCom default

    Checks whether the variable name set in the data corresponds to the
    AeroCom variable name, or whether it is an alias. Returns both the
    variable name set and the AeroCom variable name.

    Parameters
    ----------
    data : GriddedData
        Data to be checked.

    Returns
    -------
    str
        variable name as set in data (may be alias, but may also be AeroCom
        variable name, in which case first and second return parameter are the
        same).
    str
        corresponding AeroCom variable name

    """

    var = data.var_name
    try:
        vardef = const.VARS[var]
    except VariableDefinitionError:
        vardef = data.register_var_glob()

    return (var, vardef.var_name_aerocom)


def _regrid_gridded(gridded, regrid_scheme: str, regrid_res_deg: RegridResDeg):
    """
    Regrid instance of `GriddedData`

    Makes sure to handle different input options for `regrid_res_deg`.

    Parameters
    ----------
    gridded : GriddedData
        instance of :class:`GriddedData` that is supposed to be regridded.
    regrid_scheme : str
        iris scheme used for regridding (defaults to area weighted regridding)
    regrid_res_deg : int or dict, optional
        regrid resolution in degrees. If specified, the input gridded data
        objects will be regridded in lon / lat dimension to the input
        resolution (if input is integer, both lat and lon are regridded to that
        resolution, if input is dict, use keys `lat_res_deg` and `lon_res_deg`
        to specify regrid resolutions, respectively).

    Raises
    ------
    ValueError
        If input for `regrid_res_deg` is invalid.

    Returns
    -------
    GriddedData
        regridded data object

    """
    if not isinstance(regrid_res_deg, dict):  # at runtime RegridResDeg is a dict
        if not isnumeric(regrid_res_deg):
            raise ValueError(
                "Invalid input for regrid_res_deg. Need integer or dict specifying lat and lon res"
            )
        regrid_res_deg = dict(lat_res_deg=regrid_res_deg, lon_res_deg=regrid_res_deg)

    return gridded.regrid(scheme=regrid_scheme, **regrid_res_deg)


def _ensure_gridded_gridded_same_freq(data, data_ref, min_num_obs, resample_how):
    """
    Make sure 2 input gridded data objects are in the same frequency

    Checks if both input data objects are in the same frequency, and if not,
    downsample the one with higher frequency accordingly.

    Parameters
    ----------
    data : GriddedData
        first data object.
    data_ref : GriddedData
        second data object.
    min_num_obs : int or dict, optional
        Minimum number of observations for resampling.
    resample_how : str or dict, optional
        Resampling aggregators used.

    Returns
    -------
    GriddedData
        first data object.
    GriddedData
        second data object.
    str
        sampling frequency of both data objects.

    """
    ts_type_data = data.ts_type
    ts_type_data_ref = data_ref.ts_type
    if ts_type_data != ts_type_data_ref:
        # ref data is in higher resolution
        if TsType(ts_type_data_ref) > TsType(ts_type_data):
            data_ref = data_ref.resample_time(
                ts_type_data, min_num_obs=min_num_obs, how=resample_how
            )
        else:
            data = data.resample_time(ts_type_data_ref, min_num_obs=min_num_obs, how=resample_how)
    return data, data_ref, data.ts_type


def colocate_gridded_gridded(
    data,
    data_ref,
    ts_type=None,
    start=None,
    stop=None,
    filter_name=None,
    regrid_res_deg: float | RegridResDeg | None = None,
    harmonise_units=True,
    regrid_scheme: str = "areaweighted",
    update_baseyear_gridded=None,
    min_num_obs=None,
    colocate_time=False,
    resample_how=None,
    **kwargs,
):
    """Colocate 2 gridded data objects

    TODO
    ----
    - think about vertical dimension (vert_scheme input not used at the moment)

    Parameters
    ----------
    data : GriddedData
        gridded data (e.g. model results)
    data_ref : GriddedData
        reference data (e.g. gridded satellite object) that is co-located with
        `data`.
        observation data or other model)
    ts_type : str, optional
        desired temporal resolution of output colocated data (e.g. "monthly").
        Defaults to None, in which case the highest possible resolution is
        used.
    start : str or datetime64 or similar, optional
        start time for colocation, if None, the start time of the input
        :class:`GriddedData` object is used
    stop : str or datetime64 or similar, optional
        stop time for colocation, if None, the stop time of the input
        :class:`GriddedData` object is used
    filter_name : str, optional
        string specifying filter used (cf. :class:`pyaerocom.filter.Filter` for
        details). If None, then it is set to 'ALL-wMOUNTAINS', which
        corresponds to no filtering (world with mountains).
        Use ALL-noMOUNTAINS to exclude mountain sites.
    regrid_res_deg : int or dict, optional
        regrid resolution in degrees. If specified, the input gridded data
        objects will be regridded in lon / lat dimension to the input
        resolution (if input is integer, both lat and lon are regridded to that
        resolution, if input is dict, use keys `lat_res_deg` and `lon_res_deg`
        to specify regrid resolutions, respectively).
    harmonise_units : bool
        if True, units are attempted to be harmonised (note: raises Exception
        if True and units cannot be harmonised). Defaults to True.
    regrid_scheme : str
        iris scheme used for regridding (defaults to area weighted regridding)
    update_baseyear_gridded : int, optional
        optional input that can be set in order to redefine the time dimension
        in the first gridded data object `data`to be analysed. E.g., if the
        data object is a climatology (one year of data) that has set the base
        year of the time dimension to a value other than the specified input
        start / stop time this may be used to update the time in order to make
        co-location possible.
    min_num_obs : int or dict, optional
        minimum number of observations for resampling of time
    colocate_time : bool
        if True and if original time resolution of data is higher than desired
        time resolution (`ts_type`), then both datasets are colocated in time
        *before* resampling to lower resolution.
    resample_how : str or dict
        string specifying how data should be aggregated when resampling in time.
        Default is "mean". Can also be a nested dictionary, e.g.
        resample_how={'daily': {'hourly' : 'max'}} would use the maximum value
        to aggregate from hourly to daily, rather than the mean.
    **kwargs
        additional keyword args (not used here, but included such that factory
        class can handle different methods with different inputs)

    Returns
    -------
    ColocatedData
        instance of colocated data

    """
    if filter_name is None:
        filter_name = const.DEFAULT_REG_FILTER

    if harmonise_units:
        if not data.units == data_ref.units:
            try:
                data_ref.convert_unit(data.units)
            except Exception:
                raise DataUnitError(
                    f"Failed to merge data unit of reference gridded data object ({data.units}) "
                    f"to data unit of gridded data object ({data_ref.units})"
                )

    if update_baseyear_gridded is not None:
        # update time dimension in gridded data
        data.base_year = update_baseyear_gridded

    if regrid_res_deg is not None:
        data_ref = _regrid_gridded(data_ref, regrid_scheme, regrid_res_deg)
    # perform regridding
    if data.lon_res < data_ref.lon_res:  # obs has lower resolution
        data = data.regrid(data_ref, scheme=regrid_scheme)
    else:
        data_ref = data_ref.regrid(data, scheme=regrid_scheme)

    ts_type_src = [data_ref.ts_type, data.ts_type]
    # time resolution of dataset to be analysed
    data, data_ref, data_ts_type = _ensure_gridded_gridded_same_freq(
        data, data_ref, min_num_obs, resample_how
    )
    # now both are in same temporal resolution

    # input ts_type is not specified or model is in lower resolution
    # than input ts_type -> use model frequency to colocate
    if ts_type is None or TsType(data_ts_type) < TsType(ts_type):
        ts_type = data_ts_type

    # 1. match model data with potential input start / stop and update if
    # applicable
    start, stop = check_time_ival(data, start, stop)
    # 2. narrow it down with obsdata availability, if applicable
    start, stop = check_time_ival(data_ref, start, stop)

    data = data.crop(time_range=(start, stop))
    data_ref = data_ref.crop(time_range=(start, stop))

    # perform region extraction (if applicable)
    regfilter = Filter(name=filter_name)
    data = regfilter(data)
    data_ref = regfilter(data_ref)

    files_ref = [os.path.basename(x) for x in data_ref.from_files]
    files = [os.path.basename(x) for x in data.from_files]

    var, var_aerocom = resolve_var_name(data)
    var_ref, var_ref_aerocom = resolve_var_name(data_ref)
    meta = {
        "data_source": [data_ref.data_id, data.data_id],
        "var_name": [var_ref_aerocom, var_aerocom],
        "var_name_input": [var_ref, var],
        "ts_type": data_ts_type,
        "filter_name": filter_name,
        "ts_type_src": ts_type_src,
        "var_units": [str(data_ref.units), str(data.units)],
        "data_level": 3,
        "revision_ref": data_ref.data_revision,
        "from_files": files,
        "from_files_ref": files_ref,
        "colocate_time": colocate_time,
        "obs_is_clim": False,
        "pyaerocom": pya_ver,
        "min_num_obs": min_num_obs,
        "resample_how": resample_how,
    }

    data_np = data.grid.data
    if isinstance(data_np, np.ma.core.MaskedArray):
        data_np = data_np.filled(np.nan)
    data_ref_np = data_ref.grid.data
    if isinstance(data_ref_np, np.ma.core.MaskedArray):
        data_ref_np = data_ref_np.filled(np.nan)
    arr = np.asarray((data_ref_np, data_np))
    time = data.time_stamps().astype("datetime64[ns]")
    lats = data.latitude.points
    lons = data.longitude.points

    # create coordinates of DataArray
    coords = {
        "data_source": meta["data_source"],
        "time": time,
        "latitude": lats,
        "longitude": lons,
    }

    dims = ["data_source", "time", "latitude", "longitude"]

    coldata = ColocatedData(data=arr, coords=coords, dims=dims, name=data.var_name, attrs=meta)

    # add correct units for lat / lon dimensions
    coldata.latitude.attrs["standard_name"] = data.latitude.standard_name
    coldata.latitude.attrs["units"] = str(data.latitude.units)

    coldata.longitude.attrs["standard_name"] = data.longitude.standard_name
    coldata.longitude.attrs["units"] = str(data.longitude.units)

    if data_ts_type != ts_type:
        coldata = coldata.resample_time(
            to_ts_type=ts_type,
            colocate_time=colocate_time,
            min_num_obs=min_num_obs,
            how=resample_how,
            **kwargs,
        )
    return coldata


def check_time_ival(data, start, stop):
    # get start / stop of gridded data as pandas.Timestamp
    data_start = to_pandas_timestamp(data.start)
    data_stop = to_pandas_timestamp(data.stop)

    if start is None:
        start = data_start
    else:
        start = to_pandas_timestamp(start)
    if stop is None:
        stop = data_stop
    else:
        stop = to_pandas_timestamp(stop)

    if start < data_start:
        start = data_start
    if stop > data_stop:
        stop = data_stop
    # check overlap
    if stop < data_start or start > data_stop:
        raise TimeMatchError(
            f"Input time range {start}-{stop} does not overlap with data "
            f"range: {data_start}-{data_stop}"
        )
    return start, stop


def check_ts_type(data, ts_type):
    ts_type_data = TsType(data.ts_type)
    if ts_type is None:
        ts_type = ts_type_data
    elif isinstance(ts_type, str):
        ts_type = TsType(ts_type)
    if ts_type > ts_type_data:
        # desired output frequency ts_type is higher resolution than frequency
        # of data (e.g. desired output is hourly but data is daily, update
        # output ts_type)
        ts_type = ts_type_data
    return ts_type, ts_type_data


def _colocate_site_data_helper(
    stat_data,
    stat_data_ref,
    var,
    var_ref,
    ts_type,
    resample_how,
    min_num_obs,
    use_climatology_ref,
):
    """
    Helper method that colocates two timeseries from 2 StationData objects

    Used in main loop of :func:`colocate_gridded_ungridded`

    Parameters
    ----------
    stat_data : StationData
        first data object (usually the one that is to be compared with obs)
    stat_data_ref : StationData
        second data object (usually obs)
    var : str
        variable to be used from `stat_data`
    var_ref : str
        variable to be used from `stat_data_ref`
    ts_type : str
        output frequency
    resample_how : str or dict
        string specifying how data should be aggregated when resampling in time.
        Default is "mean". Can also be a nested dictionary, e.g.
        resample_how={'daily': {'hourly' : 'max'}} would use the maximum value
        to aggregate from hourly to daily, rather than the mean.
    min_num_obs : int or dict, optional
        minimum number of observations for resampling of time
    use_climatology_ref : ClimateConfig | bool, optional
        If provided, the climatology will be calculated from the config


    Raises
    ------
    TemporalResolutionError
        if obs sampling frequency is lower than desired output frequency

    Returns
    -------
    pandas.DataFrame
        dataframe containing the colocated input data (column names are
        data and ref)
    """

    # get grid and obs timeseries data (that may be sampled in arbitrary
    # time resolution, particularly the obs data)
    grid_ts = stat_data.resample_time(
        var, ts_type=ts_type, how=resample_how, min_num_obs=min_num_obs, inplace=True
    )[var]

    if isinstance(use_climatology_ref, ClimatologyConfig):
        obs_ts = stat_data_ref.calc_climatology(
            var_ref,
            start=use_climatology_ref.start,
            stop=use_climatology_ref.stop,
            min_num_obs=min_num_obs,
            clim_mincount=use_climatology_ref.min_count,
            resample_how=use_climatology_ref.resample_how,
            clim_freq=use_climatology_ref.freq,
            set_year=use_climatology_ref.set_year,
        )[var_ref]
    else:
        obs_ts = stat_data_ref.resample_time(
            var_ref,
            ts_type=ts_type,
            how=resample_how,
            min_num_obs=min_num_obs,
            inplace=True,
        )[var_ref]

    # fill up missing time stamps
    return pd.concat([obs_ts, grid_ts], axis=1, keys=["ref", "data"])


def _colocate_site_data_helper_timecol(
    stat_data,
    stat_data_ref,
    var,
    var_ref,
    ts_type,
    resample_how,
    min_num_obs,
    use_climatology_ref,
):
    """
    Helper method that colocates two timeseries from 2 StationData objects

    Other than :func:`_colocate_site_data_helper` this method applies time
    colocation in highest possible resolution (used if option `colocate_time`
    is active in colocation routine :func:`colocate_gridded_ungridded`).

    Used in main loop of :func:`colocate_gridded_ungridded`

    Parameters
    ----------
    stat_data : StationData
        first data object (usually the one that is to be compared with obs)
    stat_data_ref : StationData
        second data object (usually obs)
    var : str
        variable to be used from `stat_data`
    var_ref : str
        variable to be used from `stat_data_ref`
    ts_type : str
        output frequency
    resample_how : str or dict
        string specifying how data should be aggregated when resampling in time.
        Default is "mean". Can also be a nested dictionary, e.g.
        resample_how={'daily': {'hourly' : 'max'}} would use the maximum value
        to aggregate from hourly to daily, rather than the mean.
    min_num_obs : int or dict, optional
        minimum number of observations for resampling of time
    use_climatology_ref: ClimateConfig | bool
        if provided, NotImplementedError is raised

    Raises
    ------
    TemporalResolutionError
        if model or obs sampling frequency is lower than desired output frequency
    NotImplementedError
        if input arg `use_climatology_ref` is provided.

    Returns
    -------
    pandas.DataFrame
        dataframe containing the colocated input data (column names are
        data and ref)
    """
    if isinstance(use_climatology_ref, ClimatologyConfig):
        raise NotImplementedError(
            "Using observation climatology in colocation with option colocate_time is not available yet"
        )

    grid_tst = stat_data.get_var_ts_type(var)
    obs_tst = stat_data_ref.get_var_ts_type(var_ref)
    coltst = TsType(get_lowest_resolution(grid_tst, obs_tst))
    # =============================================================================
    #     if coltst.mulfac != 1:
    #         coltst = coltst.next_lower
    # =============================================================================

    stat_data.resample_time(
        var_name=var,
        ts_type=str(coltst),
        how=resample_how,
        min_num_obs=min_num_obs,
        inplace=True,
    )

    stat_data_ref.resample_time(
        var_name=var_ref,
        ts_type=str(coltst),
        how=resample_how,
        min_num_obs=min_num_obs,
        inplace=True,
    )

    # Save time indices of the observations and a mask of where it is NaN
    obs_idx = stat_data_ref[var_ref].index
    obs_isnan = stat_data_ref[var_ref].isnull()

    # now both StationData objects are in the same resolution, but they still
    # might have gaps in their time axis, thus concatenate them in a DataFrame,
    # which will merge the time index
    merged = pd.concat([stat_data_ref[var_ref], stat_data[var]], axis=1, keys=["ref", "data"])
    # Interpolate the model to the times of the observations
    # (for non-standard coltst it could be that 'resample_time'
    # has placed the model and observations at different time stamps)
    merged = merged.interpolate("index").reindex(obs_idx).loc[obs_idx]
    # Set to NaN at times when observations were NaN originally
    # (because the interpolation will interpolate the 'ref' column as well)
    merged.loc[obs_isnan] = np.nan
    # due to interpolation some model values may be NaN, where there is obs
    merged.loc[merged.data.isnull()] = np.nan
    # Ensure the whole timespan of the model is kept in "merged"
    stat_data[var].name = "tmp"
    merged = pd.concat([merged, stat_data[var]], axis=1)
    merged = merged[["ref", "data"]]

    grid_ts = merged["data"]
    obs_ts = merged["ref"]
    # invalidate model where obs is NaN (NB: maybe not needed any more?)
    obsnan = np.isnan(obs_ts.values)
    grid_ts[obsnan] = np.nan

    # now resample both to output frequency
    resampler = TimeResampler()
    obs_ts = resampler.resample(
        to_ts_type=ts_type,
        input_data=obs_ts,
        from_ts_type=coltst,
        how=resample_how,
        min_num_obs=min_num_obs,
    )

    grid_ts = resampler.resample(
        to_ts_type=ts_type,
        input_data=grid_ts,
        from_ts_type=coltst,
        how=resample_how,
        min_num_obs=min_num_obs,
    )
    # fill up missing time stamps
    return pd.concat([obs_ts, grid_ts], axis=1, keys=["ref", "data"])


def colocate_gridded_ungridded(
    data: GriddedData,
    data_ref: UngriddedDataContainer,
    ts_type=None,
    start=None,
    stop=None,
    filter_name=None,
    regrid_res_deg: float | RegridResDeg | None = None,
    harmonise_units=True,
    regrid_scheme: str = "areaweighted",
    var_ref=None,
    update_baseyear_gridded=None,
    min_num_obs=None,
    colocate_time=False,
    use_climatology_ref=False,
    resample_how=None,
    **kwargs,
):
    """Colocate gridded with ungridded data (low level method)

    For high-level colocation see :class:`pyaerocom.colocation.Colocator`
    and :class:`pyaerocom.ColocationSetup`

    Note
    ----
    Uses the variable that is contained in input :class:`GriddedData` object
    (since these objects only contain a single variable). If this variable
    is not contained in observation data (or contained but using a different
    variable name) you may specify the obs variable to be used via input arg
    `var_ref`

    Parameters
    ----------
    data : GriddedData
        gridded data object (e.g. model results).
    data_ref : UngriddedDataContainer
        ungridded data object (e.g. observations).
    ts_type : str
        desired temporal resolution of colocated data (must be valid AeroCom
        ts_type str such as daily, monthly, yearly.).
    start : :obj:`str` or :obj:`datetime64` or similar, optional
        start time for colocation, if None, the start time of the input
        :class:`GriddedData` object is used.
    stop : :obj:`str` or :obj:`datetime64` or similar, optional
        stop time for colocation, if None, the stop time of the input
        :class:`GriddedData` object is used
    filter_name : str
        string specifying filter used (cf. :class:`pyaerocom.filter.Filter` for
        details). If None, then it is set to 'ALL-wMOUNTAINS', which
        corresponds to no filtering (world with mountains).
        Use ALL-noMOUNTAINS to exclude mountain sites.
    regrid_res_deg : int or dict, optional
        regrid resolution in degrees. If specified, the input gridded data
        object will be regridded in lon / lat dimension to the input
        resolution (if input is integer, both lat and lon are regridded to that
        resolution, if input is dict, use keys `lat_res_deg` and `lon_res_deg`
        to specify regrid resolutions, respectively).
    harmonise_units : bool
        if True, units are attempted to be harmonised (note: raises Exception
        if True and units cannot be harmonised).
    var_ref : :obj:`str`, optional
        variable against which data in arg `data` is supposed to be compared.
        If None, then the same variable is used (i.e. `data.var_name`).
    update_baseyear_gridded : int, optional
        optional input that can be set in order to re-define the time dimension
        in the gridded data object to be analysed. E.g., if the data object
        is a climatology (one year of data) that has set the base year of the
        time dimension to a value other than the specified input start / stop
        time this may be used to update the time in order to make colocation
        possible.
    min_num_obs : int or dict, optional
        minimum number of observations for resampling of time
    colocate_time : bool
        if True and if original time resolution of data is higher than desired
        time resolution (`ts_type`), then both datasets are colocated in time
        *before* resampling to lower resolution.
    use_climatology_ref : ClimateConfig | bool, optional.
        Configuration for calculating the climatology. If set to a bool, this will not be done
    resample_how : str or dict
        string specifying how data should be aggregated when resampling in time.
        Default is "mean". Can also be a nested dictionary, e.g.
        resample_how={'daily': {'hourly' : 'max'}} would use the maximum value
        to aggregate from hourly to daily, rather than the mean.
    **kwargs
        additional keyword args (passed to
        :func:`UngriddedData.to_station_data_all`)

    Returns
    -------
    ColocatedData
        instance of colocated data

    Raises
    ------
    VarNotAvailableError
        if grid data variable is not available in ungridded data object
    AttributeError
        if instance of input :class:`UngriddedDataContainer` object contains more than
        one dataset
    TimeMatchError
        if gridded data time range does not overlap with input time range
    ColocationError
        if none of the data points in input :class:`UngriddedDataContainer` matches
        the input colocation constraints
    """
    if filter_name is None:
        filter_name = const.DEFAULT_REG_FILTER
    if data.proj_info is None:
        # reordering only implemented if no projection
        try:
            data.check_dimcoords_tseries()
        except DimensionOrderError:
            data.reorder_dimensions_tseries()

    var, var_aerocom = resolve_var_name(data)
    if var_ref is None:
        var_ref = var_aerocom
        var_ref_aerocom = var_aerocom
    else:
        var_ref_aerocom = const.VARS[var_ref].var_name_aerocom

    if var_ref not in data_ref.contains_vars:
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
    start, stop = check_time_ival(data, start, stop)
    data = data.crop(time_range=(start, stop))

    if regrid_res_deg is not None:
        data = _regrid_gridded(data, regrid_scheme, regrid_res_deg)

    # Special ts_typs for which all stations with ts_type< are removed
    reduce_station_data_ts_type = ts_type

    ts_type_src_data = data.ts_type
    ts_type, ts_type_data = check_ts_type(data, ts_type)
    if not colocate_time and ts_type < ts_type_data:
        data = data.resample_time(str(ts_type), min_num_obs=min_num_obs, how=resample_how)
        ts_type_data = ts_type

    if isinstance(use_climatology_ref, ClimatologyConfig):  # pragma: no cover
        col_freq = use_climatology_ref.freq
        obs_start = use_climatology_ref.start
        obs_stop = use_climatology_ref.stop
    else:
        col_freq = str(ts_type)
        obs_start = start
        obs_stop = stop

    # colocation frequency
    col_tst = TsType(col_freq)

    latitude = data.latitude.points
    longitude = data.longitude.points
    if data.proj_info is None:
        lat_range = [np.min(latitude), np.max(latitude)]
        lon_range = [np.min(longitude), np.max(longitude)]
        # use only sites that are within model domain

        # filter_by_meta wipes is_vertical_profile
        data_ref = data_ref.filter_by_meta(latitude=lat_range, longitude=lon_range)
    else:
        # gridded data with projection,
        # add x/y information to ungridded
        for coord in data.cube.dim_coords:
            if coord.var_name == data.proj_info.x_axis:
                vals = coord.points
                xrange = (np.min(vals), np.max(vals))
            if coord.var_name == data.proj_info.y_axis:
                vals = coord.points
                yrange = (np.min(vals), np.max(vals))
        if xrange is None or yrange is None:
            raise VariableDefinitionError(
                f"x/y axis not found in cube: {data.proj_info.x_axis}, {data.proj_info.y_axis}"
            )
        data_ref = data_ref.filter_by_projection(data.proj_info.to_proj, xrange, yrange)

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

    # to read
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
    station_types = [""] * stat_num

    data_ref_unit = None
    ts_type_src_ref = None
    if not harmonise_units:
        data_unit = str(data.units)
    else:
        data_unit = None
    # loop over all stations and append to colocated data object
    for i, obs_stat in enumerate(obs_stat_data):
        # Add coordinates to arrays required for xarray.DataArray below
        lons[i] = obs_stat.longitude
        lats[i] = obs_stat.latitude
        alts[i] = obs_stat.altitude
        station_names[i] = obs_stat.station_name
        station_types[i] = getattr(obs_stat, "station_type", "")

        # ToDo: consider removing to keep ts_type_src_ref (this was probably
        # introduced for EBAS were the original data frequency is not constant
        # but can vary from site to site)
        if ts_type_src_ref is None:
            ts_type_src_ref = obs_stat["ts_type_src"]
        elif obs_stat["ts_type_src"] != ts_type_src_ref:
            spl = ts_type_src_ref.split(";")
            if obs_stat["ts_type_src"] not in spl:
                spl.append(obs_stat["ts_type_src"])
            ts_type_src_ref = ";".join(spl)

        if data_ref_unit is None:
            try:
                data_ref_unit = obs_stat["var_info"][var_ref]["units"]
            except KeyError as e:  # variable information or unit is not defined
                logger.exception(repr(e))
        try:
            unit = obs_stat["var_info"][var_ref]["units"]
        except Exception:
            unit = None
        if not unit == data_ref_unit:
            raise ValueError(
                f"Cannot perform colocation. "
                f"Ungridded data object contains different units ({var_ref})"
            )
        # get observations (Note: the index of the observation time series
        # is already in the specified frequency format, and thus, does not
        # need to be updated, for details (or if errors occur), cf.
        # UngriddedData.to_station_data, where the conversion happens)

        # get model station data
        grid_stat = grid_stat_data[i]
        if harmonise_units:
            grid_unit = grid_stat.get_unit(var)
            to_unit = get_standard_unit(var_ref)
            if not grid_unit == to_unit:
                grid_stat.convert_unit(var, to_unit)
            if data_unit is None:
                data_unit = to_unit

        try:
            if colocate_time:
                _df = _colocate_site_data_helper_timecol(
                    stat_data=grid_stat,
                    stat_data_ref=obs_stat,
                    var=var,
                    var_ref=var_ref,
                    ts_type=col_freq,
                    resample_how=resample_how,
                    min_num_obs=min_num_obs,
                    use_climatology_ref=use_climatology_ref,
                )
            else:
                _df = _colocate_site_data_helper(
                    stat_data=grid_stat,
                    stat_data_ref=obs_stat,
                    var=var,
                    var_ref=var_ref,
                    ts_type=col_freq,
                    resample_how=resample_how,
                    min_num_obs=min_num_obs,
                    use_climatology_ref=use_climatology_ref,
                )

            # this try/except block was introduced on 23/2/2021 as temporary fix from
            # v0.10.0 -> v0.10.1 as a result of multi-weekly obsdata (EBAS) that
            # can end up resulting in incorrect number of timestamps after resampling
            # (the error was discovered using EBASMC, concpm10, 2019 and colocation
            # frequency monthly)
            try:
                # assign the unified timeseries data to the colocated data array
                arr[0, :, i] = _df["ref"].values
                arr[1, :, i] = _df["data"].values
            except ValueError:
                try:
                    mask = _df.index.intersection(time_idx)
                    _df = _df.loc[mask]
                    arr[0, :, i] = _df["ref"].values
                    arr[1, :, i] = _df["data"].values
                except ValueError as e:
                    logger.warning(
                        f"Failed to colocate time for station {obs_stat.station_name}. "
                        f"This station will be skipped (error: {e})"
                    )
        except TemporalResolutionError as e:
            # resolution of obsdata is too low
            logger.warning(
                f"{var_ref} data from site {obs_stat.station_name} will "
                f"not be added to ColocatedData. Reason: {e}"
            )
    try:
        revision = data_ref.get_data_revision(dataset_ref)
    except MetaDataError:
        revision = "MULTIPLE"
    except Exception:
        revision = "n/a"

    files = [os.path.basename(x) for x in data.from_files]

    meta = {
        "data_source": [dataset_ref, data.data_id],
        "var_name": [var_ref_aerocom, var_aerocom],
        "var_name_input": [var_ref, var],
        "ts_type": col_freq,  # will be updated below if resampling
        "filter_name": filter_name,
        "ts_type_src": [ts_type_src_ref, ts_type_src_data],
        "var_units": [data_ref_unit, data_unit],
        "data_level": 3,
        "revision_ref": revision,
        "from_files": files,
        "from_files_ref": None,
        "colocate_time": colocate_time,
        "obs_is_clim": (True if isinstance(use_climatology_ref, ClimatologyConfig) else False),
        "pyaerocom": pya_ver,
        "min_num_obs": min_num_obs,
        "resample_how": resample_how,
    }

    # create coordinates of DataArray
    coords = {
        "data_source": meta["data_source"],
        "time": time_idx,
        "station_name": station_names,
        "station_type": ("station_name", station_types),
        "latitude": ("station_name", lats),
        "longitude": ("station_name", lons),
        "altitude": ("station_name", alts),
    }

    dims = ["data_source", "time", "station_name"]
    coldata = ColocatedData(data=arr, coords=coords, dims=dims, name=var, attrs=meta)

    # add correct units for lat / lon dimensions
    coldata.latitude.attrs["standard_name"] = data.latitude.standard_name
    coldata.latitude.attrs["units"] = str(data.latitude.units)

    coldata.longitude.attrs["standard_name"] = data.longitude.standard_name
    coldata.longitude.attrs["units"] = str(data.longitude.units)

    return coldata


def correct_model_stp_coldata(coldata, p0=None, t0=273.15, inplace=False):
    """Correct modeldata in colocated data object to STP conditions

    Note
    ----
    BETA version, quite unelegant coded (at 8pm 3 weeks before IPCC deadline),
    but should do the job for 2010 monthly colocated data files (AND NOTHING
    ELSE)!

    """
    if coldata.ndim != 3:
        raise NotImplementedError("Can only handle 3D coldata so far...")
    elif not coldata.ts_type == "monthly" or not len(coldata.time) == 12:
        raise NotImplementedError(
            "Can only handle monthly colocated data files "
            "so far (since ERA5 temps are only available) "
            "in monthly resolution"
        )
    startyr = pd.Timestamp(coldata.start).year
    stopyr = pd.Timestamp(coldata.stop).year
    if not all([x == 2010 for x in (startyr, stopyr)]):
        raise NotImplementedError("Can only handle 2010 monthly data so far")

    if not inplace:
        coldata = coldata.copy()

    arr = coldata.data

    coords = zip(
        arr.latitude.values,
        arr.longitude.values,
        arr.altitude.values,
        arr.station_name.values,
    )
    if p0 is None:
        p0 = pressure()  # STD conditions sea level
    logger.info("Correcting model data in ColocatedData instance to STP")
    cfacs = []
    meantemps = []
    mintemps = []
    maxtemps = []
    ps = []
    with xr.open_dataset(const.ERA5_SURFTEMP_FILE, decode_timedelta=True)["t2m"] as temp:
        for i, (lat, lon, alt, name) in enumerate(coords):
            logger.info(name, ", Lat", lat, ", Lon", lon)
            p = pressure(alt)
            logger.info("Alt", alt)
            logger.info("P=", p / 100, "hPa")

            ps.append(p / 100)

            temps = temp.sel(latitude=lat, longitude=lon, method="nearest").data

            meantemps.append(temps.mean())
            mintemps.append(temps.min())
            maxtemps.append(temps.min())

            if not len(temps) == len(arr.time):
                raise NotImplementedError("Check timestamps")
            logger.info("Mean Temp: ", temps.mean() - t0, " C")

            corrfacs = (p0 / p) * (temps / t0)

            logger.info("Corr fac:", corrfacs.mean(), "+/-", corrfacs.std())

            cfacs.append(corrfacs.mean())

            # mularr = xr.DataArray(corrfacs)

            if not arr.station_name.values[i] == name:
                raise Exception
            elif not arr.dims[1] == "time":
                raise Exception
            arr[1, :, i] *= corrfacs

    cfacs = np.asarray(cfacs)

    logger.info("Min: ", cfacs.min())
    logger.info("Mean: ", cfacs.mean())
    logger.info("Max: ", cfacs.max())
    coldata.data.attrs["Model_STP_corr"] = True

    newcoords = dict(
        pres=("station_name", ps),
        temp_mean=("station_name", meantemps),
        temp_min=("station_name", mintemps),
        temp_max=("station_name", maxtemps),
        stp_corrfac_mean=("station_name", cfacs),
    )

    coldata.data = coldata.data.assign_coords(newcoords)

    info_str = (
        "Correction factors to convert model data from ambient to "
        "STP were computed using corrfac=(p0/p)*(T/T0) with T0=273K "
        "and p0=1013 hPa and p is the pressure at the station location "
        "(which was computed assuming a standard atmosphere and using "
        "the station altitude) and T is the 2m surface temperature at "
        "the station, applied on a monthly basis and estimated using "
        "ERA5 data"
    )

    coldata.data["pres"].attrs["units"] = "hPa"
    coldata.data["temp_mean"].attrs["units"] = "K"
    coldata.data["temp_min"].attrs["units"] = "K"
    coldata.data["temp_max"].attrs["units"] = "K"

    coldata.data.attrs["Model_STP_corr"] = True
    coldata.data.attrs["Model_STP_corr_info"] = info_str
    return coldata
