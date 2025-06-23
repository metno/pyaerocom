"""
Config file for AeroCom PhaseIII test project
"""
# Imported and updated from: https://gitlab.met.no/aeroval/config/-/blob/master/eval_py/gridded_io_aux.py

from pyaerocom.io.aux_read_cubes import (
    add_cubes,
    subtract_cubes,
    divide_cubes,
    multiply_cubes,
    compute_angstrom_coeff_cubes,
    mmr_to_vmr_cube,
    conc_from_vmr_STP,
)
from pyaerocom.units.molecular_mass import MolecularMass


M_N = float(MolecularMass("N"))
M_O = float(MolecularMass("O"))
M_H = float(MolecularMass("H"))


def calc_concnh3(concnh3):  # pragma: no cover
    in_ts_type = concnh3.ts_type

    concNnh3 = concnh3 * (M_N / (M_N + M_H * 3))
    concNnh3.units = "ug N m-3"

    concNnh3.attributes["ts_type"] = in_ts_type

    return concNnh3


def calc_concnh4(concnh4):  # pragma: no cover
    if concnh4.units == "ug m-3" or concnh4.units == "ug/m**3":
        concnh4.units = "ug/m3"
    assert concnh4.units == "ug/m3"

    in_ts_type = concnh4.ts_type
    concnh4 = concnh4.cube
    concnh4 *= M_N / (M_N + M_H * 4)
    concnh4.units = "ug N m-3"

    concnh4.attributes["ts_type"] = in_ts_type

    return concnh4


def calc_conchno3(vmrhno3):  # pragma: no cover
    if vmrhno3.units == "1e-9":
        vmrhno3.units == "ppb"
    assert vmrhno3.units == "ppb"

    in_ts_type = vmrhno3.ts_type
    conchno3 = conc_from_vmr_STP(vmrhno3.cube)
    conchno3.units = "ug/m3"
    conchno3 *= M_N / (M_H + M_N + M_O * 3)
    conchno3.attributes["ts_type"] = in_ts_type
    conchno3.units = "ug N m-3"

    return conchno3


def calc_fine_concno310(concno3f):  # pragma: no cover
    return calc_concno310(concno3f=concno3f, concno3c=None)


def calc_concno310(concno3c, concno3f):  # pragma: no cover
    if concno3c is not None:
        if concno3c.units == "ug m-3" or concno3c.units == "ug/m**3":
            concno3c.units = "ug/m3"
        assert concno3c.units == "ug/m3"
    assert concno3f.units == "ug/m3"

    in_ts_type = concno3f.ts_type
    if concno3c is not None:
        concno310 = add_cubes(concno3f.cube, concno3c.cube)
    else:
        concno310 = concno3f.cube

    concno310 *= M_N / (M_N + M_O * 3)
    concno310.attributes["ts_type"] = in_ts_type
    concno310.units = "ug N m-3"
    return concno310


def calc_concno325(concno3f):  # pragma: no cover
    assert concno3f.units == "ug/m3"
    in_ts_type = concno3f.ts_type
    concno325 = concno3f.cube
    concno325 *= M_N / (M_N + M_O * 3)

    concno325.attributes["ts_type"] = in_ts_type
    concno325.units = "ug N m-3"
    return concno325


def calc_fine_conctno3(concno3f, vmrhno3):  # pragma: no cover
    return calc_conctno3(concno3f=concno3f, concno3c=None, vmrhno3=vmrhno3)


def calc_conctno3(concno3c, concno3f, vmrhno3):  # pragma: no cover
    if concno3c is not None:
        if concno3c.units == "ug m-3" or concno3c.units == "ug/m**3":
            concno3c.units = "ug/m3"
        assert concno3c.units == "ug/m3"

    if vmrhno3.units == "1e-9":
        vmrhno3.units == "ppb"
    assert concno3f.units == "ug/m3"
    assert vmrhno3.units == "ppb"

    in_ts_type = vmrhno3.ts_type
    if concno3c is not None:
        concno3 = add_cubes(concno3f.cube, concno3c.cube)
    else:
        concno3 = concno3f.cube

    conchno3 = conc_from_vmr_STP(vmrhno3.cube)
    conchno3.units = "ug/m3"
    concno3 *= M_N / (M_N + M_O * 3)
    conchno3 *= M_N / (M_H + M_N + M_O * 3)
    conctno3 = add_cubes(concno3, conchno3)
    conctno3.attributes["ts_type"] = in_ts_type
    conctno3.units = "ug N m-3"
    return conctno3


def calc_conctnh(concnh4, vmrnh3):  # pragma: no cover
    if concnh4.units == "ug m-3" or concnh4.units == "ug/m**3":
        concnh4.units = "ug/m3"
    if vmrnh3.units == "1e-9":
        vmrnh3.units = "ppb"
    assert concnh4.units == "ug/m3"
    assert vmrnh3.units == "ppb"

    concnh3 = conc_from_vmr_STP(vmrnh3.cube)
    concnh3.units = "ug/m3"
    concnh3 *= M_N / (M_N + M_H * 3)
    in_ts_type = concnh4.ts_type
    concnh4 = concnh4.cube
    concnh4 *= M_N / (M_N + M_H * 4)
    conctnh = add_cubes(concnh3, concnh4)
    conctnh.attributes["ts_type"] = in_ts_type
    conctnh.units = "ug N m-3"
    return conctnh


def calc_aod_from_species_contributions(*gridded_objects):  # pragma: no cover
    data = gridded_objects[0].cube

    assert str(data.units) == "1"

    for obj in gridded_objects[1:]:
        assert str(obj.units) == "1"
        data = add_cubes(data, obj.cube)

    return data


FUNS = {
    "add_cubes": add_cubes,
    "subtract_cubes": subtract_cubes,
    "divide_cubes": divide_cubes,
    "multiply_cubes": multiply_cubes,
    "calc_ae": compute_angstrom_coeff_cubes,
    "calc_conctno3": calc_conctno3,
    "calc_fine_conctno3": calc_fine_conctno3,
    "calc_conctnh": calc_conctnh,
    "calc_concnh3": calc_concnh3,
    "calc_concnh4": calc_concnh4,
    "calc_conchno3": calc_conchno3,
    "calc_concno310": calc_concno310,
    "calc_fine_concno310": calc_fine_concno310,
    "calc_concno325": calc_concno325,
    "calc_aod_from_species_contributions": calc_aod_from_species_contributions,
    "mmr_to_vmr": mmr_to_vmr_cube,
}
