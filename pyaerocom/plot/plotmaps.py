#!/usr/bin/env python3

################################################################
# plotmodelmaps.py
#
# model data map plotting
#
# this file is part of the aerocom_pt package
#
#################################################################
# Created 20171130 by Jan Griesfeller for Met Norway
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

#import pdb
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import iris.coord_categorisation
import iris.plot as iplt

import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

import cf_units as unit
import os

from pyaerocom.griddeddata import GriddedData

def plotmaps(data, verbose = False, filter ="WORLD", var="od550aer",
             plotdir="./"):
    """plot aerocom standard maps

    Will plot every supplied time step"""

    if not isinstance(data, GriddedData):
        raise TypeError("Need pyaerocom.GriddedData as input")
    #define color bar;
    #will be moved somewhere else and variable specific at some point
    colorbar_levels = [0., 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8,
                       0.9, 1.0]

    colorbar_ticks = [0., 0.02, 0.04, 0.06, 0.08, 0.1, 0.3, 0.5, 0.7, 0.9]
    aod_data = {
        'red': ((0., 0, 0), (0.07, 0, 0), (0.1, 0.678, 0.678,), (0.26, 1, 1), (0.85, 1, 1), (1, 0.545, 0.545)),
        'green': ((0., 0, 0), (0.07, 1, 1), (0.24, 1, 1), (0.91, 0, 0), (1, 0, 0)),
        'blue': ((0., 1, 1), (0.07, 1, 1), (0.1, 0.133, 0.133), (0.25, 0, 0), (1, 0, 0))}

    colormap = LinearSegmentedColormap('aod_jet', aod_data)
    plt.register_cmap(cmap = colormap)
    TIME_VAR_NAME = 'time'

    PlotDailyFlag = False
    PlotMonthlyFlag = True

    for model in data:
        #assume that we have single cube for the moment
        #iterate over the time dimension
        cube = data[model].data
        #model = 'AATSR_ORAC_v4.01'

        cube.coord('latitude').guess_bounds()
        cube.coord('longitude').guess_bounds()

        #plot daily data
        if PlotDailyFlag:
            for time_sub_cube in cube.slices_over(TIME_VAR_NAME):
                pre_grid_areas = iris.analysis.cartography.area_weights(time_sub_cube)
                #pdb.set_trace()
                #print(time_sub_cube)

                # Perform the area-weighted mean for each of the datasets using the
                # computed grid-box areas.
                weighted_mean = time_sub_cube.collapsed(['latitude', 'longitude'],
                                                        iris.analysis.MEAN,
                                                        weights = pre_grid_areas)

                time = (unit.num2date(time_sub_cube.coord(TIME_VAR_NAME).points,
                                      time_sub_cube.coord(TIME_VAR_NAME).units.name,
                                      time_sub_cube.coord(TIME_VAR_NAME).units.calendar))

                date = str(time[0]).split(' ')[0].replace('-','')
                Year = date[0:4]
                TsStr = 'm'+date
                PlotType = 'MAP'

                title = " ".join([var, date, 'mean: {:6.3f}'.format(float(weighted_mean.data))])
                #ABS550_AER_an2012_mALLYEAR_WORLD_ZONALOBS_AERONETSky.ps.png
                #OD550_AER_an2017_d20171125_WORLD_MAP.ps.png
                plotfilename = os.path.join(plotdir, '_'.join([var, "an" + Year, TsStr, filter, PlotType]) + ".png")
                if verbose:
                    print(plotfilename)
                plot = iplt.pcolormesh(time_sub_cube[:, :], cmap = colormap, vmin=0., vmax=max(colorbar_levels))
                # pdb.set_trace()
                plot.axes.set_aspect(1.8)
                LatsToPlot = time_sub_cube.coord(axis='X').points
                LonsToPlot = time_sub_cube.coord(axis='Y').points
                axis = plt.axis([LatsToPlot.min(), LatsToPlot.max(), LonsToPlot.min(), LonsToPlot.max()])
                ax = plot.axes
                ax.annotate('source: AEROCOM', xy=(0.88, 0.04), xycoords='figure fraction',
                            horizontalalignment='right', fontsize=10, bbox=dict(boxstyle='square', facecolor='none',
                                                                                edgecolor='black'))
                ax.annotate(model, xy=(-174., -83.), xycoords='data', horizontalalignment='left', fontsize=13,
                            color='black', bbox=dict(boxstyle='square', facecolor='white', edgecolor='none', alpha=0.7))

                # plt.ylabel(_title(plot_defn.coords[0], with_units=True))
                # plot_defn = iplt._get_plot_defn(cube, mode, ndims)

                plt.colorbar(spacing='uniform', ticks=colorbar_ticks,
                             boundaries=colorbar_levels, extend='max')

                ax.coastlines()
                ax.set_xticks([-180., -120., -60., 0., 60, 120, 180], crs=ccrs.PlateCarree())
                ax.set_yticks([-90., -60, -30, 0., 30, 60, 90], crs=ccrs.PlateCarree())
                lon_formatter = LongitudeFormatter(number_format='.1f', degree_symbol='')
                lat_formatter = LatitudeFormatter(number_format='.1f', degree_symbol='')
                ax.xaxis.set_major_formatter(lon_formatter)
                ax.yaxis.set_major_formatter(lat_formatter)

                plt.xlabel = 'longitude'
                plt.ylabel = 'latitude'

                plt.title(title)
                plt.savefig(plotfilename, dpi=300)
                plt.close()
                #pdb.set_trace()

        elif PlotMonthlyFlag:
            #calculate monthly data

            iris.coord_categorisation.add_month(cube, TIME_VAR_NAME, name='month_number')
            iris.coord_categorisation.add_year(cube, TIME_VAR_NAME, name='month_year')
            cube_monthly = cube.aggregated_by(['month_number', 'month_year'], iris.analysis.MEAN)

            for time_sub_cube in cube_monthly.slices_over(TIME_VAR_NAME):
                pre_grid_areas = iris.analysis.cartography.area_weights(time_sub_cube)
                # pdb.set_trace()
                # print(time_sub_cube)

                # Perform the area-weighted mean for each of the datasets using the
                # computed grid-box areas.
                weighted_mean = time_sub_cube.collapsed(['latitude', 'longitude'],
                                                        iris.analysis.MEAN,
                                                        weights=pre_grid_areas)

                time = (unit.num2date(time_sub_cube.coord(TIME_VAR_NAME).points,
                                      time_sub_cube.coord(TIME_VAR_NAME).units.name,
                                      time_sub_cube.coord(TIME_VAR_NAME).units.calendar))

                date = str(time[0]).split(' ')[0].replace('-', ' ')[0:7]
                Year = date[0:4]
                TsStr = 'm' + date[-2:]
                PlotType = 'MAP'

                title = " ".join([var, date, 'mean: {:6.3f}'.format(float(weighted_mean.data))])
                # ABS550_AER_an2012_mALLYEAR_WORLD_ZONALOBS_AERONETSky.ps.png
                # OD550_AER_an2017_d20171125_WORLD_MAP.ps.png
                plotfilename = os.path.join(plotdir, '_'.join([var, "an" + Year, TsStr, filter, PlotType]) + ".png")
                if verbose:
                    print(plotfilename)
                LatsToPlot = time_sub_cube.coord(axis='X').points
                LonsToPlot = time_sub_cube.coord(axis='Y').points
                xticks = [-180., -120., -60., 0., 60, 120, 180]
                yticks = [-90., -60, -30, 0., 30, 60, 90]
                plot_ts_map(time_sub_cube, title, plotfilename, LatsToPlot, LonsToPlot, colorbar_ticks,
                            colorbar_levels, colormap, model, xticks, yticks)

