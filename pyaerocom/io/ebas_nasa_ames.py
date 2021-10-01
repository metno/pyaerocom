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
from pyaerocom.exceptions import (TimeZoneError, NasaAmesReadError)
from pyaerocom import const

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

    def __repr__(self):
        return str(self)

    def __str__(self):
        colattrs = ''
        for key, val in self.items():
            colattrs += f'{key}: {val}, '
        return colattrs[:-2]

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
            self[k] = v

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
    raw_data : ndarray
        raw flag column (containing X-digit floating point numbers)

    """
    def __init__(self, raw_data, interpret_on_init=True):
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
        self.start_meas = None
        self.stop_meas = None

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
        return basedate + (num_arr * mulfac_to_sec).astype("timedelta64[s]")

    def all_cols_contain(self, colnums, what):
        """
        Check if all input columns contain input attr `what`

        Parameters
        ----------
        colnums : list
            list of column numbers
        what : str
            name of attribute (e.g. `matrix`, `statistics`,
            `tower_inlet_height`)

        Returns
        -------
        bool
            True if all input columns contain `what` attr., else False.

        """
        return all([what in self.var_defs[col] for col in colnums])

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
                                   interpret_on_init=evaluate)
                self.flag_col_info[idx] = flag

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

        dt = stop - start
        # mid timestamps
        self.time_stamps = start + dt*.5
        self.start_meas = start
        self.stop_meas = stop

        return (start, stop)

    def get_time_gaps_meas(self, np_freq='s'):
        """Get array with time gaps between individual measurements

        This is computed based on start and stop timestamps, e.g.
        `=dt[0] = start[1] - stop[0]`

        Parameters
        ----------
        np_freq : str
            string specifying output frequency of gap values

        Returns
        -------
        ndarray
            array with time-differences as floating point number in specified
            input resolution
        """
        if self.start_meas is None:
            self.compute_time_stamps() # assigns start / stop attrs.
        start, stop = self.start_meas, self.stop_meas
        gaps = (start[1:] - stop[:-1]).astype(f'timedelta64[{np_freq}]').astype(float)
        return gaps

    def get_dt_meas(self, np_freq='s'):
        """Get array with time between individual measurements

        This is computed based on start and timestamps, e.g.
        `dt[0] = start[1] - start[0]`

        Parameters
        ----------
        np_freq : str
            string specifying output frequency of gap values

        Returns
        -------
        ndarray
            array with time-differences as floating point number in specified
            input resolution
        """
        if self.start_meas is None:
            self.compute_time_stamps() # assigns start / stop attrs.
        start = self.start_meas
        dts = (start[1:] - start[:-1]).astype(f'timedelta64[{np_freq}]').astype(float)
        return dts

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
        self.file = nasa_ames_file
        for line in open(nasa_ames_file):
            if IN_DATA: #in data block (end of file)
                try:
                    data.append(tuple([float(x.strip()) for x in line.strip().split()]))
                    #data.append([float(x.strip()) for x in line.strip().split()])
                except Exception as e:
                    const.print_log.warning(
                        f"EbasNasaAmesFile: Failed to read data row {dc}. "
                        f"Reason: {e}")
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
