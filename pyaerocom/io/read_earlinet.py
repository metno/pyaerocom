################################################################
# read_aeronet_earlinet.py
#
# read Aeronet direct sun V2 data
#
# this file is part of the pyaerocom package
#
#################################################################
# Created 20171026 by Jan Griesfeller for Met Norway
#
# Last changed: See git log
#################################################################

# Copyright (C) 2017 met.no
# Contact information:
# Norwegian Meteorological Institute
# Box 43 Blindern
# 0313 OSLO
# NORWAY
# E-mail: jan.griesfeller@met.no
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA
import os, fnmatch
from collections import OrderedDict as od
import numpy as np
import xarray
from pyaerocom import const
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom import StationData, VerticalProfile, Variable
from pyaerocom import UngriddedData

# TODO: Include backscatter signal ???
# TODO: Check file order 
# TODO: Check station names -> they are NOT UNIQUE (e.g. Potenza...) -> maybe
class ReadEarlinet(ReadUngriddedBase):
    """Interface for reading of EARLINET data"""
    #: Mask for identifying datafiles 
    _FILEMASK = '*.e*'
    
    #: version log of this class (for caching)
    __version__ = "0.07_" + ReadUngriddedBase.__baseversion__
    
    #: Name of dataset (OBS_ID)
    DATASET_NAME = const.EARLINET_NAME
    
    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [const.EARLINET_NAME]
    
    #: default variables for read method
    DEFAULT_VARS = ['zdust', 'ec5503daer', 'ec5503daer_err']
    
    Z3D_VARNAME = 'Altitude'
    
    #: dictionary specifying the file search patterns for each variable
    VAR_PATTERNS_FILE = {'ec5503daer'       : '*/f*/*.e5*', 
                         'ec5503daer_err'   : '*/f*/*.e5*',
                         'ec5323daer'       : '*/f*/*.e5*', 
                         'ec5323daer_err'   : '*/f*/*.e5*', 
                         'ec3553daer'       : '*/f*/*.e3*', 
                         'ec3553daer_err'   : '*/f*/*.e3*', 
                         'zdust'            : '*/f*/*.e*'}
    
    #: dictionary specifying the file column names (values) for each Aerocom 
    #: variable (keys)
    VAR_NAMES_FILE = {'ec5503daer'      : 'Extinction', 
                      'ec5503daer_err'  : 'ErrorExtinction', 
                      'ec5323daer'      : 'Extinction', 
                      'ec5323daer_err'  : 'ErrorExtinction', 
                      'ec3553daer'      : 'Extinction', 
                      'ec3553daer_err'  : 'ErrorExtinction', 
                      'zdust'           : 'DustLayerHeight'}
        
    META_NAMES_FILE = od(location           = 'Location',
                         start_date         = 'StartDate',
                         start_time_utc     = 'StartTime_UT',
                         stop_time_utc      = 'StopTime_UT',
                         stat_lon           = 'Longitude_degrees_east',
                         stat_lat           = 'Latitude_degrees_north',
                         wavelength_emis    = 'EmissionWavelength_nm',
                         wavelength_det     = 'DetectionWavelength_nm',
                         res_raw_m          = 'ResolutionRaw_meter',
                         zenith_ang_deg     = 'ZenithAngle_degrees',
                         system             = 'System',
                         comments           = 'Comments',
                         shots_avg          = 'ShotsAveraged',
                         detection_mode     = 'DetectionMode',
                         res_eval           = 'ResolutionEvaluated',
                         input_params       = 'InputParameters',
                         stat_alt           = 'Altitude_meter_asl',
                         eval_method        = 'EvaluationMethod')

    PROVIDES_VARIABLES = ['ec5503daer', 'ec5503daer_err',
                          'ec5323daer', 'ec5323daer_err',
                          'ec3553daer', 'ec3553daer_err',
                          'zdust']

    def __init__(self, dataset_to_read=None):
        # initiate base class
        super(ReadEarlinet, self).__init__(dataset_to_read)
        # make sure everything is properly set up
        if not all([x in self.VAR_PATTERNS_FILE for x in self.PROVIDES_VARIABLES]):
            raise AttributeError("Please specify file search masks in "
                                 "header dict VAR_PATTERNS_FILE for each "
                                 "variable defined in PROVIDES_VARIABLES")
        elif not all([x in self.VAR_NAMES_FILE for x in self.PROVIDES_VARIABLES]):
            raise AttributeError("Please specify file search masks in "
                                 "header dict VAR_NAMES_FILE for each "
                                 "variable defined in PROVIDES_VARIABLES")
        #: private dictionary containing loaded Variable instances, 
        self._var_info = {}
    
    def read_file(self, filename, vars_to_retrieve=None):
        """Read EARLINET file and return it as instance of :class:`StationData`
        
        Parameters
        ----------
        filename : str
            absolute path to filename to read
        vars_to_retrieve : :obj:`list`, optional
            list of str with variable names to read. If None, use
            :attr:`DEFAULT_VARS`
    
        Returns
        -------
        StationData 
            dict-like object containing results
        """
        # implemented in base class
        vars_to_read, vars_to_compute = self.check_vars_to_retrieve(vars_to_retrieve)
        
        if len(vars_to_compute) > 0:
            raise NotImplementedError("This feature has not yet implemented, as "
                                      "it was not required so far. The "
                                      "implementation requires handling of "
                                      "profile data as well")
        #create empty data object (is dictionary with extended functionality)
        data_out = StationData()
        data_out['stat_code'] = filename.split('/')[-3]
        data_out['dataset_name'] = self.DATASET_NAME
           
        # create empty arrays for all variables that are supposed to be read
        # from file
        for var in vars_to_read:
            if not var in self._var_info:
                self._var_info[var] = Variable(var)
        var_info = self._var_info
            
        
        # Iterate over the lines of the file
        self.logger.debug("Reading file {}".format(filename))
        
        data_in = xarray.open_dataset(filename)
        
        for k, v in self.META_NAMES_FILE.items():
            try:
                val = data_in.attrs[v]
            except:
                val = "FAILED_TO_READ"
            data_out[k] = val
        
        # get station name and country
        spl = data_out['location'].split(',')
        data_out['station_name'] = spl[0].strip()
        try:
            data_out['country'] = spl[1].strip()
        except:
            self.logger.warning('Unusual location string detected. Earlinet '
                                'location string expected to be comma separated '
                                'city, country information, got: '
                                '{}'.format(data_out['location']))
        
        str_dummy = str(data_in.StartDate)
        year = str_dummy[0:4]
        month = str_dummy[4:6]
        day = str_dummy[6:8]

        str_dummy = str(data_in.StartTime_UT).zfill(6)
        hours = str_dummy[0:2]
        minutes = str_dummy[2:4]
        seconds = str_dummy[4:6]
        datestring = '-'.join([year, month, day])
        datestring = 'T'.join([datestring, ':'.join([hours, minutes, seconds])])
        
        # Earlinet files only contain one timestamp
        dtime = np.datetime64(datestring)
        data_out['dtime'] = dtime
        data_out['has_zdust'] = False
        contains_vars = []
        for var in vars_to_read:
            netcdf_var_name = self.VAR_NAMES_FILE[var]
            # check if the desired variable is in the file
            if netcdf_var_name not in data_in.variables:
                self.logger.warning("Variable {} not found in file {}".format(var, filename))
                continue
            
            info = var_info[var]
            val = np.float64(data_in.variables[netcdf_var_name])
            # 1D variable
            if var == 'zdust':
                if not val.ndim == 0:
                    raise ValueError('Fatal: dust layer height data must be '
                                     'single value')
                if np.isnan(val) or not info.lower_limit <= val <= info.upper_limit :
                    self.logger.warning("Invalid value of variable zdust "
                                        "in file {}. Skipping...!".format(filename))
                    continue
               
                data_out['has_zdust'] = True
                data_out[var] = float(val)
                

            elif var.startswith('ec'):
                if not val.ndim == 1:
                    raise ValueError('Extinction data must be one dimensional')
                wvlg = np.float64(var[2:5])
                wvlg_str = self.META_NAMES_FILE['wavelength_emis']
                
                if not wvlg == data_in.attrs[wvlg_str]:
                    self.logger.info('No wavelength match')
                    continue
                
                # create instance of ProfileData
                profile = VerticalProfile(var)
                profile.altitude = np.float64(data_in.variables[self.Z3D_VARNAME])
                profile.data  = val
                profile.dtime = dtime
                
                data_out[var] = profile
            else:
                raise NotImplementedError
            contains_vars.append(var)
        data_out['contains_vars'] = contains_vars
        return (data_out)
    
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
        
        self.read_failed = []
        
        data_obj = UngriddedData()
        meta_key = -1.0
        idx = 0
        
        #assign metadata object
        metadata = data_obj.metadata
        meta_idx = data_obj.meta_idx
        
        last_stat_code = ''
        num_files = len(files)
        for i, _file in enumerate(files):
            self.logger.info('File {} ({})'.format(i, num_files))
            try:
                station_data = self.read_file(_file, vars_to_retrieve=
                                              vars_to_retrieve)
                if not any([var in station_data.contains_vars for var in 
                            vars_to_retrieve]):
                    self.logger.info("Station {} contains none of the desired "
                                     "variables. Skipping station..."
                                     .format(station_data.station_name))
                    continue
                stat_code = station_data['stat_code']
                if last_stat_code != stat_code:
                    meta_key += 1
                    # Fill the metatdata dict
                    # the location in the data set is time step dependant!
                    # use the lat location here since we have to choose one location
                    # in the time series plot
                    metadata[meta_key] = od()
                    metadata[meta_key].update(station_data.get_meta())
                    metadata[meta_key].update(station_data.get_station_coords())
                    metadata[meta_key]['dataset_name'] = self.DATASET_NAME
                    metadata[meta_key]['variables'] = []
                    # this is a list with indices of this station for each variable
                    # not sure yet, if we really need that or if it speeds up things
                    meta_idx[meta_key] = od()
                    last_stat_code = stat_code
                
                # Is floating point single value
                time = station_data.dtime
                for var_idx, var in enumerate(station_data.contains_vars):
                    val = station_data[var]
                    if isinstance(val, VerticalProfile):
                        add = len(val)
                        altitude = val.altitude
                        data = val.data
                    else:
                        add = 1
                        altitude = np.nan
                        data = val
                    stop = idx + add
                    #check if size of data object needs to be extended
                    if stop >= data_obj._ROWNO:
                        #if totnum < data_obj._CHUNKSIZE, then the latter is used
                        data_obj.add_chunk(add)
                    
                    #write common meta info for this station
                    data_obj._data[idx:stop, 
                                   data_obj._LATINDEX] = station_data['latitude']
                    data_obj._data[idx:stop, 
                                   data_obj._LONINDEX] = station_data['longitude']
                    data_obj._data[idx:stop, 
                                   data_obj._ALTITUDEINDEX] = station_data['altitude']
                    data_obj._data[idx:stop, 
                                   data_obj._METADATAKEYINDEX] = meta_key
                                   
                    # write data to data object
                    data_obj._data[idx:stop, data_obj._TIMEINDEX] = time
                    data_obj._data[idx:stop, data_obj._DATAINDEX] = data
                    data_obj._data[idx:stop, data_obj._DATAHEIGHTINDEX] = altitude
                    data_obj._data[idx:stop, data_obj._VARINDEX] = var_idx
                    
                    if not var in meta_idx[meta_key]:
                        meta_idx[meta_key][var] = []
                    meta_idx[meta_key][var].extend(list(range(idx, stop)))
                    
                    if not var in metadata[meta_key]['variables']:
                        metadata[meta_key]['variables'].append(var)
                    if not var in data_obj.contains_vars:
                        data_obj.contains_vars.append(var)
                    idx += add
            except:
                self.read_failed.append(_file)
                self.logger.exception('Failed to read file {}'.format(os.path.basename(_file)))
                
        # shorten data_obj._data to the right number of points
        data_obj._data = data_obj._data[:idx]
        self.data = data_obj
        return data_obj
        
    def get_file_list(self, vars_to_retrieve=None):
        """Perform recusive file search for all input variables
        
        Note
        ----
        Overloaded implementation of base class, since for Earlinet, the 
        paths are variable dependent
        
        Parameters
        ----------
        vars_to_retrieve : list
            list of variables to retrieve
        
        Returns
        -------
        list
            list containing file paths
        """
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        self.logger.info('Fetching data files. This might take a while...')
        patterns = [self.VAR_PATTERNS_FILE[var] for var in vars_to_retrieve]
        matches = []
        for root, dirnames, files in os.walk(self.DATASET_PATH):
            for pattern in patterns:
                paths = [os.path.join(root, f) for f in files]
                for path in fnmatch.filter(paths, pattern):
                    matches.append(path)
        self.files = files = list(dict.fromkeys(matches))
        return files

