import datetime
import logging
from time import timezone

import numpy as np
import pandas as pd
import xarray as xr
from memory_profiler import profile

from pointclouddata import PointCloudData

logger = logging.getLogger(__name__)

# import pyaerocom as pya
# from pandas import Timestamp
# from pyaerocom.extras.satellite_l2.sentinel5p import ReadL2Data
# from pyaerocom.plugins.mscw_ctm.reader import ReadMscwCtm


data = PointCloudData()

# Temporary for testing
MODEL_TIME_IDX = data.TIME_IDX 
MODEL_LON_IDX = data.LONGITUDE_IDX
MODEL_LAT_IDX = data.LATITUDE_IDX
MODEL_LAT_IDX = data.ALTITUDE_IDX
MODEL_DATA_IDX = data.OBSERVATION_IDX
MODEL_OUTPUT_NAME = "array" # somehow need to infer this from model, which will be a GriddedData object
ts_type = "H" # this is a conflicting notation but the ts_type in pyaerocom in the end will determin the time frequency at which to round to (https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases)



## Read in the observations
#obs_reader = ReadPointCloud()
#obs_arr = obs_reader.data(file_path = obs_file_path, vars_to_read_in=vars_to_read_in, core_columns_name_order=core_columns_name_order)

# LB: Note incorporate below into PoitnCloudData 
#attributes = obs_reader.netcdf_product_attributes(file_path=obs_file_path, file_name = "S5P_OFFL_L2__O3__PR_20211231T010540_20211231T024709_21844_02_020301_20220101T165013.nc" , obs_name=obs_name)



def compute_distance(arr1: np.array = None, arr2: np.array = None):
    """
    Generic distance function. Currently Euclidean distance
    """
    return np.linalg.norm(arr1-arr2, axis = -1)

def intersect2D(a, b):
  """
  Find row intersection between 2D numpy arrays, a and b.
  Returns another numpy array with shared rows
  Credit: https://gist.github.com/Robaina/b742f44f489a07cd26b49222f6063ef7
  """
  return np.array([x for x in set(tuple(x) for x in a) & set(tuple(x) for x in b)])

