# isort:skip_file
import logging

logger = logging.getLogger(__name__)


def geopy_available():
    """Helper method that checks if geopy library is available

    Required for import of ReadAeolusL2aData

    Returns
    -------
    bool
        True, if library is available, else False
    """
    try:
        import geopy

        return True
    except ModuleNotFoundError:
        logger.warning("geopy library is not available. Aeolus data read not enabled")
    return False


def coda_available():
    """Helper method that checks if coda library is available

    Required for import of ReadAeolusL2aData and ReadSentinel5pL2Data

    Returns
    -------
    bool
        True, if library is available, else False
    """
    try:
        import coda

        return True
    except ModuleNotFoundError:
        logger.warning(
            "coda library is not available. Sentinel5P and Aeolus data read not enabled"
        )
    return False


from .aerocom_browser import AerocomBrowser
from .ebas_file_index import EbasFileIndex, EbasSQLRequest

# low level EBAS I/O routines
from .ebas_nasa_ames import EbasNasaAmesFile
from .fileconventions import FileConventionRead
from .read_aasetal import ReadAasEtal

# read base classes
from .readgridded import ReadGridded
from .readungriddedbase import ReadUngriddedBase
from .readungridded import ReadUngridded

# Pyaerocom reading interface classes
from .read_aeronet_invv2 import ReadAeronetInvV2
from .read_aeronet_invv3 import ReadAeronetInvV3
from .read_aeronet_sdav2 import ReadAeronetSdaV2
from .read_aeronet_sdav3 import ReadAeronetSdaV3
from .read_aeronet_sunv2 import ReadAeronetSunV2
from .read_aeronet_sunv3 import ReadAeronetSunV3
from .read_airnow import ReadAirNow
from .read_earlinet import ReadEarlinet
from .read_ebas import ReadEbas
from .read_eea_aqerep import ReadEEAAQEREP
from .read_eea_aqerep_v2 import ReadEEAAQEREP_V2
from .read_gaw import ReadGAW
from .read_ghost import ReadGhost
from .read_marcopolo import ReadMarcoPolo
from .read_mscw_ctm import ReadMscwCtm

if geopy_available() and coda_available():
    # the coda and geopy libraries are needed to read l2 data of the supported satellites
    # Aeolus and Sentinel5P
    from .read_aeolus_l2a_data import ReadL2Data
    from .read_sentinel5p_data import ReadL2Data

from . import helpers_units
