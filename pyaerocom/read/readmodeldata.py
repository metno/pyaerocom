#!/usr/bin/env python3

################################################################
# readmodeldata.py
#
# model data reading class
#
# this file is part of the aerocom_pt package
#
#################################################################
# Created 20171030 by Jan Griesfeller for Met Norway
#
# Last changed: See git log
#################################################################

#Copyright (C) 2017 met.no
#Contact information:
#Norwegian Meteorological Institute
#Box 43 Blindern
#0313 OSLO
#NORWAY
#E-mail: jan.griesfeller@met.no
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#MA 02110-1301, USA


import os
import glob
from collections import OrderedDict
import sys
import numpy as np
import pandas as pd
import re

import iris
from iris.experimental.equalise_cubes import equalise_attributes
from iris.util import unify_time_units
from iris.time import PartialDateTime

import pyaerocom.config as const
from pyaerocom.custom_exceptions import IllegalArgumentError
from pyaerocom.read.suppl import FileConventionRead

class ReadModelData:
    """Class that can be used to import model data from multiple models
    
    The result
    Note
    -----
    """
    MODELDIRS = const.MODELDIRS
    # "private attributes (defined with one underscore). These may be 
    # controlled using getter and setter methods (@property operator)
    _start_time = None
    _stop_time = None
    def __init__(self, model_ids, start_time=None, stop_time=None, verbose=False):
        
        if isinstance(model_ids, str):
            model_ids = [model_ids]
        if not isinstance(model_ids, list) or not all([isinstance(x, str) for x in model_ids]):
            raise IllegalArgumentError("Please provide string or list of strings")
    
        self.model_ids = model_ids
        self.data = {}
        #control dictionary with parameters that are determined at init
        self.ctrl = {}
    
        self.verbose = verbose
        
        # only overwrite if ther is input, note that the attributes
        # start_time and stop_time are defined below as @property getter and
        # setter methods, that ensure that the input is convertible to 
        # pandas.Timestamp
        if start_time is not None:
            self.start_time = start_time
        if stop_time is not None:
            self.stop_time = stop_time
        
        #self.FILEMASKS = []
        
        self.init_results()
        if self.search_model_dirs():
            self.get_model_files()
    
    @property
    def start_time(self):
        """Get / set the desired start time of the data import
        
        Note
        ----
        Input must be convertable into :class:`pandas.Timestamp` object
        """
        t = self._start_time
        if not isinstance(t, pd.Timestamp):
            raise ValueError("Start time is not set in reading engine")
        return t
    
    @start_time.setter
    def start_time(self, value):
        try:
            self._start_time = pd.Timestamp(value)
        except:
            raise ValueError("Failed to convert input value to pandas "
                              "Timestamp: %s" %value)
            
    @property
    def stop_time(self):
        """Get / set the desired stop time of the data import
        
        Note
        ----
        Input must be convertable into :class:`pandas.Timestamp` object
        """
        t = self._stop_time
        if not isinstance(t, pd.Timestamp):
            raise ValueError("Stop time is not set in reading engine")
        return t
    
    @stop_time.setter
    def stop_time(self, value):
        try:
            self._stop_time = pd.Timestamp(value)
        except:
            raise ValueError("Failed to convert input value to pandas "
                              "Timestamp: %s" %value)
    
    @property
    def years_to_load(self):
        """Array containing year numbers that are supposed to be loaded
        
        Returns
        -------
        ndarray
        """
        return np.arange(self.start_time.year, self.stop_time.year + 1, 1)
    
    def init_results(self):
        """Initiate the import result attributes"""
        self.data = {}
        #control struct with parameters that are determined at init
        self.ctrl = {}
        for model_id in self.model_ids:
            self.data[model_id] = {}
            self.ctrl[model_id] = {}
            self.ctrl[model_id]['model_dir'] = ''  #save the location in there
            self.ctrl[model_id]['year_pos'] = -1    #pos of year in filename
            self.ctrl[model_id]['var_pos'] = -1    #pos of variable name in filename
            self.ctrl[model_id]['ts_pos'] = -1    #pos of time ste[p name in filename (daily, monthly, 3hourly, hourly)
            self.ctrl[model_id]['files'] = []    #array with file names
            self.ctrl[model_id]['vars'] = []    #array with variable names
            self.ctrl[model_id]['file_sep'] = ''    #file seperator
    
    def search_model_dirs(self):
        """Get the directory where model data for a given model resides in
        
        Returns
        -------
        bool
            True, if directory could be found, else False
        """
        for model_id in self.model_ids:
            # loop through the list of models
            for search_dir in self.MODELDIRS:
                if self.verbose:
                    print('Searching in: ', search_dir)
                # get the directories
                if os.path.isdir(search_dir):
                    print(search_dir + model_id)
                    chk_dir = glob.glob(search_dir + model_id)
                    if len(chk_dir) > 0:
                        self.ctrl[model_id]['model_dir'] = chk_dir[0]
                        if self.verbose:
                            sys.stderr.write('Found: '+ chk_dir[0] + '\n')
                            return True
                else:
                    if self.verbose:
                        sys.stderr.write('directory: %s does not exist\n'
                                         %search_dir)
        return False
    
    def model_dir(self, model_id):
        """Helper method that returns the model directory for a given ID
        
        Parameters
        ----------
        model_id : str
            string ID of model
        
        Returns
        -------
        str
            corresponding directory (if available)
        
        Raises 
        ------
        IOError
            if directory is not available or assigned location is not a 
            directory
        """
        dirloc = os.path.join(self.ctrl[model_id]['model_dir'], 'renamed')
        if not os.path.isdir(dirloc):
            raise IOError("Model directory for ID %s not available or does "
                          "not exist")
        return dirloc
    
    def get_model_files(self):
        """Search valid model files
        
        """
        # unfortunately there's more than one file naming convention
        # examples
        # aerocom3_CAM5.3-Oslo_AP3-CTRL2016-PD_od550aer_Column_2010_monthly.nc
        # aerocom.AATSR_ensemble.v2.6.daily.od550aer.2012.nc
        
        for model in self.model_ids:
            # loop through the list of models
            model_dir = self.model_dir(model)
            
            nc_files = glob.glob(model_dir + '/*.nc')
            # Check if the found file has a naming according the aerocom conventions
            for _file in nc_files:
                # divide the type (aerocom phase 2 or phase 3) based on the # of underscores in a file name
                if os.path.basename(_file).count('_') >= 4:
                    data_types = ['surface', 'column', 'modellevel']
                    # phase 3 file naming convention
                    self.ctrl[model]['file_sep'] = '_'
                    self.ctrl[model]['year_pos'] = -2
                    self.ctrl[model]['var_pos'] = -4
                    self.ctrl[model]['ts_pos'] = -1
                    c_dummy_arr = _file.split(self.ctrl[model]['file_sep'])
                    # include vars for the surface
                    if c_dummy_arr[-3].lower() in data_types:
                        self.ctrl[model]['vars'].append(c_dummy_arr[self.ctrl[model]['var_pos']])
                        self.ctrl[model]['files'].append(_file)
                    # also include 3d vars that provide station based data
                    # and contain the string vmr
                    # in this case the variable name has to slightly changed to the aerocom phase 2 naming
                    elif c_dummy_arr[-3].lower() == 'modellevelatstations':
                        if 'vmr' in c_dummy_arr[-4]:
                            self.ctrl[model]['vars'].append(c_dummy_arr[-4].replace('vmr', 'vmr3d'))
                            self.ctrl[model]['files'].append(_file)
                elif os.path.basename(_file).count('.') >= 4:
                    # phase 2
                    self.ctrl[model]['file_sep'] = '.'
                    self.ctrl[model]['year_pos'] = -2
                    self.ctrl[model]['var_pos'] = -3
                    self.ctrl[model]['ts_pos'] = -4
                    c_dummy_arr = _file.split(self.ctrl[model]['file_sep'])
                    self.ctrl[model]['vars'].append(c_dummy_arr[self.ctrl[model]['var_pos']])
                    self.ctrl[model]['files'].append(_file)

            # make sorted list of unique vars
            self.ctrl[model]['vars'] = (sorted(OrderedDict.fromkeys(self.ctrl[model]['vars'])))   
                
    def read(self, var, ts_type = 'daily'):
        """Read model data"""
        #iris.FUTURE.netcdf_promote = True
        #iris.FUTURE.cell_datetime_objects = True
        variable_constraint = iris.Constraint(cube_func=(lambda c: c.var_name == var))

        # unfortunately there's more than one file naming convention
        # examples
        # aerocom3_CAM5.3-Oslo_AP3-CTRL2016-PD_od550aer_Column_2010_monthly.nc
        # aerocom.AATSR_ensemble.v2.6.daily.od550aer.2012.nc
        #V3SearchStrArr = "_".join(['.*',var, '.*',year, ts_type])+'.nc'
        #V2SearchStrArr = ".".join(['.*',ts_type, var, year, 'nc'])
        for model in self.model_ids:
            model_dir = self.ctrl[model]['model_dir']
            if var not in self.ctrl[model]['vars']:
                sys.stderr.write("Error: variable not found in model directory.")
                sys.stderr.write("Model directory: %s" %model_dir)

            match_files = []
            for year in self.years_to_load:
                # search for filename in self.files using ts_type as default ts size
                for _file in self.ctrl[model]['files']:
                    if self.ctrl[model]['file_sep'] == '_':  #new file naming convention
                        search_string = "_".join(['.*',var, '.*',str(year), ts_type])+'.nc'
                        if re.match(search_string, _file):
                            match_files.append(_file)

                    elif self.ctrl[model]['file_sep'] == '.':    #old file naming convention
                        search_string = ".".join(['.*',ts_type, var, str(year), 'nc'])
                        if re.match(search_string, _file):
                            print("FOUND MATCH: %s" %os.path.basename(_file))
                            match_files.append(_file)
                    else:
                        # This should never be called
                        sys.stderr.write("file list not initialised\n")

            # read files using iris
            cubes = iris.cube.CubeList()
            for _file in match_files:
                #self.data[model].append(iris.load_cube(_file, variable_constraint))
                cubes.append(iris.load_cube(_file, variable_constraint))

            #now put the CubeList together and form one cube
            #1st equalise the cubes (remove non common attributes)
            equalise_attributes(cubes)
            #unify time units
            unify_time_units(cubes)

            #now concatenate the cube list to one cube
            self.data[model]=cubes.concatenate()[0]
            #rename to aerocom standard
            #self.data[model].rename(var)
            #self.time[model] = (unit.num2date(self.data[model].coord('time').points,
            #                                 self.data[model].coord('time').units.name,
            #                                  self.data[model].coord('time').units.calendar))

            #Now extract the time the user wanted
            Constraint = iris.Constraint(time=lambda cell: PartialDateTime(year=self.start_time.year,
                month=self.start_time.month,
                day=self.start_time.day)
                <= cell <= iris.time.PartialDateTime(year=self.stop_time.year,
                month=self.stop_time.month,
                day=self.stop_time.day))

            self.data[model] = self.data[model].extract(Constraint)
            #latitude constrain
            #cons = iris.Constraint(latitude=lambda cell: -45. < cell < 45.)
            #pdb.set_trace()



###################################################################################



