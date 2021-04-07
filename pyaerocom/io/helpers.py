#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
I/O helper methods of the pyaerocom package
"""
from collections import OrderedDict as od
from datetime import datetime
import os
import shutil
from time import time

from pyaerocom import const
from pyaerocom.io import AerocomBrowser
from pyaerocom.exceptions import (VarNotAvailableError, VariableDefinitionError)

#: country code file name
#: will be prepended with the path later on
COUNTRY_CODE_FILE = 'country_codes.json'

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
    if os.path.exists(loc_remote): # remote exists
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
            const.print_log.info('Copied EBAS SQL database to {}\n'
                                'Elapsed time: {:.3f} s'
                                .format(loc_local, time() - t0))

            return loc_local
        except Exception as e:
            const.print_log.warning('Failed to copy EBAS SQL database. '
                                   'Reason: {}'.format(repr(e)))
            return loc_remote
    return loc_remote

def aerocom_savename(data_id, var_name, vert_code, year, ts_type):
    """Generate filename in AeroCom conventions

    ToDo: complete docstring
    """
    return ('aerocom3_{}_{}_{}_{}_{}.nc'
            .format(data_id, var_name, vert_code, year, ts_type))

def _print_read_info(i, mod, tot_num, last_t, name, logger):
    """Helper for displaying standardised output in reading classes

    Not to be used directly
    """
    t = datetime.now()
    logger.info("Reading files {}-{} of {} ({}) | {} (delta = {} s')"
                .format(i+1,i+1+mod, tot_num, name,
                        t.strftime('%H:%M:%S'),
                        (t-last_t).seconds))
    return t

def get_metadata_from_filename(filename):
    """Try access metadata information from filename"""
    from pyaerocom.io.fileconventions import FileConventionRead
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
    from pyaerocom._lowlevel_helpers import BrowseDict
    valid = BrowseDict()
    values = BrowseDict()
    info = BrowseDict()
    with open(ebas_flags_csv) as fio:
        for line in fio:
            spl = line.strip().split(',')
            num = int(spl[0].strip())
            try:
                val_str = spl[-1][1:-1]
            except Exception:
                raise IOError('Failed to read flag information in row {} '
                              '(Check if entries in ebas_flags.csv are quoted)'
                              .format(line))
            info_str = ','.join(spl[1:-1])
            try:
                info_str = info_str[1:-1]
            except Exception:
                raise IOError('Failed to read flag information in row {} '
                              '(Check if entries in ebas_flags.csv are quoted)'
                              .format(line))
            isvalid = True if val_str == 'V' else False
            valid[num] = isvalid
            values[num] = val_str
            info[num] = info_str
    result = BrowseDict()
    result.valid = valid
    result.info = info
    result.vals = values
    return result

def add_file_to_log(filepath, err_msg):

    try:
        dirname = os.path.dirname(filepath)
        spl = dirname.split(os.sep)
        if spl[-1].lower() == 'renamed':
            model_or_obs_id = spl[-2]
        else:
            model_or_obs_id = spl[-1]
    except Exception:
        model_or_obs_id = 'others'
    try:
        logdir = const.LOGFILESDIR
        found = False
        logfile = os.path.join(logdir, model_or_obs_id + '.log')
        if os.path.exists(logfile):
            with open(logfile, 'r') as f:
                for line in f:
                    if filepath == line.strip():
                        found = True
                        break

        if not found:
            with open(logfile, 'a+') as f:
                f.write(filepath + '\n')
            with open(os.path.join(logdir, model_or_obs_id + '_ERR.log'), 'a+') as ferr:
                ferr.write('{}\n{}\n\n'.format(filepath,
                                               err_msg))
    except Exception as e:
        from pyaerocom import print_log
        const.WRITE_FILEIO_ERR_LOG = False
        print_log.info('Failed to write to file-read error logging ({}). '
                       'Deactiving lgging'.format(repr(e)))

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
    if not var_name in const.VARS:
        raise VarNotAvailableError('No such variable {}. Check variables.ini'.format(var_name))
    name = const.VARS[var_name].standard_name
    if name is None:
        raise VariableDefinitionError('standard_name not defined for variable')
    return name

def search_data_dir_aerocom(name_or_pattern, ignorecase=True):
    """Search Aerocom data directory based on model / data ID
    """
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
    if not obs_id in const.OBSLOCS_UNGRIDDED:
        raise ValueError("Observation network ID {} does not exist"
                         .format(obs_id))

    data_dir = const.OBSLOCS_UNGRIDDED[obs_id]
    if not os.path.exists(data_dir):
        raise IOError("Data directory {} of observation network {} does not "
                      "exists".format(data_dir, obs_id))
    return data_dir

def save_dict_json(d, fp, ignore_nan=True, indent=None):
    """Save a dictionary as json file using :func:`simplejson.dump`

    Parameters
    ----------
    d : dict
        input dictionary
    fp : str
        filepath of json file

    """
    import simplejson
    with open(fp, 'w') as f:
        simplejson.dump(d, f, ignore_nan=ignore_nan, indent=indent)

def search_names(update_inifile=True, check_nc_file=True):
    """Search model IDs in database

    Parameters
    ----------
    update_inifile : bool
        if True, the file *names.txt* will be updated. The file is located
        in the installation *data* directory.
    check_nc_file : bool
        If True, only model IDs are included, for which at least one nc file
        can be detected in the corresponding renamed sub directory
    """
    names = []
    for mdir in const.DATA_SEARCH_DIRS:
        print("\n%s\n" %mdir)
        sub = os.listdir(mdir)
        for item in sub:
            path = os.path.join(mdir, item, "renamed")
            if os.path.isdir(path):
                print("\n%s\n" %path)
                add = True
                if check_nc_file:
                    add = False
                    for name in os.listdir(path):
                        if name.endswith(".nc"):
                            add = True
                            break
                if add:
                    names.append(item)
    names = sorted(od.fromkeys(names))
    if update_inifile:
        from pyaerocom import __dir__
        fpath = os.path.join(__dir__, "data", "names.txt")
        f = open(fpath, "w")
        for name in names:
            f.write("%s\n" %name)
        f.close()
    return names

def get_all_names():
    """Try to import all model IDs from file names.txt in data directory"""
    from pyaerocom import __dir__
    try:
        with open(os.path.join(__dir__, "data", "names.txt")) as f:
            names = f.read().splitlines()
        f.close()
    except Exception:
        try:
            names = search_names()
        except Exception:
            raise Exception("Failed to access model IDs")
    return names

def get_country_name_from_iso(iso_code=None,
                              filename=None,
                              return_as_dict=False):
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
    if iso_code is None:
        return_as_dict = True

    if filename is None:
        #set default file name
        from pyaerocom import __dir__
        filename = os.path.join(__dir__, 'data', COUNTRY_CODE_FILE)

    import simplejson as json
    with open(filename) as fh:
        json_data = json.load(fh)

    iso_dict = {}
    for indict in json_data:
        iso_dict[indict['alpha-2']] = indict['name']

    if return_as_dict:
        return iso_dict
    else:
        try:
            ret_val = iso_dict[iso_code.upper()]
        except KeyError:
            ret_val = ''
            raise ValueError
        return ret_val



if __name__=="__main__":
    #names = search_names()
    names = get_all_names()
