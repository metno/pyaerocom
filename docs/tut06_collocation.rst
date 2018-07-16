
Collocating gridded data with discrete observations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This notebook gives an introduction into collocation of gridded data
with observations. Here, AODs of the ECMWF CAMS reanalysis model are
compared with global daily observations from the AeroNet V2 (Level 2)
for the years of 2010-2018.

NOTE
^^^^

 This notebook is currently under development

Import setup and imports
^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    import pyaerocom
    
    start=2000
    stop=2018
    
    variables = ["od550aer"]
    
    ts_type = "daily"
    
    model_id = "ECMWF_CAMS_REAN"
    obs_id = pyaerocom.const.AERONET_SUN_V2L2_AOD_DAILY_NAME
    obs_id




.. parsed-literal::

    'AeronetSunV2Lev2.daily'



Import of model data
^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    model_io = pyaerocom.io.ReadGridded(model_id, start_time=start, stop_time=stop, verbose=False)
    print(model_io)


.. parsed-literal::

    
    Pyaerocom ReadGridded
    ---------------------
    Model ID: ECMWF_CAMS_REAN
    Available variables: ['ang4487aer', 'od440aer', 'od550aer', 'od550bc', 'od550dust', 'od550oa', 'od550so4', 'od550ss', 'od865aer']
    Available years: [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 9999]


.. code:: ipython3

    for var in variables:
        model_io.read_var(var)

.. code:: ipython3

    print(model_io)


.. parsed-literal::

    
    Pyaerocom ReadGridded
    ---------------------
    Model ID: ECMWF_CAMS_REAN
    Available variables: ['ang4487aer', 'od440aer', 'od550aer', 'od550bc', 'od550dust', 'od550oa', 'od550so4', 'od550ss', 'od865aer']
    Available years: [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 9999]
    
    Loaded GriddedData objects:
    
    Pyaerocom GriddedData
    ---------------------
    Variable: od550aer
    Temporal resolution: daily
    Start / Stop: 2003-01-01T00:00:00.000000 - 2016-12-31T00:00:00.000000


.. code:: ipython3

    model_data = model_io["od550aer"]

.. code:: ipython3

    fig = model_data.quickplot_map()



.. image:: tut06_collocation/tut06_collocation_8_0.png


Import of AeroNet V2 data (Level 2)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    read = pyaerocom.io.ReadAeronetSunV2()
    obs_data = read.read_first_file()


.. parsed-literal::

    2018-07-16 15:44:45,169:INFO:
    searching for data files. This might take a while...
    2018-07-16 15:44:45,254:INFO:
    Reading file /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetRaw2.0/renamed/920801_180519_UNC-Palmira.lev20

