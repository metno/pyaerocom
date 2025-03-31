import fnmatch
import logging
import os

from pyaerocom.exceptions import VariableDefinitionError
from pyaerocom.variable import Variable
from pyaerocom.variable_helpers import parse_aliases_ini, parse_variables_ini

from pyaerocom.units import Unit

logger = logging.getLogger(__name__)


class VarCollection:
    """Variable access class based on variables.ini file"""

    def __init__(self, var_ini):
        self._all_vars = None
        self._var_ini = None

        self.var_ini = var_ini

        self._vars_added = {}

        self._cfg_parser = parse_variables_ini(var_ini)
        self._alias_parser = parse_aliases_ini()
        self._idx = -1

    @property
    def all_vars(self):
        """List of all variables

        Note
        ----
        Does not include variable names that may be inferred via
        alias families as defined in section [alias_families] in
        aliases.ini.
        """
        if self._all_vars is None:
            self._all_vars = list(self._cfg_parser) + list(self._vars_added)
        return self._all_vars

    @property
    def var_ini(self):
        """Config file specifying variable information"""
        return self._var_ini

    @var_ini.setter
    def var_ini(self, var_ini):
        if not isinstance(var_ini, str):
            raise ValueError("Invalid input for var_ini, need str")
        elif not os.path.exists(var_ini):
            raise FileNotFoundError(f"File {var_ini} does not exist")
        self._var_ini = var_ini

    def add_var(self, var):
        """Add a new variable to this collection

        Minimum requirement for new variables are attributes var_name and
        units.

        Parameters
        ----------
        var : Variable
            new variable definition

        Raises
        ------
        VariableDefinitionError
            if a variable is already defined under that name

        Returns
        -------
        None
        """
        if not isinstance(var.var_name, str):
            raise ValueError("Attr. var_name needs to be assigned to input variable")
        if var.var_name in self.all_vars:
            raise VariableDefinitionError(f"variable with name {var.var_name} is already defined")
        if not isinstance(var, Variable):
            raise ValueError("Can only add instances of Variable class...")
        if not isinstance(var.units, str):
            var.units = str(Unit(var.units))
        self._all_vars.append(var.var_name)
        self._vars_added[var.var_name] = var

    def delete_variable(self, var_name: str) -> None:
        """
        Remove input variable from this collection

        Parameters
        ----------
        var_name : str
            name of variable

        Raises
        ------
        VariableDefinitionError
            if variable does not exist or if it exists more than once.

        Returns
        -------
        None

        """
        all_vars = self.all_vars
        matches = [i for i, x in enumerate(all_vars) if x == var_name]
        if len(matches) == 0:
            raise VariableDefinitionError(f"No such variable {var_name} in VarCollection")
        elif len(matches) > 1:
            raise VariableDefinitionError(
                f"FATAL: found multiple matches for variable {var_name} in "
                f"VarCollection. Please check variables.ini"
            )
        all_vars.pop(matches[0])
        self._all_vars == all_vars
        if var_name in self._vars_added:
            del self._vars_added[var_name]

    def get_var(self, var_name):
        """
        Get variable based on variable name

        Parameters
        ----------
        var_name : str
            name of variable

        Raises
        ------
        VariableDefinitionError
            if no variable under input var_name is registered.

        Returns
        -------
        Variable
            Variable instance

        """
        if var_name in self._vars_added:
            return self._vars_added[var_name]
        var = Variable(var_name, cfg=self._cfg_parser)
        if var.var_name_aerocom not in self:
            raise VariableDefinitionError(
                f"Error (VarCollection): input variable {var_name} is not supported"
            )
        return var

    def find(self, search_pattern):
        """Find all variables that match input search pattern

        Note
        ----
        Searches for matches in variable names (:attr:`Variable.var_name`) and
        standard name (:attr:`Variable.standard_name`).

        Parameters
        ----------
        search_pattern : str
            variable search pattern

        Returns
        -------
        list
            AeroCom variable names that match the search pattern
        """
        matches = []
        for var in self:
            if fnmatch.fnmatch(var.var_name, search_pattern):
                matches.append(var.var_name)
            elif isinstance(var.standard_name, str) and fnmatch.fnmatch(
                var.standard_name, search_pattern
            ):
                matches.append(var.var_name)
        return matches

    def __dir__(self):
        """Activates auto tab-completion for all variables"""
        return self.all_vars

    def __iter__(self):
        return self

    def __next__(self):
        self._idx += 1
        if self._idx == len(self.all_vars):
            self._idx = -1
            raise StopIteration
        var_name = self.all_vars[self._idx]
        return self[var_name]

    def __contains__(self, var_name):
        if var_name in self.all_vars:
            return True
        return False

    def __len__(self):
        return len(self.all_vars)

    def __getitem__(self, var_name):
        return self.get_var(var_name)

    def __repr__(self):
        return f"VarCollection ({len(self)} entries)"

    def __str__(self):
        return repr(self)
