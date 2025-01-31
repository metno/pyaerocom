import abc
from fnmatch import fnmatch

from pyaerocom.aeroval.modelentry import ModelEntry
from pyaerocom.aeroval.obsentry import ObsEntry
from pyaerocom.exceptions import EntryNotAvailable


class BaseCollection(abc.ABC):
    def __init__(self):
        """
        Initialize an instance of BaseCollection.
        The instance maintains a dictionary of entries.
        """
        self._entries = {}

    def __iter__(self):
        """
        Iterates over each entry in the collection.

        Yields
        ------
        object
            The next entry in the collection.
        """
        yield from self._entries.values()

    @abc.abstractmethod
    def add_entry(self, key, value) -> None:
        """
        Abstract method to add an entry to the collection.

        Parameters
        ----------
        key: Hashable
            The key of the entry.
        value: object
            The value of the entry.
        """
        pass

    @abc.abstractmethod
    def remove_entry(self, key) -> None:
        """
        Abstract method to remove an entry from the collection.

        Parameters
        ----------
        key: Hashable
            The key of the entry to be removed.
        """
        pass

    @abc.abstractmethod
    def get_entry(self, key) -> object:
        """
        Abstract method to get an entry from the collection.

        Parameters
        ----------
        key: Hashable
            The key of the entry to retrieve.

        Returns
        -------
        object
            The entry associated with the provided key.
        """
        pass

    def keylist(self, name_or_pattern: str = None) -> list[str]:
        """Find model / obs names that match input search pattern(s)

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
        # Special case where the model cfg is empty, used for obs-only
        if self._entries.keys() == []:
            return []

        if name_or_pattern is None:
            name_or_pattern = "*"

        matches = []
        for key in self._entries.keys():
            if fnmatch(key, name_or_pattern) and key not in matches:
                matches.append(key)

        if len(matches) == 0:
            raise KeyError(f"No matches could be found that match input {name_or_pattern}")
        return matches

    @property
    def web_interface_names(self) -> list:
        """
        List of web interface names for each obs entry

        Returns
        -------
        list
        """
        return self.keylist()

    def as_dict(self) -> dict:
        """
        Convert object to serializable dict

        Returns
        -------
        dict
            content of class

        """
        output = {}
        for key, val in self._entries.items():
            if hasattr(val, "json_repr"):
                val = val.json_repr()
            output[key] = val
        return output


class ObsCollection(BaseCollection):
    """
    Object that represents a collection of obs entries

    "Keys" are obs names, values are instances of :class:`ObsEntry`. Values can
    also be assigned as dict and will automatically be converted into
    instances of :class:`ObsEntry`.


    Note
    ----
    Entries must not necessarily be only observations but may also be models.
    Entries provided in this collection refer to the y-axis in the AeroVal
    heatmap display and must fulfill the protocol defined by :class:`ObsEntry`.

    """

    def add_entry(self, key: str, entry: dict | ObsEntry):
        if isinstance(entry, dict):
            entry = ObsEntry(**entry)
        self._entries[key] = entry
        self._entries[key].obs_name = self.get_web_interface_name(key)

    def remove_entry(self, key: str):
        if key in self._entries:
            del self._entries[key]

    def get_entry(self, key: str) -> ObsEntry:
        """
        Getter for obs entries

        Raises
        ------
        KeyError
            if input name is not in this collection
        """
        try:
            entry = self._entries[key]
            return entry
        except (KeyError, AttributeError):
            raise EntryNotAvailable(f"no such entry {key}")

    def get_all_vars(self) -> list[str]:
        """
        Get unique list of all obs variables from all entries

        Returns
        -------
        list
            list of variables specified in obs collection

        """
        vars = []
        for ocfg in self._entries.values():
            vars.extend(ocfg.get_all_vars())
        return sorted(list(set(vars)))

    def get_web_interface_name(self, key: str) -> str:
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
        entry = self._entries.get(key)
        return (
            entry.web_interface_name
            if entry is not None and entry.web_interface_name is not None
            else key
        )

    @property
    def web_interface_names(self) -> list:
        """
        List of web interface names for each obs entry

        Returns
        -------
        list
        """
        return [self.get_web_interface_name(key) for key in self.keylist()]

    @property
    def all_vert_types(self):
        """List of unique vertical types specified in this collection"""
        return list({x.obs_vert_type for x in self._entries.values()})


class ModelCollection(BaseCollection):
    """
    Object that represents a collection of model entries

    "Keys" are model names, values are instances of :class:`ModelEntry`. Values
    can also be assigned as dict and will automatically be converted into
    instances of :class:`ModelEntry`.

    Note
    ----
    Entries must not necessarily be only models but may also be observations.
    Entries provided in this collection refer to the x-axis in the AeroVal
    heatmap display and must fulfill the protocol defined by
    :class:`ModelEntry`.
    """

    def add_entry(self, key: str, entry: dict | ModelEntry):
        if isinstance(entry, dict):
            entry = ModelEntry(**entry)
        entry.model_name = key
        self._entries[key] = entry

    def remove_entry(self, key: str):
        if key in self._entries:
            del self._entries[key]

    def get_entry(self, key: str) -> ModelEntry:
        """
        Get model entry configuration
        Parameters
        ----------
        model_name : str
            name of model

        Returns
        -------
        dict
            Dictionary that specifies the model setup ready for the analysis
        """
        if key in self._entries:
            return self._entries[key]
        else:
            raise EntryNotAvailable(f"no such entry {key}")

    def keylist(self, name_or_pattern: str = None) -> list[str]:
        """Find model / obs names that match input search pattern(s)

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
        # Special case where the model cfg is empty, used for obs-only
        if list(self._entries.keys()) == []:
            return []

        else:
            return super().keylist(name_or_pattern)
