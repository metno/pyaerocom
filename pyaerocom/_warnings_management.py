#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 18 11:27:52 2021

@author: jonasg
"""
import warnings
def filter_warnings(apply, categories=None, messages=None):
    """
    Decorator that can be used to filter particular warnings

    Parameters
    ----------
    apply : bool
        if True warnings will be filtered, else not.
    categories : list, optional
        list of warning categories to be filtered. E.g.
        [UserWarning, DeprecationWarning]. The default is None. For each
        `<entry>` :func:`warnigns.filterwarnings('ignore', category=<entry>)`
        is called.
    messages : list, optional
        list of warning messages to be filtered. E.g.
        ['Warning that can safely be ignored']. The default is None. For each
        `<entry>` :func:`warnigns.filterwarnings('ignore', message=<entry>)`
        is called.

    Example
    -------
    @filter_warnings(categories=[UserWarning, DeprecationWarning],
                     messages=['I REALLY'])
    def warn_randomly_and_add_numbers(num1, num2):
        warnings.warn(UserWarning('Harmless user warning'))
        warnings.warn(DeprecationWarning('This function is deprecated'))
        warnings.warn(Warning('I REALLY NEED TO REACH YOU'))
        return num1+num2

    """
    if categories is None:
        categories = []
    elif not isinstance(categories, list):
        raise ValueError('categories must be list or None')
    if messages is None:
        messages = []
    elif not isinstance(messages, list):
        raise ValueError('messages must be list or None')
    def decorator(func):
        def wrapper(*args, **kwargs):
            with warnings.catch_warnings():
                if apply:
                    for cat in categories:
                        warnings.filterwarnings('ignore', category=cat)
                    for msg in messages:
                        warnings.filterwarnings('ignore', message=msg)
                return func(*args, **kwargs)
        return wrapper
    return decorator

if __name__ == '__main__':

    @filter_warnings(True,[UserWarning], messages=['Deprecated'])
    def add_num_with_warnings(num1, num2):
        warnings.warn(UserWarning('User Warning'))
        warnings.warn(DeprecationWarning('Deprecated'))
        warnings.warn(Warning('General warning'))
        return num1 + num2

    print(add_num_with_warnings(1, 2))