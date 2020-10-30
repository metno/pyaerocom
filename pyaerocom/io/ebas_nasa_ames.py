#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pyearocom module for reading and processing of EBAS NASA Ames files

For details on the file format see `here <https://ebas-submit.nilu.no/
Submit-Data/Getting-started>`__
"""
import os
import numpy as np
import pandas as pd
from collections import OrderedDict as od
from datetime import datetime
from pyaerocom._lowlevel_helpers import str_underline, dict_to_str
from pyaerocom.exceptions import TimeZoneError
from pyaerocom import const

class NasaAmesReadError(IOError):
    pass

class NasaAmesVariableError(AttributeError):
    pass

class EbasColDef(dict):
    """Dict-like object for EBAS NASA Ames column definitions

    Note
    ----
    The meta attribute name 'unit' can also be accessed using the CF attr name
    'units'

    Attributes
    ----------
    name : str
        column name
    unit : str
        unit of data in column (if applicable)
    is_var : bool
        True if column corresponds to variable data, False if not
    is_flag : bool
        True, if column corresponds to Flag column, False if not
    flag_col : int
        column number of flag column that corresponds to this data column (only
        relevant if :attr:`is_var` is True)

    Parameters
    ----------
    name : str
        column name
    is_var : bool
        True if column corresponds to variable data, False if not
    is_flag : bool
        True, if column corresponds to Flag column, False if not
    unit : :obj:`str`, optional
        unit of data in column (if applicable)
    flag_col : :obj:`str`, optional
        ``name`` of flag column that corresponds to this data colum (only
        relevant if :attr:`is_var` is True)
    """
    def __init__(self, name, is_var, is_flag, unit="1"):
        self.name = name
        self.unit = unit
        self.is_var = is_var
        self.is_flag = is_flag
        self.flag_col = None

    def get_wavelength_nm(self):
        """Try to access wavelength information in nm (as float)"""
        if not 'wavelength' in self:
            raise KeyError('Column variable {} does not contain wavelength '
                           'information'.format(self.name))
        elif not 'nm' in self.wavelength:
            raise NotImplementedError('Wavelength definition is not in nm')
        return float(self.wavelength.split('nm')[0].strip())

    def to_dict(self, ignore_keys=['is_var', 'is_flag', 'flag_col',
                                   'wavelength_nm']):
        d = {}
        for k, v in self.items():
            if k in ignore_keys:
                continue
            elif k == 'unit':
                k ='units'
            d[k] = v
        return d

    def __getitem__(self, key): # add support for units attr (CF standard name)
        if key == 'units':
            key = 'unit'
        return super(EbasColDef, self).__getitem__(key)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, val):
        self[key] = val

    def to_str(self):
        s = '{}_{}'.format(self.name, self.unit)
        if 'wavelength' in self:
            s += '_{}nm'.format(self.get_wavelength_nm())
        if 'matrix' in self:
            s += '_{}'.format(self.matrix)
        if 'statistics' in self:
            s += '_{}'.format(self.statistics)
        if 'data_level' in self:
            s += '_L{}'.format(self.data_level)
        return s

    def __repr__(self):
        s = "{}: ".format(type(self).__name__)
        for k, v in self.items():
            s += "{}={}, ".format(k, v)
        return s

    def __str__(self):
        head = "Pyaerocom {}".format(type(self).__name__)
        s = "{}\n{}\n".format(head, len(head)*"-")
        for k, v in self.items():
            s += "{}: {}\n".format(k, v)
        return s

def _readline_ref_and_revision(line):
    spl = line.strip().split()
    basedate = np.datetime64(datetime.strptime('{}{}{}'.format(spl[0],
                                               spl[1], spl[2]), "%Y%m%d"), 's')
    rev = np.datetime64(datetime.strptime('{}{}{}'.format(spl[3],
                                               spl[4], spl[5]), "%Y%m%d"), 's')
    return [basedate, rev]

class NasaAmesHeader(object):
    """Header class for Ebas NASA Ames file

    Note
    ----
    Is used in :class:`EbasNasaAmesFile` and should not be used directly.

    Attributes
    -----------

    """
    _NUM_FIXLINES = 13
    _HEAD_ROWS_MANDATORY = [0,5,8,9,10,11]

    #conversion methods for first 13 header lines of
    CONV_STR = lambda l : str(l.strip())
    CONV_PI = lambda l : '; '.join([x.strip() for x in l.split(';')])
    CONV_MULTIINT = lambda l : [int(x) for x in l.strip().split()]
    CONV_MULTIFLOAT = lambda l : [float(x) for x in l.strip().split()]
    CONV_INT = lambda l : int(l.strip())
    CONV_FLOAT = lambda l : float(l.strip())
    _STARTDATE_FMT = "%Y%m%d%H%M%S"

    # the parameters that are always in the beginning of the file
    _H_FIXLINES_YIELD = [["num_head_lines", "num_head_fmt"], #line 1
                         "data_originator", #line 2
                         "sponsor_organisation", #3
                         "submitter", #4
                         "project_association", #5
                         ["vol_num", "vol_totnum"], #6
                         ["ref_date", "revision_date"], #7
                         "freq", #8
                         "descr_time_unit", #9
                         "num_cols_dependent", #10
                         "mul_factors", #11
                         "vals_invalid", #12
                         "descr_first_col", #13
                         ]
    # conversion methods are defined above
    _H_FIXLINES_CONV = [CONV_MULTIINT, #1 -> yields 2
                        CONV_PI, #2
                        CONV_STR, #3
                        CONV_STR, #4
                        CONV_STR, #5
                        CONV_MULTIINT, #6
                        _readline_ref_and_revision, #7 lambda l : [x.strip() for x in l.strip().split("     ")], #7
                        CONV_FLOAT, #8
                        CONV_STR, #9
                        CONV_INT, #10
                        CONV_MULTIFLOAT, #11
                        CONV_MULTIFLOAT, #12
                        CONV_STR] #13

    def __init__(self, **kwargs):
        self._head_fix = od(num_head_lines = np.nan,
                            num_head_fmt = np.nan,
                            data_originator = "",
                            sponsor_organisation = "",
                            submitter = "",
                            project_association = "",
                            vol_num = np.nan,
                            vol_totnum = np.nan,
                            ref_date = np.nan,
                            revision_date = np.nan,
                            freq = np.nan,
                            descr_time_unit = "",
                            num_cols_dependent = np.nan,
                            mul_factors = [],
                            vals_invalid = [],
                            descr_first_col = "")
        self._var_defs = []
        self._meta = od()
        self.update(**kwargs)

    @property
    def head_fix(self):
        """Dictionary containing fixed header info (that is always available)"""
        return self._head_fix

    @property
    def var_defs(self):
        """List containing column variable definitions

        List index is column index in file and value is instance of
        :class:`EbasColDef`
        """
        return self._var_defs

    @property
    def meta(self):
        """Meta data dictionary (specific for this file)"""
        return self._meta

    def update(self, **kwargs):
        for k, v in kwargs.items():
            try:
                self[k] = v
            except Exception:
                const.logger.warning("Invalid attribute: {}".format(k))

    def __getattr__(self, key):
        if key in self._head_fix:
            return self._head_fix[key]
        elif key in self._meta:
            return self._meta[key]
        else:
            raise AttributeError("Invalid attribute: {}".format(key))

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __setitem__(self, key, val):
        if key in self._head_fix:
            self._head_fix[key] = val
        else:
            self._meta[key] = val

    def __str__(self):
        head = "{}".format(type(self).__name__)
        s = "{}\n{}\n".format(head, len(head)*"-")
        s += dict_to_str(self._head_fix)
        s += "\n\n{}".format(str_underline("Column variable definitions",
                                           indent=3))
        for item in self._var_defs:
            s += "\n   {}".format(repr(item))
        s += "\n\n{}".format(str_underline("EBAS meta data",
                                             indent=3))
        s += dict_to_str(self.meta)

        return s

class EbasFlagCol(object):
    """Simple helper class to decode and interpret EBAS flag columns

    Attributes
    ----------
    info : EbasColDef
        EBAS column definition information for flag column (from file header)
    raw_data : ndarray
        raw flag column (containing X-digit floating point numbers)

    """
    #from pyaerocom import const
    #_FLAG_INFO = const.EBAS_FLAG_INFO
    def __init__(self, raw_data, info, interpret_on_init=True):
        if not raw_data.ndim == 1:
            raise AttributeError("Need one dimensional numpy array for flag "
                                 "column")
        self.info = info
        self.raw_data = raw_data

        self._decoded = None
        self._valid = None

        if interpret_on_init:
            self.decode()

    @property
    def FLAG_INFO(self):
        """Detailed information about EBAS flag definitions"""
        return const.ebas_flag_info

    @property
    def decoded(self):
        """Nx3 numpy array containing decoded flag columns"""
        if self._decoded is None:
            self.decode()
        return self._decoded

    @property
    def valid(self):
        """Boolean array specifying valid and invalid measurements"""
        if self._valid is None:
            self.decode()
        return self._valid

    def decode(self):
        """Decode raw flag column"""
        flags = np.zeros((len(self.raw_data), 3)).astype(int)
        mask = self.raw_data.astype(bool) # rmooves all points that are 0, i.e. that contain no flag (valid measurements)
        valid = np.ones_like(self.raw_data).astype(bool)
        not_ok = self.raw_data[mask]
        if len(not_ok) > 0:
            _decoded = []
            _valid = []
            for flag in not_ok:
                item = "{:.9f}".format(flag).split(".")[1]
                vals = [int(item[:3]), int(item[3:6]), int(item[6:9])]
                _invalid = False
                for val in vals:
                    if val == 100:
                        _invalid = False
                        break # since all other flags are irrelevant if 100 is flagged
                    elif val in self.FLAG_INFO.valid and not self.FLAG_INFO.valid[val]: #is invalid
                        _invalid = True

                _decoded.append(vals)
                _valid.append(not _invalid)

            flags[mask] = np.asarray(_decoded)
            valid[mask] = _valid

        self._valid = valid
        self._decoded = flags

class EbasNasaAmesFile(NasaAmesHeader):
    """EBAS NASA Ames file interface

    Class interface for reading and processing of EBAS NASA Ames file

    Attributes
    ----------
    time_stamps : ndarray
        array containing datetime64 objects with timestamps
    flags : dict
        dictionary containing :class:`EbasFlagCol` objects for each column
        containing flags

    Parameters
    ----------
    file : :obj:`str`, optional
        EBAS NASA Ames file. if valid file path, then the file is read on
        init (please note following options for import)
    only_head : bool
        read only file header
    replace_invalid_nan : bool
        replace all invalid values in the table by NaNs. The invalid values for
        each dependent data column are identified based on the information in
        the file header.
    convert_timestamps : bool
        compute array of numpy datetime64 timestamps from numeric timestamps
        in data
    evaluate_flags : bool
        if True, all flags in all flag columns are decoded from floating
        point representation to 3 integers, e.g.
        0.111222333 -> 111 222 333
    quality_check : bool
        perform quality check after import (for details see
        :func:`_quality_check`)
    **kwargs
        optional input args that are passed to init of :class:`NasaAmesHeader`
        base class

    """
    TIMEUNIT2SECFAC = dict(days = 3600*24,
                           Days = 3600*24)

    ERR_LOW_STATS = 'percentile:15.87'
    ERR_HIGH_STATS = 'percentile:84.13'
    def __init__(self, file=None, only_head=False, replace_invalid_nan=True,
                 convert_timestamps=True, evaluate_flags=False,
                 quality_check=True, **kwargs):
        super(EbasNasaAmesFile, self).__init__(**kwargs)
        self._data_header = [] #Header line of data block
        self._data = [] #data block

        self.time_stamps = None

        self.flag_col_info = od()

        self.file = None

        if file is not None:
            if not os.path.exists(file):
                raise IOError("File {} does not exists".format(file))
            self.read_file(file, only_head, replace_invalid_nan,
                           convert_timestamps, evaluate_flags,
                           quality_check)

    @property
    def data(self):
        """2D numpy array containing data table"""
        return self._data

    @property
    def data_header(self):
        return self._data_header

    @property
    def shape(self):
        """Shape of data array"""
        return self.data.shape

    @property
    def col_num(self):
        """Number of columns in table"""
        return self.num_cols_dependent + 1

    @property
    def col_names(self):
        """Column names of table"""
        #cols = [x["name"] for x in self.var_defs]
        return [x["name"] for x in self.var_defs]

    @property
    def col_names_vars(self):
        """Names of all columns that are flagged as variables"""
        return [x.name for x in self.var_defs if x.is_var]

    @property
    def col_nums_vars(self):
        """Column index number of all variables"""
        return [i for (i, item) in enumerate(self.var_defs) if item.is_var]

    @property
    def base_date(self):
        """Base date of data as numpy.datetime64[s]"""
        if not "timezone" in self.meta:
            raise AttributeError("Fatal: could not infer base date. Timezone "
                                 "is not available in file header")
        if not self.timezone.lower() == "utc":
            raise TimeZoneError("Timezones other than UTC are not yet supported")
        return self.ref_date
# =============================================================================
#         return np.datetime64(datetime.strptime(self.startdate, "%Y%m%d%H%M%S"),
#                              's')
# =============================================================================

    @property
    def time_unit(self):
        """Time unit of data"""
        return self.descr_time_unit.split()[0].strip()

    @staticmethod
    def numarr_to_datetime64(basedate, num_arr, mulfac_to_sec):
        """Convert array of numerical timestamps into datetime64 array

        Parameters
        ----------
        basedate : datetime64
            reference date
        num_arr : ndarray
            numerical time stamps relative to basedate
        mulfac_to_sec : float
            multiplicative factor to convert numerical values to unit of
            seconds
        Returns
        -------
        ndarray
            array containing timestamps as datetime64 objects
        """
        totnum = len(num_arr)
        if totnum == 0:
            raise AttributeError("No data available in file")
# =============================================================================
#         elif totnum == 1:
#             num_arr = np.asarray([num_arr])
# =============================================================================
        return basedate + (num_arr * mulfac_to_sec).astype("timedelta64[s]")

    def get_colnames_unique(self):
        """Create a list of unique column names"""
        names = []
        for i, colinfo in enumerate(self.var_defs):
            s = colinfo.to_str()
            if not s in names:
                names.append(s)
            else:
                s += '(Col{})'.format(i)
                names.append(s)
        return names

    def _find_col_matches(self, var_name=None, wavelength_nm=None,
                          statistics=None, data_level=None,  **kwargs):
        """Find indices of columns that match input constraints

        Parameters
        ----------
        var_name : :obj:`str`, optional
            EBAS variable name (e.g. aerosol_light_scattering_coefficient).
            If specified, only columns corresponding to this variable name
            will be extracted into the dataframe
        wavelength_nm : :obj:`int`, :obj:`tuple`, optional
            wavelength (or wavelength range -> list or tuple input) in nm. If
            specified, only columns containing wavelength dependent data as
            specified are extracted and put into the Dataframe
        statistics : :obj:`str`, optional
            specify column statistics (e.g. arithmetic mean)
        data_level : float
            data level of column

        """
        try: #statistics is defined globally
            stats_glob = self.statistics
        except Exception: #statistics is not defined globally
            stats_glob = None

        if isinstance(wavelength_nm, str):
            raise ValueError("Wavelength needs to be integer or float or range"
                             "(i.e. 2-element tuple or list)")

        try:
            if not len(wavelength_nm) == 2:
                raise Exception
            wvl_rng = True
        except Exception:
            wvl_rng = False

        if statistics is not None:
            if isinstance(statistics, str): # input for statistics is string, else ...
                stats_str = True
            else: # ... input for statistics is assumed to be tuple or list of strings
                stats_str = False
        if data_level is not None:
            try:
                data_level_glob = float(self.data_level)
                if not data_level_glob:
                    raise Exception #is undefined
            except Exception:
                data_level_glob = None
        cols = []
        for i, colinfo in enumerate(self.var_defs):
            if var_name is not None and not colinfo.name == var_name:
                continue
            if wavelength_nm is not None:
                try: #column contains wavalength information
                    wvl = colinfo.get_wavelength_nm()
                    if wvl_rng:
                        if not wavelength_nm[0] <= wvl <= wavelength_nm[1]:
                            continue
                    else:
                        if not wvl == wavelength_nm:
                            continue
                except Exception: #column does not contain wavelength information (skip)
                    continue
            if statistics is not None:
                if 'statistics' in colinfo:
                    col_stats = colinfo['statistics']
                else:
                    col_stats = stats_glob
                if col_stats is None: # no statistics info available for column
                    continue
                if stats_str and not col_stats == statistics:
                    continue
                elif not col_stats in statistics:
                    continue
            if data_level is not None:
                if 'data_level' in colinfo:
                    col_lev = float(colinfo.data_level)
                else:
                    col_lev = data_level_glob
                if col_lev is None:
                    continue
                if not col_lev == data_level:
                    continue
            cols.append(i)
        return cols

    def _find_col(self, var_name, statistics='arithmetic mean', **kwargs):
        idx = self._find_col_matches(var_name, statistics=statistics,
                                     **kwargs)
        #cols = self.get_colnames_unique()
        if len(idx) == 0:
            raise ValueError('No matches could be found for input specs')
        elif len(idx) > 1:

            msg = ('Multiple matches found for input variable, please specify '
                   'further constraints. The following column matches were '
                   'found:\n')
            for _idx in idx:
                msg += '{}\n'.format(self.var_defs[_idx])

            raise ValueError(msg)
        return idx[0]

    def to_dataframe(self, var_name=None, wavelength_nm=None,
                     statistics=None):
        """Convert table to dataframe

        Parameters
        ----------
        var_name : :obj:`str`, optional
            EBAS variable name (e.g. aerosol_light_scattering_coefficient).
            If specified, only columns corresponding to this variable name
            will be extracted into the dataframe
        wavelength_nm : :obj:`int`, :obj:`tuple`, optional
            wavelength (or wavelength range -> list or tuple input) in nm. If
            specified, only columns containing wavelength dependent data as
            specified are extracted and put into the Dataframe
        statistics : :obj:`str`, optional
            specify column statistics (e.g. arithmetic mean)

        """
        cols = self.get_colnames_unique()
        if all([x == None for x in (var_name, wavelength_nm, statistics)]):
            return pd.DataFrame(data=self.data,
                                index=self.time_stamps,
                                columns=cols)
        else:
            matches = self._find_col_matches(var_name, wavelength_nm,
                                             statistics)
            if len(matches) == 0:
                raise ValueError('No column matches could be found for input '
                                 'specs')
            _cols = []
            for idx in matches:
                _cols.append(cols[idx])
            return pd.DataFrame(data=self.data[:, matches],
                                index=self.time_stamps,
                                columns=_cols)

    def plot_var(self, var_name, statistics='arithmetic mean', ax=None,
                 style=None, **kwargs):
        """Plot time series of one column

        If percentiles are available, they will be plotted as shaded area

        Parameters
        ----------
        var_name : str
            EBAS variable name
        statistics : str
            statistics specifications
        """
        idx = self._find_col(var_name, statistics='arithmetic mean', **kwargs)
        colinfo = self.var_defs[idx]
        try :
            idx_err_low = self._find_col(var_name,
                                         statistics=self.ERR_LOW_STATS,
                                         **kwargs)
            idx_err_high = self._find_col(var_name,
                                          statistics=self.ERR_HIGH_STATS,
                                          **kwargs)
        except Exception:
            idx_err_high, idx_err_low = None, None
            print('Could not find percentile columns')

        s = pd.Series(self.data[:, idx], self.time_stamps)
        if s.isnull().all():
            raise ValueError('All values are NaN in column {} are NaN'.format(repr(colinfo)))

        if ax is None:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
        s.plot(style=style, ax=ax)
        return ax

    def assign_flagcols(self):
        _prev = 0
        for (idx, item) in enumerate(self.var_defs):
            if item.is_flag:
                for _idx in range(_prev, idx):
                    self.var_defs[_idx].flag_col=idx
                _prev = idx + 1

    def init_flags(self, evaluate=True):
        """Decode flag columns and store info in :attr:`flags`
        """
        for (idx, item) in enumerate(self.var_defs):
            if item.is_flag:
                data = self.data[:, idx]
                flag = EbasFlagCol(raw_data=data,
                                   info=item,
                                   interpret_on_init=evaluate)
                self.flag_col_info[idx] = flag

    def _set_invalid_flags_nan_col(self, colnum):
        raise NotImplementedError
        info = self.var_defs[colnum]
        flag_col = info.flag_col
        if flag_col is None:
            raise ValueError('No flag column is assigned to data column {}\n{}'
                             .format(colnum, info))

    def set_invalid_flags_nan(self, colnum=None):
        """Use flag column information to identify and remove invalid measurements"""
        if len(self.flag_col_info) == 0:
            self.init_flags()
        raise NotImplementedError

    def compute_time_stamps(self):
        """Compute time stamps from first two data columns"""
        if not self.var_defs[0].unit == self.var_defs[1].unit:
            raise NasaAmesReadError('2nd column is not endtime or does not '
                                    'have the same unit as 1st column (starttime)')
        offs = self.base_date
        unit = self.time_unit
        if not unit in self.TIMEUNIT2SECFAC:
            raise ValueError("Invalid unit for temporal resolution: {}".format(unit))
        mulfac = self.TIMEUNIT2SECFAC[unit]

        start = self.numarr_to_datetime64(offs, self.data[:,0], mulfac)
        stop = self.numarr_to_datetime64(offs, self.data[:,1], mulfac)

        self.time_stamps = start + (stop - start)*.5
        return (start, stop)

    def _quality_check(self):
        msgs = ""
        if not len(self.data_header) == len(self.var_defs):
            msgs += ("Mismatch between variable definitions in header and "
                     "number of data columns in table\n")
        if not "timezone" in self.meta:
            msgs += ("Timezone not defined in metadata")
        if msgs:
            raise AttributeError("Quality check failed. Messages: {}".format(msgs))

    def read_header(self, nasa_ames_file, quality_check=True):
        self.read_file(nasa_ames_file, only_head=True,
                       quality_check=quality_check)

    def read_file(self, nasa_ames_file, only_head=False,
                  replace_invalid_nan=True, convert_timestamps=True,
                  evaluate_flags=False, quality_check=False):
        """Read NASA Ames file

        Parameters
        ----------
        nasa_ames_file : str
            EBAS NASA Ames file
        only_head : bool
            read only file header
        replace_invalid_nan : bool
            replace all invalid values in the table by NaNs. The invalid values for
            each dependent data column are identified based on the information in
            the file header.
        convert_timestamps : bool
            compute array of numpy datetime64 timestamps from numeric timestamps
            in data
        evaluate_flags : bool
            if True, all data columns get assigned their corresponding flag
            column, the flags in all flag columns are decoded from floating
            point representation to 3 integers, e.g. 0.111222333 -> 111 222 333
            and if input ```replace_invalid_nan==True```, then the invalid
            measurements in each column are replaced with NaN's.
        quality_check : bool
            perform quality check after import (for details see
            :func:`_quality_check`)
        """
        const.logger.info("Reading NASA Ames file:\n{}".format(nasa_ames_file))
        lc = 0 #line counter
        dc = 0 #data block line counter
        mc = 0 #meta block counter
        END_VAR_DEF = np.nan #will be set (info stored in header)
        IN_DATA = False
        data = []
        _insert_invalid = None
        self.file = nasa_ames_file
        for line in open(nasa_ames_file):
            #print(lc, _NUM_FIXLINES, line)
            if IN_DATA: #in data block (end of file)
                if dc == 0:
                    const.logger.debug(line)
                try:
                    data.append(tuple([float(x.strip()) for x in line.strip().split()]))
                    #data.append([float(x.strip()) for x in line.strip().split()])
                except Exception as e:
                    data.append(_insert_invalid)
                    const.logger.warning("Failed to read data row {}. "
                                   "Error msg: {}".format(dc, repr(e)))
                dc += 1
            elif lc < self._NUM_FIXLINES: #in header section (before column definitions)
                try:
                    val = self._H_FIXLINES_CONV[lc](line)
                    attr = self._H_FIXLINES_YIELD[lc]
                    if isinstance(attr, list):
                        for i, attr_id in enumerate(attr):
                            self[attr_id] = val[i]
                    else:
                        self[attr] = val
                except Exception as e:
                    msg = ("Failed to read header row {}.\n{}\n"
                           "Error msg: {}".format(lc, line, repr(e)))
                    if lc in self._HEAD_ROWS_MANDATORY:
                        raise NasaAmesReadError("Fatal: {}".format(msg))
                    else:
                        const.logger.warning(msg)
            else: # behind header section and before data definition (contains column defs and meta info)
                if mc == 0: # still in column definition
                    END_VAR_DEF = self._NUM_FIXLINES + self.num_cols_dependent - 1
                    NUM_HEAD_LINES = self.num_head_lines
                    try:
                        self.var_defs.append(self._read_vardef_line(line))
                    except Exception as e:
                        const.logger.warning(repr(e))

                elif lc < END_VAR_DEF:
                    self.var_defs.append(self._read_vardef_line(line))

                elif lc == NUM_HEAD_LINES - 1:
                    IN_DATA = True
                    self._data_header = h = [x.strip() for x in line.split()]
                    #append information of first two columns to variable
                    #definition array.
                    self._var_defs.insert(0, EbasColDef(name=h[0],
                                                        is_flag=False,
                                                        is_var=False,
                                                        unit=self.time_unit))
                    self._var_defs.insert(1, EbasColDef(name=h[1],
                                                        is_flag=False,
                                                        is_var=False,
                                                        unit=self.time_unit))
                    if only_head:
                        return
                    const.logger.debug("REACHED DATA BLOCK")
                    _insert_invalid = tuple([np.nan]*self.col_num)

                #elif lc > self._NUM_FIXLINES + 3:
                elif lc >= END_VAR_DEF + 2:
                    try:
                        name, val = line.split(":")
                        key = name.strip().lower().replace(" ", "_")
                        self.meta[key] = val.strip()
                    except Exception as e:
                        const.logger.warning("Failed to read line no. {}.\n{}\n"
                              "Error msg: {}\n".format(lc, line, repr(e)))
                else:
                    const.logger.debug("Ignoring line no. {}: {}".format(lc, line))
                mc += 1
            lc += 1

        data = np.asarray(data)

        data[:, 1:] = data[:, 1:] * np.asarray(self.mul_factors)

        self._data = data
        if replace_invalid_nan:
            dep_dat = data[:, 1:]
            for i, val in enumerate(np.floor(self.vals_invalid)):
                col = dep_dat[:, i]
                cond = np.floor(col) == val
                col[cond] = np.nan
                dep_dat[:, i] = col

            data[:, 1:] = dep_dat
        self._data = data

        if convert_timestamps:
            self.compute_time_stamps()

        self.assign_flagcols()
        self.init_flags(evaluate=evaluate_flags)

        if quality_check:
            self._quality_check()

    def _read_vardef_line(self, line_from_file):
        """Import variable definition line from NASA Ames file"""
        spl = [x.strip() for x in line_from_file.split(",")]
        name = spl[0]
        if not len(spl) > 1:
            unit = ''
        else:
            unit = spl[1]
        data = EbasColDef(name=name,
                          is_flag=True,
                          is_var=False,
                          unit=unit)

        if not "numflag" in name:
            data.is_var = True
            data.is_flag = False
            for item in spl[2:]:
                if "=" in item:
                    # e.g. wavelength=550nm
                    sub = item.split("=")
                    if len(sub) == 2:
                        idf, val = [x.strip() for x in sub]
                        data[idf.lower().replace(' ', '_')] = val
                    else:
                        const.logger.warning("Could not interpret part of column "
                                       "definition in EBAS NASA Ames file: "
                                       "{}".format(item))
                else: #unit
                    const.logger.warning("Failed to interpret {}".format(item))

        return data

    def _data_short_str(self):
        if len(self.data) == 0:
            s = "No data available"
        else:
            s =  str(self.data)
            shape = self.data.shape
            s += "\nColnum: {}".format(shape[1])
            s += "\nTimestamps: {}".format(shape[0])
        return s

    def print_col_info(self):
        """Print information about individual columns"""
        for (idx, coldef) in enumerate(self.var_defs):
            print("Column {}\n{}".format(idx, coldef))

    def __str__(self):
        s = super(EbasNasaAmesFile, self).__str__()
        s += "\n\n{}".format(str_underline("Data", indent=3))
        s += "\n{}".format(self._data_short_str())
        return s

if __name__=="__main__":
    DIR_MC = "/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/"
    FILES_MC = ['US0035R.20150826222034.20160117041718.nephelometer..pm10.5mn.1h.US06L_TSI_3563_BND_pm10.US06L_scat_coef.lev2.nas']

    file_mc = os.path.join(DIR_MC, FILES_MC[0])

    mc = EbasNasaAmesFile(file_mc)
    print(mc)

    #alert = EbasNasaAmesFile(DIR_MC + FILES_MC[1])
    #print(alert)

    #df = alert.to_dataframe()

    #idx = alert._find_col_matches('aerosol_absorption_coefficient',
    #                              statistics='arithmetic mean')

    #alert.plot_var('aerosol_absorption_coefficient', data_level=2)
