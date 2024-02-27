from __future__ import annotations

import logging
import os

import numpy as np
import simplejson

logger = logging.getLogger(__name__)


FLOAT_DECIMALS = 5


def set_float_serialization_precision(precision: int) -> None:
    """update `FLOAT_DECIMALS`"""
    global FLOAT_DECIMALS
    FLOAT_DECIMALS = precision


def round_floats(in_data: float | dict | list | tuple) -> float | dict | list | tuple:
    """
    round all floats in `in_data` to `FLOAT_DECIMALS` precission.
    For nested structures, this method is called recursively to go through
    all levels

    Parameters
    ----------
    in_data : float, dict, tuple, list
        data structure whose numbers should be limited in precision

    Returns
    -------
    in_data
        all the floats in in_data with limited precision
        tuples in the structure have been converted to lists to make them mutable

    """

    if isinstance(in_data, (float, np.float32, np.float16, np.float128, np.float64)):
        # np.float64, is an aliase for the Python float, but is mentioned here for completeness
        # note that round and np.round yield different results with the Python round being mathematically correct
        # details are here:
        # https://numpy.org/doc/stable/reference/generated/numpy.around.html#numpy.around
        # use numpy around for now
        return np.around(in_data, FLOAT_DECIMALS)
    elif isinstance(in_data, (list, tuple)):
        return [round_floats(v) for v in in_data]
    elif isinstance(in_data, dict):
        return {k: round_floats(v) for k, v in in_data.items()}
    return in_data


def read_json(file_path):
    """Read json file

    Parameters
    ----------
    file_path : str
        json file path

    Returns
    -------
    dict
        content as dictionary
    """
    with open(file_path) as f:
        data = simplejson.load(f, allow_nan=True)
    return data


def write_json(data_dict, file_path, **kwargs):
    """Save json file

    Parameters
    ----------
    data_dict : dict
        dictionary that can be written to json file
    file_path : str
        output file path
    **kwargs
        additional keyword args passed to :func:`simplejson.dumps` (e.g.
        indent, )
    """
    kwargs.update(ignore_nan=True)
    with open(file_path, "w") as f:
        simplejson.dump(round_floats(in_data=data_dict), f, allow_nan=True, **kwargs)


def check_make_json(fp, indent=4):
    """
    Make sure input json file exists

    Parameters
    ----------
    fp : str
        filepath to be checked (must end with .json)
    indent : int
        indentation of json file

    Raises
    ------
    ValueError
        if filepath does not exist.

    Returns
    -------
    str
        input filepath.

    """
    fp = str(fp)
    if not fp.endswith(".json"):
        raise ValueError("Input filepath must end with .json")
    if not os.path.exists(fp):
        logger.info(f"Creating empty json file: {fp}")
        write_json({}, fp, indent=indent)
    return fp
