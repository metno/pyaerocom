from pydantic import ValidationError
import pytest
from pyaerocom.aeroval.glob_defaults import VarWebInfo, VarWebScaleAndColormap


def test_var_web_info():
    var_web_info = VarWebInfo()
    unique_entries = list(set(var_web_info))
    assert len(unique_entries) == len(var_web_info.keys())


def test_var_web_scale_and_colormap():
    vwsc = VarWebScaleAndColormap()
    assert "concso2" in vwsc
    assert "new_var" not in vwsc

    with pytest.raises(FileNotFoundError) as ex:
        VarWebScaleAndColormap("no_such_file")
    assert "no_such_file" in str(ex.value)

    with pytest.raises(ValidationError):
        VarWebScaleAndColormap(**{"bla": ["blub"]})

    vwsc2 = VarWebScaleAndColormap(
        config_file="", **{"new_var": {"scale": [1, 2, 4], "colmap": "my_colormap"}}
    )
    assert "new_var" in vwsc2

    vwsc3 = VarWebScaleAndColormap(new_var2={"scale": [1, 2, 4], "colmap": "my_colormap"})
    assert "new_var2" in vwsc3
