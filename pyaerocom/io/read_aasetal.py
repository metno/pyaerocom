import numpy as np
import os
import pandas as pd
#from datetime import datetime
import matplotlib.pyplot as plt
#import od
from collections import OrderedDict

from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.io.readungriddedbase import ReadUngriddedBase

class ReadSulphurAasEtAl(ReadUngriddedBase):
    """Interface for reading subset of GOL TAT data related to the nature paper.

    See Also
    ---------
        :class:`ReadUngriddedBase`
 
	"""
    # name of files in GawTadSubsetAasEtAl
    _FILEMASK = '*.csv' # fix

    #: version log of this class (for caching)
    __version__ = '0.02'

    COL_DELIM = ','

    #: Temporal resoloution
    TS_TYPE = 'monthly'

    #: Name of dataset (OBS_ID)
    DATA_ID = 'GAWTADsubsetAasEtAl'

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [DATA_ID]

    #: value corresponding to invalid measurement
    #NAN_VAL = -9999.
    NAN_VAL = -999.
    #: List of variables that are provided by this dataset (will be extended
    #: by auxiliary variables on class init, for details see __init__ method of
    #: base class ReadUngriddedBase)
    # This contains the mapping between the requested variables and what it is called in the files.
    
    #: Dictionary mapping variable name to the keys present in the files. 
    VAR_TO_KEY = {}
    VAR_TO_KEY["sconcso4pr"] = "concentration_mgS/L"
    VAR_TO_KEY["pr"] = 'precip_amount_mm'
    VAR_TO_KEY["wetso4"] = "deposition_kgS/ha"
    VAR_TO_KEY["sconcso2"] = 'concentration_ugS/m3'
    VAR_TO_KEY["sconcso4"] = 'concentration_ugS/m3'

    #: Dictionary mapping filenames to available variables in the respective files. 
    FILES_CONTAIN = {}
    FILES_CONTAIN['monthly_so2.csv'] = ['sconcso2']
    FILES_CONTAIN['monthly_so4_aero.csv'] = ['sconcso4']
    FILES_CONTAIN['monthly_so4_precip.csv'] = ['wetso4', 'pr', 'sconcso4pr']
    
    #: Dictionary mapping variable name to hard coded filenames. 
    VARS_TO_FILES = {}
    VARS_TO_FILES['sconcso2'] = ['monthly_so2.csv']
    VARS_TO_FILES['sconcso4'] = ['monthly_so4_aero.csv']
    VARS_TO_FILES['pr'] = ['monthly_so4_precip.csv']
    VARS_TO_FILES['wetso4'] = ['monthly_so4_precip.csv']
    VARS_TO_FILES['sconcso4pr'] = ['monthly_so4_precip.csv']

    #: :obj: `list` of :obj: `str` 
    #: List containing all the variables available in this data set.
    PROVIDES_VARIABLES = list(VAR_TO_KEY.keys())
    
    #: int: Number of available variables in this data set.
    num_vars = len(PROVIDES_VARIABLES)

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
       

# =============================================================================
#         def pad_zeros(array):
#             """ Try to do this vectorized,
#             Problem with the only one digit in front of numbers smaller than xero.            
#             """
#             
#             str_array = array.astype("str")
#             
#             for i, val in enumerate(array):
#                 if val < 10: 
#                 # Add zeros 
#                     str_array[i] = "0"+str(val)
#             return str_array
# =============================================================================

        station_list = []
        #print(vars_to_retrieve)
        df = pd.read_csv(filename, sep=",", low_memory=False)
        
        # 
        tconv = lambda yr, m : np.datetime64('{:04d}-{:02d}-{:02d}'.format(yr, m, 1), 's')
        
        dates_alt = [tconv(yr, m) for yr, m in 
                     zip(df.year.values, df.month.values)]
        
