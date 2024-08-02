"""
Helper methods for computation of trends

Note
----
Most methods here are private and not to be used directly. Please use
:class:`TrendsEngine` instead.
"""

import numpy as np
import pandas as pd

SEASONS = {"spring": [3, 4, 5], "summer": [6, 7, 8], "autumn": [9, 10, 11], "winter": [12, 1, 2]}

SEASON_CODES = {"spring": "MAM", "summer": "JJA", "autumn": "SON", "winter": "DJF"}

MONTHS_CODES = {
    "MAM": "spring",
    "JJA": "summer",
    "SON": "autumn",
    "DJF": "winter",
    "all": "all",
}


def _init_trends_result_dict(start_yr):
    keys = [
        "pval",
        "m",
        "m_err",
        "n",
        "y_mean",
        "y_min",
        "y_max",
        "slp",
        "slp_err",
        "reg0",  # data specific
        f"slp_{start_yr}",  # period specific
        f"slp_{start_yr}_err",  # period specific
        f"reg0_{start_yr}",  # period specific
        "data",
    ]
    return dict.fromkeys(keys)


def _compute_trend_error(m, m_err, v0, v0_err):
    """Computes error of trend estimate using gaussian error propagation

    The (normalised) trend is computed as T = m / v0

    where m denotes the slope of a regression line and v0 denotes the
    normalistation value. This method computes the uncertainty of T (delta_T)
    using gaussian error propagation of uncertainties accompanying m and v0.

    Parameters
    ----------
    m : float
        slope in units of <U> yr-1 (where <U> denotes the unit of the data).
        (m -> "montant").
    m_err : float
        slope error (same unit as `m`)
    v0 : float
        normalisation value in units of <U>
    v0_err : float
        error of `v0` (same units as `v0`)

    Returns
    -------
    float
        error of T in computed using gaussian error propagation of trend
        formula in units of %/yr
    """

    delta_sl = m_err / v0
    delta_ref = m * v0_err / v0**2
    return np.sqrt(delta_sl**2 + delta_ref**2) * 100


def _get_season(mon):
    for seas, months in SEASONS.items():
        if mon in months:
            return seas


def _get_unique_seasons(idx):
    seasons = []
    mons = idx.month
    for mon in mons:
        seas = _get_season(mon)
        if seas not in seasons:
            seasons.append(seas)
    return seasons


def _get_season_from_months(months: str) -> str:
    if months not in MONTHS_CODES:
        raise ValueError(f"{months} is not a valid season")
    return MONTHS_CODES[months]


def _mid_season(seas, yr):
    if seas == "spring":
        return np.datetime64(f"{yr}-04-15")
    if seas == "summer":
        return np.datetime64(f"{yr}-07-15")
    if seas == "autumn":
        return np.datetime64(f"{yr}-10-15")
    if seas == "winter":
        return np.datetime64(f"{yr}-01-15")
    if seas == "all":
        return np.datetime64(f"{yr}-06-15")
    raise ValueError("Invalid input for season (seas):", seas)


def _start_season(seas, yr):
    if seas == "spring":
        return f"{yr}-03-01"
    if seas == "summer":
        return f"{yr}-06-01"
    if seas == "autumn":
        return f"{yr}-09-01"
    if seas == "winter":
        return f"{yr - 1}-12-01"
    if seas == "all":
        return f"{yr}-01-01"
    raise ValueError("Invalid input for season (seas):", seas)


def _end_season(seas, yr):
    if seas == "spring":
        return f"{yr}-06-01"
    if seas == "summer":
        return f"{yr}-09-01"
    if seas == "autumn":
        return f"{yr}-12-01"
    if seas == "winter":
        return f"{yr}-03-01"
    if seas == "all":
        return f"{yr}-01-01"
    raise ValueError("Invalid input for season (seas):", seas)


def _find_area(lat, lon, regions_dict=None):
    """Find area corresponding to input lat/lon coordinate

    Parameters
    ----------
    lat : float
        latitude
    lon : float
        longitude

    Returns
    -------
    str
        name of region
    """
    from pyaerocom.region import find_closest_region_coord

    reg = find_closest_region_coord(lat, lon)[0]
    if regions_dict is not None and reg in regions_dict:
        return regions_dict[reg]
    return reg


def _years_from_periodstr(period):
    """Convert period str to start / stop years

    Parameters
    ----------
    period : str
        period str, e.g. '1990-2010'

    Returns
    -------
    int
        start year
    int
        stop year
    """
    return [int(x) for x in period.split("-")]


def _start_stop_period(period):
    """Convert period str to start / stop dates

    Parameters
    ----------
    period : str
        period str, e.g. '1990-2010'

    Returns
    -------
    date
        start datetime
    date
        stop datetime
    """
    from datetime import date

    (
        y0,
        y1,
    ) = _years_from_periodstr(period)
    return (date(y0, 1, 1), date(y1, 12, 31))


def _seas_slice(yr, season):
    pass


def _get_yearly(data, seas, start_yr):
    dates = []
    values = []
    yrs = np.unique(data.index.year)
    for yr in yrs:
        if yr < start_yr:  # winter
            continue

        if seas == "all":  # yearly trends
            subset = data.loc[str(yr)]

        else:
            start = _start_season(seas, yr)
            stop = _end_season(seas, yr)
            subset = data.loc[start:stop]

        if len(subset) == 0:
            val = np.nan
        elif np.isnan(subset.values).all():
            val = np.nan

        elif seas == "all":
            d = subset.index
            valid_mask = ~np.isnan(subset.values)
            # seasons = _get_unique_seasons(d) # original (EMEP raport)
            seasons = _get_unique_seasons(d[valid_mask])

            if len(seasons) == 4:
                val = np.nanmean(subset.values)
            else:
                val = np.nan
        else:
            val = np.nanmean(subset.values)

        dates.append(_mid_season(seas, yr))
        values.append(val)

    return pd.Series(values, index=dates)


def _init_period_dates(start_year, stop_year, season):
    start_date = _mid_season(season, start_year)
    stop_date = _mid_season(season, stop_year)

    # datetime index covering whole input period (data may not be fully covered
    # in the whole period)
    period_index = pd.date_range(start=start_date, end=stop_date, freq=pd.DateOffset(years=1))

    num_dates_period = period_index.values.astype("datetime64[Y]").astype(np.float64)
    return (start_date, stop_date, period_index, num_dates_period)
