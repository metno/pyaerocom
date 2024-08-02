from collections.abc import Callable

import numpy as np

# Type definition for a callable which filters (ie. excludes) data before calculating stats.
DataFilter = Callable[[np.ndarray, np.ndarray, np.ndarray | None], np.ndarray]

# Type definition for a callable which calculates a statistic.
StatisticsCalculator = Callable[[np.ndarray, np.ndarray, np.ndarray | None], np.float64]

# Type definition for a stats dictionary.
StatsDict = dict[str, np.float64]

# Type definition for a callable which filters out statistics from the resulting stats dictionary.
StatisticsFilter = Callable[[StatsDict], StatsDict]
