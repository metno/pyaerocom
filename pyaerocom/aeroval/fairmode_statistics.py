import logging

# from pathlib import Path
import numpy as np
import xarray as xr

from pyaerocom import ColocatedData
from pyaerocom.aeroval.experiment_output import ExperimentOutput
from pyaerocom.units.datetime import TsType

logger = logging.getLogger(__name__)


SPECIES = dict(
    concno2=dict(
        UrRV=0.24,
        RV=200,
        alpha=0.2,
        freq=TsType("hourly"),
        percentile=99.8,
        Np=5.2,
        Nnp=5.5,
    ),
    conco3mda8=dict(
        UrRV=0.18,
        RV=120,
        alpha=0.79,
        freq=TsType("daily"),
        percentile=92.9,
        Np=11.0,
        Nnp=3.0,
    ),
    concpm10=dict(
        UrRV=0.28,
        RV=50,
        alpha=0.25,
        freq=TsType("daily"),
        percentile=90.1,
        Np=20.0,
        Nnp=1.5,
    ),
    concpm25=dict(
        UrRV=0.36,
        RV=25,
        alpha=0.5,
        freq=TsType("daily"),
        percentile=90.1,
        Np=20.0,
        Nnp=1.5,
    ),
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
        period: str,
        regname: str,
    ):
        exp_output.add_fairmode_entry(
            fairmode_stats[regname],
            regname,
            obs_name,
            var_name_web,
            vert_code,
            modelname,
            model_var,
            period,
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

        mask = np.isfinite(obsvals) & np.isfinite(modvals)

        obsmean = np.mean(obsvals, axis=0, where=mask)
        modmean = np.mean(modvals, axis=0, where=mask)

        obsstd = np.std(obsvals, axis=0, where=mask)
        modstd = np.std(modvals, axis=0, where=mask)

        diff = modvals - obsvals
        diffsquare = diff**2

        rms = np.sqrt(np.nanmean(diffsquare, axis=0, where=mask))
        bias = np.nanmean(diff, axis=0, where=mask)

        βRMSUt = self._βRMSU_t(obsvals, beta=1, var_name=var_name, mask=mask)
        βRMSUs = self._βRMSU_s(obsmean, beta=1, var_name=var_name)

        NMB = self._NMB(modvals, obsvals)
        R = self.pearson_R(obsvals, modvals)
        sign = self._fairmode_sign(modstd, obsstd, R)
        crms = self._crms(modstd, obsstd, R)
        mqi = self._mqi(rms, βRMSUt, beta=1)
        mb = self._mb(bias, βRMSUt, beta=1)
        beta_Hperc = self._beta_Hperc(obsvals, modvals, var_name)
        exceedances = self._exceedances(data=data, var_name=var_name)
        fa, ma, gan, gap = self._exceedances_indicators(data=data, var_name=var_name)

        MPI_bias_t = self._MPI_bias_t(obsmean, modmean, βRMSUt)
        MPI_R_t = self._MPI_R_t(obsstd, modstd, R, βRMSUt)
        MPI_std_t = self._MPI_std_t(obsstd, modstd, βRMSUt)

        MPI_R_s = self._MPI_R_s(obsmean, modmean, βRMSUs)
        MPI_std_s = self._MPI_std_s(obsmean, modmean, βRMSUs)

        assert len(βRMSUt) == len(stations)
        assert len(sign) == len(stations)
        assert len(crms) == len(stations)
        assert len(bias) == len(stations)
        assert len(rms) == len(stations)
        assert len(mqi) == len(stations)
        assert len(mb) == len(stations)
        assert len(beta_Hperc) == len(stations)

        stats_list: dict[str, dict[str, float]] = {
            stations[i]: dict(
                exceedances_obs=int(exceedances[0][i]),
                MPI_mean=obsmean[i],
                MPI_R_t=MPI_R_t[i],
                MPI_bias_t=MPI_bias_t[i],
                MPI_std_t=MPI_std_t[i],
                MPI_R_s=MPI_R_s,
                MPI_std_s=MPI_std_s,
                MPI_Hperc=beta_Hperc[i],
                fa=int(fa[i]),
                ma=int(ma[i]),
                gan=int(gan[i]),
                gap=int(gap[i]),
                bias=bias[i],
                NMB=NMB[i],
                RMSU=βRMSUt[i],
                sign=[sign[i]],
                crms=crms[i],
                rms=[rms[i]],
                beta_mqi=[mqi[i]],
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

        mask = np.isfinite(obsvals) & np.isfinite(modvals)
        obsex = np.sum(obsvals > EXC_THRESHOLDS[var_name], axis=0, where=mask)
        modex = np.sum(modvals > EXC_THRESHOLDS[var_name], axis=0, where=mask)

        return [obsex, modex]

    @staticmethod
    def _exceedances_indicators(data: xr.DataArray, var_name: str) -> tuple[np.array]:
        obsvals = data.data[0]
        modvals = data.data[1]

        mask = np.isfinite(obsvals) & np.isfinite(modvals)
        obsex = obsvals > EXC_THRESHOLDS[var_name]
        modex = modvals > EXC_THRESHOLDS[var_name]

        fa = np.sum(np.logical_and(modex, ~obsex), axis=0, where=mask, out=None)
        ma = np.sum(np.logical_and(~modex, obsex), axis=0, where=mask, out=None)
        gan = np.sum(np.logical_and(~obsex, ~modex), axis=0, where=mask, out=None)
        gap = np.sum(np.logical_and(obsex, modex), axis=0, where=mask, out=None)

        return fa, ma, gan, gap

    @staticmethod
    def _NMB(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        num = np.nansum(x - y, axis=0)
        denum = np.nansum(x, axis=0)
        return np.where(denum == 0, np.nan, num / denum)

    @staticmethod
    def pearson_R(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        mask = np.isfinite(x) & np.isfinite(y)

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

    # in the following _s and _t are for the spatial(ly averaged) and temporal(ly-only averaged) quantities,
    # we define a _βRMSU_t to be used for the calculation of (following MeteoFrance/evaltools naming)
    # Time Bias Norm (_MPI_bias_t), Time Corr Norm (_MPI_r_t) and Time StdDev Norm (_MPI_std_t)
    # and a _βRMSU_s to be used for the calculation of Space Corr Norm (_MPI_R_s) and Space StDev Norm (_MPI_std_s)

    @staticmethod
    def _βRMSU_t(
        obsvals: np.ndarray,
        beta: float,
        var_name: str,
        mask: np.ndarray,
    ) -> np.ndarray:
        def obsuncertainty(obs: np.ndarray, spec: str) -> np.ndarray:
            """eq. 7 and 37 here https://fairmode.jrc.ec.europa.eu/document/fairmode/WG1/Guidance_MQO_Bench_vs3.3_20220519.pdf"""

            if spec not in SPECIES:
                raise ValueError(f"Unsupported {spec=}")

            UrRV = SPECIES[spec]["UrRV"]
            RV = SPECIES[spec]["RV"]
            alpha = SPECIES[spec]["alpha"]

            in_sqrt = (1 - alpha**2) * (obs**2) + alpha**2 * RV**2

            return UrRV * np.sqrt(in_sqrt)

        return beta * np.sqrt(
            np.nanmean(np.square(obsuncertainty(obsvals, var_name)), where=mask, axis=0)
        )

    @staticmethod
    def _βRMSU_s(obsmean: np.ndarray, beta: float, var_name: str) -> float:
        def obsuncertainty(obs: np.ndarray, spec: str) -> np.ndarray:
            """eq. 39 here https://fairmode.jrc.ec.europa.eu/document/fairmode/WG1/Guidance_MQO_Bench_vs3.3_20220519.pdf"""

            if spec not in SPECIES:
                raise ValueError(f"Unsupported {spec=}")

            UrRV = SPECIES[spec]["UrRV"]
            RV = SPECIES[spec]["RV"]
            alpha = SPECIES[spec]["alpha"]
            N_p = SPECIES[spec]["Np"]
            N_np = SPECIES[spec]["Nnp"]

            in_sqrt = (1 - alpha**2) / N_p * (obs**2) + alpha**2 * RV**2 / N_np

            return UrRV * np.sqrt(in_sqrt)

        return beta * np.sqrt(np.nanmean(np.square(obsuncertainty(obsmean, var_name))))

    @staticmethod
    def _MPI_R_t(obsstd: np.array, modstd: np.array, R: float, βRMSUt: np.array) -> np.array:
        # TIME Corr Norm: 2 sigma_O sigma_M(1-R) / (beta^2 RMS_U^2)
        # ----------------------------------------------------------
        # MF eq.: (2.*scores['obs_std']*scores['sim_std']*(1. - scores['PearsonR'])) / (beta*rmsu)**2
        return np.where(βRMSUt == 0, np.nan, 2 * modstd * obsstd * (1 - R) / βRMSUt**2)

    @staticmethod
    def _MPI_bias_t(obsmean: np.array, modmean: np.array, βRMSUt: np.array) -> np.array:
        # TIME Bias Norm: |BIAS| / (beta RMS_U)
        # -------------------------------------------
        # MF eq.: scores['MeanBias']/(beta*rmsu)
        return np.where(
            βRMSUt == 0, np.nan, (modmean - obsmean) / βRMSUt
        )  # check the abs here, why NMF does not have it?

    @staticmethod
    def _MPI_std_t(obsstd: np.array, modstd: np.array, βRMSUt: np.array) -> np.array:
        # TIME StDev Norm: (sigma_M-sigma_O) / (beta RMS_U)
        # ---------------------------------------------------
        # MF eq.: (scores['sim_std']-scores['obs_std'])/(beta*rmsu)
        return np.where(βRMSUt == 0, np.nan, (modstd - obsstd) / βRMSUt)

    @staticmethod
    def _MPI_R_s(obsmean: np.array, modmean: np.array, βRMSUs: float) -> float:
        # SPACE Corr Norm: 2 sigma_bar{O} sigma_bar{M} (1-R) / (beta^2 RMS_bar{U}^2)
        # ----------------------------------------------------------------------------
        # MF eq.: ((2.*np.nanstd(obs)*np.nanstd(sim)*(1. - corr)) / (beta*rmsu_)**2)
        # where sim = scores['sim_mean'], obs = scores['obs_mean']
        # corr = ((np.nanmean((obs-np.nanmean(obs))*(sim-np.nanmean(sim)))) / (np.nanstd(obs)*np.nanstd(sim)))
        corr = (
            0.0
            if np.nanstd(obsmean) * np.nanstd(modmean) == 0
            else np.nanmean((obsmean - np.nanmean(obsmean)) * (modmean - np.nanmean(modmean)))
            / (np.nanstd(obsmean) * np.nanstd(modmean))
        )
        return (
            2 * np.nanstd(obsmean) * np.nanstd(modmean) * (1.0 - corr) / βRMSUs**2
            if βRMSUs != 0
            else np.nan
        )

    @staticmethod
    def _MPI_std_s(obsmean: np.array, modmean: np.array, βRMSUs: float) -> float:
        # SPACE StDev Norm: (sigma_bar{M}-sigma_bar{O}) / ( beta RMS_bar{U})
        # -------------------------------------------------------------------
        # MF eq.: (np.nanstd(sim)-np.nanstd(obs))/(beta*rmsu_)
        # where sim = scores['sim_mean'], obs = scores['obs_mean']
        return (np.nanstd(modmean) - np.nanstd(obsmean)) / βRMSUs if βRMSUs != 0 else np.nan

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
