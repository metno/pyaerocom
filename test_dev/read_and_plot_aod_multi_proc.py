"""Test script to read and plot netCDF files containing global AOD time series
"""

import matplotlib
matplotlib.use("Agg")

from argparse import ArgumentParser
from matplotlib.colors import BoundaryNorm
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg #canvas
from time import time
import iris
from os.path import exists, join
import multiprocessing
from matplotlib.pyplot import get_cmap, close
import numpy as np
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from functools import partial

import suppl_funs as funs
from GLOB import OUT_DIR
from GLOB import TEST_FILE as PATH

RUN_ALL = 1
# the following two variables are only relevant if RUN_ALL is True
LAST_DAY = 10#82
COMPARE_PERFORMANCE = 0

CMAP = "jet"
COASTLINE_COLOR = "#e6e6e6"

PARSER = ArgumentParser()
PARSER.add_argument("--last_day", nargs='?', type=int, default=LAST_DAY)
PARSER.add_argument("--comp", help=("Compare performance between multi and "
                    "serial processing"), nargs='?', type=int, 
                    default=COMPARE_PERFORMANCE)

BOUNDS = {'od550dust'   :   (0, 1),
          'od550bc'     :   (0, .2),
          'od550aer'    :   (0, 1),
          'od550so4'    :   (0, .4),
          'od550oa'     :   (0, .4)}

# regions for plotting
REGIONS = {"WORLD"      :   ((-180, 180), (-90, 90)),
           "EUROPE"     :   ((-20, 70)  , (30, 80)),
           "ASIA"       :   ((40, 150)  , (0, 60)),
           "AUSTRALIA"  :   ((90, 180)  , (-45, 0)),
           "CHINA"      :   ((90, 140)  , (10, 60)),
           "INDIA"      :   ((65, 90)   , (5, 35)),
           "NAFRICA"    :   ((-20, 50)  , (0, 40)),
           "SAFRICA"    :   ((0, 50)    , (-40, 0)),
           "SAMERICA"   :   ((-105, -30), (-60, 20)),
           "NAMERICA"   :   ((-150, -45), (10, 80))}

# Save name dummy
#OD550_AER_an2018_d20180319_WORLD_MAP.ps.png


FIGH = 6 #inches @100dpi
       
def prepare_args_multiprocessing(cubes, last_day_idx=None, regions=REGIONS, 
                                 bounds=BOUNDS, figh=FIGH):
    """Initiate data for multiprocessing
    
    Initiate all data such that plotting jobs using :func:`plot_all_days` can 
    be performed parallel, where each job corresponds to a certain region
    (e.g. EUROPE) and parameter (e.g. od550aer).
    
    Loops over all cubes found in :param:`cubes` (e.g. N=5) and over all 
    regions in dictionary :param:`regions` (e.g. M=10) and crops cube 
    correspondingly within defined lon / lat region and between first and last 
    day (defined using :param:`last_day_idx`). That makes a list of length 
    MxN containing the prepared cubes for each species and region. Further, 
    corresponding lists of all other required input parameters for 
    :func:`plot_all_days` are created for each of the cropped cubes, that is, 
    lists of length MxN of matplotlib figure instances, longitude range, 
    latitude range, lower and upper range of colorbar and the corresponding ID 
    of the region). 
    
    In order to prepared the input
    
    
    Parameters
    ----------
    cubes : iris.cube.CubeList
        list containing cubes of different species
    last_day_idx : :obj:`int`, optional
        index of last day that is supposed to be plotted
    regions : dict
        dictionary specifying region IDs (keys) and corresponding lon / lat
        ranges
    bounds : dict
        dictionary specifying min / max ranges (values) for plotting of 
        different species (keys). The latter must correspond to the species 
        IDs as defined in the :attr:`var_name` of the different
        :class:`iris.cube.Cube` instances in :param:`cubes`. 
    
    Returns
    -------
    tuple
        7-element tuple, containing the following lists of length MxN
        
        - list: cropped cubes for each species (n (m $$\in{N}$$)) and\
            region (m $$\in{M}$$)
        - list: corresponding Figure instances for plotting
        - list: corresponding longitude ranges (tuple containing min / max)
        - list: corresponding latitude ranges (tuple containing min / max)
        - list: lower value for color-range (depends on species)
        - list: upper value for color-range (depends on species)
        - list: string ID of corresponding region
    """
    args =[]    
    if last_day_idx is None:
        last_day_idx = cubes[0].coord("time").points[-1]
    for cube in cubes:
        print(cube.var_name)
        for region, val in regions.items():
            print(region)
            lon_range, lat_range = val
            t0=time()
            dat = funs.crop_cube_lonlat(cube, lon_range, lat_range)
            dat = dat[:last_day_idx]
            print("Elapsed time crop: %.4f" %(time()-t0))
            wfac = dat.coord("longitude").shape[0] / dat.coord("latitude").shape[0]
            figw = figh * wfac + 2
            t0=time()
            fig = Figure(figsize=(figw, figh), dpi=100)
            # create canvas to draw onto
            FigureCanvasAgg(fig)
            print("Elapsed time figure: %.4f" %(time()-t0))
            vmin, vmax = bounds[cube.var_name]
            
            args.append((dat, fig, lon_range, lat_range, float(vmin),
                         float(vmax), region))
            
    return tuple(args)

