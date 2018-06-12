#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for development of EBAS single column files read from server
"""
import os
import numpy as np
from collections import OrderedDict as od
from pyaerocom.utils import str_underline
from pyaerocom import const 

VERBOSE = const.VERBOSE

#conversion methods for first 13 header lines of
conv_str = lambda l : str(l.strip())
conv_multiint = lambda l : [int(x) for x in l.strip().split()]
conv_multifloat = lambda l : [float(x) for x in l.strip().split()]
conv_int = lambda l : int(l.strip())
conv_float = lambda l : float(l.strip())


class NasaAmesReadError(IOError):
    pass

class NasaAmesVariableError(AttributeError):
    pass

class EbasVarDef(dict):
    """Dictionary for variable definitions"""
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
    _verbose = False
    _head_rows_mandatory = [0,5,7,9,10,11]

    h_fixlines_yield = [["num_head_lines", "num_head_fmt"], #line 1
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
    
    h_fixlines_conv = [conv_multiint, #1 -> yields 2
                   conv_str, #2
                   conv_str, #3
                   conv_str, #4
                   conv_str, #5
                   conv_multiint, #6
                   lambda l : [x.strip() for x in l.strip().split("     ")], #7
                   conv_float, #8
                   conv_str, #9
                   conv_int, #10
                   conv_multifloat, #11
                   conv_multifloat, #12
                   conv_str] #13
    
    def __init__(self, verbose=VERBOSE, **kwargs):
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
        return self._verbose
    
    @verbose.setter
    def verbose(self, val):
        self._verbose = val
        
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

class NasaAmesFile(NasaAmesHeader):
    _data_header = [] #Header line of data block
    _data = [] #data block
    
    @property
    def data(self):
        return self._data
    
    @property
    def data_header(self):
        return self._data_header
    
    @property
    def shape(self):
        return self.data.shape
    
    @property
    def col_num(self):
        return self.num_cols_dependent + 1
    
    @property
    def col_names(self):
        cols = [x["var_name"] for x in self.var_defs]
        return self.data_header[:2] + cols
    
    @property
    def col_names_vars(self):
        return [x.var_name for x in self.var_defs if not x.is_flag]

    @property
    def base_date(self):
       return self._base_date()
       
    @property
    def time_stamps(self):
        raise NotImplementedError
    
    def _base_date(self):
        raise NotImplementedError
       
    def _quality_check(self):
        msgs = ""
        if not len(self.data_header) - 2 == len(self.var_defs):
            msgs += ("Mismatch between variable definitions in header and "
                     "number of data columns in table\n")
        if not "timezone" in self.meta:
            msgs += ("Timezone not defined in metadata")
        if msgs:
            raise AttributeError("Quality check failed. Messages: {}".format(msgs))
        
    def read_header(self, nasa_ames_file, quality_check=True,
                    verbose=VERBOSE):
        self.read_file(nasa_ames_file, True, quality_check, verbose)
        
    def read_file(self, nasa_ames_file, only_head=False, 
                  quality_check=True, verbose=VERBOSE):
        """Read NASA Ames file
        
        Parameters
        ----------
        nasa_ames_file : str
            path of EBAS NASA Ames file
        only_head : bool
            if True, only the header is read
        quality_check : bool
            if True, a quality check is performed after reading
        """
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
                    val = self.h_fixlines_conv[lc](line)
                    attr = self.h_fixlines_yield[lc]
                    if isinstance(attr, list):    
                        for i, attr_id in enumerate(attr):
                            self[attr_id] = val[i]
                    else:
                        self[attr] = val
                except Exception as e:
                    msg = ("Failed to read header row {}.\n{}\n" 
                           "Error msg: {}".format(lc, line, repr(e)))
                    if lc in self._head_rows_mandatory:
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
                            _var.flag_id = var.var_name
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
                    self._data_header = [x.strip() for x in line.split()]
                    if only_head:
                        break
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
        
        self._data = np.asarray(data)
        if quality_check:
            self._quality_check()
            
    def _read_vardef_line(self, line_from_file):
        """Import variable definition line from NASA Ames file"""
        data = EbasVarDef()
        spl = [x.strip() for x in line_from_file.split(",")]
        #data = od()
        data.var_name = name = spl[0]
        data.unit = spl[1]
        isflag = True
        if name != "numflag":    
            isflag = False
            for item in spl[2:]:
                if "=" in item:
                    sub = item.split("=")
                    if not len(sub) == 2:
                        raise IOError("Provide some useful information here")
                    name, val = [x.strip() for x in sub]
                    data[name.lower()] = val
                else: #unit
                    if self.verbose:
                        print("Failed to interpret {}".format(item))
        data.is_flag = isflag
        data.flag_id = None
        return data
    
    def __str__(self):
        s = super(NasaAmesFile, self).__str__()
        s += str_underline("Data")
        
        return s
    
if __name__=="__main__":
    DIR_MC = "/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data"
    FILES_MC = ["DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas",]
    
    file_mc = os.path.join(DIR_MC, FILES_MC[0])
    
    mc = NasaAmesFile()
    
    mc.read_file(file_mc, quality_check=False)
    print(mc)