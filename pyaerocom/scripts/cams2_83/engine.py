from __future__ import annotations

import logging
import re
import time
import warnings
from pathlib import Path
from reprlib import repr
from tqdm import tqdm

import numpy as np
import xarray as xr

from pyaerocom import ColocatedData
from pyaerocom.aeroval._processing_base import ProcessingEngine
from pyaerocom.aeroval.coldatatojson_helpers import _select_period_season_coldata, init_regions_web, _process_sites, _init_meta_glob, _init_site_coord_arrays
from pyaerocom.exceptions import DataCoverageError, UnknownRegion
from pyaerocom.io.cams2_83.models import ModelName
from pyaerocom.aeroval.fairmode_engine import FairmodeEngine, SPECIES

logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")


class CAMS2_83_Engine(ProcessingEngine):
    def run(self, files: list[list[str | Path]], var_list: list) -> None:  # type:ignore[override]
        logger.info(f"Processing: {repr(files)}")
        coldata = [ColocatedData(data=file) for file in files]
        coldata, persistent_cols, found_vars = self._sort_coldata(coldata)
        start = time.time()
        if var_list is None:
            var_list = list(found_vars)
        elif var_list == ["conco3"] or len(var_list) > 1:
            var_list.append("conco3mda8")

        for var in var_list:
            logger.info(f"Processing Component: {var}")
            self.process_coldata(coldata[var], persistent_cols[var], var)

            # self.make_forecast_target_plots(coldata[var], persistent_cols[var], var)

        logger.info(f"Time for weird plot: {time.time() - start} sec")



    def process_coldata(self, coldata: list[ColocatedData],  persistent_coldata: list[ColocatedData], var_name: str) -> None:
        use_weights = self.cfg.statistics_opts.weighted_stats
        forecast_days = self.cfg.statistics_opts.forecast_days
        periods = self.cfg.time_cfg.periods

        use_fairmode = self.cfg.statistics_opts.use_fairmode
        calc_forecast_target = False

        if use_fairmode:
            fairmode_engine = FairmodeEngine(self.cfg)


        if use_fairmode and len(persistent_coldata) > 0 and var_name in SPECIES:
            persistent_coldata = persistent_coldata[0]
            calc_forecast_target = True

            if SPECIES[var_name]["freq"] != "hourly":
                persistent_coldata = persistent_coldata.resample_time(SPECIES[var_name]["freq"])

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
            persistent_coldata.data["season"] = persistent_coldata.data.time.dt.season
            (regborders, regs, regnames) = init_regions_web(persistent_coldata, regions_how)
            # results_mqi = {}
        results = {}
        results_fairmode = {}

        for regid, regname in regnames.items():
            results[regname] = {}
            results_fairmode[regname] = {}
            logger.info(f"Creating subset for {regname}")
            try:
                subset_region = [
                    col.filter_region(regid, check_country_meta=use_country) for col in coldata
                ]
                if calc_forecast_target:
                    persistent_subset_region = persistent_coldata.filter_region(regid, check_country_meta=use_country)
                    # results_mqi[regname] = {}
            except (DataCoverageError, UnknownRegion) as e:
                logger.info(f"Skipping forecast plot for {regname} due to error {str(e)}")
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
                            _select_period_season_coldata(col, per, season, use_meteorological_seasons)
                            for col in subset_region
                        ]
                    except (DataCoverageError, UnknownRegion) as e:
                        logger.info(f"Skipping forecast plot due to error {str(e)}")
                        continue

                    for forecast_hour in range(24 * forecast_days):
                        logger.debug(f"Calculating statistics for hour {forecast_hour}")
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
                        if SPECIES[var_name]["freq"] != "hourly":
                            fairmode_subset = fairmode_subset.resample_time(SPECIES[var_name]["freq"])

                        results_fairmode[f"{regname}"][f"{perstr}"] = fairmode_engine.fairmode_statistics(fairmode_subset, var_name)

                        if calc_forecast_target:
                            # results_mqi[f"{regname}"][f"{perstr}"] = {}
                            results_mqi = []
                            for day in range(forecast_days):
                                ds = subset[day]
                                ds_p = persistent_subset_region

                                #mqi_results = self._calc_forecast_target_MQI(ds, ds_p, var_name)
                                mqi_results = self._calc_forecast_target_MQI_vectorized(ds, ds_p, var_name, day)

                                results_mqi.append(mqi_results)

                                # results_mqi[f"{regname}"][f"{perstr}"][day] = mqi_results

                            for station in results_fairmode[f"{regname}"][f"{perstr}"]:
                                results_fairmode[f"{regname}"][f"{perstr}"][station]["beta_mb"] = []
                                results_fairmode[f"{regname}"][f"{perstr}"][station]["beta_mqi"] = []
                                for day in range(forecast_days):
                                    mqi_p = results_mqi[day][station] if station in results_mqi[day] else [np.nan, np.nan]
                                    results_fairmode[f"{regname}"][f"{perstr}"][station]["beta_mb"].append(mqi_p[0])
                                    results_fairmode[f"{regname}"][f"{perstr}"][station]["beta_mqi"].append(mqi_p[1])


                    out_dirs = self.cfg.path_manager.get_json_output_dirs(True)  # noqa: F841

                    results[f"{regname}"][f"{perstr}"] = stats_list

            self.exp_output.add_forecast_entry(
                results[regname],
                regname,
                obs_name,
                var_name_web,
                vert_code,
                (
                    modelname if (modelname == "ENS" or modelname == "MOS") else model.name
                ),  # MOS/ENS evaluation special case
                model_var,
            )
        if use_fairmode and var_name in SPECIES:
            fairmode_engine.save_fairmode_stats(
                results_fairmode,
                obs_name,
                var_name_web,
                vert_code,
                (
                    modelname if (modelname == "ENS" or modelname == "MOS") else model.name
                ),  # MOS/ENS evaluation special case
                model_var,
            )


    def _get_median_stats_point(self, data: xr.DataArray, use_weights: bool) -> dict[str, float]:
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

        diff = modvals - obsvals
        diffsquare = diff**2
        sum_obs = np.nansum(obsvals, axis=0)
        sum_diff = np.nansum(diff, axis=0)
        sum_vals = obsvals + modvals

        tmp = diff / sum_vals

        nmb = np.where(sum_obs == 0, np.nan, sum_diff / sum_obs)

        mnmb = 2.0 * np.nanmean(tmp, axis=0)
        fge = 2.0 * np.nanmean(np.abs(tmp), axis=0)
        rms = np.sqrt(np.nanmean(diffsquare, axis=0))

        R = self._pearson_R_vec(obsvals, modvals)

        stats_list["rms"] = np.nanmedian(rms)
        stats_list["R"] = np.nanmedian(R)
        stats_list["nmb"] = np.nanmedian(nmb)
        stats_list["mnmb"] = np.nanmedian(mnmb)
        stats_list["fge"] = np.nanmedian(fge)

        return stats_list

    def _pearson_R_vec(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return FairmodeEngine.pearson_R(x,y)
        # xmean = np.nanmean(x, axis=0)
        # ymean = np.nanmean(y, axis=0)
        # xm = x - xmean
        # ym = y - ymean
        # normxm = np.sqrt(np.nansum(xm * xm, axis=0))
        # normym = np.sqrt(np.nansum(ym * ym, axis=0))

        # r = np.where(
        #     normxm * normym == 0.0,
        #     np.nan,
        #     np.nansum(xm * ym, axis=0) / (normxm * normym),
        # )

        # return r

    def _calc_forecast_target_MQI(self, coldata: ColocatedData, persistent_coldata: ColocatedData, var_name: str) -> dict[str, float]:

        stations = persistent_coldata.data.station_name.values

        time = coldata.time.values
        wanted_time = time - np.timedelta64(24,"h")
        p_time = persistent_coldata.time.values

        mask = np.intersect1d(p_time, wanted_time, return_indices=True)[1]

        results = {}

        for i in tqdm(range(len(stations))):
            assert str(persistent_coldata.data.station_name[i].values) == str(coldata.data.station_name[i].values)

            obs_vals = coldata.data.data[0, :, i]
            mod_vals = coldata.data.data[1, :, i]

            len_data = len(obs_vals)

            p_mod_vals = persistent_coldata.data.data[0,mask,i]

            factor = SPECIES[var_name]["alpha"]**2*SPECIES[var_name]["RV"]**2
            uncertainty_p_obs = SPECIES[var_name]["UrRV"]*np.sqrt((1-SPECIES[var_name]["alpha"]**2)*p_mod_vals**2 + factor)

            p_diff_vals = np.maximum(np.abs(obs_vals - p_mod_vals-uncertainty_p_obs), np.abs(obs_vals - p_mod_vals + uncertainty_p_obs))

            rmse_m = np.nanmean((mod_vals-obs_vals)**2)
            rmse_p = np.nanmean((p_diff_vals)**2)

            bias_m = np.nanmean((mod_vals-obs_vals))

            mb = bias_m/rmse_p
            mqi = rmse_m/rmse_p

            results[stations[i]] = [mb, mqi]

        return results

    def _calc_forecast_target_MQI_vectorized(self, coldata: ColocatedData, persistent_coldata: ColocatedData, var_name: str, forecast_day: int) -> dict[str, float]:

        results = {}


        # Resampling of time for all other variables than NO2
        if SPECIES[var_name]["freq"] != "hourly":
            coldata = coldata.resample_time(SPECIES[var_name]["freq"])

        # Creation of mask of shared stations between normal data and peristent data
        #stations = persistent_coldata.data.station_name.values
        station_mask =  np.intersect1d(persistent_coldata.data.station_name.values, coldata.data.station_name.values, return_indices=True)
        assert np.all(persistent_coldata.data.station_name.values[station_mask[1]] == coldata.data.station_name.values[station_mask[2]])


        # Creation of mask of shared timestamps between normal data and peristent data
        time = coldata.time.values
        wanted_time = time - np.timedelta64(24*(forecast_day+1),"h")
        p_time = persistent_coldata.time.values

        time_mask = np.intersect1d(p_time, wanted_time, return_indices=True)[1]



        # Fetching of masked data
        obs_vals = coldata.data.data[0, :, station_mask[2]]
        mod_vals = coldata.data.data[1, :, station_mask[2]]

        p_mod_vals = persistent_coldata.data.data[0,:, station_mask[1]][:,time_mask] # Persitent model

        assert np.all(p_mod_vals.shape == obs_vals.shape)

        # Calculation of MQI
        factor = SPECIES[var_name]["alpha"]**2*SPECIES[var_name]["RV"]**2
        uncertainty_p_obs = SPECIES[var_name]["UrRV"]*np.sqrt((1-SPECIES[var_name]["alpha"]**2)*p_mod_vals**2 + factor)

        p_diff_vals = np.maximum(np.abs(obs_vals - p_mod_vals-uncertainty_p_obs), np.abs(obs_vals - p_mod_vals + uncertainty_p_obs))

        rmse_m = np.nanmean((mod_vals-obs_vals)**2, axis=1)
        rmse_p = np.nanmean((p_diff_vals)**2, axis=1)

        mqi = rmse_m/rmse_p

        mb_p = np.nanmean((mod_vals-obs_vals), axis=1)/rmse_p

        results = {str(station_mask[0][i]): [mb_p[i],mqi[i]] for i in range(len(mqi))}

        return results



    def _sort_coldata(
        self, coldata: list[ColocatedData]
    ) -> tuple[dict[str, list[ColocatedData]], dict[str, list[ColocatedData]], set[str]]:
        col_dict = dict()
        persistent_dict = dict()

        persistent_var_list = []
        var_list = []


        for col in coldata:
            obs_var = col.metadata["var_name_input"][0]

            if "persistent" in col.model_name:
                if obs_var in persistent_dict:
                    persistent_dict[obs_var].append(col)
                else:
                    persistent_dict[obs_var] = [col]
                    persistent_var_list.append(obs_var)
            else:
                if obs_var in col_dict:
                    col_dict[obs_var].append(col)
                else:
                    col_dict[obs_var] = [col]
                    var_list.append(obs_var)

        assert set(sorted(var_list)) == set(sorted(persistent_var_list))
        for var, cols in col_dict.items():
            col_dict[var] = sorted(cols, key=lambda x: self._get_day(x.model_name))

        return col_dict, persistent_dict, set(var_list)

    def _get_day(self, model_name: str) -> int:
        return int(re.search(".*day([0-3]).*", model_name).group(1))
