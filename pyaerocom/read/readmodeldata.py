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
import pyaerocom.config as const
import iris

class ReadModelData():
    """aerocom_pt model data reading class
    """
    MODELDIRS = const.MODELDIRS

    __version__ = 0.01
    _TESTFILE = "/lustre/storeA/project/aerocom/aerocom-users-database/CCI-Aerosol/CCI_AEROSOL_Phase2/AATSR_SU_v4.3/renamed/aerocom.AATSR_SU_v4.3.daily.od550aer.2008.nc"

    def __init__(self, ModelNamesToRead, StartTime, EndTime, VerboseFlag = False):

        self.data = {}
        #control struct with parameters that are determined at init
        self.ctrl = {}
        #save the time
        self.time = {}
        #self.Ctrl[model] = {}
        if isinstance(ModelNamesToRead, dict):
            #dictionary
            for ModelName in ModelNamesToRead:
                self.data[ModelName] = {}
                self.time[ModelName] = []
                self.ctrl[ModelName] = {}
                self.ctrl[ModelName]['ModelDir'] = ''  #save the location in there
                self.ctrl[ModelName]['YearPos'] = -1    #pos of year in filename
                self.ctrl[ModelName]['VarPos'] = -1    #pos of variable name in filename
                self.ctrl[ModelName]['TSPos'] = -1    #pos of time ste[p name in filename (daily, monthly, 3hourly, hourly)
                self.ctrl[ModelName]['files'] = []    #array with file names
                self.ctrl[ModelName]['vars'] = []    #array with variable names
                self.ctrl[ModelName]['FileSep'] = ''    #file seperator

        elif isinstance(ModelNamesToRead, list):
            #list
            for ModelName in ModelNamesToRead:
                self.data[ModelName] = {}
                self.time[ModelName] = []
                self.ctrl[ModelName] = {}
                self.ctrl[ModelName]['ModelDir'] = ''  #save the location in there
                self.ctrl[ModelName]['YearPos'] = -1    #pos of year in filename
                self.ctrl[ModelName]['VarPos'] = -1    #pos of variable name in filename
                self.ctrl[ModelName]['TSPos'] = -1    #pos of time ste[p name in filename (daily, monthly, 3hourly, hourly)
                self.ctrl[ModelName]['files'] = []    #array with file names
                self.ctrl[ModelName]['vars'] = []    #array with variable names
                self.ctrl[ModelName]['FileSep'] = ''    #file seperator
        else:
            self.data[ModelNamesToRead] = {}
            self.time[ModelNamesToRead] = []
            self.ctrl[ModelNamesToRead] = {}
            self.ctrl[ModelNamesToRead]['ModelDir'] = ''  # save the location in there
            self.ctrl[ModelNamesToRead]['YearPos'] = -1  # pos of year in filename
            self.ctrl[ModelNamesToRead]['VarPos'] = -1  # pos of variable name in filename
            self.ctrl[ModelNamesToRead]['TSPos'] = -1  # pos of time ste[p name in filename (daily, monthly, 3hourly, hourly)
            self.ctrl[ModelNamesToRead]['files'] = []  # array with file names
            self.ctrl[ModelNamesToRead]['vars'] = []  # array with variable names
            self.ctrl[ModelNamesToRead]['FileSep'] = ''  # file seperator
            ModelNamesToRead = [ModelNamesToRead]

        self.ModelNamesToread = ModelNamesToRead
        self.VerboseFlag = VerboseFlag
        # self.StartTime = np.datetime64(StartTime, 'D')  #start time as np.datetime
        # self.EndTime = np.datetime64(EndTime, 'D')     #end time as np.datetime
        self.StartTime = pd.Timestamp(StartTime)  #start time as np.datetime
        self.EndTime = pd.Timestamp(EndTime)     #end time as np.datetime
        self.Time = pd.date_range(StartTime, EndTime, freq='D')
        self.FILEMASKS = []
        self.__version__ = 0.01
        self.MODELDIRS = const.MODELDIRS    #directories to search for a model directory



        #Fill self.ModelDir
        self.GetModelDir()
        self.GetModelFiles()

    ###################################################################################


    def GetModelDir(self):
        """method to get the directory the model data for a given model resides in"""

        # Return the model directory
        # and put that in self.ModelDir

        for ModelName in self.data:
            # loop through the list of models
            for FolderToSearchIn in self.MODELDIRS:
                if self.VerboseFlag:
                    print('Searching in: ', FolderToSearchIn)
                # get the directories
                if os.path.isdir(FolderToSearchIn):
                    dir = glob.glob(FolderToSearchIn + ModelName)
                    if len(dir) > 0:
                        self.ctrl[ModelName]['ModelDir'] = dir[0]
                        if self.VerboseFlag:
                            sys.stderr.write('Found: '+dir[0]+'\n')
                            break
                    else:
                        continue
                else:
                    if self.VerboseFlag:
                        sys.stderr.write('directory: ', FolderToSearchIn, ' does not exist\n')

    ###################################################################################

    def __str__(self):

        out=[]
        for model in self.data:
            out.append(':'.join([model,self.data[model].var_name]))
            #print(':'.join([model, self.data[model].var_name]))
            #print(self.data[model])

        return "\n".join(out)


    ###################################################################################

    def GetModelFiles(self):
        """method to find the model files"""

        # unfortunately there's more than one file naming convention
        # examples
        # aerocom3_CAM5.3-Oslo_AP3-CTRL2016-PD_od550aer_Column_2010_monthly.nc
        # aerocom.AATSR_ensemble.v2.6.daily.od550aer.2012.nc
        DataTypesToList = ['surface', 'column', 'modellevel']
        for model in self.ModelNamesToread:
            # loop through the list of models
            ModelDir = os.path.join(self.ctrl[model]['ModelDir'], 'renamed')
            if os.path.isdir(ModelDir):
                FileDummy = glob.glob(ModelDir + '/*.nc')
                # Check if the found file has a naming according the aerocom conventions
                for _file in FileDummy:
                    # divide the type (aerocom phase 2 or phase 3) based on the # of underscores in a file name
                    if os.path.basename(_file).count('_') >= 4:
                        # phase 3 file naming convention
                        self.ctrl[model]['FileSep'] = '_'
                        self.ctrl[model]['YearPos'] = -2
                        self.ctrl[model]['VarPos'] = -4
                        self.ctrl[model]['TSPos'] = -1
                        c_DummyArr = _file.split(self.ctrl[model]['FileSep'])
                        # include vars for the surface
                        if c_DummyArr[-3].lower() in DataTypesToList:
                            self.ctrl[model]['vars'].append(c_DummyArr[self.ctrl[model]['VarPos']])
                            self.ctrl[model]['files'].append(_file)
                        # also include 3d vars that provide station based data
                        # and contain the string vmr
                        # in this case the variable name has to slightly changed to the aerocom phase 2 naming
                        elif c_DummyArr[-3].lower() == 'modellevelatstations':
                            if 'vmr' in c_DummyArr[-4]:
                                self.ctrl[model]['vars'].append(c_DummyArr[-4].replace('vmr', 'vmr3d'))
                                self.ctrl[model]['files'].append(_file)
                    elif os.path.basename(_file).count('.') >= 4:
                        # phase 2
                        self.ctrl[model]['FileSep'] = '.'
                        self.ctrl[model]['YearPos'] = -2
                        self.ctrl[model]['VarPos'] = -3
                        self.ctrl[model]['TSPos'] = -4
                        c_DummyArr = _file.split(self.ctrl[model]['FileSep'])
                        self.ctrl[model]['vars'].append(c_DummyArr[self.ctrl[model]['VarPos']])
                        self.ctrl[model]['files'].append(_file)

                # make sorted list of unique vars
                self.ctrl[model]['vars'] = (sorted(OrderedDict.fromkeys(self.ctrl[model]['vars'])))

            else:
                # This is just additional security
                # will likely never be called
                sys.stderr.write("Error: Model folder does not exist: \n")
                sys.stderr.write(model + "\n")



    ###################################################################################

    def Read(self, Var, TSType = 'daily'):
        """Read model data"""

        #import cf_units as unit
        from iris.experimental.equalise_cubes import equalise_attributes
        from iris.util import unify_time_units
        from iris.time import PartialDateTime

        iris.FUTURE.netcdf_promote = True
        iris.FUTURE.cell_datetime_objects = True
        variable_constraint = iris.Constraint(cube_func=(lambda c: c.var_name == Var))

        YearsToLoad = np.unique(self.Time.year)
        # unfortunately there's more than one file naming convention
        # examples
        # aerocom3_CAM5.3-Oslo_AP3-CTRL2016-PD_od550aer_Column_2010_monthly.nc
        # aerocom.AATSR_ensemble.v2.6.daily.od550aer.2012.nc
        #V3SearchStrArr = "_".join(['.*',Var, '.*',Year, TSType])+'.nc'
        #V2SearchStrArr = ".".join(['.*',TSType, Var, Year, 'nc'])
        for model in self.ModelNamesToread:
            ModelDir = self.ctrl[model]['ModelDir']
            if Var not in self.ctrl[model]['vars']:
                sys.stderr.write("Error: Variable not found in model directory.")
                sys.stderr.write("Model directory: "+ModelDir)

            MatchFiles = []
            for Year in sorted(YearsToLoad):
                # search for filename in self.files using TSType as default ts size
                for _file in self.ctrl[model]['files']:
                    if self.ctrl[model]['FileSep'] == '_':  #new file naming convention
                        SearchString = "_".join(['.*',Var, '.*',str(Year), TSType])+'.nc'
                        if re.match(SearchString, _file):
                            MatchFiles.append(_file)

                    elif self.ctrl[model]['FileSep'] == '.':    #old file naming convention
                        SearchString = ".".join(['.*',TSType, Var, str(Year), 'nc'])
                        if re.match(SearchString, _file):
                            MatchFiles.append(_file)
                    else:
                        # This should never be called
                        sys.stderr.write("file list not initialised\n")

            # read files using iris
            ModelTemps = iris.cube.CubeList()
            for _file in MatchFiles:
                #self.data[model].append(iris.load_cube(_file, variable_constraint))
                ModelTemps.append(iris.load_cube(_file, variable_constraint))

            #now put the CubeList together and form one cube
            #1st equalise the cubes (remove non common attributes)
            equalise_attributes(ModelTemps)
            #unify time units
            unify_time_units(ModelTemps)

            #now concatenate the cube list to one cube
            self.data[model]=(ModelTemps.concatenate())[0]
            #rename to aerocom standard
            #self.data[model].rename(Var)
            #self.time[model] = (unit.num2date(self.data[model].coord('time').points,
            #                                 self.data[model].coord('time').units.name,
            #                                  self.data[model].coord('time').units.calendar))

            #Now extract the time the user wanted
            Constraint = iris.Constraint(time=lambda cell: PartialDateTime(year=self.StartTime.year,
                month=self.StartTime.month,
                day=self.StartTime.day)
                <= cell <= iris.time.PartialDateTime(year=self.EndTime.year,
                month=self.EndTime.month,
                day=self.EndTime.day))

            self.data[model] = self.data[model].extract(Constraint)
            #latitude constrain
            #cons = iris.Constraint(latitude=lambda cell: -45. < cell < 45.)
            #pdb.set_trace()



###################################################################################



