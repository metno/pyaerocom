#!/usr/bin/env python3

################################################################
# readoddata_testing.py
#
# demostrator of how to use the observational data reading class
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


import pdb


from pyaerocom.read.readobsdata import ReadObsData
import pyaerocom.config as const



###################################################################################


if __name__ == '__main__':

	import argparse
	parser = argparse.ArgumentParser(description='command line interface to the readobsdata class')
	parser.add_argument("file", help="aeronet file to read")

	args = parser.parse_args()
	if args.file:
		filename=args.file

		
	#pdb.set_trace()
	test=ReadObsData([const.AERONET_SUN_V2L2_SDA_DAILY_NAME], VerboseFlag=True)
	test.read_daily()
	pdb.set_trace()
	print(test)


	#pdb.set_trace()


