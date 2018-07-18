#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import abc
import numpy as np
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.ungriddeddata import UngriddedData

class ReadAeronetBase(ReadUngriddedBase):
    """Abstract base class template for reading of Aeronet data
    
    Extended abstract base class, derived from low-level base class
    :class:`ReadUngriddedBase` that contains some more functionality
    """
    DATA_COLNAMES = {}
    METADATA_COLNAMES = {}
    @abc.abstractproperty
    def DEFAULT_VARS(self):
        """List containing default variables to read"""
        
    def read(self, vars_to_retrieve=None, first_file=None, last_file=None):
        """Read all data files into instance of :class:`UngriddedData` object
        
        Parameters
        ----------
        vars_to_retrieve : list
            list of variables that are supposed to be imported
        first_file : int
            index of first file in file list to read. If None, the very first
            file in the list is used
        last_file : int
            index of last file in list to read. If None, the very last file 
            in the list is used
            
        Example
        -------
        >>> from pyaerocom.io import ReadAeronetSdaV3
        >>> obj = ReadAeronetSdaV3()
        >>> obj.read()
        """
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
            
        if len(self.files) == 0:
            self.get_file_list()
        files = sorted(self.files)
        
        if first_file is None:
            first_file = 0
        if last_file is None:
            last_file = len(files)
        
        files = files[first_file:last_file]
        
        self.read_failed = []
        
        data_obj = UngriddedData()
        meta_key = 0.0
        idx = 0
        
        #assign metadata object
        metadata = data_obj.metadata
        
        num_vars = len(vars_to_retrieve)

        for _file in files:
            station_data = self.read_file(_file, vars_to_retrieve=vars_to_retrieve)
            # Fill the metatdata dict
            # the location in the data set is time step dependant!
            # use the lat location here since we have to choose one location
            # in the time series plot
            metadata[meta_key] = {}
            metadata[meta_key].update(station_data.get_meta())
            metadata[meta_key].update(station_data.get_coords())

            # this is a list with indexes of this station for each variable
            # not sure yet, if we really need that or if it speeds up things
            metadata[meta_key]['indexes'] = {}
            
            num_times = station_data.num_timestamps
            totnum = station_data.len_flat(num_vars)
            
            #check if size of data object needs to be extended
            if (idx + totnum) >= data_obj._ROWNO:
                #if totnum < data_obj._CHUNKSIZE, then the latter is used
                data_obj.add_chunk(totnum)
            
            #access array containing time stamps
            times = np.float64(station_data['dtime'])
            
            for var_idx, var in enumerate(vars_to_retrieve):
                values = station_data[var]
                start = idx + var_idx * num_times
                stop = start + num_times
                
                
                #write common meta info for this station
                data_obj._data[start:stop, 
                               data_obj._LATINDEX] = station_data['latitude']
                data_obj._data[start:stop, 
                               data_obj._LONINDEX] = station_data['longitude']
                data_obj._data[start:stop, 
                               data_obj._ALTITUDEINDEX] = station_data['altitude']
                data_obj._data[start:stop, 
                               data_obj._METADATAKEYINDEX] = meta_key
                               
                # write data to data object
                data_obj._data[start:stop, data_obj._TIMEINDEX] = times
                data_obj._data[start:stop, data_obj._DATAINDEX] = values
                data_obj._data[start:stop, data_obj._VARINDEX] = var_idx
                
                metadata[meta_key]['indexes'][var] = np.arange(start, stop)
            
            idx += totnum  
            meta_key = meta_key + 1.
        
        # shorten data_obj._data to the right number of points
        data_obj._data = data_obj._data[:idx]
        self.data = data_obj
        return data_obj
    

if __name__=="__main__":
    
    from pyaerocom import const
    class ReadUngriddedImplementationExample(ReadUngriddedBase):
        _FILEMASK = ".txt"
        DATASET_NAME = "Blaaa"
        __version__ = "0.01"
        PROVIDES_VARIABLES = ["od550aer"]
        REVISION_FILE = const.REVISION_FILE
        
        def __init__(self, dataset_to_read=None):
            if dataset_to_read is not None:
                self.DATASET_NAME = dataset_to_read
        
        def read(self):
            raise NotImplementedError
            
        def read_file(self):
            raise NotImplementedError
            
    c = ReadUngriddedImplementationExample(dataset_to_read='AeronetSunV2Lev1.5.daily')
    print(c.DATASET_PATH)