def annotate_aerocom(ax):
    """annotate with source: aerocom
    :rtype: None
    """

    ax.annotate('source: AEROCOM', xy=(0.88, 0.04), xycoords='figure fraction',
                horizontalalignment='right', fontsize=10, bbox=dict(boxstyle='square', facecolor='none',
                                                                    edgecolor='black'))

def plot_ts_map(data, title, plotfilename, lats_to_plot, lons_to_plot, colorbar_ticks, colorbar_levels,
                colormap, model_name,xticks, yticks,
                VerboseFlag = False):

    """function to plot one time step of a cube for aerocom"""

    plot = iplt.pcolormesh(data, cmap=colormap, vmin=0., vmax=max(colorbar_levels))
    plot.axes.set_aspect(1.8)
    plot.axes.axis([lats_to_plot.min(), lats_to_plot.max(), lons_to_plot.min(), lons_to_plot.max()])
    # axis = plt.axis([LatsToPlot.min(), LatsToPlot.max(), LonsToPlot.min(), LonsToPlot.max()])
    ax = plot.axes
    annotate_aerocom(ax)
    ax.annotate(model_name, xy=(-174., -83.), xycoords='data', horizontalalignment='left', fontsize=13,
                color='black', bbox=dict(boxstyle='square', facecolor='white', edgecolor='none', alpha=0.7))

    # plt.ylabel(_title(plot_defn.coords[0], with_units=True))
    # plot_defn = iplt._get_plot_defn(cube, mode, ndims)

    plt.colorbar(spacing='uniform', ticks=colorbar_ticks, boundaries=colorbar_levels, extend='max')

    ax.coastlines()
    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    # ax.set_xticks([-180., -120., -60., 0., 60, 120, 180], crs=ccrs.PlateCarree())
    # ax.set_yticks([-90., -60, -30, 0., 30, 60, 90], crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(number_format='.1f', degree_symbol='')
    lat_formatter = LatitudeFormatter(number_format='.1f', degree_symbol='')
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    plot.axes.set_title(title)
    plot.axes.set_xlabel('longitude')
    plot.axes.set_ylabel('latitude')
    plt.savefig(plotfilename, dpi=300)
    #pdb.set_trace()
    plt.close()
