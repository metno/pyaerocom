import pytest
from pyaerocom.aeroval.compute_fairmode_stats import compute_fairmode_stats


@pytest.mark.parametrize(
    "obs_var,stats,n_stats",
    [
        (
            "concno2",
            {
                "refdata_mean": 0,
                "refdata_std": 1,
                "data_std": 1,
                "R": 1,
                "mb": 0,
                "rms": 0,
            },  # dummy values
            9,  # "RMSE", "sign", "crms", "bias", "rms", "alpha", "UrRV", "RV", "beta_mqi"
        ),
        (
            "not_a_species",
            {"refdata_mean": 0, "refdata_std": 1, "data_std": 1, "R": 1, "mb": 0, "rms": 0},
            0,  # if observed variable is not a species then check return an empty dict
        ),
    ],
)
def test_fairmode_stats(obs_var: str, stats: dict, n_stats: int, beta: float = 1):
    # Create a list with all the statistics returned by fairmode_stats(). If adding statistics there, will need to add here.
    valid_stats = ["RMSU", "sign", "crms", "bias", "rms", "alpha", "UrRV", "RV", "beta_mqi"]
    fairmode_stats_for_testing = compute_fairmode_stats(obs_var, stats)
    # Check that the length of the returned dict has length all the fairmode stats keys if obs_var is a legitmate species, or returns an empty dict
    assert len(fairmode_stats_for_testing) == n_stats
    # If expected number of statistics is the same as the valid_stats
    if n_stats == len(valid_stats):
        # Check that all keys in dict returned by fairmode_stats() are in valid_stats.
        assert all(key in fairmode_stats_for_testing for key in valid_stats)
