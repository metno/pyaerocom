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


#import numpy as np
import iris
import matplotlib.pyplot as plt
import iris.coord_categorisation
import iris.plot as iplt

import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter



from matplotlib.colors import LinearSegmentedColormap


DEFAULT_FILE = ('/lustre/storeA/project/aerocom/aerocom-users-database/'
                'CCI-Aerosol/CCI_AEROSOL_Phase2/AATSR_ORAC_v4.01/renamed/'
                'aerocom.AATSR_ORAC_v4.01.daily.od550aer.2008.nc')
###################################################################################


if __name__ == '__main__':

	import argparse
	parser = argparse.ArgumentParser(description='command line interface to the readmodeldata class')
	parser.add_argument("file", help="model file to read", )

	args = parser.parse_args()
	if args.file:
		filename=args.file

	plotfilename_season='season_test.png'

	TimeStepToPlot= 1

	#pdb.set_trace()
	iris.FUTURE.netcdf_promote = True
	nc=iris.load_cube(filename)

	#plot 20080101 (one day)
	#contour = qplt.contourf(nc[0,:,:], 25)
	#plt.gca().coastlines()
	#plt.savefig(plotfilename, dpi=300)
	#plt.close()

	iris.coord_categorisation.add_season(nc, 'time', name='clim_season')
	season_mean = nc.aggregated_by('clim_season',iris.analysis.MEAN)

	
	season_mean.coord('latitude').guess_bounds()
	season_mean.coord('longitude').guess_bounds()
	pre_grid_areas = iris.analysis.cartography.area_weights(season_mean)

	# Perform the area-weighted mean for each of the datasets using the
	# computed grid-box areas.
	weighted_mean = season_mean.collapsed(['latitude', 'longitude'],
                                                   iris.analysis.MEAN,
                                                   weights=pre_grid_areas)	

	#pdb.set_trace()
	title = 'od550aer MAM 2008 mean: {:6.3f}'.format(weighted_mean.data[TimeStepToPlot])
	colorbar_levels=[0.,0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
	#contour = iplt.contourf(season_mean[0,:,:], 25)
	ncolors=20
	cmap = plt.get_cmap('jet', ncolors)
	cmap.set_under('white')
	cmap.set_over('purple')
	#pdb.set_trace()

	griesie_data = {'red':((0., 0, 0),(0.07,0,0),(0.1,0.678,0.678,),(0.26, 1, 1),(0.85, 1, 1),(1, 0.545, 0.545)),
             'green': ((0., 0, 0), (0.07, 1, 1), (0.24, 1, 1), (0.91, 0, 0), (1, 0, 0)),
             'blue':  ((0., 1, 1), (0.07, 1, 1), (0.1,0.133,0.133),(0.25, 0, 0), (1, 0, 0))}


	gjet = LinearSegmentedColormap('griesie_jet', griesie_data)
	plt.register_cmap(cmap=gjet)
	#contour = iplt.contourf(season_mean[0,:,:], levels=colorbar_levels, cmap = cmap)
	#contour = iplt.contourf(season_mean[0,:,:], levels=colorbar_levels, cmap = gjet)
	plot = iplt.pcolormesh(season_mean[TimeStepToPlot,:,:], cmap = gjet, vmin=0., vmax=max(colorbar_levels))
	#pdb.set_trace()
	plot.axes.set_aspect(1.8)
	x = LatsToPlot = nc.coord(axis='X').points
	y = LonsToPlot = nc.coord(axis='Y').points
	axis = plt.axis([x.min(), x.max(), y.min(), y.max()])
	ax=plot.axes
	model = 'AATSR_ORAC_v4.01'
	ax.annotate('source: AEROCOM', xy=(0.88, 0.04), xycoords='figure fraction',
		horizontalalignment='right', fontsize=10, bbox=dict(boxstyle='square', facecolor='none', 
		edgecolor='black'))
	ax.annotate(model, xy=(-174.,-83.), xycoords='data',horizontalalignment='left', fontsize=13, 
		color='black', bbox=dict(boxstyle='square', facecolor='white', edgecolor='none',alpha=0.7 ))

	plt.xlabel = 'longitude'
	plt.ylabel = 'latitude'

	#plt.ylabel(_title(plot_defn.coords[0], with_units=True))
	#plot_defn = iplt._get_plot_defn(cube, mode, ndims)

	levels=colorbar_levels
	ticks=[0., 0.02, 0.04, 0.06, 0.08, 0.1, 0.3, 0.5, 0.7, 0.9]
	plt.colorbar(spacing='uniform',ticks=ticks, boundaries=levels,extend='max')
	plt.gca().coastlines()
	ax.set_xticks([-180., -120., -60., 0., 60, 120, 180], crs=ccrs.PlateCarree())
	ax.set_yticks([-90., -60, -30, 0., 30, 60, 90], crs=ccrs.PlateCarree())
	lon_formatter = LongitudeFormatter(number_format='.1f',
		degree_symbol='')
	lat_formatter = LatitudeFormatter(number_format='.1f', degree_symbol='')
	ax.xaxis.set_major_formatter(lon_formatter)
	ax.yaxis.set_major_formatter(lat_formatter)

	plt.title(title)
	plt.savefig(plotfilename_season, dpi=300)
	#pdb.set_trace()
	plt.close()



	#plt.show()



	#pdb.set_trace()
	#print(test)


	#pdb.set_trace()


