
EBAS file query and database browser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The previous tutorial showed how to read EBAS NASA Ames files and gave
insights into the strucure of these files. However, this did not include
the specification of an actual data request (for instance: get data from
all stations in the arcitc that contain measurements of the AOD between
2010 and 2016).

In this tutorial, we show, how such requests can be specified easily in
pyaerocom and how the database can be browsed for instance by variable
name, type of instrument, location or other relevant parameters.

The notebook is categorised as follows:

-  Defining a request
-  Retrieve all files for a request
-  Browse the database

Specifying a request
^^^^^^^^^^^^^^^^^^^^

Request parameters can be specified using the ``EbasSQLRequest`` class.
E.g.:

.. code:: ipython3

    import pyaerocom as pya
    
    request = pya.io.ebas_sqlite_query.EbasSQLRequest(variables=('aerosol_light_scattering_coefficient',
                                                                 'aerosol_light_backscattering_coefficient',
                                                                 'pressure'),
                                                      start_date="2010-01-01", 
                                                      stop_date="2011-01-01")
    print(request)


.. parsed-literal::

    variables: ('aerosol_light_scattering_coefficient', 'aerosol_light_backscattering_coefficient', 'pressure')
    start_date: 2010-01-01
    stop_date: 2011-01-01
    station_names: None
    matrices: None
    altitude_range: None
    lon_range: None
    lat_range: None
    instrument_types: None
    statistics: None
    


The request class is an extended dictionary and can thus be used like a
dictionary:

.. code:: ipython3

    request.update(instrument_types=("nephelometer"))
    print(request)


.. parsed-literal::

    variables: ('aerosol_light_scattering_coefficient', 'aerosol_light_backscattering_coefficient', 'pressure')
    start_date: 2010-01-01
    stop_date: 2011-01-01
    station_names: None
    matrices: None
    altitude_range: None
    lon_range: None
    lat_range: None
    instrument_types: nephelometer
    statistics: None
    


Execution of file request query
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that we have defined which files we would like to look into, we can
execute the query and retrieve all files that match our specifications.
This can be done with the ``EbasFileIndex`` class:

.. code:: ipython3

    db = pya.io.EbasFileIndex()
    files = db.execute_request(request)

.. code:: ipython3

    print("Total number of files found:{}\nRequest:\n{}".format(len(files), request))


.. parsed-literal::

    Total number of files found:56
    Request:
    variables: ('aerosol_light_scattering_coefficient', 'aerosol_light_backscattering_coefficient', 'pressure')
    start_date: 2010-01-01
    stop_date: 2011-01-01
    station_names: None
    matrices: None
    altitude_range: None
    lon_range: None
    lat_range: None
    instrument_types: nephelometer
    statistics: None
    


Browsing the database
^^^^^^^^^^^^^^^^^^^^^

The ``EbasFileIndex`` class provides some convenience function that
allow to browse meta information for a given request. These are
illustrated in the following:

For instance, we can check, what variables could actually be retrieved
in the request:

.. code:: ipython3

    print(db.contains_variables(request))


.. parsed-literal::

    ['pressure', 'aerosol_light_backscattering_coefficient', 'aerosol_light_scattering_coefficient']


Or what matrices the data contains:

.. code:: ipython3

    print(db.contains_matrices(request))


.. parsed-literal::

    ['instrument', 'aerosol', 'pm10', 'pm1']


Or which station coordinates (lon, lat) the dataset contains:

.. code:: ipython3

    print(db.contains_coordinates(request))


.. parsed-literal::

    [23.583333, -79.783839, -122.9576034546, -104.986864, -62.3415260315, 7.985, 11.0096197128, 12.93386, 10.97964, -8.266, -16.4994, -3.605, 2.35, 24.283333, 24.116111111, 2.95, 25.666667, 19.583333, -9.89944, 77.151389, 8.633333, 10.7, 126.17, 4.926389, 8.252, 11.888333, 2.533333, -65.618, 13.15, 120.87, -156.6114654541, -111.9841, -112.1288, -111.6832, -112.8, -109.3889, -155.5761566162, -86.148, -68.2608, -113.9958, -81.7, -103.1772, -97.5, -24.7999992371, -124.1510009766, -105.5457, -111.9692, -77.04, -109.7958, 18.48968]


Now, let's narrow this down:

