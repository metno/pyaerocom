import os
import pandas as pd
from tqdm import tqdm
import numpy as np
from pyaerocom import const
from pyaerocom.exceptions import DataRetrievalError
from pyaerocom.helpers import varlist_aerocom
from pyaerocom.mathutils import concx_to_vmrx
from pyaerocom.molmasses import get_molmass
from pyaerocom.ungriddeddata import UngriddedData
from geonum import atmosphere as atm
from pyaerocom.io import ReadUngriddedBase

P_STD = atm.p0 # standard atmosphere pressure
T_STD = atm.T0_STD # standard atmosphere temperature

def _conc_to_vmr_marcopolo_stats(data, to_var, from_var,
                                 p_pascal=None, T_kelvin=None,
                                 mmol_air=None):
    if p_pascal is None:
        p_pascal = P_STD
    if T_kelvin is None:
        T_kelvin =  T_STD
    if mmol_air is None:
        mmol_air = get_molmass('air_dry')

    for stat in data:
        if not from_var in stat:
            continue

        concdata = stat[from_var]

        mmol_var = get_molmass(to_var)
        from_unit = stat['var_info'][from_var]['units']
        to_unit = const.VARS[to_var].units
        vmrvals = concx_to_vmrx(concdata,
                             p_pascal=p_pascal,
                             T_kelvin=T_kelvin,
                             mmol_var= mmol_var,
                             mmol_air=mmol_air,
                             conc_unit=from_unit,
                             to_unit=to_unit)
        stat[to_var] = vmrvals
        vi = {}
        vi.update(stat['var_info'][from_var])
        vi['computed'] = True
        vi['units'] = to_unit
        vi['units_info'] = (
            f'The original data is provided as mass conc. in units of ug m-3 and '
            f'was converted to ppb assuming a standard atmosphere '
            f'(p={p_pascal/100}hPa, T={T_kelvin}K) assuming dry molar mass of air '
            f'M_Air_dry={mmol_air}g/mol and total molecular mass of '
            f'{from_var}={mmol_var}g/mol'
            )
        stat['var_info'][to_var] = vi

    return data

