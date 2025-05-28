"""
Methods and / or classes to perform 3D colocation
"""

from __future__ import annotations

import logging
import os
from typing import NamedTuple

import iris
import numpy as np
from pyaerocom.units import Unit

from pyaerocom import __version__ as pya_ver
from pyaerocom import const
from pyaerocom.climatology_config import ClimatologyConfig
from pyaerocom._lowlevel_helpers import LayerLimits, RegridResDeg
from pyaerocom.exceptions import (
    DataUnitError,
    DimensionOrderError,
    MetaDataError,
    TemporalResolutionError,
    VarNotAvailableError,
)
from pyaerocom.filter import Filter
from pyaerocom.helpers import make_datetime_index
from pyaerocom.units.datetime import TsType

from .colocated_data import ColocatedData
from .colocation_utils import (
    _colocate_site_data_helper,
    _colocate_site_data_helper_timecol,
    _regrid_gridded,
    check_time_ival,
    check_ts_type,
    resolve_var_name,
)

logger = logging.getLogger(__name__)


class ColocatedDataLists(NamedTuple):
    colocateddata_for_statistics: list[ColocatedData]
    colocateddata_for_profile_viz: list[ColocatedData]


def _colocate_vertical_profile_gridded(
    data,
    data_ref,
    start=None,
    stop=None,
    filter_name=None,
    harmonise_units=True,
    var_ref=None,
    min_num_obs=None,
    colocate_time=False,
    use_climatology_ref=False,
    resample_how=None,
    layer_limits: LayerLimits | None = None,
    obs_stat_data=None,
    ungridded_lons=None,
    ungridded_lats=None,
    col_freq=None,
    col_tst=None,
    var=None,
    var_aerocom=None,
    var_ref_aerocom=None,
) -> list[ColocatedData]:
    if layer_limits is None:
        raise Exception("layer limits must be provided")

    data_ref_unit = None
    ts_type_src_ref = None
    if not harmonise_units:
        data_unit = str(data.units)
    else:
        data_unit = None

    pd_freq = col_tst.to_pandas_freq()
    time_idx = make_datetime_index(start, stop, pd_freq)

    time_num = len(time_idx)
    stat_num = len(obs_stat_data)

    arr = np.full((2, time_num, stat_num), np.nan)

    lons = np.full(stat_num, np.nan)
    lats = np.full(stat_num, np.nan)
    alts = np.full(stat_num, np.nan)

    station_names = [""] * stat_num

    dataset_ref = data_ref.contains_datasets[0]
    ts_type_src_data = data.ts_type

    list_of_colocateddata_objects = []
    for vertical_layer in layer_limits:
        # Think about efficiency here in terms of order of loops. candidate for parallelism
        # create the 2D layer data
        arr = np.full((2, time_num, stat_num), np.nan)
        try:
            data_this_layer = (
                data.extract(
                    iris.Constraint(
                        coord_values={
                            "altitude": lambda cell: vertical_layer["start"]
                            < cell
                            < vertical_layer["end"]
                        }
                    )
                )
                .collapsed("altitude", iris.analysis.MEAN)
                .copy()
            )
        except Exception as e:
            logger.warning(f"No altitude in model data layer {vertical_layer}")
            logger.debug(f"Raised: {e}")
            continue

        grid_stat_data_this_layer = data_this_layer.to_time_series(
            longitude=ungridded_lons,
            latitude=ungridded_lats,
        )

        # loop over all stations and append to colocated data object
        for i, obs_stat in enumerate(obs_stat_data):
            # Add coordinates to arrays required for xarray.DataArray below
            lons[i] = obs_stat.longitude
            lats[i] = obs_stat.latitude
            alts[i] = obs_stat.station_coords[
                "altitude"
            ]  # altitude refers to altitude of the data. be explicit where getting from
            station_names[i] = obs_stat.station_name

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
            grid_stat_this_layer = grid_stat_data_this_layer[i]

            # Make a copy of the station data and resample it to the mean based on hourly resolution. Needs testing!
            obs_stat_this_layer = obs_stat.copy()

            try:
                obs_stat_this_layer[var_ref] = (
                    obs_stat_this_layer.select_altitude(
                        var_name=var_ref, altitudes=list(vertical_layer.values())
                    )
                    .mean("altitude", skipna=True)  # very important to skip nans here
                    .to_series()  # make pandas series
                )
            except ValueError:
                logger.warning(
                    f"Var: {var_ref}. Skipping {obs_stat_this_layer.station_name} in altitude layer {vertical_layer} because no data"
                )
                continue

            if harmonise_units:
                grid_unit = grid_stat_this_layer.get_unit(var)
                obs_unit = obs_stat_this_layer.get_unit(var_ref)
                if not grid_unit == obs_unit:
                    grid_stat_this_layer.convert_unit(var, obs_unit)
                if data_unit is None:
                    data_unit = obs_unit

            try:
                if colocate_time:
                    _df = _colocate_site_data_helper_timecol(
                        stat_data=grid_stat_this_layer,
                        stat_data_ref=obs_stat_this_layer,
                        var=var,
                        var_ref=var_ref,
                        ts_type=col_freq,
                        resample_how=resample_how,
                        min_num_obs=min_num_obs,
                        use_climatology_ref=use_climatology_ref,
                    )
                else:
                    _df = _colocate_site_data_helper(
                        stat_data=grid_stat_this_layer,
                        stat_data_ref=obs_stat_this_layer,
                        var=var,
                        var_ref=var_ref,
                        ts_type=col_freq,
                        resample_how=resample_how,
                        min_num_obs=min_num_obs,
                        use_climatology_ref=use_climatology_ref,
                    )

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
            revision = data_ref.get_data_revision[dataset_ref]
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
            "vertical_layer": vertical_layer,
        }

        # create coordinates of DataArray
        coords = {
            "data_source": meta["data_source"],
            "time": time_idx,
            "station_name": station_names,
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

        coldata.data.attrs["altitude_units"] = str(data.altitude.units)

        coldata.vertical_layer = vertical_layer

        list_of_colocateddata_objects.append(coldata)

    return list_of_colocateddata_objects


def colocate_vertical_profile_gridded(
    data,
    data_ref,
    ts_type: str = None,
    start: str | None = None,
    stop: str | None = None,
    filter_name: str = None,
    regrid_res_deg: float | RegridResDeg | None = None,
    harmonise_units: bool = True,
    regrid_scheme: str = "areaweighted",
    var_ref: str = None,
    update_baseyear_gridded: int = None,
    min_num_obs: int | dict | None = None,
    colocate_time: bool = False,
    use_climatology_ref: dict = False,
    resample_how: str | dict = None,
    colocation_layer_limits: tuple[LayerLimits, ...] | None = None,
    profile_layer_limits: tuple[LayerLimits, ...] | None = None,
    **kwargs,
) -> ColocatedDataLists:
    """
    Colocated vertical profile data with gridded (model) data

    The guts of this function are placed in a helper function as not to repeat the code.
    This is done because colocation must occur twice:
        i) at the the statistics are computed
        ii) at a finer vertical resolution for profile visualization
    Some things you do not want to compute twice, however.
    So (most of) the things that correspond to both colocation instances are computed here,
    and then passed to the helper function.

    Returns
        colocated_data_lists : ColocatedDataLists

    -------
    """

    if filter_name is None:
        filter_name = const.DEFAULT_REG_FILTER
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

    if any(
        not {"start", "end"}.issubset(layer)
        for layer in colocation_layer_limits + profile_layer_limits
    ):
        raise KeyError(
            "start and end must be provided for profiles in each vertical layer in colocate_vertical_profile_gridded"
        )

    data_ref_meta_idxs_with_var_info = []
    for i in range(len(data_ref.metadata)):
        if "altitude" not in data_ref.metadata[i]["var_info"]:
            logger.warning(
                f"Warning: Station {data_ref.metadata[i]['station_name']} does not have any var_info"
            )
        else:
            data_ref_meta_idxs_with_var_info.append(i)

    if any(
        data.altitude.units != Unit(data_ref.metadata[i]["var_info"]["altitude"]["units"])
        for i in data_ref_meta_idxs_with_var_info
    ):
        logger.info(
            f"Mismatching units in colocation_3d.py. Model has units {data.altitude.units} whereas not all observations have this unit. Debug to find out where."
        )
        raise DataUnitError

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

    if regrid_res_deg is not None:  # pragma: no cover
        data = _regrid_gridded(data, regrid_scheme, regrid_res_deg)

    # Special ts_typs for which all stations with ts_type< are removed
    reduce_station_data_ts_type = ts_type

    # ts_type_src_data = data.ts_type
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
    altitude = data.altitude.points
    lat_range = [np.min(latitude), np.max(latitude)]
    lon_range = [np.min(longitude), np.max(longitude)]
    alt_range = [np.min(altitude), np.max(altitude)]
    # use only sites that are within model domain

    # filter_by_meta wipes is_vertical_profile
    # Also note that filter_by_meta may not be calling alt_range. Function filter_altitude is defined but not used
    data_ref = data_ref.filter_by_meta(latitude=lat_range, longitude=lon_range, altitude=alt_range)

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

    if len(all_stats["stats"]) == 0:
        raise VarNotAvailableError(
            f"Variable {var_ref} is not available in specified time interval ({start}-{stop})"
        )

    # Colocation has to occur twice for vertical profiles.
    # Once for the colocation which we will compute the statistics over.
    # The second time is just to show the vertical profiles on the web. This needs to be finer
    # Here we make a list with the list of ColocatedData objects for both colocation purposes
    output_prep = [
        _colocate_vertical_profile_gridded(
            data=data,
            data_ref=data_ref,
            start=start,
            stop=stop,
            filter_name=filter_name,
            harmonise_units=harmonise_units,
            var_ref=var_ref,
            min_num_obs=min_num_obs,
            colocate_time=colocate_time,
            use_climatology_ref=use_climatology_ref,
            resample_how=resample_how,
            layer_limits=layer_limits,
            obs_stat_data=all_stats["stats"],
            ungridded_lons=all_stats["longitude"],
            ungridded_lats=all_stats["latitude"],
            col_freq=col_freq,
            col_tst=col_tst,
            var=var,
            var_aerocom=var_aerocom,
            var_ref_aerocom=var_ref_aerocom,
        )
        for layer_limits in (colocation_layer_limits, profile_layer_limits)
    ]
    # Create a namedtuple for output.
    # Each element in the tuple is a list of ColocatedData objects.
    # The length of these lists is the same as the number of colocation layers

    for coldata in output_prep[1]:
        coldata.data.attrs["just_for_viz"] = 1

    colocated_data_lists = ColocatedDataLists(
        *output_prep
    )  # put the list of prepared output into namedtuple object s.t. both position and named arguments can be used

    return colocated_data_lists
