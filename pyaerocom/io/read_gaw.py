"""Interface for reading GAW files.

This file is part of the pyaerocom package.

Example
-------
Notebook: '../../notebooks/DMS.ipynb'
"""

import numpy as np
from collections import OrderedDict as od
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom import const
from pyaerocom.stationdata import StationData
import pandas as pd
import matplotlib.pyplot as plt

class ReadGAW(ReadUngriddedBase):
    """Class for reading DMS data

    Extended class derived from  low-level base class :class: ReadUngriddedBase
    that contains some more functionallity.
    """
    # Mask for identifying datafiles
    _FILEMASK = '*.dat'

    # Version log of this class (for caching)
    __version__ = '0.01'

    # Name of the dataset (OBS_ID)
    DATA_ID = const.DMS_AMS_CVO_NAME  # change this since we added more vars?

    # List of all datasets supported by this interface
    SUPPORTED_DATASETS = [DATA_ID]

    # Temporal resolution flag for the supported dataset that is provided in a
    # defined temporal resolution
    TS_TYPE = 'daily'

    # Dictionary specifying values corresponding to invalid measurements
    NAN_VAL ={}
    NAN_VAL['vmrdms'] = -999999999999.99
    NAN_VAL['concso4'] = -999999999999.99
    NAN_VAL['concbc'] = -999999999999.99  # Assumed, there is actually no missing data in the file
    NAN_VAL['concmsa'] = -999999999999.99
    NAN_VAL['nd'] = -9999
    NAN_VAL['sd'] = -99999.
    NAN_VAL['f'] = -9999

    # Dictionary specifying the file column names (values) for each Aerocom
    # variable (keys)
    # Do we want CS and REM? Don't know what these columns represent...
    VAR_NAMES_FILE = {}
    VAR_NAMES_FILE['vmrdms'] = 'dimethylsulfide'
    VAR_NAMES_FILE['concbc'] = 'blackCarbon'
    VAR_NAMES_FILE['concso4'] = 'SO4'
    VAR_NAMES_FILE['concmsa'] = 'MSA'
    VAR_NAMES_FILE['nd'] = 'ND'
    VAR_NAMES_FILE['sd'] = 'SD'
    VAR_NAMES_FILE['f'] = 'F'

    # List of variables that are provided by this dataset (will be extended
    # by auxiliary variables on class init, for details see __init__ method of
    # base class ReadUngriddedBase)
    PROVIDES_VARIABLES = list(VAR_NAMES_FILE.keys())

    INSTRUMENT_NAME = 'unknown'

    @property
    def DEFAULT_VARS(self):
        return self.PROVIDES_VARIABLES

    @property
    def DATASET_NAME(self):
        """Name of the dataset"""
        return self.data_id

    def read_file(self, filename, vars_to_retrieve=None,
                  vars_as_series=False):
        """Read a single DMS file
        Parameters
        ----------
        filename : str
            Absolute path to filename to read.
        vars_to_retrieve : :obj:`list`, optional
            List of strings with variable names to read. If None, use :attr:
                `DEFAULT_VARS`.
        vars_as_series : bool
            If True, the data columns of all variables in the result dictionary
            are converted into pandas Series objects.

        Returns
        -------
        StationData
            Dict-like object containing the results.

        """
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]

        for var in vars_to_retrieve:
            if not var in self.PROVIDES_VARIABLES:
                raise ValueError('Invalid input variable {}'.format(var))

        # Iterate over the lines of the file
        self.logger.info("Reading file {}".format(filename))

        # We need to map the variables in the file with the values in VAR_NAME_FILE,
        # and for that we reverse the dictionary.
        # reverse dict to get keys of certain values (possible only because
        # values are hashable and unique)
        # Could also define the dict VAR_NAMES_FILE with the inverse order and
        # PROVIDES_VARIABLES = list(VAR_NAMES_FILE.values())
        inv_dict = dict(zip(self.VAR_NAMES_FILE.values(), self.VAR_NAMES_FILE.keys()))

        # Open the file, store the metadata in the first lines of the file,
        # skip empty lines, and store the headers and the data
        with open(filename, 'r') as f:
            # metadata (fixed number of rows in gaw files)
            meta = [next(f).split(':', 1)[1] for data in range(26)]

            f.readline()
            f.readline()
            f.readline()
            f.readline()
            f.readline()
            file_vars = f.readline().split()

            data = []
            for line in f:
                line = line.replace('/', '-')  # some dates have the wrong format
                rows = line.split()
                data.append(rows)

        # the next line lines should be deleted after correcting msa file
        # Drop line with empties (e.g. last line in msa file)
        for i in range(len(data)):
                if np.shape(data[i])[0] != 10:
                    del data[i]

        data = np.array(data)

        # names of the columns in the file that I want to use
        file_vars = file_vars[5:9]
        # If we want to include CS and REM, then:
        # file_vars = file_vars[5:]
        # and add these variables to VAR_NAMES_FILE

        # The variables analized are only the intersection of those provided by
        # the dataset, vars_to_retrieve, and those available in the file,
        # file_vars.
        vars_to_retrieve_file = list(set(vars_to_retrieve).intersection(
                [inv_dict[x] for x in file_vars]))

        # dictionary with keys and column index in the data
        data_idx = { file_vars[i]: i+4 for i in range(0, len(file_vars) ) }

        # Empty data object (a dictionary with extended functionality)
        data_out = StationData()
        data_out.data_id = self.data_id
        data_out.dataset_name = self.DATASET_NAME

        # Fill dictionary with relevant metadata and variables from the file.
        # Reformat the strings, and replace whitespaces in with underscore.
        data_out['station_name'] = meta[6].strip().replace(' ', '_')
        try:
            data_out['longitude'] = float(meta[12].strip())
            data_out['latitude'] = float(meta[11].strip())
            data_out['altitude'] = float(meta[13].strip())
        except Exception as e:
            from pyaerocom.exceptions import MetaDataError
            raise MetaDataError('Failed to read station coordinates. {}'
                                .format(repr(e)))
        data_out['filename'] = meta[1].strip()
        try:
            data_out['data_version'] = int(meta[5].strip())
        except Exception:
            data_out['data_version'] = None
        data_out['ts_type'] = meta[19].strip().replace(' ', '_')
        data_out['PI_email'] = meta[16].strip().replace(' ', '_')
        data_out['dataaltitude'] = meta[15].strip().replace(' ', '_')
        data_out['variables'] = vars_to_retrieve_file
        u = meta[20].strip().replace(' ', '_')

        # data in vars_to_retrieve_file
        for var in vars_to_retrieve_file:
            # find column
            print(self.VAR_NAMES_FILE[var])
            idx = data_idx[self.VAR_NAMES_FILE[var]]

            # decide what to do with values == '#REF!' or '-'. Maybe dropping the
            # entire line instead is the best option
            data[:, idx] = np.where(data[:, idx]=='#REF!',
                        self.NAN_VAL[var], data[:, idx])
            data[:, idx] = np.where(data[:, idx]=='-',
                        self.NAN_VAL[var], data[:, idx])

            # get data
            data_out['var_info'][var] = od()
            if idx == 4:  # variable
                if u == 'ppt':
                    data_out['var_info'][var]['units'] = 'mol mol-1'
                    data_out[var] = np.asarray(data[:, idx]).astype(np.float) * 1e12
                    # reset nan values
                    data_out[var] = np.where(data_out[var]==self.NAN_VAL['vmrdms']*1e12,
                            self.NAN_VAL['vmrdms'], data_out[var])
                elif u == 'ng/m3':
                    data_out['var_info'][var]['units'] = 'ug/m3'
                    data_out[var] = np.asarray(data[:, idx]).astype(np.float) * 1e-3
                    data_out[var] = np.where(data_out[var]==self.NAN_VAL['concmsa']*1e-3,
                            self.NAN_VAL['concmsa'], data_out[var])
                else:
                    data_out['var_info'][var]['units'] = u
                    data_out[var] = data[:, idx].astype(np.float)
            else:
                data_out['var_info'][var]['units'] = 1  # If dimensionless quantity
                data_out[var] = data[:, idx].astype(np.float)

        # If only vmrdms above, we need to write sd and f
        data_out['f']  = data[:, data_idx[self.VAR_NAMES_FILE['f']]]
        data_out['sd']  = data[:, data_idx[self.VAR_NAMES_FILE['sd']]]
        # Add date and time and the rest of the data to a dictionary
        data_out['dtime'] = []

        # if any hour is missing, just look at the date. This could be a
        # problem if the dataset has many observations for the same day and
        # only one observations does not specify the hour
        # Another option is to drop observations with missing hour, but then
        # a problem arises when data is not hourly.
        if any('99:99' in s for s in data[:, 1]):
            datestring = data[:, 0]
        else:
            datestring = np.core.defchararray.add(data[:, 0], 'T')
            datestring = np.core.defchararray.add(datestring, data[:, 1])
        data_out['dtime'] = datestring.astype("datetime64[s]")

        # Replace invalid measurements with nan values
        i= 0
        for key, value in self.NAN_VAL.items():
            if key in data_out.keys():
                print(key, value, i)
                if data_out[key].dtype != 'float64':
                    data_out[key] = data_out[key].astype('float64')
                data_out[key][data_out[key]==value]=np.nan
                i = i+1

        # convert data vectors to pandas.Series (if attribute
        # vars_as_series=True)
        if vars_as_series:
            for var in vars_to_retrieve_file:
                if var in data_out:
                    data_out[var] = pd.Series(data_out[var],
                                              index=data_out['dtime'])

        return data_out

    def read(self, vars_to_retrieve=None,
             files=None,
             first_file=None,
             last_file=None):
        """Method that reads list of files as instance of :class:`UngriddedData`

        Parameters
        ----------
        vars_to_retrieve : :obj:`list` or similar, optional
            List containing variable IDs that are supposed to be read. If None,
            all variables in :attr:`PROVIDES_VARIABLES` are loaded.
        files : :obj:`list`, optional
            List of files to be read. If None, then the file list used is the
            returned from :func:`get_file_list`.
        first_file : :obj:`int`, optional
            Index of the first file in :obj:'file' to be read. If None, the
            very first file in the list is used.
        last_file : :obj:`int`, optional
            Index of the last file in :obj:'file' to be read. If None, the very
            last file in the list is used.

        Returns
        -------
        UngriddedData
            data object
        """

        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]

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

        # Assign metadata object and index
        metadata = data_obj.metadata
        meta_idx = data_obj.meta_idx

        for i, _file in enumerate(files):
            station_data = self.read_file(_file,
                                          vars_to_retrieve=vars_to_retrieve)

            # only the variables in the file
            num_vars = len(station_data.var_info.keys())

            # Fill the metadata dict.
            # The location in the data set is time step dependant
            metadata[meta_key] = od()
            metadata[meta_key].update(station_data.get_meta())
            metadata[meta_key].update(station_data.get_station_coords())
            metadata[meta_key]['variables'] = list(station_data.var_info.keys()) #vars_to_retrieve
            if ('instrument_name' in station_data
                and station_data['instrument_name'] is not None):
                instr = station_data['instrument_name']
            else:
                instr = self.INSTRUMENT_NAME
            metadata[meta_key]['instrument_name'] = instr

            metadata[meta_key]['var_info'] = station_data['var_info']

            # List with indices of this station for each variable
            meta_idx[meta_key] = od()

            num_times = len(station_data['dtime'])

            totnum = num_times * num_vars

            # Check whether the size of the data object needs to be extended
            if (idx + totnum) >= data_obj._ROWNO:
                # if totnum < data_obj._CHUNKSIZE, then the latter is used
                data_obj.add_chunk(totnum)

            for var_idx, var in enumerate(list(station_data.var_info)):
                values = station_data[var]
                start = idx + var_idx * num_times
                stop = start + num_times

                # Write common meta info for this station (data lon, lat and
                # altitude are set to station locations)
                data_obj._data[start:stop, data_obj._LATINDEX
                               ] = station_data['latitude']
                data_obj._data[start:stop, data_obj._LONINDEX
                               ] = station_data['longitude']
                data_obj._data[start:stop, data_obj._ALTITUDEINDEX
                               ] = station_data['altitude']
                data_obj._data[start:stop, data_obj._METADATAKEYINDEX
                               ] = meta_key
                data_obj._data[start:stop, data_obj._DATAHEIGHTINDEX
                               ] = station_data['dataaltitude']
                data_obj._data[start:stop, data_obj._DATAERRINDEX
                               ] = station_data['sd']
                data_obj._data[start:stop, data_obj._DATAFLAGINDEX
                               ] = station_data['f']
                data_obj._data[start:stop, data_obj._TIMEINDEX
                               ] = station_data['dtime']
                data_obj._data[start:stop, data_obj._DATAINDEX
                               ] = values
                data_obj._data[start:stop, data_obj._VARINDEX
                               ] = var_idx
                meta_idx[meta_key][var] = np.arange(start, stop)

                if not var in data_obj.var_idx:
                    data_obj.var_idx[var] = var_idx

            idx += totnum
            meta_key = meta_key + 1.

        # Shorten data_obj._data to the right number of points
        data_obj._data = data_obj._data[:idx]
        #data_obj.data_revision[self.DATASET_NAME] = self.data_revision
        self.data = data_obj

        return data_obj

