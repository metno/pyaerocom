import os
from glob import glob
import pandas as pd
from tqdm import tqdm
import numpy as np
from pyaerocom import const
from pyaerocom.io import ReadUngriddedBase
from pyaerocom.exceptions import DataCoverageError
from pyaerocom import UngriddedData, StationData

class ReadAirNow(ReadUngriddedBase):

    # data type of files
    _FILETYPE = '.dat'

    # to recursively retrieve list of data files
    _FILEMASK = f'/**/*{_FILETYPE}'

    #: version log of this class (for caching)
    __version__ = '0.1'

    #: column delimiter
    FILE_COL_DELIM = '|'

    #: columns in data files
    FILE_COL_NAMES = ['date','time', 'station_id',
                      'station_name', 'time_zone',
                      'variable', 'unit', 'value',
                      'institute']

    #: mapping of columns in station metadata file to pyaerocom standard
    STATION_META_MAP = {
            'aqsid'             : 'station_id',
            'name'              : 'station_name',
            'lat'               : 'latitude',
            'lon'               : 'longitude',
            'elevation'         : 'altitude',
            'city'              : 'city',
            'address'           : 'address',
            'timezone'          : 'timezone',
            'environment'       : 'environment',
            'modificationdate'  : 'modificationdate',
            'populationclass'   : 'classification',
            'comment'           : 'comment'
            }

    STATION_META_DTYPES = {
            'station_id'        : str,
            'station_name'      : str,
            'latitude'          : float,
            'longitude'         : float,
            'altitude'          : float,
            'city'              : str,
            'address'           : str,
            'timezone'          : str,
            'environment'       : str,
            'modificationdate'  : str,
            'classification'    : str,
            'comment'           : str
            }
    #:
    BASEYEAR = 2000

    #: Name of dataset (OBS_ID)
    DATA_ID = 'AirNow' #'GAWTADsubsetAasEtAl'

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [DATA_ID]

    #: units found in file
    UNIT_MAP = {
        'C' : 'celcius',
        'M/S' : 'm s-1',
        'MILLIBAR' : 'mbar',
        'MM' : 'mm',
        'PERCENT' : '%',
        'PPB' : 'ppb',
        'PPM' : 'ppm',
        'UG/M3' : 'ug m-2',
        'WATTS/M2': 'W m-2'
        }

    VAR_MAP = {
        'concbc'    : 'BC',
        'concco'    : 'CO',
        'concnh3'   : 'NH3',
        'concno'    : 'NO',
        'concno2'   : 'NO2',
        'concnox'   : 'NOX',
        'concnoy'   : 'NOY',
        'conco3'    : 'OZONE',
        'concpm10'  : 'PM10',
        'concpm25'  : 'PM2.5',
        'concso2'   : 'SO2',
        }

    PROVIDES_VARIABLES = list(VAR_MAP.keys())

    DEFAULT_VARS = PROVIDES_VARIABLES

    TS_TYPE = 'hourly'

    #: file containing station metadata
    STAT_METADATA_FILENAME = 'allStations_20191224.csv'

    def __init__(self, data_dir=None):
        super(ReadAirNow, self).__init__(None, dataset_path=data_dir)
        self.make_datetime64_array = np.vectorize(self._date_time_str_to_datetime64)

    def _date_time_str_to_datetime64(self, date, time):
        mm, dd, yy = date.split('/')
        HH, MM = time.split(':')
        yr=str(self.BASEYEAR + int(yy))
        # returns as datetime64[s]
        return np.datetime64(f'{yr}-{mm}-{dd}T{HH}:{MM}:00')

    def _datetime_from_filename(self, filepath):
        fn = os.path.basename(filepath).split(self._FILETYPE)[0]
        assert len(fn) == 10
        tstr = f'{fn[:4]}-{fn[4:6]}-{fn[6:8]}T{fn[8:10]}:00:00'
        return np.datetime64(tstr)

    def get_file_list(self):
        basepath = self.DATASET_PATH
        pattern = f'{basepath}{self._FILEMASK}'
        files = sorted(glob(pattern))
        return files

    def _read_file(self, file, assert_same_dtime=True):
        df = pd.read_csv(file,sep=self.FILE_COL_DELIM,
                         names=self.FILE_COL_NAMES)
        return df

    def _read_files(self, files, vars_to_retrieve):

        stat_meta = self._init_station_metadata()
        stat_ids = list(stat_meta.keys())
        print('read data file(s)')
        # initialize empty dataframe

        varcol = self.FILE_COL_NAMES.index('variable')
        statcol = self.FILE_COL_NAMES.index('station_id')
        tzonecol = self.FILE_COL_NAMES.index('time_zone')
        unitcol = self.FILE_COL_NAMES.index('unit')
        valcol = self.FILE_COL_NAMES.index('value')

        arrs = []
        for i in tqdm(range(len(files))):
            fp = files[i]
            filedata = self._read_file(fp)
            arr = filedata.values

            for i, var in enumerate(vars_to_retrieve):
                if i == 0:
                    mask = arr[:, varcol] == self.VAR_MAP[var]
                else:
                    mask = np.logical_or(mask, arr[:, varcol] == self.VAR_MAP[var])
            matches = mask.sum()
            if matches:
                vardata = arr[mask]
                arrs.append(vardata)

        data = np.concatenate(arrs)

        dtime = self.make_datetime64_array(data[:, 0], data[:, 1])
        stats = []
        for var in vars_to_retrieve:
            # extract only variable data (should speed things up)
            var_in_file = self.VAR_MAP[var]
            mask = data[:, varcol] == var_in_file
            subset = data[mask]
            dtime_subset = dtime[mask]
            statlist = np.unique(subset[:, statcol])


            for stat_id in statlist:
                if not stat_id in stat_ids:
                    continue
                statmask = subset[:, statcol] == stat_id
                if statmask.sum() == 0:
                    continue
                statdata = subset[statmask]
                timestamps = dtime_subset[statmask]

                stat = StationData(**stat_meta[stat_id])
                offs = np.unique(statdata[:, tzonecol])


                if not len(offs) == 1:
                    raise NotImplementedError(
                        f'Encountered several timezones for station ID {stat_id}'
                        )
                # account for timezone
                timedelta = np.timedelta64(int(offs[0]), 'h')
                vals = statdata[:, valcol]
                units = np.unique(statdata[:, unitcol])
                if len(units) != 1:
                    raise NotImplementedError(
                        f'Encountered several units for {var}'
                        )
                elif not units[0] in self.UNIT_MAP:
                    raise AttributeError(
                        'Encountered unregistered unit {units[0]} for {var}'
                        )
                stat['dtime'] = timestamps + timedelta
                stat['timezone'] ='UTC'
                stat[var] = vals
                unit = self.UNIT_MAP[units[0]]
                stat['var_info'][var] = dict(units=unit)
                stats.append(stat)
        return stats

    def read_file(self):
        raise NotImplementedError('Not needed for these data since the format '
                                  'is unsuitable...')

    def _read_metadata_file(self):
        fn = os.path.join(self.DATASET_PATH, self.STAT_METADATA_FILENAME)
        cfg = pd.read_csv(fn,sep=',', converters={'aqsid': lambda x: str(x)})
        return cfg

    def _init_station_metadata(self):

        cfg = self._read_metadata_file()
        meta_map = self.STATION_META_MAP

        cols = list(cfg.columns.values)
        col_idx = {}
        for from_meta, to_meta in meta_map.items():
            col_idx[to_meta] = cols.index(from_meta)

        arr = cfg.values
        dtypes = self.STATION_META_DTYPES
