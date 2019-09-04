#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains functionality related to regions in pyaerocom
"""
import os
from ast import literal_eval
import re, fnmatch
try:
    from ConfigParser import ConfigParser
except: 
    from configparser import ConfigParser
from pyaerocom import __dir__, logger
from pyaerocom.obs_io import OBS_WAVELENGTH_TOL_NM
from pyaerocom.exceptions import VariableDefinitionError
from pyaerocom._lowlevel_helpers import list_to_shortstr, dict_to_str

is_3d =  lambda var_name: True if '3d' in var_name.lower() else False
str2bool = lambda val: val.lower() in ('true', '1', 't', 'yes')

class VarNameInfo(object):
    """This class can be used to retrieve information from variable names"""
    _VALID_WVL_RANGE = [100, 2000]
    _VALID_WVL_IDS = ['od', 'abs', 'ec', 'scatc', 'absc', 'bscatc', 'ssa']
    PATTERNS = {'od' : r'od\d+aer'}
    def __init__(self, var_name):
        self.var_name = var_name.lower()
        self._nums = []
        try:
            self._nums = self._numbers_in_string(var_name)
        except:
            pass
     
    @staticmethod
    def _numbers_in_string(s):
        return [int(x) for x in re.findall(r'\d+', s)]
    
    @property
    def contains_numbers(self):
        """Boolean specifying whether this variable name contains numbers"""
        if len(self._nums) > 0:
            return True
        return False
    
    @property
    def is_wavelength_dependent(self):
        """Boolean specifying whether this variable name is wavelength dependent"""
        for item in self._VALID_WVL_IDS:
            if self.var_name.startswith(item):
                return True
        return False
    
    @property
    def contains_wavelength_nm(self):
        """Boolean specifying whether this variable contains a certain wavelength"""
        if not self.contains_numbers:
            return False
        low, high = self._VALID_WVL_RANGE
        if self._nums and low <= self._nums[0] <= high:
            return True
        return False
    
    @property
    def wavelength_nm(self):
        """Wavelength in nm (if appliable)"""
        if not self.is_wavelength_dependent:
            raise VariableDefinitionError('Variable {} is not wavelength '
                                          'dependent (does not start with '
                                          'either of {})'.format(self.var_name,
                                                     self._VALID_WVL_IDS))
            
        elif not self.contains_wavelength_nm:
            raise VariableDefinitionError('Wavelength could not be extracted '
                                          'from variable name')
        return self._nums[0]

        
    @property
    def is_optical_density(self):
        """Boolean specifying whether variable is an optical depth"""
        if re.match(self.PATTERNS['od'], self.var_name) and self.contains_wavelength_nm:
            return True
        return False
    
    def in_wavelength_range(self, low, high):
        """Boolean specifying whether variable is within wavelength range
        
        Parameters
        ----------
        low : float
            lower end of wavelength range to be tested
        high : float
            upper end of wavelength range to be tested
        
        Returns
        -------
        bool
            True, if this variable is wavelength dependent and if the 
            wavelength that is inferred from the filename is within the 
            specified input range
        """
        return low <= self.wavelength <= high
    
    def translate_to_wavelength(self, to_wavelength):
        """Create new variable name at a different wavelength
        
        Parameters
        ----------
        to_wavelength : float
            new wavelength in nm
        
        Returns
        -------
        VarNameInfo
            new variable name
        """
        if not self.contains_wavelength_nm:
            raise ValueError('Variable {} is not wavelength dependent'.format(self.var_name))
        name = self.var_name.replace(str(self.wavelength_nm),
                                     str(to_wavelength))
        return VarNameInfo(name)
    
    def __str__(self):
        s = ('\nVariable {}\n'
             'is_wavelength_dependent: {}\n'
             'is_optical_density: {}'.format(self.var_name,
                                                self.is_wavelength_dependent,
                                                self.is_optical_density))
        if self.is_wavelength_dependent:
            s += '\nwavelength_nm: {}'.format(self.wavelength_nm)
        return s
 
def parse_variables_ini(fpath=None):
    """Returns instance of ConfigParser to access information"""
    if fpath is None:
        fpath = os.path.join(__dir__, "data", "variables.ini")
        
    if not os.path.exists(fpath):
        raise FileNotFoundError("FATAL: variables.ini file could not be found "
                                "at {}".format(fpath))
    parser = ConfigParser()
    parser.read(fpath)
    return parser

def parse_aliases_ini():
    """Returns instance of ConfigParser to access information"""
    fpath = os.path.join(__dir__, "data", "aliases.ini")
    if not os.path.exists(fpath):
        raise FileNotFoundError("FATAL: aliases.ini file could not be found "
                                "at {}".format(fpath))
    parser = ConfigParser()
    parser.read(fpath)
    return parser

def _read_alias_ini(parser=None):
    """Read all alias definitions from aliases.ini file and return as dict
    
    Returns
    -------
    dict
        keys are AEROCOM standard names of variable, values are corresponding
        aliases
    """
    if parser is None:
        parser = parse_aliases_ini()
    aliases = {}
    items = parser['aliases']
    for var_name in items:
        _aliases = [x.strip() for x in items[var_name].strip().split(',')]
        for alias in _aliases:
            aliases[alias] = var_name
    for var_fam, alias_fam in parser['alias_families'].items():
        if ',' in alias_fam:
            raise Exception('Found invalid definition of alias family {}: {}. '
                            'Only one family can be mapped to a variable name'
                            .format(var_fam, alias_fam))
    return aliases

def get_aliases(var_name, parser=None):
    """Get aliases for a certain variable"""
    if parser is None:
        file = os.path.join(__dir__, "data", "aliases.ini")
        parser = ConfigParser()
        parser.read(file)
        
    info = parser['aliases']
    aliases = []
    if var_name in info:
        aliases.extend([a.strip() for a in info[var_name].split(',')])
    for var_fam, alias_fam in parser['alias_families'].items():
        if var_name.startswith(var_fam):
            alias = var_name.replace(var_fam, alias_fam)
            aliases.append(alias)
    return aliases

def _check_alias_family(var_name, parser):
    for var_fam, alias_fam in parser['alias_families'].items():
        if var_name.startswith(alias_fam):
            var_name_aerocom = var_name.replace(alias_fam, var_fam)
            return var_name_aerocom
    raise VariableDefinitionError('Input variable could not be identified as '
                                  'belonging to either of the available alias '
                                  'variable families')

class Variable(object):
    """Interface that specifies default settings for a variable
    
    See `variables.ini <https://github.com/metno/pyaerocom/blob/master/
    pyaerocom/data/variables.ini>`__ file for an overview of currently available 
    default variables.
    
    Parameters
    ----------
    var_name : str
        string ID of variable (see file variables.ini for valid IDs)
    init : bool
        if True, input variable name is attempted to be read from config file
    cfg : ConfigParser
        open config parser that holds the information in config file available
        (i.e. :func:`ConfigParser.read` has been called with config file as 
        input)
    **kwargs
        any valid class attribute (e.g. map_vmin, map_vmax, ...)
        
    Attributes
    ----------
    var_name : str
        AEROCOM variable name (see e.g. `AEROCOM protocol 
        <http://aerocom.met.no/protocol_table.html>`__ for a list of 
        available variables)
    var_name_alt : str
        Alternative variable name that is searched for in variables.ini file
        to find variable information. Is e.g. set to scatc550aer if input 
        is scatc550dryaer. This means, that if scatc550dryaer is not explictely
        defined in
    is_3d : bool
        flag that indicates if variable is 3D
    is_dry : bool
        flag that is set based on filename that indicates if variable data
        corresponds to dry conditions.
    units : str
        unit of variable (None if no unit)
    aliases : list
        list of alternative names for this variable
    minimum : float
        lower limit of allowed value range
    upper_limit : float
        upper limit of allowed value range
    obs_wavelength_tol_nm : float
        wavelength tolerance (+/-) for reading of obsdata. Default is 10, i.e.
        if this variable is defined at 550 nm and obsdata contains measured 
        values of this quantity within interval of 540 - 560, then these data
        is used
    scat_xlim : float
        x-range for scatter plot
    scat_ylim : float
        y-range for scatter plot
    scat_loglog : bool
        scatter plot on loglog scale
    scat_scale_factor : float
        scale factor for scatter plot
    map_vmin : float
        data value corresponding to lower end of colormap in map plots of this
        quantity
    map_vmax : float
        data value corresponding to upper end of colormap in map plots of this
        quantity
    map_c_under : str
        color used for values below :attr:`map_vmin` in map plots of this
        quantity
    map_c_over : str
        color used for values exceeding :attr:`map_vmax` in map plots of this
        quantity
    map_cbar_levels : :obj:`list`, optional
        levels of colorbar
    map_cbar_ticks : :obj:`list`, optional
        colorbar ticks
    """
    literal_eval_list = lambda val: list(literal_eval(val))
    str2list = lambda val: [x.strip() for x in val.split(',')]
    _TYPE_CONV={'wavelength_nm': float,
                'minimum': float,
                'maximum': float,
                'dimensions' : str2list,
                'obs_wavelength_tol_nm': float,
                'scat_xlim': literal_eval_list,
                'scat_ylim': literal_eval_list,
                'scat_loglog': str2bool,
                'scat_scale_factor': float,
                'dry_rh_max':float,
                'map_vmin': float,
                'map_vmax': float,
                'map_cbar_levels': literal_eval_list,
                'map_cbar_ticks': literal_eval_list}
    
    ALT_NAMES = {'units' : 'unit'}  
    
    RH_MAX_DRY = 0.4
    
    plot_info_keys = ['scat_xlim',
                      'scat_ylim',
                      'scat_loglog',
                      'scat_scale_factor',
                      'map_vmin',
                      'map_vmax',
                      'map_c_under',
                      'map_c_over',
                      'map_cbar_levels',
                      'map_cbar_ticks']
    
    def __init__(self, var_name="od550aer", init=True, cfg=None, **kwargs):
        #save orig. input for whatever reasons
        self._var_name_input = var_name 
        self.is_3d = False
        self.is_dry = False
        
        var_name = var_name.lower()
        
        if '3d' in var_name:
            logger.info('Variable name {} contains 3d. Activating flag is_3d '
                        'and removing from var_name string'.format(var_name))
            var_name = var_name.replace('3d','')
            self.is_3d = True
        if 'dry' in var_name:
            self.is_dry = True
            var_name_alt = var_name.replace('dry', '')
        else:
            var_name_alt = var_name
            
        self.var_name = var_name
        self.var_name_alt = var_name_alt #alternative var_name
        self.standard_name = None
        self.units = '1'
        #self.aliases = []
        self.wavelength_nm = None
        self.dry_rh_max = None
        self.dimensions = None
        self.minimum = -9e30
        self.maximum = 9e30

        self.description = None
        self.comments_and_purpose = None

        #wavelength tolerance in nm
        self.obs_wavelength_tol_nm = None
        
        self.scat_xlim = None
        self.scat_ylim = None
        self.scat_loglog = None
        self.scat_scale_factor = 1.0
            
        # settings for map plotting
        self.map_vmin = None
        self.map_vmax = None
        self.map_c_under = None
        self.map_c_over = None
        self.map_cbar_levels = None
        self.map_cbar_ticks = None
        # imports default information and, on top, variable information (if 
        # applicable)
        if init:
            self.parse_from_ini(var_name, 
                                var_name_alt=self.var_name_alt,
                                cfg=cfg) 
        
        self.update(**kwargs)
        if self.obs_wavelength_tol_nm is None:
            self.obs_wavelength_tol_nm = OBS_WAVELENGTH_TOL_NM
    
    @property
    def unit(self):
        """Unit of variable (old name, deprecated)"""
        from warnings import warn
        warn(DeprecationWarning('Attr. name unit in Variable '
                                'class is deprecated. Please '
                                'use units instead'))
        return self.units
        
    @property
    def plot_info(self):
        """Dictionary containing plot information"""
        d = {}
        for k in self.plot_info_keys:
            d[k] = self[k]
        return d
    
    def update(self, **kwargs):
        for key, val in kwargs.items():
            self[key] = val
        
    @property
    def has_unit(self):
        """Boolean specifying whether variable has unit"""
        return True if not self.unit in (1, None) else False
    
    @property
    def lower_limit(self):
        """Old attribute name for :attr:`minimum` (following HTAP2 defs)"""
        logger.warning(DeprecationWarning('Old name for attribute minimum'))
        return self.minimum
     
    @property
    def upper_limit(self):
        """Old attribute name for :attr:`minimum` (following HTAP2 defs)"""
        logger.warning(DeprecationWarning('Old name for attribute minimum'))
        return self.maximum 
    
    @property
    def unit_str(self):
        """string representation of unit"""
        if self.unit is None:
            return ''
        else:
            return '[{}]'.format(self.unit)
    
    @staticmethod
    def read_config():
        return parse_variables_ini()
    
    @property
    def var_name_info(self):
        return VarNameInfo(self.var_name)
        
    @property
    def aliases(self):
        """Alias variable names that are frequently found / used
        
        Returns
        -------
        list
            list containing valid aliases
        """
        return get_aliases(self.var_name)
    
    @property
    def long_name(self):
        """Wrapper for :attr:`description`"""
        return self.description
    
    def keys(self):
        return list(self.__dict__.keys())
    
    def parse_from_ini(self, var_name=None, var_name_alt=None, cfg=None):
        """Import information about default region
        
        Parameters
        ----------
        var_name : str
            variable name
        var_name_alt : str
            alternative variable name that is used if variable name is not
            available
        cfg : ConfigParser
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
        if cfg is None:
            cfg = self.read_config()
        var_info = {} 
        if var_name is not None and var_name != 'DEFAULT':
            if var_name in cfg:
                logger.info("Found default configuration for variable "
                            "{}".format(var_name))
                var_info = cfg[var_name]
                #self.var_name = var_name
            elif isinstance(var_name_alt, str) and var_name_alt in cfg:
                var_info = cfg[var_name_alt]
            else:
                ap = parse_aliases_ini()
                aliases = _read_alias_ini(ap)
                if var_name in aliases:
                    var_name = aliases[var_name]
                    var_info = cfg[var_name]
                else :
                    try:
                        var_name=_check_alias_family(var_name, ap)
                        var_info = cfg[var_name]
                    except VariableDefinitionError:
                    
                        logger.warning("No default configuration available for "
                                       "variable {}. Using DEFAULT settings"
                                       .format(var_name))
            
        default = cfg['DEFAULT']
        
        for key in self.keys():
            if key in self.ALT_NAMES:
                if self.ALT_NAMES[key] in var_info:
                    self._add(key, var_info[self.ALT_NAMES[key]])
            elif key in var_info:
                self._add(key, var_info[key])
            elif key in default:
                self._add(key, default[key])
             
        self.var_name = var_name
    
    def _add(self, key, val):
        if key in self._TYPE_CONV:
            try:
                val = self._TYPE_CONV[key](val)
            except:
                pass
        elif key == 'units':
            if val == 'None':
                val = '1'
        if val == 'None':
            val = None
        self[key] = val
        
    def __setitem__(self, key, val):
        self.__dict__[key] = val
    
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __repr__(self):
       return ("{}\nstandard_name: {}; Unit: {}"
               .format(self.var_name, self.standard_name, 
                       self.unit))
   
    def __str__(self):
        head = "Pyaerocom {}".format(type(self).__name__)
        s = "\n{}\n{}".format(head, len(head)*"-")
        
        plot_s = '\nPlotting settings\n......................'
        
        for k, v in self.__dict__.items():
            if k in self.plot_info_keys:
                if v is None:
                    continue
                if isinstance(v, dict):
                    plot_s += "\n{} (dict)".format(k)
                    plot_s = dict_to_str(v, plot_s, indent=3, 
                                         ignore_null=True)
                elif isinstance(v, list):
                    plot_s += "\n{} (list, {} items)".format(k, len(v))
                    plot_s += list_to_shortstr(v)
                else:
                    plot_s += "\n%s: %s" %(k,v)
            else:
                if isinstance(v, dict):
                    s += "\n{} (dict)".format(k)
                    s = dict_to_str(v, s, indent=3, ignore_null=True)
                elif isinstance(v, list):
                    s += "\n{} (list, {} items)".format(k, len(v))
                    s += list_to_shortstr(v)
                else:
                    s += "\n%s: %s" %(k,v)
        
        s += plot_s
        return s

