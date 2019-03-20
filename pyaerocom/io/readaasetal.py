import os

import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import od

from pyaerocom import const, print_log

from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.io.readungriddedbase import ReadUngriddedBase

# PATH ON LUSTRE /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/PYAEROCOM/GAWTADSulphurSubset/data
# Note to self: NUMBERS_OF_WIERD_STATIONS = np.array([8, 69,127,134,145,169,181,188,189,202,203,237,240,286,315,613,247,312,387,535])


class ReadSulphurAasEtAl(ReadUngriddedBase):
    """Interface for reading subset of GOL TAT data related to the nature paper.

    .. seealso::

        :class:`ReadUngriddedBase`
	"""
    # name of files in GawTadSubsetAasEtAl
    _FILEMASK = '*.csv' # fix

    #: version log of this class (for caching)
    __version__ = '0.01'

    COL_DELIM = ','

    #: Temporal resoloution
    TS_TYPE = 'monthly'

    #: Name of dataset (OBS_ID)
    DATA_ID = 'GAWTADsubsetAasEtAl'

    #: Path were data is located (hard coded for now)
    DATASET_PATH = '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/PYAEROCOM/GAWTADSulphurSubset/data' # fix

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [DATA_ID]

    #: value corresponding to invalid measurement
    #NAN_VAL = -9999.
    NAN_VAL = -999.

    mapping = {}
    mapping['concentration_mgS/L'] = 'sconcSO4precip'
    mapping['precip_amount_mm'] = 'pr'
    mapping['deposition_kgS/ha'] = 'wetSO4'
    mapping['concentration_ugS/m3'] = ['sconcso2', 'sconcso4'] # fix denne
    #: List of variables that are provided by this dataset (will be extended
    #: by auxiliary variables on class init, for details see __init__ method of
    #: base class ReadUngriddedBase)
    # TODO fix this
    VAR_NAMES_FILE = {}
    # No defalt variables in these files.
    VAR_NAMES_FILE["aero"] = "concentration_ugS/m3"
    VAR_NAMES_FILE["p0"] = 'concentration_mgS/L'
    VAR_NAMES_FILE["p1"] = 'precip_amount_mm'
    VAR_NAMES_FILE["p2"] = 'deposition_kgS/ha'

    PROVIDES_VARIABLES = list(VAR_NAMES_FILE.keys())
    num_vars = len(PROVIDES_VARIABLES)


    @property
    def DEFAULT_VARS(self):
        return self.PROVIDES_VARIABLES

    def read_file(self, filename, vars_to_retrieve=None): #  -> List[StationData]:
        """Read GawTadSubsetAasEtAl files

        Parameters
        ----------
        filename : str
        absolute path to filename to read

        Returns
        -------
        station_list : List[StationData]
        List of dictionary-like object containing data
        """

        station_list = []

        df = pd.read_csv(filename,sep=",", low_memory=False)
        df["day"] = np.ones((len(df["year"]))).astype('int')
        df['dtime'] = df.apply(lambda row: datetime(row['year'], row['month'], row["day"]), axis=1) # array av numpy.datetime64
        df.rename(columns= {"Sampler":"instrument_name"}, inplace = True)
        df.pop("year")
        df.pop("month")
        df.pop("day")
        grouped = df.groupby(by = "station_name")

        # Looping over every station:
        for name, group in grouped:

            s = StationData()
            s['station_name'] = name
            s["altitude"] = np.nan
            s["filename"] = filename

            # Needs a update
            s["PI"] = None
            s["PI_email"] = None
            s["data_id"] = self.DATA_ID
            s["ts_type"] = self.TS_TYPE

            temp_vars = []

            for key in group.keys():
                # if key is a variable
                if key in self.mapping.keys():
                    # Todo this needs to be improved
                    if isinstance(self.mapping[key], str):
                        var = self.mapping[key]
                        temp_vars.append(var)
                    elif "so2" in filename:
                        var = self.mapping[key][0]
                        temp_vars.append(var)
                    else:
                        var = self.mapping[key][1]
                        temp_vars.append(var)
                    s[var] = pd.to_numeric(group[key], errors='coerce').values
                    # the above line makes sure that both integers and nan values are considered numeric
                else:
                    if key == 'dtime':
                        s[key] = group[key].values
                    else:
                        s[key] = group[key].values[0]
            s['variables'] = temp_vars
            station_list.append(s)
        return station_list

    def read(self, vars_to_retrieve = None, files=None, first_file=None,last_file=None):
        """
        Method that reads list of files as instance of :class:`UngriddedData`

        Parameters COPY from AeronetSunV3Lev2
        ----------
        vars_to_retrieve : :obj:`list` or similar, optional,
        list containing variable IDs that are supposed to be read. If None,
        all variables in :attr:`PROVIDES_VARIABLES` are loaded
        files : :obj:`list`, optional
        list of files to be read. If None, then the file list is used that
        is returned on :func:`get_file_list`.
        first_file : :obj:`int`, optional
        index of first file in file list to read. If None, the very first
        file in the list is used
        last_file : :obj:`int`, optional
        index of last file in list to read. If None, the very last file
        in the list is used

        Returns
        -------
        UngriddedData
        data object

        """

        if files is None:
            if len(self.files) == 0:
                self.get_file_list()
            files = self.files

        if first_file is None:
            first_file = 0
        if last_file is None:
            last_file = len(files)

        files = files[first_file:last_file]

        data_obj = UngriddedData()

        meta_key = 0.0
        idx = 0

        #assign metadata object
        metadata = data_obj.metadata
        meta_idx = data_obj.meta_idx
        nr_which_are_already_there = 0

        for file in self.files:
            station_data_list = self.read_file(file, vars_to_retrieve=None)

            # Fill the metatdata dict
            # the location in the data set is time step dependant!
            # use the lat location here since we have to choose one location
            # in the time series plot

            for station_data in station_data_list:
                #self.counter += 1
                metadata[meta_key] = od()
                metadata[meta_key].update(station_data.get_meta())
                metadata[meta_key].update(station_data.get_station_coords())
                metadata[meta_key]['data_id'] = self.DATA_ID
                metadata[meta_key]['ts_type'] = self.TS_TYPE
                metadata[meta_key]['variables'] = station_data["variables"]

                # Is instrumentname
                if 'instrument_name' in station_data and station_data['instrument_name'] is not None:
                    instr = station_data['instrument_name']
                else:
                    instr = self.INSTRUMENT_NAME

                metadata[meta_key]['instrument_name'] = instr

                # this is a list with indices of this station for each variable
                # not sure yet, if we really need that or if it speeds up things
                meta_idx[meta_key] = od()

                num_times = len(station_data['dtime'])
                num_vars = len(station_data["variables"])
                vars_to_retrieve = station_data["variables"]

                times = np.float64(station_data['dtime'].astype('datetime64[us]'))
                totnum = num_times * num_vars

                if (idx + totnum) >= data_obj._ROWNO:
                    data_obj.add_chunk(totnum)

                for var_idx, var in enumerate(vars_to_retrieve):

                    values = station_data[var]

                    start = idx + var_idx * num_times
                    stop = start + num_times

                    data_obj._data[start:stop, data_obj._LATINDEX] = station_data['latitude']
                    data_obj._data[start:stop, data_obj._LONINDEX] = station_data['longitude']
                    data_obj._data[start:stop, data_obj._ALTITUDEINDEX] = station_data['altitude']
                    data_obj._data[start:stop, data_obj._METADATAKEYINDEX] = meta_key

                    # write data to data object
                    data_obj._data[start:stop, data_obj._TIMEINDEX] = times
                    data_obj._data[start:stop, data_obj._DATAINDEX] = values
                    data_obj._data[start:stop, data_obj._VARINDEX] = var_idx

                    meta_idx[meta_key][var] = np.arange(start, stop)
                    
                    if not var in data_obj.var_idx:
                        data_obj.var_idx[var] = var_idx

                meta_key += 1
                #nr_which_are_already_there += stop
                idx += totnum
        # When we finish reading crop the dataobject to the last index.
        data_obj._data = data_obj._data[:idx]
        data_obj.data_revision[self.DATA_ID] = self.data_revision
        self.data = data_obj
        return data_obj


if __name__ == "__main__":
     from pyaerocom import change_verbosity

     change_verbosity('warning')
     aa = ReadSulphurAasEtAl('GAWTADsubsetAasEtAl')
     ungridded = aa.read()
     print(np.shape(ungridded._data))
     print(np.shape(ungridded.metadata[0.0]))

     #print(ungridded.contains_vars)
     #ax = ungridded.plot_station_coordinates(color='lime')
     #ax.figure.savefig('/home/hannas/Desktop/test_stations_aasetal.png')

     #print(ungridded.unique_station_names)
     #print(ungridded.metadata[0])

     #stat = ungridded.to_station_data('Abington')

     #print(stat)
     #
     #ax = ungridded.plot_station_timeseries('Abington', 'sconcso2')

     #ax.figure.savefig('/home/hannas/Desktop/test_plot_tseries_first_station.png')