.. code:: ipython3

    request.update(lat_range=(60, 90))
    print(db.contains_coordinates(request))


.. parsed-literal::

    [-62.3415260315, 24.283333, 24.116111111, 11.888333, -156.6114654541]


Print all station names:

.. code:: ipython3

    print(db.contains_station_names(request))


.. parsed-literal::

    ['Alert', 'Hyytiälä', 'Pallas (Sammaltunturi)', 'Zeppelin mountain (Ny-Ålesund)', 'Barrow']


Custom browsing
^^^^^^^^^^^^^^^

The previous browsing methods (e.g. ``contains_coordinates()``,
``contains_matrices``, ``contains_variables``) are all just simple
wrappers for the general query method ``make_query_str`` of the
``EbasSQLRequest`` class, that is then called by the ``EbasFileIndex``
class using the method ``execute_request``). Thus, if needed, you may
define your own request simply by using the provided interface. Here an
example using the request constraints specified above. Let's say we want
to retrieve a list of station names and their coordinates (lon, lat,
alt). This can be done by calling (we store the results in a list named
``station_info``):

.. code:: ipython3

    station_info = db.execute_request(request.make_query_str(what=("station_name", 
                                                                   "station_longitude",
                                                                   "station_latitude",
                                                                   "station_altitude")))
    
    for item in station_info:
        print(item)


.. parsed-literal::

    Alert
    Hyytiälä
    Pallas (Sammaltunturi)
    Zeppelin mountain (Ny-Ålesund)
    Barrow


You can see that the results for each station are stored in tuples in
the order of the request.

Read all files
^^^^^^^^^^^^^^

Let's update the file list and read all files.

.. code:: ipython3

    files = db.execute_request(request)
    print("Total number of files found: {}".format(len(files)))


.. parsed-literal::

    Total number of files found: 7


Let's read the files:

.. code:: ipython3

    import os
    data = []
    data_dir = os.path.join(pya.const.OBSCONFIG["EBASMC"]["PATH"], 'data')
    for f in files:
        data.append(pya.io.EbasNasaAmesFile(os.path.join(data_dir, f)))


