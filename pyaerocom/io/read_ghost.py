# -*- coding: utf-8 -*-
# this file is part of the pyaerocom package
# Copyright (C) 2018 met.no
# Contact information:
# Norwegian Meteorological Institute
# Box 43 Blindern
# 0313 OSLO
# NORWAY
# Author: Jonas Gliss
# E-mail: jonasg@met.no
# License: https://github.com/metno/pyaerocom/blob/master/LICENSE
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA
import cf_units
import glob
import os
import numpy as np
import pandas as pd
import xarray as xr

import pyaerocom as pya
from pyaerocom import const
from pyaerocom.exceptions import DataSourceError
from pyaerocom.mathutils import vmrx_to_concx
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.io.ghost_meta_keys import GHOST_META_KEYS
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.helpers import varlist_aerocom
from pyaerocom.tstype import TsType
from pyaerocom.molmasses import get_molmass

def _vmr_to_conc_ghost_stats(data, mconcvar, vmrvar):
    """
    Convert VMR data to mass concentration for list of GHOST StationData objects

    Note
    ----
    This is a private function used in :class:`ReadGhost` and is not supposed
    to be used directly.

    Parameters
    ----------
    data : list
        list of :class:`StationData` objects containing VMR data (e.g. vmrno2)
    mconcvar : str
        Name of mass concentration variable (e.g. concno2)
    vmrvar : str
        Name of VMR variable (e.g. vmrno2)

    Returns
    -------
    data : list
        list of modified :class:`StationData` objects that include computed
        mass concentrations in addition to VMR data.

    """
    for stat in data:
        vmrdata = stat[vmrvar]
        meta = stat['meta']
        p = meta['network_provided_volume_standard_pressure']
        T = meta['network_provided_volume_standard_temperature']
        mmol_var = get_molmass(vmrvar)
        unit_var = meta['var_info'][vmrvar]['units']
        to_unit = const.VARS[mconcvar].units
        conc = vmrx_to_concx(vmrdata,
                             p_pascal=p,
                             T_kelvin=T,
                             mmol_var=mmol_var,
                             vmr_unit=unit_var,
                             to_unit=to_unit)
        stat[mconcvar] = conc
        vi = {}
        vi.update(meta['var_info'][vmrvar])
        vi['computed'] = True
        vi['units'] = to_unit
        meta['var_info'][mconcvar] = vi

    return data

