import logging
import os

import numpy as np

from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
from pyaerocom.griddeddata import GriddedData
from pyaerocom.helpers import make_dummy_cube_latlon, numpy_to_cube
from pyaerocom.variable_helpers import get_variable

logger = logging.getLogger(__name__)


def make_config_template(proj_id: str, exp_id: str) -> EvalSetup:
    """
    Make a template for an AeroVal evaluation setup

    Parameters
    ----------
    proj_id : str
        ID of project.
    exp_id : str
        ID of experiment

    Returns
    -------
    EvalSetup
        template evaluation setup (all defaults are set) that can be used to
        add model and obs entries, and modified to meet the purposes.
    """
    return EvalSetup(proj_id, exp_id)


def compute_model_average_and_diversity(
    cfg,
    var_name,
    model_names=None,
    ts_type=None,
    lat_res_deg=2,
    lon_res_deg=3,
    data_id=None,
    avg_how=None,
    extract_surface=True,
    ignore_models=None,
    comment=None,
    model_use_vars=None,
):
    """Compute median or mean model based on input models

    Note
    ----
    - BETA version that will likely undergo revisions.
    - Time selection currently not properly handled

    Parameters
    ----------
    cfg : AerocomEvaluation
        analysis instance
    var_name : str
        name of variable
    model_names : list, optional
        list of model names. If None, all entries in input engine are used.
    ts_type : str, optional
        output freq. Defaults to monthly.
    lat_res_deg : int, optional
        output latitude resolution, defaults to 2 degrees.
    lon_res_deg : int, optional
        output longitude resolution, defaults to 3 degrees.
    data_id : str, optional
        output data_id of ensemble model.
    avg_how : str, optional
        how to compute averages (choose from mean or median), defaults to
        "median".
    extract_surface : bool
        if True (and if data contains model levels), surface level is
        extracted
    ignore_models : list, optional
        list of models to be ignored
    comment : str, optional
        comment string added to metadata of output data objects.
    model_use_vars : dict, optional
        model variables to be used.


    Returns
    -------
    GriddedData
        ensemble model for input variable computed averaged using median or
        mean (input avg_how). Default is median.
    GriddedData
        corresponding diversity field, if avg_how is "mean", then computed
        using definition from
        Textor et al., 2006 (ACP) DOI: 10.5194/acp-6-1777-2006. If avg_how
        is "median" then interquartile range is used (Q3-Q1)/Q2
    GriddedData or None
        Q1 field (only output if avg_how is median)
    GriddedData or None
        Q3 field (only output if avg_how is median)
    GriddedData or None
        standard deviation field (only output if avg_how is mean)
    """
    if not isinstance(cfg, ExperimentProcessor):
        raise ValueError("invalid input, need ExperimentProcessor")
    cfg.cfg._check_time_config()
    if ts_type is None:
        ts_type = "monthly"
    if avg_how is None:
        avg_how = "median"
    if model_use_vars is None:
        model_use_vars = {}
    if ignore_models is None:
        ignore_models = []

    if avg_how == "mean":
        avg_fun = np.mean
    elif avg_how == "median":
        avg_fun = np.median
    else:
        raise ValueError(f"Invalid input for avg_how {avg_how}")

    if data_id is None:
        data_id = f"AEROCOM-{avg_how.upper()}"

    if model_names is None:
        model_names = list(cfg.cfg.model_cfg)

    if len(ignore_models) > 0:
        models = []
        for model in model_names:
            if model not in ignore_models:
                models.append(model)
    else:
        models = model_names

    if not len(models) > 1:
        raise ValueError("Need more than one model to compute average...")

    dummy = make_dummy_cube_latlon(lat_res_deg=lat_res_deg, lon_res_deg=lon_res_deg)

    loaded = []
    from_files = []
    from_models = []
    from_vars = []
    models_failed = []

    unit_out = get_variable(var_name).units

    for m in models:
        mname = m.model_name
        logger.info(f"Adding {mname} ({var_name})")

        mid = cfg.cfg.model_cfg.get_entry(mname).model_id
        if mid == data_id or mname == data_id:
            continue

        read_var = var_name
        col = cfg.get_colocator(model_name=mname)
        if mname in model_use_vars:
            muv = model_use_vars[mname]
            if var_name in muv:
                read_var = muv[var_name]

        try:
            data = col.get_model_data(read_var)
            if not data.units == unit_out:
                data.convert_unit(unit_out)

            elif not data.longitude.circular:
                if not data.check_lon_circular():
                    raise Exception(f"Longitude of {mname} is not circular...")
            data.reorder_dimensions_tseries()
            data = data.resample_time(ts_type)
            if data.ndim == 4:
                if extract_surface:
                    data = data.extract_surface_level()
                else:
                    raise NotImplementedError("Cannot process ModelLevel fields yet")
            data = data.regrid(dummy)
            logger.info("Success!")
        except Exception as e:
            models_failed.append(mid)
            logger.info(f"Failed! Reason: {e}")
            continue

        loaded.append(data.cube.data)
        from_files.extend(data.from_files)
        from_models.append(data.data_id)
        from_vars.append(data.var_name)

    if not len(loaded) > 1:
        raise ValueError("Can only compute average if more than one model is available")

    from_files = [os.path.basename(f) for f in from_files]

    dims = [data.time, dummy.coord("latitude"), dummy.coord("longitude")]

    # the merged data objects
    arr = np.asarray(loaded)

    # average (mean or median)
    avgarr = avg_fun(arr, axis=0)

    if avg_how == "mean":
        stdarr = np.std(arr, axis=0)
        divarr = np.std(arr / avgarr, axis=0) * 100
    else:
        q1arr = np.quantile(arr, 0.25, axis=0)
        q3arr = np.quantile(arr, 0.75, axis=0)
        divarr = (q3arr - q1arr) / avgarr * 100

    if comment is None:
        comment = f"Ensemble {avg_how} for variable {var_name}. "

    # median or mean
    avg_out = GriddedData(
        numpy_to_cube(
            avgarr,
            dims=dims,
            var_name=var_name,
            units=data.units,
            ts_type=ts_type,
            data_id=data_id,
            from_files=from_files,
            from_models=from_models,
            from_vars=from_vars,
            models_failed=models_failed,
            comment=comment,
        )
    )

    commentdiv = comment + " Diversity field in units of % (IQR for median, std for mean)"

    # IQR or std based diversity
    div_out = GriddedData(
        numpy_to_cube(
            divarr,
            dims=dims,
            var_name=f"{var_name}div",
            units="%",
            ts_type=ts_type,
            data_id=data_id,
            from_files=from_files,
            from_models=from_models,
            from_vars=from_vars,
            models_failed=models_failed,
            comment=commentdiv,
        )
    )

    std_out, q1_out, q3_out = None, None, None
    if avg_how == "mean":
        commentstd = comment + " Standard deviation"
        std_out = GriddedData(
            numpy_to_cube(
                stdarr,
                dims=dims,
                var_name=f"{var_name}std",
                units=data.units,
                ts_type=ts_type,
                data_id=data_id,
                from_files=from_files,
                from_models=from_models,
                from_vars=from_vars,
                models_failed=models_failed,
                comment=commentstd,
            )
        )
    else:
        commentq1 = comment + " First quantile."
        q1_out = GriddedData(
            numpy_to_cube(
                q1arr,
                dims=dims,
                var_name=f"{var_name}q1",
                units=data.units,
                ts_type=ts_type,
                data_id=data_id,
                from_files=from_files,
                from_models=from_models,
                from_vars=from_vars,
                models_failed=models_failed,
                comment=commentq1,
            )
        )

        commentq3 = comment + " Third quantile."
        q3_out = GriddedData(
            numpy_to_cube(
                q3arr,
                dims=dims,
                var_name=f"{var_name}q3",
                units=data.units,
                ts_type=ts_type,
                data_id=data_id,
                from_files=from_files,
                from_models=from_models,
                from_vars=from_vars,
                models_failed=models_failed,
                comment=commentq3,
            )
        )

    return (avg_out, div_out, q1_out, q3_out, std_out)
