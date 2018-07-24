#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from collections import OrderedDict as od
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.exceptions import MetaDataError

class ReadAeronetBase(ReadUngriddedBase):
    """TEMPLATE: Abstract base class template for reading of Aeronet data
    
    Extended abstract base class, derived from low-level base class
    :class:`ReadUngriddedBase` that contains some more functionality.
    """
    #: column delimiter in data block of files
    COL_DELIM = ','
    
    #: dictionary specifying the file column names (values) for each Aerocom 
    #: variable (keys)
    VAR_NAMES_FILE = {}
    
    #: dictionary specifying the file column names (values) for each 
    #: metadata key (cf. attributes of :class:`StationData`, e.g.
    #: 'station_name', 'longitude', 'latitude', 'altitude')
    META_NAMES_FILE = {}
    
    def __init__(self, dataset_to_read=None):
        super(ReadAeronetBase, self).__init__(dataset_to_read)
        
        # dictionary that contains information about the file columns
        # is written in method _update_col_index
        self._col_index = od()
        
        # header string referring to the content in attr. col_index. Is 
        # updated whenever the former is updated (i.e. when method
        # _update_col_index is called). Can be used to check if
        # file structure changed between subsequent files so that 
        # col_index is only recomputed when the file structure changes 
        # and not for each file individually
        self._last_col_index_str = None
    
    @property
    def col_index(self):
        """Dictionary that specifies the index for each data column
        
        Note
        ----
        
        Implementation depends on the data. For instance, if the variable 
        information is provided in all files (of all stations) and always in 
        the same column, then this can be set as a fixed dictionary in the 
        __init__ function of the implementation (see e.g. class
        :class:`ReadAeronetSunV2`). 
        In other cases, it may not be ensured
        that each variable is available in all files or the column definition
        may differ between different stations. In the latter case you may 
        automise the column index retrieval by providing the header names for 
        each meta and data column you want to extract using the attribute 
        dictionaries :attr:`META_NAMES_FILE` and :attr:`VAR_NAMES_FILE` by 
        calling :func:`_update_col_index` in your implementation of 
        :func:`read_file` when you reach the line that contains the header 
        information.
        """
        return self._col_index
    
    def _update_col_index(self, col_index_str):
        """Update column information for fast access during read_file
        
        Note
        ----
        If successful (no exceptions raised), then this methods overwrites the 
        current column index information stored in :attr:`col_index`.
        
        Parameters
        ----------
        col_index_str : str
            header string of data table in files
            
        Returns
        -------
        dict
            dictionary containing indices (values) for each data /
            metadata key specified in ``VAR_NAMES_FILE`` and ``META_NAMES_FILE``.
            
        Raises
        ------
        MetaDataError
            if one of the specified meta data columns does not exist in data
        """
        cols = col_index_str.strip().split(self.COL_DELIM)
        mapping = od()
        for idx, info_str in enumerate(cols):
            mapping[info_str] = idx
        col_index = od()
        # find meta indices
        for key, val in self.META_NAMES_FILE.items():
            if not val in mapping:
                raise MetaDataError("Required meta-information string {} could "
                                    "not be found in file header".format(val))
            col_index[key] = mapping[val]
        for key, val in self.VAR_NAMES_FILE.items():
            if val in mapping:
                col_index[key] = mapping[val]    
        self._col_index = col_index
        self._last_col_index_str = col_index_str
        return col_index
    
    
    def read(self, vars_to_retrieve=None, files=None, first_file=None, 
             last_file=None):
        """Method that reads list of files as instance of :class:`UngriddedData`
        
        Parameters
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
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        if files is None:
            if len(self.files) == 0:
                self.get_file_list()
            files = self.files
    
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
            metadata[meta_key]['dataset_name'] = self.DATASET_NAME
            # this is a list with indices of this station for each variable
            # not sure yet, if we really need that or if it speeds up things
            metadata[meta_key]['idx'] = {}
            
            num_times = len(station_data['dtime'])
            
            #access array containing time stamps
            # TODO: check using index instead (even though not a problem here 
            # since all Aerocom data files are of type timeseries)
            times = np.float64(station_data['dtime'])
            
            totnum = num_times * num_vars
            
            #check if size of data object needs to be extended
            if (idx + totnum) >= data_obj._ROWNO:
                #if totnum < data_obj._CHUNKSIZE, then the latter is used
                data_obj.add_chunk(totnum)
            
            
            
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
                
                metadata[meta_key]['idx'][var] = np.arange(start, stop)
            
            idx += totnum  
            meta_key = meta_key + 1.
        
        # shorten data_obj._data to the right number of points
        data_obj._data = data_obj._data[:idx]
        self.data = data_obj
        return data_obj
    

if __name__=="__main__":
    class ReadUngriddedImplementationExample(ReadUngriddedBase):
        _FILEMASK = ".txt"
        DATASET_NAME = "Blaaa"
        SUPPORTED_DATASETS = ['Blaaa', 'Blub']
        __version__ = "0.01"
        PROVIDES_VARIABLES = ["od550aer"]
        
        def __init__(self, dataset_to_read=None):
            if dataset_to_read is not None:
                self.DATASET_NAME = dataset_to_read
        
        @property
        def col_index(self):
            raise NotImplementedError
            
        def read(self):
            raise NotImplementedError
            
        def read_file(self):
            raise NotImplementedError
            
    c = ReadUngriddedImplementationExample(dataset_to_read='AeronetSunV2Lev1.5.daily')
    print(c.DATASET_PATH)
