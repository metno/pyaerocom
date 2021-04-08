#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Variable categorisation groups

These are needed in some cases to infer, e.g. units associated with variable
names.

Note: the below definitions are far from complete
"""

emi_startswith = 'emi'
wetdep_startswith = 'wet'
drydep_startswith = 'dry'

# additional emission rate variables (that do not start with emi*)
emi_add_vars = []

# additional deposition rate variables (that do not start with wet* or dry*)
dep_add_vars = ['pr']

# additional rate variables (that are not emission or deposition rates)
rate_add_vars = []