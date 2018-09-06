
EBAS file query and database browser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The previous tutorial showed how to read EBAS NASA Ames files and gave
insights into the structure of these files. However, this did not
include the specification of an actual data request (for instance: get
data from all stations in the arctic that contain measurements of the
AOD between 2010 and 2016).

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
    
    request = pya.io.ebas_file_index.EbasSQLRequest(variables=('aerosol_light_scattering_coefficient',
                                                                 'aerosol_light_backscattering_coefficient',
                                                                 'pressure'),
                                                      start_date="2010-01-01", 
                                                      stop_date="2011-01-01")
    print(request)


.. parsed-literal::

    2018-09-05 14:08:17,560:INFO:
    Reading aliases ini file: /home/jonasg/github/pyaerocom/pyaerocom/data/aliases.ini
    2018-09-05 14:08:18,299:WARNING:
    geopy library is not available. Aeolus data read not enabled


.. parsed-literal::

    
    Pyaerocom EbasSQLRequest
    ------------------------
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
    Filename request string:
    select distinct filename from variable join station on station.station_code=variable.station_code where comp_name in ('aerosol_light_scattering_coefficient', 'aerosol_light_backscattering_coefficient', 'pressure') and first_end < '2011-01-01' and last_start > '2010-01-01';


You can also output the actual SQL query string:

.. code:: ipython3

    print(request.make_query_str())


.. parsed-literal::

    select distinct filename from variable join station on station.station_code=variable.station_code where comp_name in ('aerosol_light_scattering_coefficient', 'aerosol_light_backscattering_coefficient', 'pressure') and first_end < '2011-01-01' and last_start > '2010-01-01';


The request class is an extended dictionary and can thus be used like a
dictionary:

.. code:: ipython3

    request.update(instrument_types=("nephelometer"))
    print(request)


.. parsed-literal::

    
    Pyaerocom EbasSQLRequest
    ------------------------
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
    Filename request string:
    select distinct filename from variable join station on station.station_code=variable.station_code where instr_type in ('nephelometer') and comp_name in ('aerosol_light_scattering_coefficient', 'aerosol_light_backscattering_coefficient', 'pressure') and first_end < '2011-01-01' and last_start > '2010-01-01';


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
    
    Pyaerocom EbasSQLRequest
    ------------------------
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
    Filename request string:
    select distinct filename from variable join station on station.station_code=variable.station_code where instr_type in ('nephelometer') and comp_name in ('aerosol_light_scattering_coefficient', 'aerosol_light_backscattering_coefficient', 'pressure') and first_end < '2011-01-01' and last_start > '2010-01-01';


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

    [('pressure',), ('aerosol_light_backscattering_coefficient',), ('aerosol_light_scattering_coefficient',)]


Or what matrices the data contains:

.. code:: ipython3

    print(db.contains_matrices(request))


.. parsed-literal::

    [('instrument',), ('aerosol',), ('pm10',), ('pm1',)]


Or which station coordinates (lon, lat) the dataset contains:

.. code:: ipython3

    print(db.contains_coordinates(request))


.. parsed-literal::

    [(23.583333, 42.166667), (-79.783839, 44.231006), (-122.9576034546, 50.059299469), (-104.986864, 54.353743), (-62.3415260315, 82.4991455078), (7.985, 46.5475), (11.0096197128, 47.8014984131), (12.93386, 51.53014), (10.97964, 47.4165), (-8.266, -70.666), (-16.4994, 28.309), (-3.605, 37.164), (2.35, 41.766667), (24.283333, 61.85), (24.116111111, 67.973333333), (2.95, 45.76667), (25.666667, 35.316667), (19.583333, 46.966667), (-9.89944, 53.32583), (77.151389, 28.427778), (8.633333, 45.8), (10.7, 44.183333), (126.17, 33.28), (4.926389, 51.970278), (8.252, 58.38853), (11.888333, 78.906667), (2.533333, -72.016667), (-65.618, 18.381), (13.15, 56.016667), (120.87, 23.47), (-156.6114654541, 71.3230133057), (-111.9841, 35.9731), (-112.1288, 36.0778), (-111.6832, 34.3405), (-112.8, 31.9506), (-109.3889, 32.0097), (-155.5761566162, 19.5362300873), (-86.148, 37.1317), (-68.2608, 44.3772), (-113.9958, 48.5103), (-81.7, 36.2), (-103.1772, 29.3022), (-97.5, 36.6), (-24.7999992371, -89.9969482422), (-124.1510009766, 41.0541000366), (-105.5457, 40.2783), (-111.9692, 35.1406), (-77.04, 38.9), (-109.7958, 34.9139), (18.48968, -34.35348)]


Now, let’s narrow this down:

.. code:: ipython3

    request.update(lat_range=(60, 90))
    print(db.contains_coordinates(request))


.. parsed-literal::

    [(-62.3415260315, 82.4991455078), (24.283333, 61.85), (24.116111111, 67.973333333), (11.888333, 78.906667), (-156.6114654541, 71.3230133057)]