.. parsed-literal::

    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/CA0420G.20100101000000.20150209103939.nephelometer...1y.1h.CA01L_TSI_3563_ALT.CA01L_scat_coef.lev2.nas
    Failed to read header row 6.
    2010 01 01 2015 02 09
    
    Error msg: IndexError('list index out of range',)
    Ignoring line no. 97: 0
    
    Ignoring line no. 98: 53
    
    REACHED DATA BLOCK
      0.000000   0.041667   973.59 0.392000   0.70 0.392000  301.32 0.392000  1.70400000 0.392000 99.99999999 0.460000  1.398528 0.392000 99.999999 0.460000  1.897151 0.392000 99.999999 0.460000  1.60500000 0.392000 99.99999999 0.460000  1.520000 0.392000 99.999999 0.460000  1.682868 0.392000 99.999999 0.460000  1.41100000 0.392000 99.99999999 0.460000  1.302849 0.392000 99.999999 0.460000  1.537151 0.392000 99.999999 0.460000  16.39900000 0.392000 999.99999999 0.460000  15.911377 0.392000 999.999999 0.460000  17.052887 0.392000 999.999999 0.460000  14.22400000 0.392000 999.99999999 0.460000  13.938566 0.392000 999.999999 0.460000  14.567189 0.392000 999.999999 0.460000  11.62600000 0.392000 999.99999999 0.460000  11.227075 0.392000 999.999999 0.460000  11.987189 0.392000 999.999999 0.460000 99999.99 0.460000 999.99 0.460000 9999.99 0.460000
    
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/CA0420G.20100101000000.20170516083933.nephelometer..pm10.1y.1h.CA01L_TSI_3563_ALT_pm10.CA01L_scat_coef.lev2.nas
    Failed to read header row 6.
    2010 01 01 2017 05 16
    
    Error msg: IndexError('list index out of range',)
    Ignoring line no. 35: 0
    
    Ignoring line no. 36: 54
    
    REACHED DATA BLOCK
      0.000000   0.041667   973.59   0.70  301.32  1.11600000  0.808528  1.317151  1.06500000  0.980000  1.142868 -0.96600000 -1.072868 -0.842849  14.61500000  14.062792  15.367189  11.70000000  11.392830  12.000057   6.56100000   6.185641   6.912868 0.392000
    
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/FI0050R.20100101000000.20121004000000.nephelometer..aerosol.1y.1h.FI03L_TSI3563.FI03L_Corrected_according_to_Anderson_and_Ogre..nas
    Failed to read header row 6.
    2010 01 01 2012 10 04
    
    Error msg: IndexError('list index out of range',)
    Ignoring line no. 34: 0
    
    Ignoring line no. 35: 33
    
    REACHED DATA BLOCK
      0.000000   0.041667   2.97   2.87   3.07   2.47   2.42   2.51   2.10   1.91   2.25   27.20   26.77   27.60   19.72   19.37   20.04   12.53   12.26   12.81   980.61  291.42 0.247000
    
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/FI0096G.20100412110000.20160705103730.nephelometer..pm10.9mo.1h.FI01L_TSI_3563_PAL_dry.FI01L_neph_control_lev1_0_0_1.lev2.nas
    Failed to read header row 6.
    2010 01 01 2016 07 05
    
    Error msg: IndexError('list index out of range',)
    Ignoring line no. 34: 0
    
    Ignoring line no. 35: 60
    
    REACHED DATA BLOCK
    101.458333 101.500000  939.0000000  299.4000000   1.196056   1.150314   1.241439   1.005160   0.974795   1.036001   1.022035   0.957909   1.084102   10.408017   10.305080   10.513390    7.616671    7.525326    7.708703   5.327212   5.288039    5.365250 0.390191
    
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/NO0042G.20100101000000.20150216111241.nephelometer..pm10.1y.1h.SE02L_TSI_3563_ZEP_dry.SE02L_scat_coef.lev2.nas
    Failed to read header row 6.
    2010 01 01 2015 02 16
    
    Error msg: IndexError('list index out of range',)
    Ignoring line no. 35: 0
    
    Ignoring line no. 36: 39
    
    REACHED DATA BLOCK
      0.000000   0.041667  955.500   6.800  300.000    -9.457    -9.629    -9.123   -6.280   -6.519   -6.110  -12.471  -12.627  -12.314     7.019     6.583     7.700     5.635     5.173     5.955    3.842    3.730    4.224 0.459000
    
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/US0008R.20100101000000.20150819091559.nephelometer...1y.1h.US06L_TSI_3563_BRW.US06L_scat_coef..nas
    Failed to read header row 6.
    2010 01 01 2015 08 19
    
    Error msg: IndexError('list index out of range',)
    Ignoring line no. 85: 0
    
    Ignoring line no. 86: 37
    
    REACHED DATA BLOCK
      0.000000   0.041667  1.25384600 0.000000  1.02888900 0.000000  0.459675 0.000000  0.375144 0.000000   2.001625 0.000000  1.751166 0.000000  0.87384610 0.000000  0.53888890 0.000000  0.659675 0.000000  0.392524 0.000000  1.040975 0.000000  0.712428 0.000000  0.68038460 0.000000  0.39518520 0.000000  0.539675 0.000000  0.251262 0.000000  0.880325 0.000000  0.596214 0.000000  9.8123080E+00 0.000000   5.71963000 0.000000   8.787725 0.000000   4.503978 0.000000   10.482100 0.000000   6.792332 0.000000   8.06538500 0.000000   4.37518500 0.000000   7.818700 0.000000   4.045144 0.000000   8.412600 0.000000   4.726214 0.000000   6.30153800 0.000000   2.75666700 0.000000   5.889675 0.000000   2.540000 0.000000   6.640975 0.000000   2.987476 0.000000
    
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/US0008R.20100101000000.20150819091559.nephelometer..pm10.1y.1h.US06L_TSI_3563_BRW.US06L_scat_coef.lev2.nas
    Failed to read header row 6.
    2010 01 01 2015 08 19
    
    Error msg: IndexError('list index out of range',)
    Ignoring line no. 35: 0
    
    Ignoring line no. 36: 53
    
    REACHED DATA BLOCK
      0.000000   0.041667  1030.95   0.00  302.69  1.25384615  0.459675   2.001625  0.87384615  0.659675  1.040975  0.68038462  0.539675  0.880325    9.81230769   8.787725   10.482100   8.06538462   7.818700   8.412600   6.30153846   5.889675   6.640975 0.000000
    


.. code:: ipython3

    len(data)




.. parsed-literal::

    7


