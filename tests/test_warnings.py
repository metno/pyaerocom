import warnings

import pytest

from pyaerocom._warnings_management import ignore_warnings


@pytest.mark.filterwarnings("error")
def test_filter_warnings_decorator():
    @ignore_warnings(True, UserWarning, "User Warning")
    @ignore_warnings(True, DeprecationWarning, "Deprecated")
    def add_num_with_warnings(num1, num2):
        warnings.warn(UserWarning("User Warning"))
        warnings.warn(DeprecationWarning("Deprecated"))
        warnings.warn(UserWarning("General warning"))
        return num1 + num2

    with pytest.warns(UserWarning, match="General warning"):
        add_num_with_warnings(1, 2)


@pytest.mark.filterwarnings("error")
def test_filter_warnings_category():
    """filter one warning based on the type of warning"""

    # ignore warning
    with ignore_warnings(True, RuntimeWarning):
        warnings.warn(RuntimeWarning("somethng unexpected..."))


    # raise warning
    with pytest.warns(RuntimeWarning):
        with ignore_warnings(False, RuntimeWarning):
            warnings.warn(RuntimeWarning("somethng unexpected..."))


@pytest.mark.filterwarnings("error")
def test_filter_warnings_message():
    """filter one warning based on the warning message"""

    # ignore warning
    with ignore_warnings(True, Warning, "Deprecated"):
        warnings.warn(Warning("Deprecated"))

    with ignore_warnings(True, Warning, "A", "B", "C"):
        warnings.warn(Warning("A"))
        warnings.warn(Warning("B"))
        warnings.warn(Warning("C"))

    # raise warning
    with pytest.warns(Warning, match="Deprecated"):
        with ignore_warnings(False, Warning, "Deprecated"):
            warnings.warn(Warning("Deprecated"))
