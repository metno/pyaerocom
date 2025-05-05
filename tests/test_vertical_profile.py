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
    "kwargs,exception",
    [
        pytest.param(
            dict(),
            TypeError,
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
            ValueError,
            id="wrong data",
        ),
    ],
)
def test_VerticalProfile_error(kwargs: dict, exception: type[Exception]):
    with pytest.raises(exception):
        VerticalProfile(**kwargs)
