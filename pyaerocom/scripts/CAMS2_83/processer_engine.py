from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from reprlib import repr
from typing import Tuple
from unittest import result

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pyaerocom import ColocatedData
from pyaerocom.aeroval._processing_base import ProcessingEngine
from pyaerocom.aeroval.coldatatojson_helpers import _add_entry_json, write_json
from pyaerocom.io.cams2_83.models import ModelName

logger = logging.getLogger(__name__)


class CAMS2_83_Engine(ProcessingEngine):
    def run(self, files: list[list[str | Path]], var_list: list) -> None:  # type:ignore[override]
        logger.info(f"Processing: {repr(files)}")
        coldata = [ColocatedData(file) for file in files]
        coldata, found_vars = self._sort_coldata(coldata)
        if var_list is None:
            var_list = list(found_vars)
        for var in var_list:
            logger.info(f"Processing Component: {var}")
            self.process_coldata(coldata[var])

    def process_coldata(self, coldata: list[ColocatedData]) -> None:
        use_weights = self.cfg.statistics_opts.weighted_stats
        out_dirs = self.cfg.path_manager.get_json_output_dirs(True)
        forecast_days = self.cfg.statistics_opts.forecast_days

        model = ModelName[coldata[0].model_name.split("-")[2]]
        vert_code = coldata[0].get_meta_item("vert_code")
        obs_name = coldata[0].obs_name

        if "var_name_input" in coldata[0].metadata:
            obs_var = coldata[0].metadata["var_name_input"][0]
            model_var = coldata[0].metadata["var_name_input"][1]
        else:
            obs_var = model_var = "UNDEFINED"

        # mcfg = self.cfg.model_cfg.get_entry("-".join(model_name.split("-")[:-1]))
        mcfg = self.cfg.model_cfg.get_entry(model.name)
        var_name_web = mcfg.get_varname_web(model_var, obs_var)

        hourrange = list(range(24 * forecast_days))

        stats_list: dict[str, list[float]] = {
            "rms": [],
            "R": [],
            # "R_spearman": [],
            # "R_kendall": [],
            "nmb": [],
            "mnmb": [],
            "fge": [],
        }

        for hour in hourrange:
            leap = hour // 24
            h = hour % 24
            col = coldata[leap]
            time = col.time.data

            time_to_use = []
            for t in time:
                if pd.Timestamp(t).hour == h:
                    time_to_use.append(t)

            data = col.data.sel(time=time_to_use)

            stats = self._get_median_stats_point(data, use_weights)

            for key in stats_list.keys():
                stats_list[key].append(stats[key])

        name = "day0.json"  # f"cams2-83_{model_name}-{model_var}.json"
        filename = os.path.join(out_dirs["conf"], name)

        results = {"WORLD": {"2021-2022-all": stats_list}}
        _add_entry_json(
            filename, results, obs_name, var_name_web, vert_code, model.name, model_var
        )

    def _get_median_stats_point(self, data, use_weights) -> dict:

        stats_list: dict[str, list[float]] = {
            "rms": [],
            "R": [],
            "nmb": [],
            "mnmb": [],
            "fge": [],
        }

        station_list = data.station_name.data
        for station in station_list:
            d = data.sel(station_name=[station])
            arr = ColocatedData(d)
            stats = arr.calc_statistics(use_area_weights=use_weights)

            for key in stats_list.keys():
                stats_list[key].append(stats[key])

        median_stats = {}
        for key in stats_list.keys():
            median_stats[key] = np.nanmedian(np.array(stats_list[key]))

        return median_stats

    def _sort_coldata(
        self, coldata: list[ColocatedData]
    ) -> Tuple[dict[str, list[ColocatedData]], set[str]]:
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
            l = sorted(cols, key=lambda x: self._get_day(x.model_name))
            col_dict[var] = l

        return col_dict, set(var_list)

    def _get_day(self, model_name: str) -> int:
        return int(re.search(".*day([0-3]).*", model_name).group(1))
