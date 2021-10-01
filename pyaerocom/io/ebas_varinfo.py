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
        """Open ebas_config.ini file with `ConfigParser`

        Returns
        -------
        ConfigParser
        """
        from pyaerocom import __dir__
        fpath = os.path.join(__dir__, "data", "ebas_config.ini")
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
            if not var_name in conf_reader:
                raise VarNotAvailableError('Variable {} is not available in '
                                           'EBAS interface'.format(var_name))

        var_info = conf_reader[var_name]
        for key in self.keys():
            if key in var_info:
                val = var_info[key]
                if key == 'scale_factor':
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
        if self.requires is not None:
            raise ValueError(
                f'This variable {self.var_name} requires other variables '
                f'for reading, thus more than one SQL request is needed. '
                f'Please use :func:`make_sql_requests` instead')

        variables = self.component

        if variables is None:
            raise AttributeError(
                f'At least one component (Ebas variable name) '
                f'must be specified for retrieval of variable {self.var_name}'
                )

        # default request
        req = EbasSQLRequest(variables=variables, matrices=self.matrix,
                              instrument_types=self.instrument,
                              statistics=self.statistics)

        req.update(**constraints)
        return req

    def make_sql_requests(self, **constraints):
        """Create a list of SQL requests for the specifications in this object

        Parameters
        ----------
        requests : dict, optional
            other SQL requests linked to this one (e.g. if this variable
            requires)
        constraints
            request constraints deviating from default. For details on
            parameters see :class:`EbasSQLRequest`

        Returns
        -------
        list
            list of :class:`EbasSQLRequest` instances for this component and
            potential required components.
        """
        requests = {}
        if self.component is not None:
            req = EbasSQLRequest(variables=self.component,
                                 matrices=self.matrix,
                                 instrument_types=self.instrument,
                                 statistics=self.statistics)
            req.update(**constraints)
            requests[self.var_name] = req

        if self.requires is not None:
            for var in self.requires:
                if var in requests:
                    # ToDo: check if this can be generalised better
                    raise ValueError(
                        f'Variable conflict in EBAS SQL request: '
                        f'{var} cannot depent on itself...')
                info = EbasVarInfo(var)
                _reqs = info.make_sql_requests(**constraints)
                for _var, _req in _reqs.items():
                    if _var in requests:
                        # ToDo: check if this can be generalised better
                        raise ValueError(
                            f'Variable conflict in EBAS SQL request: '
                            f'{_var} cannot depent on itself...')
                    requests[_var] = _req

        return requests

    def __str__(self):
        head = "Pyaerocom {}".format(type(self).__name__)
        s = "\n{}\n{}".format(head, len(head)*"-")
        for k, v in self.items():
                s += "\n%s: %s" %(k,v)
        return s
