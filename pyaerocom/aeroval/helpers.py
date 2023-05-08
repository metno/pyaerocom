import glob
import logging
import os
import shutil
from pathlib import Path

import numpy as np

from pyaerocom import const
from pyaerocom.aeroval.modelentry import ModelEntry
from pyaerocom.aeroval.varinfo_web import VarinfoWeb
from pyaerocom.colocateddata import ColocatedData
from pyaerocom.colocation_auto import Colocator
from pyaerocom.exceptions import TemporalResolutionError
from pyaerocom.griddeddata import GriddedData
from pyaerocom.helpers import (
    get_highest_resolution,
    get_max_period_range,
    make_dummy_cube,
    start_stop_str,
)
from pyaerocom.io import ReadGridded
from pyaerocom.tstype import TsType
from pyaerocom.variable import Variable

logger = logging.getLogger(__name__)


def check_var_ranges_avail(model_data, var_name):
    """
    Check if lower and upper variable ranges are available for input variable

    Parameters
    ----------
    model_data : GriddedData
        modeldata containing variable data
    var_name : str
        variable name to be checked (must be the same as model data
        AeroCom variable name).

    Raises
    ------
    ValueError
        if ranges for input variable are not defined and if input model data
        corresponds to a different variable than the input variable name.

    Returns
    -------
    None

    """
    try:
        VarinfoWeb(var_name)
    except AttributeError:
        if model_data.var_name_aerocom == var_name:
            model_data.register_var_glob(delete_existing=True)
        else:
            raise ValueError(
                f"Mismatch between variable name of input model_data "
                f"({model_data.var_name_aerocom}) and var_name {var_name}"
            )


def _check_statistics_periods(periods: list) -> list:
    """
    Check input list of period strings is valid

    Parameters
    ----------
    periods : list
        list containing period strings to be checked.

    Raises
    ------
    ValueError
        if input is not a list or any of the provided periods in that list is
        not a string or invalid.

    Returns
    -------
    list
        list of periods

    """
    checked = []
    if not isinstance(periods, list):
        raise ValueError("statistics_periods needs to be a list")
    for per in periods:
        if not isinstance(per, str):
            raise ValueError("All periods need to be strings")
        spl = [x.strip() for x in per.split("-")]
        if len(spl) > 2:
            raise ValueError(
                f"Invalid value for period ({per}), can be either single "
                f"years or period of years (e.g. 2000-2010)."
            )
        _per = "-".join([str(int(val)) for val in spl])
        checked.append(_per)
    return checked


def _period_str_to_timeslice(period: str) -> slice:
    """
    Convert input period to a time slice

    Parameters
    ----------
    period : str
        period, e.g. "2000-2010"

    Raises
    ------
    ValueError
        if input period is invalid

    Returns
    -------
    slice
        slice containing start and end strings.
    """
    spl = period.split("-")
    if len(spl) == 1:
        return slice(spl[0], spl[0])
    elif len(spl) == 2:
        return slice(*spl)
    raise ValueError(period)


def _get_min_max_year_periods(statistics_periods):
    """Get lowest and highest available year from all periods

    Parameters
    ----------
    statistics_periods : list
        list of periods for experiment

    Returns
    -------
    int
        start year
    int
        stop year (may be the same as start year, e.g. if periods suggest
        single year analysis).
    """
    startyr, stopyr = 1e6, -1e6
    for per in statistics_periods:
        sl = _period_str_to_timeslice(per)
        perstart, perstop = int(sl.start), int(sl.stop)
        if perstart < startyr:
            startyr = perstart
        if perstop > stopyr:
            stopyr = perstop
    return startyr, stopyr


def make_dummy_model(obs_list: list, cfg) -> str:
    # Sets up variable for the model register
    tmpdir = const.LOCAL_TMP_DIR
    const.add_data_search_dir(tmpdir)

    model_id = "dummy_model"
    outdir = os.path.join(tmpdir, f"{model_id}/renamed")

    os.makedirs(outdir, exist_ok=True)

    # Finds dates and freq to use, so that all observations are covered
    (start, stop) = get_max_period_range(cfg.time_cfg.periods)
    freq = get_highest_resolution(*cfg.time_cfg.freqs)

    tmp_var_obj = Variable()
    # Loops over variables in obs
    for obs in obs_list:
        for var in cfg.obs_cfg[obs]["obs_vars"]:
            # Create dummy cube

            dummy_cube = make_dummy_cube(var, start_yr=start, stop_yr=stop, freq=freq)

            # Converts cube to GriddedData
            dummy_grid = GriddedData(dummy_cube)

            # Set the value to be the mean of acceptable values to prevent incorrect outlier removal
            # This needs some care though because the defaults are (currently) -inf and inf, which leads to erroneous removal

            if not (
                dummy_grid.var_info.minimum == tmp_var_obj.VMIN_DEFAULT
                or dummy_grid.var_info.maximum == tmp_var_obj.VMAX_DEFAULT
            ):
                dummy_grid.data *= (dummy_grid.var_info.minimum + dummy_grid.var_info.maximum) / 2

            # Loop over each year
            yr_gen = dummy_grid.split_years()

            for dummy_grid_yr in yr_gen:
                # Add to netcdf
                yr = dummy_grid_yr.years_avail()[0]
                vert_code = cfg.obs_cfg[obs]["obs_vert_type"]

                save_name = dummy_grid_yr.aerocom_savename(model_id, var, vert_code, yr, freq)
                dummy_grid_yr.to_netcdf(outdir, savename=save_name)

    # Add dummy model to cfg
    cfg.model_cfg["dummy"] = ModelEntry(model_id="dummy_model")

    return model_id


def delete_dummy_model(model_id: str) -> None:
    tmpdir = const.LOCAL_TMP_DIR
    const.add_data_search_dir(tmpdir)

    renamed = Path(tmpdir) / f"{model_id}/renamed"
    for path in renamed.glob("*.nc"):
        print(f"Deleting dummy model {path}")
        path.unlink()
