from pyaerocom.stats.types import StatsDict


class FilterDropStats:
    """
    Drops stats from a StatsDict which are in a provided list of values.
    """

    def __init__(self, stats_to_drop: list[str]):
        self.stats_to_drop = stats_to_drop

    def __call__(self, stats: StatsDict) -> StatsDict:
        for k in self.stats_to_drop:
            if k in stats.keys():
                del stats[k]

        return stats
