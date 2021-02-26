#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Methods and / or classes to perform colocation
"""
import numpy as np
import os
import pandas as pd
import xarray as xr
from pyaerocom import logger, const
from pyaerocom import __version__ as pya_ver

from pyaerocom.colocateddata import ColocatedData
from pyaerocom.exceptions import (ColocationError,
                                  DataUnitError,
                                  DimensionOrderError,
                                  MetaDataError,
                                  TemporalResolutionError,
                                  TimeMatchError,
                                  VarNotAvailableError)
from pyaerocom.filter import Filter
from pyaerocom.helpers import (to_pandas_timestamp,
                               to_datestring_YYYYMMDD,
                               make_datetime_index,
                               isnumeric,
                               get_lowest_resolution)
from pyaerocom.time_resampler import TimeResampler
from pyaerocom.tstype import TsType
from pyaerocom.variable import Variable

def _check_var_registered(var, aerocom_var, gridded_data):
    vars_avail = const.VARS.all_vars
    if not any([x in vars_avail for x in [var, aerocom_var]]):
        newvar = Variable(var_name=var,
                          standard_name=gridded_data.standard_name,
                          long_name=gridded_data.long_name,
                          units=gridded_data.units)

        const.VARS.add_var(newvar)

def _regrid_gridded(gridded, regrid_scheme, regrid_res_deg):
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
    if not isinstance(regrid_res_deg, dict):
        if not isnumeric(regrid_res_deg):
            raise ValueError('Invalid input for regrid_res_deg. Need integer '
                             'or dict specifying lat and lon res')
        regrid_res_deg = dict(lat_res_deg=regrid_res_deg,
                              lon_res_deg=regrid_res_deg)

    return gridded.regrid(scheme=regrid_scheme, **regrid_res_deg)

def colocate_gridded_gridded(gridded_data, gridded_data_ref, ts_type=None,
                             start=None, stop=None, filter_name=None,
                             regrid_res_deg=None, vert_scheme=None,
                             harmonise_units=True,
                             regrid_scheme='areaweighted',
                             update_baseyear_gridded=None,
                             apply_time_resampling_constraints=None,
                             min_num_obs=None,
                             colocate_time=False,
                             resample_how=None,
                             **kwargs):
    """Colocate 2 gridded data objects

    Todo
    ----
    - think about vertical dimension (vert_scheme input not used at the moment)

    Parameters
    ----------
    gridded_data : GriddedData
        gridded data (e.g. model results)
    gridded_data_ref : GriddedData
        reference dataset that is used to evaluate
        :attr:`gridded_data` (e.g. gridded observation data)
    ts_type : str
        desired temporal resolution of colocated data (must be valid AeroCom
        ts_type str such as daily, monthly, yearly..)
    start : :obj:`str` or :obj:`datetime64` or similar, optional
        start time for colocation, if None, the start time of the input
        :class:`GriddedData` object is used
    stop : :obj:`str` or :obj:`datetime64` or similar, optional
        stop time for colocation, if None, the stop time of the input
        :class:`GriddedData` object is used
    filter_name : str
        string specifying filter used (cf. :class:`pyaerocom.filter.Filter` for
        details). If None, then it is set to 'WORLD-wMOUNTAINS', which
        corresponds to no filtering (world with mountains).
        Use WORLD-noMOUNTAINS to exclude mountain sites.
    regrid_res_deg : int or dict, optional
        regrid resolution in degrees. If specified, the input gridded data
        objects will be regridded in lon / lat dimension to the input
        resolution (if input is integer, both lat and lon are regridded to that
        resolution, if input is dict, use keys `lat_res_deg` and `lon_res_deg`
        to specify regrid resolutions, respectively).
    vert_scheme : str
        string specifying scheme used to reduce the dimensionality in case
        input grid data contains vertical dimension. Example schemes are
        `mean, surface, altitude`, for details see
        :func:`GriddedData.to_time_series`.
    harmonise_units : bool
        if True, units are attempted to be harmonised (note: raises Exception
        if True and units cannot be harmonised).
    regrid_scheme : str
        iris scheme used for regridding (defaults to area weighted regridding)
    update_baseyear_gridded : int, optional
        optional input that can be set in order to redefine the time dimension
        in the gridded data object to be analysed. E.g., if the data object
        is a climatology (one year of data) that has set the base year of the
        time dimension to a value other than the specified input start / stop
        time this may be used to update the time in order to make colocation
        possible.
    apply_time_resampling_constraints : bool, optional
        if True, then time resampling constraints are applied as provided via
        :attr:`min_num_obs` or if that one is unspecified, as defined in
        :attr:`pyaerocom.const.OBS_MIN_NUM_RESAMPLE`. If None, than
        :attr:`pyaerocom.const.OBS_APPLY_TIME_RESAMPLE_CONSTRAINTS` is used
        (which defaults to True !!).
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

    if vert_scheme is not None:
        raise NotImplementedError(f'This type of colocation is not implemented '
                                  f'for gridded / gridded colocation... ({vert_scheme})')

    if filter_name is None:
        filter_name = const.DEFAULT_REG_FILTER

    if harmonise_units:
        if not gridded_data.units == gridded_data_ref.units:
            try:
                gridded_data_ref.convert_unit(gridded_data.units)
            except Exception:
                raise DataUnitError('Failed to merge data unit of reference '
                                    'gridded data object ({}) to data unit '
                                    'of gridded data object ({})'
                                    .format(gridded_data.units,
                                            gridded_data_ref.units))

    var, var_ref = gridded_data.var_name, gridded_data_ref.var_name
    aerocom_var = gridded_data.var_name_aerocom
    _check_var_registered(var, aerocom_var, gridded_data)

    if update_baseyear_gridded is not None:
        # update time dimension in gridded data
        gridded_data.base_year = update_baseyear_gridded

    if regrid_res_deg is not None:
        gridded_data_ref = _regrid_gridded(gridded_data_ref,
                                           regrid_scheme,
                                           regrid_res_deg)
    # perform regridding
    if gridded_data.lon_res < gridded_data_ref.lon_res: #obs has lower resolution
        gridded_data = gridded_data.regrid(gridded_data_ref,
                                           scheme=regrid_scheme)
    else:
        gridded_data_ref = gridded_data_ref.regrid(gridded_data,
                                                   scheme=regrid_scheme)
    # get start / stop of gridded data as pandas.Timestamp
    grid_start = to_pandas_timestamp(gridded_data.start)
    grid_stop = to_pandas_timestamp(gridded_data.stop)

    grid_start_ref = to_pandas_timestamp(gridded_data_ref.start)
    grid_stop_ref = to_pandas_timestamp(gridded_data_ref.stop)

    # time resolution of dataset to be analysed
    grid_ts_type = grid_ts_type_src = gridded_data.ts_type
    ref_ts_type = ref_ts_type_src = gridded_data_ref.ts_type
    if ref_ts_type != grid_ts_type:
        # ref data is in higher resolution
        if TsType(ref_ts_type) > TsType(grid_ts_type):

            gridded_data_ref = gridded_data_ref.resample_time(
                    grid_ts_type,
                    apply_constraints=apply_time_resampling_constraints,
                    min_num_obs=min_num_obs,
                    how=resample_how)


        else:
            gridded_data = gridded_data.resample_time(
                    ref_ts_type,
                    apply_constraints=apply_time_resampling_constraints,
                    min_num_obs=min_num_obs,
                    how=resample_how)
            grid_ts_type = ref_ts_type
    # now both are in same temporal resolution

    # input ts_type is not specified or model is in lower resolution
    # than input ts_type -> use model frequency to colocate
    if ts_type is None or TsType(grid_ts_type) < TsType(ts_type):
        ts_type = grid_ts_type

    if start is None:
        start = grid_start
    else:
        start = to_pandas_timestamp(start)
    if stop is None:
        stop = grid_stop
    else:
        stop = to_pandas_timestamp(stop)

    if grid_start_ref > start:
        start = grid_start_ref
    if grid_stop_ref < stop:
        stop = grid_stop_ref
    # check overlap
    if stop < grid_start or start > grid_stop:
        raise TimeMatchError('Input time range {}-{} does not '
                             'overlap with data range: {}-{}'
                             .format(start, stop, grid_start, grid_stop))
    gridded_data = gridded_data.crop(time_range=(start, stop))
    gridded_data_ref = gridded_data_ref.crop(time_range=(start, stop))

    # perform region extraction (if applicable)
    regfilter = Filter(name=filter_name)
    gridded_data = regfilter(gridded_data)
    gridded_data_ref = regfilter(gridded_data_ref)

    if not gridded_data.shape == gridded_data_ref.shape:
        raise ColocationError('Shape mismatch between two colocated data '
                               'arrays, please debug')
    files_ref = [os.path.basename(x) for x in gridded_data_ref.from_files]
    files = [os.path.basename(x) for x in gridded_data.from_files]


    meta = {'data_source'       :   [gridded_data_ref.data_id,
                                     gridded_data.data_id],
            'var_name'          :   [var_ref, var],
            'ts_type'           :   grid_ts_type,
            'filter_name'       :   filter_name,
            'ts_type_src'       :   [ref_ts_type_src, grid_ts_type_src],
            'start_str'         :   to_datestring_YYYYMMDD(start),
            'stop_str'          :   to_datestring_YYYYMMDD(stop),
            'var_units'         :   [str(gridded_data_ref.units),
                                     str(gridded_data.units)],
            'vert_scheme'       :   vert_scheme,
            'data_level'        :   3,
            'revision_ref'      :   gridded_data_ref.data_revision,
            'from_files'        :   files,
            'from_files_ref'    :   files_ref,
            'colocate_time'     :   colocate_time,
            'obs_is_clim'       :   False,
            'pyaerocom'         :   pya_ver,
            'apply_constraints' :   apply_time_resampling_constraints,
            'min_num_obs'       :   min_num_obs,
            'resample_how'      :   resample_how}

    meta.update(regfilter.to_dict())

    data = gridded_data.grid.data
    if isinstance(data, np.ma.core.MaskedArray):
        data = data.filled(np.nan)
    data_ref = gridded_data_ref.grid.data
    if isinstance(data_ref, np.ma.core.MaskedArray):
        data_ref = data_ref.filled(np.nan)
    arr = np.asarray((data_ref,
                      data))
    time = gridded_data.time_stamps().astype('datetime64[ns]')
    lats = gridded_data.latitude.points
    lons = gridded_data.longitude.points


    # create coordinates of DataArray
    coords = {'data_source' : meta['data_source'],
              'time'        : time,
              'latitude'    : lats,
              'longitude'   : lons}

    dims = ['data_source', 'time', 'latitude', 'longitude']

    data = ColocatedData(data=arr, coords=coords, dims=dims,
                         name=gridded_data.var_name, attrs=meta)

    # add correct units for lat / lon dimensions
    data.latitude.attrs['standard_name'] = gridded_data.latitude.standard_name
    data.latitude.attrs['units'] = str(gridded_data.latitude.units)

    data.longitude.attrs['standard_name'] = gridded_data.longitude.standard_name
    data.longitude.attrs['units'] = str(gridded_data.longitude.units)

    if grid_ts_type != ts_type:
        data = data.resample_time(to_ts_type=ts_type,
                                  colocate_time=colocate_time,
                                  apply_constraints=apply_time_resampling_constraints,
                                  min_num_obs=min_num_obs,
                                  how=resample_how,
                                  **kwargs)
    return data

