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

    # TODO: Check if stats are calculated on the aggrigated regional timeseries, or if the timeseries for all stations in the region is sent in
    # Might have to be done differently for spatial and temporal stats
    # Might have to check if the aggrigation/mean done for temporal timeseries is done the same as rest of pyaerocom
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

    def _get_radar_stats(
        self,
        data: xr.DataArray,
        var_name: str,
        use_weights: bool,
    ) -> dict[str, dict[str, float]]:

        def critY(obs: np.ndarray, mask, axis=None) -> np.ndarray:
            return SPECIES[var_name]["UrRV"] * np.sqrt(
                (1 - SPECIES[var_name]["alpha"] ** 2)
                * (np.mean(obs, where=mask, axis=axis) ** 2 / SPECIES[var_name]["Np"])
                + (
                    SPECIES[var_name]["alpha"] ** 2
                    * SPECIES[var_name]["RV"] ** 2
                    / SPECIES[var_name]["Nnp"]
                )
            )

        stats = {}

        # Calculate the seasonal, weekly, and diurnal differences for each station type

        for c in ["rur", "urb", "sub"]:
            subset = data.where(data.station_type == c)
            obsvals = subset.data[0]
            modvals = subset.data[1]

            mask = np.isfinite(obsvals) & np.isfinite(modvals)

            rms = critY(obsvals, mask)

            season_stats = self._season_diff(obsvals, modvals, mask, subset.time.dt.month, rms)
            week_stats = self._week_diff(obsvals, modvals, mask, subset.time.dt.day, rms)
            day_stats = self._day_diff(obsvals, modvals, mask, subset.time.dt.hour, rms)

            stats[c] = dict(season=season_stats, week=week_stats, day=day_stats)

        # MQI
        obsvals = data.data[0]
        modvals = data.data[1]

        mask = np.isfinite(obsvals) & np.isfinite(modvals)

        critH = SPECIES[var_name]["UrRV"] * np.sqrt(
            (1 - SPECIES[var_name]["alpha"] ** 2)
            * (np.std(obsvals, where=mask) ** 2 + np.mean(obsvals, where=mask) ** 2)
            + (SPECIES[var_name]["alpha"] ** 2 * SPECIES[var_name]["RV"] ** 2)
        )

        diff = modvals - obsvals
        diffsquare = diff**2

        rms = np.sqrt(np.nanmean(diffsquare, where=mask))
        stats["MQI_YD"] = rms / critH
        stats["MQI_HD"] = np.abs(
            np.mean(obsvals, where=mask) - np.mean(modvals, where=mask)
        ) / critY(obsvals, mask)

        # MPI

        stats["temporal"] = {
            "bias": np.abs(np.mean(modvals, where=mask) - np.mean(obsvals, where=mask)) / critH,
            "1-R": 2
            * np.std(modvals, where=mask)
            * np.std(obsvals, where=mask)
            * (1 - FairmodeStatistics.pearson_R(obsvals.flatten(), modvals.flatten()))
            / critH**2,
            "std": np.abs(np.std(modvals, where=mask) - np.std(obsvals, where=mask)) / critH,
        }

        mean_obs = np.mean(obsvals, where=mask)
        mean_mod = np.mean(modvals, where=mask)
        mean_mask = np.isfinite(mean_obs) & np.isfinite(mean_mod)

        station_critY = critY(obsvals, mask, axis=0)

        sumsq = np.sqrt(np.mean(station_critY**2))

        stats["spatial"] = {
            "1-R": 2
            * np.std(mean_obs, where=mean_mask)
            * np.std(mean_mod, where=mean_mask)
            * (1 - FairmodeStatistics.pearson_R(mean_obs.flatten(), mean_mod.flatten()))
            / sumsq**2,
            "std": np.abs(np.std(mean_mod, where=mean_mask) - np.std(mean_obs, where=mean_mask))
            / sumsq,
        }

        # Urban-rural difference

        ub_obs = data.where(data.station_type == "urb").data[0]
        ub_mod = data.where(data.station_type == "urb").data[1]

        rb_obs = data.where(data.station_type == "rur").data[0]
        rb_mod = data.where(data.station_type == "rur").data[1]

        ub_mask = np.isfinite(ub_obs) & np.isfinite(ub_mod)
        rb_mask = np.isfinite(rb_obs) & np.isfinite(rb_mod)

        ub_critY = critY(ub_obs, ub_mask)
        rb_critY = critY(rb_obs, rb_mask)

        stats["ub-rb"] = np.abs(
            (np.mean(ub_mod, where=ub_mask) - np.mean(ub_obs, where=ub_mask) / ub_critY)
            - (np.mean(rb_mod, where=rb_mask) - np.mean(rb_obs, where=rb_mask) / rb_critY)
        )

        return stats
