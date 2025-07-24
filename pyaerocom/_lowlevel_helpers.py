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


class AsciiFileLoc(Loc):
    def create(self, value):
        logger.info(f"create ascii file {value}")
        open(value, "w").close()


class BrowseDict(MutableMapping):
    """Dictionary-like object with getattr and setattr options

    Dictionary that supports reading and writing values with . syntax.

    For example:

    d = BrowseDict()

    d.a = 1
    d["b"] = 2

    print(d)
    # BrowseDict: {'a': 1, 'b': 2}
    """

    FORBIDDEN_KEYS = []

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    @property
    def _class_name(self):
        return _class_name(self)

    def keys(self):
        return list(self.__dict__)

    def values(self):
        return [getattr(self, x) for x in self.keys()]

    def items(self):
        for key in self.keys():
            yield key, self[key]

    def __setitem__(self, key, val) -> None:
        if key in self.FORBIDDEN_KEYS:
            raise KeyError(f"invalid key {key}")
        self.__dict__[key] = val

    def __getitem__(self, key):
        return self.__dict__[key]

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
            if hasattr(val, "json_repr"):
                val = val.json_repr()
            output[key] = val
        return output

    def __str__(self):
        return str(self.to_dict())


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
                    "invalid value encountered in cast",
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
