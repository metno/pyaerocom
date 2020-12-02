
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
from matplotlib.axes import Axes
from cartopy.mpl.geoaxes import GeoAxes
from matplotlib.colors import ListedColormap
from seaborn import color_palette

def griddeddata_to_jsondict(data, lat_res_deg=5, lon_res_deg=5):

    if not data.ts_type == 'monthly':
        data = data.resample_time('monthly')

    data = data.regrid(lat_res_deg=lat_res_deg, lon_res_deg=lon_res_deg)

    try:
        data.check_dimcoords_tseries()
    except:
        data.reorder_dimensions_tseries()

    arr = data.to_xarray()
    latname, lonname = 'lat', 'lon'
    try:
        stacked = arr.stack(station_name=(latname, lonname))
    except:
        latname, lonname = 'latitude', 'longitude'
        stacked = arr.stack(station_name=(latname, lonname))

    dd = {}

    dd['time'] = [pd.to_datetime(t).strftime('%Y-%m-%d') for t in data.time_stamps()]

    nparr = stacked.data
    for i, (lat, lon) in enumerate(stacked.station_name.values):

        coord = lat, lon
        vals = nparr[:, i]
        dd[str(coord)] = sd = {}
        sd['lat'] = lat
        sd['lon'] = lon
        sd['data'] = vals.tolist()

    return dd

def calc_contour_json(data, vmin=None, vmax=None, cmap=None, nlayers=None,
                      try_use_default_layers=True):

    vardef = data.var_info

    if cmap is None:
        cmap = vardef.map_cmap
        if not isinstance(cmap, str):
            cmap = 'Blues'
    if nlayers is None:
        nlayers = 10
    try:
        import geojsoncontour
    except ModuleNotFoundError:
        raise ModuleNotFoundError('Map processing for web interface requires '
                                  'library geojsoncontour which is not part of the '
                                  'standard installation of pyaerocom.')

    GeoAxes._pcolormesh_patched = Axes.pcolormesh
    # ToDo: check if matplotib backend 'agg' can be used
    #plt.style.use('ggplot')
    levels = None
    if try_use_default_layers:
        levels = vardef.map_cbar_levels
        if isinstance(levels, list) and len(levels) > 0:
            vmin, vmax = levels[0], levels[-1]

    if vmin is None:
        vmin = vardef.map_vmin
    if vmax is None:
        vmax = vardef.map_vmax

    if any([x is None for x in [vmin, vmax]]):
        raise ValueError('Please specify vmin, vmax')

    if levels is None:
        levels = np.linspace(vmin, vmax, nlayers)

    cm = ListedColormap(color_palette(cmap, len(levels)-1))

    proj = ccrs.PlateCarree()
    ax = plt.axes(projection=proj)

    try:
        data.check_dimcoords_tseries()
    except:
        data.reorder_dimensions_tseries()

    nparr = data.cube.data
    lats = data.latitude.points
    lons = data.longitude.points

    geojson = {}

    for i, month in enumerate(data.time_stamps()):
        date = str(month).split('T')[0]
        datamon = nparr[i]
        contour = ax.contourf(lons, lats, datamon,
                              transform=proj,
                              colors=cm.colors,
                              levels=levels)

        result = geojsoncontour.contourf_to_geojson(
                    contourf=contour
                    )

        geojson[date] = eval(result)

    cb = ax.figure.colorbar(contour, ax=ax)
    #set the legend in one key

    from matplotlib.colors import to_hex
    colors_hex = [to_hex(val) for val in cm.colors]

    geojson['legend'] = {
        'colors': colors_hex,
        'levels':  list(levels)
    }
    return geojson

if __name__ == '__main__':
    import pyaerocom as pya
    dd = '/home/jonasg/MyPyaerocom/AEROCOM-MEDIAN-2x3-GLISSETAL2020-1_AP3-CTRL/renamed'
    reader = pya.io.ReadGridded('AEROCOM-MEDIAN-2x3-GLISSETAL2020-1_AP3-CTRL',
                              data_dir=dd)

    data = reader.read_var('od550aer', start=2010)

    griddeddata_to_jsondict(data)








