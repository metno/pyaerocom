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
from pyaerocom.aeroval.coldatatojson_helpers import _select_period_season_coldata, init_regions_web
from pyaerocom.exceptions import DataCoverageError, UnknownRegion
from pyaerocom.io.cams2_83.models import ModelName

logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")


class CAMS2_83_Engine(ProcessingEngine):
    def run(self, files: list[list[str | Path]], var_list: list) -> None:  # type:ignore[override]
        logger.info(f"Processing: {repr(files)}")
        coldata = [ColocatedData(data=file) for file in files]
        coldata, found_vars = self._sort_coldata(coldata)
        start = time.time()
        if var_list is None:
            var_list = list(found_vars)
        for var in var_list:
            logger.info(f"Processing Component: {var}")
            self.process_coldata(coldata[var])

        logger.info(f"Time for weird plot: {time.time() - start} sec")

    def process_coldata(self, coldata: list[ColocatedData]) -> None:
        use_weights = self.cfg.statistics_opts.weighted_stats
        out_dirs = self.cfg.path_manager.get_json_output_dirs(True)
        forecast_days = self.cfg.statistics_opts.forecast_days
        periods = self.cfg.time_cfg.periods

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

        results = {}

        for regid, regname in regnames.items():
            results[regname] = {}
            logger.info(f"Creating subset for {regname}")
            try:
                subset_region = [
                    col.filter_region(regid, check_country_meta=use_country) for col in coldata
                ]
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
                            _select_period_season_coldata(col, per, season)
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
        xmean = np.nanmean(x, axis=0)
        ymean = np.nanmean(y, axis=0)
        xm = x - xmean
        ym = y - ymean
        normxm = np.sqrt(np.nansum(xm * xm, axis=0))
        normym = np.sqrt(np.nansum(ym * ym, axis=0))

        r = np.where(
            normxm * normym == 0.0,
            np.nan,
            np.nansum(xm * ym, axis=0) / (normxm * normym),
        )

        return r

    def _sort_coldata(
        self, coldata: list[ColocatedData]
    ) -> tuple[dict[str, list[ColocatedData]], set[str]]:
        col_dict = dict()
        var_list = []

        for col in coldata:
            obs_var = col.metadata["var_name_input"][0]

            if obs_var in col_dict:
                col_dict[obs_var].append(col)
            else:
                col_dict[obs_var] = [col]
                var_list.append(obs_var)

        for var, cols in col_dict.items():
            col_dict[var] = sorted(cols, key=lambda x: self._get_day(x.model_name))

        return col_dict, set(var_list)

    def _get_day(self, model_name: str) -> int:
        return int(re.search(".*day([0-3]).*", model_name).group(1))
