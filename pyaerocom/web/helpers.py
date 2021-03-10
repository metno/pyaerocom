#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 14:00:44 2019

ToDo
----
- the configuration classes could inherit from a base class or could be more unified

"""
import simplejson
from traceback import format_exc
from pyaerocom import const
from pyaerocom._lowlevel_helpers import BrowseDict
from pyaerocom.metastandards import DataSource
from pyaerocom.exceptions import InitialisationError

class ObsConfigEval(BrowseDict):
    """Observation configuration for evaluation (dictionary)

    Note
    ----
    Only :attr:`obs_id` and `obs_vars` are mandatory, the rest is optional.

    Attributes
    ----------
    obs_id : str
        ID of observation network in AeroCom database
        (e.g. 'AeronetSunV3Lev2.daily')
    obs_type : str
        specifies whether data is gridded or ungridded. Choose from 'gridded'
        or 'ungridded'. This is optional, but some functionality will not work
        if it is not set (such as registering auxiliary variables).
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
        the web interface for separating different categories of measurements
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
    ALT_NAMES_VERT_CODES = dict(ModelLevel = 'Profile')

    SUPPORTED_VERT_LOCS = DataSource.SUPPORTED_VERT_LOCS
    def __init__(self, **kwargs):

        self.obs_id = None
        self.obs_type = None

        self.obs_vars = None
        self.obs_ts_type_read = None
        self.obs_vert_type = None
        self.obs_aux_requires = {}
        self.instr_vert_loc = None

        self.is_superobs=False
        self.only_superobs=False

        self.read_opts_ungridded = None

        self.update(**kwargs)
        self.check_cfg()
        self.check_add_obs()

    def check_add_obs(self):
        """Check if this dataset is an auxiliary post dataset"""
        if not isinstance(self.obs_aux_requires, dict):
            raise ValueError(
                f'Invalid value obs_aux_requires={self.obs_aux_requires}'
                f'Need dict...'
                )
        elif len(self.obs_aux_requires) > 0:
            if not self.obs_type == 'ungridded':
                raise NotImplementedError(
                    'Cannot initialise auxiliary setup for {}. Aux obs reading '
                    'is so far only possible for ungridded observations.'
                    .format(self.obs_id))
            try:
                const.add_ungridded_post_dataset(**self)
            except Exception:
                raise InitialisationError(
                    'Cannot initialise auxiliary reading setup for {}. '
                    'Reason:\n{}'.format(self.obs_id, format_exc()))


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
            const.print_log.warning('Please use {} for obs_vert_code '
                                        'and not {}'.format(_ovt, ovt))
            return _ovt
        valid = self.SUPPORTED_VERT_CODES + list(self.ALT_NAMES_VERT_CODES.keys())
        raise ValueError('Invalid value for obs_vert_type: {}. '
                         'Supported codes are {}.'
                         .format(self.obs_vert_type,
                                 valid))

class ModelConfigEval(BrowseDict):
    """Modeln configuration for evaluation (dictionary)

    Note
    ----
    Only :attr:`model_id` is mandatory, the rest is optional.

    Attributes
    ----------
    model_id : str
        ID of model run in AeroCom database (e.g. 'ECMWF_CAMS_REAN')
    model_ts_type_read : :obj:`str` or :obj:`dict`, optional
        may be specified to explicitly define the reading frequency of the
        model data. Not to be confused with :attr:`ts_type`, which specifies
        the frequency used for colocation. Can be specified variable specific
        by providing a dictionary.
    model_use_vars : :obj:`dict`, optional
        dictionary that specifies mapping of model variables. Keys are
        observation variables, values are the corresponding model variables
        (e.g. model_use_vars=dict(od550aer='od550csaer'))
    model_read_aux : :obj:`dict`, optional
        may be used to specify additional computation methods of variables from
        models. Keys are obs variables, values are dictionaries with keys
        `vars_required` (list of required variables for computation of var
        and `fun` (method that takes list of read data objects and computes
        and returns var)
    """
    def __init__(self, model_id, **kwargs):
        self.model_id = model_id
        self.model_ts_type_read = None
        self.model_use_vars = {}
        self.model_read_aux = {}

        self.update(**kwargs)
        self.check_cfg()

    def check_cfg(self):
        """Check that minimum required attributes are set and okay"""
        if not isinstance(self.model_id, str):
            raise ValueError('Invalid input for model_id {}. Need str.'
                             .format(self.model_id))

def read_json(file_path):
    """Read json file

    Parameters
    ----------
    file_path : str
        json file path

    Returns
    -------
    dict
        content as dictionary
    """
    with open(file_path, 'r') as f:
        data = simplejson.load(f)
    return data

def write_json(data_dict, file_path, indent=4):
    """Save json file

    Parameters
    ----------
    data_dict : dict
        dictionary that can be written to json file
    file_path : str
        output file path
    """
    with open(file_path, 'w+') as f:
        f.write(simplejson.dumps(data_dict, indent=4))
