"""
Settings and helper methods / classes for I/O of observation data

Note
----
Some settings like paths etc can be found in :mod:`pyaerocom.config.py`
"""

from pyaerocom._lowlevel_helpers import dict_to_str, str_underline

#: Wavelength tolerance for observations if data for required wavelength
#: is not available
OBS_WAVELENGTH_TOL_NM = 10.0

#: This boolean can be used to enable / disable the former (i.e. use
#: available wavelengths of variable in a certain range around variable
#: wavelength).
OBS_ALLOW_ALT_WAVELENGTHS = True


class ObsVarCombi:
    def __init__(self, obs_id, var_name):
        self.obs_id = obs_id
        self.var_name = var_name

    def __repr__(self):
        return f"{self.obs_id};{self.var_name}"

    def __str__(self):
        return repr(self)


class AuxInfoUngridded:
    MAX_VARS_PER_METHOD = 2

    def __init__(
        self, data_id, vars_supported, aux_requires, aux_merge_how, aux_funs=None, aux_units=None
    ):
        self.data_id = data_id
        self.vars_supported = vars_supported

        self.aux_requires = aux_requires
        self.aux_merge_how = aux_merge_how
        self.aux_funs = aux_funs
        self.aux_units = aux_units
        self.check_status()

    def to_dict(self):
        """Dictionary representation of this object

        Ignores any potential private attributes.
        """
        dd = {}
        for key, val in self.__dict__.items():
            if any([key.startswith(x) for x in ("_", "__")]):
                continue
            dd[key] = val
        return dd

    def check_status(self):
        """
        Check if specifications are correct and consistent

        Raises
        ------
        ValueError
            If one of the class attributes is invalid
        NotImplementedError
            If computation method contains more than 2 variables / datasets

        """
        if isinstance(self.vars_supported, str):
            self.vars_supported = [self.vars_supported]

        if isinstance(self.aux_merge_how, str):
            nv = len(self.vars_supported)
            self.aux_merge_how = dict(zip(self.vars_supported, [self.aux_merge_how] * nv))
        if self.aux_funs is None:
            self.aux_funs = {}
        if self.aux_units is None:
            self.aux_units = {}

        for var in self.vars_supported:
            if var not in self.aux_requires:
                raise ValueError(f"Variable {var} is not defined in attr aux_requires...")

            elif var not in self.aux_merge_how:
                raise ValueError(
                    f"Missing information about how {var} should be merged (aux_merge_how)"
                )
            merge_how = self.aux_merge_how[var]
            if merge_how == "eval":
                if var not in self.aux_funs:
                    raise ValueError(
                        f"Specification of computation function is missing for var {var}"
                    )
                fun = self.aux_funs[var]

                if not isinstance(fun, str):
                    raise ValueError("eval functions need to be strings")

            aux_info = self.aux_requires[var]

            fc = 0
            for aux_id, var_info in aux_info.items():
                if isinstance(var_info, str):
                    # make sure variables are represented as list, even if
                    # it is only one
                    aux_info[aux_id] = var_info = [var_info]
                for _var in var_info:
                    obsvar = ObsVarCombi(aux_id, _var)
                    obsvarstr = str(obsvar)
                    if merge_how == "eval" and obsvarstr not in fun:
                        raise ValueError(
                            f"Mismatch between aux_requires and aux_funs for variable {var}. "
                            f"No such obs;var string {obsvarstr} in computation method {fun}"
                        )

                    fc += 1
                    if fc > self.MAX_VARS_PER_METHOD:
                        raise NotImplementedError("So far only 2 variables can be combined...")

    def __repr__(self):
        return f"{type(self).__name__}; data_id: {self.data_id}; vars_supported: {self.vars_supported}"

    def __str__(self):
        name = str(type(self).__name__)
        s = str_underline(name)
        s += dict_to_str(self.to_dict())
        return s
