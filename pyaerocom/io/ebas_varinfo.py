#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from configparser import ConfigParser

from pyaerocom import const
from pyaerocom._lowlevel_helpers import BrowseDict
from pyaerocom.io import EbasSQLRequest
from pyaerocom.exceptions import VarNotAvailableError

class EbasVarInfo(BrowseDict):
    """Interface for mapping between EBAS variable information and AeroCom

    For more information about EBAS variable and data information see
    `EBAS website <http://ebas.nilu.no/>`__.

    Attributes
    ----------
    var_name : str
        AeroCom variable name
    component : list
        list of EBAS variable / component names that are mapped to
        :attr:`var_name`
    matrix : list, optional
        list of EBAS matrix values that are accepted, default is None, i.e.
        all available matrices are used
    instrument : list, optional
        list of all instruments that are accepted for this variable
    requires : list, optional
        for variables that are computed and not directly available in EBAS.
        Provided as list of (AeroCom) variables that are required to
        compute :attr:`var_name` (e.g. for `sc550dryaer` this would be
        `[sc550aer,scrh]`).
    scale_factor : float, optional
        multiplicative scale factor that is applied in order to convert
        EBAS variable into AeroCom variable (e.g. 1.4 for conversion of
        EBAS OC measurement to AeroCom concoa variable)
    old_name : str
        old variable name (refers to outdated conventions, currently not used)

    Parameters
    ----------
    var_name : str
        AeroCom variable name
    init : bool
        if True, EBAS configuration for input variable is retrieved from
        data file ebas_config.ini (if possible)
    **kwargs
        additional keyword arguments (currently not used)

    """

    def __init__(self, var_name, init=True, **kwargs):
        self.var_name = var_name

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

        #: old variable name
        self.old_name = None

        #imports default information and, on top, variable information (if
        # applicable)
        if init:
            self.parse_from_ini(var_name)

    @staticmethod
    def PROVIDES_VARIABLES():
        """List specifying provided variables"""
        data = EbasVarInfo.open_config()
        return [k for k in data.keys()]

    @staticmethod
    def open_config():
        from pyaerocom import __dir__
        fpath = os.path.join(__dir__, "data", "ebas_config.ini")
        if not os.path.exists(fpath):
            raise IOError("Ebas config file could not be found: {}".format(fpath))
        conf_reader = ConfigParser()
        conf_reader.read(fpath)
        return conf_reader

    @property
    def var_name_aerocom(self):
        """Variable name in AeroCom convention"""
        return const.VARS[self.var_name].var_name_aerocom

    def parse_from_ini(self, var_name=None, conf_reader=None):
        """
        Parse EBAS info for input AeroCom variable (works also for aliases)

        Parameters
        ----------
        var_name : str
            AeroCom variable name
        conf_reader : ConfigParser
            open config parser object

        Raises
        ------
        VarNotAvailableError
            if variable is not supported

        Returns
        -------
        bool
            True, if default could be loaded, False if not
        """
        if conf_reader is None:
            conf_reader = self.open_config()

        if not var_name in conf_reader:
            # this will raise Variable
            var_name = const.VARS[var_name].var_name_aerocom
# =============================================================================
#             const.print_log.warning('Updating variable name {} to {}'
#                                     .format(self.var_name, var_name))
#             self.var_name = var_name
# =============================================================================
            if not var_name in conf_reader:
                raise VarNotAvailableError('Variable {} is not available in '
                                           'EBAS interface'.format(var_name))

        var_info = conf_reader[var_name]
        for key in self.keys():
            if key in var_info:
                val = var_info[key]
                if key in ('var_name', 'old_name') :
                    self[key] = val
                elif key == 'scale_factor':
                    self[key] = float(val.split('#')[0].strip())
                else:
                    self[key] = list(dict.fromkeys([x for x in val.split(',')]))
        self.var_name=var_name

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
        constraints
            request constraints deviating from default. For details on
            parameters see :class:`EbasSQLRequest`

        Returns
        -------
        EbasSQLRequest
            the SQL request object that can be used to retrieve corresponding
            file names using instance of :func:`EbasFileIndex.get_file_names`.
        """
        variables = self.get_all_components()

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
    # TODO: check this method...
    raise NotImplementedError('This method needs review and should be moved '
                              'into another module...')
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
