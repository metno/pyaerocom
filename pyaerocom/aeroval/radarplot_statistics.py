import logging

# from pathlib import Path
import numpy as np
import xarray as xr
from typing import Callable

from pyaerocom import ColocatedData
from pyaerocom.aeroval.fairmode_statistics import FairmodeStatistics, SPECIES
from pyaerocom.aeroval.experiment_output import ExperimentOutput
from pyaerocom.units.datetime import TsType

logger = logging.getLogger(__name__)


class RadarPlotStatistics:
    """
    Class for computing the radar plot statistics

    see https://gmd.copernicus.org/articles/18/4231/2025/
    """

    def __init__(self):
        pass

    def save_radarplot_stats(
        self,
        exp_output: ExperimentOutput,
        radar_stats: dict,
        obs_name: str,
        var_name_web: str,
        vert_code: str,
        modelname: str,
        model_var: str,
        period: str,
        regname: str,
    ):
        print("Saving radar plot")
        exp_output.add_radarplot_entry(
            radar_stats[regname],
            regname,
            obs_name,
            var_name_web,
            vert_code,
            modelname,
            model_var,
            period,
        )

    def get_radarplot_statistics(self, coldata: ColocatedData, var_name: str):
        return self._get_radar_stats(coldata.data, var_name, False)

    def _season_diff(
        self,
        obsdata: np.ndarray,
        moddata: np.ndarray,
        mask: np.ndarray,
        months: np.ndarray,
        rms: float,
    ) -> float:
        diff_obs = np.nanmean(obsdata[np.isin(months, [12, 1, 2]), :]) - np.nanmean(
            obsdata[np.isin(months, [6, 7, 8]), :]
        )
        diff_mod = np.nanmean(moddata[np.isin(months, [12, 1, 2]), :]) - np.nanmean(
            moddata[np.isin(months, [6, 7, 8]), :]
        )

        return (diff_mod - diff_obs) / rms

    def _week_diff(
        self,
        obsdata: np.ndarray,
        moddata: np.ndarray,
        mask: np.ndarray,
        days: np.ndarray,
        rms: float,
    ) -> float:
        diff_obs = np.nanmean(obsdata[np.isin(days, [1, 2, 3, 4, 5]), :]) - np.nanmean(
            obsdata[np.isin(days, [6, 7]), :]
        )
        diff_mod = np.nanmean(moddata[np.isin(days, [1, 2, 3, 4, 5]), :]) - np.nanmean(
            moddata[np.isin(days, [6, 7]), :]
        )

        return (diff_mod - diff_obs) / rms

    def _day_diff(
        self,
        obsdata: np.ndarray,
        moddata: np.ndarray,
        mask: np.ndarray,
        hours: np.ndarray,
        rms: float,
    ) -> float:
        day_hours = list(range(8, 21))
        night_hours = list(range(0, 8)) + list(range(20, 24))
        diff_obs = np.nanmean(obsdata[np.isin(hours, day_hours), :]) - np.nanmean(
            obsdata[np.isin(hours, night_hours), :]
        )
        diff_mod = np.nanmean(moddata[np.isin(hours, day_hours), :]) - np.nanmean(
            moddata[np.isin(hours, night_hours), :]
        )

        return (diff_mod - diff_obs) / rms

    def _get_UB_RB(self, subset_ub: xr.DataArray, subset_rb: xr.DataArray, var_name: str) -> float:
        # For UB
        obsdata_ub = subset_ub.data[0]
        moddata_ub = subset_ub.data[1]

        # For RB
        obsdata_rb = subset_rb.data[0]
        moddata_rb = subset_rb.data[1]

        mask_ub = np.isfinite(obsdata_ub) & np.isfinite(moddata_ub)
        mask_rb = np.isfinite(obsdata_rb) & np.isfinite(moddata_rb)

        rms_ub = FairmodeStatistics._βRMSU_s(
            np.mean(obsdata_ub, axis=0, where=mask_ub), 1, var_name
        )
        rms_rb = FairmodeStatistics._βRMSU_s(
            np.mean(obsdata_rb, axis=0, where=mask_rb), 1, var_name
        )

        inc_model = np.mean(moddata_ub, where=mask_ub) - np.mean(moddata_rb, where=mask_rb)
        inc_obs = np.mean(obsdata_ub, where=mask_ub) - np.mean(obsdata_rb, where=mask_rb)

        mpi = abs(inc_model - inc_obs) / (0.5 * (rms_ub + rms_rb))

        return mpi

    def _get_radar_mpi(
        self,
        obsvals: np.ndarray,
        modvals: np.ndarray,
        var_name: str,
        mask: np.ndarray,
    ) -> dict[str, dict]:

        obsmean = np.mean(obsvals, axis=0, where=mask)
        modmean = np.mean(modvals, axis=0, where=mask)

        obsmean_t = np.mean(obsvals, axis=1, where=mask)
        modmean_t = np.mean(modvals, axis=1, where=mask)

        mask_t = np.isfinite(obsmean_t) & np.isfinite(modmean_t)
        R = FairmodeStatistics.pearson_R(obsmean_t, modmean_t)

        obsstd = np.std(obsmean_t, where=mask_t)
        modstd = np.std(modmean_t, where=mask_t)

        βRMSUt = FairmodeStatistics._βRMSU_t(obsmean_t, beta=1, var_name=var_name, mask=mask_t)
        βRMSUs = FairmodeStatistics._βRMSU_s(obsmean, beta=1, var_name=var_name)

        MPI_bias_t = FairmodeStatistics._MPI_bias_t(np.mean(obsmean), np.mean(modmean), βRMSUt)
        MPI_R_t = FairmodeStatistics._MPI_R_t(obsstd, modstd, R, βRMSUt)
        MPI_std_t = FairmodeStatistics._MPI_std_t(obsstd, modstd, βRMSUt)

        MPI_R_s = FairmodeStatistics._MPI_R_s(obsmean, modmean, βRMSUs)
        MPI_std_s = FairmodeStatistics._MPI_std_s(obsmean, modmean, βRMSUs)
        MPI_bias_s = np.where(βRMSUs == 0, np.nan, (np.mean(modmean) - np.mean(obsmean)) / βRMSUs)

        return {
            "spatial": {
                "1-R": float(MPI_R_s),
                "bias": float(MPI_bias_s),
                "std": float(MPI_std_s),
            },
            "temporal": {
                "1-R": float(MPI_R_t),
                "bias": float(MPI_bias_t),
                "std": float(MPI_std_t),
            },
        }

    def _get_radar_mqi(
        self, obsdata: np.ndarray, moddata: np.ndarray, var_name: str, mask: np.ndarray
    ) -> tuple[float, float]:
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

        diff = moddata - obsdata
        diffsquare = diff**2

        rmse = np.sqrt(np.mean(diffsquare, where=mask))
        rms = FairmodeStatistics._βRMSU_s(np.mean(obsdata, axis=0, where=mask), 1, var_name)

        mqi_hd = rmse / rms

        mqi_yd = abs(np.mean(obsdata, where=mask) - np.mean(moddata, where=mask)) / (
            obsuncertainty(np.mean(obsdata, where=mask), var_name)
        )

        return float(mqi_hd), float(mqi_yd)

    def _get_radar_stats(
        self,
        data: xr.DataArray,
        var_name: str,
        use_weights: bool,
    ) -> dict[str, dict[str, float]]:
        stats = {}

        for c in ["rur", "urb", "sub"]:
            subset = data.where(data.station_type == c)
            obsvals = subset.data[0]
            modvals = subset.data[1]

            mask = np.isfinite(obsvals) & np.isfinite(modvals)

            rms = FairmodeStatistics._βRMSU_s(np.mean(obsvals, axis=0, where=mask), 1, var_name)

            season_stats = self._season_diff(obsvals, modvals, mask, subset.time.dt.month, rms)
            week_stats = self._week_diff(obsvals, modvals, mask, subset.time.dt.day, rms)
            day_stats = self._day_diff(obsvals, modvals, mask, subset.time.dt.hour, rms)

            stats[c] = dict(season=season_stats, week=week_stats, day=day_stats)

        obsvals = data.data[0]
        modvals = data.data[1]

        mask = np.isfinite(obsvals) & np.isfinite(modvals)

        mpis = self._get_radar_mpi(obsvals, modvals, var_name, mask)

        stats["temporal"] = mpis["temporal"]
        stats["spatial"] = mpis["spatial"]

        mqi_hd, mqi_yd = self._get_radar_mqi(obsvals, modvals, var_name, mask)
        stats["MQI_YD"] = mqi_yd
        stats["MQI_HD"] = mqi_hd

        stats["ub-rb"] = self._get_UB_RB(
            data.where(data.station_type == "urb"),
            data.where(data.station_type == "rur"),
            var_name,
        )
        return stats
