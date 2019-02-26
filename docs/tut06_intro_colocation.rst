
Colocating gridded data with discrete observations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This notebook gives an introduction into collocation of gridded data
with observations. Here, the 550 nm AODs of the ECMWF CAMS reanalysis
model are compared with global daily AeroNet Sun V2 (Level 2) data for
the year 2010. The collocated data will be analysed and visualised in
monthly resolution. The analysis results will be plotted in the form of
the well known Aerocom loglog scatter plots as can be found in the
online interface (see e.g.
`here <http://aerocom.met.no/cgi-bin/aerocom/surfobs_annualrs.pl>`__).

Import setup and imports
^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    import pyaerocom as pya
    pya.change_verbosity('critical')
    
    YEAR = 2010
    VAR = "od550aer"
    TS_TYPE = "daily"
    MODEL_ID = "ECMWF_CAMS_REAN"
    OBS_ID = 'AeronetSunV3Lev2.daily'


.. parsed-literal::

    Initating pyaerocom configuration
    Checking server configuration ...
    Checking access to: /lustre/storeA
    Access to lustre database: True
    Init data paths for lustre
    Expired time: 0.016 s


Import of model data
^^^^^^^^^^^^^^^^^^^^

Create reader instance for model data and print overview of what is in
there.

.. code:: ipython3

    model_reader = pya.io.ReadGridded(MODEL_ID)
    print(model_reader)


.. parsed-literal::

    
    Pyaerocom ReadGridded
    ---------------------
    Model ID: ECMWF_CAMS_REAN
    Data directory: /lustre/storeA/project/aerocom/aerocom-users-database/ECMWF/ECMWF_CAMS_REAN/renamed
    Available variables: ['ang4487aer', 'ec532aer3D', 'od440aer', 'od550aer', 'od550bc', 'od550dust', 'od550oa', 'od550so4', 'od550ss', 'od865aer', 'sconcpm10', 'sconcpm25']
    Available years: [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 9999]
    Available time resolutions ['daily', 'monthly']


Since we are only interested in a single year we can use the method

.. code:: ipython3

    model_data = model_reader.read_var(VAR, start=YEAR)
    #model_data = read_result[VAR][YEAR]
    print(model_data)


.. parsed-literal::

    pyaerocom.GriddedData: ECMWF_CAMS_REAN
    Grid data: Aerosol optical depth at 550 nm / (1) (time: 365; latitude: 161; longitude: 320)
         Dimension coordinates:
              time                             x              -               -
              latitude                         -              x               -
              longitude                        -              -               x
         Attributes:
              Conventions: CF-1.6
              NCO: "4.5.4"
              history: Sat May 26 21:08:48 2018: ncecat -O -u time -n 365,3,1 CAMS_REAN_001.nc...
              nco_openmp_thread_number: 1
         Cell methods:
              mean: step
              mean: time


.. code:: ipython3

    fig = model_data.quickplot_map(time_idx=0)



.. image:: tut06_intro_colocation/tut06_intro_colocation_7_0.png


Import of AeroNet Sun V3 data (Level 2)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Import Aeronet data and apply filter that selects only stations that are
located at altitudes between 0 and 1000 m.

.. code:: ipython3

    obs_reader = pya.io.ReadUngridded(OBS_ID, [VAR, 'ang4487aer'])
    obs_data = obs_reader.read().filter_by_meta(altitude=[0, 1000])
    print(obs_data)


.. parsed-literal::

    Found Cache match for AeronetSunV3Lev2.daily


.. parsed-literal::

    
    Pyaerocom UngriddedData
    -----------------------
    Contains networks: ['AeronetSunV3Lev2.daily']
    Contains variables: ['ang4487aer', 'od550aer']
    Contains instruments: ['sun_photometer']
    Total no. of meta-blocks: 1013
    Filters that were applied:
     Filter time log: 20190226171835
    	altitude: [0, 1000]


Plot station coordinates
^^^^^^^^^^^^^^^^^^^^^^^^

First, plot all stations that are available at all times (as red dots),
then (on top of that in green), plot all stations that provide AODs in
2010.

.. code:: ipython3

    ax = obs_data.plot_station_coordinates(color='r', markersize=20,
                                           label='All stations')
    ax = obs_data.plot_station_coordinates(var_name='od550aer', start=2010, 
                                           filter_name='WORLD-noMOUNTAINS',
                                           color='lime', markersize=8, legend=True,
                                           title='Aeronet V3 stations',
                                           ax=ax) #just pass the GeoAxes instance that was created in the first call



.. image:: tut06_intro_colocation/tut06_intro_colocation_11_0.png


Now perform collocation and plot corresponding scatter plots with statistical values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

2010 monthly World no mountains
'''''''''''''''''''''''''''''''

Colocate 2010 data in monthly resolution using (cf. green dots in
station plot above).

.. code:: ipython3

    obs_data




.. parsed-literal::

    UngriddedData <networks: ['AeronetSunV3Lev2.daily']; vars: ['ang4487aer', 'od550aer']; instruments: ['sun_photometer'];No. of stations: 1013



.. code:: ipython3

    data_coloc = pya.colocation.colocate_gridded_ungridded(model_data, obs_data, ts_type='monthly',
                                                           filter_name='WORLD-noMOUNTAINS')
    data_coloc


.. parsed-literal::

    Interpolating data of shape (12, 161, 320). This may take a while.
    Successfully interpolated cube




