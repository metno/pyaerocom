import logging

# from pathlib import Path
import numpy as np
import xarray as xr

from pyaerocom import ColocatedData
from pyaerocom.aeroval.experiment_output import ExperimentOutput
from pyaerocom.units.datetime import TsType

logger = logging.getLogger(__name__)


SPECIES = dict(
    concno2=dict(UrRV=0.24, RV=200, alpha=0.2, freq=TsType("hourly"), percentile=99.8),
    conco3mda8=dict(UrRV=0.18, RV=120, alpha=0.79, freq=TsType("daily"), percentile=92.9),
    concpm10=dict(UrRV=0.28, RV=50, alpha=0.25, freq=TsType("daily"), percentile=90.1),
    concpm25=dict(UrRV=0.36, RV=25, alpha=0.5, freq=TsType("daily"), percentile=90.1),
)


class FairmodeStatistics:
    """
    Class for computing the FAIRMODE statistics

    FAIRMODE is the Forum for Air Quality Modeling, an initiative to bring together air quality modelers and users.
        - Promote and Support the use of models by EU Member States
        - Emphasis is on model application for air quality policy (monitoring, regulation, etc.)
        - Develop harmonized set of tools to test whether or a not a model is fit for a given purpose
        - CAMS has to make use of FAIRMODE diagrams

    This module contains methods to compute the relevant FAIRMODE statistics.
    """

    species = SPECIES

    def __init__(self):
        pass

    def save_fairmode_stats(
        self,
        exp_output: ExperimentOutput,
        fairmode_stats: dict,
        obs_name: str,
        var_name_web: str,
        vert_code: str,
        modelname: str,
        model_var: str,
    ):
        for regname in fairmode_stats:
            exp_output.add_fairmode_entry(
                fairmode_stats[regname],
                regname,
                obs_name,
                var_name_web,
                vert_code,
                modelname,
                model_var,
            )

    def fairmode_statistics(self, coldata: ColocatedData, var_name: str):
        return self._get_stats(coldata.data, var_name, False)

    def _get_stats(
        self, data: xr.DataArray, var_name: str, use_weights: bool
    ) -> dict[str, dict[str, float]]:
        stations = data.station_name.values
        station_types = data.station_type.values

        obsvals = data.data[0]
        modvals = data.data[1]

        mask = ~np.isnan(obsvals) * ~np.isnan(modvals)

        obsmean = np.nanmean(obsvals, axis=0)

        obsstd = np.std(obsvals, axis=0, where=mask)
        modstd = np.std(modvals, axis=0, where=mask)

        diff = modvals - obsvals
        diffsquare = diff**2

        rms = np.sqrt(np.nanmean(diffsquare, axis=0, where=mask))
        bias = np.nanmean(diff, axis=0, where=mask)

        R = self.pearson_R(obsvals, modvals)
        rmsu = self._RMSU(obsmean, obsstd, var_name)
        sign = self._fairmode_sign(modstd, obsstd, R)
        crms = self._crms(modstd, obsstd, R)
        mqi = self._mqi(rms, rmsu, beta=1)
        mb = self._mb(bias, rmsu, beta=1)
        beta_Hperc = self._beta_Hperc(obsvals, modvals, var_name)

        assert len(rmsu) == len(stations)
        assert len(sign) == len(stations)
        assert len(crms) == len(stations)
        assert len(bias) == len(stations)
        assert len(rms) == len(stations)
        assert len(mqi) == len(stations)
        assert len(mb) == len(stations)
        assert len(beta_Hperc) == len(stations)

        stats_list: dict[str, dict[str, float]] = {
            stations[i]: dict(
                RMSU=rmsu[i],
                sign=[sign[i]],
                crms=crms[i],
                bias=bias[i],
                rms=[rms[i]],
                beta_mqi=[mqi[i]],
                Hperc=beta_Hperc[i],
                persistence_model=False,
                station_type=station_types[i],
                **{k: (str(v) if k == "freq" else v) for (k, v) in SPECIES[var_name].items()},
            )
            for i in range(len(stations))
        }

        return stats_list

    @staticmethod
    def pearson_R(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        mask = ~np.isnan(x) * ~np.isnan(y)

        xmean = np.mean(x, axis=0, where=mask)
        ymean = np.mean(y, axis=0, where=mask)
        xm = x - xmean
        ym = y - ymean
        normxm = np.sqrt(np.sum(xm * xm, axis=0, where=mask))
        normym = np.sqrt(np.sum(ym * ym, axis=0, where=mask))

        r = np.where(
            normxm * normym == 0.0,
            np.nan,
            np.sum(xm * ym, axis=0, where=mask) / (normxm * normym),
        )

        return r

    @staticmethod
    def _RMSU(mean: float, std: float, spec: str) -> float:
        """RMSU is the Root Mean Squared Uncertainty associated with the uncertainty of the observations, U(O_i)."""

        if spec not in SPECIES:
            raise ValueError(f"Unsupported {spec=}")

        UrRV = SPECIES[spec]["UrRV"]
        RV = SPECIES[spec]["RV"]
        alpha = SPECIES[spec]["alpha"]

        in_sqrt = (1 - alpha**2) * (mean**2 + std**2) + alpha**2 * RV**2

        return UrRV * np.sqrt(in_sqrt)

    @staticmethod
    def _fairmode_sign(mod_std: float, obs_std: float, R: float) -> float:
        a = np.where(
            np.logical_or(obs_std <= 0, R >= 1),
            1,
            np.abs(mod_std - obs_std) / (obs_std * np.sqrt(2 * (1 - R))),
        )
        return np.where(a >= 1, 1.0, -1.0)

    @staticmethod
    def _crms(mod_std: float, obs_std: float, R: float) -> float:
        """Returns the Centered Root Mean Squared Error"""
        return np.sqrt(mod_std**2 + obs_std**2 - 2 * mod_std * obs_std * R)

    @staticmethod
    def _mqi(rms: float, rmsu: float, *, beta: float) -> float:
        """Model Quality Indicator (MQI). Pass beta=1 for `beta MQI`"""
        return rms / (rmsu * beta)

    @staticmethod
    def _mb(bias: float, rmsu: float, *, beta: float) -> float:
        """Model Bias(MB). Pass beta=1 for `beta MB`"""
        return bias / (rmsu * beta)

    @staticmethod
    def _beta_Hperc(obs: np.ndarray, mod: np.ndarray, var_name: str, beta=1) -> np.ndarray:
        percentile = SPECIES[var_name]["percentile"]
        Operc = np.nanpercentile(obs, percentile, axis=0)
        Mperc = np.nanpercentile(mod, percentile, axis=0)

        factor = SPECIES[var_name]["alpha"] ** 2 * SPECIES[var_name]["RV"] ** 2
        uncertainty_Operc = SPECIES[var_name]["UrRV"] * np.sqrt(
            (1 - SPECIES[var_name]["alpha"] ** 2) * Operc**2 + factor
        )

        return (Operc - Mperc) / (beta * uncertainty_Operc)
