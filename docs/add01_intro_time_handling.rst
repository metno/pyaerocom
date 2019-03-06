
Handling of time in pyaerocom
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**NOTE**: the topics of this notebook are not necessarily required for
using *pyaerocom*. It The
`GriddedData <http://aerocom.met.no/pya/api.html#module-pya.griddeddata>`__
class of *pyaerocom* was introduced in a previous tutorial.

Here, we illustrate how *pyaerocom* handles time. In particular, how
*pyaerocom* performs the conversion of CF conform numerical time stamps
with a defined unit (i.e. basedate and calendar, see e.g.
`here <http://cfconventions.org/Data/cf-conventions/cf-conventions-1.6/build/cf-conventions.html#time-coordinate>`__
for details) into datetime-like objects that can be interpreted by tools
such as `Pandas <https://pandas.pydata.org/>`__.

The easiest way to work with time stamps in model data is, to simply
work on the internal numerical indices, avoiding the necessity to
convert them into actual datetime objects. However, sometimes (e.g. if
we want to extract and analyse a time-series of global average Aerosol
optical densities), we wish to use third party libraries such as Pandas,
which require the timestamps to be datetime-like objects.

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

    Initating pyaerocom configuration
    Checking server configuration ...
    Checking access to: /lustre/storeA
    Access to lustre database: True
    Init data paths for lustre
    Expired time: 0.019 s


.. code:: ipython3

    data_ecmwf = pya.GriddedData(fpath_ecmwf, var_name="od550aer", name="ECMWF_OSUITE")
    data_aatsr = pya.GriddedData(fpath_aatsr, var_name="od550aer", name="AATSR")


.. parsed-literal::

    /home/jonasg/anaconda3/lib/python3.6/site-packages/iris/fileformats/_pyke_rules/compiled_krb/fc_rules_cf_fc.py:1932: UserWarning: Ignoring netCDF variable 'od550oa' invalid units '~'
      warnings.warn(msg)
    /home/jonasg/anaconda3/lib/python3.6/site-packages/iris/fileformats/_pyke_rules/compiled_krb/fc_rules_cf_fc.py:1932: UserWarning: Ignoring netCDF variable 'od550dust' invalid units '~'
      warnings.warn(msg)
    /home/jonasg/anaconda3/lib/python3.6/site-packages/iris/fileformats/_pyke_rules/compiled_krb/fc_rules_cf_fc.py:1932: UserWarning: Ignoring netCDF variable 'od550so4' invalid units '~'
      warnings.warn(msg)
    /home/jonasg/anaconda3/lib/python3.6/site-packages/iris/fileformats/_pyke_rules/compiled_krb/fc_rules_cf_fc.py:1932: UserWarning: Ignoring netCDF variable 'od550bc' invalid units '~'
      warnings.warn(msg)
    /home/jonasg/anaconda3/lib/python3.6/site-packages/iris/fileformats/_pyke_rules/compiled_krb/fc_rules_cf_fc.py:1932: UserWarning: Ignoring netCDF variable 'od550aer' invalid units '~'
      warnings.warn(msg)


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

    First time stamp ECMWF 2018-01-01 00:00:00 (data type: <class 'cftime._cftime.real_datetime'>)
    First time stamp AATSR 2008-01-01 00:00:00 (data type: <class 'cftime._cftime.DatetimeJulian'>)


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

    TypeError("Cannot convert input [2008-01-01 00:00:00] of type <class 'cftime._cftime.DatetimeJulian'> to Timestamp",)


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
that whenever ``cell`` is called, it performs a conversion of the
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

    [real_datetime(2018, 1, 1, 0, 0), real_datetime(2018, 1, 2, 0, 0)]
    
    [cftime.DatetimeJulian(2008, 1, 1, 0, 0, 0, 0, 0, 1), cftime.DatetimeJulian(2008, 1, 2, 0, 0, 0, 0, 1, 2)]


This worked, but however, is it fast?

.. code:: ipython3

    %%timeit 
    [t.point for t in times_ecmwf.cells()]


.. parsed-literal::

    89 ms ± 2.85 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


.. code:: ipython3

    %%timeit
    [t.point for t in times_aatsr.cells()]


.. parsed-literal::

    92.5 ms ± 3.9 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


The answer is: No, it is not fast, and furthermore, the latter datatype
will not be accepted by pandas as a valid datetime object. We can,
however, convert the datapoints to numpy datetime64 objects during the
conversion (if we want).

.. code:: ipython3

    %%timeit 
    [np.datetime64(t.point) for t in times_ecmwf.cells()]


.. parsed-literal::

    91.7 ms ± 3.24 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


.. code:: ipython3

    %%timeit
    [np.datetime64(t.point) for t in times_aatsr.cells()]


.. parsed-literal::

    88.6 ms ± 2.86 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


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

    4.52 ms ± 65.6 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


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
“gregorian”). THis function is included in **pyaerocom** and can be
accessed via:

.. code:: ipython3

    from pyaerocom.helpers import cftime_to_datetime64 as pya_tconversion
    help(pya_tconversion)


.. parsed-literal::

    Help on function cftime_to_datetime64 in module pyaerocom.helpers:
    
    cftime_to_datetime64(times, cfunit=None, calendar=None)
        Convert numerical timestamps with epoch to numpy datetime64
        
        This method was designed to enhance the performance of datetime conversions
        and is based on the corresponding information provided in the cftime 
        package (`see here <https://github.com/Unidata/cftime/blob/master/cftime/
        _cftime.pyx>`__). Particularly, this object does, what the :func:`num2date` 
        therein does, but faster, in case the time stamps are not defined on a non
        standard calendar.
        
        Parameters
        ----------
        times : :obj:`list` or :obj:`ndarray` or :obj:`iris.coords.DimCoord`
            array containing numerical time stamps (relative to basedate of 
            ``cfunit``). Can also be a single number.
        cfunit : :obj:`str` or :obj:`Unit`, optional
            CF unit string (e.g. day since 2018-01-01 00:00:00.00000000 UTC) or
            unit. Required if `times` is not an instance of 
            :class:`iris.coords.DimCoord`
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
    


.. code:: ipython3

    %%timeit
    pya_tconversion(times_ecmwf.points, times_ecmwf.units)


.. parsed-literal::

    248 µs ± 10.7 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


For the AATSR data, the method is slower, since here, the slower
``num2date`` method is used.

.. code:: ipython3

    %%timeit
    pya_tconversion(times_aatsr.points, times_aatsr.units)


.. parsed-literal::

    6.35 ms ± 62.4 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


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

    302 µs ± 9.87 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


.. code:: ipython3

    %%timeit
    data_aatsr.time_stamps()


.. parsed-literal::

    6.51 ms ± 84 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

