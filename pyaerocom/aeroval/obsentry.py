#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 14:00:44 2019

ToDo
----
- the configuration classes could inherit from a base class or could be more unified

"""
from pyaerocom import const
from pyaerocom._lowlevel_helpers import BrowseDict, ListOfStrings
from pyaerocom.metastandards import DataSource
from pyaerocom.aeroval._lowlev import EvalEntry

class ObsEntry(EvalEntry, BrowseDict):
    """Observation configuration for evaluation (dictionary)

    Note
    ----
    Only :attr:`obs_id` and `obs_vars` are mandatory, the rest is optional.

    Attributes
    ----------
    obs_id : str
        ID of observation network in AeroCom database
        (e.g. 'AeronetSunV3Lev2.daily')
    obs_vars : list
        list of pyaerocom variable names that are supposed to be analysed
        (e.g. ['od550aer', 'ang4487aer'])
    obs_ts_type_read : :obj:`str` or :obj:`dict`, optional
        may be specified to explicitly define the reading frequency of the
        observation data (so far, this does only apply to gridded obsdata such
        as satellites). For ungridded reading, the frequency may be specified
        via :attr:`obs_id`, where applicable (e.g. AeronetSunV3Lev2.daily).
        Can be specified variable specific in form of dictionary.
    obs_vert_type : :obj:`str` or :obj:`dict`, optional
        Aerocom vertical code encoded in the model filenames (only AeroCom 3
        and later). Specifies which model file should be read in case there are
        multiple options (e.g. surface level data can be read from a
        *Surface*.nc file as well as from a *ModelLevel*.nc file). If input is
        string (e.g. 'Surface'), then the corresponding vertical type code is
        used for reading of all variables that are colocated (i.e. that are
        specified in :attr:`obs_vars`). Else (if input is dictionary, e.g.
        `obs_vert_type=dict(od550aer='Column', ec550aer='ModelLevel')`),
        information is extracted variable specific, for those who are defined
        in the dictionary, for all others, `None` is used.
    obs_aux_requires : dict, optional
        information about required datasets / variables for auxiliary
        variables.
    instr_vert_loc : str, optional
        vertical location code of observation instrument. This is used in
        the aeroval interface for separating different categories of measurements
        such as "ground", "space" or "airborne".
    is_superobs : bool
        if True, this observation is a combination of several others which all
        have to have their own obs config entry.
    only_superobs : bool
        this indicates whether this configuration is only to be used as part
        of a superobs network, and not individually.
    read_opts_ungridded : :obj:`dict`, optional
        dictionary that specifies reading constraints for ungridded reading
        (c.g. :class:`pyaerocom.io.ReadUngridded`).
    """
    SUPPORTED_VERT_CODES = ['Column', 'Profile', 'Surface']
    ALT_NAMES_VERT_CODES = dict(ModelLevel='Profile')

    SUPPORTED_VERT_LOCS = DataSource.SUPPORTED_VERT_LOCS

    obs_vars = ListOfStrings()
    def __init__(self, **kwargs):

        self.obs_id = ''

        self.obs_vars = []
        self.obs_ts_type_read = None
        self.obs_vert_type = ''
        self.obs_aux_requires = {}
        self.instr_vert_loc = None

        self.is_superobs=False
        self.only_superobs=False

        self.read_opts_ungridded = {}

        self.update(**kwargs)
        self.check_cfg()

    def get_all_vars(self) -> list:
        """
        Get list of all variables associated with this entry

        Returns
        -------
        list
            DESCRIPTION.

        """
        return self.obs_vars

    def get_vert_code(self, var):
        """Get vertical code name for obs / var combination"""
        vc = self['obs_vert_type']
        if isinstance(vc, str):
            val = vc
        elif isinstance(vc, dict) and var in vc:
            val = vc[var]
        else:
            raise ValueError(f'invalid value for obs_vert_type: {vc}')
        if not val in self.SUPPORTED_VERT_CODES:
            raise ValueError(
                f'invalid value for obs_vert_type: {val}. Choose from '
                f'{self.SUPPORTED_VERT_CODES}.')
        return val


    def check_cfg(self):
        """Check that minimum required attributes are set and okay"""

        if not self.is_superobs and not isinstance(self.obs_id, (str, dict)):
            raise ValueError('Invalid value for obs_id: {}. Need str or dict '
                         'or specification of ids and variables via '
                         'obs_compute_post'
                         .format(self.obs_id))
        if isinstance(self.obs_vars, str):
            self.obs_vars = [self.obs_vars]
        elif not isinstance(self.obs_vars, list):
            raise ValueError('Invalid input for obs_vars. Need list or str, '
                             'got: {}'.format(self.obs_vars))
        ovt = self.obs_vert_type
        if ovt is None:
            raise ValueError('obs_vert_type is not defined. Please specify '
                             'using either of the available codes: {}. '
                             'It may be specified for all variables (as string) '
                             'or per variable using a dict'
                             .format(self.SUPPORTED_VERT_CODES))
        elif (isinstance(ovt, str) and not ovt in self.SUPPORTED_VERT_CODES):
            self.obs_vert_type = self._check_ovt(ovt)
        elif isinstance(self.obs_vert_type, dict):
            for var_name, val in self.obs_vert_type.items():
                if not val in self.SUPPORTED_VERT_CODES:
                    raise ValueError('Invalid value for obs_vert_type: {} '
                                     '(variable {}). Supported codes are {}.'
                                     .format(self.obs_vert_type,
                                             var_name,
                                             self.SUPPORTED_VERT_CODES))
        ovl = self.instr_vert_loc
        if isinstance(ovl, str) and not ovl in self.SUPPORTED_VERT_LOCS:
            raise AttributeError(
                f'Invalid value for instr_vert_loc: {ovl} for {self.obs_id}. '
                f'Please choose from: {self.SUPPORTED_VERT_LOCS}'
                )

    def _check_ovt(self, ovt):
        """Check if obs_vert_type string is valid alias

        Parameters
        ----------
        ovt : str
            obs_vert_type string

        Returns
        -------
        str
            valid obs_vert_type

        Raises
        ------
        ValueError
            if `ovt` is invalid
        """
        if ovt in self.ALT_NAMES_VERT_CODES:
            _ovt = self.ALT_NAMES_VERT_CODES[ovt]
            const.print_log.warning(
                f'Please use {_ovt} for obs_vert_code and not {ovt}')
            return _ovt
        valid = self.SUPPORTED_VERT_CODES + list(self.ALT_NAMES_VERT_CODES.keys())
        raise ValueError('Invalid value for obs_vert_type: {}. '
                         'Supported codes are {}.'
                         .format(self.obs_vert_type,
                                 valid))

