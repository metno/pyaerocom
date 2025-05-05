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
        `<entry>` :func:`warnings.filterwarnings('ignore', Warning, message=<entry>)`
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
    elif all(isinstance(msg, str) for msg in messages):
        message = "|".join(messages)
    else:
        raise ValueError("messages must be list of strings")

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=category, message=message)
        yield


def ignore_basemap_warning():  # pragma: no cover
    warnings.filterwarnings("ignore", r".*install Basemap$", UserWarning, "geonum", append=True)


def ignore_earth_radius_warning():  # pragma: no cover
    warnings.filterwarnings(
        "ignore", "Using DEFAULT_SPHERICAL_EARTH_RADIUS", UserWarning, "iris.*", append=True
    )
