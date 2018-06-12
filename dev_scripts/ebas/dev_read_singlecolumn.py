#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for development of EBAS single column files read from server
"""
import os
import numpy as np
from collections import OrderedDict as od

DIR_SC = "/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBAS/data"
DIR_MC = "/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data"

FILES_SC =["ZA0001G.20120101.20140211.aerosol_light_backscattering_coefficient.pm10.1y.1h.ZA02L_TSI_3563_CPT.ZA02L_scat_coef.nas"]
FILES_MC = ["DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas",]

NUM_FIXLINES = 13

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

conv_str = lambda l : str(l.strip())
conv_multiint = lambda l : [int(x) for x in l.strip().split()]
conv_multifloat = lambda l : [float(x) for x in l.strip().split()]
conv_int = lambda l : int(l.strip())
conv_float = lambda l : float(l.strip())

h_fixlines_conv = [conv_multiint, #1 -> yields 2
                   conv_str, #2
                   conv_str, #3
                   conv_str, #4
                   conv_str, #5
                   conv_multiint, #6
                   lambda l : [x.strip() for x in l.strip().split("     ")], #7
                   conv_float, #8
                   conv_str, #9
                   conv_int,
                   conv_multifloat,
                   conv_multifloat, 
                   conv_str]

VERBOSE = True
class NasaAmesHeader(object):
    _verbose = False
    _head_fix = od(num_head_lines = np.nan,
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
    _var_defs = []
    _meta = od()
    def __init__(self, verbose=VERBOSE, **kwargs):
    
        self.verbos = verbose
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
        s += "\n{}".format(_str_underline("Column variable definitions"))
        for item in self._var_defs:
            s += "{}\n".format(item)
        s += "\n{}".format(_str_underline("EBAS meta data"))
        
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
    def start_date(self):
       raise NotImplementedError
       
    @property
    def time_stamps(self):
        raise NotImplementedError
    
    def read_header(self, nasa_ames_file):
        self.read_file(nasa_ames_file, True)
        
    def _quality_check(self):
        msgs = ""
        if not len(self.data_header) - 2 == len(self.var_defs):
            msgs += ("Mismatch between variable definitions in header and "
                     "number of data columns in table\n")
        if not "timezone" in self.meta:
            msgs += ("Timezone not defined in metadata")
        if msgs:
            raise AttributeError("Quality check failed. Messages: {}".format(msgs))
            
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
        
        lc = 0 #line counter
        dc = 0 #data block line counter
        mc = 0 #meta block counter
        END_VAR_DEF = np.nan #will be set (info stored in header)
        IN_DATA = False 
        data = []
        _insert_invalid = None
        for line in open(nasa_ames_file):
            #print(lc, NUM_FIXLINES, line)
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
            elif lc < NUM_FIXLINES:
                try:
                    val = h_fixlines_conv[lc](line)
                    attr = h_fixlines_yield[lc]
                    if isinstance(attr, list):    
                        for i, attr_id in enumerate(attr):
                            self[attr_id] = val[i]
                    else:
                        self[attr] = val
                except Exception as e:
                    raise NasaAmesReadError("Fatal: Failed to read header "
                                            "row {}. Error msg: {}".format(lc, repr(e)))
            else:
                if mc == 0:
                    END_VAR_DEF = NUM_FIXLINES + self.num_cols_dependent - 1
                    NUM_HEAD_LINES = self.num_head_lines
                    try:
                        self.var_defs.append(self._read_vardef_line(line))
                    except Exception as e:
                        if verbose:
                            print(repr(e))
                           
                elif lc < END_VAR_DEF:
                    try:
                        self.var_defs.append(self._read_vardef_line(line))
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
                    
                elif lc > NUM_FIXLINES + 3:
                    try:
                        name, val = line.split(":")
                        key = name.strip().lower().replace(" ", "_")
                        self.meta[key] = val.strip()
                    except Exception as e:
                        print("Failed to read line {}.\n"
                              "Error msg: {}\n".format(line, repr(e)))
                else:
                    if verbose:
                        print("Ignoring line: {}".format(line)) 
                mc += 1
            lc += 1
        
        self._data = np.asarray(data)
        if quality_check:
            self._quality_check()
            
    def _read_vardef_line(self, line_from_file):
        """Import variable definition line from NASA Ames file"""
        spl = [x.strip() for x in line_from_file.split(",")]
        data = od()
        data["var_name"] = name = spl[0]
        data["unit"] = spl[1]
        if name != "numflag":    
            for item in spl[2:]:
                if "=" in item:
                    sub = item.split("=")
                    if not len(sub) == 2:
                        raise IOError("Provide some useful information here")
                    name, val = [x.strip() for x in sub]
                    data[name.lower()] = val
                elif " nm" in item: #wavelength without key
                    data["wavelength"] = item
                else: #unit
                    if self.verbose:
                        print("Failed to interpret {}".format(item))
        return data
    
    def __str__(self):
        s = super(NasaAmesFile, self).__str__()
        s += _str_underline("Data")
        
        return s
    
def _str_underline(s):
    return "{}\n{}\n".format(s, len(s)*"-")

if __name__=="__main__":
    from time import time
    RUN_OLD = False
    RUN_PERFORMANCE_TEST = False
    files_sc = [os.path.join(DIR_SC, x) for x in FILES_SC]    
    files_mc = [os.path.join(DIR_MC, x) for x in FILES_MC]

    a = NasaAmesFile()
    
    times = []
    repeat = 100
    if not RUN_OLD:
        if not RUN_PERFORMANCE_TEST:
        
            a.read_file(files_sc[0], only_head=True)
            #print(a)
        
        
    
        
        else:
            for k in range(repeat):
                t0 = time()
                a.read_file(files_sc[0], verbose=False)
                times.append(time()-t0)
            dt_avg = np.average(times)
            print("Elapsed time (from class): {:.5f} s".format(dt_avg))
            
            
            
            
    else:
        for file in files_sc:
            t0 = time()
            lc = 0 #line counter
            dc = 0 #data block line counter
            END_VAR_DEF = np.nan
            IN_DATA = False
            data = []
            
            for line in open(file):
                if IN_DATA:
                    if dc == 0:
                        print(line)
                    data.append(tuple([float(x.strip()) for x in line.strip().split()]))
                    dc += 1
                elif lc < NUM_FIXLINES - 1:
                    val = h_fixlines_conv[lc](line)
                    attr = h_fixlines_yield[lc]
                    if isinstance(attr, list):    
                        for i, attr_id in enumerate(attr):
                            a[attr_id] = val[i]
                    else:
                        a[attr] = val
                else:
                    if lc == NUM_FIXLINES - 1:
                        END_VAR_DEF = NUM_FIXLINES + a.num_cols_dependent - 1
                        NUM_HEAD_LINES = a.num_head_lines
                        #a._var_defs.append(_read_vardef_line(line))
                    elif lc < END_VAR_DEF:
                        a.var_defs.append(_read_vardef_line(line))
        
                    elif lc == NUM_HEAD_LINES - 1:
                        IN_DATA = True
                        print("REACHED DATA BLOCK")
                        
                    elif lc > NUM_FIXLINES + 3:
                        try:
                            name, val = line.split(":")
                            key = name.strip().lower().replace(" ", "_")
                            a.meta[key] = val.strip()
                        except Exception as e:
                            print("Failed to read line {}.\n"
                                  "Error msg: {}\n".format(line, repr(e)))
                    else:
                        print("Ignoring line: {}".format(line))
                        
                lc += 1
            data = tuple(data)
            a._data = np.asarray(data)
            print("Elapsed time (script): {:.1f} s".format(time()-t0))

                
    
        
    
    
    
    
