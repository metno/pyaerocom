from __future__ import annotations

import logging
import re
import time
import warnings
from pathlib import Path
from reprlib import repr

import numpy as np
import xarray as xr

from pyaerocom import ColocatedData
from pyaerocom.aeroval._processing_base import ProcessingEngine
from pyaerocom.aeroval.coldatatojson_helpers import (
    _select_period_season_coldata,
    init_regions_web,
)
from pyaerocom.aeroval.fairmode_statistics import SPECIES, FairmodeStatistics
from pyaerocom.exceptions import DataCoverageError, UnknownRegion
from pyaerocom.io.cams2_83.models import ModelName
from pyaerocom.units.datetime import TsType

logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")


class CAMS2_83_Engine(ProcessingEngine):
    MEDIANSCORE_SPECIES = [
        "concno2",
        "concco",
        "conco3",
        "concso2",
        "concpm10",
        "concpm25",
    ]

    def run(
        self, files: list[list[str | Path]], var_list: list
    ) -> None:  # type:ignore[override]
        logger.info(f"Processing: {repr(files)}")
        coldata = [ColocatedData(data=file) for file in files]
        coldata, persistence_cols, found_vars, found_persistence = self._sort_coldata(
            coldata
        )
        start = time.time()

        if var_list is None:
            var_list_2 = list(found_vars)
            if not var_list_2:
                logging.warning(
                    f"No variables found in colocated data var_list={var_list}, found_vars={found_vars}"
                )
                return
        elif var_list == ["conco3"] or (len(var_list) > 1 and "conco3" in var_list):
            var_list_2 = list(var_list)
            var_list_2.append("conco3mda8")
        else:
            var_list_2 = list(var_list)

        logger.info(f"Running CAMS2_83_Engine.run with var_list_2 {var_list_2}")
        for var in var_list_2:
            if var not in found_vars:
                logger.warning(f"{var} not found in coldata, skipping")
                continue
            logger.info(f"Processing Component: {var}")
            if found_persistence:
                self.process_coldata(coldata[var], persistence_cols[var], var)
            else:
                self.process_coldata(coldata[var], [], var)

        logger.info(f"Time for weird plot: {time.time() - start} sec")

    def process_coldata(
        self,
        coldata: list[ColocatedData],
        persistence_coldata: list[ColocatedData],
        var_name: str,
    ) -> None:
        use_weights = self.cfg.statistics_opts.weighted_stats
        forecast_days = self.cfg.statistics_opts.forecast_days
        periods = self.cfg.time_cfg.periods

        # use_fairmode = self.cfg.statistics_opts.use_fairmode
        use_fairmode = self.cfg.cams2_83_cfg.use_cams2_83_fairmode
        calc_forecast_target = False

        calc_medianscores = True if var_name in self.MEDIANSCORE_SPECIES else False

        if use_fairmode:
            fairmode_statistics = FairmodeStatistics()

        if use_fairmode and len(persistence_coldata) > 0 and var_name in SPECIES:
            persistence_coldata = persistence_coldata[0]
            calc_forecast_target = True

            if SPECIES[var_name]["freq"] != TsType("hourly"):
                persistence_coldata = persistence_coldata.resample_time(
                    SPECIES[var_name]["freq"],
                    settings_from_meta=True,
                )

        if "var_name_input" in coldata[0].metadata:
            obs_var = coldata[0].metadata["var_name_input"][0]
            model_var = coldata[0].metadata["var_name_input"][1]
        else:
            obs_var = model_var = "UNDEFINED"

        # for the MOS/ENS evaluation experiment the models are just strings
        # we do not want them added to the ModelName class
        # so we need a bunch of ugly special cases here
        modelname = coldata[0].model_name.split("-")[2]
        if modelname == "ENS" or modelname == "MOS":
            model = modelname
        else:
            model = ModelName[modelname]
        vert_code = coldata[0].get_meta_item("vert_code")
        obs_name = coldata[0].obs_name
        if modelname == "ENS" or modelname == "MOS":  # MOS/ENS evaluation special case
            mcfg = self.cfg.model_cfg.get_entry(modelname)
        else:
            mcfg = self.cfg.model_cfg.get_entry(model.name)
        var_name_web = mcfg.get_varname_web(model_var, obs_var)
        seasons = self.cfg.time_cfg.get_seasons()

        regions_how = "country"
        use_country = True
        for i in range(forecast_days):
            coldata[i].data["season"] = coldata[i].data.time.dt.season
            (regborders, regs, regnames) = init_regions_web(coldata[i], regions_how)

        if calc_forecast_target:
            persistence_coldata.data["season"] = persistence_coldata.data.time.dt.season
            (regborders, regs, regnames) = init_regions_web(
                persistence_coldata, regions_how
            )
            # results_mqi = {}
        results = {}
        results_fairmode = {}

        for regid, regname in regnames.items():
            results[regname] = {}
            results_fairmode[regname] = {}
            logger.info(f"Creating subset for {regname}")
            try:
                subset_region = [
                    col.filter_region(regid, check_country_meta=use_country)
                    for col in coldata
                ]
                if calc_forecast_target:
                    persistence_subset_region = persistence_coldata.filter_region(
                        regid, check_country_meta=use_country
                    )
                    # results_mqi[regname] = {}
            except (DataCoverageError, UnknownRegion) as e:
                logger.info(
                    f"Skipping forecast plot for {regname} due to error {str(e)}"
                )
                continue
            for per in periods:
                for season in seasons:
                    perstr = f"{per}-{season}"

                    stats_list: dict[str, list[float]] = dict(
                        rms=[], R=[], nmb=[], mnmb=[], fge=[]
                    )
                    logger.info(f"Making subset for {regid}, {per} and {season}")
                    if season not in coldata[0].data["season"].data and season != "all":
                        logger.info(
                            f"Season {season} is not available for {per} and will be skipped"
                        )
                        continue

                    try:
                        subset = [
                            _select_period_season_coldata(
                                col, per, season, use_meteorological_seasons=True
                            )
                            for col in subset_region
                        ]
                    except (DataCoverageError, UnknownRegion) as e:
                        logger.info(f"Skipping forecast plot due to error {str(e)}")
                        continue
                    if calc_medianscores:
                        for forecast_hour in range(24 * forecast_days):
                            logger.debug(
                                f"Calculating statistics for hour {forecast_hour}"
                            )
                            leap, hour = divmod(forecast_hour, 24)
                            ds = subset[leap]
                            ds = ds.data.sel(time=(ds.time.dt.hour == hour))
                            start = time.time()
                            stats = self._get_median_stats_point_vec(ds, use_weights)
                            logger.debug(time.time() - start)
                            for key in stats_list:
                                stats_list[key].append(stats[key])

                    if use_fairmode and var_name in SPECIES:

                        fairmode_subset = subset[0]
                        if SPECIES[var_name]["freq"] != TsType("hourly"):
                            fairmode_subset = fairmode_subset.resample_time(
                                SPECIES[var_name]["freq"],
                                settings_from_meta=True,
                            )

                        results_fairmode[f"{regname}"][f"{perstr}"] = (
                            fairmode_statistics.fairmode_statistics(
                                fairmode_subset, var_name
                            )
                        )

                        if calc_forecast_target:
                            
                            results_mqi = []
                            for day in range(forecast_days):
                                ds = subset[day]
                                ds_p = persistence_subset_region

                                
                                mqi_results = self._calc_forecast_target_MQI_vectorized(
                                    ds, ds_p, var_name, day
                                )

                                results_mqi.append(mqi_results)

                               

                            for station in results_fairmode[f"{regname}"][f"{perstr}"]:
                                results_fairmode[f"{regname}"][f"{perstr}"][station][
                                    "rms"
                                ] = []
                                results_fairmode[f"{regname}"][f"{perstr}"][station][
                                    "beta_mqi"
                                ] = []
                                results_fairmode[f"{regname}"][f"{perstr}"][station][
                                    "sign"
                                ] = []

                                results_fairmode[f"{regname}"][f"{perstr}"][station][
                                    "persistence_model"
                                ] = True
                                for day in range(forecast_days):
                                    mqi_p = (
                                        results_mqi[day][station]
                                        if station in results_mqi[day]
                                        else [np.nan, np.nan, np.nan]
                                    )
                                    results_fairmode[f"{regname}"][f"{perstr}"][
                                        station
                                    ]["rms"].append(mqi_p[0])
                                    results_fairmode[f"{regname}"][f"{perstr}"][
                                        station
                                    ]["beta_mqi"].append(mqi_p[1])
                                    results_fairmode[f"{regname}"][f"{perstr}"][
                                        station
                                    ]["sign"].append(mqi_p[2])

                    out_dirs = self.cfg.path_manager.get_json_output_dirs(
                        True
                    )  # noqa: F841

                    results[f"{regname}"][f"{perstr}"] = stats_list

            if calc_medianscores:
                self.exp_output.add_forecast_entry(
                    results[regname],
                    regname,
                    obs_name,
                    var_name_web,
                    vert_code,
                    (
                        modelname
                        if (modelname == "ENS" or modelname == "MOS")
                        else model.name
                    ),  # MOS/ENS evaluation special case
                    model_var,
                )

        if use_fairmode and var_name in SPECIES:
            fairmode_statistics.save_fairmode_stats(
                self.exp_output,
                results_fairmode,
                obs_name,
                var_name_web,
                vert_code,
                (
                    modelname
                    if (modelname == "ENS" or modelname == "MOS")
                    else model.name
                ),  # MOS/ENS evaluation special case
                model_var,
            )

    def _get_median_stats_point(
        self, data: xr.DataArray, use_weights: bool
    ) -> dict[str, float]:
        stats_list: dict[str, list[float]] = dict(rms=[], R=[], nmb=[], mnmb=[], fge=[])
        station_list = data.station_name.data
        for station in station_list:
            d = data.sel(station_name=[station])
            arr = ColocatedData(data=d)
            stats = arr.calc_statistics(use_area_weights=use_weights)
            for key in stats_list.keys():
                stats_list[key].append(stats[key])
        median_stats = {}
        for key in stats_list.keys():
            median_stats[key] = np.nanmedian(np.array(stats_list[key]))

        return median_stats

    def _get_median_stats_point_vec(
        self, data: xr.DataArray, use_weights: bool
    ) -> dict[str, float]:
        stats_list: dict[str, float] = dict(rms=0.0, R=0.0, nmb=0.0, mnmb=0.0, fge=0.0)

        obsvals = data.data[0]
        modvals = data.data[1]

        mask = ~np.isnan(obsvals) * ~np.isnan(modvals)

        diff = modvals - obsvals
        diffsquare = diff**2
        sum_obs = np.sum(obsvals, axis=0, where=mask)
        sum_diff = np.sum(diff, axis=0, where=mask)
        sum_vals = obsvals + modvals

        tmp = diff / sum_vals

        nmb = np.where(sum_obs == 0, np.nan, sum_diff / sum_obs)

        mnmb = 2.0 * np.mean(tmp, axis=0, where=mask)
        fge = 2.0 * np.mean(np.abs(tmp), axis=0, where=mask)
        rms = np.sqrt(np.mean(diffsquare, axis=0, where=mask))

        R = self._pearson_R_vec(obsvals, modvals)

        stats_list["rms"] = np.nanmedian(rms)
        stats_list["R"] = np.nanmedian(R)
        stats_list["nmb"] = np.nanmedian(nmb)
        stats_list["mnmb"] = np.nanmedian(mnmb)
        stats_list["fge"] = np.nanmedian(fge)

        return stats_list

    def _pearson_R_vec(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return FairmodeStatistics.pearson_R(x, y)

    def _calc_forecast_target_MQI_vectorized(
        self,
        coldata: ColocatedData,
        persistence_coldata: ColocatedData,
        var_name: str,
        forecast_day: int,
    ) -> dict[str, float]:

        results = {}

        # Resampling of time for all other variables than NO2
        if SPECIES[var_name]["freq"] != TsType("hourly"):
            coldata = coldata.resample_time(
                SPECIES[var_name]["freq"],
                settings_from_meta=True,
            )

        # Creation of mask of shared stations between normal data and persistence data
        # stations = persistence_coldata.data.station_name.values
        station_mask = np.intersect1d(
            persistence_coldata.data.station_name.values,
            coldata.data.station_name.values,
            return_indices=True,
        )
        assert np.all(
            persistence_coldata.data.station_name.values[station_mask[1]]
            == coldata.data.station_name.values[station_mask[2]]
        )

        # Gets times. Moves percistence time forward, indicating that the obs on day N is the perstence model on day N+1 (or rather N+forecast_day+1)
        data_time = coldata.time.values
        p_time = persistence_coldata.time.values + np.timedelta64(
            24 * (forecast_day + 1), "h"
        )  # This needs to be checked if it is correct for forecast days > 0

        # Masks the time, so that only dates which has a valid persistence model and data are used
        time_mask = np.intersect1d(p_time, data_time, return_indices=True)

        # Fetching of masked data
        obs_vals = coldata.data.data[0, :, station_mask[2]][:, time_mask[2]]
        mod_vals = coldata.data.data[1, :, station_mask[2]][:, time_mask[2]]
        p_mod_vals = persistence_coldata.data.data[0, :, station_mask[1]][
            :, time_mask[1]
        ]  # persistence model

        # Gets a NaN mask
        mask = ~np.isnan(obs_vals) * ~np.isnan(mod_vals) * ~np.isnan(p_mod_vals)

        # Sanity Check
        assert np.all(p_mod_vals.shape == obs_vals.shape)

        sign = self._target_plot_sign(
            obsvals=obs_vals, modvals=mod_vals, mask=mask, var_name=var_name
        )

        # Calculation of MQI
        factor = SPECIES[var_name]["alpha"] ** 2 * SPECIES[var_name]["RV"] ** 2
        uncertainty_p_obs = SPECIES[var_name]["UrRV"] * np.sqrt(
            (1 - SPECIES[var_name]["alpha"] ** 2) * p_mod_vals**2 + factor
        )

        p_diff_vals = np.maximum(
            np.abs(obs_vals - p_mod_vals - uncertainty_p_obs),
            np.abs(obs_vals - p_mod_vals + uncertainty_p_obs),
        )

        rmse_m = np.sqrt(np.nanmean((mod_vals - obs_vals) ** 2, axis=1, where=mask))
        rmse_p = np.sqrt(np.nanmean((p_diff_vals) ** 2, axis=1, where=mask))

        mqi = rmse_m / rmse_p

        results = {
            str(station_mask[0][i]): [rmse_p[i], mqi[i], sign[i]]
            for i in range(len(mqi))
        }

        return results

    def _target_plot_sign(
        self,
        obsvals: np.ndarray,
        modvals: np.ndarray,
        mask: np.ndarray,
        var_name: str,
    ) -> np.ndarray:

        threshold = SPECIES[var_name]["RV"]
        false_alarms = np.sum(
            np.logical_and(modvals > threshold, obsvals <= threshold, where=mask),
            axis=1,
            where=mask,
        )
        missed_alarms = np.sum(
            np.logical_and(modvals <= threshold, obsvals > threshold, where=mask),
            axis=1,
            where=mask,
        )
        sign = np.where(
            false_alarms <= missed_alarms, -1.0, 1.0
        )  
        return sign

    def _sort_coldata(
        self, coldata: list[ColocatedData]
    ) -> tuple[
        dict[str, list[ColocatedData]], dict[str, list[ColocatedData]], set[str], bool
    ]:
        col_dict = dict()
        persistence_dict = dict()

        persistence_var_list = []
        var_list = []

        found_persistence = False

        for col in coldata:
            obs_var = col.metadata["var_name_input"][0]

            if "persistence" in col.model_name:
                found_persistence = True
                if obs_var in persistence_dict:
                    persistence_dict[obs_var].append(col)
                else:
                    persistence_dict[obs_var] = [col]
                    persistence_var_list.append(obs_var)
            else:
                if obs_var in col_dict:
                    col_dict[obs_var].append(col)
                else:
                    col_dict[obs_var] = [col]
                    var_list.append(obs_var)
        if found_persistence:
            logger.info(f"persistence model has been found for {persistence_var_list}")
            assert set(sorted(var_list)) == set(sorted(persistence_var_list))
        for var, cols in col_dict.items():
            col_dict[var] = sorted(cols, key=lambda x: self._get_day(x.model_name))

        return col_dict, persistence_dict, set(var_list), found_persistence

    def _get_day(self, model_name: str) -> int:
        return int(re.search(".*day([0-3]).*", model_name).group(1))
