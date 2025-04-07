from __future__ import annotations

from pyaerocom.aux_var_helpers import vmrx_to_concx
from pyaerocom.units.helpers import get_standard_unit
from pyaerocom.units.molecular_mass import get_molmass
from pyaerocom.stationdata import StationData


def vmr_to_ghost_stations(
    data: list[StationData], mconcvar: str, vmrvar: str
) -> list[StationData]:
    """
    Convert VMR data to mass concentration for list of GHOST StationData objects

    Note
    ----
    This is a private function used in :class:`ReadGhost` and is not supposed
    to be used directly.

    Parameters
    ----------
    data : list
        list of :class:`StationData` objects containing VMR data (e.g. vmrno2)
    mconcvar : str
        Name of mass concentration variable (e.g. concno2)
    vmrvar : str
        Name of VMR variable (e.g. vmrno2)

    Returns
    -------
    data : list
        list of modified :class:`StationData` objects that include computed
        mass concentrations in addition to VMR data.

    """
    for stat in data:
        vmrdata = stat[vmrvar]
        meta = stat["meta"]
        p_pascal = meta["network_provided_volume_standard_pressure"]
        T_kelvin = meta["network_provided_volume_standard_temperature"]
        mmol_var = get_molmass(vmrvar)
        unit_var = meta["var_info"][vmrvar]["units"]
        to_unit = get_standard_unit(mconcvar)
        conc = vmrx_to_concx(
            vmrdata,
            p_pascal=p_pascal,
            T_kelvin=T_kelvin,
            mmol_var=mmol_var,
            vmr_unit=unit_var,
            to_unit=to_unit,
        )
        stat[mconcvar] = conc
        vi = {}
        vi.update(meta["var_info"][vmrvar])
        vi["computed"] = True
        vi["units"] = to_unit
        meta["var_info"][mconcvar] = vi

    return data
