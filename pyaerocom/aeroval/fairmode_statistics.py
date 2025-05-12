import logging

# from pathlib import Path
import numpy as np
import xarray as xr

from pyaerocom import ColocatedData
from pyaerocom.aeroval.experiment_output import ExperimentOutput
from pyaerocom.units.datetime import TsType

logger = logging.getLogger(__name__)


SPECIES = dict(
    concno2=dict(UrRV=0.24, RV=200, alpha=0.2, freq=TsType("hourly"), percentile=99.8, Np=5.2, Nnp=5.5),
    conco3mda8=dict(UrRV=0.18, RV=120, alpha=0.79, freq=TsType("daily"), percentile=92.9, Np=11., Nnp=3.),
    concpm10=dict(UrRV=0.28, RV=50, alpha=0.25, freq=TsType("daily"), percentile=90.1, Np=20., Nnp=1.5),
    concpm25=dict(UrRV=0.36, RV=25, alpha=0.5, freq=TsType("daily"), percentile=90.1, Np=20., Nnp=1.5),
)

EXC_THRESHOLDS = dict(  # we assume all the units are ug/m3
    concpm25=25.0,
    concpm10=50.0,
    conco3mda8=120.0,
    concno2=200.0,
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

        obsmean = np.nanmean(obsvals, axis=0, where=mask)
        modmean = np.nanmean(modvals, axis=0, where=mask)

        obsstd = np.std(obsvals, axis=0, where=mask)
        modstd = np.std(modvals, axis=0, where=mask)

        diff = modvals - obsvals
        diffsquare = diff**2

        rms = np.sqrt(np.nanmean(diffsquare, axis=0, where=mask))
        bias = np.nanmean(diff, axis=0, where=mask)

        NMB = self._NMB(modvals, obsvals)
        R = self.pearson_R(obsvals, modvals)
        rmsu = self._RMSU(obsmean, obsstd, var_name)
        sign = self._fairmode_sign(modstd, obsstd, R)
        crms = self._crms(modstd, obsstd, R)
        mqi = self._mqi(rms, rmsu, beta=1)
        mb = self._mb(bias, rmsu, beta=1)
        beta_Hperc = self._beta_Hperc(obsvals, modvals, var_name)
        exceedances = self._exceedances(data=data, var_name=var_name)

        BRMSUt = self.BRMSU_t(obsvals, beta=1, spec=var_name, mask=mask)
        BRMSUs = self.BRMSU_s(obsmean, beta=1, spec=var_name, mask=mask)

        assert np.allclose(rmsu, BRMSUt, equal_nan=True)

        MPI_bias_t = self._MPI_bias_t(obsmean, modmean, BRMSUt)
        MPI_R_t = self._MPI_R_t(obsstd, modstd, R, BRMSUt)
        MPI_std_t = self._MPI_std_t(obsstd, modstd, BRMSUt)

        MPI_R_s = self._MPI_R_s(obsmean, modmean, BRMSUs)
        MPI_std_s = self._MPI_std_s(obsmean, modmean, BRMSUs)

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
                obs_mean=obsmean[i],
                mod_std=modstd[i],
                mod_mean=modmean[i],
                exceedances_obs=int(exceedances[0][i]),
                exceedances_mod=int(exceedances[1][i]),
                MPI_R_t=MPI_R_t[i],
                MPI_bias_t=MPI_bias_t[i],
                MPI_std_t=MPI_std_t[i],
                MPI_R_s=MPI_R_s,
                MPI_std_s=MPI_std_s,
                NMB=NMB[i],
                R=R[i],
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
    def _exceedances(data: xr.DataArray, var_name: str) -> list[np.array]:
        if var_name == "concno2":
            new_data = data.resample(time="1D", skipna=True).max()
        else:
            new_data = data

        obsvals = new_data.data[0]
        modvals = new_data.data[1]

        mask = ~np.isnan(obsvals) * ~np.isnan(modvals)
        obsex = np.nansum(obsvals > EXC_THRESHOLDS[var_name], axis=0, where=mask)
        modex = np.nansum(modvals > EXC_THRESHOLDS[var_name], axis=0, where=mask)

        return [obsex, modex]

    @staticmethod
    def _NMB(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        num = np.nansum(x - y, axis=0)
        denum = np.nansum(x, axis=0)
        return np.where(denum == 0, np.nan, num / denum)

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

    def obsuncertainty(self, obs: np.ndarray, spec: str) -> np.ndarray:
        """formula 57 here https://fairmode.jrc.ec.europa.eu/document/fairmode/WG1/Guidance_MQO_Bench_vs3.3_20220519.pdf"""

        if spec not in SPECIES:
            raise ValueError(f"Unsupported {spec=}")

        UrRV = SPECIES[spec]["UrRV"]
        RV = SPECIES[spec]["RV"]
        alpha = SPECIES[spec]["alpha"]

        in_sqrt = (1 - alpha**2) * (obs**2) + alpha**2 * RV**2

        return UrRV * np.sqrt(in_sqrt)

    def BRMSU_t(self, obsvals: np.ndarray, beta: float, spec: str, mask: np.ndarray) -> np.ndarray:
        return beta * np.sqrt(np.nanmean(np.square(self.obsuncertainty(obsvals, spec), where=mask), axis=0))

    def BRMSU_s(self, obsmean: np.ndarray, beta: float, spec: str) -> float:
        return beta * np.sqrt(np.nanmean(self.obsuncertainty(obsmean, spec)))

    @staticmethod
    def _MPI_R_t(obsstd: np.array, modstd: np.array, R: float, BRMSUt: np.array) -> np.array:
        # TIME Corr Norm: 2 sigma_O sigma_M(1-R) / (beta^2 RMS_U^2)
        # ----------------------------------------------------------
        # MF formula: (2.*scores['obs_std']*scores['sim_std']*(1. - scores['PearsonR'])) / (beta*rmsu)**2
        return np.where(BRMSUt == 0, np.nan, 2 * modstd * obsstd * (1 - R) / BRMSUt**2)

    @staticmethod
    def _MPI_bias_t(obsmean: np.array, modmean: np.array, BRMSUt: np.array) -> np.array:
        # TIME Bias Norm: |BIAS| / (beta RMS_U)
        # -------------------------------------------
        # MF formula: scores['MeanBias']/(beta*rmsu)
        return np.where(
            BRMSUt == 0, np.nan, np.abs(modmean - obsmean) / BRMSUt
        )  # check the abs here, why NMF does not have it?

    @staticmethod
    def _MPI_std_t(obsstd: np.array, modstd: np.array, BRMSUt: np.array) -> np.array:
        # TIME StDev Norm: (sigma_M-sigma_O) / (beta RMS_U)
        # ---------------------------------------------------
        # MF formula: (scores['sim_std']-scores['obs_std'])/(beta*rmsu)
        return np.where(BRMSUt == 0, np.nan, modstd - obsstd / BRMSUt)

    @staticmethod
    def _MPI_R_s(obsmean: np.array, modmean: np.array, BRMSUs: float) -> float:
        # SPACE Corr Norm: 2 sigma_bar{O} sigma_bar{M} (1-R) / (beta^2 RMS_bar{U}^2)
        # ----------------------------------------------------------------------------
        # MF formula: ((2.*np.nanstd(obs)*np.nanstd(sim)*(1. - corr)) / (beta*rmsu_)**2)
        # where sim = scores['sim_mean'], obs = scores['obs_mean']
        # corr = ((np.nanmean((obs-np.nanmean(obs))*(sim-np.nanmean(sim)))) / (np.nanstd(obs)*np.nanstd(sim)))
        corr = (
            0.0
            if np.nanstd(obsmean) * np.nanstd(modmean) == 0
            else np.nanmean((obsmean - np.nanmean(obsmean)) * (modmean - np.nanmean(modmean)))
            / (np.nanstd(obsmean) * np.nanstd(modmean))
        )
        return (
            2 * np.nanstd(obsmean) * np.nanstd(modmean) * (1.0 - corr) / BRMSUs**2
            if BRMSUs != 0
            else np.nan
        )

    @staticmethod
    def _MPI_std_s(obsmean: np.array, modmean: np.array, BRMSUs: float) -> float:
        # SPACE StDev Norm: (sigma_bar{M}-sigma_bar{O}) / ( beta RMS_bar{U})
        # -------------------------------------------------------------------
        # MF formula: (np.nanstd(sim)-np.nanstd(obs))/(beta*rmsu_)
        # where sim = scores['sim_mean'], obs = scores['obs_mean']
        return (np.nanstd(modmean) - np.nanstd(obsmean)) / BRMSUs if BRMSUs != 0 else np.nan

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

        return (Mperc - Operc) / (beta * uncertainty_Operc)