if __name__ == "__main__":

    # Test that the reading routine works

    r = ReadGAW()
    data = r.read(vars_to_retrieve = ['vmrdms', 'f'])

    # If I want to use dms_ai = data['Amsterdam_Island'].vmrdms
    # data = r.read(files=['/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/PYAEROCOM/DMS_AMS_CVO/data/ams137s00.lsce.as.fl.dimethylsulfide.nl.da.dat',
    #                '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/PYAEROCOM/DMS_AMS_CVO/data/cvo116n00.uyrk.as.cn.dimethylsulfide.nl.da.dat',
    #                '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/PYAEROCOM/DMS_AMS_CVO/data/so4.dat'],
    #                vars_to_retrieve = ['vmrdms', 'f'])

    print('vars to retrieve:', data.vars_to_retrieve)
    print('metadata:', data.metadata )

    stat = data['Cape_Verde_Observatory']

    # Print the station data object
    print('Cape Verde Observatory:', stat)

    # plot flag at Amsterdam Island
    ax = stat.plot_timeseries('f')
    plt.show()

    # Plot vmrdms at Amsterdam Island and Cape Verde Observatory in the same figure
    ax = data.plot_station_timeseries(station_name='Amsterdam_Island',
                                      var_name = 'vmrdms',
                                      label='Amsterdam Island')
    data.plot_station_timeseries(station_name='Cape_Verde_Observatory',
                                 var_name = 'vmrdms',
                                 ax=ax,
                                 label='Cape Verde Observatory')
    ax.set_title("vmrdms")
    plt.show()

    # Compare with papers
    # References:
    # https://agupubs.onlinelibrary.wiley.com/doi/epdf/10.1029/2000JD900236
    # https://aerocom.met.no/DATA/AEROCOM_WORK/oxford10/pdf_pap/suntharalingam_sulfate_2010.pdf

    # 2004-2008
    # plot monthly mean
    # dms_ai = data['Amsterdam_Island'].vmrdms  # error when reading more than one file with the same station name
    dms_ai = data[0].vmrdms # if all the files are read
    dms_ai_0408 = dms_ai['2004-1-1':'2008-12-31']
    dms_ai_monthly_0408 = dms_ai_0408.resample('M', 'mean')
    plt.figure()
    ax = dms_ai_monthly_0408.plot()
    ax.set_title('Monthlty mean of vmrdms at Amsterdam Island (2004-2008)')
    plt.show()

    # plot climatology
    dms_climat_0408 = dms_ai_monthly_0408.groupby(
            dms_ai_monthly_0408.index.month).mean()
    #dms_climat_0408 = dms_ai_0408.groupby(dms_ai_0808.index.month).mean()
    print('DMS climatology at Amsterdam Island (2004-2008):', dms_climat_0408)
    plt.figure()
    ax = dms_climat_0408.plot(label='mean')
    ax.set_title('Monthly climatology of vmrdms at Amsterdam Island (2004-2008)')
    plt.show()

    # 1990-1999
    dms_ai_9099 = dms_ai['1990-1-1':'1999-12-31']

    print('count:', dms_ai_9099.count())  # Should be 2820
    dms_ai_monthly_mean_9099 = dms_ai_9099.resample('M').mean()

    dms_climat_9099 = dms_ai_monthly_mean_9099.groupby(
            dms_ai_monthly_mean_9099.index.month).mean()

    print('DMS climatology at Amsterdam Island (1990-1999):', dms_climat_9099)
    plt.figure()
    ax = dms_climat_9099.plot(label='mean')
    ax.set_title('Climatology of vmrdms at Amsterdam Island (1990-1999)')

    dms_ai_monthly_median_9099 = dms_ai_9099.resample('M').median()

    dms_median_9099 = dms_ai_monthly_median_9099.groupby(
            dms_ai_monthly_median_9099.index.month).median()

    print('DMS monthly median at Amsterdam Island (1990-1999):', dms_median_9099)
    dms_median_9099.plot(label='median', ax=ax)
    plt.legend(loc='best')
    plt.show()

    # Test that the reading routine wirks for the rest of the variables
    # SO4
    data2 = r.read(vars_to_retrieve = ['concso4'])
    stat = data2[5]
    ax = stat.plot_timeseries('concso4')
    plt.show()

    # black carbon
    data3 = r.read(vars_to_retrieve = ['concbc'])
    stat = data3[1]
    ax = stat.plot_timeseries('concbc')
    plt.show()

    # dms second file
    data4 = r.read(vars_to_retrieve = ['vmrdms'])
    stat = data4[3]
    ax = stat.plot_timeseries('vmrdms')
    plt.show()

    # msa
    data5 = r.read(vars_to_retrieve = ['concmsa'])
    stat = data5[4]
    ax = stat.plot_timeseries('concmsa')
    plt.show()
