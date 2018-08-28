
Handling of time in pyaerocom
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The
`GriddedData <http://aerocom.met.no/pya/api.html#module-pya.griddeddata>`__
class of *pyaerocom* was introduced in the previous tutorial.

Here, we want to illustrate one particular feature of *pya*, namely the
conversion of CF conform numerical time stamps with a defined unit
(i.e. basedate and calendar, see e.g.
`here <http://cfconventions.org/Data/cf-conventions/cf-conventions-1.6/build/cf-conventions.html#time-coordinate>`__
for details) into datetime-like objects that can be interpreted by tools
such as `Pandas <https://pandas.pydata.org/>`__. The easiest way to work
with time stamps in model data is, to simply work on the internal
numerical indices, avoiding the necessity to convert them into actual
datetime objects. However, sometimes (e.g. if we want to extract and
analyse a time-series of global average Aerosol optical densities), we
wish to use third party libraries such as Pandas, which require the
timestamps to be datetime-like objects.

This notebook illustrates how time is handled in the iris module,
particularly in the
`Cube <http://scitools.org.uk/iris/docs/v1.9.0/html/iris/iris/cube.html#iris.cube.Cube>`__
class, which is the basic data representation object in the *pya*
``GriddedData`` class. In particular, it emphazises some peculiarities
that can lead to complications and finally shows, how *pya* circumvents
these issues. We shall see, that this does not only reduce the risk of
conversion Errors, but even results in a quite significant performance
boost when converting from numerical CF timestamps to
``numpy.datetime64`` time stamps.

Load and some example data
^^^^^^^^^^^^^^^^^^^^^^^^^^

