from __future__ import annotations

import numpy as np
import pytest

from pyaerocom.aeroval.fairmode_stats import fairmode_stats

FAIRMODE_KEYS = {"RMSU", "sign", "crms", "bias", "rms", "alpha", "UrRV", "RV", "beta_mqi"}


@pytest.mark.parametrize(
    "obs_var,stats",
    [
        pytest.param(
            "concno2",
            dict(refdata_mean=0, refdata_std=1, data_std=1, R=1, mb=0, rms=0),
            id="dummy vars",
        )
    ],
)
def test_fairmode_stats(obs_var: str, stats: dict):
    fairmode = fairmode_stats(obs_var, stats)
    assert set(fairmode) == FAIRMODE_KEYS


@pytest.mark.parametrize(
    "obs_var,stats",
    [
        pytest.param(
            "not_a_species",
            dict(refdata_mean=0, refdata_std=1, data_std=1, R=1, mb=0, rms=0),
            id="unknown obs variable",
        ),
        pytest.param(
            "vmro3",
            dict(refdata_mean=np.nan, refdata_std=1, data_std=1, R=1, mb=0, rms=0),
            id="NaN mean",
        ),
        pytest.param(
            "conco3",
            dict(refdata_mean=0, refdata_std=np.nan, data_std=1, R=1, mb=0, rms=0),
            id="NaN obs_std",
        ),
        pytest.param(
            "conco3",
            dict(refdata_mean=0, refdata_std=1, data_std=np.nan, R=1, mb=0, rms=0),
            id="NaN mod_std",
        ),
        pytest.param(
            "conco3",
            dict(refdata_mean=0, refdata_std=1, data_std=1, R=np.nan, mb=0, rms=0),
            id="NaN R",
        ),
        pytest.param(
            "conco3",
            dict(refdata_mean=0, refdata_std=1, data_std=1, R=1, mb=np.nan, rms=0),
            id="NaN bias",
        ),
        pytest.param(
            "vmro3",
            dict(refdata_mean=0, refdata_std=1, data_std=1, R=1, mb=1, rms=np.nan),
            id="NaN rms",
        ),
    ],
)
def test_empty_stats(obs_var: str, stats: dict):
    fairmode = fairmode_stats(obs_var, stats)
    assert not fairmode


@pytest.mark.parametrize(
    "obs_var,stats,error",
    [
        pytest.param(
            "concpm10",
            {
                "refdata_mean": 0,
                "refdata_std": -1,  # Negative std
                "data_std": 1,
                "R": 1,
                "mb": 1,
                "rms": 1,
            },
            "negative obs_std=-1",
            id="obs_std",
        ),
        pytest.param(
            "concpm10",
            {
                "refdata_mean": 0,
                "refdata_std": 1,
                "data_std": -1,  # Negative std
                "R": 1,
                "mb": 1,
                "rms": 1,
            },
            "negative mod_std=-1",
            id="mod_std",
        ),
        pytest.param(
            "concpm25",
            {
                "refdata_mean": 0,
                "refdata_std": 1,
                "data_std": 1,
                "R": 10,  # Correlation must be in [-1, 1]
                "mb": 1,
                "rms": 1,
            },
            "out of range R=10",
            id="R",
        ),
    ],
)
def test_fairmode_error(obs_var: str, stats: dict, error: str):
    with pytest.raises(AssertionError) as e:
        fairmode_stats(obs_var, stats)
    assert str(e.value) == error