class VarCollection(object):
    """Variable access class based on variables config file"""
    
    def __init__(self, var_ini):
        self._all_vars = None
        self._var_ini = None
        
        self.var_ini = var_ini
        
        self._cfg_parser = parse_variables_ini(var_ini)
        self._alias_parser = parse_aliases_ini()
        self._idx = -1
        
        logger.info("Importing variable aliases info")
        
    @property
    def all_vars(self):
        """List of all variables
        
        Note: does not include variable names that may be inferred via 
        alias families as defined in section [alias_families] in
        aliases.ini.
        """
        if self._all_vars is None:
            all_vars = [k.lower() for k in self._cfg_parser.keys()]
            all_vars.extend(list(_read_alias_ini()))
            self._all_vars=all_vars
        return self._all_vars
    
    @property
    def var_ini(self):
        """Config file specifying variable information"""
        return self._var_ini
    
    @var_ini.setter
    def var_ini(self, var_ini):
        
        if not os.path.exists(var_ini):
            raise IOError("File {} does not exist".format(var_ini))
        self._var_ini = var_ini
    
    def find(self, search_pattern):
        """Find all variables that match input search pattern
        
        Note
        ----
        Searches for matches in variable names (:attr:`Variable.var_name`) and 
        standard name (:attr:`Variable.standard_name`).
        
        Parameters
        ----------
        search_pattern : str
            variable search pattern
        
        Returns
        -------
        list
            AeroCom variable names that match the search pattern
        """
        matches = []
        for var in self:
            if fnmatch.fnmatch(var.var_name, search_pattern):
                matches.append(var.var_name)
            elif (isinstance(var.standard_name, str) and 
                  fnmatch.fnmatch(var.standard_name, search_pattern)):
                matches.append(var.var_name)
        return matches
        
    def get_coord_var_and_standard_names(self):
        """Get dictionary with coord and standard names"""
        d = {}
        for k in self.all_vars:
            d[k] = self[k]['standard_name']
        return d
    
    def _read_ini(self):
        parser = ConfigParser()
        parser.read(self.var_ini)
        return parser
        
    def __dir__(self):
        """Activates auto tab-completion for all variables"""
        return self.all_vars
    
    def __iter__(self):
        return self
    
    def __next__(self):
        self._idx += 1
        if self._idx == len(self.all_vars):
            self._idx = -1
            raise StopIteration
        var_name = self.all_vars[self._idx]
        return self[var_name]
    
    def __contains__(self, var_name):
        """Enables using ``in`` method
        
        Example
        -------
        >>> all_vars = VarCollection()
        >>> 'od550aer' in all_vars
        True
        >>> 'blaa' in all_vars
        False
        """
        if var_name in self.all_vars:
            return True
        return False
    
    def __getattr__(self, attr):
        """Use . operator to access variables
        
        Example
        -------
        >>> all_vars = VarCollection()
        >>> all_vars.od550aer
        Variable od550aer
        """
        if attr in self.__dict__:
            return self.__dict__[attr]
        return self[attr]
        
    def __getitem__(self, var_name):
        """Use [] operator to access variables
        
        Example
        -------
        >>> all_vars = VarCollection()
        >>> all_vars['od550aer']
        Variable od550aer
        """
        #make sure to be in the right namespace
        if var_name in self:
            return Variable(var_name, cfg=self._cfg_parser)
    
        low = var_name.lower()
        check = low.replace('3d','').replace('dry', '')
        
        if not check in self:
            try:
                _check_alias_family(check, parser=self._alias_parser)
            except VariableDefinitionError:    
                raise VariableDefinitionError("No default configuration "
                                              "available for variable {}"
                                              .format(var_name))
        return Variable(var_name, cfg=self._cfg_parser)
        
        
    def __str__(self):
        head = "Pyaerocom {}".format(type(self).__name__)
        s = '\n{}\n{}\n{}'.format(len(head)*"-", head, len(head)*"-")
        for v in self.all_vars:
            s += '\n{}'.format(v)
       
        return s   
  
def get_variable(var_name):
    from pyaerocom import const
    return const.VARS[var_name]

def all_vars_to_dataframe():
    """Make an overview table for all variables"""
    import pandas as pd
    head = ['Name', 'Standard name', 'unit', 'Wavelength [nm]', 'Dimensions',
            'Comments and purpose'] 
    res = []
    for varname in all_var_names():
        var = Variable(varname)
        res.append([varname, var.standard_name, var.unit, var.wavelength_nm,
                    var.dimensions, var.comments_and_purpose])
    df = pd.DataFrame(res, columns=head)
    return df

def all_var_names():
    """Helper method that returns all currently defined variable names"""
    return [k for k in Variable.read_config().keys()]

if __name__=="__main__":
    
    import pyaerocom as pya
    
    all_vars = VarCollection(pya.const._coords_info_file)

    print(pya.const.VARS.sconcso4)
    print(Variable('sconcso4'))