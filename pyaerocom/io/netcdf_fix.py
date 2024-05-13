import logging

import netCDF4

# avoid a broken autoadjusting chunk-cache in netcdf by setting a static cache
# see https://github.com/Unidata/netcdf-c/issues/2913
nc_cache = netCDF4.get_chunk_cache()
netCDF4.set_chunk_cache(2 * nc_cache[0], nc_cache[1], nc_cache[2])
logging.getLogger(__name__).debug("netcdf-chunk-cache fix applied")
