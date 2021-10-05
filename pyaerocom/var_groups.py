"""
Variable categorisation groups

These are needed in some cases to infer, e.g. units associated with variable
names.

Note: the below definitions are far from complete
"""

emi_startswith = 'emi'
wetdep_startswith = 'wet'
drydep_startswith = 'dry'
totdep_startswith = 'dep'

# additional emission rate variables (that do not start with emi*)
emi_add_vars = []

# additional deposition rate variables (that do not start with wet* or dry*)
dep_add_vars = []