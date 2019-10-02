#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 11:07:06 2018

@author: jonasg
"""
import os
try:
    from ConfigParser import ConfigParser
except: 
    from configparser import ConfigParser

from pyaerocom import __dir__, logger
from pyaerocom._lowlevel_helpers import BrowseDict
from pyaerocom.io import EbasSQLRequest

class EbasVarInfo(BrowseDict):
    """EBAS I/O variable information for Aerocom
    
    See `variables.ini <https://github.com/metno/pyaerocom/blob/master/
    pyaerocom/data/variables.ini>`__ file for an overview of currently available 
    default variables.
    
    Attributes
    ----------
    var_name : str
        Aerocom variable name
    
    """
    def __init__(self, var_name="abs550aer", init=True, **kwargs):
        self.var_name = var_name
        
        #: aliases
        self.aliases = []
        
        #: old variable name
        self.old_name = None
        
        #: list of variable / component names (EBAS side)
        self.component = None
        
        #: list of matrix names (EBAS side, optional)
        self.matrix = None
        
        #: list of instrument names (EBAS side, optional)
        self.instrument = None
        
        #: list containing variable statistics info (EBAS side, optional)
        self.statistics = None
        
        #: list of additional variable required for retrieval of this variable
        self.requires = None
        
        #: scale factor for conversion to Aerocom units
        self.scale_factor = 1
        
        #imports default information and, on top, variable information (if 
        # applicable)
        if init:
            self.parse_from_ini(var_name) 
    
    @staticmethod
    def PROVIDES_VARIABLES():
        data = EbasVarInfo.open_config()
        return [k for k in data.keys()]
        
    @staticmethod
    def open_config():
        fpath = os.path.join(__dir__, "data", "ebas_config.ini")
        if not os.path.exists(fpath):
            raise IOError("Ebas config file could not be found: %s"
                          %fpath)
        conf_reader = ConfigParser()
        conf_reader.read(fpath)
        return conf_reader
    
    def _check_aliases(self, varname, conf_reader):
        for section, item in conf_reader.items():
            if 'aliases' in item:
                if varname in [x.strip() for x in item['aliases'].split(',')]:
                    logger.warning('Found alias match ({}) for variable {}, '
                                   'Note that searching for aliases slows down '
                                   'things, thus, please consider using the '
                                   'actual aerocom variable '
                                   'name'.format(varname, section))
                    return section
        raise IOError('No alias match could be found for variable {}'.format(varname))
        
    def parse_from_ini(self, var_name=None, conf_reader=None):
        """Import information about default region
        
        Parameters
        ----------
        var_name : str
            strind ID of region (must be specified in `regions.ini <https://
            github.com/metno/pyaerocom/blob/master/pyaerocom/data/regions.ini>`__ 
            file)
        conf_reader : ConfigParser
            open config parser object
            
        Returns
        -------
        bool
            True, if default could be loaded, False if not
        
        Raises
        ------
        IOError
            if regions.ini file does not exist

        
        """
        if conf_reader is None:
            conf_reader = self.open_config()
        
        if not var_name in conf_reader:
            try:
                var_name = self._check_aliases(var_name, conf_reader)
            except Exception as e:
                raise IOError("No variable information  found for {} "
                              "(including aliases): Error: {}".format(var_name,
                               repr(e)))
        var_info = conf_reader[var_name]
        for key in self.keys():
            if key in var_info:
                val = var_info[key]
                if key in ('var_name', 'old_name') :
                    self[key] = val
                elif key =='scale_factor':
                    self[key] = float(val.split('#')[0].strip())
                else:
                    self[key] = list(dict.fromkeys([x for x in val.split(',')]))
        
        if self.old_name is not None:
            self.aliases.append(self.old_name)
    
    def to_dict(self):
        """Convert into dictionary"""
        d = {}
        for k, v in self.items():
            if k == 'unit':
                k = 'units'
            if v is not None:
                d[k] = v
        return d
    
    def get_all_components(self):
        """Get list of all components"""
        return get_all_components(self.var_name)
    
    def make_sql_request(self, **constraints):
        """Create an SQL request for the specifications in this object
        
        Parameters
        ----------
        **constraints
            request constraints deviating from default. For details on 
            parameters see :class:`EbasSQLRequest`
            
        Returns
        -------
        EbasSQLRequest
            the SQL request object that can be used to retrieve corresponding 
            file names using instance of :func:`EbasFileIndex.get_file_names`.
        """
        variables = self.get_all_components()
# =============================================================================
#         if self.component is not None:
#             variables.extend(self.component)
#         if self.requires is not None:
#             for aux_var in self.requires:
#                 aux_info = EbasVarInfo(aux_var)
#                 if aux_info.component is not None:
#                     variables.extend(aux_info.component)
#                 elif aux_info.requires is not None:
#                     variables.extend(aux_info.requires)
#         
#         # remove duplicates
#         variables = list(set(variables))
# =============================================================================
        if len(variables) == 0:
            raise AttributeError('At least one component (Ebas variable name) '
                             'must be specified for retrieval of variable '
                             '{}'.format(self.var_name))
    
        # default request
        req = EbasSQLRequest(variables=variables, matrices=self.matrix,
                              instrument_types=self.instrument,
                              statistics=self.statistics)
        
            
        req.update(**constraints)
        return req
        
    def __str__(self):
        head = "Pyaerocom {}".format(type(self).__name__)
        s = "\n{}\n{}".format(head, len(head)*"-")
        for k, v in self.items():
                s += "\n%s: %s" %(k,v)
        return s

def get_all_components(var_name, varlist=None):
    """Get all EBAS components required to read a certain variable
    
    Parameters
    ----------
    var_name : str
        AeroCom variable name
    varlist : list, optional
        list of components already inferred (this function runs recursively).
        
    Returns
    -------
    list
        list of components required to read / compute input AeroCom variable
    """
    if varlist is None:
        varlist = []
    aux_info = EbasVarInfo(var_name)
    if aux_info.component is not None:
        varlist.extend(aux_info.component)
    if aux_info.requires is not None:
        for aux_var in aux_info.requires:
            varlist = get_all_components(aux_var, varlist)
    return list(set(varlist))

def check_all_variables():
    """Helper function that checks all EBAS variables against SQL database
    
    For all variables, see file ``ebas_config.ini`` in data directory
    
    Raises
    ------
    AttributeError
        if one of the variable definitions in the ini file is not according to
        requirements
    """
    from pyaerocom.io import EbasFileIndex
    all_vars = EbasVarInfo.PROVIDES_VARIABLES()
    db = EbasFileIndex()
    db_info = {'component'     :   db.ALL_VARIABLES,
               'matrix'        :   db.ALL_MATRICES,
               'instrument'    :   db.ALL_INSTRUMENTS,
               'statistics'    :   db.ALL_STATISTICS_PARAMS}
    
    errors = []
    checked_vars = []
    for varname in all_vars:
        info = EbasVarInfo(varname)
        print('Checking variable {}'.format(varname))
        if varname in checked_vars:
            errors.append('Variable {} is defined more than once'.format(varname))
        checked_vars.append(varname)
        for attr, items_db in db_info.items():
            vals_to_check = info[attr]
            if vals_to_check is not None:
                if not isinstance(vals_to_check, list):
                    raise AttributeError('Please check attribute {} of '
                                         'variable {}'.format(attr, varname))
                for item in vals_to_check:
                    if not item in items_db:
                        s=''
                        for compname, db_vals in db_info.items():
                            if item in db_vals:
                                s += ('\nAdditional info: ID {} was found in '
                                      'databes attr {}'.format(item, compname))
                        errors.append(("No such {} ({}) in database. Please "
                                       "check variable {}.{}".format(attr, 
                                                                     item,
                                                                     varname,
                                                                     s)))
                        
    return errors
            
if __name__=="__main__":
    print(EbasVarInfo('concso2'))
    
    print(get_all_components('ang4470dryaer'))
