#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Small helper utility functions for pyaerocom
"""
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor

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

    return ('Invalid input for {} ({}), choose from {}'
            .format(argname, argval, argopts))

def check_dir_access(path, timeout=0.1):
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
    pool = ThreadPoolExecutor()
    def try_ls(testdir, timeout):
        future = pool.submit(os.listdir, testdir)
        try:
            future.result(timeout)
            return True
        except Exception:
            return False
    return try_ls(path, timeout)

def check_write_access(path, timeout=0.1):
    """Check if input location provides write access

    Parameters
    ----------
    path : str
        directory to be tested
    timeout : float
        timeout in seconds (to avoid blockage at non-existing locations)

    """
    if not isinstance(path, str):
        # not a path
        return False

    pool = ThreadPoolExecutor()

    def _test_write_access(path):
        test = os.path.join(path, '_tmp')
        try:
            os.mkdir(test)
            os.rmdir(test)
            return True
        except Exception:
            return False

    def run_timeout(path, timeout):
        future = pool.submit(_test_write_access, path)
        try:
            return future.result(timeout)
        except Exception:
            return False
    return run_timeout(path, timeout)

def _class_name(obj):
    """Returns class name of an object"""
    return type(obj).__name__

from collections.abc import MutableMapping
class BrowseDict(MutableMapping):
    """Dictionary-like object with getattr and setattr options

    Extended dictionary that supports dynamic value generation (i.e. if an
    assigned value is callable, it will be executed on demand).
    """
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    # The next five methods are requirements of the ABC.
    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError as e:
            raise KeyError(e)

    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        '''echoes class, id, & reproducible representation in the REPL'''
        _repr = repr(self.__dict__)
        return f'{_class_name(self)}: {_repr}'

    def to_dict(self):
        return dict(self)

    def pretty_str(self):
        return dict_to_str(self.to_dict())

    def __str__(self):
        s = ''
        for k, v in self.items():
            s += '\n{}: {}'.format(k, v)
        return s

class ConstrainedContainer(BrowseDict):
    """Restrictive dict-like class with fixed keys

    This class enables to create dict-like objects that have a fixed set of
    keys and value types (once assigned). Optional values may be instantiated
    as None, in which case the first time instantiation definecs its type.

    Note
    ----
    The limitations for assignments are only restricted to setitem operations
    and attr assignment via "." works like in every other class.

    Example
    -------
    class MyContainer(ConstrainedContainer):
        def __init__(self):
            self.val1 = 1
            self.val2 = 2
            self.option = None

    >>> mc = MyContainer()
    >>> mc['option'] = 42
    """
    #: key / value pairs of constrained settings: keys are keys of this dict
    #: and values are lists of allowed values for that key
    CONSTRAINT_VALS = {}

    #: use private keys to
    PRIVATE_KEYS = []
    def __setitem__(self, key, val):
        self._check_valid(key, val)
        setattr(self, key, val)

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
            if isinstance(val, ConstrainedContainer):
                val = val.json_repr()
            output[key] = val
        return output

    def _check_valid(self, key, val):
        """make sure no new attr is added

        Note
        ----
        Only used in __setitem__ not in __setattr__.
        """
        current = getattr(self, key)
        current_tp = type(current)
        if not key in self:
            raise ValueError(f'Invalid key {key}')
        elif not current is None and not isinstance(val, current_tp):
            raise ValueError(
                f'Invalid type {type(val)} for key: {key}. Need {current_tp} '
                f'(Current value: {current})')
        elif key in self.CONSTRAINT_VALS:
            self._assert_constraint(key, val)

    def _assert_constraint(self, key, val):
        if not val in self.CONSTRAINT_VALS[key]:
            raise ValueError(key, val)

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
    #make a copy of the first dictionary
    new = dict(**dict1)
    merge_failed = []
    # loop over all entries of second one
    for key, val in dict2.items():
        try:
            # entry does not exist in first dict or is None
            if not key in new or new[key] is None:
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
            except:
                try:
                    if (this==val).all():
                        continue
                except:
                    pass

            # both values are strings, merge with ';' delim
            if isinstance(this, str) and isinstance(val, str):
                new[key] = '{};{}'.format(this, val)

            elif isinstance(this, list) and isinstance(val, list):
                for item in val:
                    if not item in this:
                        this.append(item)
                new[key] = this

            elif all(isinstance(x, dict) for x in (this, val)):
                new[key] = merge_dicts(this, val)

            elif any(isinstance(x, list) for x in (this, val)):
                if isinstance(this, list):
                    lst = this
                    check = val #this is not list
                else:
                    lst = val
                    check = this #this is not list
                for item in lst:
                    if not type(item) == type(check):
                        raise ValueError('Cannot merge key {} since items in {} '
                                         'are of different type, that does not '
                                         'match {}'.format(key, lst, check))
                lst.append(check)
                new[key] = lst

            else:
                new[key] = [this, val]
        except Exception:
            if discard_failing:
                merge_failed.append(key)
            else:
                raise
    new['merge_failed'] = merge_failed

    return new

def chk_make_subdir(base, name):
    """Check if sub-directory exists in parent directory"""
    d = os.path.join(base, name)
    if not os.path.exists(d):
        os.mkdir(d)
    return d

def check_dirs_exist(*dirs, **add_dirs):
    for d in dirs:
        if not os.path.exists(d):
            print('Creating dir: {}'.format(d))
            os.mkdir(d)
    for k, d in add_dirs.items():
        if not os.path.exists(d):
            os.mkdir(d)
            print('Creating dir: {} ({})'.format(d, k))

def list_to_shortstr(lst, indent=0, name=None):
    """Custom function to convert a list into a short string representation"""
    def _short_lst_fmt(lin):
        lout = []
        for val in lin:
            try:
                ndigits = -1*np.floor(np.log10(abs(np.asarray(val)))).astype(int) + 2
                lout.append('{:.{}f}'.format(val, ndigits))
            except Exception:
                lout.append(val)
        return lout
    if name is None:
        name_str = '{} ({} items): '.format(type(lst).__name__, len(lst))
    else:
        name_str = '{} ({}, {} items): '.format(name, type(lst).__name__, len(lst))
    indentstr = indent*" "
    if len(lst) == 0:
        return "\n{}{}[]".format(indentstr, name_str)
    elif len(lst) < 6:
        lfmt = _short_lst_fmt(lst)
        return "\n{}{}{}".format(indentstr, name_str, lfmt)
    else: #first 2 and last 2 items
        lfmt= _short_lst_fmt([lst[0], lst[1], lst[-2], lst[-1]])
        s = ("\n{}{}[{}, {}, ..., {}, {}]"
             .format(indentstr, name_str, lfmt[0], lfmt[1], lfmt[2], lfmt[3]))

    return s

def sort_dict_by_name(d, pref_list=None):
    """Sort entries of input dictionary by their names and return ordered

    Parameters
    ----------
    d : dict
        input dictionary

    Returns
    -------
    OrderedDict
        sorted and ordered dictionary
    """
    from collections import OrderedDict as od
    if pref_list is None:
        pref_list = []
    s = od()
    sorted_keys = sorted(d)
    for k in pref_list:
        if k in d:
            s[k] = d[k]
    for k in sorted_keys:
        if not k in pref_list:
            s[k] = d[k]
    return s

def dict_to_str(dictionary, s=None, indent=0, ignore_null=False):
    """Custom function to convert dictionary into string (e.g. for print)

    Parameters
    ----------
    dictionary : dict
        the dictionary
    s : str
        the input string
    indent : int
        indent of dictionary content
    ignore_null : bool
        if True, None entries in dictionary are ignored

    Returns
    -------
    str
        the modified input string

    Example
    -------

    >>> string = "Printing dictionary d"
    >>> d = dict(Bla=1, Blub=dict(BlaBlub=2))
    >>> print(dict_to_str(d, string))
    Printing dictionary d
       Bla: 1
       Blub (dict)
        BlaBlub: 2

    """
    if s is None:
        s = ''
    for k, v in dictionary.items():
        if ignore_null and v is None:
            continue
        elif isinstance(v, dict):
            s += "\n{}{} ({}):".format(indent*' ', k, type(v).__name__)
            s = dict_to_str(v, s, indent+2)
        elif isinstance(v, list):
            s += list_to_shortstr(v, indent=indent, name=k)
        elif isinstance(v, np.ndarray) and v.ndim==1:
            s += list_to_shortstr(v, indent=indent, name=k)
        else:
            s += "\n{}{}: {}".format(indent*" ", k, v)
    return s

def str_underline(s, indent=0):
    """Create underlined string"""
    s = indent*" " + "{}\n".format(s)
    s+= indent*" " + "{}".format(len(s)*"-")
    return s

if __name__ == '__main__':
    d = BrowseDict(bla=1, blub=42, blablub=dict(bla=42, blub=43))

    d.update(**{'mypy': 55})
    class CDict(ConstrainedContainer):
        def __init__(self):
            self.bla = 1
            self.blub = 2
            self.option = None

    cd = CDict()
    print(cd)
    cd['option'] = 42
    cd['option'] = {}

    cd.update(**{'mypy': 55})