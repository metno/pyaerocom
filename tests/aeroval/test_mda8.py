import logging

import pytest

from pyaerocom.aeroval.mda8 import calc_mda8
from pyaerocom.colocation.colocated_data import ColocatedData
from tests.fixtures.collocated_data import EXAMPLE_FILE

logger = logging.getLogger(__name__)


def test_calc_mda8():
    coldata = ColocatedData(EXAMPLE_FILE)

    coldata2 = calc_mda8(coldata, "od550aer", "od550aer2")

    pass
