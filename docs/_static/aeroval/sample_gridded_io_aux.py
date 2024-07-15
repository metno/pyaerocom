"""
Sample gridded IO AUX file for computation of new model variables

This file can be registered in an AeroVal configuration script and the
callable functions in FUNS can be used to compute new model variables.

In this example only 1 function is registered that is already implemented in
pyaerocom.

The function is documented here:

https://pyaerocom.readthedocs.io/en/latest/api.html?highlight=compute_angstrom_coeff_cubes#pyaerocom.io.aux_read_cubes.compute_angstrom_coeff_cubes

Similar functions (that take iris.cube.Cube instances as input and return a
new "Cube" can be defined in this file directly and then registered with a
name (key) in FUNS and then used in configuration files to compute auxiliary
model variables.
"""

from pyaerocom.io.aux_read_cubes import compute_angstrom_coeff_cubes

FUNS = {
    "calc_ae": compute_angstrom_coeff_cubes,
}
