import numpy as np
import os
import pandas as pd
#from datetime import datetime
import matplotlib.pyplot as plt
from collections import OrderedDict

from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
#from pyaerocom.io.helpers_units import (unitconv_sfc_conc, unitconv_wet_depo)

from pyaerocom.units_helpers import convert_unit
from pyaerocom.helpers import get_tot_number_of_seconds

class ReadSulphurAasEtAl(ReadUngriddedBase):
    """ Interface for reading subset of GAW-TAD-EANET data related to the nature paper.

    See Also
    ---------
        :class:`ReadUngriddedBase`
	"""
    # name of files in GawTadSubsetAasEtAl
    _FILEMASK = '*.csv' # fix

    #: version log of this class (for caching)
    __version__ = '0.07'

    COL_DELIM = ','

    #: Temporal resoloution
    TS_TYPE = 'monthly'

    #: Name of dataset (OBS_ID)
    DATA_ID = 'GAWTADsubsetAasEtAl' #'GAWTADsubsetAasEtAl'

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [DATA_ID]

    #: value corresponding to invalid measurement
    #NAN_VAL = -9999.
    NAN_VAL = -999.
    #: List of variables that are provided by this dataset (will be extended
    #: by auxiliary variables on class init, for details see __init__ method of
    #: base class ReadUngriddedBase)
    # This contains the mapping between the requested variables and what it is called in the files.
    
    COLNAMES_VARS = {}
    COLNAMES_VARS['concentration_mgS/L']  = ['concso4pr']
    COLNAMES_VARS['concentration_ugS/m3'] = ['concso4', 'concso2']
    COLNAMES_VARS['precip_amount_mm']     = ['pr']
    COLNAMES_VARS['deposition_kgS/ha']    = ['wetso4']

    #: Dictionary mapping filenames to available variables in the respective files. 
    FILES_CONTAIN = {}
    FILES_CONTAIN['monthly_so2.csv']        = ['concso2']
    FILES_CONTAIN['monthly_so4_aero.csv']   = ['concso4']
    FILES_CONTAIN['monthly_so4_precip.csv'] = ['wetso4', 'pr', 'concso4pr']
    
    #: Dictionary mapping variable name to hard coded filenames. 
    VARS_TO_FILES = {}
    VARS_TO_FILES['concso2']   = ['monthly_so2.csv']
    VARS_TO_FILES['concso4']   = ['monthly_so4_aero.csv']
    VARS_TO_FILES['pr']        = ['monthly_so4_precip.csv']
    VARS_TO_FILES['wetso4']    = ['monthly_so4_precip.csv']
    VARS_TO_FILES['concso4pr'] = ['monthly_so4_precip.csv']
    
    # (from to unit)
    UNITCONVERSION = {'concso2':   ('ug S/m3', 'ug m-3'), 
                      'concso4':   ('ug S/m3', 'ug m-3'), 
                      'wetso4':    ('kg S/ha', 'kg m-2'),  #  s-1
                      'concso4pr': ('mg S/L',   'g m-3')
                      }

    #: :obj: `list` of :obj: `str` 
    #: List containing all the variables available in this data set.
    PROVIDES_VARIABLES = list(VARS_TO_FILES.keys())
    
    #: int: Number of available variables in this data set.
    num_vars = len(PROVIDES_VARIABLES)
    
    #def __init__(self):
        #print("hello update ")
        #super(ReadUngriddedBase).__init__(dataset_to_read = DATA_ID)
    
    @property
    def DEFAULT_VARS(self):
        return self.PROVIDES_VARIABLES

    def read_file(self, filename, vars_to_retrieve): #  -> List[StationData]:
        """ Read one GawTadSubsetAasEtAl file

        Parameters
        ----------
        filename : str
            absolute path to filename to read

        vars_to_retrieve : :obj:`list` of `str`, :obj: `str`:, optional,
            list containing variable IDs that are supposed to be read. 
            
        Returns
        -------
        station_list : List[StationData]
            List of dictionary-like object containing data
        """
        station_list = []
        df = pd.read_csv(filename, sep=",", low_memory=False)
        # Converting month and year. 
        tconv = lambda yr, m : np.datetime64('{:04d}-{:02d}-{:02d}'.format(yr, m, 1), 's')
        dates_alt = [tconv(yr, m) for yr, m in
                     zip(df.year.values, df.month.values)]
        df['dtime'] = np.array(dates_alt)

        # array av numpy.datetime64
        df.rename(columns= {"Sampler":"instrument_name"}, inplace=True)
        grouped = df.groupby(by = "station_name")

        # Looping over every station:
        for name, station_group in grouped:
            station_group = station_group.drop_duplicates(subset='dtime', keep='first')  # Drops duplacate rows 
         
            s = StationData()
            # Meta data
            s['station_name'] = name
            s["altitude"] = np.nan
            s["filename"] = filename
            s["data_id"] = self.DATA_ID
            s["ts_type"] = self.TS_TYPE
            s['variables'] = []

            var_names = self.COLNAMES_VARS
            # Looping over all keys in the grouped data frame.
            for key in station_group:
                # Enters if the the key is a variable
                if key in var_names:
                    _var = np.intersect1d(var_names[key], vars_to_retrieve)
                    if len(_var) == 0:
                        continue
                    elif len(_var) > 1:
                        raise IOError('Found multiple matches...')
                    var = _var[0]
                    if var in self.UNITCONVERSION.keys():
                        # Convert units 
                        from_unit, to_unit = self.UNITCONVERSION[var]
                        values = pd.to_numeric(station_group[key],
                                               errors='coerce').values
                        s[var] = convert_unit(data=values, from_unit = from_unit, 
                                             to_unit = to_unit, var_name = var)
                        if var == 'wetso4':
                            s[var] = s[var]/get_tot_number_of_seconds(ts_type = 'monthly', 
                                                 dtime = station_group['dtime'])
                    else:
                        # This should only be true for
                        s[var] = pd.to_numeric(station_group[key],
                                               errors='coerce').values
                                             
                    s['variables'].append(var)
                else:
                    if key == 'dtime':
                        s[key] = station_group[key].values
                    else:
                        # Store the meta data. 
                        s[key] = station_group[key].values[0]
                
            # Added the created station to the station list.
            station_list.append(s)
        return station_list
    

    def read(self, vars_to_retrieve=None):
        """ Method that reads list of files as instance of :class:`UngriddedData`

        Parameters 
        ----------
        vars_to_retrieve : :obj:`list` or `str`:, optional,
            list containing variable IDs that are supposed to be read. If None,
            all variables in :attr:`PROVIDES_VARIABLES` are loaded

        files : :obj:`list`, optional
            list of files to be read. If None, then the file list is used that
            is returned on :func:`get_file_list`.

        Returns
        -------
        UngriddedData : :class:`UngriddedData`
            data object
            
        """

        files = self.get_file_list()

        unit={}
        unit['concso2'] = 'ug m-3'
        unit['concso4'] = 'ug m-3'
        unit['pr']       = 'mm'
        unit['wetso4']   = 'kg m-2 s-1'
        unit['concso4pr'] = 'g m-3' # removed sulphur from unit mgS/L

        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        data_obj = UngriddedData()

        meta_key = 0.0
        idx = 0
        varindex = -1
        
        #assign metadata object
        metadata = data_obj.metadata # OrderedDict
        meta_idx = data_obj.meta_idx # OrderedDict

        for file in files:
            filename = os.path.basename(file)
            if not filename in self.FILES_CONTAIN:
                raise IOError('Invalid file name {}, this should not happen.'
                              .format(filename))
            var_matches = [var for var in vars_to_retrieve if var in
                            self.FILES_CONTAIN[filename]]
            if len(var_matches) == 0:
                continue
            station_data_list = self.read_file(file, 
                                               vars_to_retrieve=var_matches)
            for station_data in station_data_list:
                #self.counter += 1
                metadata[meta_key] = OrderedDict()
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
                metadata[meta_key]['data_revision'] = self.data_revision

                # this is a list with indices of this station for each variable
                # not sure yet, if we really need that or if it speeds up things
                meta_idx[meta_key] = OrderedDict()

                num_times = len(station_data['dtime'])
                num_vars = len(station_data["variables"])
                temp_vars = station_data["variables"]
                tconv = station_data['dtime'].astype('datetime64[s]')
                times = np.float64(tconv)
                totnum = num_times * num_vars

                if (idx + totnum) >= data_obj._ROWNO:
                    # This results in a error because it doesn't want to multiply empty with nan
                    data_obj.add_chunk(totnum)
                for var_count, var in enumerate(temp_vars):

                    values = station_data[var]
                    start = idx + var_count * num_times
                    stop = start + num_times

                    if not var in data_obj.var_idx:
                        varindex += 1
                        data_obj.var_idx[var] = varindex
                        var_idx = varindex
                    else:
                        var_idx = data_obj.var_idx[var]

                    metadata[meta_key]['var_info'] = OrderedDict()
                    metadata[meta_key]['var_info'][var] = OrderedDict()
                    metadata[meta_key]['var_info'][var]['units'] = unit[var]

                    data_obj._data[start:stop, data_obj._LATINDEX] = station_data['latitude']
                    data_obj._data[start:stop, data_obj._LONINDEX] = station_data['longitude']
                    data_obj._data[start:stop, data_obj._ALTITUDEINDEX] = station_data['altitude']
                    data_obj._data[start:stop, data_obj._METADATAKEYINDEX] = meta_key

                    # write data to data object
                    data_obj._data[start:stop, data_obj._TIMEINDEX] = times
                    data_obj._data[start:stop, data_obj._DATAINDEX] = values
                    data_obj._data[start:stop, data_obj._VARINDEX] = var_idx

                    meta_idx[meta_key][var] = np.arange(start, stop)

                meta_key += 1
                idx += totnum
                
        data_obj._data = data_obj._data[:idx]
        self.data = data_obj # initalizing a pointer to it selves
        return data_obj
 
