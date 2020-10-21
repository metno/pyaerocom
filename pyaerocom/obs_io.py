#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings and helper methods / classes for I/O of obervation data

Note
----
Some settings like paths etc can be found in :mod:`pyaerocom.config.py`
"""
#: Wavelength tolerance for observations if data for required wavelength
#: is not available
OBS_WAVELENGTH_TOL_NM = 10.0

#: This boolean can be used to enable / disable the former (i.e. use
#: available wavelengths of variable in a certain range around variable
#: wavelength).
OBS_ALLOW_ALT_WAVELENGTHS = True


class ObsVarCombi(object):
    def __init__(self, obs_id, var_name):
        self.obs_id = obs_id
        self.var_name = var_name

    def __repr__(self):
        return '{};{}'.format(self.obs_id, self.var_name)

    def __str__(self):
        return repr(self)

class AuxInfoUngridded(object):
    MAX_VARS_PER_METHOD = 2
    def __init__(self, data_id, vars_supported, aux_requires,
                 aux_funs):

        if isinstance(vars_supported, str):
            vars_supported = [vars_supported]

        self.data_id = data_id
        self.vars_supported = vars_supported

        self.aux_requires = aux_requires
        self.aux_funs = aux_funs
        self.check_status()

    def to_dict(self):
        """Dictionary representation of this object"""
        return dict(
            data_id = self.data_id,
            vars_supported = self.vars_supported,
            aux_requires = self.aux_requires,
            aux_funs = self.aux_funs
            )

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
        for var in self.vars_supported:
            if not var in self.aux_requires:
                raise ValueError('Variable {} is not defined in attr '
                                     'aux_requires...'.format(var))
            elif not var in self.aux_funs:
                raise ValueError('Variable {} is not defined in attr '
                                     'aux_funs...'.format(var))

            fun = self.aux_funs[var]

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
                    if not obsvarstr in fun:
                        raise ValueError('Mismatch between aux_requires and '
                                         'aux_funs for variable {}. No such '
                                         'obs;var string {} in computation '
                                         'method {}'
                                         .format(var, obsvarstr, fun))

                    fc += 1
                    if fc > self.MAX_VARS_PER_METHOD:
                        raise NotImplementedError('So far only 2 variables '
                                                  'can be combined...')

if __name__ == '__main__':

    print(ObsVarCombi('Bla', 'od550aer'))