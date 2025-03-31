import warnings

import pytest

from pyaerocom._warnings import ignore_warnings


@pytest.mark.filterwarnings("error")
def test_filter_warnings_decorator():
    @ignore_warnings(UserWarning, "User Warning")
    @ignore_warnings(DeprecationWarning, "Deprecated")
    def add_num_with_warnings(num1, num2):
        warnings.warn("User Warning", UserWarning)
        warnings.warn("Deprecated", DeprecationWarning)
        warnings.warn("General warning", UserWarning)
        return num1 + num2

    with pytest.warns(UserWarning, match="General warning"):
        add_num_with_warnings(1, 2)


@pytest.mark.filterwarnings("error")
def test_filter_warnings_category():
    """filter one warning based on the type of warning"""

    with ignore_warnings(RuntimeWarning):
        warnings.warn(RuntimeWarning("something unexpected..."))


@pytest.mark.filterwarnings("error")
def test_filter_warnings_message():
    """filter one warning based on the warning message"""

    with ignore_warnings(Warning, "Deprecated"):
        warnings.warn(Warning("Deprecated"))

    with ignore_warnings(Warning, "A", "B", "C"):
        warnings.warn(Warning("A"))
        warnings.warn(Warning("B"))
        warnings.warn(Warning("C"))
