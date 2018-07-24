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
from pyaerocom.utils import str_underline
from pyaerocom.exceptions import TimeZoneError
from pyaerocom import const 

class NasaAmesReadError(IOError):
    pass

class NasaAmesVariableError(AttributeError):
    pass

class EbasColDef(dict):
    """Dict-like object for EBAS NASA Ames column definitions
    
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
    flag_id : str
        ``name`` of flag column that corresponds to this data colum (only
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
    flag_id : :obj:`str`, optional
        ``name`` of flag column that corresponds to this data colum (only
        relevant if :attr:`is_var` is True)
    """
    def __init__(self, name, is_var, is_flag, unit="", flag_id=""):
        self.name = name
        self.unit = unit
        self.is_var = is_var
        self.is_flag = is_flag
        self.flag_id = flag_id
        
    def __getattr__(self, key):
        return self[key]
    
    def __setattr__(self, key, val):
        self[key] = val
    
    def __str__(self):
        s=""
        for k, v in self.items():
            s += "{}: {}\n".format(k, v)
        return s
    
class NasaAmesHeader(object):
    _NUM_FIXLINES = 13
    _VERBOSE = False
    _HEAD_ROWS_MANDATORY = [0,5,8,9,10,11]
    
    #conversion methods for first 13 header lines of
    CONV_STR = lambda l : str(l.strip())
    CONV_MULTIINT = lambda l : [int(x) for x in l.strip().split()]
    CONV_MULTIFLOAT = lambda l : [float(x) for x in l.strip().split()]
    CONV_INT = lambda l : int(l.strip())
    CONV_FLOAT = lambda l : float(l.strip())
    _STARTDATE_FMT = "%Y%m%d%H%M%S"

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
    
    _H_FIXLINES_CONV = [CONV_MULTIINT, #1 -> yields 2
                        CONV_STR, #2
                        CONV_STR, #3
                        CONV_STR, #4
                        CONV_STR, #5
                        CONV_MULTIINT, #6
                        lambda l : [x.strip() for x in l.strip().split("     ")], #7
                        CONV_FLOAT, #8
                        CONV_STR, #9
                        CONV_INT, #10
                        CONV_MULTIFLOAT, #11
                        CONV_MULTIFLOAT, #12
                        CONV_STR] #13
    
    def __init__(self, verbose=const.VERBOSE, **kwargs):
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
        self.verbose = verbose
        self.update(**kwargs)
    
    @property
    def verbose(self):
        return self._VERBOSE
    
    @verbose.setter
    def verbose(self, val):
        self._VERBOSE = val
        
    @property
    def head_fix(self):
        return self._head_fix
    
    @property
    def var_defs(self):
        return self._var_defs
        
    @property
    def meta(self):
        return self._meta
        
    def update(self, **kwargs):
        for k, v in kwargs.items():
            try:
                self[k] = v
            except:
                if self.verbose:
                    print("Invalid attribute: {}".format(k))
                    
            
    def __getattr__(self, key):
        if key in self._head_fix:
            return self._head_fix[key]
        elif key in self._meta:
            return self._meta[key]
        else:
            raise AttributeError("Invalid attribute: {}".format(key))
            
    def __setitem__(self, key, val):
        if key in self._head_fix:
            self._head_fix[key] = val
        else:
            self._meta[key] = val
    
    def __str__(self):
        head = "Pyaerocom {}".format(type(self).__name__)
        s = "{}\n{}\n".format(head, len(head)*"-")
        for k, v in self._head_fix.items():
            s += "{}: {}\n".format(k, v)
        s += "\n{}".format(str_underline("Column variable definitions"))
        for item in self._var_defs:
            s += "{}\n".format(item)
        s += "\n{}".format(str_underline("EBAS meta data"))
        
        for k, v in self.meta.items():
            s += "\t{}: {}\n".format(k, v)
        
        return s

