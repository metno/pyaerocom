"""
I/O helper methods of the pyaerocom package
"""

from __future__ import annotations

import logging
import os
import shutil
from datetime import datetime
from pathlib import Path
from time import time

import simplejson as json

from pyaerocom import const
from pyaerocom.data import resources
from pyaerocom.exceptions import VariableDefinitionError, VarNotAvailableError
from pyaerocom.io import AerocomBrowser

logger = logging.getLogger(__name__)


#: country code file name
#: will be prepended with the path later on
COUNTRY_CODE_FILE = "country_codes.json"


def _check_ebas_db_local_vs_remote(loc_remote, loc_local):
    """
    Check and if applicable, copy ebas_file_index.sqlite3 into cache dir

    Note
    ----
    This may speedup things if remote location is on a mounted server location.
    Nothing the user should worry about in any case.

    Parameters
    ----------
    loc_remote : str
        remote location of ebas_file_index.sqlite3
    loc_local : str
        local (cached) location of ebas_file_index.sqlite3

    Returns
    -------
    str
        valid location of ebas_file_index.sqlite3 that is supposed to be used

    """
    if os.path.exists(loc_remote):  # remote exists
        if os.path.exists(loc_local):
            chtremote = os.path.getmtime(loc_remote)
            chtlocal = os.path.getmtime(loc_local)
            if chtlocal == chtremote:
                return loc_local

        # changing time differs -> try to copy to local and if that
        # fails, use remote location
        try:
            t0 = time()
            shutil.copy2(loc_remote, loc_local)
            logger.info(
                f"Copied EBAS SQL database to {loc_local}\nElapsed time: {time() - t0:.3f} s"
            )

            return loc_local
        except Exception as e:
            logger.warning(f"Failed to copy EBAS SQL database. Reason: {repr(e)}")
            return loc_remote
    return loc_remote


def aerocom_savename(data_id, var_name, vert_code, year, ts_type):
    """Generate filename in AeroCom conventions

    ToDo: complete docstring
    """
    return f"aerocom3_{data_id}_{var_name}_{vert_code}_{year}_{ts_type}.nc"


def _print_read_info(i, mod, tot_num, last_t, name, logger):  # pragma: no cover
    """Helper for displaying standardised output in reading classes

    Not to be used directly
    """
    t = datetime.now()
    logger.info(
        f"Reading files {i + 1}-{i + 1 + mod} of {tot_num} "
        f"({name}) | {t:%T} (delta = {(t - last_t).seconds} s')"
    )
    return t


def get_metadata_from_filename(filename):
    """Try access metadata information from filename"""
    from pyaerocom.io.file_conventions import FileConventionRead

    fc = FileConventionRead().from_file(filename)
    return fc.get_info_from_file(filename)


def read_ebas_flags_file(ebas_flags_csv):
    """Reads file ebas_flags.csv

    Parameters
    ----------
    ebas_flags_csv : str
        file containing flag info

    Returns
    -------
    dict
        dict with loaded flag info
    """
    valid = {}
    values = {}
    info = {}
    with open(ebas_flags_csv) as fio:
        for line in fio:
            spl = line.strip().split(",")
            num = int(spl[0].strip())
            try:
                val_str = spl[-1][1:-1]
            except Exception:
                raise OSError(
                    f"Failed to read flag information in row {line} "
                    f"(Check if entries in ebas_flags.csv are quoted)"
                )
            info_str = ",".join(spl[1:-1])
            try:
                info_str = info_str[1:-1]
            except Exception:
                raise OSError(
                    f"Failed to read flag information in row {line} "
                    f"(Check if entries in ebas_flags.csv are quoted)"
                )
            isvalid = True if val_str == "V" else False
            valid[num] = isvalid
            values[num] = val_str
            info[num] = info_str
    result = {}
    result["valid"] = valid
    result["info"] = info
    result["vals"] = values
    return result


