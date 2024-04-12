from typing import Callable, Optional

import numpy as np

# Type definition for a callable which filters (ie. excludes) data before calculating stats.
DataFilter = Callable[
    [np.array, np.array, Optional[np.array]], tuple[np.array, np.array, Optional[np.array]]
]

# Type definition for a callable which calculates a statistic.
StatisticsCalculator = Callable[[np.array, np.array, Optional[np.array]], np.float64]

# Type definition for a callable which filters out statistics from the resulting stats dictionary.
StatisticsFilter = Callable[[dict[str, np.float64]], dict[str, np.float64]]

# Type definition for a stats dictionary.
StatsDict = dict[str, np.float64]
