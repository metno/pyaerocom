from __future__ import annotations

import logging
from pathlib import Path
from reprlib import repr

import numpy as np
import xarray as xr

from pyaerocom import ColocatedData
from pyaerocom.aeroval._processing_base import ProcessingEngine
from pyaerocom.aeroval.coldatatojson_helpers import write_json

logger = logging.getLogger(__name__)


class CAMS2_83_Engine(ProcessingEngine):
    def run(self, files: list[list[str | Path]]) -> None:  # type:ignore[override]
        logger.info(f"Processing: {repr(files)}")
        coldata = [ColocatedData(file) for file in files]
        self.process_coldata(coldata)

    def process_coldata(self, coldata: list[ColocatedData]) -> None:
        use_weights = self.cfg.statistics_opts.weighted_stats
        stats_list: dict[str, list[float]] = dict(rms=[], R=[], nmb=[], mnmb=[], fge=[])
        for forecast_hour in range(24 * 1):
            leap, hour = divmod(forecast_hour, 24)
            ds = coldata[leap].data
            ds = ds.data.sel(time=(ds.time.dt.hour == hour))
            stats = self._get_median_stats_point(ds, use_weights)
            for key in stats_list:
                stats_list[key].append(stats[key])

        out_dirs = self.cfg.path_manager.get_json_output_dirs(True)
        model_name = coldata[0].model_name
        if "var_name_input" in coldata[0].metadata:
            model_var = coldata[0].metadata["var_name_input"][1]
        else:
            model_var = "UNDEFINED"
        path = Path(out_dirs["conf"]) / f"cams2-83_{model_name}-{model_var}.json"
        write_json(stats_list, path, ignore_nan=True)

    def _get_median_stats_point(self, data: xr.DataArray, use_weights: bool) -> dict[str, float]:

        stats_list: dict[str, list[float]] = dict(rms=[], R=[], nmb=[], mnmb=[], fge=[])
        for station, ds in data.groupby("station_name"):
            stats = ColocatedData(ds).calc_statistics(use_area_weights=use_weights)
            for key in stats_list.keys():
                stats_list[key].append(stats[key])

        stats = {key: np.nanmedian(value) for key, value in stats_list.items()}
        return stats
