from pyaerocom.access_testdata import AccessTestData

# class that provides / ensures access to testdataset
tda = AccessTestData()

# checks if testdata-minimal is available and if not, tries to download it
# automatically into ~/MyPyaerocom/testdata-minimal

assert tda.init(), "cound not find minimal test data"
TESTDATADIR = AccessTestData().testdatadir
