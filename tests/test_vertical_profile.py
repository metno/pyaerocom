from __future__ import annotations

from typing import Type

import pytest

import pyaerocom.vertical_profile as mod


def test_VerticalProfile():
    mod.VerticalProfile(
        data=[1],
        altitude=[1],
        dtime=[1],
        var_name="bla",
        data_err=[1],
        var_unit="1",
        altitude_unit="1",
    )


@pytest.mark.parametrize(
    "kwargs,exception,error",
    [
        pytest.param(
            dict(),
            TypeError,
            "__init__() missing 7 required positional arguments: 'data', 'altitude', 'dtime', 'var_name', 'data_err', 'var_unit', and 'altitude_unit'",
            id="no args",
        ),
        pytest.param(
            dict(
                data=[1, 2],
                altitude=[1],
                dtime=[1],
                var_name="bla",
                data_err=[1],
                var_unit="1",
                altitude_unit="1",
            ),
            AssertionError,
            "",
            id="wrong data",
        ),
    ],
)
def test_VerticalProfile_error(kwargs: dict, exception: Type[Exception], error: str):
    with pytest.raises(exception) as e:
        mod.VerticalProfile(**kwargs)
    assert str(e.value) == error


@pytest.mark.parametrize(
    "args",
    [
        dict(),
        dict(plot_errs=False),
        dict(whole_alt_range=True),
        dict(errs_shaded=False),
        dict(add_vertbar_zero=False),
    ],
)
def test_VerticalProfile_plot(args):
    vp = mod.VerticalProfile(
        data=[1, 4, 3, 2, 1],
        altitude=[1, 2, 3, 4, 5],
        dtime=[1],
        var_name="bla",
        data_err=[1, 1, 1, 1, 1],
        var_unit="ug m-3",
        altitude_unit="m",
    )
    vp.plot(**args)
