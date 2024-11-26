import json
from pathlib import Path

import numpy as np
import pytest

from pyaerocom.aeroval.json_utils import (
    read_json,
    round_floats,
    set_float_serialization_precision,
    write_json,
)


@pytest.fixture()
def json_path(tmp_path: Path) -> Path:
    path = tmp_path / "file.json"
    assert not path.exists()
    return path


@pytest.mark.parametrize(
    "raw,precision,rounded",
    [
        pytest.param(
            1.12344567890,
            5,
            1.12345,
            id="single float",
        ),
        pytest.param(
            [np.float64(2.3456789), np.float32(3.456789012)],
            3,
            [2.346, pytest.approx(3.457, 1e-3)],
            id="np.float list",
        ),
        pytest.param(
            (np.float128(4.567890123), np.float64(5.6789012345)),
            5,
            [pytest.approx(4.56789, 1e-5), 5.67890],
            id="np.float tuple",
        ),
        pytest.param(
            dict(bla=np.float128(0.1234455667), blubb=1, ha="test"),
            5,
            dict(bla=pytest.approx(0.12345, 1e-5), blubb=1, ha="test"),
            id="mixed dict",
        ),
    ],
)
def test_round_floats(raw, precision: int, rounded):
    set_float_serialization_precision(precision)
    _rounded = round_floats(raw)
    if isinstance(raw, list | tuple):
        assert type(_rounded) is list
    if isinstance(raw, dict):
        assert type(_rounded) is dict
    assert _rounded == rounded


def test_read_json(json_path: Path):
    data = {"bla": 42}
    json_path.write_text(json.dumps(data))
    assert json_path.exists()
    assert read_json(json_path) == data


@pytest.mark.parametrize("data", [{"bla": 42}, {"bla": 42, "blub": np.nan}])
@pytest.mark.parametrize("kwargs", [dict(), dict(ignore_nan=True, indent=5)])
def test_write_json(json_path: Path, data: dict, kwargs: dict):
    write_json(data, json_path, **kwargs)
    assert json_path.exists()


def test_write_json_error(json_path: Path):
    with pytest.raises(TypeError) as e:
        write_json({"bla": 42}, json_path, bla=42)
    assert str(e.value).endswith("unexpected keyword argument 'bla'")
