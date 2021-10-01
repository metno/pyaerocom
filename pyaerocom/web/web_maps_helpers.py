
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
from matplotlib.axes import Axes
from cartopy.mpl.geoaxes import GeoAxes
from matplotlib.colors import ListedColormap
from seaborn import color_palette

# ToDo: this needs to be revisited and reorganised for later processing of
# multiyear data which may be lower resolution than monthly.
RES_TIME_INFO = {'monthly' : '%Y-%m-15'}

def _get_timestamps_json(data):
    tt = data.ts_type
    if not data.ts_type in RES_TIME_INFO:
        raise ValueError(f'GriddedData needs to be in either of the '
                         f'supported resolutions: {RES_TIME_INFO.keys()}')
    fmt = RES_TIME_INFO[tt]
    return [pd.to_datetime(t).strftime(fmt) for t in data.time_stamps()]

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

    dd['time'] = _get_timestamps_json(data)

    nparr = stacked.data.astype(np.float64)
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
    tst = _get_timestamps_json(data)
    for i, date in enumerate(tst):
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