#        station_names = arr[:, col_idx['station_name']]
        stats = {}
        for row in arr:
            stat = {}
            for meta_key, col_num in col_idx.items():
                stat[meta_key] = dtypes[meta_key](row[col_num])
            sid = stat['station_id']
            stats[sid] = stat

        return stats

    def read(self, vars_to_retrieve=None, first_file=None, last_file=None):

        if isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]

        files = self.get_file_list()
        if first_file is None:
            first_file = 0
        if last_file is None:
            last_file = len(files)
        files = files[first_file:last_file]

        stats = self._read_files(files, vars_to_retrieve)

        data = UngriddedData.from_station_data(stats)

        return data


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    plt.close('all')
    path_data = '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/MACC_INSITU_AirNow'
    path_data = '/home/jonasg/MyPyaerocom/data/obsdata/MACC_INSITU_AirNow'

    test_file =  path_data + '/202001/2020010100.dat'
    reader = ReadAirNow(data_dir=path_data)

    #data = reader._read_file(test_file)

    last_file = None
    varis = ['concpm10', 'concpm25']
    data = reader.read(varis, last_file=last_file)

    if last_file == 10 and varis == ['concpm10', 'concpm25']:
        assert len(data.unique_station_names) == 744
    data.plot_station_coordinates()
    #data1 = _read_file_alt(files[0])
