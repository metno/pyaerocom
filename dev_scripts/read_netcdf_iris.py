"""Test script to read and plot netCDF files using Iris
"""
import iris
from pandas import Timestamp
PATH = ('/lustre/storeA/project/aerocom/aerocom1/ECMWF_OSUITE_NRT_test/'
        'renamed/aerocom.ECMWF_OSUITE_NRT_test.daily.od550aer.2018.nc')      

if __name__=="__main__":
    # this is a CubeList
    cubes = iris.load(PATH)

    # take one of the cubes
    cube = cubes[1]
    print(cube)
    
    
    #Coordinates
    time = cube.coord("time")
    lons = cube.coord("longitude")
    lats = cube.coord("latitude")
    
    lons.guess_bounds()
    lats.guess_bounds()
    
    lonlat_constraint = iris.Constraint(longitude=lambda cell: 15 < cell < 25,
                             latitude=lambda cell: 35 < cell < 45)
    # crop cube in lon / lat
    do_op1 = 1
    if do_op1:
        #http://scitools.org.uk/iris/docs/latest/userguide/subsetting_a_cube.html
        cube_crop = cube.extract(lonlat_constraint)
    
    else:
        #this one handles longitudes regardless whether they are defined
        #0 <= lon <= 360 or -180 <= lon <= 180
        cube_crop = cube.intersection(longitude=(15, 25),
                                      latitude=(35, 45))
                
    # We only have the first 83 days of 2018 in the dataset
    start = Timestamp("2018-1-15")
    stop = Timestamp("2018-2-20")
    
    t_lower = iris.time.PartialDateTime(year=start.year,
                                   month=start.month,
                                   day=start.day)
    t_upper = iris.time.PartialDateTime(year=stop.year,
                                   month=stop.month,
                                   day=stop.day)
    
    time_constraint = iris.Constraint(time=lambda cell: t_lower <= cell <= t_upper)
    crop_time_opt1 = 0
    
    if crop_time_opt1:
        cube_crop = cube_crop[:82]
    else:
        # crop in time using actual timestamp
        cube_crop = cube_crop.extract(time_constraint)
        
    first_day = cube_crop[0]
    
    print(first_day.data.shape)
    
    weights = iris.analysis.cartography.area_weights(cube_crop)
    
    import numpy as np
    avg_val = np.average(cube_crop.data, weights=weights, axis=(1,2))
    
    # the actual data can be accessed using the "data" attribute of a Cube
    # this loads the data
    dat = cube_crop.data
    
    
    ### Now try to apply constraints already on load and use method
    # load_cube from iris rather then load
    var_name = cube_crop.var_name
    var_constraint = iris.Constraint(cube_func=lambda c: c.var_name==var_name)
    
    constraint = var_constraint & time_constraint & lonlat_constraint
    cube = iris.load_cube(PATH, constraint)
    
    