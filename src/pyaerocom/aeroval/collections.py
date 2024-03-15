import abc
from fnmatch import fnmatch

from pyaerocom._lowlevel_helpers import BrowseDict
from pyaerocom.aeroval.modelentry import ModelEntry
from pyaerocom.aeroval.obsentry import ObsEntry
from pyaerocom.exceptions import EntryNotAvailable, EvalEntryNameError


class BaseCollection(BrowseDict, abc.ABC):
    #: maximum length of entry names
    MAXLEN_KEYS = 25
    #: Invalid chars in entry names
    FORBIDDEN_CHARS_KEYS = ["_"]

    def _check_entry_name(self, key):
        if any([x in key for x in self.FORBIDDEN_CHARS_KEYS]):
            raise EvalEntryNameError(
                f"Invalid name: {key}. Must not contain any of the following "
                f"characters: {self.FORBIDDEN_CHARS_KEYS}"
            )

    def __setitem__(self, key, value):
        self._check_entry_name(key)
        if "web_interface_name" in value:
            self._check_entry_name(value["web_interface_name"])
        super().__setitem__(key, value)

    def keylist(self, name_or_pattern: str = None) -> list:
        """Find model names that match input search pattern(s)

        Parameters
        ----------
        name_or_pattern : str, optional
            Name or pattern specifying search string.

        Returns
        -------
        list
            list of keys in collection that match input requirements. If
            `name_or_pattern` is None, all keys will be returned.

        Raises
        ------
        KeyError
            if no matches can be found
        """
        if name_or_pattern is None:
            name_or_pattern = "*"

        matches = []
        for key in self.keys():
            if fnmatch(key, name_or_pattern) and not key in matches:
                matches.append(key)
        if len(matches) == 0:
            raise KeyError(f"No matches could be found that match input {name_or_pattern}")
        return matches

    @abc.abstractmethod
    def get_entry(self, key) -> object:
        """
        Getter for eval entries

        Raises
        ------
        KeyError
            if input name is not in this collection
        """
        pass

    @property
    @abc.abstractmethod
    def web_iface_names(self) -> list:
        """
        List of webinterface names for
        """
        pass


class ObsCollection(BaseCollection):
    """
    Dict-like object that represents a collection of obs entries

    Keys are obs names, values are instances of :class:`ObsEntry`. Values can
    also be assigned as dict and will automatically be converted into
    instances of :class:`ObsEntry`.


    Note
    ----
    Entries must not necessarily be only observations but may also be models.
    Entries provided in this collection refer to the y-axis in the AeroVal
    heatmap display and must fulfill the protocol defined by :class:`ObsEntry`.

    """

    SETTER_CONVERT = {dict: ObsEntry}

    def get_entry(self, key) -> object:
        """
        Getter for obs entries

        Raises
        ------
        KeyError
            if input name is not in this collection
        """
        try:
            entry = self[key]
            entry["obs_name"] = self.get_web_iface_name(key)
            return entry
        except (KeyError, AttributeError):
            raise EntryNotAvailable(f"no such entry {key}")

    def get_all_vars(self) -> list:
        """
        Get unique list of all obs variables from all entries

        Returns
        -------
        list
            list of variables specified in obs collection

        """
        vars = []
        for ocfg in self.values():
            vars.extend(ocfg.get_all_vars())
        return sorted(list(set(vars)))

    def get_web_iface_name(self, key):
        """
        Get webinterface name for entry

        Note
        ----
        Normally this is the key of the obsentry in :attr:`obs_config`,
        however, it might be specified explicitly via key `web_interface_name`
        in the corresponding value.

        Parameters
        ----------
        key : str
            key of entry.

        Returns
        -------
        str
            corresponding name

        """
        entry = self[key]
        if not "web_interface_name" in entry:
            return key
        return entry["web_interface_name"]

    @property
    def web_iface_names(self) -> list:
        """
        List of web interface names for each obs entry

        Returns
        -------
        list
        """
        return [self.get_web_iface_name(key) for key in self.keylist()]

    @property
    def all_vert_types(self):
        """List of unique vertical types specified in this collection"""
        return list({x["obs_vert_type"] for x in self.values()})


class ModelCollection(BaseCollection):
    """
    Dict-like object that represents a collection of model entries

    Keys are model names, values are instances of :class:`ModelEntry`. Values
    can also be assigned as dict and will automatically be converted into
    instances of :class:`ModelEntry`.


    Note
    ----
    Entries must not necessarily be only models but may also be observations.
    Entries provided in this collection refer to the x-axis in the AeroVal
    heatmap display and must fulfill the protocol defined by
    :class:`ModelEntry`.

    """

    SETTER_CONVERT = {dict: ModelEntry}

    def get_entry(self, key) -> object:
        """Get model entry configuration

        Since the configuration files for experiments are in json format, they
        do not allow the storage of executable custom methods for model data
        reading. Instead, these can be specified in a python module that may
        be specified via :attr:`add_methods_file` and that contains a
        dictionary `FUNS` that maps the method names with the callable methods.

        As a result, this means that, by default, custom read methods for
        individual models in :attr:`model_config` do not contain the
        callable methods but only the names. This method will take care of
        handling this and will return a dictionary where potential custom
        method strings have been converted to the corresponding callable
        methods.

        Parameters
        ----------
        model_name : str
            name of model

        Returns
        -------
        dict
            Dictionary that specifies the model setup ready for the analysis
        """
        try:
            entry = self[key]
            entry["model_name"] = key
            return entry
        except (KeyError, AttributeError):
            raise EntryNotAvailable(f"no such entry {key}")

    @property
    def web_iface_names(self) -> list:
        """
        List of web interface names for each obs entry

        Returns
        -------
        list
        """
        return self.keylist()
