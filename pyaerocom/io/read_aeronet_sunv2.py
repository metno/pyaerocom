################################################################
# read_aeronet_sunv2.py
#
# read Aeronet direct sun V2 data
#
# this file is part of the aerocom_pt package
#
#################################################################
# Created 20171026 by Jan Griesfeller for Met Norway
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

"""
Note
----
    This module has not yet been translated / shipped to the pyaerocom 
    library
"""
import os
import glob

import numpy as np

import pandas as pd
import re
import pyaerocom.config as const


class ReadAeronetSunV2:
	"""Read Aeronet direct sun version 2 data
	"""
	FILEMASK = '*.lev20'
	__version__='0.02'
	DATASET_NAME = const.AERONET_SUN_V2L2_AOD_DAILY_NAME
	DATASET_PATH = const.OBSCONFIG[const.AERONET_SUN_V2L2_AOD_DAILY_NAME]['PATH']
	#Flag if the dataset contains all years or not
	DATASET_IS_YEARLY = False

	def __init__(self, VerboseFlag=False):
		self.VerboseFlag = VerboseFlag
		self.data = {}
		self.index = len(self.data)
		self.GetFileList()
		#read revision data from 1st data file name
		#example: 920801_160312_Minsk.ONEILL_20
		self.Revision=os.path.basename(self.files[0]).split('_')[1]

	def __iter__(self):
		return self

	def __next__(self):
		if self.index == 0:
			raise StopIteration
		self.index = self.index - 1
		return self.data[self.index]

	def __repr__(self):
		return ','.join(self.data.keys())



	###################################################################################


	def ReadDailyFile(c_Filename, VerboseFlag = False):
		# function to read Aeronet Sun files
		# The data is read into pandas Series
		#
		####################################################################################
		# Created 201602 by Jan Griesfeller for Met Norway
		#
		# Last update: 20160309	JG	Prepare code for repository
		####################################################################################

		#import numpy as np


	#Level 2.0. Quality Assured Data.<p>The following data are pre and post field calibrated, automatically cloud cleared and manually inspected.
	#Version 2 Direct Sun Algorithm
	#Location=Zvenigorod,long=36.775,lat=55.695,elev=200,Nmeas=11,PI=Brent_Holben,Email=Brent.N.Holben@nasa.gov
	#AOD Level 2.0,Daily Averages,UNITS can be found at,,, http://aeronet.gsfc.nasa.gov/data_menu.html
	#Date(dd-mm-yy),Time(hh:mm:ss),Julian_Day,AOT_1640,AOT_1020,AOT_870,AOT_675,AOT_667,AOT_555,AOT_551,AOT_532,AOT_531,AOT_500,AOT_490,AOT_443,AOT_440,AOT_412,AOT_380,AOT_340,Water(cm),%TripletVar_1640,%TripletVar_1020,%TripletVar_870,%TripletVar_675,%TripletVar_667,%TripletVar_555,%TripletVar_551,%TripletVar_532,%TripletVar_531,%TripletVar_500,%TripletVar_490,%TripletVar_443,%TripletVar_440,%TripletVar_412,%TripletVar_380,%TripletVar_340,%WaterError,440-870Angstrom,380-500Angstrom,440-675Angstrom,500-870Angstrom,340-440Angstrom,440-675Angstrom(Polar),N[AOT_1640],N[AOT_1020],N[AOT_870],N[AOT_675],N[AOT_667],N[AOT_555],N[AOT_551],N[AOT_532],N[AOT_531],N[AOT_500],N[AOT_490],N[AOT_443],N[AOT_440],N[AOT_412],N[AOT_380],N[AOT_340],N[Water(cm)],N[440-870Angstrom],N[380-500Angstrom],N[440-675Angstrom],N[500-870Angstrom],N[340-440Angstrom],N[440-675Angstrom(Polar)]
	#16:09:2006,00:00:00,259.000000,-9999.,0.036045,0.036734,0.039337,-9999.,-9999.,-9999.,-9999.,-9999.,0.064670,-9999.,-9999.,0.069614,-9999.,0.083549,0.092204,0.973909,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,1.126095,0.973741,1.474242,1.135232,1.114550,-9999.,-9999.,11,11,11,-9999.,-9999.,-9999.,-9999.,-9999.,11,-9999.,-9999.,11,-9999.,11,11,11,11,11,11,11,11,-9999.
		i_DateIndex=0
		i_TimeIndex=1
		i_JulienDayIndex=2
		i_OD1640Index=3
		i_OD1020Index=4
		i_OD870Index=5
		i_OD675Index=6
		i_OD667Index=7
		i_OD555Index=8
		i_OD551Index=9
		i_OD532Index=10
		i_OD531Index=11
		i_OD500Index=12
		i_OD440Index=15
		i_OD380Index=17
		i_OD340Index=18

		f_NanVal=np.float_(-9999.)

		d_DataOut={}
		#Iterate over the lines of the file
		if VerboseFlag:
			print(c_Filename)
		with open(c_Filename, 'rt') as InFile:
			c_HeadLine=InFile.readline()
			c_Algorithm=InFile.readline()
			c_Dummy=InFile.readline()
			#re.split(r'=|\,',c_Dummy)
			i_Dummy=iter(re.split(r'=|\,',c_Dummy.rstrip())) 
			dict_Loc=dict(zip(i_Dummy, i_Dummy))

			d_DataOut['latitude']=float(dict_Loc['lat'])
			d_DataOut['longitude']=float(dict_Loc['long'])
			d_DataOut['altitude']=float(dict_Loc['elev'])
			d_DataOut['station name']=dict_Loc['Location']
			d_DataOut['PI']=dict_Loc['PI']
			#d_DataOut['']=
			#d_DataOut['']=
			c_Dummy=InFile.readline()
			c_Header=InFile.readline()


			DataArr={}
			#d_DataOut['time']=[]
			d_DataOut['od500aer']=[]
			d_DataOut['od440aer']=[]
			d_DataOut['od870aer']=[]
			d_DataOut['ang4487aer']=[]
			d_DataOut['od550aer']=[]
			d_Time=[]


			for line in InFile:
				# process line
				c_DummyArr=line.split(',')
				#the following uses the standatd python datetime functions
				day, month, year = c_DummyArr[i_DateIndex].split(':')
				hour, minute, second = c_DummyArr[i_TimeIndex].split(':')

				#This uses the numpy datestring64 functions that e.g. also support Months as a time step for timedelta
				#Build a proper ISO 8601 UTC date string
				day, month, year = c_DummyArr[i_DateIndex].split(':')
				#pdb.set_trace()
				datestring='-'.join([year, month, day])
				datestring='T'.join([datestring,  c_DummyArr[i_TimeIndex]])
				datestring='+'.join([datestring, '00:00'])
				d_Time.append(np.datetime64(datestring))

				d_DataOut['od500aer'].append(np.float_(c_DummyArr[i_OD500Index]))
				if d_DataOut['od500aer'][-1] == f_NanVal: d_DataOut['od500aer'][-1]=np.nan
				d_DataOut['od440aer'].append(np.float_(c_DummyArr[i_OD440Index]))
				if d_DataOut['od440aer'][-1] == f_NanVal: d_DataOut['od440aer'][-1]=np.nan
				d_DataOut['od870aer'].append(np.float_(c_DummyArr[i_OD870Index]))
				if d_DataOut['od870aer'][-1] == f_NanVal: d_DataOut['od870aer'][-1]=np.nan
				
				d_DataOut['ang4487aer'].append(-1.0*np.log(d_DataOut['od440aer'][-1]/d_DataOut['od870aer'][-1])/np.log(0.44/.870))
				d_DataOut['od550aer'].append(d_DataOut['od500aer'][-1]*(0.55/0.50)**np.float_(-1.)*d_DataOut['ang4487aer'][-1])
				#;fill up time steps of the now calculated od550_aer that are nans with values calculated from the
				#;440nm wavelength to minimise gaps in the time series
				if np.isnan(d_DataOut['od550aer'][-1]): 
					d_DataOut['od550aer'][-1]=d_DataOut['od440aer'][-1]*(0.55/0.44)**np.float_(-1.)*d_DataOut['ang4487aer'][-1]

		#convert to real numpy arrays
		d_DataOut['od500aer']=pd.Series(d_DataOut['od500aer'],index=d_Time)
		d_DataOut['od440aer']=pd.Series(d_DataOut['od440aer'],index=d_Time)
		d_DataOut['od870aer']=pd.Series(d_DataOut['od870aer'],index=d_Time)
		d_DataOut['ang4487aer']=pd.Series(d_DataOut['ang4487aer'],index=d_Time)
		d_DataOut['od550aer']=pd.Series(d_DataOut['od550aer'],index=d_Time)
		#pdb.set_trace()
		return(d_DataOut)

	###################################################################################

	def ReadDaily(self):
		"""create a dictionary with all the stations using the station name as key"""
		
		for File in self.files:
			if self.VerboseFlag:
				print(File)
			
			TempData=ReadAeronetSunV2.ReadDailyFile(File)
			self.data[TempData['station name']]=TempData


	###################################################################################

	def GetFileList(self):
		"""search for files to read """

		if self.VerboseFlag:
			print('searching for data files. This might take a while...')
		self.files=glob.glob(os.path.join(ReadAeronetSunV2.DATASET_PATH,
                                    ReadAeronetSunV2.FILEMASK))



###################################################################################



