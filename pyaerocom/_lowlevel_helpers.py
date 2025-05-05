"""
Small helper utility functions for pyaerocom
"""

import abc
import logging
import os
from collections.abc import MutableMapping
from pathlib import Path
from typing import TypeVar

import numpy as np
from typing_extensions import TypedDict

from pyaerocom._warnings import ignore_warnings

logger = logging.getLogger(__name__)


def invalid_input_err_str(argname, argval, argopts):
    """Just a small helper to format an input error string for functions

    Parameters
    ----------
    argname : str
        name of input argument
    argval
        (invalid) value of input argument
    argopts
        possible input args for arg

    Returns
    -------
    str
        formatted string that can be parsed to an Exception
    """

    return f"Invalid input for {argname} ({argval}), choose from {argopts}"


def check_dir_access(path):
    """Uses multiprocessing approach to check if location can be accessed

    Parameters
    ----------
    loc : str
        path that is supposed to be checked

    Returns
    -------
    bool
        True, if location is accessible, else False
    """
    if not isinstance(path, str):
        return False

    return os.access(path, os.R_OK)


def check_write_access(path):
    """Check if input location provides write access

    Parameters
    ----------
    path : str
        directory to be tested

    """
    if not isinstance(path, str):
        # not a path
        return False

    return os.access(path, os.W_OK)


def _class_name(obj):
    """Returns class name of an object"""
    return type(obj).__name__


# TODO: Check to see if instances of these classes can instead use pydantic
class Validator(abc.ABC):
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, obj, objtype=None):
        try:
            return obj.__dict__[self._name]
        except (AttributeError, KeyError):
            raise AttributeError("value not set...")

    def __set__(self, obj, val):
        val = self.validate(val)
        obj.__dict__[self._name] = val

    @abc.abstractmethod
    def validate(self, val):
        pass


class TypeValidator(Validator):
    def __init__(self, type):
        self._type = type

    def validate(self, val):
        if not isinstance(val, self._type):
            raise ValueError(f"need instance of {self._type}")
        return val


class StrType(Validator):
    def validate(self, val):
        if not isinstance(val, str):
            raise ValueError(f"need str, got {val}")
        return val


class Loc(abc.ABC):
    """Abstract descriptor representing a path location

    Descriptor: TODO
    See here: https://docs.python.org/3/howto/descriptor.html#complete-practical-example

    Note
    ----
    - Child classes need to implement :func:`create`
    - value is allowed to be `None` in which case no checks are performed
    """

    def __init__(
        self,
        default=None,
        assert_exists=False,
        auto_create=False,
        tooltip=None,
    ):
        self.assert_exists = assert_exists
        self.auto_create = auto_create
        self.tooltip = "" if tooltip is None else tooltip
        self.__set__(self, default)

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        try:
            val = obj.__dict__[self.name]
        except (KeyError, AttributeError):
            val = self.default
        return val

    def __set__(self, obj, value):
        value = self.validate(value)
        try:
            obj.__dict__[self.name] = value
        except AttributeError:
            self.default = value

    def validate(self, value):
        if value is None:
            return value
        elif isinstance(value, Path):
            value = str(value)
        if not isinstance(value, str):
            raise ValueError(value)
        if self.assert_exists and not os.path.exists(value):
            if self.auto_create:
                self.create(value)
            else:
                raise FileNotFoundError(value)
        return value

    @abc.abstractmethod
    def create(self, value):
        pass


class DirLoc(Loc):
    def create(self, value):
        os.makedirs(value, exist_ok=True)
        logger.info(f"created directory {value}")


class AsciiFileLoc(Loc):
    def create(self, value):
        logger.info(f"create ascii file {value}")
        open(value, "w").close()


