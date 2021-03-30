#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 17:12:54 2020

@author: jonasg
"""

from pathlib import Path
import os
import requests
import tarfile

from traceback import format_exc
from pyaerocom import const
from pyaerocom.exceptions import DataRetrievalError
from pyaerocom.io import (ReadAeronetSunV3, ReadAeronetSdaV3, ReadAeronetInvV3,
                          ReadEbas, ReadAirNow, ReadGhost)

class TestDataAccess(object):
    #: That's were the testdata can be downloaded from
    URL_TESTDATA = 'https://pyaerocom.met.no/pyaerocom-suppl/testdata-minimal.tar.gz'

    #: Directory where testdata will be downloaded into
    BASEDIR_DEFAULT = const.OUTPUTDIR

    #: Name of testdata directory
    TESTDATADIRNAME = 'testdata-minimal'

    #: Paths to be added to pya.const. All relative to :attr:`basedir`
    ADD_PATHS = {

        'MODELS'                        : 'modeldata',
        'OBSERVATIONS'                  : 'obsdata',
        'CONFIG'                        : 'config',
        'AeronetSunV3L2Subset.daily'    : 'obsdata/AeronetSunV3Lev2.daily/renamed',
        'AeronetSDAV3L2Subset.daily'    : 'obsdata/AeronetSDAV3Lev2.daily/renamed',
        'AeronetInvV3L2Subset.daily'    : 'obsdata/AeronetInvV3Lev2.daily/renamed',
        'EBASSubset'                    : 'obsdata/EBASMultiColumn',
        'AirNowSubset'                  : 'obsdata/AirNowSubset',
        'G.EEA.daily.Subset'            : 'obsdata/GHOST/data/EEA_AQ_eReporting/daily',
        'G.EEA.hourly.Subset'           : 'obsdata/GHOST/data/EEA_AQ_eReporting/hourly',
        'G.EBAS.daily.Subset'            : 'obsdata/GHOST/data/EBAS/daily',
        'G.EBAS.hourly.Subset'           : 'obsdata/GHOST/data/EBAS/hourly'


    }

    _UNGRIDDED_READERS = {
        'AeronetSunV3L2Subset.daily'  : ReadAeronetSunV3,
        'AeronetSDAV3L2Subset.daily'  : ReadAeronetSdaV3,
        'AeronetInvV3L2Subset.daily'  : ReadAeronetInvV3,
        'EBASSubset'                  : ReadEbas,
        'AirNowSubset'                : ReadAirNow,
        'G.EEA.daily.Subset'          : ReadGhost,
        'G.EEA.hourly.Subset'         : ReadGhost,
        'G.EBAS.daily.Subset'          : ReadGhost,
        'G.EBAS.hourly.Subset'         : ReadGhost,

    }

    def __init__(self, basedir=None):
        self._basedir = None
        if basedir is not None:
            self.basedir = basedir

    @property
    def basedir(self):
        """Directory into which testdata will be downloaded"""
        if self._basedir is not None:
            return Path(self._basedir)
        return Path(self.BASEDIR_DEFAULT)

    @basedir.setter
    def basedir(self, val):
        if not os.path.isdir(val):
            raise ValueError(f'Input basedir {val} is not a directory...')
        self._basedir = val

    @property
    def testdatadir(self):
        """Directory containing testdata"""
        return self.basedir.joinpath(self.TESTDATADIRNAME)

    def download(self, basedir=None):
        """
        Download testdata

        Parameters
        ----------
        basedir : str, optional
            directory in which testdata is supposed to be downloaded
        Returns
        -------
        bool
            True if download was successful, else False

        """
        if basedir is not None:
            self.basedir = basedir
        const.print_log.info(f'Downloading pyaerocom testdata into '
                             f'{self.basedir}')

        download_loc = self.basedir.joinpath(f'{self.TESTDATADIRNAME}.tar.gz')

        try:
            r = requests.get(self.URL_TESTDATA)
            with open(download_loc, 'wb') as f:
                f.write(r.content)

            with tarfile.open(download_loc, 'r:gz') as tar:
                tar.extractall(const.OUTPUTDIR)
                tar.close()
        except Exception:
            const.print_log.warning('Failed to download testdata. Traceback:\n{}'
                                    .format(format_exc()))
            return False
        finally:
            if download_loc.exists():
                os.remove(download_loc)
        return True

    def check_access(self, add_check_paths=None):
        """
        Method that checks if testdata can be accessed

        See also :func:`check_access_and_download_if_needed`.

        Parameters
        ----------
        add_check_paths : dict, optional
            additional paths used to validate testdata relative to testdata
            directory. Paths in :attr:`ADD_PATHS` will always be validated as
            they are required to be available in testdataset.

        Returns
        -------
        bool
            True if testdata is available and all relevant path locations
            could be validated, else False.

        """
        check_paths = {}
        check_paths.update(self.ADD_PATHS)
        if isinstance(add_check_paths, dict):
            check_paths.update(add_check_paths)

        datadir = self.testdatadir
        if not datadir.exists():
            return False

        for data_id, subdir in check_paths.items():
            if not datadir.joinpath(subdir).exists():
                return False
        return True

    def check_access_and_download_if_needed(self, add_check_paths=None):
        """
        Method that checks if testdata can be accessed and if not downloads it

        Parameters
        ----------
        add_check_paths : dict, optional
            additional paths used to validate testdata relative to testdata
            directory. Paths in :attr:`ADD_PATHS` will always be validated as
            they are required to be available in testdataset.

        Returns
        -------
        bool
            True if testdata is available and all relevant path locations
            could be validated, else False.

        """
        if not self.check_access(add_check_paths):
            try:
                if self.download() and self.check_access(add_check_paths):
                    return True
            except Exception as e:
                const.print_log.warning(f'Failed to access testdata: {e}')
            return False
        return True

    def init(self, add_check_paths=None):
        if not self.check_access_and_download_if_needed(add_check_paths):
            return False

        testdatadir = self.testdatadir
        for name, relpath in self.ADD_PATHS.items():
            ddir = str(testdatadir.joinpath(relpath))
            if name in self._UNGRIDDED_READERS:
                if name in const.OBSLOCS_UNGRIDDED and ddir == const.OBSLOCS_UNGRIDDED[name]:
                    const.print_log.info(f'dataset {name} is already registered')
                    continue
                reader = self._UNGRIDDED_READERS[name]
                try:
                    const.add_ungridded_obs(name, ddir,
                                            reader=reader,
                                            check_read=False)
                except Exception as e:
                    const.print_log.warning(
                        f'Failed to instantiate testdata since ungridded '
                        f'dataset {name} at {ddir} could not be registered: {e}')
                    return False
                const.print_log.info(
                    f'Adding ungridded dataset {name} located at {ddir}.'
                    f'Reader: {reader}')

            else:
                const.add_data_search_dir(ddir)
                const.print_log.info(f'Adding data search directory {ddir}.')
        return True

def initialise():
    td = TestDataAccess()
    if td.init():
        const.print_log.info(f'pyaerocom-testdata is ready to be used. The data '
                             f'is available at {td.testdatadir}')
    else:
        const.print_log.warning('Failed to initiate pyaerocom-testdata')
if __name__ == '__main__':
    initialise()