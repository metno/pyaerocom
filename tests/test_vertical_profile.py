from __future__ import annotations

import pytest

from pyaerocom.vertical_profile import VerticalProfile


@pytest.fixture(scope="module")
def vertical_profile() -> VerticalProfile:
    return VerticalProfile(
        data=[1, 4, 3, 2, 1],
        altitude=[1, 2, 3, 4, 5],
        dtime=[1],
        var_name="bla",
        data_err=[1, 1, 1, 1, 1],
        var_unit="ug m-3",
        altitude_unit="m",
    )


@pytest.mark.parametrize(
    "kwargs,exception,error",
    [
        pytest.param(
            dict(),
            TypeError,
            "missing 7 required positional arguments: 'data', 'altitude', 'dtime', 'var_name', 'data_err', 'var_unit', and 'altitude_unit'",
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
def test_VerticalProfile_error(kwargs: dict, exception: type[Exception], error: str):
    with pytest.raises(exception) as e:
        VerticalProfile(**kwargs)
    assert str(e.value).endswith(error)


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(),
        dict(plot_errs=False),
        dict(whole_alt_range=True),
        dict(errs_shaded=False),
        dict(add_vertbar_zero=False),
    ],
)
def test_VerticalProfile_plot(vertical_profile: VerticalProfile, kwargs: dict[str, bool]):
    vertical_profile.plot(**kwargs)
