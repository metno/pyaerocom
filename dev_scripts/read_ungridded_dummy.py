#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 11:38:43 2018

@author: jonasg
"""
from pyaerocom.io import ReadUngriddedBase
from pyaerocom import UngriddedData
import numpy as np

class ReadDummy(ReadUngriddedBase):
    _FILEMASK = '*.txt'
    __version__ = 0.01
    
    DATASET_NAME = 'AEOLUS'
    SUPPORTED_DATASETS = ['AEOLUS']
    
    DEFAULT_VARS = ['od550aer']
    PROVIDES_VARIABLES = ['od550aer']
    
    def read_file(self, vars_to_retrieve=None):
        # this method checks if all variables in input array can be provided 
        # by this interface. 
        vars_to_read, vars_to_compute = self.check_vars_to_retrieve(vars_to_retrieve)
        
        data_out = {}
        
        #write your file read here
        # ...
        # ...
        # return read data object
        return data_out
    
    def read(self, vars_to_retrieve):
        # Leeres Datenobjekt anlegen
        data_obj = UngriddedData()
        
        # date index pointer in numpy array
        index_pointer = 0
        
        # metadata key pointer for each file
        meta_key = 0.0
        
        # ist in der Basisklasse implementiert, kann aber auch ueberschrieben werden, falls noetig
        files = self.get_file_list()
        for f in files:
            # load data from individual file (returns e.g. dictionary, or StationData)
            file_data = self.read_file()
            for var_idx, var in enumerate(vars_to_retrieve):
                # add station / file metadata e.g.
                data_obj.metadata[meta_key]['longitude'] = file_data['longitude']
                data_obj.metadata[meta_key]['latitude'] = file_data['latitude']
                data_obj.metadata[meta_key]['altitude'] = file_data['altitude']
                
                # now copy all data columns
                
                # time stamps, assuming array or list of numpy.datetime64 objects
                time_stamps = file_data['dtime'] 
                
                # the actual data for this variable
                var_data = file_data[var] 
                
                # the number of datapoints added to the Ungridded data object
                add_num = len(var_data)
                stop_idx = index_pointer + add_num
                if stop_idx >= data_obj._ROWNO:
                    # add_chunk actually adds a minimum of 1000 datapoints, it only uses add_num if add_num >= 1000
                    data_obj.add_chunk(add_num)
                
                # now you can add the variable to the data numpy array
                data_obj._data[index_pointer:stop_idx, 
                                                data_obj._LATINDEX] = file_data['latitude']
                data_obj._data[index_pointer:stop_idx,
                               data_obj._LONINDEX] = file_data['longitude']
                data_obj._data[index_pointer:stop_idx,
                               data_obj._ALTITUDEINDEX] = file_data['altitude']
                data_obj._data[index_pointer:stop_idx,
                               data_obj._METADATAKEYINDEX] = meta_key
                              
                # write data to data object
                data_obj._data[index_pointer:stop_idx, data_obj._TIMEINDEX] = np.float64(time_stamps)
                data_obj._data[index_pointer:stop_idx, data_obj._DATAINDEX] = var_data
                data_obj._data[index_pointer:stop_idx, data_obj._DATAHEIGHTINDEX] = file_data['altitude'] #or data
                data_obj._data[index_pointer:stop_idx, data_obj._VARINDEX] = var_idx
                
                index_pointer += add_num
                
            meta_key += 1.
                
if __name__ == "__main__":
    dummy = ReadDummy()
    dummy.get_file_list()