Print all station names:

.. code:: ipython3

    print(db.contains_station_names(request))


.. parsed-literal::

    [('Alert',), ('Hyytiälä',), ('Pallas (Sammaltunturi)',), ('Zeppelin mountain (Ny-Ålesund)',), ('Barrow',)]


Custom browsing
^^^^^^^^^^^^^^^

The previous browsing methods (e.g. ``contains_coordinates()``,
``contains_matrices``, ``contains_variables``) are all just simple
wrappers for the general query method ``make_query_str`` of the
``EbasSQLRequest`` class, that is then called by the ``EbasFileIndex``
class using the method ``execute_request``). Thus, if needed, you may
define your own request simply by using the provided interface. Here an
example using the request constraints specified above. Let’s say we want
to retrieve a list of station names and their coordinates (lon, lat,
alt). This can be done by calling (we store the results in a list named
``station_info``):

.. code:: ipython3

    query_str = request.make_query_str(what=("station_name",
                                             "station_longitude",
                                             "station_latitude",
                                             "station_altitude"))
    
    station_info = db.execute_request(query_str)
    
    for item in station_info:
        print(item)


.. parsed-literal::

    ('Alert', -62.3415260315, 82.4991455078, 210.0)
    ('Hyytiälä', 24.283333, 61.85, 181.0)
    ('Pallas (Sammaltunturi)', 24.116111111, 67.973333333, 565.0)
    ('Zeppelin mountain (Ny-Ålesund)', 11.888333, 78.906667, 474.0)
    ('Barrow', -156.6114654541, 71.3230133057, 11.0)


You can see that the results for each station are stored in tuples in
the order of the request.

Read all files
^^^^^^^^^^^^^^

Let’s update the file list and read all files.

.. code:: ipython3

    files = db.execute_request(request)
    print("Total number of files found: {}".format(len(files)))


.. parsed-literal::

    Total number of files found: 7


Let’s read the files:

.. code:: ipython3

    import os
    data = []
    data_dir = os.path.join(pya.const.OBSCONFIG["EBASMC"]["PATH"], 'data')
    for f in files:
        data.append(pya.io.EbasNasaAmesFile(os.path.join(data_dir, f[0])))