class BrowseDict(MutableMapping):
    """Dictionary-like object with getattr and setattr options

    Extended dictionary that supports dynamic value generation (i.e. if an
    assigned value is callable, it will be executed on demand).
    """

    ADD_GLOB = []
    FORBIDDEN_KEYS = []
    #: Keys to be ignored when converting to json
    IGNORE_JSON = []
    MAXLEN_KEYS = 1e2
    SETTER_CONVERT = {}

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    @property
    def _class_name(self):
        return _class_name(self)

    def keys(self):
        return list(self.__dict__) + self.ADD_GLOB

    def _get_glob_vals(self):
        return [getattr(self, x) for x in self.ADD_GLOB]

    def values(self):
        return [getattr(self, x) for x in self.keys()]

    def items(self):
        for key in self.keys():
            yield key, getattr(self, key)

    def __setitem__(self, key, val) -> None:
        key, val, ok = self._setitem_checker(key, val)
        if not ok:
            return
        if bool(self.SETTER_CONVERT):
            for fromtp, totp in self.SETTER_CONVERT.items():
                if isinstance(val, fromtp):
                    if fromtp is dict:
                        val = totp(**val)
                    else:
                        val = totp(val)

        if isinstance(key, str):
            if len(key) > self.MAXLEN_KEYS:
                raise KeyError(f"key {key} exceeds max length of {self.MAXLEN_KEYS}")
            if key in self.FORBIDDEN_KEYS:
                raise KeyError(f"invalid key {key}")
        setattr(self, key, val)

    def _setitem_checker(self, key, val):
        return key, val, True

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except TypeError:
            # if key is not str
            return self.__dict__[key]
        except AttributeError as e:
            raise KeyError(e)

    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        """echoes class, id, & reproducible representation in the REPL"""
        _repr = repr(self.__dict__)
        return f"{_class_name(self)}: {_repr}"

    def to_dict(self):
        out = {}
        for key, val in self.items():
            out[key] = val
        return out

    def json_repr(self) -> dict:
        """
        Convert object to serializable json dict

        Returns
        -------
        dict
            content of class

        """
        output = {}
        for key, val in self.items():
            if key in self.IGNORE_JSON:
                continue
            if hasattr(val, "json_repr"):
                val = val.json_repr()
            output[key] = val
        return output

    def import_from(self, other) -> None:
        """
        Import key value pairs from other object

        Other than :func:`update` this method will silently ignore input
        keys that are not contained in this object.

        Parameters
        ----------
        other : dict or BrowseDict
            other dict-like object containing content to be updated.

        Raises
        ------
        ValueError
            If input is invalid type.

        Returns
        -------
        None

        """
        if not isinstance(other, dict | BrowseDict):
            raise ValueError("need dict-like object")
        for key, val in other.items():
            if key in self:
                self[key] = val
            elif key in self.FORBIDDEN_KEYS:
                raise KeyError(f"invalid key {key}")

    def pretty_str(self):
        return dict_to_str(self.to_dict())

    def __str__(self):
        return str(self.to_dict())


class ConstrainedContainer(BrowseDict):
    """Restrictive dict-like class with fixed keys

    This class enables to create dict-like objects that have a fixed set of
    keys and value types (once assigned). Optional values may be instantiated
    as None, in which case the first time instantiation defines its type.

    Note
    ----
    The limitations for assignments are only restricted to setitem operations
    and attr assignment via "." works like in every other class.

    Example
    -------
    >>> class MyContainer(ConstrainedContainer):
    ...    def __init__(self):
    ...        self.val1 = 1
    ...        self.val2 = 2
    ...        self.option = None
    >>> mc = MyContainer()
    >>> mc['option'] = 42
    """

    CRASH_ON_INVALID = True

    def __setitem__(self, key, val):
        super().__setitem__(key, val)

    def _invoke_dtype(self, current_tp, val):
        return current_tp(**val)

    def _check_valtype(self, key, val):
        current_tp = type(self[key])
        if type(val) is not current_tp and isinstance(self[key], BrowseDict):
            val = current_tp(**val)
        return val

    def _setitem_checker(self, key, val):
        """make sure no new attr is added

        Note
        ----
        Only used in __setitem__ not in __setattr__.
        """
        if key not in dir(self):
            if self.CRASH_ON_INVALID:
                raise ValueError(f"Invalid key {key}")
            logger.warning(f"Invalid key {key} in {self._class_name}. Will be ignored.")
            return key, val, False

        current = getattr(self, key)
        val = self._check_valtype(key, val)
        current_tp = type(current)

        if current is not None and not isinstance(val, current_tp):
            raise ValueError(
                f"Invalid type {type(val)} for key: {key}. Need {current_tp} "
                f"(Current value: {current})"
            )
        return key, val, True


class NestedContainer(BrowseDict):
    def _occurs_in(self, key) -> list:
        objs = []
        if key in self:
            objs.append(self)
        for k, v in self.items():
            if isinstance(v, dict | BrowseDict) and key in v:
                objs.append(v)
            if len(objs) > 1:
                print(key, "is contained in multiple containers ", objs)
        return objs

    def keys_unnested(self) -> list:
        keys = []
        for key, val in self.items():
            keys.append(key)
            if isinstance(val, NestedContainer):
                keys.extend(val.keys_unnested())
            elif isinstance(val, ConstrainedContainer | dict):
                for subkey, subval in val.items():
                    keys.append(subkey)
        return keys

    def update(self, **settings):
        for key, val in settings.items():
            to_update = self._occurs_in(key)
            if len(to_update) == 0:
                raise AttributeError(f"invalid key {key}")
            for obj in to_update:
                obj[key] = val

    def __str__(self):
        return dict_to_str(self)