# =============================================================================
#         #days = np.ones((len(df["year"]))).astype('int')
#         #df['day'] = days
#         #df['dtime'] = df.apply(lambda row: datetime(row['year'], row['month'], row["day"]), axis=1) 
#         month = pad_zeros(df['month'].astype(int))
#         #print(month)
#                
#         year = df['year'].values.astype(int).astype("str")        
#         days = np.array(["01" for i in range(len(year)) ])
#         
#         dates = [y + "-" + m + "-" + d for y, m, d in zip(year, month, days)]
# =============================================================================
        
        df['dtime'] = np.array(dates_alt)  

        # array av numpy.datetime64
        df.rename(columns= {"Sampler":"instrument_name"}, inplace=True)
        #df.pop("year")
        #df.pop("month")
        #df.pop("day")
        grouped = df.groupby(by = "station_name")

        # Looping over every station:
        for name, station_group in grouped:

            s = StationData()
            # Meta data
            s['station_name'] = name
            s["altitude"] = np.nan
            s["filename"] = filename
            s["data_id"] = self.DATA_ID
            s["ts_type"] = self.TS_TYPE
            s['variables'] = []
            
            # The variables present in this file is the intersection between 
            # the keys in the file and the variables name available, 
            # here expressed in terms of their keynames in order to retrieve them.
            variables_present = list(set(station_group.keys()).intersection(
                                                    self.VAR_TO_KEY.values()))

            # Looping over all keys in the grouped data frame.
            for key in station_group: # NOT YEAR OR MONTH, BUT WOULD LIKE TO KEEP THOSE.
                # Enters if the the key is a variable
                if key in variables_present:
                    # Looping over all varibales to retrieve
                    for var in vars_to_retrieve:
                        if var == "wetso4":
                            # input unit is kg S/ha
                            y = station_group['year'].values
                            m = station_group['month'].values
                            
                            monthly_to_sec = days_in_month(y, m)*24*60*60             
                            mass_sulhpor = pd.to_numeric(station_group[key], 
                                                         errors='coerce').values
                            s[var] = unitconversion_wet_deposition(mass_sulhpor, 
                             "monthly")/monthly_to_sec#monthly_to_sec[:156]
                            # output variable is ks so4 m-2s-1
                        else:
                            # Other variable have the correct unit.
                            s[var] = pd.to_numeric(station_group[key], 
                                                   errors='coerce').values
                        # Adds the variable
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
        """
        Method that reads list of files as instance of :class:`UngriddedData`

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
        UngriddedData
            data object
            
        """
        files = self.get_file_list()
                
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        data_obj = UngriddedData()

        meta_key = 0.0
        idx = 0
        varindex = -1 # might cause trouble
        
        #assign metadata object
        metadata = data_obj.metadata # OrderedDict
        meta_idx = data_obj.meta_idx # OrderedDict

        for file in files:
            filename = os.path.basename(file)
            if not filename in self.FILES_CONTAIN:
                raise IOError('Invalid file name {}, this should not happen'
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
                    #var_count += varindex
                    values = station_data[var]
                    start = idx + var_count * num_times
                    stop = start + num_times

                    if not var in data_obj.var_idx:
                        varindex += 1
                        data_obj.var_idx[var] = varindex
                        var_idx = varindex
                        print("adding var {} (assigned index: {})".format(var, varindex))
                    else:
                        var_idx = data_obj.var_idx[var]

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
        data_obj.data_revision[self.DATA_ID] = self.data_revision
        self.data = data_obj # initalizing a pointer to it selves
        return data_obj
    
def is_leap_year(year):
    """
    Returns boolean:
        True : its a leap year.
        False : its not.
    """
    return (year % 4 == 0) and (year % 100 != 0) or (year % 400 == 0)

def days_in_month(years, months):
    """
    Returns one array of values containing the number of values in a specific 
    month. 
    """
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    index_feb = np.where(months==2)[0]
    nr_of_days = []
    if len(index_feb) == 0:
        nr_of_days = np.array([days[m-1] for m in months])
        print(nr_of_days)
        return nr_of_days
    else:
        for counter, m in enumerate(months):
            if is_leap_year(years[counter]) and m == 2:
                nr_of_days.append(29)
            else:
                nr_of_days.append(days[m-1])
        return np.array(nr_of_days)

def unitconversion_wet_deposition(data, ts_type="monthly"):
    """
    Converting:  ug S/ ha to ug SOx/m2 
    Adding mass of oksygen.
    
    Parameters:
    ------------------
    data: array-like
    
    ts_type: Default monthly
    The timeseries type.
    
    Return:
    ------------
    data in units of ug sox/m3
    """
    # TODO : add for a different number of days in one year.
    mm_s = 0.001*32.065 # in kilos pr mol
    mm_o = 4*15.9999*0.001 # molar mass of four okygen atom ins 
    
    nr_molecules = mass_to_nr_molecules(data, mm_s) # in the order of 10**27 
    added_weight_oksygen = nr_molecules_to_mass(nr_molecules, mm_o)
    mass = data + added_weight_oksygen
    return mass*10000

def mass_to_nr_molecules(mass, Mm):
    """
    Mass, Molar mass need to be in the same unit, either both g and g/mol 
    or kg and kg/mol.
    """
    A = 6.022*10**23
    #TODO: this assumes you have one 
    return mass/Mm*A    

def nr_molecules_to_mass(nr_molecules, Mm):
    """
    Molar mass in the unit you want mass returned in
    Molar mass in grams pr kilo
    """
    A = 6.022*10**23
    return Mm*nr_molecules/A
    
def unitconversion_surface_consentrations(data, nr_of_O = 2):
    """
    Converting:  ugS/ m3 to ug sox/m3
    
    Parameters:
    ------------------
    data: array-like
    Contains the data in units of ugS/m3.
    
    nr_of_O: int
    The number of O's in you desired SOx compound.
    
    Return:
    ------------
    data in units of ug SOx/m3
    
    """
    mm_s = 32.065*10**6 # in units of ug/mol
    mm_o = nr_of_O*15.9999*10**6 ## in units of ug/mol
    nr_molecules = mass_to_nr_molecules(data, mm_s) # 32.065*10**6) [ug/mol]
    added_weight_oksygen = nr_molecules_to_mass(nr_molecules, mm_o) # ug
    # added weights in micrograms 
    mass = data + added_weight_oksygen # in micrograms
    return mass
    
def unitconversion_wet_deposition_back(data, ts_type = "monthly"):
    """
    Converting:  ug SOx/m3 to ugS/ m3. 
    Removing mass of oxygen. 
    
    Parameters:
    ------------------
    data: array-like
    
    ts_type: Default monthly
    The timeseries type.
    
    Return:
    ------------------
    data in units of ug SOx/m3
    """
    mm_compund = 0.001*32.065 + 0.001*15.999*4
    mm_s = 0.001*32.065
    #A = 6.022*10**23
    # TODO : add for a different number of days in one year.
    nr_molecules = nr_molecules_to_mass(data, mm_compund) # in the order of 10**27 
    #added_weight_oksygen = nr_molecules*4*15.9999*0.001/
    #mass = data - added_weight_oksygen
    mass_S = nr_molecules_to_mass(nr_molecules, mm_s)
    return mass_S/10000 # to be multiplied by the numebers of days in a month

def unitconversion_surface_consentrations_back(data, nr_of_O = 2):
    """
    Converting: ug SOx/m3 to  ugS/ m3.
    
    Parameters:
    ------------------
    data: array-like
    Contains the data in units of ug ugS/m3.
    
    nr_of_O: int
    The number of O's in you desired SOx compound.
    
    Return:
    ------------
    data in units of ugS/ m3.
    """

    mmO = nr_of_O*15.9999*10**6
    mmS = 32.065
    
    nr_molecules = data/ (nr_of_O*mmO*10**6) * (6.022*10**23)
    weight_sox = nr_molecules*mmS*10**6 # in micrograms
    # added weights in micrograms 
    return weight_sox

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

     #change_verbosity('info')
     V = "wetso4"
     aa = ReadSulphurAasEtAl('GAWTADsubsetAasEtAl')
     
     #so2 = aa.read('sconcso2')
     #so4_aero = aa.read('sconcso4')
     
     
     dataNone = aa.read(V)#['sconcso4', 'sconcso2']
     name = 'Abington'
     abington = dataNone.to_station_data("Oulanka", V)
     abington.plot_timeseries(V)
     
     #abington2 = dataNone.to_station_data("Oulanka", 'sconcso2')
     #abington2.plot_timeseries('sconcso2')
     
     plt.show()
    #dataString = aa.read("sconcso4")
     #dataString.plot_station_coordinates(markersize=12, color='lime')
     #print(dataString.station_name)
     #abington = dataString.to_station_data("Abington", 'sconcso4')
     #abington.plot_timeseries('sconcso4')
     #plt.show()
     
     #dataList =  aa.read(["sconcso2","sconcso4"])
     #dataList.plot_station_coordinates(markersize=12, color='red')
     #plt.show()

     #sprint(ungridded.metadata[2.0])
     #when = ungridded.meta_idx[2.0]['sconcso2']
     #print(ungridded._data[when[0]:when[-1], ungridded._DATAINDEX])

     #dataNone.plot_station_coordinates('wetso4', color='lime')
     #plt.show()
     #ax.figure.savefig('/home/hannas/Desktop/test_stations_aasetal.png')
     #print(ungridded._data[0, :]) #:250
     #print(ungridded.unique_station_names)
     #print(ungridded.metadata[0])


     #stat = ungridded.to_station_data('Abington', "sconcso4")
     #stat.plot_timeseries("sconcso4", ax = ax)
     #plt.show()
     #ax = ungridded.plot_station_timeseries('Abington', 'sconcso2')
     #ax.figure.savefig('/home/hannas/Desktop/test_plot_tseries_first_station.png')

