from __future__ import annotations

import warnings
from contextlib import contextmanager
from typing import Type


@contextmanager
def ignore_warnings(
    apply: bool, category: Type[Warning] = Warning, *, messages: list[str] | str | None = None
):
    """
    Ignore particular warnings with a decorator or context manager

    Parameters
    ----------
    apply : bool
        if True warnings will be ignored, else not.
    category : subclass of Warning (default: Warning)
        warning category to be ignored. E.g. UserWarning, DeprecationWarning.
        The default is Warning.
    messages : list[str], str, optional
        list of warning messages to be ignored. E.g.
        ['Warning that can safely be ignored']. The default is None. For each
        `<entry>` :func:`warnigns.filterwarnings('ignore', category, message=<entry>)`
        is called.

    Example
    -------
    @ignore_warnings(True, UserWarning)
    @ignore_warnings(True, DeprecationWarning)
    @ignore_warnings(True, messages=['I REALLY'])
    def warn_randomly_and_add_numbers(num1, num2):
        warnings.warn(UserWarning('Harmless user warning'))
        warnings.warn(DeprecationWarning('This function is deprecated'))
        warnings.warn(Warning('I REALLY NEED TO REACH YOU'))
        return num1+num2

    """
    if not issubclass(category, Warning):
        raise ValueError("category must be a Warning subclass")

    if not messages:
        messages = [""]
    elif type(messages) == str:
        messages = [messages]

    if not isinstance(messages, list):
        raise ValueError("messages must be list or None")
    elif not all(type(msg) == str for msg in messages):
        raise ValueError("messages must be list of strings")

    try:
        if not apply:
            yield
            return
        with warnings.catch_warnings():
            for msg in messages:
                warnings.filterwarnings("ignore", category=category, message=msg)
            yield
    finally:
        pass
