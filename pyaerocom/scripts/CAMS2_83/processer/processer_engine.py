from datetime import datetime
from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
from pandas import Timestamp, date_range
from pyaerocom import ColocatedData, colocateddata, const
from pyaerocom.aeroval._processing_base import ProcessingEngine


class CAMS2_83_Engine(ProcessingEngine):
    def run(self, files: list[list[str]] | list[list[Path]]) -> None:
        coldata = []
        print(files)
        for file in files:
            const.print_log.info(f"Processing: {file}")

            coldata.append(ColocatedData(file))

        self.process_coldata(coldata)

    def process_coldata(self, coldata: list[ColocatedData]) -> None:
        use_weights = self.cfg.statistics_opts.weighted_stats

        hourrange = list(range(24 * 1))

        stats_list = {
            "rms": [],
            "R": [],
            # "R_spearman": [],
            # "R_kendall": [],
            "nmb": [],
            "mnmb": [],
            "fge": [],
        }

        print(len(coldata))
        for hour in hourrange:
            leap = hour // 24
            h = hour % 24
            col = coldata[leap]
            time = col.time.data

            time_to_use = []
            for t in time:
                if Timestamp(t).hour == h:
                    time_to_use.append(t)

            data = col.data.sel(time=time_to_use)

            stats = self._get_median_stats_point(data, use_weights)

            for key in stats_list.keys():
                stats_list[key].append(stats[key])

        plt.plot(stats_list["rms"])
        plt.xlabel("Forecast Time [h]")
        plt.ylabel("RMSE")
        plt.title("Weird Plot for JJA2021")
        plt.savefig(
            "/lustre/storeB/project/fou/kl/emep/People/danielh/projects/pyaerocom/CAMS2_83_Processer/rms_JJA2021.png"
        )

        plt.clf()

        plt.plot(stats_list["R"])
        plt.xlabel("Forecast Time [h]")
        plt.ylabel("R")
        plt.title("Weird Plot for JJA2021")
        plt.savefig(
            "/lustre/storeB/project/fou/kl/emep/People/danielh/projects/pyaerocom/CAMS2_83_Processer/R_JJA2021.png"
        )
        plt.clf()

        plt.plot(stats_list["fge"])
        plt.xlabel("Forecast Time [h]")
        plt.ylabel("FGE")
        plt.title("Weird Plot for JJA2021")
        plt.savefig(
            "/lustre/storeB/project/fou/kl/emep/People/danielh/projects/pyaerocom/CAMS2_83_Processer/fge_JJA2021.png"
        )
        plt.clf()

        plt.plot(stats_list["mnmb"])
        plt.xlabel("Forecast Time [h]")
        plt.ylabel("MNMB")
        plt.title("Weird Plot for JJA2021")
        plt.savefig(
            "/lustre/storeB/project/fou/kl/emep/People/danielh/projects/pyaerocom/CAMS2_83_Processer/MNMB_JJA2021.png"
        )

    def _get_median_stats_point(self, data, use_weights) -> dict:

        stats_list = {
            "rms": [],
            "R": [],
            # "R_spearman": [],
            # "R_kendall": [],
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

        print(median_stats)
        return median_stats