class ReadGhost(ReadUngriddedBase):
    """Reading interface for GHOST data

    This reader supports both reading of provided EEA and EBAS datasets.
    It may not have implemented all variables provided in the input data, you
    can check all provided variables via :attr:`PROVIDES_VARIABLES`. If you
    find one variable missing in this reading routine, you can register it
    yourself in the class header (see :attr:`VARNAMES_DATA` below) from a
    forked pyaerocom repo and send a pull request, or you can contact us about
    it.

    Note
    ----
    This class inherits from the metaclass template `ReadUngriddedBase`.
    Please have a look at that and make sure you understand the idea behind
    it.

    Information about data quality (Email from D. Bowdalo 2.3.2020)
    --------------------------------------------------------------
    Inside is hourly and daily resolution data for O3, NO, NO2, CO, SO2, PM2.5
    and PM10 for 2018 and 2019.

    The data is a mesh of the EEA E1a (validated)/E2a (UTD) data streams.
    Almost all of the 2018 data is from the E1a stream and all of the 2019 is
    from the E2a stream.
    These can be entirely separated out using the QA code 4 ('Not Maximum
    Data Quality Level’), for which all data from the E2a stream is flagged
    with.

    Additionally I put the QA code 5 ('Preliminary Data’) in my list of
    default QA codes to screen by Jonas, but you may wish to remove this as a
    lot of the 2019 E2a data is flagged by EEA as preliminary, and therefore
    flagged by my processing accordingly.
    """

    #: version of the reader
    __version__ = '0.0.13'

    _FILEMASK = '*.nc'

    #: Default data ID
    DATA_ID = 'GHOST.EEA.daily'


    #: IDs of supported datasets
    SUPPORTED_DATASETS = ['GHOST.EEA.monthly',
                          'GHOST.EEA.hourly',
                          'GHOST.EEA.daily',
                          'GHOST.EBAS.monthly',
                          'GHOST.EBAS.hourly',
                          'GHOST.EBAS.daily',]

    #: sampling frequencies of supported datasets
    TS_TYPES = {'GHOST.EEA.monthly'   : 'monthly',
                'GHOST.EEA.hourly'    : 'hourly',
                'GHOST.EEA.daily'     : 'daily',
                'GHOST.EBAS.monthly'  : 'monthly',
                'GHOST.EBAS.hourly'   : 'hourly',
                'GHOST.EBAS.daily'    : 'daily'}

    #: List of GHOST metadata keys
    META_KEYS = GHOST_META_KEYS

    #: Names of flag variables in GHOST NetCDF files
    FLAG_VARS = ['flag', 'qa']

    #:
    FLAG_DIMNAMES = {'qa'   : 'N_qa_codes',
                     'flag' : 'N_flag_codes'}

    #: dictionary mapping GHOST variable names to AeroCom variable names
    VARNAMES_DATA = {'concpm10'  : 'pm10',
                     'concpm10al': 'pm10al',
                     'concpm10as': 'pm10as',
                     'concpm25'  : 'pm2p5',
                     'concpm1'   : 'pm1',
                     'conccl'    : 'sconccl',
                     'concso4'   : 'sconcso4',
                     'vmrco'     : 'sconcco',
                     'vmrno'     : 'sconcno',
                     'vmrno2'    : 'sconcno2',
                     'vmro3'     : 'sconco3',
                     'vmrso2'    : 'sconcso2',
                     'concno3'   : 'sconcno3',
                     'concnh4'   : 'sconcnh4'
                     }

    AUX_REQUIRES = {'concco'    :  ['vmrco'],
                    'concno'    :  ['vmrno'],
                    'concno2'   :  ['vmrno2'],
                    'conco3'    :  ['vmro3'],
                    'concso2'   :  ['vmrso2']}

    AUX_FUNS = {
        'concco'    : _vmr_to_conc_ghost_stats,
        'concno'    : _vmr_to_conc_ghost_stats,
        'concno2'   : _vmr_to_conc_ghost_stats,
        'conco3'    : _vmr_to_conc_ghost_stats,
        'concso2'   : _vmr_to_conc_ghost_stats}

    CONVERT_UNITS_META = {
        'network_provided_volume_standard_pressure' : 'Pa',
    }

    # This is the default list of flags that mark bad / invalid data, as
    # provided by Dene: [0, 1, 2, 3, 6, 20, 21, 22, 72, 75, 82, 83, 90, 91,
    #92, 105 (removed), 110, 111, 112, 113, 115, 132, 133]

    #: Default flags used to invalidate data points (these may be either from
    #: provided flag or qa variable, or both, currently only from qa variable)
    DEFAULT_FLAGS_INVALID = {'qa' : np.asarray([[0, 1, 2, 3, 6, 20, 21, 22, 72,
                                                 75, 82, 83, 90, 91, 92, 110,
                                                 111, 112, 113, 115, 131, 132,
                                                 133]]),
                             'flag' : None}

    @property
    def PROVIDES_VARIABLES(self):
        """
        list of variable names that can be retrieved through this interface
        """
        return list(self.VARNAMES_DATA) + list(self.AUX_FUNS)

    @property
    def DEFAULT_VARS(self):
        """
        list of default variables to retrieve
        """
        return self.PROVIDES_VARIABLES

    @property
    def var_names_data_inv(self):
        """
        Inverted version of dictionary :attr:`VARNAMES_DATA`
        """
        try:
            return self._var_names_inv
        except AttributeError:
            self._var_names_inv ={v: k for k, v in self.VARNAMES_DATA.items()}
            return self._var_names_inv

    @property
    def TS_TYPE(self):
        """
        Default implementation of string for temporal resolution
        """
        try:
            return self.TS_TYPES[self.data_id]
        except KeyError:
            return self._ts_type_from_DATASET_PATH()

    def get_file_list(self, vars_to_read=None, pattern=None):
        """
        Retrieve a list of files to read based on input variable names

        Parameters
        ----------
        vars_to_read : str, optional
            list of variables to be imported. If None, use The default is None.
        pattern : TYPE, optional
            DESCRIPTION. The default is None.

        Raises
        ------
        ValueError
            If no files can be found for any of the input variables.

        Returns
        -------
        list
            list with file paths

        """
        if vars_to_read is None:
            vars_to_read =  self.PROVIDES_VARIABLES
        elif isinstance(vars_to_read, str):
            vars_to_read = [vars_to_read]

        if pattern is None:
            pattern = self._FILEMASK

        files = []
        for var in vars_to_read:
            if var in self.VARNAMES_DATA:
                # make sure to check for right variable, user may use either
                # AeroCom variable name or GHOST variable name
                var = self.VARNAMES_DATA[var]

            _dir = os.path.join(self.DATASET_PATH, var)
            _files = glob.glob('{}/{}'.format(_dir, pattern))
            if len(_files) == 0:
                raise DataSourceError(f'Could not find any data files for {var}')
            files.extend(_files)

        self.files = sorted(files)
        return self.files

    def get_meta_filename(self, filename):
        """Extract metadata from data filename

        Parameters
        ----------
        filename : str
            data file path or name.

        Returns
        -------
        dict
            dictionary containing var_name, start and stop, and eventually
            also frequency (ts_type)
        """
        var, time = os.path.basename(filename).split('.nc')[0].split('_')

        per = pd.Period(freq='M', year=int(time[:4]), month=int(time[-2:]))
        return dict(var_name=var, start=per.start_time,
                    stop=per.end_time)

    @staticmethod
    def _eval_flags_slice(slc, invalid_flags):
        """
        Compare a flag slice of a data point with input flags marking invalid

        Returns
        -------
        bool
            True, if data point is valid, else False
        """
        if len(np.intersect1d(slc, invalid_flags)) == 0:
            return True
        return False

    def _ts_type_from_DATASET_PATH(self):
        try:
            freq = str(TsType(os.path.basename(self.DATASET_PATH)))
        except Exception as e:
            freq = 'undefined'
        self.TS_TYPES[self.data_id] = freq
        return freq

    def _eval_flags(self, vardata, invalidate_flags, ds):
        valid = np.ones_like(vardata).astype(bool)
        for flagvar in self.FLAG_VARS:
            # check if this flag variable is in input dictionary
            if flagvar in invalidate_flags:
                invalidate = invalidate_flags[flagvar]
                if invalidate is None:
                    continue
                flags = ds[flagvar]
                slice_dim = flags.dims.index(self.FLAG_DIMNAMES[flagvar])

                valid *= np.apply_along_axis(self._eval_flags_slice,
                                             slice_dim, flags.values,
                                             invalidate)
        invalid = ~valid
        return invalid

    def read_file(self, filename, var_to_read=None, invalidate_flags=None,
                  var_to_write=None):
        """Read GHOST NetCDF data file

        Parameters
        ----------
        filename : str
            absolute path to filename to read
        var_name : str, optional
            name of variable to be read, if None, it is inferred from filename

        Returns
        -------
        list
            list of loaded `StationData` objects (dict-like data objects)

        """
        if invalidate_flags is None:
            invalidate_flags = self.DEFAULT_FLAGS_INVALID

        if var_to_read is None:
            var_to_read = self.get_meta_filename(filename)['var_name']
        elif var_to_read in self.VARNAMES_DATA:
            if var_to_write is None:
                var_to_read, var_to_write = self.VARNAMES_DATA[var_to_read], var_to_read
            else:
                var_to_read = self.VARNAMES_DATA[var_to_read]

        if var_to_write is None:
            var_to_write = self.var_names_data_inv[var_to_read]

        ds = xr.open_dataset(filename)

        if not all(x in ds.dims for x in ['station', 'time']):
            raise AttributeError('Missing dimensions')
        if not 'station_name' in ds:
            raise AttributeError('No variable station_name found')

        stats = []

        # get all station metadata values as numpy arrays, since xarray isel,
        # __getitem__, __getattr__ are slow... this can probably be solved
        # more elegantly
        meta_glob = {}
        for meta_key in self.META_KEYS:
            try:
                meta_glob[meta_key] = ds[meta_key].values
            except KeyError:
                const.print_log.warning('No such metadata key in GHOST data file: '
                                     '{}'.format(os.path.basename(filename)))

        for meta_key, to_unit in self.CONVERT_UNITS_META.items():
            from_unit = ds[meta_key].attrs['units']

            if from_unit != to_unit:
                cfac = cf_units.Unit(from_unit).convert(1, to_unit)
                meta_glob[meta_key] *= cfac

        tvals = ds['time'].values

        vardata = ds[var_to_read] #DataArray
        varinfo = vardata.attrs

        # ToDo: it is important that station comes first since we use numpy
        # indexing below and not xarray.isel or similar, due to performance
        # issues. This may need to be updated in case of profile data.
        assert vardata.dims == ('station', 'time')
        data_np = vardata.values

        # evaluate flags
        invalid = self._eval_flags(vardata, invalidate_flags, ds)

        for idx in ds.station.values:

            stat = {}
            meta = pya.metastandards.StationMetaData()
            meta['ts_type'] = self.TS_TYPE
            stat['time'] = tvals
            stat['meta'] = meta
            meta['var_info'] = {}

            for meta_key, vals in meta_glob.items():
                meta[meta_key] = vals[idx]

            #vardata = subset[var_name]
            stat[var_to_write] = data_np[idx]

            meta['var_info'][var_to_write] = {}
            meta['var_info'][var_to_write].update(varinfo)

            # import flagdata (2D array with time and flag dimensions)
            #invalid = self._eval_flags(vardata, invalidate_flags)
            stat['data_flagged'] = {}
            stat['data_flagged'][var_to_write] = invalid[idx]
            stats.append(stat)

        return stats

    def _add_flags_var_to_compute(self, statlist_from_file, var_to_compute):
        for stat in statlist_from_file:
            for i, req in enumerate(self.AUX_REQUIRES[var_to_compute]):
                flags = stat['data_flagged'][req]
                if i == 0:
                    # pointer (safes computation time in case only one variable
                    # is required, i.e. the same flags can be used)
                    stat['data_flagged'][var_to_compute] = flags
                else:
                    const.print_log.warning('THIS HAS NOT BEEN TESTED AND IS '
                                            'SHOULD CURRENTLY NOT BE ABLE '
                                            'TO BE REACHED.')
                    current = stat['data_flagged'][var_to_compute].copy()
                    updated = np.logical_or(current, flags)
                    stat['data_flagged'][var_to_compute] = updated
        return statlist_from_file

    def compute_additional_vars(self, statlist_from_file, vars_to_compute):
        """
        Compute additional variables for all sites

        Parameters
        ----------
        statlist_from_file : list
            list of :class:`StationData` objects containing variable data that
            can be read from the data files.
        vars_to_compute : list
            list of variables to be computed from the variables contained in
            `statlist_from_file`.

        Returns
        -------
        statlist_from_file : list
            list of modified :class:`StationData` objects, containing computed
            variables in addition to the data that was contained in them
            initially
        vars_added : list
            list of variables that could be successfully added

        """
        vars_added = []
        for var in vars_to_compute:
            first_stat = statlist_from_file[0]
            can_compute = True
            requires = self.AUX_REQUIRES[var]
            for req in requires:
                if not req in first_stat:
                    can_compute = False
            if can_compute:
                # this will add the variable data to each station data in
                # statlist_from_file
                statlist_from_file = self.AUX_FUNS[var](statlist_from_file, var,
                                             *requires)
                statlist_from_file = self._add_flags_var_to_compute(
                    statlist_from_file, var)

                if not var in vars_added:
                    vars_added.append(var)
        return (statlist_from_file, vars_added)

    def read(self, vars_to_retrieve=None, files=None, first_file=None,
             last_file=None, pattern=None, check_time=True, **kwargs):
        """Read data files into :class:`UngriddedData` object

        Parameters
        ----------
        vars_to_retrieve : list, optional
            list containing variables that are supposed to be read. If None,
            :attr:`DEFAULT_VARS` is used.
        files : list, optional
            list of files to be read. If None, then the file list is used that
            is returned on :func:`get_file_list`.
        first_file : int, optional
            index of first file in file list to read. If None, the first
            file in the list is used
        last_file : int, optional
            index of last file in list to read. If None, the last file
            in the list is used
         file_pattern : str, optional
            string pattern for file search (cf :func:`get_file_list`)

        Returns
        -------
        UngriddedData
            data object
        """
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]

        # make sure to use AeroCom variable names in output data
        vars_to_retrieve = varlist_aerocom(vars_to_retrieve)

        vars_to_read, vars_to_compute = self.check_vars_to_retrieve(vars_to_retrieve)

        if files is None:
            files = self.get_file_list(vars_to_read, pattern=pattern)
        elif isinstance(files, str):
            files = [files]

        if first_file is None:
            first_file = 0
        if last_file is None:
            last_file = len(files)

        files = files[first_file:last_file]

        data_obj = UngriddedData(num_points=1000000)

        meta_key = -1.0
        idx = 0

        #assign metadata object
        metadata = data_obj.metadata
        meta_idx = data_obj.meta_idx
        var_count_glob = -1
        rename = self.var_names_data_inv
        from tqdm import tqdm
        for i in tqdm(range(len(files))):
            _file = files[i]
            metafile = self.get_meta_filename(_file)
            var_to_read = metafile['var_name']
            begin = metafile['start']
            end = metafile['stop']

            var_read = rename[var_to_read]
            stats = self.read_file(_file, var_to_read=var_to_read,
                                   var_to_write=var_read, **kwargs)

            stats, added = self.compute_additional_vars(stats, vars_to_compute)
            if len(stats) == 0:
                const.logger.info('File {} does not contain any of the input '
                                  'variables {}'
                                  .format(_file, vars_to_retrieve))
            vars_avail = [var_read] + added
            vars_to_add = list(np.intersect1d(vars_to_retrieve, vars_avail))
            if len(vars_to_add) == 0:
                continue
            chunksize = 500000
            for stat in stats:
                meta_key += 1
                meta_idx[meta_key] = {}

                meta = stat['meta']
                vi = meta['var_info']

                meta['var_info'] = {}

                metadata[meta_key] = meta
                metadata[meta_key]['data_id'] = self.data_id
                # duplicate for now
                metadata[meta_key]['instrument_name'] = meta['measuring_instrument_name']
                statname = metadata[meta_key]['station_name']
                if '/' in statname:
                    statname = statname.replace('/','-')
                metadata[meta_key]['station_name'] = statname

                times = stat['time'].astype('datetime64[s]')
                timenums = np.float64(times)

                if check_time and (begin > times[0] or end < times[-1]):
                    raise ValueError('Something seems to be off with time '
                                     'dimension...')

                num_vars = len(vars_to_add)
                num_times = len(times)

                totnum = num_times * num_vars

                #check if size of data object needs to be extended
                if (idx + totnum) >= data_obj._ROWNO:
                    #if totnum < data_obj._CHUNKSIZE, then the latter is used
                    data_obj.add_chunk(chunksize)

                for j, var_to_write in enumerate(vars_to_add):
                    values = stat[var_to_write]

                    start = idx + j*num_times
                    stop = start + num_times

                    if not var_to_write in data_obj.var_idx:
                        var_count_glob += 1
                        var_idx = var_count_glob
                        data_obj.var_idx[var_to_write] = var_idx
                    else:
                        var_idx = data_obj.var_idx[var_to_write]

                    meta['var_info'][var_to_write] = vi[var_to_write]
                    #write common meta info for this station (data lon, lat and
                    #altitude are set to station locations)
                    data_obj._data[start:stop,
                                   data_obj._LATINDEX] = meta['latitude']
                    data_obj._data[start:stop,
                                   data_obj._LONINDEX] = meta['longitude']
                    data_obj._data[start:stop,
                                   data_obj._ALTITUDEINDEX] = meta['altitude']
                    data_obj._data[start:stop,
                                   data_obj._METADATAKEYINDEX] = meta_key

                    # write data to data object
                    data_obj._data[start:stop, data_obj._TIMEINDEX] = timenums

                    data_obj._data[start:stop, data_obj._DATAINDEX] = values

                    # add invalid measurements
                    invalid = stat['data_flagged'][var_to_write]
                    data_obj._data[start:stop, data_obj._DATAFLAGINDEX] = invalid

                    data_obj._data[start:stop, data_obj._VARINDEX] = var_idx

                    meta_idx[meta_key][var_to_write] = np.arange(start, stop)

                idx += totnum

        data_obj._data = data_obj._data[:idx]
        data_obj._check_index()
        return data_obj

if __name__ == '__main__':
    import pyaerocom as pya
    OBS_BASEDIR = '/home/jonasg/MyPyaerocom/data/obsdata'


    # make sure it works also on lustre
    GHOST_EBAS_DAILY_LOCAL =  os.path.join(OBS_BASEDIR, 'GHOST/data/EBAS/daily')
    GHOST_EEA_DAILY_LOCAL = os.path.join(OBS_BASEDIR, 'GHOST/data/EEA_AQ_eReporting/daily')

    obs = ReadGhost('GHOST.EBAS.daily', GHOST_EBAS_DAILY_LOCAL).read('concno')