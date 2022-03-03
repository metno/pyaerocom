"""
Interface for reading EEA AqERep files (formerly known as Airbase data).
"""

from pyaerocom import const
from pyaerocom.io.read_eea_aqerep_base import ReadEEAAQEREPBase


class ReadEEAAQEREP(ReadEEAAQEREPBase):
    """Class for reading EEA AQErep data

    Extended class derived from  low-level base class :class: ReadUngriddedBase
    that contains the main functionality.
    """

    #: Name of the dataset (OBS_ID)
    DATA_ID = const.EEA_NRT_NAME  # change this since we added more vars?

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [DATA_ID]

    #: Eionet offers 2 data revisions
    #: E2a (near real time) and E1a (quality controlled)
    #: this class reads the E2a data for now.
    # But by changing the base path
    # and this constant, it can also read the E1a data set
    DATA_PRODUCT = "E2a"