#@profile
def colocate_pointcloud_pointcloud(obs: np.array = None, model: np.array = None, allowable_delta_t: float = 0, allowable_distance: float = 0):
    """
    Given two pointcloud with the same ts_type (i.e.., on the same temporal grid), collocate them
    """


    if obs is None and model is None:
        return np.empty()

    date_format = pd.datetime # trying different date formats for testing

    #allowable_delta_t = np.timedelta64(allowable_delta_t, "s")
    #allowable_delta_t = datetime.timedelta(seconds=allowable_delta_t)
    allowable_delta_t = pd.Timedelta(seconds = allowable_delta_t)

    # # Saftey check which needs testing
    #assert np.all(isinstance(time, Timestamp) for time in obs[:,data.TIME_UTC_IDX])
    epoch_time = pd.Timestamp('1970-01-01 00:00:00.000000Z') # 112 bytes
    #breakpoint()
    # a little silly because they will be strings. np.datetime64 approach is depricated
    #if np.any(isinstance(obs[:, data.TIME_IDX], str)):
    #obs[:, data.TIME_IDX] = np.array(obs[:, data.TIME_IDX], dtype=np.datetime64) # depricated and will raise an error in future. datetime better?
    #obs[:, data.TIME_IDX] = pd.to_datetime(obs[:, data.TIME_IDX])
    obs_time_since_epoch = (pd.to_datetime(obs[:, data.TIME_IDX]) - epoch_time).total_seconds()
    obs_time_since_epoch = np.int32(obs_time_since_epoch) # each element 28 bytes
    #if np.any(isinstance(model[:, data.TIME_IDX], str)):
    #model[:, MODEL_TIME_IDX] = np.array(model[:, MODEL_TIME_IDX], dtype=np.datetime64)
    #model[:, MODEL_TIME_IDX] = pd.to_datetime(model[:, MODEL_TIME_IDX])
    model_time_as_pandas_date = pd.to_datetime(model[:, data.TIME_IDX]) 
    model_time_since_epoch = (model_time_as_pandas_date - epoch_time).total_seconds() # note the different approach that must be taken here because of the previous conversion. testing faster options
    model_time_since_epoch = np.int32(model_time_since_epoch)
    #model[:, data.TIME_IDX]= pd.to_datetime(model[:, data.TIME_IDX]) # may be clever, may cause pain later to only do this to model
    print("Finished converting times")
    logger.debug("Finished converting times")
   
    # Do temporal subsetting on model
    start_obs = pd.to_datetime(obs[0, data.TIME_IDX])
    stop_obs = pd.to_datetime(obs[-1, data.TIME_IDX])
    start_model_idx = np.argmax(start_obs - allowable_delta_t <= model_time_as_pandas_date) # np.argmax returns the index of first occurance of True
    stop_model_idx = np.argmax(stop_obs + allowable_delta_t <= model_time_as_pandas_date)
    # Consider onlt the subset of the model which is within the same temporal subset as the obs chunk
    model = model[start_model_idx:stop_model_idx,:]
    model_time_since_epoch = model_time_since_epoch[start_model_idx:stop_model_idx]
    del model_time_as_pandas_date

    print("Computing temporal distance...")
    logger.debug("Computing temporal distance...")
    # this assumes same ts_type
    #delta_t = obs[:, data.TIME_IDX][:, None] - model[:, MODEL_TIME_IDX][None, :] # This is the (first) bottleneck. Could turing this into a difference of seconds and then convertin back be faster?
    delta_t = obs_time_since_epoch[:, None] - model_time_since_epoch[None, :]
    print("Delta_t computed. Computing valid_time...")
    logger.debug("Delta_t computed. Computing valid_time...")
    
    valid_time = np.array(np.where(delta_t <= allowable_delta_t.total_seconds())).transpose() 
    print("valid_time computed...")
    logger.debug("valid_time computed...")
    
    del delta_t, model_time_since_epoch, obs_time_since_epoch # clear out of memory A$AP
    print("Temporal distance computed and cleared from memory")
    logger.debug("Temporal distance computed and cleared from memory") 


    print("Computing spatial distance...")
    logger.debug("Computing spatial distance...")
    # Now compute spatial distance
    #breakpoint() # .astype(np.float32)
    distances = compute_distance(obs[:, [data.LONGITUDE_IDX, data.LATITUDE_IDX, data.ALTITUDE_IDX]][:, None, ...].astype(np.float32), 
                                model[:, [MODEL_LON_IDX, MODEL_LAT_IDX, MODEL_LAT_IDX]][None, ...].astype(np.float32) 
    ) # this is actually quite fast
    #breakpoint()
    
    print("Spatial distance computed. Computing valid_distance...")
    logger.debug("Spatial distance computed. Computing valid_distance...")
    valid_distance = np.array(np.where(distances <= allowable_distance)).transpose()
    del distances
    print("Computed valid_distance. distances cleared from memory")
    logger.debug("Computed valid_distance. distances cleared from memory")

    # Idea: Get the intersection of the indices which are both temporally and spatially colocated
    # this approach is remarkably inefficient but np doesn't have a 2d intersection function and intersect1d isn't giving me what I want
    print("Computing intersection of valid indcies")# This is another bottleneck.
    logger.debug("Computing intersection of valid indcies")
    # Old method using nearly 500 MB for n = 750. Obscene
    #val_t = set((tuple(i) for i in np.array(valid_time).transpose()))
    #val_d = set((tuple(i) for i in np.array(valid_distance).transpose()))    
    #valid = val_t.intersection(val_d)
    #del val_t, val_d # maybe not required

    # attempting to make faster but this broadcasting method is failing for large arrrays. no idea why
    # Trying to make efficient but check not digging myself into a hole
    if len(valid_distance) < len(valid_time):
        intersect = (valid_distance[:, None] == valid_time).all(-1).any(1) # think I want to broadcast the smaller array
        valid = valid_distance[intersect]
    else:
        intersect = (valid_time[:, None] == valid_distance).all(-1).any(1) # compute intersection of 2d array with nump broadcasting
        valid = valid_time[intersect]
    del intersect

    # m = (A[:, None] == B).all(-1).any(1)
    # valid = intersect2D(np.array(valid_time).transpose(), np.array(valid_distance).transpose())
    # valid = np.array(list(valid)).transpose() 
    
    # consider sorting here. chunks should be sorted by time
    valid = valid[:, valid[0,:].argsort()] # sort on the 0th row, corresponding to the observation indices
    print("Valid indices computed")
    logger.debug("Valid indices computed")


    #print("COMPUTING EXPANDED OBS AND MODEL")
    #obs = obs[valid[0]]
    #model = model[valid[1]]
    #print("EXPANDED OBS AND MODEL COMPUTED")

    print("Allocating colocated array...")
    logger.debug("Allocating colocated array...")
    num_rows_to_allocate = len(obs) # each 
    num_cols_to_allocate = obs.shape[1] + 1 # store (t,x,y,z,o,m) 
    colocated_array = np.empty((num_rows_to_allocate, num_cols_to_allocate), dtype = object) # in serial case this is 80MB
    colocated_array[:,0:obs.shape[1]] = obs[valid[:,0]]
    colocated_array[:,-1] = model[valid[:,1], MODEL_DATA_IDX]
    print("Colocated array complete. Returning array...")
    logger.debug("Colocated array complete. Returning array...")
    return colocated_array


