import warnings

import pytest

from pyaerocom._warnings_management import filter_warnings


@pytest.mark.filterwarnings("error")
def test_filter_warnings_decorator():
    @filter_warnings(True, [UserWarning], messages=["Deprecated"])
    def add_num_with_warnings(num1, num2):
        warnings.warn(UserWarning("User Warning"))
        warnings.warn(DeprecationWarning("Deprecated"))
        warnings.warn(Warning("General warning"))
        return num1 + num2

    with pytest.warns(Warning, match="General warning"):
        add_num_with_warnings(1, 2)


@pytest.mark.filterwarnings("error")
def test_filter_warnings_category():
    """filter one warning based on the type of warning"""

    # ignore warning
    with filter_warnings(True, [RuntimeWarning]):
        warnings.warn(RuntimeWarning("somethng unexpected..."))

    with filter_warnings(True, [RuntimeWarning, UserWarning, DeprecationWarning]):
        warnings.warn(RuntimeWarning("somethng unexpected?."))
        warnings.warn(UserWarning("somethng unusual?"))
        warnings.warn(DeprecationWarning("somethng deprecated?"))

    # raise warning
    with pytest.warns(RuntimeWarning):
        with filter_warnings(False, [RuntimeWarning]):
            warnings.warn(RuntimeWarning("somethng unexpected..."))


@pytest.mark.filterwarnings("error")
def test_filter_warnings_message():
    """filter one warning based on the warning message"""

    # ignore warning
    with filter_warnings(True, messages=["Deprecated"]):
        warnings.warn(Warning("Deprecated"))

    with filter_warnings(True, messages=["A", "B", "C"]):
        warnings.warn(Warning("A"))
        warnings.warn(Warning("B"))
        warnings.warn(Warning("C"))

    # raise warning
    with pytest.warns(Warning, match="Deprecated"):
        with filter_warnings(False, messages=["Deprecated"]):
            warnings.warn(Warning("Deprecated"))
