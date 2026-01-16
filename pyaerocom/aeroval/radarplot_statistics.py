import logging

# from pathlib import Path
import numpy as np
import xarray as xr
from typing import Callable

from pyaerocom import ColocatedData
from pyaerocom.aeroval.fairmode_statistics import FairmodeStatistics
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

        return stats
