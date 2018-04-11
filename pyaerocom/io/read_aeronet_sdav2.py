################################################################
# read_aeronet_sdav1.py
#
# class to read aeronet sda data 
# (https://aeronet.gsfc.nasa.gov/cgi-bin/combined_data_access_new)
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
from collections import OrderedDict

import numpy as np
from datetime import datetime
import pandas as pd
import re
import pyaerocom.config as const

class ReadAeronetSDAV2:
	"""Read Aeronet SDA data class
	"""
	#FILEMASK = '*_A*.ONEILL_20'
	FILEMASK = '*.ONEILL_20'
	version__='0.02'
	DATASET_NAME = const.AERONET_SUN_V2L2_SDA_DAILY_NAME
	DATASET_PATH = const.OBSCONFIG[const.AERONET_SUN_V2L2_SDA_DAILY_NAME]['PATH']
	#Flag if the dataset contains all years or not
	DATASET_IS_YEARLY = False

	###################################################################################

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
	


	###################################################################################

	def ReadDailyFile(InFile, VarsToReturn=None):

		#This how the beginning of data file lookes like

		#Level 2.0 Quality Assured Data. The following AERONET-SDA data are derived from AOD data which are pre and post-field calibrated and manually inspected.
		#SDA Version 4.1 (tauf_tauc),Note: the labels in square brackets that follow some of the parameter (column) names are the symbols associated with these parameters in the original SDA publication of O'Neill et al. (2003)
		#Location=Zvenigorod,Latitude=55.695000,Longitude=36.775000,Elevation[m]=200.000000,PI=Brent_Holben,Email=Brent.N.Holben@nasa.gov
		#SDA from Level 2.0 AOD,Daily Average,UNITS can be found at,,, http://aeronet.gsfc.nasa.gov/data_menu.html
		#Date(dd:mm:yyyy),Time(hh:mm:ss),Julian_Day,Total_AOD_500nm[tau_a],Fine_Mode_AOD_500nm[tau_f],Coarse_Mode_AOD_500nm[tau_c],FineModeFraction_500nm[eta],2nd_Order_Reg_Fit_Error-Total_AOD_500nm[regression_dtau_a],RMSE_Fine_Mode_AOD_500nm[Dtau_f],RMSE_Coarse_Mode_AOD_500nm[Dtau_c],RMSE_FineModeFraction_500nm[Deta],Angstrom_Exponent(AE)-Total_500nm[alpha],dAE/dln(wavelength)-Total_500nm[alphap],AE-Fine_Mode_500nm[alpha_f],dAE/dln(wavelength)-Fine_Mode_500nm[alphap_f],870nm_Input_AOD,675nm_Input_AOD,667nm_Input_AOD,555nm_Input_AOD,551nm_Input_AOD,532nm_Input_AOD,531nm_Input_AOD,500nm_Input_AOD,490nm_Input_AOD,443nm_Input_AOD,440nm_Input_AOD,412nm_Input_AOD,380nm_Input_AOD,Last_Processing_Date,Number_of_Wavelengths,Number_of_Observations,Exact_Wavelengths_for_Input_AOD
		#16:09:2006,00:00:00,259.000000,0.059239,0.032410,0.026828,0.571506,0.004645,0.007370,0.005064,0.091573,1.278830,-0.656569,2.354811,1.413517,0.036734,0.039337,-999.,-999.,-999.,-999.,-999.,0.064670,-999.,-999.,0.069614,-999.,0.083549,27:11:2007,5,11,0.868800,0.675600,0.440400,0.500500,0.380100

		DATE_INDEX=0
		TIME_INDEX=1
		JULIEN_DAY_INDEX=2
		TOTAL_AOD_500NM_TAU_A_INDEX=3
		FINE_MODE_AOD_500NM_TAU_F_INDEX=4
		COARSE_MODE_AOD_500NM_TAU_C_INDEX=5
		FINE_MODE_FRACTION_500NM_ETA_INDEX=6
		#i_2nd_Order_Reg_Fit_Error-Total_AOD_500nm[regression_dtau_a]=7
		RMSE_FINE_MODE_AOD_500NM_DTAU_INDEX=8
		RMSE_COARSE_MODE_AOD_500NM_DTAU_INDEX=9
		RMSE_FINE_MODE_FRACTION_500NM_DETA_INDEX=10
		#i_Angstrom_Exponent(AE)-Total_500nm[alpha]=11
		#i_dAE/dln(wavelength)-Total_500nm[alphap]=12
		#i_AE-Fine_Mode_500nm[alpha_f]=13
		#i_dAE/dln(wavelength)-Fine_Mode_500nm[alphap_f]=14
		I870NM_INPUT_AOD_INDEX=15
		I675NM_INPUT_AOD_INDEX=16
		I667NM_INPUT_AOD_INDEX=17
		I555NM_INPUT_AOD_INDEX=18
		I551NM_INPUT_AOD_INDEX=19
		I532NM_INPUT_AOD_INDEX=20
		I531NM_INPUT_AOD_INDEX=21
		I500NM_INPUT_AOD_INDEX=22
		I490NM_INPUT_AOD_INDEX=23
		I443NM_INPUT_AOD_INDEX=24
		I440NM_INPUT_AOD_INDEX=25
		I412NM_INPUT_AOD_INDEX=26
		I380NM_INPUT_AOD_INDEX=27
		LAST_PROCESSING_DATE_INDEX=28
		NUMBER_OF_WAVELENGTHS_INDEX=29
		NUMBER_OF_OBSERVATIONS_INDEX=30
		EXACT_WAVELENGTHS_FOR_INPUT_AOD_INDEX=31



		f_NanVal=np.float_(-9999.)

		d_DataOut={}
		#Iterate over the lines of the file
		with open(InFile, 'rt') as InFile:
			c_HeadLine=InFile.readline()
			c_Algorithm=InFile.readline()
			c_Dummy=InFile.readline()
			#re.split(r'=|\,',c_Dummy)
			i_Dummy=iter(re.split(r'=|\,',c_Dummy.rstrip())) 
			dict_Loc=dict(zip(i_Dummy, i_Dummy))

			#pdb.set_trace()
			d_DataOut['latitude']=float(dict_Loc['Latitude'])
			d_DataOut['longitude']=float(dict_Loc['Longitude'])
			d_DataOut['altitude']=float(dict_Loc['Elevation[m]'])
			d_DataOut['station name']=dict_Loc['Location']
			d_DataOut['PI']=dict_Loc['PI']
			c_Dummy=InFile.readline()
			c_Header=InFile.readline()


			DataArr={}
			#d_DataOut['time']=[]
			d_DataOut['od500aer']=[]
			d_DataOut['od500gt1aer']=[]
			d_DataOut['od500lt1aer']=[]
			d_DataOut['od440aer']=[]
			d_DataOut['od870aer']=[]
			d_DataOut['ang4487aer']=[]
			d_DataOut['od550aer']=[]
			d_DataOut['od550gt1aer']=[]
			d_DataOut['od550lt1aer']=[]
			d_Time=[]


			for line in InFile:
				# process line
				c_DummyArr=line.split(',')
				#the following uses the standatd python datetime functions
				day, month, year = c_DummyArr[DATE_INDEX].split(':')
				hour, minute, second = c_DummyArr[TIME_INDEX].split(':')

				#This uses the numpy datestring64 functions that e.g. also support Months as a time step for timedelta
				#Build a proper ISO 8601 UTC date string
				day, month, year = c_DummyArr[DATE_INDEX].split(':')
				#pdb.set_trace()
				datestring='-'.join([year, month, day])
				datestring='T'.join([datestring,  c_DummyArr[TIME_INDEX]])
				datestring='+'.join([datestring, '00:00'])
				d_Time.append(np.datetime64(datestring))

				d_DataOut['od500aer'].append(np.float_(c_DummyArr[TOTAL_AOD_500NM_TAU_A_INDEX]))
				if d_DataOut['od500aer'][-1] == f_NanVal: d_DataOut['od500aer'][-1]=np.nan
				d_DataOut['od440aer'].append(np.float_(c_DummyArr[I440NM_INPUT_AOD_INDEX]))
				if d_DataOut['od440aer'][-1] == f_NanVal: d_DataOut['od440aer'][-1]=np.nan
				d_DataOut['od870aer'].append(np.float_(c_DummyArr[I870NM_INPUT_AOD_INDEX]))
				if d_DataOut['od870aer'][-1] == f_NanVal: d_DataOut['od870aer'][-1]=np.nan

				d_DataOut['od500gt1aer'].append(np.float_(c_DummyArr[COARSE_MODE_AOD_500NM_TAU_C_INDEX]))
				if d_DataOut['od500gt1aer'][-1] == f_NanVal: d_DataOut['od500gt1aer'][-1]=np.nan
				d_DataOut['od500lt1aer'].append(np.float_(c_DummyArr[FINE_MODE_AOD_500NM_TAU_F_INDEX]))
				if d_DataOut['od500lt1aer'][-1] == f_NanVal: d_DataOut['od500lt1aer'][-1]=np.nan

				
				d_DataOut['ang4487aer'].append(-1.0*np.log(d_DataOut['od440aer'][-1]/d_DataOut['od870aer'][-1])/np.log(0.44/.870))
				d_DataOut['od550aer'].append(d_DataOut['od500aer'][-1]*(0.55/0.50)**np.float_(-1.)*d_DataOut['ang4487aer'][-1])
				d_DataOut['od550gt1aer'].append(d_DataOut['od500gt1aer'][-1]*(0.55/0.50)**np.float_(-1.)*d_DataOut['ang4487aer'][-1])
				d_DataOut['od550lt1aer'].append(d_DataOut['od500lt1aer'][-1]*(0.55/0.50)**np.float_(-1.)*d_DataOut['ang4487aer'][-1])
				#;fill up time steps of the now calculated od550_aer that are nans with values calculated from the
				#;440nm wavelength to minimise gaps in the time series
				#if np.isnan(d_DataOut['od550aer'][-1]): 
					#d_DataOut['od550aer'][-1]=d_DataOut['od440aer'][-1]*(0.55/0.44)**np.float_(-1.)*d_DataOut['ang4487aer'][-1]

		#convert to pandas series
		d_DataOut['od500aer']=pd.Series(d_DataOut['od500aer'],index=d_Time)
		d_DataOut['od500gt1aer']=pd.Series(d_DataOut['od500gt1aer'],index=d_Time)
		d_DataOut['od500lt1aer']=pd.Series(d_DataOut['od500lt1aer'],index=d_Time)
		d_DataOut['od440aer']=pd.Series(d_DataOut['od440aer'],index=d_Time)
		d_DataOut['od870aer']=pd.Series(d_DataOut['od870aer'],index=d_Time)
		d_DataOut['ang4487aer']=pd.Series(d_DataOut['ang4487aer'],index=d_Time)
		d_DataOut['od550aer']=pd.Series(d_DataOut['od550aer'],index=d_Time)
		d_DataOut['od550gt1aer']=pd.Series(d_DataOut['od550gt1aer'],index=d_Time)
		d_DataOut['od550lt1aer']=pd.Series(d_DataOut['od550lt1aer'],index=d_Time)

		return d_DataOut
		#pdb.set_trace()


	###################################################################################

	def ReadDaily(self):
		"""create a dictionary with all the stations using the station name as key"""

		for File in self.files:
			if self.VerboseFlag:
				print(File)

			TempData=ReadAeronetSDAV2.ReadDailyFile(File)
			self.data[TempData['station name']]=TempData


	###################################################################################

	def GetFileList(self):
		"""search for files to read """

		if self.VerboseFlag:
			print('searching for data files. This might take a while...')
		self.files=glob.glob(os.path.join(ReadAeronetSDAV2.DATASET_PATH,ReadAeronetSDAV2.FILEMASK))


###################################################################################


