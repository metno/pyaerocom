################################################################
# read/__init__.py
#
# init for data reading
#
# this file is part of the aerocom_pt package
#
#################################################################
# Created 20171030 by Jan Griesfeller for Met Norway
#
# Last changed: See git log
#################################################################

#Copyright (C) 2017 met.no
#Contact information:
#Norwegian Meteorological Institute
#Box 43 Blindern
#0313 OSLO
#NORWAY
#E-mail: jan.griesfeller@met.no
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#MA 02110-1301, USA

# =============================================================================
# from .read_aeronet_sdav2 import ReadAeronetSDAV2
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
        from logging import getLogger
        logger = getLogger('pyaerocom')
        logger.warning('geopy library is not available. Aeolus data read not '
                       'enabled')
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
        from logging import getLogger
        logger = getLogger('pyaerocom')
        logger.warning('coda library is not available. Sentinel5P and Aeolus data read not enabled')
    return False

from .aerocom_browser import AerocomBrowser
from .readungriddedbase import ReadUngriddedBase

# low level EBAS I/O routines
from .ebas_nasa_ames import EbasNasaAmesFile
from .ebas_file_index import EbasSQLRequest, EbasFileIndex

# Pyaerocom reading interface classes
from .read_aeronet_invv2 import ReadAeronetInvV2
from .read_aeronet_invv3 import ReadAeronetInvV3
from .read_aeronet_sdav2 import ReadAeronetSdaV2
from .read_aeronet_sdav3 import ReadAeronetSdaV3
from .read_aeronet_sunv2 import ReadAeronetSunV2
from .read_aeronet_sunv3 import ReadAeronetSunV3
from .read_earlinet import ReadEarlinet
from .read_ebas import ReadEbas
from .read_gaw import ReadGAW
from .read_aasetal import ReadAasEtal
from .read_ghost import ReadGhost
from .read_airnow import ReadAirNow
from .read_marcopolo import ReadMarcoPolo
from .read_eea_aqerep import ReadEEAAQEREP
from .read_eea_aqerep_v2 import ReadEEAAQEREP_V2

from .readgridded import ReadGridded
from .read_mscw_ctm import ReadMscwCtm
from .readungridded import ReadUngridded
from .fileconventions import FileConventionRead

if geopy_available() and coda_available():
    # the coda and geopy libraries are needed to read l2 data of the supported satellites
    # Aeolus and Sentinel5P
    from .read_aeolus_l2a_data import ReadL2Data
    from .read_sentinel5p_data import ReadL2Data

from . import testfiles
from . import helpers_units
