import logging
from pathlib import Path

import numpy as np
import xarray as xr

from pyaerocom import ColocatedData
from pyaerocom.aeroval._processing_base import DataImporter, ProcessingEngine
from pyaerocom.aeroval.coldatatojson_helpers import (
    _select_period_season_coldata,
    init_regions_web,
)
from pyaerocom.exceptions import DataCoverageError, UnknownRegion

logger = logging.getLogger(__name__)


SPECIES = dict(
    concno2=dict(UrRV=0.24, RV=200, alpha=0.2, freq="hourly"),
    conco3mda8=dict(UrRV=0.18, RV=120, alpha=0.79, freq="daily"),
    concpm10=dict(UrRV=0.28, RV=50, alpha=0.25, freq="daily"),
    concpm25=dict(UrRV=0.36, RV=25, alpha=0.5, freq="daily"),
)


class FairmodeEngine(ProcessingEngine, DataImporter):
    """
    Engine for processing of fairmode statistics
    """

    species = SPECIES

    def run(self, files: list[list[str | Path]], var_list: list) -> None:  # type:ignore[override]
        converted = []
        for file in files:
            logger.info(f"Processing: {file}")
            coldata = ColocatedData(data=file)
            self.process_coldata(coldata)
            converted.append(file)
        return converted

    def process_coldata(self, coldata: ColocatedData):
        # use_weights = self.cfg.statistics_opts.weighted_stats
        out_dirs = self.cfg.path_manager.get_json_output_dirs(True)
        forecast_days = self.cfg.statistics_opts.forecast_days
        periods = self.cfg.time_cfg.periods

        if "var_name_input" in coldata[0].metadata:
            obs_var = coldata[0].metadata["var_name_input"][0]
            model_var = coldata[0].metadata["var_name_input"][1]
        else:
            obs_var = model_var = "UNDEFINED"

        modelname = coldata[0].model_name.split("-")[2]
        vert_code = coldata[0].get_meta_item("vert_code")
        obs_name = coldata[0].obs_name

        mcfg = self.cfg.model_cfg.get_entry(modelname)

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

                    stats_list = self.fairmode_statistics(subset, obs_var)

                    out_dirs = self.cfg.path_manager.get_json_output_dirs(True)  # noqa: F841

                    results[f"{regname}"][f"{perstr}"] = stats_list

            self.save_fairmode_stats(
                results,
                obs_name,
                var_name_web,
                vert_code,
                modelname,
                model_var,
            )

    def save_fairmode_stats(
        self,
        fairmode_stats: dict,
        obs_name: str,
        var_name_web: str,
        vert_code: str,
        modelname: str,
        model_var: str,
    ):
        for regname in fairmode_stats:
            self.exp_output.add_fairmode_entry(
                fairmode_stats[regname],
                regname,
                obs_name,
                var_name_web,
                vert_code,
                modelname,
                model_var,
            )

    def fairmode_statistics(self, coldata: ColocatedData, var_name: str):
        return self._get_stats(coldata.data, var_name, False)

    def _get_stats(
        self, data: xr.DataArray, var_name: str, use_weights: bool
    ) -> dict[str, dict[str, float]]:
        stations = data.station_name.values

        obsvals = data.data[0]
        modvals = data.data[1]

        obsmean = np.nanmean(obsvals, axis=0)
        # modmean = np.nanmean(modvals, axis=0)
        obsstd = np.nanstd(obsvals, axis=0)
        modstd = np.nanstd(modvals, axis=0)

        diff = modvals - obsvals
        diffsquare = diff**2

        rms = np.sqrt(np.nanmean(diffsquare, axis=0))
        bias = np.nanmean(diff, axis=0)

        R = FairmodeEngine.pearson_R(obsvals, modvals)
        rmsu = self._RMSU(obsmean, obsstd, var_name)
        sign = self._fairmode_sign(modstd, obsstd, R)
        crms = self._crms(modstd, obsstd, R)
        mqi = self._mqi(rms, rmsu, beta=1)
        mb = self._mb(bias, rmsu, beta=1)

        # assert np.some(np.isclose(
        #     rmsu * mqi,
        #     np.sqrt((bias) ** 2 + (modstd - obsstd) ** 2 + (2 * obsstd * modstd * (1 - R))),
        #     rtol=1e-2,
        # )), "failed MQI check"

        assert len(rmsu) == len(stations)
        assert len(sign) == len(stations)
        assert len(crms) == len(stations)
        assert len(bias) == len(stations)
        assert len(rms) == len(stations)
        assert len(mqi) == len(stations)
        assert len(mb) == len(stations)

        stats_list: dict[str, dict[str, float]] = {
            stations[i]: dict(
                RMSU=rmsu[i],
                sign=sign[i],
                crms=crms[i],
                bias=bias[i],
                rms=rms[i],
                beta_mqi=mqi[i],
                bias_mb=mb[i],
                **SPECIES[var_name],
            )
            for i in range(len(stations))
        }

        return stats_list

    @staticmethod
    def pearson_R(x: np.ndarray, y: np.ndarray) -> np.ndarray:
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

    def _RMSU(self, mean: float, std: float, spec: str) -> float:
        """RMSU is the Root Mean Squared Uncertainity associated with the uncertainity of the observations, U(O_i)."""

        if spec not in SPECIES:
            raise ValueError(f"Unsupported {spec=}")

        UrRV = SPECIES[spec]["UrRV"]
        RV = SPECIES[spec]["RV"]
        alpha = SPECIES[spec]["alpha"]

        in_sqrt = (1 - alpha**2) * (mean**2 + std**2) + alpha**2 * RV**2

        return UrRV * np.sqrt(in_sqrt)

    def _fairmode_sign(self, mod_std: float, obs_std: float, R: float) -> float:
        a = np.where(
            np.logical_or(obs_std <= 0, R >= 1),
            1,
            np.abs(mod_std - obs_std) / (obs_std * np.sqrt(2 * (1 - R))),
        )
        return np.where(a >= 1, 1, -1)
        # if obs_std <= 0 or R >= 1:  # guard aginst sqrt(<0) or div0 errors
        #     return 1
        # a = np.abs(mod_std - obs_std) / (obs_std * np.sqrt(2 * (1 - R)))
        # return 1 if a >= 1 else -1

    def _crms(self, mod_std: float, obs_std: float, R: float) -> float:
        """Returns the Centered Root Mean Squared Error"""
        return np.sqrt(mod_std**2 + obs_std**2 - 2 * mod_std * obs_std * R)

    def _mqi(self, rms: float, rmsu: float, *, beta: float) -> float:
        """Model Quality Indicator (MQI). Pass beta=1 for `beta MQI`"""
        return rms / (rmsu * beta)

    def _mb(self, bias: float, rmsu: float, *, beta: float) -> float:
        """Model Bias(MB). Pass beta=1 for `beta MB`"""
        return bias / (rmsu * beta)