class EbasFlagCol(object):
    def __init__(self, raw_data, info, decode_on_init=True):
        if not raw_data.ndim == 1:
            raise AttributeError("Need one dimensional numpy array for flag "
                                 "column")
        self.info = info
        self.raw_data = raw_data
        
        self.flags = None
        
        if decode_on_init:
            self.decode()
            
    def decode(self):
        flags = np.zeros((len(self.raw_data), 3)).astype(int)
        mask = self.raw_data.astype(bool)
        not_ok = self.raw_data[mask]
        
        decoded = []
        for flag in not_ok:
            item = "{:.9f}".format(flag).split(".")[1]
            decoded.append([int(item[:3]), int(item[3:6]), int(item[6:9])])
        flags[mask] = np.asarray(decoded)
        self.flags = flags
        
        
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
    decode_flags : bool
        if True, all flags in all flag columns are decoded from floating 
        point representation to 3 integers, e.g. 
        0.111222333 -> 111 222 333
    quality_check : bool
        perform quality check after import (for details see 
        :func:`_quality_check`)
    verbose : bool
        print output
    **kwargs 
        optional input args that are passed to init of :class:`NasaAmesHeader`
        base class
    
    """
    TIMEUNIT2SECFAC = dict(days = 3600*24)
    def __init__(self, file=None, only_head=False, replace_invalid_nan=True,
                 convert_timestamps=True, decode_flags=True, 
                 quality_check=True, verbose=const.VERBOSE, **kwargs):
        super(EbasNasaAmesFile, self).__init__(verbose, **kwargs)
        self._data_header = [] #Header line of data block
        self._data = [] #data block
        
        self.time_stamps = None
        
        self.flags = od()
        
        if file is not None and os.path.exists(file):
            self.read_file(file, only_head, replace_invalid_nan, 
                           convert_timestamps, decode_flags,
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
        """Base date of data"""
        if not "timezone" in self.meta:
            raise AttributeError("Fatal: could not infer base date. Timezone "
                                 "is not available in file header")
        if not self.timezone.lower() == "utc":
            raise TimeZoneError("Timezones other than UTC are not yet supported")
        return np.datetime64(datetime.strptime(self.startdate, "%Y%m%d%H%M%S"))
    
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
        elif totnum == 1:
            num_arr = np.asarray([num_arr])
        return basedate + (num_arr * mulfac_to_sec).astype("timedelta64[s]")
    
# =============================================================================
#     def decode_flags_col(self, colnum=None):
#         """Decode flags column
#         
#         Parameters
#         ----------
#         colnum : int
#             flag column number (only relevant if file contains multiple flag
#             columns)
#         """
#         if colnum is None:
#             l = self.col_names
#             flag_cols = [i for (i, item) in enumerate(l) if "numflag" in item]
#             if len(flag_cols) > 1:
#                 raise ValueError("Found multiple flag columns: {}. Please "
#                                  "specify which column to decode.".format(flag_cols))
#             colnum = flag_cols[0]
#         elif not self.var_defs[colnum].is_flag:
#             raise IndexError("Provided column number is not a flag column")
# =============================================================================
        
            
    def to_dataframe(self):
        """Convert table to dataframe"""
        return pd.DataFrame(data=self.data[:,self.col_nums_vars],
                            index=self.time_stamps,
                            columns=self.col_names_vars)
    
    def init_flags(self, decode=True):
        for (idx, item) in enumerate(self.var_defs):
            if item.is_flag:
                data = self.data[:, idx]
                flag = EbasFlagCol(raw_data=data,
                                   info=item, 
                                   decode_on_init=decode)
                self.flags[item.name] = flag
                
                
    def compute_time_stamps(self):
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
        self.read_file(nasa_ames_file, True, quality_check)
        
    def read_file(self, nasa_ames_file, only_head=False, 
                  replace_invalid_nan=True,
                  convert_timestamps=True, decode_flags=True, 
                  quality_check=True):
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
        decode_flags : bool
            if True, all flags in all flag columns are decoded from floating 
            point representation to 3 integers, e.g. 
            0.111222333 -> 111 222 333
        quality_check : bool
            perform quality check after import (for details see 
            :func:`_quality_check`)
        """
        verbose = self.verbose
        if verbose:
            print("Reading NASA Ames file:\n{}".format(nasa_ames_file))
        lc = 0 #line counter
        dc = 0 #data block line counter
        mc = 0 #meta block counter
        END_VAR_DEF = np.nan #will be set (info stored in header)
        IN_DATA = False 
        data = []
        _insert_invalid = None
        for line in open(nasa_ames_file):
            #print(lc, _NUM_FIXLINES, line)
            if IN_DATA:
                if dc == 0 and verbose:
                    print(line)
                try:
                    data.append(tuple([float(x.strip()) for x in line.strip().split()]))
                    #data.append([float(x.strip()) for x in line.strip().split()])
                except Exception as e:
                    data.append(_insert_invalid)
                    if verbose:
                        print("Failed to read data row {}. "
                              "Error msg: {}".format(dc, repr(e)))
                dc += 1
            elif lc < self._NUM_FIXLINES:
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
                        if self.verbose:
                            print(msg)
            else:
                _flagmap_idx = 0
                if mc == 0:
                    END_VAR_DEF = self._NUM_FIXLINES + self.num_cols_dependent - 1
                    NUM_HEAD_LINES = self.num_head_lines
                    try:
                        self.var_defs.append(self._read_vardef_line(line))
                    except Exception as e:
                        if verbose:
                            print(repr(e))
                           
                elif lc < END_VAR_DEF:
                    var = self._read_vardef_line(line)
                    #if variable corresponds to flag column, assign this 
                    #flag column to all previously read variables
                    if var.is_flag:
                        for _var in self.var_defs[_flagmap_idx:]:
                            _var.flag_id = var.name
                    self.var_defs.append(var)
                    _flagmap_idx = len(self.var_defs)
                    try:
                        pass
                        #self.var_defs.append(var)
                    except Exception as e:
                        if verbose:
                            print(repr(e))
    
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
                    if verbose:
                        print("REACHED DATA BLOCK")
                    _insert_invalid = tuple([np.nan]*self.col_num)
                    
                    
                #elif lc > self._NUM_FIXLINES + 3:
                elif lc >= END_VAR_DEF + 2:
                    try:
                        name, val = line.split(":")
                        key = name.strip().lower().replace(" ", "_")
                        self.meta[key] = val.strip()
                    except Exception as e:
                        print("Failed to read line no. {}.\n{}\n"
                              "Error msg: {}\n".format(lc, line, repr(e)))
                else:
                    if verbose:
                        print("Ignoring line no. {}: {}".format(lc, line)) 
                mc += 1
            lc += 1
        
        data = np.asarray(data) 
        
        data[:, 1:] = data[:, 1:] * np.asarray(self.mul_factors)
        
        self._data = data
        if replace_invalid_nan:
            dep_dat = data[:, 1:]
            for i, val in enumerate(np.floor(self.vals_invalid)):
                try:
                    col = dep_dat[:, i]
                    cond = np.floor(col) == val
                    col[cond] = np.nan
                    dep_dat[:, i] = col
                except:
                    if self.verbose:
                        print("Failed to replace invalid values with NaNs "
                              "in column {}".format(self.col_names[i+1]))
            data[:, 1:] =dep_dat
        self._data = data
        
        if convert_timestamps:
            try:
                self.compute_time_stamps()
            except Exception as e:
                if self.verbose:
                    print("Failed to compute time stamps.\n"
                          "Error message: {}".format(repr(e)))
        self.init_flags(decode_flags)
        if quality_check:
            self._quality_check()
            
    def _read_vardef_line(self, line_from_file):
        """Import variable definition line from NASA Ames file"""
        spl = [x.strip() for x in line_from_file.split(",")]
        name = spl[0]
        data = EbasColDef(name=name,
                          is_flag=True,
                          is_var=False,
                          unit=spl[1])
        
        if name != "numflag":    
            data.is_var = True
            data.is_flag = False
            for item in spl[2:]:
                if "=" in item:
                    sub = item.split("=")
                    if not len(sub) == 2:
                        raise IOError("Provide some useful information here")
                    idf, val = [x.strip() for x in sub]
                    data[idf.lower()] = val
                else: #unit
                    if self.verbose:
                        print("Failed to interpret {}".format(item))
        
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
        s += str_underline("Data")
        s += self._data_short_str()
        return s
    
if __name__=="__main__":
    DIR_MC = "/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data"
    FILES_MC = ["DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas",]
    
    file_mc = os.path.join(DIR_MC, FILES_MC[0])
    
    f = open(file_mc)
    lines = f.readlines()
    
    mc = EbasNasaAmesFile(file_mc)
    print(mc)
    
#    print(mc.to_dataframe())