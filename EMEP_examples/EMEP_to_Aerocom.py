import pyaerocom as pya
from pyaerocom.io.read_emep import ReadEMEP
from pyaerocom.variable import get_emep_variables
from pyaerocom.io.readgridded import ReadGridded
from EMEP_to_Aerocom import *
import glob
import os
import xarray as xr

# Mapping of ts_type to EMEP filenames
ts_type_EMEP_filename = {'daily':'Base_day.nc', 'monthly':'Base_month.nc', 'yearly': 'Base_fullrun.nc'}

# Map of EMEP variable prefix to vertical type used for storing nc files
map_prefix_aero = {'AOD': 'Column' ,'AAOD' : 'Column', 'Abs_coeff': 'ModelLevel',
                   'AbsCoeff': 'ModelLevel',
                   'DDEP': 'Surface', 'Emis': 'Surface',
                   'COLUMN': 'Column', 'D3': 'ModelLevel',
                   'SURF': 'Surface', 'WDEP': 'Surface',
                  'z3d': 'Surface',
                  'Z': 'Surface'}


def EMEP_to_aerocom(in_folder, out_folder, ts_type, year, data_id, filename=None):
    """
    Converts all (known) variables from in_folder/filename to Aerocom format in out_folder.
    """
    
    if filename == None:
        try:
            filename = ts_type_EMEP_filename[ts_type]
        except KeyError as e:
            print('ts_type not recognized')
            #exit
    
    filepath = os.path.join(in_folder, filename)

    
    if not (os.path.isdir(in_folder) and os.path.isdir(out_folder)):
        raise FileNotFoundError('in_folder or out_folder is not a folder')
        # exit ?
    if not os.path.isfile(filepath):
        raise FileNotFoundError('File to be converted not found: {}'.format(filepath))
        # exit?
        
    reader = ReadEMEP(filepath, data_id=data_id)
    for key, var in get_emep_variables().items():
#         print('Converting {} / {}'.format(key, var))
        # Load data
        try:
            data = reader.read_var(key, ts_type=ts_type)
        except KeyError as e:
            print('{} not found in {} EMEP files\n'.format(key, ts_type))
            continue
        except ValueError as e:
            print(repr(e))
            continue
        data.change_base_year(year) # Change year to match emission year
        data.time.long_name='Time'
        data.time.var_name='time'

        # Infer vertical coordinate from variable naming
        type_emep = (var.split('_')[0])
        vert_code = map_prefix_aero[type_emep]
        data.to_netcdf(out_folder, vert_code=vert_code);

#     # TODO: Also convert auxiliary variable
#     for var in reader.AUX_REQUIRES:
#         data = reader.read_var(var, ts_type=ts_type)
#         data.change_base_year(year)
#         type_emep = (var.split('_')[0])
#         data.to_netcdf(out_folder, vert_code=vert_code);
        
def compare(control, convert, time=0):
    """
    Checks that the values for a given time index in control and convert are the same.
    Control and convert are xarray DataArrays
    
    Returns True if there are no differences.
    """
    
    result = []
    diff = control.isel(time=time).values - convert.isel(time=time)
    mintest = float(diff.min()) == 0
    maxtest = float(diff.max()) == 0
    result = (mintest and maxtest)
    return result

def run_compare(ts_type, year, alltimes=False):
    # Loop through all variables and compare
    # If alltimes = True -> check all timesteps
    results = {}
    ts_type='monthly'
    for variable in var_in_both:
        control = control_reader.read_var(variable, start=year, ts_type=ts_type).to_xarray().load()
        convert = convert_reader.read_var(variable, start=year, ts_type=ts_type).to_xarray().load()
        if variable[0:3] in ['dry', 'wet']: # Dry and wet deposition have been converted to kg m-2 s-1
            # Will fail because units has been changed
            continue
    #         result = compare(control, convert)
        else:
            if alltimes:
                for i in range(0, len(control.time)):
                    result = compare(control, convert, time=i)
                    results['{}_time_{}'.format(variable, i)] = result
            else:
                results[variable] = compare(control, convert)
    return results