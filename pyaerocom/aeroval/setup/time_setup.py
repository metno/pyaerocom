from pydantic import (
    BaseModel,
    Field,
)
from typing import Literal


class TimeSetup(BaseModel):
    """
    Time setup options

    Attributes
    ----------
    add_seasons : bool, default True
        if True, seasons will be ['all', 'DJF', 'MAM', 'JJA', 'SON'], if False, just ['all'].
    use_meteorological_seasons : bool, default False
        if True, then statistics are based on the meteorological definition of seasons. This is relevant
        for periods that are a single year. So if :attr:`add_seasons` is True, for a given year ['DJF'] will
        refer to data from Dec of the previous year (if available) and Jan/Feb of the same year, while if
        :attr:`use_meteorological_seasons` is False, it will be based on data from Jan/Feb and December
        of the same year. Similarly, and weather or not :attr:`add_seasons` is True,
        if :attr:`use_meteorological_seasons` is True, ['all'] (whole year) will refer to data from Dec of
        the previous year to Nov of the same year, while if False, it will refer to data from Jan to Dec
        of the same year.
    """

    DEFAULT_FREQS: Literal["monthly", "yearly"] = "monthly"
    SEASONS: list[str] = ["all", "DJF", "MAM", "JJA", "SON"]
    main_freq: str = "monthly"
    freqs: list[str] = ["monthly", "yearly"]
    periods: list[str] = Field(default_factory=list)
    add_seasons: bool = True
    use_meteorological_seasons: bool = False

    def get_seasons(self):
        """
        Get list of seasons to be analysed

        Returns :attr:`SEASONS` if :attr:`add_seasons` it True, else `[
        'all']` (only whole year).

        Returns
        -------
        list
            list of season strings for analysis

        """
        if self.add_seasons:
            return self.SEASONS
        return ["all"]

    def _get_all_period_strings(self):
        """
        Get list of all period strings for evaluation

        Returns
        -------
        list
            list of period / season strings
        """
        output = []
        for per in self.periods:
            for season in self.get_seasons():
                perstr = f"{per}-{season}"
                output.append(perstr)
        return output
