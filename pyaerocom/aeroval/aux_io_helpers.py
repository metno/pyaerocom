import importlib
import os
import sys
from collections.abc import Callable

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from typing import TYPE_CHECKING

from pydantic import (
    BaseModel,
    model_validator,
)

from pyaerocom._lowlevel_helpers import AsciiFileLoc


def check_aux_info(fun, vars_required, funcs):
    """
    Make sure information is correct for computation of auxiliary variables

    Parameters
    ----------
    fun : str or callable
        name of function or function used to compute auxiliary variable. If
        str, then arg `funcs` needs to be provided.
    vars_required : list
        list of required variables for computation of auxiliary variable.
    funcs : dict
        Dictionary with possible functions (values) and names (keys)

    Returns
    -------
    dict
        dict containing callable function object and list of variables
        required.

    """
    spec = _AuxReadSpec(fun=fun, vars_required=vars_required, funcs=funcs)
    return dict(fun=spec.fun, vars_required=spec.vars_required)


class _AuxReadSpec(BaseModel):
    """
    Class that specifies requirements for computation of additional variables

    Attributes
    ----------
    vars_required : list
        list of required variables for computation of auxiliary variable.
    fun : callable
        function used to compute auxiliary variable.

    Parameters
    ----------
    fun : str or callable
        name of function or function used to compute auxiliary variable. If
        str, then arg `funcs` needs to be provided.
    vars_required : list
        list of required variables for computation of auxiliary variable.
    funcs : dict
        Dictionary with possible functions (values) and names (keys)

    """

    if TYPE_CHECKING:
        fun: Callable
    else:
        fun: str | Callable
    vars_required: list[str]
    funcs: dict[str, Callable]

    @model_validator(mode="after")
    def validate_fun(self) -> Self:
        if callable(self.fun):
            return self
        elif isinstance(self.fun, str):
            self.fun = self.funcs[self.fun]
            return self
        else:
            raise ValueError("failed to retrieve aux func")


class ReadAuxHandler:
    """
    Helper class for import of auxiliary function objects

    Attributes
    ----------
    aux_file : str
        path to python module containing function definitions (note: function
        definitions in module need to be stored in a dictionary called
        `FUNS` in the file, where keys are names of the functions and
        values are callable objects.)

    Parameters
    ----------
    aux_file : str
        input file containing auxiliary functions (details see Attributes
        section).
    """

    aux_file = AsciiFileLoc(assert_exists=True, auto_create=False)

    def __init__(self, aux_file: str):
        self.aux_file = aux_file

    def import_module(self):
        """
        Import :attr:`aux_file` as python module

        Uses :func:`importlib.import_module` for import.
        Returns
        -------
        module
            imported module.

        """
        moddir, fname = os.path.split(self.aux_file)
        if moddir not in sys.path:
            sys.path.append(moddir)
        modname = fname.split(".")[0]
        return importlib.import_module(modname)

    def import_all(self):
        """
        Import all callable functions in module with their names

        Currently, these are expected to be stored in a dictionary called
        `FUNS` which should be defined in the python module.

        Returns
        -------
        dict
            function definitions.

        """
        mod = self.import_module()
        return mod.FUNS