def plot_all_days(cube, fig, lon_range, lat_range, vmin, vmax, region_id, 
                  dirs):
    """Plot all days for a specific variable and region"""
    var_id = funs.var_str(cube)
    
    for j in range(cube.shape[0]):
        fig = plot_day_logspacing(cube, fig, j, lon_range, lat_range, 
                                  vmin, vmax)
        #pause(0.005)
        name = funs.save_name(cube, day_idx=j, region_id=region_id)
        #fig.savefig(join(dirs[var_id][region_id], name))
        
        fig.savefig(join(dirs[var_id][region_id], name))
        fig.clf()
        print("Species: %s (%s, %s)" %(var_id, funs.daystring(cube, j), 
              region_id))
            
def plot_day_logspacing(cube, fig, day_idx=0, lon_range=(-180, 180), 
                        lat_range=(-90, 90), vmin=None, vmax=None, 
                        cmap_id=CMAP):
    """Plot variable on map using pcolormesh
    
    Parameters
    ----------
    cube : iris.cube.Cube
        cube containing data. Note that the input cube must correspond 2D cube
        containing data from one time stamp (i.e. ndim=2).
    day_idx : int
        index of timestamp that is to be plotted
    lon_range : tuple
        tuple specifying plotted longitude range 
    lat_range : tuple
        tuple specifying plotted latitude range
    vmin : float
        lower limit for AOD display
    vmax : float
        upper limit for AOD display
    cmap_id : str
        string ID of matplotlib colormap supposed to be used
    """    
    if fig.canvas is None:
        FigureCanvasAgg(fig)
    if cube.ndim != 3:
        msg = ("Invalid dimension %d of input cube, need ndim=2 (i.e. data "
               "corresponding to one timestamp" %cube.ndim)
        raise ValueError(msg)
    dat = cube[day_idx]
    
    geo_ax = fig.add_axes([0.1, .1, .8, .8], projection=ccrs.PlateCarree())
    ax_cbar = fig.add_axes([0.85, .1, .02, .8])
    
    lvls = funs.init_cmap_levels(vmin, vmax)
    cmap = get_cmap(cmap_id)
    norm = BoundaryNorm(lvls, ncolors=cmap.N, clip=True)
    
    lons, lats = dat.coord("longitude").points, dat.coord("latitude").points
    X, Y = np.meshgrid(lons, lats)
    mesh = geo_ax.pcolormesh(X, Y, dat.data, cmap=cmap, norm=norm)#, figure=fig)
    #mesh = iplt.pcolormesh(cube,cmap=cmap, norm=norm, figure=fig)
    geo_ax.coastlines(color=COASTLINE_COLOR)
    #things that do not need to be done when day is updated
    
    ticks = funs.get_cmap_ticks(lvls)
