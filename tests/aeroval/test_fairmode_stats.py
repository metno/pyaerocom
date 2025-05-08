from __future__ import annotations

import numpy as np
import pytest

from pyaerocom.aeroval.fairmode_stats import fairmode_stats

FAIRMODE_KEYS = {"RMSU", "sign", "crms", "bias", "rms", "alpha", "UrRV", "RV", "beta_mqi", "freq"}


@pytest.mark.parametrize(
    "obs_var,stats,freq",
    [
        pytest.param(
            "concno2",
            dict(refdata_mean=0, refdata_std=1, data_std=1, R=1, mb=0, rms=0),
            "hourly",
            id="dummy_no2",
        ),
        pytest.param(
            "conco3mda8",
            dict(refdata_mean=0, refdata_std=1, data_std=1, R=1, mb=0, rms=0),
            "daily",
            id="dummy_o3mda8",
        ),
    ],
)
def test_fairmode_stats(obs_var: str, stats: dict, freq: str):
    fairmode = fairmode_stats(obs_var, stats, freq)
    assert set(fairmode) == FAIRMODE_KEYS


@pytest.mark.parametrize(
    "obs_var,stats,freq",
    [
        pytest.param(
            "conco3",
            dict(refdata_mean=0, refdata_std=1, data_std=1, R=1, mb=0, rms=0),
            "daily",
            id="not a valid species",
        ),
        pytest.param(
            "concno2",
            dict(refdata_mean=0, refdata_std=1, data_std=1, R=1, mb=0, rms=0),
            "daily",
            id="wrong frequency no2",
        ),
        pytest.param(
            "concpm10",
            dict(refdata_mean=0, refdata_std=1, data_std=1, R=1, mb=0, rms=0),
            "hourly",
            id="wrong frequency pm10",
        ),
        pytest.param(
            "concpm10",
            dict(refdata_mean=np.nan, refdata_std=1, data_std=1, R=1, mb=0, rms=0),
            "daily",
            id="NaN mean",
        ),
        pytest.param(
            "concpm10",
            dict(refdata_mean=0, refdata_std=np.nan, data_std=1, R=1, mb=0, rms=0),
            "daily",
            id="NaN obs_std",
        ),
        pytest.param(
            "concpm10",
            dict(refdata_mean=0, refdata_std=1, data_std=np.nan, R=1, mb=0, rms=0),
            "daily",
            id="NaN mod_std",
        ),
        pytest.param(
            "concpm10",
            dict(refdata_mean=0, refdata_std=1, data_std=1, R=np.nan, mb=0, rms=0),
            "daily",
            id="NaN R",
        ),
        pytest.param(
            "concpm10",
            dict(refdata_mean=0, refdata_std=1, data_std=1, R=1, mb=np.nan, rms=0),
            "daily",
            id="NaN bias",
        ),
        pytest.param(
            "concpm10",
            dict(refdata_mean=0, refdata_std=1, data_std=1, R=1, mb=1, rms=np.nan),
            "daily",
            id="NaN rms",
        ),
    ],
)
def test_empty_stats(obs_var: str, stats: dict, freq: str):
    fairmode = fairmode_stats(obs_var, stats, freq)
    assert not fairmode


@pytest.mark.parametrize(
    "obs_var,stats,freq,error",
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
            "daily",
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
            "daily",
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
            "daily",
            "out of range R=10",
            id="R",
        ),
    ],
)
def test_fairmode_error(obs_var: str, stats: dict, freq: str, error: str):
    with pytest.raises(AssertionError) as e:
        fairmode_stats(obs_var, stats, freq)
    assert str(e.value) == error
