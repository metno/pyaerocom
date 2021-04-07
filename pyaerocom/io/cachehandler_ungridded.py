#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Caching class for reading and writing of ungridded data Cache objects
"""
import glob, os, pickle

from pyaerocom import const
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.exceptions import (CacheReadError,
                                  CacheWriteError)

# TODO: Write data attribute list contains_vars in header of pickled file and
# check if variables match the request
class CacheHandlerUngridded(object):
    """Interface for reading and writing of cache files

    Cache filename mask is

    <dataset_to_read>_<var>.pkl

    e.g. EBASMC_scatc550aer.pkl

    Attributes
    ----------
    reader : ReadUngriddedBase
        reading class for dataset
    loaded_data : dict
        dictionary containing successfully loaded instances of single variable
        :class:`UngriddedData` objects (keys are variable names)
    """
    __version__ = '1.12'
    #: Cache file header keys that are checked (and required unchanged) when
    #: reading a cache file
    CACHE_HEAD_KEYS = ['pyaerocom_version',
                       'newest_file_in_read_dir',
                       'newest_file_date_in_read_dir',
                       'data_revision',
                       'reader_version',
                       'ungridded_data_version',
                       'cacher_version']

    def __init__(self, reader=None, cache_dir=None,
                 **kwargs):
        self._reader = None
        if reader is not None:
            self.reader = reader

        self.loaded_data = {}
        self._cache_dir = cache_dir

    @property
    def reader(self):
        """Instance of reader class"""
        if self._reader is None:
            raise AttributeError('No reader class assigned to cache object')
        return self._reader

    @reader.setter
    def reader(self, val):
        from pyaerocom.io import ReadUngriddedBase
        if not isinstance(val, ReadUngriddedBase):
            try:
                val = val.get_reader()
                if not isinstance(val, ReadUngriddedBase):
                    raise TypeError('Invalid input for reader')
            except Exception:
                raise TypeError('Invalid input for reader')
        self._reader = val
        self.loaded_data = {}

    @property
    def cache_dir(self):
        """Directory where cache data objects are stored"""
        if self._cache_dir is not None:
            return self._cache_dir
        return const.CACHEDIR

    @cache_dir.setter
    def cache_dir(self, val):
        if not isinstance(val, str) or not os.path.exists(val):
            raise FileNotFoundError('Input directory does not exist: {}'
                                    .format(val))
        self._cache_dir = val

    @property
    def dataset_to_read(self):
        """Data ID of the associated dataset"""
        return self.reader.dataset_to_read

    @property
    def src_data_dir(self):
        """Data source directory of the associated dataset

        Needed to check whether an existing cache file is outdated
        """
        return self.reader.DATASET_PATH

    def default_file_name(self, var_name):
        """File name of cache file


        Parameters
        ----------
        var_name : str
            name of variable to be cached.

        Returns
        -------
        str
            file name of pickle file
        """
        name = '_'.join([self.dataset_to_read, var_name])
        return name + '.pkl'

    def file_path(self, var_or_file_name, cache_dir=None):
        """File path of cache file

        Parameters
        ----------
        var_or_file_name : str
            name of output filename or variable that is supposed to be stored.
            Default usage is to provide variable and then
            :func:`default_file_name` is used. Can be None if
            input `data` contains only a single variable.
        cache_dir : str, optional
            output directory (default is pyaerocom cache dir accessed via
            :func:`cache_dir`).

        Returns
        -------
        str
            output file path
        """
        if not var_or_file_name.endswith('.pkl'):
            var_or_file_name = self.default_file_name(var_or_file_name)
        if cache_dir is None:
            cache_dir = self.cache_dir
        elif not os.path.exists(cache_dir):
            raise FileNotFoundError('Specified output directory does not exist:'
                                    '{}'.format(cache_dir))
        return os.path.join(cache_dir, var_or_file_name)

    def _check_pkl_head_vs_database(self, in_handle):

        current = self.cache_meta_info()

        head = pickle.load(in_handle)
        if not isinstance(head, dict):
            raise CacheReadError('Invalid cache file')
        for k, v in head.items():
            if not k in current:
                raise CacheReadError('Invalid cache header key: {}'.format(k))
            elif not v == current[k]:
                const.print_log.info('{} is outdated (value: {}). Current '
                                     'value: {}'.format(k, v, current[k]))
                return False
        return True

    def cache_meta_info(self):
        """Dictionary containing relevant caching meta-info"""
        try:
            newestp = max(glob.iglob(os.path.join(self.src_data_dir, '*')),
                         key=os.path.getctime)
            newest_date = os.path.getctime(newestp)
            newest = os.path.basename(newestp)

        except Exception:
            newest = None
            newest_date = None

        try:
            rev = self.reader.data_revision
            reader_ver = self.reader.__version__
        except AttributeError:
            rev = None
            reader_ver = None
        current = dict.fromkeys(self.CACHE_HEAD_KEYS)
        from pyaerocom import __version__

        current['pyaerocom_version'] = __version__
        current['newest_file_in_read_dir'] = newest
        current['newest_file_date_in_read_dir'] = newest_date
        current['data_revision'] = rev
        current['reader_version'] = reader_ver
        current['ungridded_data_version'] = UngriddedData.__version__
        current['cacher_version'] = self.__version__
        return current

    def check_and_load(self, var_or_file_name, force_use_outdated=False,
                       cache_dir=None):
        """Check if cache file exists and load

        Note
        ----
        If a cache file exists for this database, but cannot be loaded or is
        outdated against pyaerocom updates, then it will be removed (the latter
        only if :attr:`pyaerocom.const.RM_CACHE_OUTDATED` is True).

        Parameters
        ----------
        var_or_file_name : str
            name of output filename or variable that is supposed to be stored.
            Default usage is to provide variable and then
            :func:`default_file_name` is used. Can be None if
            input `data` contains only a single variable.ead
        force_use_outdated : bool
            if True, read existing cache file even if it is not up to date or
            pyaerocom version changed (not recommended to use)
        cache_dir : str, optional
            output directory (default is pyaerocom cache dir accessed via
            :func:`cache_dir`).

        Returns
        -------
        bool
            True, if cache file exists and could be successfully loaded, else
            False. Note: if import is successful, the corresponding data object
            (instance of :class:`pyaerocom.UngriddedData` can be accessed via
            :attr:`loaded_data'

        Raises
        ------
        TypeError
            if cached file is not an instance of :class:`pyaerocom.UngriddedData`
            class (which should not happen)
        """
        try:
            fp = self.file_path(var_or_file_name, cache_dir=cache_dir)
        except FileNotFoundError as e:
            const.logger.warning(repr(e))
            return False

        if not os.path.isfile(fp):
            const.logger.info('Cache file does not exist: {}'
                              .format(fp))
            return False

        delete_existing = const.RM_CACHE_OUTDATED if not force_use_outdated else False

        in_handle = open(fp, 'rb')
        if force_use_outdated:
            last_meta = pickle.load(in_handle)
            assert len(last_meta) == len(self.CACHE_HEAD_KEYS)
            ok = True
        else:
            try:
                ok = self._check_pkl_head_vs_database(in_handle)
            except Exception as e:
                ok = False
                delete_existing = True
                const.logger.exception('File error in cached data file {}. File will '
                                 'be removed and data reloaded'
                                 'Error: {}'.format(fp, repr(e)))
        if not ok:
            # TODO: Should we delete the cache file if it is outdated ???
            const.logger.info('Aborting reading cache file {}. Aerocom database '
                              'or pyaerocom version has changed compared to '
                              'cached version'
                              .format(fp))
            in_handle.close()
            if delete_existing: #something was wrong
                const.print_log.info('Deleting outdated cache file: {}'
                                     .format(fp))
                os.remove(fp)
            return False

        # everything is okay
        data = pickle.load(in_handle)
        if not isinstance(data, UngriddedData):
            raise TypeError('Unexpected data type stored in cache file, need '
                            'instance of UngriddedData, got {}'
                            .format(type(data)))

        self.loaded_data[var_or_file_name] = data
        const.logger.info('Successfully loaded cache file {}'
                          .format(fp))
        return True

    def delete_all_cache_files(self):
        """
        Deletes all pickled data objects in cache directory

        If not set differently, the cache directory is the pyaerocom default,
        accessible via :attr:`pyaerocom.const.CACHEDIR`.

        """
        for fp in glob.glob('{}/*.pkl'.format(self.cache_dir)):
            os.remove(fp)
            const.print_log.info('Deleted {}'.format(fp))

    def write(self, data, var_or_file_name=None, cache_dir=None):
        """Write single-variable instance of UngriddedData to cache

        Parameters
        ----------
        data : UngriddedData
            object containing the data (possibly containing multiple variables)
        var_or_file_name : str, optional
            name of output filename or variable that is supposed to be stored.
            Default usage is to provide variable and then
            :func:`default_file_name` is used. Can be None if
            input `data` contains only a single variable.
        cache_dir : str, optional
            output directory (default is pyaerocom cache dir accessed via
            :func:`cache_dir`).

        Returns
        -------
        str
            output file path
        """
        meta = self.cache_meta_info()

        if not isinstance(data, UngriddedData):
            raise TypeError('Invalid input, need instance of UngriddedData, '
                            'got {}'.format(type(data)))

        if not var_or_file_name.endswith('.pkl'):
            var_name = var_or_file_name
            if len(data.contains_datasets) > 1:
                raise CacheWriteError('Input UngriddedData object contains '
                                      'datasets: {}. Can only write single '
                                      'dataset objects'
                                      .format(data.contains_datasets))
            if var_name is None:
                if len(data.contains_vars) > 1:
                    raise CacheWriteError('Input UngriddedData object for {} contains '
                                          'more than one variable: {}. Please '
                                          'specify which variable should be '
                                          'cached'
                                          .format(self.reader.data_id,
                                                  data.contains_vars))
                var_name = data.contains_vars[0]

            elif not var_name in data.contains_vars:
                raise CacheWriteError('Cannot write cache file: variable {} does '
                                      'not exist in input UngriddedData object'
                                      .format(var_name))

            if len(data.contains_vars) > 1:
                data = data.extract_var(var_name)

        fp = self.file_path(var_or_file_name, cache_dir=cache_dir)
        const.logger.info('Writing cache file: {}'.format(fp))
        success = True
        # OutHandle = gzip.open(c__cache_file, 'wb') # takes too much time
        out_handle = open(fp, 'wb')

        try:
            # write cache header
            pickle.dump(meta, out_handle, pickle.HIGHEST_PROTOCOL)
            # write data
            pickle.dump(data, out_handle, pickle.HIGHEST_PROTOCOL)

        except Exception as e:
            from pyaerocom import print_log
            print_log.exception('Failed to write cache: {}'.format(repr(e)))
            success=False
        finally:
            out_handle.close()
            if not success:
                os.remove(fp)
        const.logger.info('Wrote: {}'.format(fp))
        return fp

    def __str__(self):
        return 'pyaerocom.CacheHandlerUngridded\nDefault cache dir: {}'.format(self.cache_dir)

if __name__ == "__main__":

    ch = CacheHandlerUngridded()
    print(ch)
