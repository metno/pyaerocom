import warnings
from contextlib import contextmanager


@contextmanager
def ignore_warnings(category: type[Warning], *messages: str):
    """
    Ignore particular warnings with a decorator or context manager

    Parameters
    ----------
    category : subclass of Warning
        warning category to be ignored. E.g. UserWarning, DeprecationWarning.
        The default is Warning.
    *messages : str, optional
        warning messages to be ignored. E.g.
        ignore_warnings(Warning, 'Warning that can safely be ignored', 'Other warning to ignore').
        For each
        `<entry>` :func:`warnigns.filterwarnings('ignore', Warning, message=<entry>)`
        is called.

    Example
    -------
    @ignore_warnings(UserWarning)
    @ignore_warnings(DeprecationWarning)
    @ignore_warnings(Warning, 'I REALLY')
    def warn_randomly_and_add_numbers(num1, num2):
        warnings.warn(UserWarning('Harmless user warning'))
        warnings.warn(DeprecationWarning('This function is deprecated'))
        warnings.warn(Warning('I REALLY NEED TO REACH YOU'))
        return num1+num2

    """
    if not issubclass(category, Warning):
        raise ValueError("category must be a Warning subclass")

    if not messages:
        message = ""
    elif all(type(msg) == str for msg in messages):
        message = "|".join(messages)
    else:
        raise ValueError("messages must be list of strings")

    try:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=category, message=message)
            yield
    finally:
        pass


def ignore_basemap_warning():  # pragma: no cover
    warnings.filterwarnings("ignore", r".*install Basemap$", UserWarning, "geonum")
