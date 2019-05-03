#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains functionality related to regions in pyaerocom
"""
import os
from ast import literal_eval
import re
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
 
def _read_alias_ini():
    """Read all alias definitions from aliases.ini file and return as dict
    
    Returns
    -------
    dict
        keys are AEROCOM standard names of variable, values are corresponding
        aliases
    """
    file = os.path.join(__dir__, "data", "aliases.ini")
    if not os.path.exists(file):
        return {}
    parser = ConfigParser()
    parser.read(file)
    aliases = {}
    items = parser['aliases']
    for var_name in items:
        _aliases = [x.strip() for x in items[var_name].strip().split(',')]
        for alias in _aliases:
            aliases[alias] = var_name
    return aliases

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
    unit : str
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
        
    _TYPE_CONV={'wavelength_nm': float,
                'minimum': float,
                'maximum': float,
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
        self.unit = 1
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
        fpath = os.path.join(__dir__, "data", "variables.ini")
        if not os.path.exists(fpath):
            raise IOError("Variable ini file could not be found: %s"
                          %fpath)
        cfg = ConfigParser()
        cfg.read(fpath)
        return cfg
    
    
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
        file = os.path.join(__dir__, "data", "aliases.ini")
        parser = ConfigParser()
        parser.read(file)
        info = parser['aliases']
        if self.var_name in info:
            return [a.strip() for a in info[self.var_name].split(',')]
        return []
    
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
                aliases = _read_alias_ini()
                if var_name in aliases:
                    var_name = aliases[var_name]
                    var_info = cfg[var_name]
                else:
                    logger.warning("No default configuration available for "
                                   "variable {}. Using DEFAULT settings"
                                   .format(var_name))
            
        default = cfg['DEFAULT']
        
        for key in self.keys():
            ok = True
            if key in var_info:
                val = var_info[key]
            elif key in default:
                val = default[key]
            else:
                ok = False
            if ok:
                if key in self._TYPE_CONV:
                    try:
                        val = self._TYPE_CONV[key](val)
                    except:
                        pass
                elif key == 'unit':
                    if val == 'None' or val=='1':
                        val=1
                if val == 'None':
                    val = None
                self[key] = val
        self.var_name = var_name
        
    def __setitem__(self, key, val):
        self.__dict__[key] = val
    
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __repr__(self):
       return ("Variable {}\nUnit: {}\ndescriptions: {}\nstandard_name: {}\n"
               .format(self.var_name, self.unit, self.description,
                       self.standard_name))
   
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
    _var_ini = None
    def __init__(self, var_ini):
        
        self.var_ini = var_ini
        
        self._cfg = self._read_ini()
        
        self.all_vars = [k.lower() for k in self._cfg.keys()]
    
        
        logger.info("Importing variable aliases info")
        self.all_vars.extend(list(_read_alias_ini()))
            
    @property
    def var_ini(self):
        """Config file specifying variable information"""
        return self._var_ini
    
    @var_ini.setter
    def var_ini(self, var_ini):
        
        if not os.path.exists(var_ini):
            raise IOError("File {} does not exist".format(var_ini))
        self._var_ini = var_ini
    
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
    
    def __getattr__(self, var_name):
        """Use . operator to access variables
        
        Example
        -------
        >>> all_vars = VarCollection()
        >>> all_vars.od550aer
        Variable od550aer
        """
        return self[var_name]
        
    def __getitem__(self, var_name):
        """Use [] operator to access variables
        
        Example
        -------
        >>> all_vars = VarCollection()
        >>> all_vars['od550aer']
        Variable od550aer
        """
        #make sure to be in the right namespace
        low = var_name.lower()
        check = low.replace('3d','').replace('dry', '')
        
        if not check in self:
            raise VariableDefinitionError("No default configuration available "
                                          "for variable {}".format(var_name))
        return Variable(var_name, cfg=self._cfg)
        
        
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
    from pyaerocom import const
    all_vars = VarCollection(const._coords_info_file)
    
    print(all_vars.asc)
    