def merge_dicts(dict1, dict2, discard_failing=True):
    """Merge two dictionaries

    Parameters
    ----------
    dict1 : dict
        first dictionary
    dict2 : dict
        second dictionary
    discard_failing : bool
        if True, any key, value pair that cannot be merged from the 2nd into
        the first will be skipped, which means, the value of the output dict
        for that key will be the one of the first input dict. All keys that
        could not be merged can be accessed via key 'merge_failed' in output
        dict. If False, any Exceptions that may occur will be raised.

    Returns
    -------
    dict
        merged dictionary
    """
    # make a copy of the first dictionary
    new = dict(**dict1)
    merge_failed = []
    # loop over all entries of second one
    for key, val in dict2.items():
        try:
            # entry does not exist in first dict or is None
            if key not in new or new[key] is None:
                new[key] = val
                continue
            # get value of first input dict
            this = new[key]

            # check if values are the same and skip (try/except is because for
            # some data types equality tests may return iterable (e.g. compare
            # 2 numpy arrays))
            try:
                if this == val:
                    continue
            except Exception:
                try:
                    if (this == val).all():
                        continue
                except Exception:
                    pass

            # both values are strings, merge with ';' delim
            if isinstance(this, str) and isinstance(val, str):
                new[key] = f"{this};{val}"

            elif isinstance(this, list) and isinstance(val, list):
                for item in val:
                    if item not in this:
                        this.append(item)
                new[key] = this

            elif all(isinstance(x, dict) for x in (this, val)):
                new[key] = merge_dicts(this, val)

            elif any(isinstance(x, list) for x in (this, val)):
                if isinstance(this, list):
                    lst = this
                    check = val  # this is not list
                else:
                    lst = val
                    check = this  # this is not list
                for item in lst:
                    if type(item) is not type(check):
                        raise ValueError(
                            f"Cannot merge key {key} since items in {lst} "
                            f"are of different type, that does not match {check}"
                        )
                lst.append(check)
                new[key] = lst

            else:
                new[key] = [this, val]
        except Exception:
            if discard_failing:
                merge_failed.append(key)
            else:
                raise
    new["merge_failed"] = merge_failed

    return new


def chk_make_subdir(base, name):
    """Check if sub-directory exists in parent directory"""
    d = os.path.join(base, name)
    os.makedirs(d, exist_ok=True)
    return d


def list_to_shortstr(lst, indent=0):
    """Custom function to convert a list into a short string representation"""

    def _short_lst_fmt(lin):
        lout = []
        for val in lin:
            try:
                with ignore_warnings(
                    RuntimeWarning,
                    "divide by zero encountered in log10",
                    "overflow encountered in scalar multiply",
                ):
                    ndigits = -1 * np.floor(np.log10(abs(np.asarray(val)))).astype(int) + 2
                lout.append(f"{val:.{ndigits}f}")
            except Exception:
                lout.append(val)
        return lout

    name_str = f"{type(lst).__name__} ({len(lst)} items): "
    indentstr = indent * " "
    if len(lst) == 0:
        return f"{indentstr}{name_str}[]"
    elif len(lst) < 6:
        lfmt = _short_lst_fmt(lst)
        return f"{indentstr}{name_str}{lfmt}"
    else:  # first 2 and last 2 items
        lfmt = _short_lst_fmt([lst[0], lst[1], lst[-2], lst[-1]])
        s = f"{indentstr}{name_str}[{lfmt[0]}, {lfmt[1]}, ..., {lfmt[2]}, {lfmt[3]}]"

    return s


T = TypeVar("T")


def sort_dict_by_name(d: dict[str, T], pref_list: list[str] | None = None) -> dict[str, T]:
    """Sort entries of input dictionary by their names and return ordered

    Parameters
    ----------
    d : dict
        input dictionary
    pref_list : list, optional
        preferred order of items (may be subset of keys in input dict)

    Returns
    -------
    dict
        sorted and ordered dictionary
    """
    if pref_list is None:
        pref_list = []
    s = {}
    sorted_keys = sorted(d)
    for k in pref_list:
        if k in d:
            s[k] = d[k]
    for k in sorted_keys:
        if k not in pref_list:
            s[k] = d[k]
    return s


def dict_to_str(dictionary, indent=0, ignore_null=False):
    """Custom function to convert dictionary into string (e.g. for print)

    Parameters
    ----------
    dictionary : dict
        the dictionary
    indent : int
        indent of dictionary content
    ignore_null : bool
        if True, None entries in dictionary are ignored

    Returns
    -------
    str
        the modified input string

    """
    if len(dictionary) == 0:
        return "{}"
    elif len(dictionary) == 1:
        pre = ind = offs = ""
    else:
        pre = "\n"
        ind = indent * " "
        offs = " "
    s = "{"

    for key, val in dictionary.items():
        if ignore_null and val is None:
            continue
        elif isinstance(val, dict | BrowseDict):
            val = dict_to_str(val, indent + 2)
        elif isinstance(val, list):
            val = list_to_shortstr(val, indent=indent)
        elif isinstance(val, np.ndarray) and val.ndim == 1:
            val = list_to_shortstr(val, indent=indent)
        s += f"{pre}{ind}{offs}{key}: {val}"
    s += pre + ind + "}"
    return s


def str_underline(title: str, indent: int = 0):
    """Create underlined string"""
    length = indent + len(title)
    underline = "-" * len(title)
    return f"{title:>{length}}\n{underline:>{length}}"


class RegridResDeg(TypedDict):
    """Typed dict for regridding resolution degrees"""

    lat_res_deg: float
    lon_res_deg: float


class LayerLimits(TypedDict):
    """Typed dict of 3D colocation layer limits"""

    start: float
    end: float
