#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 09:06:06 2018

@author: jonasg
"""
import re
import os
import fnmatch
from pyaerocom import const, logger
from pyaerocom._lowlevel_helpers import BrowseDict
from pyaerocom.exceptions import DataSearchError

class AerocomBrowser(BrowseDict):
    """Interface for browsing all Aerocom data direcories

    Note
    ----
    Use :func:`browse` to find directories matching a
    certain search pattern.
    The class methods :func:`find_matches` and :func:`find_dir` both use
    :func:`browse`, the only difference is, that the :func:`find_matches` adds
    the search result (a list with strings) to

    """
    def _browse(self, name_or_pattern, ignorecase=True, return_if_match=True):
        """Search all Aerocom data directories that match input name or pattern

        Note
        ----
        Please do not use this function but either
        Parameters
        ----------
        name_or_pattern : str
            name or pattern of data (can be model or obs data)
        ignorecase : bool
            if True, upper / lower case is ignored
        return_if_match : bool
            if True, then the data directory is returned as string, if it can
            be found, else, only a list is returned that contains all
            matches. The latter takes longer since the whole database is
            searched.

        Returns
        -------
        :obj:`str` or :obj:`list`
            Data directory (str, if ``return_if_match`` is True) or list
            containing valid Aerocom names (which can then be used to
            retrieve the paths)

        Raises
        ------
        DataSearchError
            if no match or no unique match can be found
        """
        pattern = fnmatch.translate(name_or_pattern)
        _candidates = []
        _msgs = []
        _warnings = []

        for obs_id, obs_path in const.OBSLOCS_UNGRIDDED.items():
            if ignorecase:
                match = name_or_pattern.lower() == obs_id.lower()
            else:
                match = name_or_pattern == obs_id
            if match:
                logger.info("Found match for search pattern in obs network "
                            "directories {}".format(obs_id))
                path = os.path.normpath(obs_path)
                if os.path.exists(path):
                    self[obs_id] = path
                    if return_if_match:
                        return path
            else:
                if ignorecase:
                    match = bool(re.search(pattern, obs_id, re.IGNORECASE))
                else:
                    match = bool(re.search(pattern, obs_id))
                if match:
                    path = os.path.normpath(obs_path)
                    if os.path.exists(path):
                        self[obs_id] = path
                        _candidates.append(obs_id)
                        if return_if_match:
                            return path

        for search_dir in const.DATA_SEARCH_DIRS:
            # get the directories
            if os.path.isdir(search_dir):
                #subdirs = listdir(search_dir)
                subdirs = [x for x in os.listdir(search_dir) if
                           os.path.isdir(os.path.join(search_dir, x))]
                for subdir in subdirs:
                    if ignorecase:
                        match = bool(re.search(pattern, subdir,re.IGNORECASE))
                    else:
                        match = bool(re.search(pattern, subdir))
                    if match:
                        _dir = os.path.normpath(os.path.join(search_dir, subdir))
                        _rnsubdir = os.path.join(_dir, "renamed")
                        if os.path.isdir(_rnsubdir):
                            logger.info("{} has subdir renamed. Using that one"
                                        .format(_dir))
                            _dir = _rnsubdir
                        if any([_dir in x for x in self.values()]):
                            # directory was already found before
                            continue
                        # append name of candidate ...
                        _candidates.append(subdir)
                        # ... and the corresponding data directory
                        self[subdir] = _dir

                        # now check if it is actually an exact match, if
                        # applicable
                        if return_if_match:

                            if ignorecase:
                                match = name_or_pattern.lower() == subdir.lower()
                            else:
                                match = name_or_pattern == subdir
                            if match:
                                logger.info("Found match for ID {}"
                                            .format(name_or_pattern))
                                if return_if_match:
                                    return _dir

            else:
                _msgs.append('directory %s does not exist\n'
                                 %search_dir)
        for msg in _msgs:
            logger.info(msg)

        for warning in _warnings:
            logger.warning(warning)

        if len(_candidates) == 0:
            raise DataSearchError('No matches could be found for search pattern '
                          '{}'.format(name_or_pattern))
        if return_if_match:
            if len(_candidates) == 1:
                logger.info("Found exactly one match for search pattern "
                            "{}: {}".format(name_or_pattern, _candidates[0]))
                return self[_candidates[0]]
            raise DataSearchError('Found multiple matches for search pattern {}. '
                          'Please choose from {}'.format(name_or_pattern,
                                              _candidates))
        return _candidates

    @property
    def dirs_found(self):
        """All directories that were found"""
        return list(self.values())

    @property
    def ids_found(self):
        """All data IDs that were found"""
        return list(self.keys())

    def find_data_dir(self, name_or_pattern, ignorecase=True):
        """Find match of input name or pattern in Aerocom database

        Parameters
        ----------
        name_or_pattern : str
            name or pattern of data (can be model or obs data)
        ignorecase : bool
            if True, upper / lower case is ignored

        Returns
        -------
        str
            data directory of match

        Raises
        ------
        DataSearchError
            if no matches or no unique match can be found
        """
        if name_or_pattern in self:
            logger.info('{} found in instance of AerocomBrowser'.format(name_or_pattern))
            return self[name_or_pattern]
        logger.info('Searching database for {}'.format(name_or_pattern))
        return self._browse(name_or_pattern, ignorecase=ignorecase,
                            return_if_match=True) #returns list

    def find_matches(self, name_or_pattern, ignorecase=True):
        """Search all Aerocom data directories that match input name or pattern

        Parameters
        ----------
        name_or_pattern : str
            name or pattern of data (can be model or obs data)
        ignorecase : bool
            if True, upper / lower case is ignored

        Returns
        -------
        list
            list of names that match the pattern (corresponding paths can be
            accessed from this class instance)

        Raises
        ------
        DataSearchError
            if no matches can be found
        """
        return self._browse(name_or_pattern, ignorecase=ignorecase,
                            return_if_match=False) #returns list

if __name__ == "__main__":
    browser = AerocomBrowser()
    dd = browser.find_data_dir('TM5_AP3-CTRL2016*')
    ea = browser.find_data_dir('Earli*')
    ea1 = browser.find_matches('Earlinet')

    print(ea)
    print(ea1)
# =============================================================================
#     try:
#         data_dir = browser.find_data_dir('*Cam5.3-Oslo*')
#     except DataSearchError as e:
#         print(repr(e))
#
#
#
#     matches = browser.find_matches('*Cam5.3-Oslo*')
#
#     for match in matches:
#         print('{}: {}'.format(match, browser[match]))
#
#     data_dir_earlinet = browser.find_data_dir('EARLIN*')
#
#     data_dir_earlinet = browser.find_data_dir('EARLIN*')
#
#     browser.find_data_dir('Earlinet')
#
#
#
#
# =============================================================================