def add_file_to_log(filepath, err_msg):
    """
    Add input file path to error logdir

    The logdir location can be accessed via :attr:`pyaerocom.const.LOGFILESDIR`

    Parameters
    ----------
    filepath : str or Path
        path of file that has an error
    err_msg : str
        Problem associated with input file

    """
    if isinstance(filepath, Path):
        filepath = str(filepath)
    try:
        dirname = os.path.dirname(filepath)
        spl = dirname.split(os.sep)
        if spl[-1].lower() == "renamed":
            model_or_obs_id = spl[-2]
        else:
            model_or_obs_id = spl[-1]
    except Exception:
        model_or_obs_id = "others"

    logdir = const.LOGFILESDIR

    logfile = os.path.join(logdir, f"{model_or_obs_id}.log")

    if os.path.exists(logfile):  # check if this file is already flagged
        with open(logfile) as f:
            for line in f:
                if filepath == line.strip():
                    return  # file is already flagged -> ignore

    logfile_err = os.path.join(logdir, f"{model_or_obs_id}_ERR.log")
    with open(logfile, "a+") as f:
        f.write(f"{filepath}\n")
    with open(logfile_err, "a+") as ferr:
        ferr.write(f"{filepath}\n{err_msg}\n\n")


def get_standard_name(var_name):
    """Get standard name of aerocom variable

    Parameters
    ----------
    var_name : str
        HTAP2 variable name

    Returns
    --------
    str
        corresponding standard name

    Raises
    ------
    VarNotAvailableError
        if input variable is not defined in *variables.ini* file
    VariableDefinitionError
        if standarad name is not set for variable in *variables.ini* file
    """
    if var_name not in const.VARS:
        raise VarNotAvailableError(f"No such variable {var_name}. Check variables.ini")
    name = const.VARS[var_name].standard_name
    if name is None:
        raise VariableDefinitionError("standard_name not defined for variable")
    return name


def search_data_dir_aerocom(name_or_pattern, ignorecase=True):
    """Search Aerocom data directory based on model / data ID"""
    browser = AerocomBrowser()
    return browser.find_data_dir(name_or_pattern, ignorecase)


def get_all_supported_ids_ungridded():
    """Get list of datasets that are supported by :class:`ReadUngridded`

    Returns
    -------
    list
        list with supported network names
    """
    from pyaerocom.io import ReadUngridded

    return ReadUngridded().SUPPORTED_DATASETS


def get_obsnetwork_dir(obs_id):
    """Returns data path for obsnetwork ID

    Parameters
    ----------
    obs_id : str
        ID  of obsnetwork (e.g. AeronetSunV2Lev2.daily)

    Returns
    -------
    str
        corresponding directory from ``pyaerocom.const``

    Raises
    ------
    ValueError
        if obs_id is invalid
    IOError
        if directory does not exist
    """
    if obs_id not in const.OBSLOCS_UNGRIDDED:
        raise ValueError(f"Observation network ID {obs_id} does not exist")

    data_dir = const.OBSLOCS_UNGRIDDED[obs_id]
    if not os.path.exists(data_dir):
        raise FileNotFoundError(
            f"Data directory {data_dir} for observation network {obs_id} does not exist"
        )
    return data_dir


def get_country_name_from_iso(
    iso_code: str | None = None, filename: str | Path | None = None, return_as_dict: bool = False
):
    """get the country name from the 2 digit iso country code

    the underlaying json file was taken from this github repository
    https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes

    Parameters
    ----------
    iso_code : :obj:`str`
        string containing the 2 character iso code of the country (e.g. no for Norway)
    filename : :obj:`str` , optional
        optional string with the json file to read
    return_as_dict : :obj:`bool`, optional
        flag to get the entire list of countries as a dictionary with the country codes
        as keys and the country names as value
        Useful if you have to get the names for a lot of country codes

    Returns
    -------
    string with country name or dictionary with iso codes as keys and the country names as values
    empty string if the country code was not found


    Raises
    ------
    ValueError
        if the country code ins invalid
    """
    if filename is None:
        # set default file name
        with resources.path("pyaerocom.data", COUNTRY_CODE_FILE) as path:
            filename = path

    if isinstance(filename, str):
        filename = Path(filename)
    json_data = json.loads(filename.read_text())

    iso_dict = {}
    for indict in json_data:
        iso_dict[indict["alpha-2"]] = indict["name"]

    if iso_code is None or return_as_dict:
        return iso_dict

    return iso_dict[iso_code.upper()]
