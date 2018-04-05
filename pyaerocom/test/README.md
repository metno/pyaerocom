## pyaerocom test-suite

All test routines of the pyaerocom package are supposed to be developed here. Suggestion is to use :mod:`pytest` as test interface. All modules in this folder (i.e. *.py*  files) should contain ***test*** in the filename, as well as all test methods and classes.

Run the testsuite from the toplevel directory of the `pyaerocom` package (i.e. where the setup.py file lies) using:

	python -m pytest

For details see [here](https://docs.pytest.org/en/latest/usage.html).
