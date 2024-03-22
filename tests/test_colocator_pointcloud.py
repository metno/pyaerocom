import time

import pytest

from colocator_pointcloud import (colocate_pointcloud_gridded,
                                  colocate_pointcloud_pointcloud)
from pointclouddata import PointCloudData
from readpointcloud import ReadPointCloud

# LB: Alot of this porbably could go into a fixture later
obs_file_path = "/home/lewisb/data/TROPOMI/CopernicusHub/O3_Profiles/"
model_file_path = "/home/lewisb/data/MODELDATA/"

obs_test_files = []
obs_test_files.append(obs_file_path + "S5P_OFFL_L2__O3__PR_20211231T010540_20211231T024709_21844_02_020301_20220101T165013.nc")


model_test_files = []
model_test_files.append(model_file_path + "dummy_data.nc")
model_test_files.append(model_file_path + "Base_hour_cjx.nc")

# With custom ReadPointCloud Class
var_name = "profileo3"
obs_name = 'ozone_profile' # for now just a string, but in theory might want other product.variables
vars_to_read_in = [obs_name, "altitude", "time_utc", "qa_value"] # select a subsect of the PRODUCT group to read in. Include averaging_kernel?
core_columns_name_order = ["time_utc", "longitude", "latitude", "altitude", obs_name, "qa_value"] # dictionary of how I want to order the column

chunksize = 7.5 * 1e3 #1e5

reader = ReadPointCloud() # using for reading in dummy model data


data = PointCloudData()

# Compare memory and timing
## Numpy
# st = time.time()
# obs_arr = data.data_numpy(filename = obs_test_files[0], vars_to_read_in = vars_to_read_in, core_columns_name_order = core_columns_name_order)
# et = time.time()
# print(f"obs_arr is {obs_arr.nbytes / 1e6 :.2f} MB and took {et-st :.2f} seconds to compute")

## Dask array
# st = time.time()
# obs_dist = data.data_distributed_array(filename = obs_test_files[0], vars_to_read_in = vars_to_read_in, core_columns_name_order = core_columns_name_order)
# # LB: at this point obs_dist has still not been computed.
# obs_dist = obs_dist.rechunk({0: chunksize}, balance = True)

# # LB: Wish we could try below but I get NotImplementedError cause dtype=object, but maybe there is a way to figure this out
# # obs_dist = obs_dist.rechunk({0: -1, 1: 'auto'}, block_size_limit=1e8, balance=True) # rechunk the big array into smaller pieces automatically along rows but balance them to be roughly the same size
# tmp_obs_dist = obs_dist.compute() # after this point there are no partitions unless specified beforehand
# et = time.time()
# print(f"obs_dist is {tmp_obs_dist.nbytes / 1e6 :.2f} MB takes {et-st} seconds to compute in local memory")
# del tmp_obs_dist

# assert obs_arr.shape == obs_dist.shape # should be getting the exact same thing despite hacking filtering on dask QA_THRESHOLD

# Read in the "model"
# Make fake model data by making a copy of the coordinates
MODEL_OBS_IDX = data.OBSERVATION_IDX # temporary for testing

@pytest.fixture
def dummy_model():
    reader = ReadPointCloud() # Model data is on a grid but whatever
    return reader.read_netcdf_file_product(f"{model_file_path}dummy_data.nc")

@pytest.fixture
def obs_one_orbit_file():
    obs_dist = data.data_distributed_array(filename = obs_test_files[0], vars_to_read_in = vars_to_read_in, core_columns_name_order = core_columns_name_order)
    obs_dist = obs_dist.rechunk({0: chunksize}, balance = True)
    return obs_dist.compute()

# @pytest.fixture
# def obs_one_orbit_file_pandas_df():
#     return data.data_df(filename = obs_test_files[0], vars_to_read_in = vars_to_read_in, core_columns_name_order = core_columns_name_order)


@pytest.mark.parametrize(
    "obs, model,allowable_delta_t,allowable_distance",
    [
        # (obs_one_orbit_file.blocks[0].compute(), obs_one_orbit_file, 30, 0),
    ]
)
def test_colocate_pointcloud_pointcloud_one_block_same_data(obs, model, allowable_delta_t, allowable_distance):
    colocated = colocate_pointcloud_pointcloud(obs = obs, model = model, allowable_delta_t = allowable_delta_t, allowable_distance=allowable_distance)
    assert all(colocated[:,data.OBSERVATION_IDX] - colocated[:, MODEL_OBS_IDX] == 0)


# @pytest.mark.parametrize(
#     "obs, model",
#     [
#         #(obs_one_orbit_file, dummy_model),
#         #(obs_one_orbit_file_pandas_df, dummy_model),
            
#     ]
# )

def test_colocate_pointcloud_gridded_one_block():
    st = time.time()
    # Test differences between distributed dataframe and single dataframe
    obs = data.data_distributed_df(filename = obs_test_files[0], vars_to_read_in = vars_to_read_in, core_columns_name_order = core_columns_name_order) 
    obs = obs.repartition(partition_size = "50MB") # temporary parition size for testing
    model = reader.read_netcdf_file(filename=f"{model_file_path}dummy_data.nc")
    colocated = colocate_pointcloud_gridded(obs.partitions[0].compute(), model)
    et = time.time()
    print(f"{et-st} seconds")
    assert obs.columns.size < colocated.columns.size # should now have a new column with model data






# temporary for testing, pytest will take care of this stuff eventually
# test_colocate_pointcloud_pointcloud_one_block_same_data()
#test_colocate_pointcloud_gridded_one_block()