def _colocate_site_data_helper(stat_data, stat_data_ref, var, var_ref,
                               ts_type, resample_how,
                               apply_time_resampling_constraints,
                               min_num_obs,
                               use_climatology_ref):
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
    apply_time_resampling_constraints : bool, optional
        if True, then time resampling constraints are applied as provided via
        :attr:`min_num_obs` or if that one is unspecified, as defined in
        :attr:`pyaerocom.const.OBS_MIN_NUM_RESAMPLE`. If None, than
        :attr:`pyaerocom.const.OBS_APPLY_TIME_RESAMPLE_CONSTRAINTS` is used
        (which defaults to True !!).
    min_num_obs : int or dict, optional
        minimum number of observations for resampling of time
    use_climatology_ref : bool
        if True, climatological timeseries are used from observations

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
                var,
                ts_type=ts_type,
                how=resample_how,
                apply_constraints=apply_time_resampling_constraints,
                min_num_obs=min_num_obs,
                inplace=True)[var]

    if use_climatology_ref:
        obs_ts = stat_data_ref.calc_climatology(
                var_ref,
                apply_constraints=apply_time_resampling_constraints,
                min_num_obs=min_num_obs)[var_ref]
    else:
        obs_ts = stat_data_ref.resample_time(
                    var_ref,
                    ts_type=ts_type,
                    how=resample_how,
                    apply_constraints=apply_time_resampling_constraints,
                    min_num_obs=min_num_obs,
                    inplace=True)[var_ref]

    # fill up missing time stamps
    return pd.concat([obs_ts, grid_ts], axis=1, keys=['ref', 'data'])

