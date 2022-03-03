"""
Variable categorisation groups

These are needed in some cases to infer, e.g. units associated with variable
names. Used in :class:`pyaerocom.variable.Variable` to identify certain groups.

Note
-----
The below definitions are far from complete
"""

#: start string of emission variables
emi_startswith = "emi"
#: start string of wet deposition variables
wetdep_startswith = "wet"
#: start string of dry deposition variables
drydep_startswith = "dry"
#: start string of total deposition variables
totdep_startswith = "dep"

#: additional emission rate variables (that do not start with emi*)
emi_add_vars = []

#: additional deposition rate variables (that do not start with wet* or dry*)
dep_add_vars = []
