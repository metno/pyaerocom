from pydantic import (
    BaseModel,
    ConfigDict,
    NonNegativeInt,
    PositiveInt,
)

from pyaerocom.aeroval.json_utils import set_float_serialization_precision


class StatisticsSetup(BaseModel, extra="allow"):
    """
    Setup options for statistical calculations

    Attributes
    ----------
    weighted_stats : bool
        if True, statistics are calculated using area weights,
        this is only relevant for gridded / gridded evaluations.
    annual_stats_constrained : bool
        if True, then only sites are considered that satisfy a potentially
        specified annual resampling constraint (see
        :attr:`pyaerocom.colocation.ColocationSetup.min_num_obs`). E.g.

        lets say you want to calculate statistics (bias,
        correlation, etc.) for monthly model / obs data for a given site and
        year. Lets further say, that there are only 8 valid months of data, and
        4 months are missing, so statistics will be calculated for that year
        based on 8 vs. 8 values. Now if
        :attr:`pyaerocom.colocation.ColocationSetup.min_num_obs` is
        specified in way that requires e.g. at least 9 valid months to
        represent the whole year, then this station will not be considered in
        case `annual_stats_constrained` is True, else it will. Defaults to
        False.
    stats_tseries_base_freq : str, optional
        The statistics Time Series display in AeroVal (under Overall Evaluation)
        is computed in intervals of a certain frequency, which is specified
        via :attr:`TimeSetup.main_freq` (defaults to monthly). That is,
        monthly colocated data is used as a basis to compute the statistics
        for each month (e.g. if you have 10 sites, then statistics will be
        computed based on 10 monthly values for each month of the timeseries,
        1 value for each site). `stats_tseries_base_freq` may be specified in
        case a higher resolution is supposed to be used as a basis to compute
        the timeseries in the resolution specified by
        :attr:`TimeSetup.main_freq` (e.g. if daily is specified here, then for
        the above example 310 values would be used - 31 for each site - to
        compute the statistics for a given month (in this case, a month with 31
        days, obviously).
    drop_stats: tuple, optional
        tuple of strings with names of statistics (as determined by keys in
        aeroval.glob_defaults.py's statistics_defaults) to not compute. For example,
        setting drop_stats = ("mb", "mab"), results in json files in hm/ts with
        entries which do not contain the mean bias and mean absolute bias,
        but the other statistics are preserved.
    stats_decimals: int, optional
        If provided, overwrites the decimals key in glod_defaults for the statistics, which has a default of 3.
        Setting this higher of lower changes the number of decimals shown on the Aeroval webpage.
    round_floats_precision: int, optional
        Sets the precision argument for the function `pyaerocom.aaeroval.json_utils:set_float_serialization_precision`


    Parameters
    ----------
    kwargs
        any of the supported attributes, e.g.
        `StatisticsSetup(annual_stats_constrained=True)`

    """

    # Pydantic ConfigDict
    model_config = ConfigDict(protected_namespaces=())
    # StatisticsSetup attributes
    MIN_NUM: PositiveInt = 1
    weighted_stats: bool = True
    annual_stats_constrained: bool = False

    # Trends config
    add_trends: bool = False  # Adding trend calculations, only trends over the average time series over stations in a region
    avg_over_trends: bool = (
        False  # Adds calculation of avg over trends of time series of stations in region
    )
    obs_min_yrs: NonNegativeInt = 0  # Removes stations with less than this number of years of valid data (a year with data points in all four seasons) Should in most cases be the same as stats_min_yrs
    stats_min_yrs: PositiveInt = obs_min_yrs  # Calculates trends if number of valid years are equal or more than this. Should in most cases be the same as obs_min_yrs
    sequential_yrs: bool = False  # Whether or not the min_yrs should be sequential

    stats_tseries_base_freq: str | None = None
    forecast_evaluation: bool = False
    forecast_days: PositiveInt = 4
    use_fairmode: bool = False
    use_diurnal: bool = False
    obs_only_stats: bool = False
    model_only_stats: bool = False
    drop_stats: tuple[str, ...] = ()
    stats_decimals: int | None = None
    round_floats_precision: int | None = None

    if round_floats_precision:
        set_float_serialization_precision(round_floats_precision)
