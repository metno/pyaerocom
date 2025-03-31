"""
Helper methods for access of and working with land/sea masks. pyaerocom
provides automatic access to HTAP land sea masks from this URL:

https://pyaerocom.met.no/pyaerocom-suppl

Filtering by these masks is implemented in :class:`Filter` and all relevant
data classes (i.e. :class:`GriddedData`, :class:`UngriddedData`,
:class:`ColocatedData`).
"""

import glob
import logging
import os

import numpy as np
import requests
import xarray as xr
from iris import load_cube

from pyaerocom import const
from pyaerocom.exceptions import DataRetrievalError
from pyaerocom.helpers import numpy_to_cube

logger = logging.getLogger(__name__)


def available_htap_masks():
    """
    List of HTAP mask names

    Returns
    ----------
    list
        Returns a list of available htap region masks.
    """
    return const.HTAP_REGIONS


def download_htap_masks(regions_to_download=None):
    """Download HTAP mask

    URL: https://pyaerocom.met.no/pyaerocom-suppl.

    Parameters
    -----------
    regions_to_download : list
        List containing the regions to download.

    Returns
    -------
    list
        List of file paths that point to the mask files that were successfully
        downloaded

    Raises
    ------
    ValueError
        if one of the input regions does not exist
    DataRetrievalError
        if download fails for one of the input regions
    """

    if regions_to_download is None:
        regions_to_download = const.HTAP_REGIONS
    elif isinstance(regions_to_download, str):
        regions_to_download = [regions_to_download]
    elif not isinstance(regions_to_download, list):
        raise ValueError("Invalid input for regions_to_download, need list or str")

    path_out = const.FILTERMASKKDIR
    base_url = const.URL_HTAP_MASKS

    paths = []
    for region in regions_to_download:
        if region not in const.HTAP_REGIONS:
            raise ValueError(f"No such HTAP region {region}")
        elif region == "EAS":
            filename = f"{region}htap.nc"
            file_out = os.path.join(path_out, f"{region}htap.0.1x0.1deg.nc")
        else:
            filename = f"{region}htap.0.1x0.1deg.nc"
            file_out = os.path.join(path_out, filename)

        url = os.path.join(base_url, filename)

        try:
            r = requests.get(url)
            open(file_out, "wb").write(r.content)
            paths.append(file_out)
        except Exception as e:
            raise DataRetrievalError(f"Failed to download HTAP mask {region}. Reason {repr(e)}")
    return paths


def get_htap_mask_files(*region_ids):
    """Get file paths to input HTAP regions

    Parameters
    ----------
    *region_ids
        ID's of regions for which mask files are supposed to be retrieved

    Returns
    -------
    list
        list of file paths for each input region

    Raises
    ------
    FileNotFoundError
        if default local directory for storage of HTAP masks does not exist
    NameError
        if multiple mask files are found for the same region
    """
    mask_dir = const.FILTERMASKKDIR
    if not os.path.exists(mask_dir):
        raise FileNotFoundError("HTAP mask directory does not exist")
    out = []
    for region in region_ids:
        if region not in const.HTAP_REGIONS:
            raise ValueError(f"No such HTAP region {region}")
        files = glob.glob(os.path.join(mask_dir, f"{region}*.nc"))
        if len(files) != 1:
            if len(files) == 0:
                logger.info(f"Downloading HTAP mask {region}")
                files = download_htap_masks(region)
            elif len(files) > 1:
                raise NameError(f"Found multiple masks for region {region}")
        out.append(files[0])
    return out


def load_region_mask_xr(*regions):
    """Load boolean mask for input regions (as xarray.DataArray)

    Parameters
    -----------
    *regions
        regions that are supposed to be loaded and merged (just use string,
        no list or similar)

    Returns
    ---------
    xarray.DataArray
        boolean mask for input region(s)
    """
    masks = None
    for i, fil in enumerate(get_htap_mask_files(*regions)):
        r = regions[i]
        if i == 0:
            masks = xr.load_dataset(fil)[r + "htap"]
            name = r
        else:
            masks += xr.load_dataset(fil)[r + "htap"]
            name += f"-{r}"
    if masks is not None:
        mask = masks.where(masks < 1, 1)
    mask["name"] = name
    mask.attrs["long_name"] = name
    mask = mask.rename({"lat": "latitude", "long": "longitude"})
    return mask


def load_region_mask_iris(*regions):
    """Loads regional mask to iris.

    Parameters
    -----------
    region_id : str
        Chosen region.

    Returns
    ---------
    iris.cube.Cube
        cube representing merged mask from input regions
    """
    cubes = []
    names = []
    for i, fil in enumerate(get_htap_mask_files(*regions)):
        names.append(regions[i])
        cubes.append(load_cube(fil))
    if len(cubes) == 1:
        out = cubes[0]
    else:
        merged_np = np.max([x.data for x in cubes], axis=0)
        out = numpy_to_cube(merged_np, dims=(cubes[0].coords()[0], cubes[0].coords()[1]))
        out.units = cubes[0].units
    name = "-".join(names)
    out.var_name = name
    # out.attributes['long_name'] = name
    return out


def get_mask_value(lat, lon, mask):
    """Get value of mask at input lat / lon position

    Parameters
    ----------
    lat : float
        latitude
    lon : float
        longitude
    mask : xarray.DataArray
        data array

    Returns
    -------
    float
        nearest neighbour mask value to input lat lon
    """
    if not isinstance(mask, xr.DataArray):
        raise ValueError(f"Invalid input for mask: need DataArray, got {type(mask)}")
    return float(mask.sel(latitude=lat, longitude=lon, method="nearest"))


def check_all_htap_available():
    """
    Check for missing HTAP masks on local computer and download
    """
    return get_htap_mask_files(*available_htap_masks())


def get_lat_lon_range_mask_region(mask, latdim_name=None, londim_name=None):
    """
    Get outer lat/lon rectangle of a binary mask

    Parameters
    ----------
    mask : xr.DataArray
        binary mask
    latdim_name : str, optional
        Name of latitude dimension. The default is None, in which case lat is
        assumed.
    londim_name : str, optional
        Name of longitude dimension. The default is None, in which case long is
        assumed.

    Returns
    -------
    dict
        dictionary containing lat and lon ranges of the mask.

    """
    if latdim_name is None:  # htap
        latdim_name = "lat"
    if londim_name is None:
        londim_name = "long"  # htap
    assert isinstance(mask, xr.DataArray)
    assert mask.dims == (latdim_name, londim_name)

    data = mask.data
    lats = mask.latitude.data
    lons = mask.longitude.data

    lonmask = np.where(data.any(axis=0))[0]  # flatten latitude dimension
    firstidx, lastidx = lonmask.min(), lonmask.max()
    lonr = sorted([lons[firstidx], lons[lastidx]])

    latmask = np.where(data.any(axis=1))[0]  # flatten latitude dimension
    firstidx, lastidx = latmask.min(), latmask.max()
    latr = sorted([lats[firstidx], lats[lastidx]])

    return dict(lat_range=latr, lon_range=lonr)