def colocate_pointcloud_gridded(obs : xr.DataArray = None, model = None):
    if obs is None and model is None:
        return

        # convert str time into datetime to be useful. 
    obs.time_utc = pd.to_datetime(obs.time_utc, utc = True) # this probably should be taken care of ahead of time in GriddedData

    # Drop the obs which are outside of the model domain
    in_model_lon_bounds = (model.longitude.min() <= obs[:, data.LONGITUDE_IDX] <= model.longitude.max())
    in_model_lat_bounds = (model.latitude.min() <= obs[:, data.LATITUDE_IDX] <= model.latitude.max())
    in_model_alt_bounds = (model.altitude.min() <= obs[:, data.ALTITUDE_IDX] <= model.altitude.max())
    in_model_time_bounds = (model.time.min() <= obs[:, data.TIME_IDX] <= model.time.max())

    obs = obs[ in_model_lon_bounds & in_model_lat_bounds & in_model_alt_bounds & in_model_time_bounds]

    # Keep only the subset of the model which is in the obs bounds
    # subsetting with .loc. Seems pretty fast and working
    model = model.loc[dict(lon = slice(obs.longitude.min(), obs.longitude.max()), lat=slice(obs.latitude.min(), obs.latitude.max()), alt = slice(obs.altitude.min(), obs.altitude.max()))]

    # breakpoint()
    # https://stackoverflow.com/questions/57781130/xarray-select-index-dataarray-from-the-time-labels-from-another-dataarray
    # Could do something like
    #model_new = model.where(model.alt.isin(obs.altitude), drop = True)


    ind_lon = xr.DataArray(obs.longitude, dims="linear_index")
    ind_lat = xr.DataArray(obs.latitude, dims="linear_index")
    ind_alt = xr.DataArray(obs.altitude, dims="linear_index")
    ind_time = xr.DataArray(obs.time_utc, dims="linear_index")

    # note model is now an xr.Dataset
    # use .sel to get the nearest model point corresponding to the observation points

    # LB: Before we get too far. question what is meant by "nearest". Want to impose restrictions on physical distance and temporal delta
    # LB: Need to use `tolerance` argument, but may need to do this sequentially
    model = model.sel(lon = ind_lon, lat = ind_lat, alt = ind_alt, time = ind_time, method = "nearest")

    # model = model.sel(lon=ind_lon, method = "nearest", tolerance = 0.5)
    # model = model.sel(lat=ind_lat, method = "nearest", tolerance = 0.5)
    # # https://github.com/pydata/xarray/issues/4995
    # model = model.sel(alt=ind_alt, method = "nearest", tolerance = 1000.) # setting this low causing issues
    # breakpoint()
    # model = model.sel(time=ind_time, method = "nearest", tolerance = np.timedelta64(1,ts_type))


    #model = model.sel(lon=ind_lon, lat=ind_lat, alt=ind_alt, time=ind_time, method="nearest")
    df = model.to_pandas()[MODEL_OUTPUT_NAME] # from the model get the output we want and put it in a dataframe
    # add a new column to the obs df with the colocated model values as a new column
    return pd.concat((obs,df), axis= "columns")