if __name__=="__main__":
    F0 = '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/Earlinet/data/ev/f2010/ev1008192050.e532'
    F150 = '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/Earlinet/data/kb/f2001/kb0108091955.e532'
    read = ReadEarlinet()
    read.verbosity_level = 'info'
    
    data = xarray.open_dataset(F150)
    print(data)
    dat = read.read_file(F150, vars_to_retrieve=read.PROVIDES_VARIABLES)
    print(dat)
    
    from time import time
    t0=time()
    #data = read.read(vars_to_retrieve='zdust', first_file=345, last_file=1000)
    print("Elapsed time read all zdust: {} s".format(time() - t0))
    stat_test = False
    if stat_test:
        all_stats = []
        stat = ''
        last_stat = ''
        files = read.get_file_list()
        problematic = []
        read_failed = []
        for i, file in enumerate(files):
            ok = True
            try:
                data = xarray.open_dataset(file)
            except:
                read_failed.append(file)
                ok = False
            if ok:
                stat = data.attrs['Location'].split(',')[0].strip()
                if stat != last_stat:
                    print('New location: {} (file no. {})'.format(stat, i))
                    lon = data.attrs['Longitude_degrees_east']
                    lat = data.attrs['Latitude_degrees_north']
                    print("Lon / lat: ({:.3f}, {:.3f})".format(lon, lat))
                    
                    if stat in all_stats:
                        print('Order not conserved')
                        problematic.append(stat)
                    all_stats.append(stat)
                last_stat = stat
            
        
            
    