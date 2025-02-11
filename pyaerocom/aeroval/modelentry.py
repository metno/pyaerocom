# import inspect
from copy import deepcopy

from pydantic import BaseModel, ConfigDict
from pyaerocom.aeroval.aux_io_helpers import check_aux_info


class ModelEntry(BaseModel):
    """Model configuration for evaluation (BaseModel)

    Note
    ----model_read_aux
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
    model_rename_vars : dict
        key / value pairs specifying new variable names for model variables
        in the output json files (is applied after co-location).
    model_read_aux : dict
        may be used to specify additional computation methods of variables from
        models. Keys are obs variables, values are dictionaries with keys
        `vars_required` (list of required variables for computation of var
        and `fun` (method that takes list of read data objects and computes
        and returns var)
    """

    ##   Pydantic ConfigDict
    model_config = ConfigDict(
        validate_assignment=True,
        protected_namespaces=(),
    )

    model_id: str
    model_ts_type_read: str | dict | None = ""  # TODO: see if can make None
    model_name: str | None = None
    model_use_vars: dict = {}
    model_add_vars: dict[str, tuple[str, ...]] = {}
    model_read_aux: dict = {}
    model_rename_vars: dict = {}
    flex_ts_type: bool = True
    model_data_dir: str | None = None
    # attributes previously given as kwargs used in CAMS2_83
    gridded_reader_id: dict[str, str] = {"model": "ReadGridded", "obs": "ReadGridded"}
    model_kwargs: dict = {}

    @property
    def aux_funs_required(self):
        """
        Boolean specifying whether this entry requires auxiliary variables
        """
        return True if bool(self.model_read_aux) else False

    def json_repr(self) -> dict:
        return self.model_dump()

    def get_vars_to_process(self, obs_vars: tuple) -> tuple:
        """
        Get lists of obs / mod variables to be processed

        Parameters
        ----------
        obs_vars : tuple
            tuple of observation variables

        Returns
        -------
        list
            list of observation variables (potentially extended from input
            list)
        list
            corresponding model variables which are mapped based on content
            of :attr:`model_add_vars` and :attr:`model_use_vars`.

        """
        obsout, modout = [], []
        for obsvar in obs_vars:
            obsout.append(obsvar)
            if obsvar in self.model_use_vars:
                modout.append(self.model_use_vars[obsvar])
            else:
                modout.append(obsvar)

        for ovar, mvars in self.model_add_vars.items():
            for mvar in mvars:
                obsout.append(ovar)
                modout.append(mvar)
        return (obsout, modout)

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
        output = deepcopy(self.model_dump())
        if self.aux_funs_required:
            output["model_read_aux"].update(self._get_aux_funcs_setup(funs))
        return output