# =============================================================================
#     try:
#         ax_cbar = fig.axes[1]
#         [x.remove for x in ax_cbar.artists]
# =============================================================================
    cbar = fig.colorbar(mesh, norm=norm, boundaries=lvls, cax=ax_cbar)
# =============================================================================
#     except:
#         cbar = fig.colorbar(mesh, norm=norm, boundaries=lvls)
# =============================================================================
    # Set some suitable fixed "logarithmic" colourbar tick positions.
    cbar.set_ticks(ticks)
    cbar.set_label(funs.var_str(dat))
    # Modify the tick labels so that the centre one shows "+/-<minumum-level>".
    #tick_levels[3] = r'$\pm${:g}'.format(minimum_log_level)
    cbar.set_ticklabels(["%.3f" %x for x in ticks])
    
    geo_ax.set_xlim([lon_range[0], lon_range[1]])
    geo_ax.set_ylim([lat_range[0], lat_range[1]])
    
    geo_ax.set_xticks(np.linspace(lon_range[0], lon_range[1], 7), 
                   crs=ccrs.PlateCarree())
    geo_ax.set_yticks(np.linspace(lat_range[0], lat_range[1], 7), 
                   crs=ccrs.PlateCarree())
    
    lon_formatter = LongitudeFormatter(number_format='.1f',
                                       degree_symbol='',
                                       dateline_direction_label=True)
    lat_formatter = LatitudeFormatter(number_format='.1f',
                                      degree_symbol='')
    
    geo_ax.xaxis.set_major_formatter(lon_formatter)
    geo_ax.yaxis.set_major_formatter(lat_formatter)

    geo_ax.set_xlabel("Longitude", fontsize=12)
    geo_ax.set_ylabel("Latitude", fontsize=12)
    # Label the colourbar to show the units.
    #bar.set_label('[{}, log scale]'.format(anomaly.units))
    tit = ("%s %s mean: %.3f" %(funs.var_str(dat), 
                                funs.daystring(cube, day_idx),
                                funs.area_weighted_mean(dat)))
    geo_ax.set_title(tit)
    return fig


def plot_multiproc(plot_fun, args_multiproc):
    t0 = time()
    pool = multiprocessing.Pool()
    pool.starmap(plot_fun, args_multiproc)
    pool.close()
    pool.join()
    dt = time() - t0
    print("Elapsed time multiprocessing: %s s" %dt)
    return dt
        
if __name__=="__main__":
    iris.FUTURE.netcdf_promote = True
    close("all")
    if not exists(PATH):
        raise IOError("Path %s does not exist" %PATH)
    
    opts = PARSER.parse_args()
    print(opts)

    #funs.custom_mpl(rcParams)
    cubes = iris.load(PATH)
    
    
    if RUN_ALL:
        dirs = funs.init_save_dirs(cubes, REGIONS, OUT_DIR)
        
        args_multiproc = prepare_args_multiprocessing(cubes, opts.last_day, REGIONS)
        plot_fun = partial(plot_all_days, dirs=dirs)
        
        dt = plot_multiproc(plot_fun, args_multiproc)
        
        if opts.comp:
            t0 = time()
            for input_args in args_multiproc:
                plot_all_days(*input_args, dirs=dirs)
            dt1 = time() - t0
            
            print("Number of plotted days / species / regions: %d / %d / %d\n"
                  "Elapsed time multiprocessing: %s s\n" 
                  "Elapsed time serial processing: %s s" 
                  %(args_multiproc[0][0].shape[0], len(cubes), len(REGIONS), dt, dt1))
        
    
    
    
    
    
    
    
    
    
    
    
