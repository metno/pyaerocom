import warnings

import pytest

from pyaerocom._warnings_management import filter_warnings

@pytest.mark.filterwarnings("error")
def test_filter_warnings():
    @filter_warnings(True, [UserWarning], messages=["Deprecated"])
    def add_num_with_warnings(num1, num2):
        warnings.warn(UserWarning("User Warning"))
        warnings.warn(DeprecationWarning("Deprecated"))
        warnings.warn(Warning("General warning"))
        return num1 + num2

    with pytest.warns(Warning, match="General warning"):
        add_num_with_warnings(1, 2)