.. parsed-literal::

    2018-09-05 14:08:23,106:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/CA0420G.20100101000000.20150209103939.nephelometer...1y.1h.CA01L_TSI_3563_ALT.CA01L_scat_coef.lev2.nas
    2018-09-05 14:08:23,135:WARNING:
    Failed to read header row 6.
    2010 01 01 2015 02 09
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:23,142:DEBUG:
    Ignoring line no. 97: 0
    
    2018-09-05 14:08:23,144:DEBUG:
    Ignoring line no. 98: 53
    
    2018-09-05 14:08:23,147:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:23,148:DEBUG:
      0.000000   0.041667   973.59 0.392000   0.70 0.392000  301.32 0.392000  1.70400000 0.392000 99.99999999 0.460000  1.398528 0.392000 99.999999 0.460000  1.897151 0.392000 99.999999 0.460000  1.60500000 0.392000 99.99999999 0.460000  1.520000 0.392000 99.999999 0.460000  1.682868 0.392000 99.999999 0.460000  1.41100000 0.392000 99.99999999 0.460000  1.302849 0.392000 99.999999 0.460000  1.537151 0.392000 99.999999 0.460000  16.39900000 0.392000 999.99999999 0.460000  15.911377 0.392000 999.999999 0.460000  17.052887 0.392000 999.999999 0.460000  14.22400000 0.392000 999.99999999 0.460000  13.938566 0.392000 999.999999 0.460000  14.567189 0.392000 999.999999 0.460000  11.62600000 0.392000 999.99999999 0.460000  11.227075 0.392000 999.999999 0.460000  11.987189 0.392000 999.999999 0.460000 99999.99 0.460000 999.99 0.460000 9999.99 0.460000
    
    2018-09-05 14:08:23,627:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/CA0420G.20100101000000.20170516083933.nephelometer..pm10.1y.1h.CA01L_TSI_3563_ALT_pm10.CA01L_scat_coef.lev2.nas
    2018-09-05 14:08:23,840:WARNING:
    Failed to read header row 6.
    2010 01 01 2017 05 16
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:23,844:DEBUG:
    Ignoring line no. 35: 0
    
    2018-09-05 14:08:23,846:DEBUG:
    Ignoring line no. 36: 54
    
    2018-09-05 14:08:23,851:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:23,853:DEBUG:
      0.000000   0.041667   973.59   0.70  301.32  1.11600000  0.808528  1.317151  1.06500000  0.980000  1.142868 -0.96600000 -1.072868 -0.842849  14.61500000  14.062792  15.367189  11.70000000  11.392830  12.000057   6.56100000   6.185641   6.912868 0.392000
    
    2018-09-05 14:08:24,187:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/FI0050R.20100101000000.20121004000000.nephelometer..aerosol.1y.1h.FI03L_TSI3563.FI03L_Corrected_according_to_Anderson_and_Ogre..nas
    2018-09-05 14:08:24,232:WARNING:
    Failed to read header row 6.
    2010 01 01 2012 10 04
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:24,236:DEBUG:
    Ignoring line no. 34: 0
    
    2018-09-05 14:08:24,238:DEBUG:
    Ignoring line no. 35: 33
    
    2018-09-05 14:08:24,241:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:24,244:DEBUG:
      0.000000   0.041667   2.97   2.87   3.07   2.47   2.42   2.51   2.10   1.91   2.25   27.20   26.77   27.60   19.72   19.37   20.04   12.53   12.26   12.81   980.61  291.42 0.247000
    
    2018-09-05 14:08:24,439:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/FI0096G.20100412110000.20160705103730.nephelometer..pm10.9mo.1h.FI01L_TSI_3563_PAL_dry.FI01L_neph_control_lev1_0_0_1.lev2.nas
    2018-09-05 14:08:24,523:WARNING:
    Failed to read header row 6.
    2010 01 01 2016 07 05
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:24,527:DEBUG:
    Ignoring line no. 34: 0
    
    2018-09-05 14:08:24,529:DEBUG:
    Ignoring line no. 35: 60
    
    2018-09-05 14:08:24,533:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:24,536:DEBUG:
    101.458333 101.500000  939.0000000  299.4000000   1.196056   1.150314   1.241439   1.005160   0.974795   1.036001   1.022035   0.957909   1.084102   10.408017   10.305080   10.513390    7.616671    7.525326    7.708703   5.327212   5.288039    5.365250 0.390191
    
    2018-09-05 14:08:24,783:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/NO0042G.20100101000000.20150216111241.nephelometer..pm10.1y.1h.SE02L_TSI_3563_ZEP_dry.SE02L_scat_coef.lev2.nas
    2018-09-05 14:08:24,885:WARNING:
    Failed to read header row 6.
    2010 01 01 2015 02 16
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:24,888:DEBUG:
    Ignoring line no. 35: 0
    
    2018-09-05 14:08:24,891:DEBUG:
    Ignoring line no. 36: 39
    
    2018-09-05 14:08:24,893:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:24,896:DEBUG:
      0.000000   0.041667  955.500   6.800  300.000    -9.457    -9.629    -9.123   -6.280   -6.519   -6.110  -12.471  -12.627  -12.314     7.019     6.583     7.700     5.635     5.173     5.955    3.842    3.730    4.224 0.459000
    
    2018-09-05 14:08:25,145:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/US0008R.20100101000000.20150819091559.nephelometer...1y.1h.US06L_TSI_3563_BRW.US06L_scat_coef..nas
    2018-09-05 14:08:25,195:WARNING:
    Failed to read header row 6.
    2010 01 01 2015 08 19
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:25,202:DEBUG:
    Ignoring line no. 85: 0
    
    2018-09-05 14:08:25,205:DEBUG:
    Ignoring line no. 86: 37
    
    2018-09-05 14:08:25,208:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:25,210:DEBUG:
      0.000000   0.041667  1.25384600 0.000000  1.02888900 0.000000  0.459675 0.000000  0.375144 0.000000   2.001625 0.000000  1.751166 0.000000  0.87384610 0.000000  0.53888890 0.000000  0.659675 0.000000  0.392524 0.000000  1.040975 0.000000  0.712428 0.000000  0.68038460 0.000000  0.39518520 0.000000  0.539675 0.000000  0.251262 0.000000  0.880325 0.000000  0.596214 0.000000  9.8123080E+00 0.000000   5.71963000 0.000000   8.787725 0.000000   4.503978 0.000000   10.482100 0.000000   6.792332 0.000000   8.06538500 0.000000   4.37518500 0.000000   7.818700 0.000000   4.045144 0.000000   8.412600 0.000000   4.726214 0.000000   6.30153800 0.000000   2.75666700 0.000000   5.889675 0.000000   2.540000 0.000000   6.640975 0.000000   2.987476 0.000000
    
    2018-09-05 14:08:25,592:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/US0008R.20100101000000.20150819091559.nephelometer..pm10.1y.1h.US06L_TSI_3563_BRW.US06L_scat_coef.lev2.nas
    2018-09-05 14:08:25,633:WARNING:
    Failed to read header row 6.
    2010 01 01 2015 08 19
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:25,637:DEBUG:
    Ignoring line no. 35: 0
    
    2018-09-05 14:08:25,639:DEBUG:
    Ignoring line no. 36: 53
    
    2018-09-05 14:08:25,642:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:25,645:DEBUG:
      0.000000   0.041667  1030.95   0.00  302.69  1.25384615  0.459675   2.001625  0.87384615  0.659675  1.040975  0.68038462  0.539675  0.880325    9.81230769   8.787725   10.482100   8.06538462   7.818700   8.412600   6.30153846   5.889675   6.640975 0.000000
    


.. code:: ipython3

    len(data)




.. parsed-literal::

    7