class ReadMarcoPolo(ReadUngriddedBase):
    """
    Reading routine for chinese MarcoPolo observations
    """

    #: Data type of files
    _FILETYPE = '.csv'

    #: Filemask for glob data file search
    _FILEMASK = f'*{_FILETYPE}'

    #: Column delimiter
    FILE_COL_DELIM = ','

    #: Version log of this class (for caching)
    __version__ = '0.02'

    #: Default data ID
    DATA_ID = 'MarcoPolo'

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [DATA_ID]

    #: Indices of columns in data files
    FILE_COLS = {
        'station_id'    : 0,
        'datetime'      : 1,
        'var_name'      : 2,
        'value'         : 3
        }
    #: Mapping of columns in station metadata file to pyaerocom standard
    STATION_META_MAP = {
        'stationId'     : 'station_id',
        'stationName'   : 'station_name',
        'cityId'        : 'city_id',
        'latitude'      : 'latitude',
        'longitude'     : 'longitude',
        'cityName'      : 'city'
        }

    #: conversion functions for metadata dtypes
    STATION_META_DTYPES = {
        'station_id'     : str,
        'station_name'   : str,
        'city_id'        : str,
        'latitude'      : float,
        'longitude'     : float,
        'city'      : str
        }

    #: Variable names in data files
    VAR_MAP = {
        'concco': 'co',
        'concso2': 'so2',
        'concno2': 'no2',
        'conco3': 'o3',
        'concpm10': 'pm10',
        'concpm25': 'pm2_5'
        }

    #: Variable units (not provided in data files)
    VAR_UNITS = {
        'concco'   : 'unknown',
        'concso2'  : 'unknown',
        'concno2'  : 'ug m-3', # mail from Henk Eskes, 1 Feb. 2021
        'conco3'   : 'ug m-3', # mail from Henk Eskes, 1 Feb. 2021
        'concpm10' : 'ug m-3', # mail from Henk Eskes, 1 Feb. 2021
        'concpm25' : 'ug m-3' # mail from Henk Eskes, 1 Feb. 2021
        }

    #: Variables that are computed (cannot be read directly)
    AUX_REQUIRES = {
        'vmro3'  : ['conco3'],
        'vmrno2' : ['concno2']
        }

    #: functions used to convert variables that are computed
    AUX_FUNS = {
        'vmro3'  : _conc_to_vmr_marcopolo_stats,
        'vmrno2' : _conc_to_vmr_marcopolo_stats
        }


    PROVIDES_VARIABLES = list(VAR_MAP.keys())
    DEFAULT_VARS = ['concpm10', 'concpm25', 'concno2', 'conco3']

    TS_TYPE = 'hourly'

    STAT_METADATA_FILENAME = 'station_info.xlsx'

    def __init__(self, dataset_to_read=None, data_dir=None):
        super(ReadMarcoPolo, self).__init__(dataset_to_read=dataset_to_read,
                                         dataset_path=data_dir)

        try:
            import openpyxl
        except ImportError:
            raise ImportError(
                'ReadMarcoPolo class needs package openpyxl '
                'which is not part of the pyaerocom standard installation. '
                'Please install openpyxl via conda or pip.')

    def _read_metadata_file(self):
        fn = os.path.join(self.DATASET_PATH, self.STAT_METADATA_FILENAME)
        cfg = pd.read_excel(fn,engine='openpyxl')
        return cfg

    def _init_station_metadata(self):
        """
        Initiate metadata for all stations

        Returns
        -------
        dict
            dictionary with metadata dictionaries for all stations

        """

        cfg = self._read_metadata_file()

        meta_map = self.STATION_META_MAP
        dtypes = self.STATION_META_DTYPES

        cols = list(cfg.columns.values)
        col_idx = {}
        for from_meta, to_meta in meta_map.items():
            col_idx[to_meta] = cols.index(from_meta)

        arr = cfg.values

        stats = {}
        for row in arr:
            stat = {}
            for meta_key, col_num in col_idx.items():
                stat[meta_key] = dtypes[meta_key](row[col_num])
            stat['data_id'] = self.data_id
            stat['ts_type'] = self.TS_TYPE
            stats[stat['station_id']] = stat

        return stats

    def _read_file(self, file):
        df = pd.read_csv(file, sep=self.FILE_COL_DELIM)
        return df

    def _make_station_data(self, var, var_stats_unique, stat_ids, var_stats,
                           var_dtime, var_values, stat_meta):

        units = self.VAR_UNITS
        stats = []
        for stat_id in var_stats_unique:
            if not stat_id in stat_ids:
                continue

            statmask = var_stats == stat_id

            if statmask.sum() == 0:
                continue

            timestamps = var_dtime[statmask]
            vals = var_values[statmask]



            stat = {}
            stat.update(stat_meta[stat_id])

            stat['dtime'] = timestamps
            stat['timezone'] ='unknown'
            stat[var] = vals
            unit = units[var]
            stat['var_info'] = {}
            stat['var_info'][var] = dict(units=unit)
            stats.append(stat)
        return stats

    def _read_files(self, files, vars_to_retrieve):

        filecols = self.FILE_COLS

        stat_meta = self._init_station_metadata()

        # get all station IDs found in the metadata file
        stat_ids = list(stat_meta.keys())

        arrs = []

        varcol = filecols['var_name']
        for i in tqdm(range(len(files))):
            filedata = self._read_file(files[i])
            arr = filedata.values

            for i, var in enumerate(vars_to_retrieve):
                filevar = self.VAR_MAP[var]
                if i == 0:
                    mask = arr[:, varcol] == filevar
                else:
                    mask = np.logical_or(mask, arr[:, varcol] == filevar)
            matches = mask.sum()
            if matches:
                vardata = arr[mask]
                arrs.append(vardata)
        if len(arrs) == 0:
            raise DataRetrievalError(
                'None of the input variables could be found in input list')
        data = np.concatenate(arrs)

        dtime = data[:, filecols['datetime']].astype('datetime64[s]')

        varis = data[:, varcol].astype(str)
        values = data[:, filecols['value']].astype(np.float64)
        statids = data[:, filecols['station_id']].astype(str)

        stats = []
        for var in vars_to_retrieve:
            var_in_file = self.VAR_MAP[var]

            varmask = varis == var_in_file

            var_values = values[varmask]
            var_stats = statids[varmask]
            var_dtime = dtime[varmask]

            var_stats_unique = np.unique(var_stats)

            var_stats = self._make_station_data(var, var_stats_unique,
                                                stat_ids, var_stats,
                                                var_dtime, var_values,
                                                stat_meta)
            stats.extend(var_stats)

        return stats

    def read_file(self):
        """
        This method is not implemented (but needs to be declared for template)

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError('Not needed for these data since the format '
                                  'is unsuitable...')

    def compute_additional_vars(self, statlist_from_file, vars_to_compute):

        for var in vars_to_compute:
            fun = self.AUX_FUNS[var]
            requires = self.AUX_REQUIRES[var]
            # this will add the variable data to each station data in
            # statlist_from_file
            statlist_from_file = fun(statlist_from_file, var, *requires)


        return statlist_from_file

    def read(self, vars_to_retrieve=None, first_file=None, last_file=None):
        """
        Read variable data

        Parameters
        ----------
        vars_to_retrieve : str or list, optional
            List of variables to be retrieved. The default is None.
        first_file : int, optional
            Index of first file to be read. The default is None, in which case
            index 0 in file list is used.
        last_file : int, optional
            Index of last file to be read. The default is None, in which case
            last index in file list is used.

        Returns
        -------
        data : UngriddedData
            loaded data object.

        """
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]

        # make sure to use AeroCom variable names in output data
        vars_to_retrieve = varlist_aerocom(vars_to_retrieve)

        vars_to_read, vars_to_compute = self.check_vars_to_retrieve(vars_to_retrieve)

        files = self.get_file_list()
        if first_file is None:
            first_file = 0
        if last_file is None:
            last_file = len(files)
        files = files[first_file:last_file]

        stats = self._read_files(files, vars_to_read)

        stats = self.compute_additional_vars(stats, vars_to_compute)

        data = UngriddedData.from_station_data(stats)

        return data

if __name__ == '__main__':
    path_data = '/home/jonasg/MyPyaerocom/data/obsdata/CHINA_SON2020_MP_NRT'

    reader = ReadMarcoPolo(data_dir=path_data)

    #files = reader.get_file_list()
    #print(files)

    data = reader.read(['vmro3'], last_file=1)

# =============================================================================
#     stats = data.to_station_data_all('concpm10')['stats']
#
#     stat = stats[0]
#     stats[0].plot_timeseries('concpm10')
# =============================================================================


    #data = read_cams84_china(files, ['concpm10','concpm25'])
