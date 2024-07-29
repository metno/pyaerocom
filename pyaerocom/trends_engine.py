import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from scipy.stats import kendalltau
from scipy.stats.mstats import theilslopes

from pyaerocom.trends_helpers import (
    _compute_trend_error,
    _get_yearly,
    _init_period_dates,
    _init_trends_result_dict,
    _start_season,
    _start_stop_period,
)


class TrendsEngine:
    """Trend computation engine (does not need to be instantiated)"""

    CMAP = matplotlib.colormaps["bwr"]
    NORM = Normalize(-10, 10)

    @staticmethod
    def compute_trend(
        data, ts_type, start_year, stop_year, min_num_yrs, season=None, slope_confidence=None
    ):
        """
        Compute trend

        Parameters
        ----------
        data : pd.Series
            input timeseries data
        ts_type : str
            frequency of input data (must be monthly or yearly)
        start_year : int or str
            start of period for trend
        stop_year : int or str
            end of period for trend
        min_num_yrs : int
            minimum number of years for trend computation
        season : str, optional
            which season to use, defaults to whole year (no season)
        slope_confidence : float, optional
            confidence of slope, between 0 and 1, defaults to 0.68.

        Returns
        -------
        dict
            trends results for input data

        """

        if season is None:
            season = "all"
        if slope_confidence is None:
            slope_confidence = 0.68
        if ts_type not in ["yearly", "monthly"]:
            raise ValueError(ts_type)

        result = _init_trends_result_dict(start_year)
        start_str = _start_season(season, start_year)
        stop_str = str(stop_year)
        data = data.loc[start_str:stop_str]

        result["period"] = f"{start_year}-{stop_year}"
        result["season"] = season
        if len(data) == 0:
            return result

        (start_date, stop_date, period_index, num_dates_period) = _init_period_dates(
            start_year, stop_year, season
        )

        if ts_type == "monthly":
            data = _get_yearly(data, season, start_year)

        result["data"] = data
        dates = data.index.values
        values = data.values

        # get period filter mask
        tmask = np.logical_and(dates >= start_date, dates <= stop_date)

        # apply period mask to jsdate vector and value vector
        dates_data = dates[tmask]

        # vector containing data values
        vals = values[tmask]

        valid = ~np.isnan(vals)

        # works only on not nan values
        dates_data = dates_data[valid]
        vals = vals[valid]

        num_dates_data = dates_data.astype("datetime64[Y]").astype(np.float64)

        # TODO: len(y) is number of years - 1 due to midseason averages
        result["n"] = len(vals)

        if not len(vals) >= min_num_yrs:
            return result

        result["y_mean"] = np.nanmean(vals)
        result["y_min"] = np.nanmin(vals)
        result["y_max"] = np.nanmax(vals)

        # Mann / Kendall test
        [tau, pval] = kendalltau(x=num_dates_data, y=vals)

        (slope, yoffs, slope_low, slope_up) = theilslopes(
            y=vals, x=num_dates_data, alpha=slope_confidence
        )

        # estimate error of slope at input confidence level
        slope_err = np.mean([abs(slope - slope_low), abs(slope - slope_up)])

        reg_data = slope * num_dates_data + yoffs
        reg_period = slope * num_dates_period + yoffs

        # value used for normalisation of slope to compute trend T
        # T=m / v0
        v0_data = reg_data[0]
        v0_period = reg_period[0]

        # Compute the mean residual value, which is used to estimate
        # the uncertainty in the normalisation value used to compute
        # trend
        mean_residual = np.mean(np.abs(vals - reg_data))

        # trend is slope normalised by first reference value.
        # 2 trends are computed, 1. the trend using the first value of
        # the regression line at the first available data year, 2. the
        # trend corresponding to the value corresponding to the first
        # year of the considered period.

        trend_data = slope / v0_data * 100
        trend_period = slope / v0_period * 100

        # Compute errors of normalisation values
        v0_err_data = mean_residual
        t0_data, tN_data = num_dates_data[0], num_dates_data[-1]
        t0_period = num_dates_period[0]

        # sanity check
        assert t0_data < tN_data
        assert t0_period <= t0_data

        dt_ratio = (t0_data - t0_period) / (tN_data - t0_data)

        v0_err_period = v0_err_data * (1 + dt_ratio)

        trend_data_err = _compute_trend_error(
            m=slope, m_err=slope_err, v0=v0_data, v0_err=v0_err_data
        )

        trend_period_err = _compute_trend_error(
            m=slope, m_err=slope_err, v0=v0_period, v0_err=v0_err_period
        )

        result["pval"] = pval
        result["m"] = slope
        result["m_err"] = slope_err
        result["yoffs"] = yoffs

        result["slp"] = trend_data
        result["slp_err"] = trend_data_err
        result["reg0"] = v0_data
        tp, tperr, v0p = None, None, None
        if v0_period > 0:
            tp = trend_period
            tperr = trend_period_err
            v0p = v0_period
        result[f"slp_{start_year}"] = tp
        result[f"slp_{start_year}_err"] = tperr
        result[f"reg0_{start_year}"] = v0p

        return result


class TrendPlotter:  # pragma: no cover
    def __init__(self):
        raise NotImplementedError(
            "consider removing or re-implementing (based on code from v0.10.0)"
        )

    def get_trend_color(self, trend_val):
        return self.CMAP(self.NORM(trend_val))

    def plot(self, season="all", period=None, ax=None):
        if season not in self.seasons_avail:
            raise AttributeError(f"No results available for season {season}")
        if period is None:
            if len(self.results[season]) > 1:
                raise ValueError(
                    f"Found multiple trends for different periods: {list(self.results[season])}. "
                    f"Please specify period..."
                )
            period = list(self.results[season])[0]
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=(18, 8))
        if self.has_daily:
            ax.plot(self.daily, "-", marker=".", label="daily", c="#d9d9d9")
        if self.has_monthly:
            ax.plot(self.monthly, label="monthly", c="#4d4d4d")
        ax.plot(self.get_yearly(season), " ok", label="yearly")
        if period in self.periods_avail:
            (s_data, s_period, td, tp, tdstr, tpstr) = self._get_trend_data(season, period)

            ax.plot(s_data, "-", color=self.get_trend_color(td), label="trend", lw=2)
            ax.plot(s_period, "--", color=self.get_trend_color(tp))
            ax.text(0.01, 0.95, tpstr, transform=ax.transAxes, fontsize=14)
            ax.text(0.01, 0.9, tdstr, transform=ax.transAxes, fontsize=14)

        ax.yaxis.grid(c="#d9d9d9", ls="-.")
        ylbl = self.var_name
        if self.var_name is not None and "units" in self.meta:
            u = str(self.meta["units"])
            if u not in ["", "1"]:
                ylbl += f" [{u}]"
        ax.set_ylabel(ylbl)
        tit = ""
        if self.meta["station_name"] is not None:
            tit += self.meta["station_name"]
            try:
                self.meta.load_dataset_info()
            except Exception:
                pass
            dsinfo = self.meta.dataset_str()
            if dsinfo is not None:
                tit += f"; {dsinfo}"
            tit += " - "
        tit += period
        ax.set_title(tit)
        ax.legend(loc=1)

        ax.set_xlim(_start_stop_period(period))

        return ax