def _check_line_endings(filename):
    ll = None
    wrong_endings = {}
    with open(filename, 'r') as f:
        prev = None
        for i, line in enumerate(f.readlines()):
            spl = line.split(',')
            if not spl[-1] == '\n':
                wrong_endings[i+1] = line
            if ll is None:
                ll = len(spl)
            elif not len(spl) == ll:
                print(i)
                print(prev)
                print(spl)
                raise Exception
            prev = spl
    return wrong_endings

if __name__ == "__main__":
     from pyaerocom import change_verbosity
     import matplotlib.pyplot as plt
     #change_verbosity('info')
     #V = "concso4pr"
     aa = ReadSulphurAasEtAl('GAWTADsubsetAasEtAl')
         # todo : 
     #so2 = aa.read('concso2')
     #so4_aero = aa.read('concso4')
     V = ['concso2']
     ungridded = aa.read(V)
     names = ungridded.station_name[:10]
     abington = ungridded.to_station_data('K-puszta', V)
     abington.plot_timeseries(V[0])
     plt.show()
     #plt.show()
     #dataString = aa.read("concso4")
     #dataString.plot_station_coordinates(markersize=12, color='lime')
     #print(dataString.station_name)
     #abington = dataString.to_station_data("Abington", 'concso4')
     #abington.plot_timeseries('concso4')
     #plt.show()
     
     #dataList =  aa.read(["concso2","concso4"])
     #dataList.plot_station_coordinates(markersize=12, color='red')
     #plt.show()

     #sprint(ungridded.metadata[2.0])
     #when = ungridded.meta_idx[2.0]['concso2']
     #print(ungridded._data[when[0]:when[-1], ungridded._DATAINDEX])

     #dataNone.plot_station_coordinates('wetso4', color='lime')
     #plt.show()
     #ax.figure.savefig('/home/hannas/Desktop/test_stations_aasetal.png')
     #print(ungridded._data[0, :]) #:250
     #print(ungridded.unique_station_names)
     #print(ungridded.metadata[0])


     #stat = ungridded.to_station_data('Abington', "concso4")
     #stat.plot_timeseries("concso4", ax = ax)
     #plt.show()
     #ax = ungridded.plot_station_timeseries('Abington', 'concso2')
     #ax.figure.savefig('/home/hannas/Desktop/test_plot_tseries_first_station.png')

