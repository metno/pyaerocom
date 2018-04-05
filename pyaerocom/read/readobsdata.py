#!/usr/bin/env python3

################################################################
# readoddata.py
#
# observational data reading class
#
# this file is part of the aerocom_pt package
#
#################################################################
# Created 20171024 by Jan Griesfeller for Met Norway
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

from pyaerocom.read.read_aeronet_sdav2 import ReadAeronetSDAV2
from pyaerocom.read.read_aeronet_sunv2 import ReadAeronetSunV2
import pyaerocom.config as const

class ReadObsData(ReadAeronetSDAV2,ReadAeronetSunV2):
	"""aerocom_pt observation data reading class
	"""

	SUPPORTED_DATASETS = [const.AERONET_SUN_V2L2_AOD_DAILY_NAME, const.AERONET_SUN_V2L2_SDA_DAILY_NAME]
	SDA_TEST_FILE='/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSun2.0.SDA.daily/renamed/920801_160312_Zvenigorod.ONEILL_20'
	SUN_TEST_FILE='/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetRaw2.0/renamed/920801_170401_Zambezi.lev20'
	#
	DATASET_IDX_AERONETSDA2_0 = 0
	DATASET_IDX_AERONETSUN2_0 = 1

	def __init__(self, DataSetsToRead, VerboseFlag=False):
		if isinstance( DataSetsToRead, list):
			self.DataSetsToRead =  DataSetsToRead
		else:
			self.DataSetsToRead = [DataSetsToRead]

		self.VerboseFlag = VerboseFlag
		self.data = {}
		self.FILEMASKS = []
		self.__version__ = 0.01
		self.DATASETNAMES = []
		self.SuperClasses = {}
		self.infiles = []
		#file caching
		self.WriteCacheFile = True
		#now init the needed superclasses
		#pdb.set_trace()

		for DataSetToRead in self.DataSetsToRead:
			#skip unknown data sets
			#pdb.set_trace()
			if DataSetToRead == ReadObsData.SUPPORTED_DATASETS[ReadObsData.DATASET_IDX_AERONETSDA2_0]:
				#AeronetSDAV2
				Dummy = ReadAeronetSDAV2(VerboseFlag = VerboseFlag)	

			elif DataSetToRead == ReadObsData.SUPPORTED_DATASETS[ReadObsData.DATASET_IDX_AERONETSUN2_0]:
				#Aeronet direct sun V2
				Dummy = ReadAeronetSunV2(VerboseFlag = VerboseFlag)

			else:
				continue

			self.DATASETNAMES.append(Dummy.DATASET_NAME)
			self.FILEMASKS.append(Dummy.FILEMASK)
			self.SuperClasses[DataSetToRead] = Dummy

		self.index = len(self.data)


	def __iter__(self):
		return self

	def __next__(self):
		if self.index == 0:
			raise StopIteration
		self.index = self.index - 1
		return self.data[self.index]

	def __repr__(self):
		Out=[]
		for dataset in self.data:
			Out.append(dataset+':')
			for stationid in self.data[dataset]:
				Out.append(stationid)

		return '\n'.join(Out)

	def __getitem__(self, item):
		return self.data[item]


	###################################################################################


	def ReadDaily(self):
		"""Read observations"""

		for DataSetToRead in self.DataSetsToRead:
			#test if the data set has yearly files or not
			if self.SuperClasses[DataSetToRead].DATASET_IS_YEARLY:
				#write cache file with start and end date
				self.CacheFile = ''
			else:
				#write cache file without start and end date:
				self.CacheFile = os.path.join(
					const.OBSDATACACHEDIR, 
					'_'.join([self.SuperClasses[DataSetToRead].DATASET_NAME,'AllYears','AllVars.plk']))

			if not self.ReadCacheData(DataSetToRead):
				self.SuperClasses[DataSetToRead].ReadDaily()
				self.data[DataSetToRead] = self.SuperClasses[DataSetToRead].data
				SuccessFlag = self.SaveCacheData(DataSetToRead)

	###################################################################################
	def SaveCacheData(self, DataSetToCache):
		"""save cache file"""

		if not self.WriteCacheFile:
			return

		import pickle

		SuccessFlag = False
		#get newest file in read dir
		DataDir=self.SuperClasses[DataSetToCache].DATASET_PATH
		NewestFileInReadDir = max(glob.iglob(os.path.join(DataDir,'*')), key=os.path.getctime)
		NewestFileDateInReadDir = os.path.getctime(NewestFileInReadDir)
		DoNotCacheFile = os.path.join(const.OBSDATACACHEDIR,'DONOTCACHE')
		RevisionFile = os.path.join(DataDir,'Revision.txt')
		Revision=''
		if os.path.isfile(RevisionFile):
			with open(RevisionFile, 'rt') as InFile:
				Revision = InFile.readline().strip()
				InFile.close()

		c_CacheFile=self.CacheFile
		print('Writing cache file ',c_CacheFile)
		#OutHandle = gzip.open(c_CacheFile, 'wb')
		OutHandle = open(c_CacheFile, 'wb')
		NewestFileInReadDirSaved = NewestFileInReadDir
		NewestFileDateInReadDirSaved = NewestFileDateInReadDir
		RevisionSaved = Revision
		Version = self.SuperClasses[DataSetToCache].__version__
		pickle.dump(NewestFileInReadDirSaved, OutHandle, pickle.HIGHEST_PROTOCOL)
		pickle.dump(NewestFileDateInReadDirSaved, OutHandle, pickle.HIGHEST_PROTOCOL)
		pickle.dump(RevisionSaved, OutHandle, pickle.HIGHEST_PROTOCOL)
		pickle.dump(Version, OutHandle, pickle.HIGHEST_PROTOCOL)
		#pdb.set_trace()
		pickle.dump(self.data[DataSetToCache], OutHandle,pickle.HIGHEST_PROTOCOL)
		OutHandle.close()
		print('done')
		SuccessFlag = True
		return SuccessFlag



	###################################################################################


	def ReadCacheData(self, DataSetToCache):
		"""read cache file"""

		import pickle

		SuccessFlag = False
		#get newest file in read dir
		DataDir=self.SuperClasses[DataSetToCache].DATASET_PATH
		NewestFileInReadDir = max(glob.iglob(os.path.join(DataDir,'*')), key=os.path.getctime)
		NewestFileDateInReadDir=os.path.getctime(NewestFileInReadDir)
		DoNotCacheFile=os.path.join(const.OBSDATACACHEDIR,'DONOTCACHE')
		RevisionFile=os.path.join(DataDir,'Revision.txt')
		Revision=''
		if os.path.isfile(RevisionFile):
			with open(RevisionFile, 'rt') as InFile:
				Revision=InFile.readline().strip()
				InFile.close()

		c_CacheFile=self.CacheFile

		#pdb.set_trace()
		if os.path.isfile(c_CacheFile) and not os.path.isfile(DoNotCacheFile):
			print('cache file found! Start reading...')
			#now check if the cache file is outdated or not
			#Inhandle=f = gzip.open(c_CacheFile,'rb')
			InHandle=open(c_CacheFile,'rb')
			NewestFileInReadDirSaved=pickle.load(InHandle)
			NewestFileDateInReadDirSaved=pickle.load(InHandle)
			RevisionSaved=pickle.load(InHandle)
			VersionSaved=pickle.load(InHandle)
			if (NewestFileInReadDirSaved == NewestFileInReadDir
				and NewestFileDateInReadDirSaved == NewestFileDateInReadDir 
				and VersionSaved == self.SuperClasses[DataSetToCache].__version__):
				#read the obs data structs
					self.data[DataSetToCache] = pickle.load(InHandle)
					SuccessFlag = True
					print('done')
			elif VersionSaved != self.SuperClasses[DataSetToCache].__version__:
				print('cached data comes from outdated reading routine! Rereading data...')
		else:
			if os.path.isfile(DoNotCacheFile):
				print('DONOTCACHE file found! Rereading data...')
			else:
				#cache file not found
				print('cache NOT file found!')
				os.makedirs(const.OBSDATACACHEDIR, exist_ok=True)

		#pdb.set_trace()
		return SuccessFlag
		

###################################################################################



