from copy import deepcopy
from pyaerocom._lowlevel_helpers import (BrowseDict, DictType,
                                         StrType, DictStrKeysListVals)
from pyaerocom.aeroval.aux_io_helpers import check_aux_info
from pyaerocom.aeroval._lowlev import EvalEntry

class ModelEntry(EvalEntry, BrowseDict):
    """Modeln configuration for evaluation (dictionary)

    Note
    ----
    Only :attr:`model_id` is mandatory, the rest is optional.

    Attributes
    ----------
    model_id : str
        ID of model run in AeroCom database (e.g. 'ECMWF_CAMS_REAN')
    model_ts_type_read : str or dict, optional
        may be specified to explicitly define the reading frequency of the
        model data. Not to be confused with :attr:`ts_type`, which specifies
        the frequency used for colocation. Can be specified variable specific
        by providing a dictionary.
    model_use_vars : dict
        dictionary that specifies mapping of model variables. Keys are
        observation variables, values are strings specifying the corresponding
        model variable to be used
        (e.g. model_use_vars=dict(od550aer='od550csaer'))
    model_add_vars : dict
        dictionary that specifies additional model variables. Keys are
        observation variables, values are lists of strings specifying the
        corresponding model variables to be used
        (e.g. model_use_vars=dict(od550aer=['od550csaer', 'od550so4']))
    model_read_aux : dict
        may be used to specify additional computation methods of variables from
        models. Keys are obs variables, values are dictionaries with keys
        `vars_required` (list of required variables for computation of var
        and `fun` (method that takes list of read data objects and computes
        and returns var)
    """
    model_id = StrType()
    model_use_vars = DictType()
    model_add_vars = DictStrKeysListVals()
    model_read_aux = DictType()

    def __init__(self, model_id, **kwargs):
        self.model_id = model_id
        self.model_ts_type_read = ''
        self.model_use_vars = {}
        self.model_add_vars = {}
        self.model_read_aux = {}

        self.update(**kwargs)

    @property
    def aux_funs_required(self):
        """
        Boolean specifying whether this entry requires auxiliary variables
        """
        return True if bool(self.model_read_aux) else False

    def get_all_vars(self):
        """
        Get all variables specified in this entry

        Note
        ----
        By default, in Aeroval, model entries are processed against an
        observation entry (see :class:`ObsEntry`), in which the variables to
        be processed are specified. That means, that in a  default setup,
        this method returns an empty list. Only if additional variables are
        specified in this object (via :attr:`model_use_vars` or
        :attr:`model_add_vars`), then this method will return these variables
        in the output list.

        Returns
        -------
        list
            list of variables
        """
        muv = list(self.model_use_vars.values())
        mav = []
        for val in self.model_add_vars.values():
            mav.extend(val)
        mra = list(self.model_read_aux.keys())
        return list(set(muv + mav + mra))

    def get_varname_web(self, mod_var, obs_var):
        if obs_var in self.model_add_vars and mod_var in self.model_add_vars[obs_var]:
            return mod_var
        return obs_var

    def _get_aux_funcs_setup(self, funs):
        mra = {}
        for var, aux_info in self.model_read_aux.items():
            mra[var] = check_aux_info(funcs=funs, **aux_info)
        return mra

    def prep_dict_analysis(self, funs=None) -> dict:
        if funs is None:
            funs = {}
        output = deepcopy(self.to_dict())
        if self.aux_funs_required:
            output['model_read_aux'].update(self._get_aux_funcs_setup(funs))
        return output
