from .molecular_mass import MolecularMass

# Definitions of various custom constants and conversion factors.

M_H = MolecularMass("H")
M_O = MolecularMass("O")
M_N = MolecularMass("N")
M_S = MolecularMass("S")

M_SO2 = MolecularMass("SO2")
M_SO4 = MolecularMass("SO4")
M_NO2 = MolecularMass("NO2")
M_NO3 = MolecularMass("NO3")

M_NH3 = MolecularMass("NH3")
M_NH4 = MolecularMass("NH4")

HA_TO_SQM = 10_000  # m^2 ha^1

SECONDS_IN_DAY = 24 * 60 * 60
