# -*- coding: utf-8 -*-
"""Interface for reading DMS data at Amsterdam Island and Cape Verde Observatory.

This file is part of the pyaerocom package.

Example
-------

Reference to notebook with examples?

Notes
-----

Attributes
----------

"""

# TODO: check figures!!!!

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
    DATA_ID = const.DMS_AMS_CVO_NAME
    
    # List of all datasets supported by this interface
    SUPPORTED_DATASETS = [DATA_ID]
    
    # Temporal resolution flag for the supported dataset that is provided in a 
    # defined temporal resolution
    TS_TYPE = 'daily'
    
    # Default variables for read method
    DEFAULT_VARS = ['vmrdms', 'sd']
    
    # Dictionary specifying values corresponding to invalid measurements
    NAN_VAL ={}
    NAN_VAL['vmrdms'] = -999999999999.99
    NAN_VAL['nd'] = -9999
    NAN_VAL['sd'] = -99999.
    NAN_VAL['f'] = -9999
    
    # Dictionary specifying the file column names (values) for each Aerocom 
    # variable (keys)
    VAR_NAMES_FILE = {}
    VAR_NAMES_FILE['vmrdms'] = 'dimethylsulfide'
    VAR_NAMES_FILE['nd'] = 'ND'
    VAR_NAMES_FILE['sd'] = 'SD'
    VAR_NAMES_FILE['f'] = 'F'

    # List of variables that are provided by this dataset (will be extended 
    # by auxiliary variables on class init, for details see __init__ method of
    # base class ReadUngriddedBase)
    PROVIDES_VARIABLES = list(VAR_NAMES_FILE.keys())

    INSTRUMENT_NAME = 'unknown'
    
    @property
    def DATASET_NAME(self): 
        """Name of the dataset"""
        return self.DATA_ID
    
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
         
        # Open the file, store the metadata in the first lines of the file, 
        # skip empty lines and headers, and store the data.
        with open(filename, 'r') as f:         
        
            # metadata (first rows in the file)
            meta = [next(f).split(':', 1)[1] for data in range(26)]

            f.readline()
            f.readline()
            f.readline()
            f.readline()
            f.readline()
            data_keys = f.readline().split()
            
            data = []
            for line in f:
                rows = line.split()
                data.append(rows)
        
        data = np.array(data) 
        # names of the columns in the file that I want to use        
        data_keys = data_keys[5:] 
        # dictionary with keys and column index in the data
        data_idx = { data_keys[i]: i+4 for i in range(0, len(data_keys) ) }
               
        # Empty data object (a dictionary with extended functionality)
        data_out = StationData()    
        data_out.data_id = self.DATA_ID
        data_out.dataset_name = self.DATASET_NAME  # is this supposed to be the same?
                
        # Fill dictionary with relevant metadata and variables from the file.
        # Reformatthe strings, and replace whitespaces in with underscore.
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
            data_out['data_version'] = int(meta[5].strip())  #(meta[5].strip())  #   ??????????????????
        except:
            data_out['data_version'] = None
        data_out['ts_type'] = meta[19].strip().replace(' ', '_')
        data_out['PI_email'] = meta[16].strip().replace(' ', '_')
        data_out['dataaltitude'] = meta[15].strip().replace(' ', '_')
        data_out['variables'] = vars_to_retrieve 
        u = meta[20].strip().replace(' ', '_')
    
        # data in vars_to_retrieve
        # only vmrdms or all??
        for var in vars_to_retrieve:
            # find column
            idx = data_idx[self.VAR_NAMES_FILE[var]]
            # get data
            data_out['var_info'][var] = od()
            if idx == 4:  # vmrdms
                if u == 'ppt':
                    data_out['var_info'][var]['units'] = 'mol mol-1'
                    data_out[var] = np.asarray(data[:, idx]).astype(np.float) * 1e12
                    # reset nan values
                    data_out[var] = np.where(data_out[var]==self.NAN_VAL['vmrdms']*1e12, 
                            self.NAN_VAL['vmrdms'], data_out[var])  
                else:
                    data_out['var_info'][var]['units'] = u
                    data_out[var] = data[:, idx].astype(np.float)
            else:
                data_out['var_info'][var]['units'] = 1  # Or leave empty? 
                data_out[var] = data[:, idx].astype(np.float)
                
        
        # If only vmrdms above, we need to write sd and f
        data_out['f']  = data[:, data_idx[self.VAR_NAMES_FILE['f']]]
        data_out['sd']  = data[:, data_idx[self.VAR_NAMES_FILE['sd']]]
        # Add date and time and the rest of the data to a dictionary
        data_out['dtime'] = []
        #data_out['vmrdms'] = []
        #data_out['nd'] = []
        #data_out['sd'] = []
        #data_out['f'] = []
        
        datestring = np.core.defchararray.add(data[:, 0], 'T')
        datestring = np.core.defchararray.add(datestring, data[:, 1])
        data_out['dtime'] = datestring.astype("datetime64[s]")
        
        #for i in range(1, len(data)):
        #    datestring = data[i][0]  + 'T' + data[i][1]
        #    data_out['dtime'].append(np.datetime64(datestring, 's'))
            #try:
            #    data_out['vmrdms'].append(np.float(data[i][4]))
            #except:
            #    data_out['vmrdms'] = None
            #data_out['vmrdms'].append((data[i][4]))
            #data_out['nd'].append(np.float(data[i][5]))
            #data_out['sd'].append(np.float(data[i][6]))
            #data_out['f'].append(np.int(data[i][7]))
             
        # Convert the data (not the metadata) to arrays
        #data_out['vmrdms'] = np.asarray(data_out['vmrdms'])
        #data_out['nd'] = np.asarray(data_out['nd'])
        #data_out['sd'] = np.asarray(data_out['sd'])
        #data_out['f'] = np.asarray(data_out['f'])
        #data_out['dtime'] = np.asarray(data_out['dtime'])
        
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
            for var in vars_to_retrieve:
                if var in data_out:
                    data_out[var] = pd.Series(data_out[var], 
                                              index=data_out['dtime'])
                
                    
        # We want our units in mole mole-1 for vmrdms
        #if  data_out['var_info']['units'] == 'ppt':
        #    data_out['var_info']['units'] = 'mole mole-1'
        #    data_out['vmrdms'] = data_out['vmrdms'] * 10e12
        
        
        return data_out
    
    def read(self, vars_to_retrieve=None, 
             files=['/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/PYAEROCOM/DMS_AMS_CVO/data/ams137s00.lsce.as.fl.dimethylsulfide.nl.da.dat',
                    '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/PYAEROCOM/DMS_AMS_CVO/data/cvo116n00.uyrk.as.cn.dimethylsulfide.nl.da.dat'],
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
        
        # TODO: the method should be able to read all the files in the directory
        
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
        meta_key = 0.0  # Why 0.0 ??? 
        idx = 0  
        
        # Assign metadata object and index
        metadata = data_obj.metadata
        meta_idx = data_obj.meta_idx
    
        num_vars = len(vars_to_retrieve)


        for i, _file in enumerate(files):
            station_data = self.read_file(_file, 
                                          vars_to_retrieve=vars_to_retrieve)

            # Fill the metadata dict.
            # The location in the data set is time step dependant.
            metadata[meta_key] = od()
            metadata[meta_key].update(station_data.get_meta())
            metadata[meta_key].update(station_data.get_station_coords())
            #metadata[meta_key].update(station_data.get_unit('vmrdms'))
            #metadata[meta_key]['dataset_name'] = self.DATASET_NAME
            #metadata[meta_key]['ts_type'] = self.TS_TYPE
            metadata[meta_key]['variables'] = vars_to_retrieve
            #metadata[meta_key]['data_id'] = self.DATA_ID
            if ('instrument_name' in station_data 
                and station_data['instrument_name'] is not None):
                instr = station_data['instrument_name']
            else:
                instr = self.INSTRUMENT_NAME
            metadata[meta_key]['instrument_name'] = instr
            
            # TODO: Add more keys to var_info
            #var_info = {}
            
            # Var info is a dictionary and it must contain the key 'units' to 
            # be able to do the colocation
            #if (station_data['var_info']['units'] is not None):
            #    u = station_data['var_info']['units']
            #else:
            #    u = 1
                
            #print('unit:', u)
           
            # 
            #metadata[meta_key]['var_info']['units'] = u
            #print(metadata[meta_key]['var_info']['units'])
            
            
            # List with indices of this station for each variable
            meta_idx[meta_key] = od()
            
            num_times = len(station_data['dtime'])

            totnum = num_times * num_vars
            
            # Check whether the size of the data object needs to be extended
            if (idx + totnum) >= data_obj._ROWNO:
                # if totnum < data_obj._CHUNKSIZE, then the latter is used
                data_obj.add_chunk(totnum)
                     
            for var_idx, var in enumerate(vars_to_retrieve):
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
                # Write data to data object
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
        data_obj.data_revision[self.DATASET_NAME] = self.data_revision
        self.data = data_obj
        
        print(self)
        return data_obj
    
if __name__ == "__main__":
    
    # References: 
    # https://agupubs.onlinelibrary.wiley.com/doi/epdf/10.1029/2000JD900236
    # https://aerocom.met.no/DATA/AEROCOM_WORK/oxford10/pdf_pap/suntharalingam_sulfate_2010.pdf
     
    r = ReadGAW()
    data = r.read(vars_to_retrieve = ['vmrdms', 'f'])
    print('vars to retrieve:', data.vars_to_retrieve)
    
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
    
    # 2004-2008
    # plot monthly mean
    dms_ai = data['Amsterdam_Island'].vmrdms
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
  



 