.. parsed-literal::

    <xarray.DataArray 'od550aer' (data_source: 2, time: 12, station_name: 278)>
    array([[[     nan, 0.117588, ...,      nan, 0.222138],
            [     nan, 0.132128, ...,      nan, 0.429762],
            ...,
            [0.132236, 0.195057, ...,      nan, 0.261765],
            [     nan, 0.098409, ...,      nan, 0.37905 ]],
    
           [[0.189948, 0.140062, ..., 0.079353, 0.204337],
            [0.150408, 0.190089, ..., 0.10622 , 0.257806],
            ...,
            [0.159844, 0.178564, ..., 0.054091, 0.239393],
            [0.147172, 0.138039, ..., 0.077916, 0.19986 ]]])
    Coordinates:
      * data_source   (data_source) <U22 'AeronetSunV3Lev2.daily' 'ECMWF_CAMS_REAN'
        var_name      (data_source) <U8 'od550aer' 'od550aer'
      * time          (time) datetime64[ns] 2010-01-15 2010-02-15 ... 2010-12-15
      * station_name  (station_name) <U19 'ARM_Darwin' ... 'Zinder_Airport'
        latitude      (station_name) float64 -12.43 37.97 15.35 ... 32.64 13.78
        longitude     (station_name) float64 130.9 23.72 -1.479 ... -114.6 8.99
        altitude      (station_name) float64 29.9 130.0 305.0 ... 20.0 63.0 456.0
    Attributes:
        data_source:      ['AeronetSunV3Lev2.daily', 'ECMWF_CAMS_REAN']
        var_name:         ['od550aer', 'od550aer']
        ts_type:          monthly
        filter_name:      WORLD-noMOUNTAINS
        ts_type_src:      daily
        ts_type_src_ref:  daily
        start_str:        20100101
        stop_str:         20101231
        unit:             ['1', '1']
        data_level:       colocated
        revision_ref:     20181212
        region:           WORLD
        lon_range:        [-180, 180]
        lat_range:        [-90, 90]
        alt_range:        [-1000000.0, 1000.0]



.. code:: ipython3

    data_coloc.plot_scatter()




.. parsed-literal::

    <matplotlib.axes._subplots.AxesSubplot at 0x7fce32af0780>




.. image:: tut06_intro_colocation/tut06_intro_colocation_16_1.png


2010 daily Europe no mountains
''''''''''''''''''''''''''''''

Now perform colocation only over Europe. Starting with a station plot.

.. code:: ipython3

    obs_data.plot_station_coordinates(var_name='od550aer', start=2010, 
                                      filter_name='EUROPE-noMOUNTAINS',
                                      color='lime', markersize=20, legend=True,
                                      title='Aeronet V3 stations')




.. parsed-literal::

    <cartopy.mpl.geoaxes.GeoAxes at 0x7fce32a70550>




.. image:: tut06_intro_colocation/tut06_intro_colocation_18_1.png


.. code:: ipython3

    data_coloc = pya.colocation.colocate_gridded_ungridded(model_data, obs_data, ts_type='daily',
                                                           filter_name='EUROPE-noMOUNTAINS')
    data_coloc


.. parsed-literal::

    Interpolating data of shape (365, 161, 320). This may take a while.
    Successfully interpolated cube




.. parsed-literal::

    <xarray.DataArray 'od550aer' (data_source: 2, time: 365, station_name: 89)>
    array([[[0.163447,      nan, ...,      nan,      nan],
            [0.078648,      nan, ...,      nan,      nan],
            ...,
            [     nan,      nan, ...,      nan,      nan],
            [     nan,      nan, ...,      nan,      nan]],
    
           [[0.086522, 0.015151, ..., 0.075447, 0.03005 ],
            [0.067198, 0.043074, ..., 0.103671, 0.042999],
            ...,
            [0.242585, 0.186407, ..., 0.053797, 0.011344],
            [0.079498, 0.122098, ..., 0.027066, 0.019639]]])
    Coordinates:
      * data_source   (data_source) <U22 'AeronetSunV3Lev2.daily' 'ECMWF_CAMS_REAN'
        var_name      (data_source) <U8 'od550aer' 'od550aer'
      * time          (time) datetime64[ns] 2010-01-01 2010-01-02 ... 2010-12-31
      * station_name  (station_name) <U19 'ATHENS-NOA' 'Andenes' ... 'Yekaterinburg'
        latitude      (station_name) float64 37.97 69.28 44.66 ... 51.77 41.15 57.04
        longitude     (station_name) float64 23.72 16.01 -1.163 ... 24.92 59.54
        altitude      (station_name) float64 130.0 379.0 11.0 ... 160.0 54.0 300.0
    Attributes:
        data_source:      ['AeronetSunV3Lev2.daily', 'ECMWF_CAMS_REAN']
        var_name:         ['od550aer', 'od550aer']
        ts_type:          daily
        filter_name:      EUROPE-noMOUNTAINS
        ts_type_src:      daily
        ts_type_src_ref:  daily
        start_str:        20100101
        stop_str:         20101231
        unit:             ['1', '1']
        data_level:       colocated
        revision_ref:     20181212
        region:           EUROPE
        lon_range:        [-20, 70]
        lat_range:        [30, 80]
        alt_range:        [-1000000.0, 1000.0]



.. code:: ipython3

    data_coloc.plot_scatter()




.. parsed-literal::

    <matplotlib.axes._subplots.AxesSubplot at 0x7fce540e00b8>




.. image:: tut06_intro_colocation/tut06_intro_colocation_20_1.png