Get and load test data file using the new pya interface (the underlying
datatype of ``GriddedData`` is ``iris.cube.Cube``.

.. code:: ipython3

    import pyaerocom as pya
    files = pya.io.testfiles.get()
    
    fpath_ecmwf = files['models']['ecmwf_osuite']
    fpath_aatsr = files['models']['aatsr_su_v4.3']


.. parsed-literal::

    2018-08-28 14:18:18,376:INFO:
    Reading aliases ini file: /home/jonasg/github/cloned/pyaerocom/pyaerocom/data/aliases.ini
    2018-08-28 14:18:19,168:WARNING:
    geopy library is not available. Aeolus data read not enabled


.. code:: ipython3

    data_ecmwf = pya.GriddedData(fpath_ecmwf, var_name="od550aer", name="ECMWF_OSUITE")
    data_aatsr = pya.GriddedData(fpath_aatsr, var_name="od550aer", name="AATSR")


.. parsed-literal::

    /home/jonasg/anaconda3/lib/python3.6/site-packages/iris/fileformats/_pyke_rules/compiled_krb/fc_rules_cf_fc.py:1808: UserWarning: Ignoring netCDF variable 'od550so4' invalid units '~'
      warnings.warn(msg)
    /home/jonasg/anaconda3/lib/python3.6/site-packages/iris/fileformats/_pyke_rules/compiled_krb/fc_rules_cf_fc.py:1808: UserWarning: Ignoring netCDF variable 'od550oa' invalid units '~'
      warnings.warn(msg)
    /home/jonasg/anaconda3/lib/python3.6/site-packages/iris/fileformats/_pyke_rules/compiled_krb/fc_rules_cf_fc.py:1808: UserWarning: Ignoring netCDF variable 'od550bc' invalid units '~'
      warnings.warn(msg)
    /home/jonasg/anaconda3/lib/python3.6/site-packages/iris/fileformats/_pyke_rules/compiled_krb/fc_rules_cf_fc.py:1808: UserWarning: Ignoring netCDF variable 'od550dust' invalid units '~'
      warnings.warn(msg)
    /home/jonasg/anaconda3/lib/python3.6/site-packages/iris/fileformats/_pyke_rules/compiled_krb/fc_rules_cf_fc.py:1808: UserWarning: Ignoring netCDF variable 'od550aer' invalid units '~'
      warnings.warn(msg)
    2018-08-28 14:18:21,244:INFO:
    Rolling longitudes to -180 -> 180 definition


Note that, if the longitudes are defined on a 0 -> 360 degree grid, they
are automatically converted to -180 -> 180 (the case of the ECMWF data).

Digging into the time representation of the iris Cube datatype
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``GriddedData`` class is based on the ``iris.Cube`` object, which
can be accessed via the ``grid`` attribute. In the following, some
features of the ``Cube`` class are introduced.

.. code:: ipython3

    cube_ecmwf = data_ecmwf.grid
    cube_aatsr = data_aatsr.grid

Peculiarities of time handling when using the ``Cube`` interface
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Starting with how time is handled. The time is represented as numerical
value relative to a basic date and frequency unit and in the optimum
case, also the specification of a calendar, according to the `NetCDF CF
conventions <http://cfconventions.org/Data/cf-conventions/cf-conventions-1.6/build/cf-conventions.html#time-coordinate>`__.

.. code:: ipython3

    times_ecmwf = cube_ecmwf.coord("time")
    print("ECMWF\nFirst point:%s\nTime unit: %s\nCalendar: %s\n" %(times_ecmwf.points[0],
                                                                   times_ecmwf.units.name, 
                                                                   times_ecmwf.units.calendar))
    times_aatsr= cube_aatsr.coord("time")
    print("AATSR\nFirst point:%s\nTime unit: %s\nCalendar: %s\n" %(times_aatsr.points[0], 
                                                                 times_aatsr.units.name, 
                                                                 times_aatsr.units.calendar))


.. parsed-literal::

    ECMWF
    First point:0.0
    Time unit: day since 2018-01-01 00:00:00.00000000 UTC
    Calendar: gregorian
    
    AATSR
    First point:0.0
    Time unit: day since 2008-01-01 00:00:00.00000000 UTC
    Calendar: julian
    


Note that the AATSR data is defined using a Julian calendar. The actual
time objects are instances of the ``DimCoord`` class of the iris
package.

.. code:: ipython3

    print(type(times_ecmwf), type(times_aatsr))


.. parsed-literal::

    <class 'iris.coords.DimCoord'> <class 'iris.coords.DimCoord'>


Now, if we want to convert these numerically represented time stamps
into datetime-like objects that, for instance, the ``pandas`` library
understands, we have several options. The first one, which is the most
obvious one, is using the provided iris interface which does the
conversion for us, that is, using the ``cell(index)`` method (with the
corresponding ``index``) of the ``DimCoord`` class in combination with
the ``cells()`` iterator method. However, as we shall see below, this is
not only the slowest solution but it is also prone to errors in case the
calendar is not standard (e.g. Julian).

.. code:: ipython3

    t0_ecmwf = times_ecmwf.cell(0).point
    t0_aatsr = times_aatsr.cell(0).point
    print("First time stamp ECMWF %s (data type: %s)" %(t0_ecmwf, type(t0_ecmwf)))
    print("First time stamp AATSR %s (data type: %s)" %(t0_aatsr, type(t0_aatsr)))


.. parsed-literal::

    First time stamp ECMWF 2018-01-01 00:00:00 (data type: <class 'datetime.datetime'>)
    First time stamp AATSR 2008-01-01 00:00:00 (data type: <class 'netcdftime._netcdftime.DatetimeJulian'>)


As you can see, the ``cell`` method returns different datatypes,
dependent on the CF unit convention, that is, a standard Python
``datetime.datetime`` object, if the calendar is Gregorian, and a
``netcdftime._netcdftime.DatetimeJulian`` object in case of a Julian
calendar. Problem here is, that the former is understood by pandas,
while the latter is not.

.. code:: ipython3

    import pandas
    
    t0_ecmwf_pandas = pandas.Timestamp(t0_ecmwf)
    try:
        t0_aatsr_pandas = pandas.Timestamp(t0_aatsr)
    except TypeError as e:
        print(repr(e))


.. parsed-literal::

    TypeError("Cannot convert input [2008-01-01 00:00:00] of type <class 'netcdftime._netcdftime.DatetimeJulian'> to Timestamp",)


Nontheless, numpy is easier in that sense, since it understands both
datatypes.

.. code:: ipython3

    import numpy as np
    
    t0_ecmwf_np = np.datetime64(t0_ecmwf)
    t0_aatsr_np = np.datetime64(t0_aatsr)
    print(t0_ecmwf_np, t0_aatsr_np)


.. parsed-literal::

    2018-01-01T00:00:00.000000 2008-01-01T00:00:00.000000


Fair enough, but however, in the end we want to ensure to have a
conversion method ready that handles any calendar, and that is
considerably fast. We just saw, that ``datetime64`` works for both
datetime formats that we get when calling the ``cell`` method of the
``DimCoord`` object that holds the time stamps. However, keep in mind,
that whenever ``call`` is called, it performs a conversion of the
numeric value into either ``datetime.datetime`` or, for non-standard
calendars, into a datetime object from the
`cftime <https://github.com/Unidata/cftime>`__ package. So, either way,
when using the ``cell`` method we have to iterate over all indices to
convert the numerical values into datetime-like objects. The latter may
be done using the ``cells()`` iterator of the ``DimCoord`` class.

.. code:: ipython3

    times_ecmwf_conv = [t.point for t in times_ecmwf.cells()]
    times_aatsr_conv = [t.point for t in times_aatsr.cells()]
    #display first two
    print("%s\n\n%s" %(times_ecmwf_conv[:2],times_aatsr_conv[:2]))


.. parsed-literal::

    [datetime.datetime(2018, 1, 1, 0, 0), datetime.datetime(2018, 1, 2, 0, 0)]
    
    [netcdftime._netcdftime.DatetimeJulian(2008, 1, 1, 0, 0, 0, 0, -1, 1), netcdftime._netcdftime.DatetimeJulian(2008, 1, 2, 0, 0, 0, 0, -1, 1)]


This worked, but however, is it fast?

.. code:: ipython3

    %%timeit 
    [t.point for t in times_ecmwf.cells()]


.. parsed-literal::

    181 ms ± 39.9 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


.. code:: ipython3

    %%timeit
    [t.point for t in times_aatsr.cells()]


.. parsed-literal::

    108 ms ± 4 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


The answer is: No, it is not fast, and furthermore, the latter datatype
will not be accepted by pandas as a valid datetime object. We can,
however, convert the datapoints to numpy datetime64 objects during the
conversion (if we want).

.. code:: ipython3

    %%timeit 
    [np.datetime64(t.point) for t in times_ecmwf.cells()]


.. parsed-literal::

    126 ms ± 3.66 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


.. code:: ipython3

    %%timeit
    [np.datetime64(t.point) for t in times_aatsr.cells()]


.. parsed-literal::

    128 ms ± 12.9 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


That looks okay, since it does not lead to a notable decrease in the
performance and ensures, that pandas will understand the datatype.
However, about 100ms for conversion of 365 dates is rather slow.

Other options to convert timestamps
'''''''''''''''''''''''''''''''''''

Above we saw how we can convert the numerical timestamps into an array
of numpy ``datetime64`` objects (which is what we want in the end). As
we shall see below, the conversion can be significantly accelarated if
we do not use the iris interface provided by the ``cell(index)`` method
and the ``cells()`` iterator, but rather directly use the underlying
``cftime`` library (that iris uses).

.. code:: ipython3

    %%timeit
    [np.datetime64(t) for t in times_ecmwf.units.num2date(times_ecmwf.points)]


.. parsed-literal::

    1.68 ms ± 12.8 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


This is quite an improvement. But if we dig a little deeper, we can
boost this even more, as we shall see in the following. Basically, what
it does is accessing the base date that is encrypted in the unit, i.e.

.. code:: ipython3

    print(times_ecmwf.units.name)


.. parsed-literal::

    day since 2018-01-01 00:00:00.00000000 UTC


and based on this base date, and the encrypted temporal resolution (here
*day*) uses the `pure numpy datetime
functionality <https://docs.scipy.org/doc/numpy-1.14.0/reference/arrays.datetime.html>`__
to convert the stuff. For this, we have to test if the first sub string
(here *day*) is valid according to the CF standard, which we do using
some features from the ``netCDF4`` package and by defining a function,
that translates the numerical timestamps into ``datetime64`` objects
based on the information encoded in the units string(e.g. *day since
2018-01-01 00:00:00.00000000 UTC*) and the corresponding calendar (e.g.
“gregorian”).

.. code:: ipython3

    from cf_units import Unit
    from datetime import MINYEAR, datetime
    from numpy import asarray, datetime64
    from netCDF4 import (microsec_units, millisec_units, sec_units, min_units,
                        hr_units, day_units)
    from netCDF4._netCDF4 import _dateparse
    # Start of the gregorian calendar
    # adapted from here: https://github.com/Unidata/cftime/blob/master/cftime/_cftime.pyx   
    GREGORIAN_BASE = datetime(1582, 10, 15)
    
    def cftime_to_datetime64(timesnum, cfunit, calendar=None):
        """Convert numerical timestamps with epoch to numpy datetime64
        
        This method was designed to enhance the performance of datetime conversions
        and is based on the corresponding information provided in the cftime 
        package (`see here <https://github.com/Unidata/cftime/blob/master/cftime/
        _cftime.pyx>`__). Particularly, this object does, what the :func:`num2date` 
        therein does, but faster, in case the time stamps are not defined on a non
        standard calendar.
        
        Parameters
        ----------
        timesnum : :obj:`list` or :obj:`ndarray`
            array containing numerical time stamps (relative to basedate of 
            ``cfunit``). Can also be a single number.
        cfunit : :obj:`str` or :obj:`Unit`
            CF unit string (e.g. day since 2018-01-01 00:00:00.00000000 UTC) or
            unit
        calendar : :obj:`str`, optional
            string specifying calendar (only required if ``cfunit`` is of type
            ``str``).
            
        Returns
        -------
        ndarray
            numpy array containing timestamps as datetime64 objects
            
        Raises
        ------
        ValueError
            if cfunit is ``str`` and calendar is not provided or invalid, or if 
            the cfunit string is invalid
            
        Example
        -------
        
        >>> cfunit_str = 'day since 2018-01-01 00:00:00.00000000 UTC'
        >>> cftime_to_datetime64(10, cfunit_str, "gregorian")
        array(['2018-01-11T00:00:00.000000'], dtype='datetime64[us]')
        """
        try:
            len(timesnum)
        except:
            timesnum = [timesnum]
        if isinstance(cfunit, str):
            if calendar is None:
                raise ValueError("Require specification of calendar for "
                                 "conversion into datetime64 objects")
            cfunit = Unit(cfunit, calendar) #raises Error if calendar is invalid
        if not isinstance(cfunit, Unit):
            raise ValueError("Please provide cfunit either as instance of class "
                             "cf_units.Unit or as a string")
        cfu_str, calendar = cfunit.name, cfunit.calendar
        basedate = _dateparse(cfu_str)
        cfu_str = cfunit.name
        basedate = _dateparse(cfu_str)  
        if ((calendar == 'proleptic_gregorian' and basedate.year >= MINYEAR) or 
            (calendar in ['gregorian','standard'] and basedate > GREGORIAN_BASE)):
            cfu_str = cfunit.name
            res = cfu_str.split()[0].lower()
            if res in microsec_units:
                tstr = "us"
            elif res in millisec_units:
                tstr = "ms"
            elif res in sec_units:
                tstr = "s"
            elif res in min_units:
                tstr = "m"
            elif res in hr_units:
                tstr = "h"
            elif res in day_units:
                tstr = "D"
            else:
                raise ValueError('unsupported time units')
            
            basedate = datetime64(basedate)
            return basedate + asarray(timesnum, dtype="timedelta64[%s]" %tstr)
        else:
            return asarray([datetime64(t) for t in cfunit.num2date(timesnum)])

Now let’s see how this one performs.

.. code:: ipython3

    %%timeit
    cftime_to_datetime64(times_ecmwf.points, times_ecmwf.units)


.. parsed-literal::

    56.7 µs ± 923 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)


How pya does it
^^^^^^^^^^^^^^^

Due to this significant increase in performance for standard calendars
(compared to the methods used in netCDF4), the above method was
implemented in the pya package (`see
here <aerocom.met.no/pya/api.html#pya.helpers.cftime_to_datetime64>`__).

.. code:: ipython3

    from pyaerocom.helpers import cftime_to_datetime64 as pya_tconversion

.. code:: ipython3

    %%timeit
    pya_tconversion(times_ecmwf.points, times_ecmwf.units)


.. parsed-literal::

    343 µs ± 9.93 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


For the AATSR data, the method is slower, since here, the slower
``num2date`` method is used.

.. code:: ipython3

    %%timeit
    pya_tconversion(times_aatsr.points, times_aatsr.units)


.. parsed-literal::

    2.15 ms ± 27.2 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


Now this is an improvement. Starting with around 100ms when using the
iris interface (i.e. iterating over ``cells`` of the ``DimCoord``), for
conversion of 365 time stamps, we ended up with the order of 10
microseconds. And at the same time the new method ensures that we have
them in a format that also pandas understands.

The method is also the standard conversion method in the
``GriddedData.time_stamps()`` method:

.. code:: ipython3

    %%timeit
    data_ecmwf.time_stamps()


.. parsed-literal::

    373 µs ± 6 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


.. code:: ipython3

    %%timeit
    data_aatsr.time_stamps()


.. parsed-literal::

    2.16 ms ± 68.4 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

