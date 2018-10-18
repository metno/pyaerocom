
Reading of ungridded data - ReadUngridded data class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ungridded data in pyaerocom can be any data that is not stored in a
gridded standard format such as NetCDF or that would not make sense to
be imported / represented in a gridded format.

One example is the `AERONET <https://aeronet.gsfc.nasa.gov/>`__
database, which provides aerosol optical properties (such as the Aerosol
optical depth) which are measured at individual stations around the
globe. The sampled parameters and provided variables can vary from
station to station, and of course do the sample times.

Ungridded data in pyaerocom is organised *per observation network* and
the basic idea is, to read data from a whole network (or even more than
one) at once, and have it represented in one object.

Sticking to the
