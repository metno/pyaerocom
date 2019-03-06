
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

    Initating pyaerocom configuration
    Checking server configuration ...
    Checking access to: /lustre/storeA
    Access to lustre database: True
    Init data paths for lustre
    Expired time: 0.020 s


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
    datalevel: None
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
    datalevel: None
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

    Total number of files found:78
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
    datalevel: None
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

    [('instrument',), ('aerosol',), ('pm1',), ('pm10',)]


Or which station coordinates (lon, lat) the dataset contains:

.. code:: ipython3

    print(db.contains_coordinates(request))


.. parsed-literal::

    [(23.583333, 42.166667), (-79.783839, 44.231006), (-122.9576034546, 50.059299469), (-104.986864, 54.353743), (-62.3415260315, 82.4991455078), (7.985, 46.5475), (11.0096197128, 47.8014984131), (12.93386, 51.53014), (10.97964, 47.4165), (-8.266, -70.666), (-3.605, 37.164), (-6.733333, 37.1), (2.35, 41.766667), (24.283333, 61.85), (24.116111111, 67.973333333), (2.964886, 45.772223), (25.666667, 35.316667), (19.583333, 46.966667), (-9.89944, 53.32583), (77.151389, 28.427778), (8.633333, 45.8), (10.7, 44.183333), (126.17, 33.28), (4.926389, 51.970278), (8.252, 58.38853), (11.88668, 78.90715), (2.533333, -72.016667), (-65.618, 18.381), (13.15, 56.016667), (120.87, 23.47), (-156.6114654541, 71.3230133057), (-111.9841, 35.9731), (-112.1288, 36.0778), (-111.6832, 34.3405), (-83.9416, 35.6334), (-112.8, 31.9506), (-109.3889, 32.0097), (-155.5761566162, 19.5362300873), (-86.148, 37.1317), (-68.2608, 44.3772), (-113.9958, 48.5103), (-114.2158, 39.005), (-81.7, 36.2), (-103.1772, 29.3022), (-78.4358, 38.5225), (-122.1243, 46.7582), (-97.484999, 36.605), (-24.7999992371, -89.9969482422), (-124.1510009766, 41.0541000366), (-105.5457, 40.2783), (-111.9692, 35.1406), (-77.04, 38.9), (-109.7958, 34.9139), (18.48968, -34.35348)]


Now, let’s narrow this down:

.. code:: ipython3

    request.update(lat_range=(60, 90))
    print(db.contains_coordinates(request))


.. parsed-literal::

    [(-62.3415260315, 82.4991455078), (24.283333, 61.85), (24.116111111, 67.973333333), (11.88668, 78.90715), (-156.6114654541, 71.3230133057)]


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
    ('Zeppelin mountain (Ny-Ålesund)', 11.88668, 78.90715, 474.0)
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

.. code:: ipython3

    len(data)




.. parsed-literal::

    7


