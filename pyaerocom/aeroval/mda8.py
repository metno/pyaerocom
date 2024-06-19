import logging

import xarray as xr

from pyaerocom.colocation.colocated_data import ColocatedData

logger = logging.getLogger(__name__)


def calc_mda8(coldata: ColocatedData, /, invar, outvar):
    data = coldata.data
    ravg = data.rolling(time=8, min_periods=6).mean()

    daily_max = ravg.resample(time="1D").max()

    if isinstance(data, xr.DataArray):
        data = data.to_dataset(name=invar)

    data[outvar] = daily_max

    coldata.data = data.to_dataarray()

    return coldata
