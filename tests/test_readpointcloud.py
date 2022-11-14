from importlib.metadata import metadata
from socket import gethostname

import xarray as xr
from readpointcloud import ReadPointCloud

if gethostname() == "pc5654":  # if working locally
    obs_file_path = "/home/lewisb/data/TROPOMI/CopernicusHub/O3_Profiles/"
else:  # probably on PPI
    obs_file_path = "/lustre/storeB/users/lewisb/data/TROPOMI/CopernicusHub/O3_Profiles/"


obs_test_files = []
obs_test_files.append(
    obs_file_path
    + "S5P_OFFL_L2__O3__PR_20211231T010540_20211231T024709_21844_02_020301_20220101T165013.nc"
)

breakpoint()


def test_read_netcdf_file_group_product():
    reader = ReadPointCloud()
    xarray_data = reader.read_netcdf_file(obs_test_files[0], group="PRODUCT")
    assert isinstance(xarray_data, xr.Dataset)


def test_read_netcdf_product_attributes():
    pass


def test_generic_test_for_testing():
    reader = ReadPointCloud(data_id="profileo3", data_dir=obs_file_path)
    print("made reader")
    breakpoint()


test_generic_test_for_testing()

# test_read_netcdf_product_attributes()
