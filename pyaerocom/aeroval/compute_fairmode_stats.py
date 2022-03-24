"""
Functions for computing the FAIRMODE statistics
"""

from math import sqrt, isclose
from typing import Tuple


def _get_RMSU(mean: float, std: float, species: str) -> Tuple[float, float, float, float]:
    species_values = dict(
        concno2=dict(
            UrRV=0.24,
            RV=200,
            alpha=0.2,
        ),
        vmro3=dict(
            UrRV=0.18,
            RV=120,
            alpha=0.79,
        ),
        concpm10=dict(
            UrRV=0.28,
            RV=50,
            alpha=0.13,
        ),
        concpm25=dict(
            UrRV=0.28,
            RV=25,
            alpha=0.3,
        ),
    )

    if species not in species_values.keys():
        raise KeyError(f"Species {species} not in list {species_values.keys()}")

    UrRV = species_values[species]["UrRV"]
    RV = species_values[species]["RV"]
    alpha = species_values[species]["alpha"]

    in_sqrt = (1 - alpha**2) * (mean**2 + std**2) + alpha**2 * RV**2

    return UrRV * sqrt(in_sqrt), UrRV, RV, alpha


def _get_fairmode_sign(mod_std: float, obs_std: float, R: float) -> float:
    if obs_std * sqrt(2 * (1 - R)) == 0:
        return 1
    a = abs(mod_std - obs_std) / (obs_std * sqrt(2 * (1 - R)))
    return 1 if a >= 1 else -1


def _get_crms(mod_std: float, obs_std: float, R: float) -> float:
    return sqrt(mod_std**2 + obs_std**2 - 2 * mod_std * obs_std * R)


def _get_beta_mqi(rms: float, rmsu: float) -> float:
    """Returns Beta*MQI. Divide by chosen Beta to get MQI."""
    return rms / rmsu


def compute_fairmode_stats(obs_var: str, stats: dict) -> dict:
    species_list = ["concno2", "vmro3", "concpm10", "concpm25"]

    fairmode_stats = dict()

    if obs_var not in species_list:
        return fairmode_stats

    mean = stats["refdata_mean"]
    obs_std = stats["refdata_std"]
    mod_std = stats["data_std"]
    R = stats["R"]
    bias = stats["mb"]
    rms = stats["rms"]

    crms = _get_crms(mod_std, obs_std, R)  # sqrt(rms ** 2 - bias ** 2)
    sign = _get_fairmode_sign(mod_std, obs_std, R)
    rmsu, UrRV, RV, alpha = _get_RMSU(mean, obs_std, obs_var)
    beta_mqi = _get_beta_mqi(rms, rmsu)

    # Check that fairmode staistics are computed as expected by checking MQI (Model Quality Indicator) for beta = 1
    assert isclose(
        rmsu * beta_mqi,
        sqrt((bias) ** 2 + (mod_std - obs_std) ** 2 + (2 * obs_std * mod_std * (1 - R))),
        rel_tol=1e-5,
    )

    fairmode_stats["RMSU"] = rmsu
    fairmode_stats["sign"] = sign
    fairmode_stats["crms"] = crms
    fairmode_stats["bias"] = bias
    fairmode_stats["rms"] = rms
    fairmode_stats["alpha"] = alpha
    fairmode_stats["UrRV"] = UrRV
    fairmode_stats["RV"] = RV
    fairmode_stats["beta_mqi"] = beta_mqi

    return fairmode_stats
