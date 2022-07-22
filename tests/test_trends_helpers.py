import pytest
import numpy as np
import pandas as pd

from pyaerocom.trends_helpers import _init_trends_result_dict,  _get_season_from_months

def test__init_trends_result_dict():
    result = _init_trends_result_dict(2022)
    assert isinstance(result, dict)
    assert len(result.keys()) == 14

def test__get_season_from_months_wrong():
    not_a_season = "cat"
    with pytest.raises(ValueError) as e:
        result = _get_season_from_months(not_a_season)
    assert e.type is ValueError