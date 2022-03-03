from pathlib import Path

import numpy as np
import pytest

from pyaerocom.io.read_aeronet_sdav2 import ReadAeronetSdaV2
from tests.conftest import TEST_RTOL, lustre_unavail


@lustre_unavail
def test_load_berlin_AeroSdaV2L2D():
    reader = ReadAeronetSdaV2()
    files = reader.find_in_file_list("*Berlin*")
    assert len(files) == 1
    assert Path(files[0]).name == "920801_180519_Berlin_FUB.ONEILL_20"

    test_vars = ["od870aer", "ang4487aer", "od550aer", "od550gt1aer", "od550lt1aer"]

    data = reader.read_file(files[0], vars_to_retrieve=test_vars)

    assert all(x in data for x in test_vars)

    # more than 100 timestamps
    assert all(len(data[x]) > 100 for x in test_vars)

    assert isinstance(data["dtime"][0], np.datetime64)
    assert data["dtime"][0] == np.datetime64("2014-07-06T00:00:00")

    means = [data[var].mean() for var in test_vars]
    desired = [
        0.0671392659574468,
        1.5027900015754372,
        0.1338938495016503,
        0.02333982521802314,
        0.11055405137562464,
    ]
    assert means == pytest.approx(desired, rel=TEST_RTOL)
