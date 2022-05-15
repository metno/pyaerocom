"""
Functions for computing the FAIRMODE statistics

FAIRMODE is the Forum for Air Quality Modeling, an initative to bring together air quality modelers and users.
    - Promote and Support the use of models by EU Member States
    - Emphasis is on model application for air quality policy (monitoring, regulation, etc.)
    - Develop harmonized set of tools to test whether or a not a model is fit for a given purpose
    - CAMS has to make use of FAIRMODE diagrams

This module contains methods to cmpute the relevant FAIRMODE statistics.
"""

from numpy import isclose, isnan, nan, sqrt

SPECIES = dict(
    concno2=dict(UrRV=0.24, RV=200, alpha=0.2),
    vmro3=dict(UrRV=0.18, RV=120, alpha=0.79),
    concpm10=dict(UrRV=0.28, RV=50, alpha=0.13),
    concpm25=dict(UrRV=0.36, RV=25, alpha=0.3),
)


def _RMSU(mean: float, std: float, spec: str) -> float:
    """RMSU is the Root Mean Squared Uncertainity associated with the uncertainity of the observations, U(O_i)."""

    if spec not in SPECIES:
        raise ValueError(f"Unsupported {spec=}")

    UrRV = SPECIES[spec]["UrRV"]
    RV = SPECIES[spec]["RV"]
    alpha = SPECIES[spec]["alpha"]

    in_sqrt = (1 - alpha**2) * (mean**2 + std**2) + alpha**2 * RV**2

    return UrRV * sqrt(in_sqrt)


def _fairmode_sign(mod_std: float, obs_std: float, R: float) -> float:
    if isnan(R) or isnan(obs_std):
        return nan
    assert obs_std >= 0, f"negative {obs_std=}"
    assert -1 <= R <= 1, f"out of range {R=}"
    if obs_std <= 0 or R >= 1:  # guard aginst sqrt(<0) or div0 errors
        return 1
    a = abs(mod_std - obs_std) / (obs_std * sqrt(2 * (1 - R)))
    return 1 if a >= 1 else -1


def _crms(mod_std: float, obs_std: float, R: float) -> float:
    """Returns the Centered Root Mean Squared Error"""
    return sqrt(mod_std**2 + obs_std**2 - 2 * mod_std * obs_std * R)


def _mqi(rms: float, rmsu: float, *, beta: float) -> float:
    """Model Quality Indicator (MQI). Pass beta=1 for `beta MQI`"""
    return rms / (rmsu * beta)


def fairmode_stats(obs_var: str, stats: dict) -> dict:
    if obs_var not in SPECIES or any(isnan(list(stats.values()))):
        return {}

    mean = stats["refdata_mean"]
    obs_std = stats["refdata_std"]
    mod_std = stats["data_std"]
    R = stats["R"]
    bias = stats["mb"]
    rms = stats["rms"]

    crms = _crms(mod_std, obs_std, R)  # sqrt(rms ** 2 - bias ** 2)
    sign = _fairmode_sign(mod_std, obs_std, R)
    rmsu = _RMSU(mean, obs_std, obs_var)
    beta_mqi = _mqi(rms, rmsu, beta=1)

    # Check that fairmode staistics are computed as expected by checking MQI (Model Quality Indicator) for beta = 1
    assert isclose(
        rmsu * beta_mqi,
        sqrt((bias) ** 2 + (mod_std - obs_std) ** 2 + (2 * obs_std * mod_std * (1 - R))),
        rtol=1e-5,
    )

    fairmode = dict(
        RMSU=rmsu,
        sign=sign,
        crms=crms,
        bias=bias,
        rms=rms,
        beta_mqi=beta_mqi,
        **SPECIES[obs_var],
    )
    return fairmode
