from importlib.metadata import metadata

import xarray as xr

from readpointcloud import ReadPointCloud

obs_file_path = "/home/lewisb/data/TROPOMI/CopernicusHub/O3_Profiles/"

obs_name = 'ozone_profile'

obs_test_files = []
obs_test_files.append(obs_file_path + "S5P_OFFL_L2__O3__PR_20211231T010540_20211231T024709_21844_02_020301_20220101T165013.nc")

core_columns_name_order = ["time_utc", "longitude", "latitude", "altitude", obs_name, "qa_value"]

def test_read_netcdf_file_group_product():
    reader = ReadPointCloud()
    xarray_data = reader.read_netcdf_file(obs_test_files[0], group = "PRODUCT")
    assert isinstance(xarray_data, xr.Dataset)

def test_read_netcdf_product_attributes():
    pass

def test_generic_test_for_testing():
    reader = ReadPointCloud(data_id = "profileo3", data_dir = obs_file_path)
    print("made reader")
    breakpoint()

test_generic_test_for_testing()

#test_read_netcdf_product_attributes()
