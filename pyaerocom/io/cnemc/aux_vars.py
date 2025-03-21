import xarray as xr
from geonum import atmosphere as atm

from pyaerocom.aux_var_helpers import concx_to_vmrx
from pyaerocom.units.molecular_mass import get_molmass


def conc_to_vmr(da: xr.DataArray, *, vmr: str, units: str = "ppb") -> xr.DataArray:
    data = concx_to_vmrx(
        da.values,
        p_pascal=atm.p0,  # standard atmosphere pressure
        T_kelvin=atm.T0_STD,  # standard atmosphere temperature
        mmol_var=get_molmass(da.name),
        mmol_air=get_molmass("air_dry"),
        conc_unit=da.units,
        to_unit=units,
    )
    return xr.DataArray(data, da.coords, da.dims, name=vmr, attrs={"units": units})


def vmro3_from_ds(ds: xr.Dataset) -> xr.DataArray:
    return conc_to_vmr(ds["conco3"], vmr="vmro3")


def vmro3max_from_ds(ds: xr.Dataset) -> xr.DataArray:
    return conc_to_vmr(ds["conco3"], vmr="vmro3max")


def vmrno2_from_ds(ds: xr.Dataset) -> xr.DataArray:
    return conc_to_vmr(ds["concno2"], vmr="vmrno2")