def _colocate_site_data_helper_timecol(stat_data, stat_data_ref, var, var_ref,
                               ts_type, resample_how,
                               apply_time_resampling_constraints,
                               min_num_obs,
                               use_climatology_ref):
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
    apply_time_resampling_constraints : bool, optional
        if True, then time resampling constraints are applied as provided via
        :attr:`min_num_obs` or if that one is unspecified, as defined in
        :attr:`pyaerocom.const.OBS_MIN_NUM_RESAMPLE`. If None, than
        :attr:`pyaerocom.const.OBS_APPLY_TIME_RESAMPLE_CONSTRAINTS` is used
        (which defaults to True !!).
    min_num_obs : int or dict, optional
        minimum number of observations for resampling of time
    use_climatology_ref : bool
        if True, NotImplementedError is raised

    Raises
    ------
    TemporalResolutionError
        if model or obs sampling frequency is lower than desired output frequency
    NotImplementedError
        if input arg `use_climatology_ref` is True.

    Returns
    -------
    pandas.DataFrame
        dataframe containing the colocated input data (column names are
        data and ref)
    """
    if use_climatology_ref:
        raise NotImplementedError(
            'Using observation climatology in colocation with option '
            'colocate_time=True is not available yet ...')

    grid_tst = stat_data.get_var_ts_type(var)
    obs_tst = stat_data_ref.get_var_ts_type(var_ref)
    coltst = TsType(get_lowest_resolution(grid_tst, obs_tst))
    if coltst.mulfac != 1:
        coltst = coltst.next_lower
    stat_data.resample_time(
        var_name=var,
        ts_type=str(coltst),
        how=resample_how,
        apply_constraints=apply_time_resampling_constraints,
        min_num_obs=min_num_obs,
        inplace=True)

    stat_data_ref.resample_time(
        var_name=var_ref,
        ts_type=str(coltst),
        how=resample_how,
        apply_constraints=apply_time_resampling_constraints,
        min_num_obs=min_num_obs,
        inplace=True)
    # now both StationData objects are in the same resolution, but they still
    # might have gaps in their time axis, thus concatenate them in a DataFrame,
    # which will merge the time index
    merged = pd.concat([stat_data_ref[var_ref], stat_data[var]],
                       axis=1, keys=['ref', 'data'])

    grid_ts = merged['data']
    obs_ts = merged['ref']
    # invalidate model where obs is NaN
    obsnan = np.isnan(obs_ts.values)
    grid_ts[obsnan] = np.nan

    # now resample both to output frequency
    resampler = TimeResampler()
    obs_ts = resampler.resample(
        to_ts_type=ts_type,
        input_data=obs_ts,
        from_ts_type=coltst,
        how=resample_how,
        apply_constraints=apply_time_resampling_constraints,
        min_num_obs=min_num_obs
        )

    grid_ts = resampler.resample(
        to_ts_type=ts_type,
        input_data=grid_ts,
        from_ts_type=coltst,
        how=resample_how,
        apply_constraints=apply_time_resampling_constraints,
        min_num_obs=min_num_obs
        )
    # fill up missing time stamps
    return pd.concat([obs_ts, grid_ts], axis=1, keys=['ref', 'data'])

def colocate_gridded_ungridded(gridded_data, ungridded_data, ts_type=None,
                               start=None, stop=None, filter_name=None,
                               regrid_res_deg=None, vert_scheme=None,
                               harmonise_units=True,
                               regrid_scheme='areaweighted',
                               var_ref=None,
                               update_baseyear_gridded=None,
                               ignore_station_names=None,
                               apply_time_resampling_constraints=None,
                               min_num_obs=None,
                               colocate_time=False,
                               use_climatology_ref=False,
                               resample_how=None,
                               **kwargs):
    """Colocate gridded with ungridded data (low level method)

    For high-level colocation see :class:`pyaerocom.colocation_auto.Colocator`
    and :class:`pyaerocom.colocation_auto.ColocationSetup`

    Note
    ----
    Uses the variable that is contained in input :class:`GriddedData` object
    (since these objects only contain a single variable). If this variable
    is not contained in observation data (or contained but using a different
    variable name) you may specify the obs variable to be used via input arg
    `var_ref`

    Parameters
    ----------
    gridded_data : GriddedData
        gridded data object (e.g. model results).
    ungridded_data : UngriddedData
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
        details). If None, then it is set to 'WORLD-wMOUNTAINS', which
        corresponds to no filtering (world with mountains).
        Use WORLD-noMOUNTAINS to exclude mountain sites.
    regrid_res_deg : int or dict, optional
        regrid resolution in degrees. If specified, the input gridded data
        object will be regridded in lon / lat dimension to the input
        resolution (if input is integer, both lat and lon are regridded to that
        resolution, if input is dict, use keys `lat_res_deg` and `lon_res_deg`
        to specify regrid resolutions, respectively).
    vert_scheme : str
        string specifying scheme used to reduce the dimensionality in case
        input grid data contains vertical dimension. Example schemes are
        `mean, surface, altitude`, for details see
        :func:`GriddedData.to_time_series`.
    harmonise_units : bool
        if True, units are attempted to be harmonised (note: raises Exception
        if True and units cannot be harmonised).
    var_ref : :obj:`str`, optional
        variable against which data in :attr:`gridded_data` is supposed to be
        compared. If None, then the same variable is used
        (i.e. `gridded_data.var_name`).
    update_baseyear_gridded : int, optional
        optional input that can be set in order to re-define the time dimension
        in the gridded data object to be analysed. E.g., if the data object
        is a climatology (one year of data) that has set the base year of the
        time dimension to a value other than the specified input start / stop
        time this may be used to update the time in order to make colocation
        possible.
    ignore_station_names : str or list, optional
        station name or pattern or list of station names or patterns that should
        be ignored
    apply_time_resampling_constraints : bool, optional
        if True, then time resampling constraints are applied as provided via
        :attr:`min_num_obs` or if that one is unspecified, as defined in
        :attr:`pyaerocom.const.OBS_MIN_NUM_RESAMPLE`. If None, than
        :attr:`pyaerocom.const.OBS_APPLY_TIME_RESAMPLE_CONSTRAINTS` is used
        (which defaults to True !!).
    min_num_obs : int or dict, optional
        minimum number of observations for resampling of time
    colocate_time : bool
        if True and if original time resolution of data is higher than desired
        time resolution (`ts_type`), then both datasets are colocated in time
        *before* resampling to lower resolution.
    use_climatology_ref : bool
        if True, climatological timeseries are used from observations
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
        if instance of input :class:`UngriddedData` object contains more than
        one dataset
    TimeMatchError
        if gridded data time range does not overlap with input time range
    ColocationError
        if none of the data points in input :class:`UngriddedData` matches
        the input colocation constraints
    """
    if filter_name is None:
        filter_name = const.DEFAULT_REG_FILTER

    try:
        gridded_data.check_dimcoords_tseries()
    except DimensionOrderError:
        gridded_data.reorder_dimensions_tseries()

    var = gridded_data.var_name
    aerocom_var = gridded_data.var_name_aerocom

    _check_var_registered(var, aerocom_var, gridded_data)

    if var_ref is None:
        if aerocom_var is not None:
            var_ref = aerocom_var
        else:
            var_ref = var

    if not var_ref in ungridded_data.contains_vars:
        raise VarNotAvailableError('Variable {} is not available in ungridded '
                                   'data (which contains {})'
                                   .format(var_ref,
                                           ungridded_data.contains_vars))
    elif len(ungridded_data.contains_datasets) > 1:
        raise AttributeError('Colocation can only be performed with '
                             'ungridded data objects that only contain a '
                             'single dataset. Use method `extract_dataset` of '
                             'UngriddedData object to extract single datasets')

    dataset_ref = ungridded_data.contains_datasets[0]

    if update_baseyear_gridded is not None:
        # update time dimension in gridded data
        gridded_data.base_year = update_baseyear_gridded

    grid_ts_type_src = gridded_data.ts_type
    grid_ts_type = TsType(gridded_data.ts_type)
    if isinstance(ts_type, str):
        to_ts_type = TsType(ts_type)
    if ts_type is None or grid_ts_type < to_ts_type:
        to_ts_type = grid_ts_type
    elif grid_ts_type > to_ts_type and not colocate_time:
        gridded_data = gridded_data.resample_time(
            str(to_ts_type),
            apply_constraints=apply_time_resampling_constraints,
            min_num_obs=min_num_obs,
            how=resample_how
            )
        grid_ts_type = to_ts_type

    # get start / stop of gridded data as pandas.Timestamp
    grid_start = to_pandas_timestamp(gridded_data.start)
    grid_stop = to_pandas_timestamp(gridded_data.stop)

    if start is None:
        start = grid_start
    else:
        start = to_pandas_timestamp(start)
    if stop is None:
        stop = grid_stop
    else:
        stop = to_pandas_timestamp(stop)

    if start < grid_start:
        start = grid_start
    if stop > grid_stop:
        stop = grid_stop
    # check overlap
    if stop < grid_start or start > grid_stop:
        raise TimeMatchError('Input time range {}-{} does not '
                             'overlap with data range: {}-{}'
                             .format(start, stop, grid_start, grid_stop))
    # create instance of Filter class (may, in the future, also include all
    # filter options, e.g. start, stop, variables, only land, only oceans, and
    # may also be linked with other data object, e.g. if data is only supposed
    # to be used if other data object exceeds a certain threshold... but for
    # now, only region and altitude range)
    regfilter = Filter(name=filter_name)

    # apply filter to data
    ungridded_data = regfilter.apply(ungridded_data)

    #crop time
    gridded_data = regfilter.apply(gridded_data)
    if start > grid_start or stop < grid_stop:
        gridded_data = gridded_data.crop(time_range=(start, stop))

    if regrid_res_deg is not None:
        gridded_data = _regrid_gridded(gridded_data, regrid_scheme,
                                       regrid_res_deg)

    if use_climatology_ref:
        col_freq='monthly'
        obs_start = const.CLIM_START
        obs_stop = const.CLIM_STOP
    else:
        col_freq = str(to_ts_type)#TS_TYPE_TO_PANDAS_FREQ[grid_ts_type]
        obs_start = start
        obs_stop = stop

    # colocation frequency
    col_tst = TsType(col_freq)

    # ToDo: move the following code into new function
    # GriddedData.get_latlon_ranges
    latitude = gridded_data.latitude.points
    longitude = gridded_data.longitude.points
    lat_range = [np.min(latitude), np.max(latitude)]
    lon_range = [np.min(longitude), np.max(longitude)]
    # End ToDo

    ungridded_data = ungridded_data.filter_by_meta(latitude=lat_range,
                                                   longitude=lon_range)

    # get timeseries from all stations in provided time resolution
    # (time resampling is done below in main loop)
    all_stats = ungridded_data.to_station_data_all(
            vars_to_convert=var_ref,
            start=obs_start,
            stop=obs_stop,
            by_station_name=True,
            ignore_index=ignore_station_names,
            **kwargs
            )

    obs_stat_data = all_stats['stats']
    ungridded_lons = all_stats['longitude']
    ungridded_lats = all_stats['latitude']

    if len(obs_stat_data) == 0:
        raise VarNotAvailableError('Variable {} is not available in specified '
                                   'time interval ({}-{})'
                                   .format(var_ref, start, stop))
    # make sure the gridded data is in the right dimension
    if gridded_data.ndim > 3:
        if vert_scheme is None:
            vert_scheme = 'mean'
        if not vert_scheme in gridded_data.SUPPORTED_VERT_SCHEMES:
            raise ValueError('Vertical scheme {} is not supported'.format(vert_scheme))

    grid_stat_data = gridded_data.to_time_series(longitude=ungridded_lons,
                                                 latitude=ungridded_lats,
                                                 vert_scheme=vert_scheme)

    pd_freq = col_tst.to_pandas_freq()
    time_idx = make_datetime_index(start, stop, pd_freq)

    time_num = len(time_idx)
    stat_num = len(obs_stat_data)
    coldata = np.empty((2, time_num, stat_num))*np.nan

    lons = [np.nan] * stat_num
    lats = [np.nan] * stat_num
    alts = [np.nan] * stat_num
    station_names = [''] * stat_num

    ungridded_unit = None
    ts_type_src_ref = None
    if not harmonise_units:
        gridded_unit = str(gridded_data.units)
    else:
        gridded_unit = None

    # loop over all stations and append to colocated data object
    for i, obs_stat in enumerate(obs_stat_data):
        # Add coordinates to arrays required for xarray.DataArray below
        lons[i] = obs_stat.longitude
        lats[i] = obs_stat.latitude
        alts[i] = obs_stat.altitude
        station_names[i] = obs_stat.station_name

        # ToDo: consider removing to keep ts_type_src_ref (this was probably
        # introduced for EBAS were the original data frequency is not constant
        # but can vary from site to site)
        if ts_type_src_ref is None:
            ts_type_src_ref = obs_stat['ts_type_src']
        elif obs_stat['ts_type_src'] != ts_type_src_ref:
            spl = ts_type_src_ref.split(';')
            if not obs_stat['ts_type_src'] in spl:
                spl.append(obs_stat['ts_type_src'])
            ts_type_src_ref = ';'.join(spl)

        if ungridded_unit is None:
            try:
                ungridded_unit = obs_stat['var_info'][var_ref]['units']
            except KeyError as e: #variable information or unit is not defined
                logger.exception(repr(e))
        try:
            unit = obs_stat['var_info'][var_ref]['units']
        except Exception:
            unit = None
        if not unit == ungridded_unit:
            raise ValueError('Cannot perform colocation. Ungridded data '
                             'object contains different units ({})'.format(var_ref))
        # get observations (Note: the index of the observation time series
        # is already in the specified frequency format, and thus, does not
        # need to be updated, for details (or if errors occur), cf.
        # UngriddedData.to_station_data, where the conversion happens)

        # get model station data
        grid_stat = grid_stat_data[i]
        if harmonise_units:
            grid_unit = grid_stat.get_unit(var)
            obs_unit = obs_stat.get_unit(var_ref)
            if not grid_unit == obs_unit:
                grid_stat.convert_unit(var, obs_unit)
            if gridded_unit is None:
                gridded_unit = obs_unit

        try:
            if colocate_time:
                _df = _colocate_site_data_helper_timecol(

                    stat_data=grid_stat,
                    stat_data_ref=obs_stat,
                    var=var, var_ref=var_ref,
                    ts_type=col_freq,
                    resample_how=resample_how,
                    apply_time_resampling_constraints=apply_time_resampling_constraints,
                    min_num_obs=min_num_obs,
                    use_climatology_ref=use_climatology_ref)
            else:
                _df = _colocate_site_data_helper(

                    stat_data=grid_stat,
                    stat_data_ref=obs_stat,
                    var=var, var_ref=var_ref,
                    ts_type=col_freq,
                    resample_how=resample_how,
                    apply_time_resampling_constraints=apply_time_resampling_constraints,
                    min_num_obs=min_num_obs,
                    use_climatology_ref=use_climatology_ref)


            # this try/except block was introduced on 23/2/2021 as temporary fix from
            # v0.10.0 -> v0.10.1 as a result of multi-weekly obsdata (EBAS) that
            # can end up resulting in incorrect number of timestamps after resampling
            # (the error was discovered using EBASMC, concpm10, 2019 and colocation
            # frequency monthly)
            try:
                # assign the unified timeseries data to the colocated data array
                coldata[0, :, i] = _df['ref'].values
                coldata[1, :, i] = _df['data'].values
            except ValueError as e:
                const.print_log.warning(
                    f'Failed to colocate time for station {obs_stat.station_name}. '
                    f'This station will be skipped (error: {e})'
                    )

        except TemporalResolutionError as e:
            # resolution of obsdata is too low
            const.print_log.warning(
                f'{var_ref} data from site {obs_stat.station_name} will '
                f'not be added to ColocatedData. Reason: {e}'
                )
    try:
        revision = ungridded_data.data_revision[dataset_ref]
    except Exception:
        try:
            revision = ungridded_data._get_data_revision_helper(dataset_ref)
        except MetaDataError:
            revision = 'MULTIPLE'
        except Exception:
            revision = 'n/a'

    files = [os.path.basename(x) for x in gridded_data.from_files]

    meta = {
            'data_source'       :   [dataset_ref,
                                     gridded_data.name],
            'var_name'          :   [var_ref, var],
            'ts_type'           :   col_freq, # will be updated below if resampling
            'filter_name'       :   filter_name,
            'ts_type_src'       :   [ts_type_src_ref, grid_ts_type_src],
            'start_str'         :   to_datestring_YYYYMMDD(start),
            'stop_str'          :   to_datestring_YYYYMMDD(stop),
            'var_units'         :   [ungridded_unit,
                                     gridded_unit],
            'vert_scheme'       :   vert_scheme,
            'data_level'        :   3,
            'revision_ref'      :   revision,
            'from_files'        :   files,
            'from_files_ref'    :   None,
            'stations_ignored'  :   ignore_station_names,
            'colocate_time'     :   colocate_time,
            'obs_is_clim'       :   use_climatology_ref,
            'pyaerocom'         :   pya_ver,
            'apply_constraints' :   apply_time_resampling_constraints,
            'min_num_obs'       :   min_num_obs,
            'resample_how'      :   resample_how}


    meta.update(regfilter.to_dict())

    # create coordinates of DataArray
    coords = {'data_source' : meta['data_source'],
              'time'        : time_idx,
              'station_name': station_names,
              'latitude'    : ('station_name', lats),
              'longitude'   : ('station_name', lons),
              'altitude'    : ('station_name', alts)
              }

    dims = ['data_source', 'time', 'station_name']
    data = ColocatedData(data=coldata, coords=coords, dims=dims, name=var,
                         attrs=meta)

    # add correct units for lat / lon dimensions
    data.latitude.attrs['standard_name'] = gridded_data.latitude.standard_name
    data.latitude.attrs['units'] = str(gridded_data.latitude.units)

    data.longitude.attrs['standard_name'] = gridded_data.longitude.standard_name
    data.longitude.attrs['units'] = str(gridded_data.longitude.units)

    return data

def correct_model_stp_coldata(coldata, p0=None, t0=273.15, inplace=False):
    """Correct modeldata in colocated data object to STP conditions

    Note
    ----
    BETA version, quite unelegant coded (at 8pm 3 weeks before IPCC deadline),
    but should do the job for 2010 monthly colocated data files (AND NOTHING
    ELSE)!

    """
    if coldata.ndim != 3:
        raise NotImplementedError('Can only handle 3D coldata so far...')
    elif not coldata.ts_type == 'monthly' or not len(coldata.time)==12:
        raise NotImplementedError('Can only handle monthly colocated data files '
                                  'so far (since ERA5 temps are only available) '
                                  'in monthly resolution')
    startyr = pd.Timestamp(coldata.start).year
    stopyr = pd.Timestamp(coldata.stop).year
    if not all([x==2010 for x in (startyr, stopyr)]):
        raise NotImplementedError('Can only handle 2010 monthly data so far')

    if not inplace:
        coldata = coldata.copy()
    temp = xr.open_dataset(const.ERA5_SURFTEMP_FILE)['t2m']
    from geonum.atmosphere import pressure
    arr = coldata.data

    coords = zip(arr.latitude.values, arr.longitude.values,
                 arr.altitude.values, arr.station_name.values)
    if p0 is None:
        p0 = pressure() #STD conditions sea level
    const.logger.info('Correcting model data in ColocatedData instance to STP')
    cfacs = []
    meantemps = []
    mintemps = []
    maxtemps =[]
    ps = []
    for i, (lat, lon, alt, name) in enumerate(coords):
        const.logger.info(name, ', Lat', lat, ', Lon', lon)
        p = pressure(alt)
        const.logger.info('Alt', alt)
        const.logger.info('P=', p/100, 'hPa')

        ps.append(p/100)

        temps = temp.sel(latitude=lat, longitude=lon, method='nearest').data

        meantemps.append(temps.mean())
        mintemps.append(temps.min())
        maxtemps.append(temps.min())

        if not len(temps) == len(arr.time):
            raise NotImplementedError('Check timestamps')
        const.logger.info('Mean Temp: ', temps.mean() - t0, ' C')

        corrfacs = (p0 / p) * (temps / t0)

        const.logger.info('Corr fac:', corrfacs.mean(), '+/-', corrfacs.std())

        cfacs.append(corrfacs.mean())

        #mularr = xr.DataArray(corrfacs)

        if not arr.station_name.values[i] == name:
            raise Exception
        elif not arr.dims[1] == 'time':
            raise Exception
        arr[1, :, i] *= corrfacs

    cfacs = np.asarray(cfacs)

    const.logger.info('Min: ', cfacs.min())
    const.logger.info('Mean: ', cfacs.mean())
    const.logger.info('Max: ', cfacs.max())
    coldata.data.attrs['Model_STP_corr'] = True

    newcoords = dict(pres=('station_name', ps),
                     temp_mean=('station_name', meantemps),
                     temp_min=('station_name', mintemps),
                     temp_max=('station_name', maxtemps),
                     stp_corrfac_mean=('station_name', cfacs))

    coldata.data = coldata.data.assign_coords(newcoords)

    info_str = ('Correction factors to convert model data from ambient to '
                'STP were computed using corrfac=(p0/p)*(T/T0) with T0=273K '
                'and p0=1013 hPa and p is the pressure at the station location '
                '(which was computed assuming a standard atmosphere and using '
                'the station altitude) and T is the 2m surface temperature at '
                'the station, applied on a monthly basis and estimated using '
                'ERA5 data')

    coldata.data['pres'].attrs['units'] = 'hPa'
    coldata.data['temp_mean'].attrs['units'] = 'K'
    coldata.data['temp_min'].attrs['units'] = 'K'
    coldata.data['temp_max'].attrs['units'] = 'K'

    coldata.data.attrs['Model_STP_corr'] = True
    coldata.data.attrs['Model_STP_corr_info'] = info_str
    return coldata

if __name__=='__main__':
    import pyaerocom as pya
    import matplotlib.pyplot as plt
    plt.close('all')

    obsdata = pya.io.ReadUngridded().read('EBASMC', 'ac550aer')

    # update unit to wrong unit
    obsdata.check_convert_var_units('ac550aer', 'm-1', inplace=True)

    obsdata.remove_outliers('ac550aer', inplace=True)