
Merging of several StationData objects into one
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This notebook illustrates how one can merge several instances
StationData objects into one objects. This merging only works for data
from the same station and a typical case is if the data source files for
one station are separated into many single files containing only parts
of the data (e.g. if the files contain only one year of data).

In the following, the example of the EBAS database is used for
illustration. In particular, we will focus on the retrieval of the
aerosol light scattering coefficients at 550 nm (**scatc550aer** in
AEROCOM naming convention) for the station **Jungfraujoch**, located in
Germany.

.. code:: ipython3

    import pyaerocom as pya


.. parsed-literal::

    Initating pyaerocom configuration
    Checking server configuration ...
    Checking access to: /lustre/storeA
    Access to lustre database: True
    Init data paths for lustre
    Expired time: 0.015 s


Get list of all files containing scattering data for EBAS station Jungfraujoch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    reader = pya.io.ReadEbas()
    data = reader.read(vars_to_retrieve='scatc550aer', 
                                datalevel=2, station_names='Jungfraujoch')
    print(data)


.. parsed-literal::

    Reading file 1 of 26 (ReadEbas)
    Reading file 3 of 26 (ReadEbas)
    Reading file 5 of 26 (ReadEbas)
    Reading file 7 of 26 (ReadEbas)
    Reading file 9 of 26 (ReadEbas)
    Reading file 11 of 26 (ReadEbas)
    Reading file 13 of 26 (ReadEbas)
    Reading file 15 of 26 (ReadEbas)
    Reading file 17 of 26 (ReadEbas)
    Reading file 19 of 26 (ReadEbas)
    Reading file 21 of 26 (ReadEbas)
    Reading file 23 of 26 (ReadEbas)
    Reading file 25 of 26 (ReadEbas)
    
    Pyaerocom UngriddedData
    -----------------------
    Contains networks: ['EBASMC']
    Contains variables: ['scatc550aer']
    Contains instruments: ['IN3563', 'TSI_3563_JFJ_dry', 'Ecotech_Aurora3000_JFJ_dry']
    Total no. of meta-blocks: 26
    Filters that were applied:
     Filter time log: 20190226172014
    	datalevel: 2
    	station_names: Jungfraujoch


As you can see, the data has successfully been imported into an instance
of the ``UngriddedData`` class. This class is organised *by file*, that
is, for each of the 26 files that were imported, there is one metadata
dictionary assigned. Let’s look at the metadata from the first file:

.. code:: ipython3

    data.metadata[0]




.. parsed-literal::

    OrderedDict([('latitude', 46.5475),
                 ('longitude', 7.985),
                 ('altitude', 3578.0),
                 ('station_name', 'Jungfraujoch'),
                 ('instrument_name', 'IN3563'),
                 ('PI', 'Baltensperger, Urs; Weingartner, Ernest'),
                 ('ts_type', 'hourly'),
                 ('data_id', 'EBASMC'),
                 ('revision_date', numpy.datetime64('2018-10-31T00:00:00')),
                 ('filename',
                  'CH0001G.19950101000000.20181031145000.nephelometer..aerosol.1y.1h.CH02L_IN3563.CH02L_backscat_coef.lev2.nas'),
                 ('var_info',
                  OrderedDict([('scatc550aer',
                                {'name': 'aerosol_light_scattering_coefficient',
                                 'unit': '1/Mm',
                                 'wavelength': '550.0 nm',
                                 'method_ref': 'CH02L_scat_coef',
                                 'matrix': 'aerosol',
                                 'statistics': 'arithmetic mean'})])),
                 ('variables', ['scatc550aer'])])



And the last one:

.. code:: ipython3

    data.metadata[25]




.. parsed-literal::

    OrderedDict([('latitude', 46.5475),
                 ('longitude', 7.985),
                 ('altitude', 3580.0),
                 ('station_name', 'Jungfraujoch'),
                 ('instrument_name', 'Ecotech_Aurora3000_JFJ_dry'),
                 ('PI', 'Bukowiecki, Nicolas; Baltensperger, Urs'),
                 ('ts_type', 'hourly'),
                 ('data_id', 'EBASMC'),
                 ('revision_date', numpy.datetime64('2018-03-20T00:00:00')),
                 ('filename',
                  'CH0001G.20170101000000.20180320151536.nephelometer..aerosol.1y.1h.CH02L_Ecotech_Aurora3000_JFJ_dry.CH02L_Neph_Aurora3000.lev2.nas'),
                 ('var_info',
                  OrderedDict([('scatc550aer',
                                {'name': 'aerosol_light_scattering_coefficient',
                                 'unit': '1/Mm',
                                 'wavelength': '525.0 nm',
                                 'statistics': 'arithmetic mean',
                                 'matrix': 'aerosol'})])),
                 ('variables', ['scatc550aer'])])



As you can see, both files contain scattering data but do not share all
the same metadata attributes (e.g. ``instrument_name`` is different,
which might be due to technological updates over time).

Let’s have a look at the respective time-series for both stations.
First, convert into instance of ``StationData`` class and then plot.

.. code:: ipython3

    first_file = data.to_station_data(0, vars_to_convert='scatc550aer')
    print(first_file)


.. parsed-literal::

    
    Pyaerocom StationData
    ---------------------
    var_info (BrowseDict([('scatc550aer', {'name': 'aerosol_light_scattering_coefficient', 'unit': '1/Mm', 'wavelength': '550.0 nm', 'method_ref': 'CH02L_scat_coef', 'matrix': 'aerosol', 'statistics': 'arithmetic mean', 'overlap': False})]))
       scatc550aer (<class 'dict'>)
        name: aerosol_light_scattering_coefficient
        unit: 1/Mm
        wavelength: 550.0 nm
        method_ref: CH02L_scat_coef
        matrix: aerosol
        statistics: arithmetic mean
        overlap: False
    station_coords ({'latitude': 46.5475, 'longitude': 7.985, 'altitude': 3578.0})
       latitude: 46.5475
       longitude: 7.985
       altitude: 3578.0
    data_err (BrowseDict([('scatc550aer', array([nan, nan, nan, ..., nan, nan, nan]))]))
       scatc550aer (array, 8760 items)
       [nan
        nan
        ...
        nan
        nan]
    
    overlap (BrowseDict())
    filename: CH0001G.19950101000000.20181031145000.nephelometer..aerosol.1y.1h.CH02L_IN3563.CH02L_backscat_coef.lev2.nas
    station_id: None
    station_name: Jungfraujoch
    instrument_name: IN3563
    PI: Baltensperger, Urs; Weingartner, Ernest
    country: None
    ts_type: hourly
    latitude: 46.5475
    longitude: 7.985
    altitude: 3578.0
    data_id: EBASMC
    dataset_name: None
    data_product: None
    data_version: None
    data_level: None
    revision_date: 2018-10-31T00:00:00
    ts_type_src: hourly
    
    Data arrays
    .................
    dtime (array, 8760 items)
       [numpy.datetime64('1995-01-01T00:30:00.000000000')
        numpy.datetime64('1995-01-01T01:29:59.000000000')
        ...
        numpy.datetime64('1995-12-31T22:29:59.000000000')
        numpy.datetime64('1995-12-31T23:29:59.000000000')]
    
    Pandas Series
    .................
    scatc550aer (Series, 8760 items)


.. code:: ipython3

    last_file = data.to_station_data(25)
    print(last_file)


.. parsed-literal::

    
    Pyaerocom StationData
    ---------------------
    var_info (BrowseDict([('scatc550aer', {'name': 'aerosol_light_scattering_coefficient', 'unit': '1/Mm', 'wavelength': '525.0 nm', 'statistics': 'arithmetic mean', 'matrix': 'aerosol', 'overlap': False})]))
       scatc550aer (<class 'dict'>)
        name: aerosol_light_scattering_coefficient
        unit: 1/Mm
        wavelength: 525.0 nm
        statistics: arithmetic mean
        matrix: aerosol
        overlap: False
    station_coords ({'latitude': 46.5475, 'longitude': 7.985, 'altitude': 3580.0})
       latitude: 46.5475
       longitude: 7.985
       altitude: 3580.0
    data_err (BrowseDict([('scatc550aer', array([nan, nan, nan, ..., nan, nan, nan]))]))
       scatc550aer (array, 8760 items)
       [nan
        nan
        ...
        nan
        nan]
    
    overlap (BrowseDict())
    filename: CH0001G.20170101000000.20180320151536.nephelometer..aerosol.1y.1h.CH02L_Ecotech_Aurora3000_JFJ_dry.CH02L_Neph_Aurora3000.lev2.nas
    station_id: None
    station_name: Jungfraujoch
    instrument_name: Ecotech_Aurora3000_JFJ_dry
    PI: Bukowiecki, Nicolas; Baltensperger, Urs
    country: None
    ts_type: hourly
    latitude: 46.5475
    longitude: 7.985
    altitude: 3580.0
    data_id: EBASMC
    dataset_name: None
    data_product: None
    data_version: None
    data_level: None
    revision_date: 2018-03-20T00:00:00
    ts_type_src: hourly
    
    Data arrays
    .................
    dtime (array, 8760 items)
       [numpy.datetime64('2017-01-01T00:30:00.000000000')
        numpy.datetime64('2017-01-01T01:29:59.000000000')
        ...
        numpy.datetime64('2017-12-31T22:29:59.000000000')
        numpy.datetime64('2017-12-31T23:29:59.000000000')]
    
    Pandas Series
    .................
    scatc550aer (Series, 8760 items)


.. code:: ipython3

    first_file.plot_timeseries('scatc550aer');



.. image:: add04_stationdata_merging/add04_stationdata_merging_11_0.png


.. code:: ipython3

    last_file.plot_timeseries('scatc550aer');



.. image:: add04_stationdata_merging/add04_stationdata_merging_12_0.png


As you can see, the files contain data from different years. Now, how
can we get these objects into one object that contains the timeseries of
both files from this station?

This is actually very easy:

.. code:: ipython3

    merged = first_file.merge_other(last_file, 'scatc550aer')
    print(merged)


.. parsed-literal::

    
    Pyaerocom StationData
    ---------------------
    var_info (BrowseDict([('scatc550aer', {'name': 'aerosol_light_scattering_coefficient', 'unit': '1/Mm', 'wavelength': '550.0 nm;525.0 nm', 'method_ref': 'CH02L_scat_coef', 'matrix': 'aerosol', 'statistics': 'arithmetic mean', 'overlap': False})]))
       scatc550aer (<class 'dict'>)
        name: aerosol_light_scattering_coefficient
        unit: 1/Mm
        wavelength: 550.0 nm;525.0 nm
        method_ref: CH02L_scat_coef
        matrix: aerosol
        statistics: arithmetic mean
        overlap: False
    station_coords ({'latitude': 46.5475, 'longitude': 7.985, 'altitude': 3578.0})
       latitude: 46.5475
       longitude: 7.985
       altitude: 3578.0
    data_err (BrowseDict([('scatc550aer', array([nan, nan, nan, ..., nan, nan, nan]))]))
       scatc550aer (array, 8760 items)
       [nan
        nan
        ...
        nan
        nan]
    
    overlap (BrowseDict())
    filename: CH0001G.19950101000000.20181031145000.nephelometer..aerosol.1y.1h.CH02L_IN3563.CH02L_backscat_coef.lev2.nas;CH0001G.20170101000000.20180320151536.nephelometer..aerosol.1y.1h.CH02L_Ecotech_Aurora3000_JFJ_dry.CH02L_Neph_Aurora3000.lev2.nas
    station_id: None
    station_name: Jungfraujoch
    instrument_name: IN3563;Ecotech_Aurora3000_JFJ_dry
    PI: Baltensperger, Urs; Weingartner, Ernest;Bukowiecki, Nicolas
    country: None
    ts_type: hourly
    latitude: 46.5475
    longitude: 7.985
    altitude: 3578.0
    data_id: EBASMC
    dataset_name: None
    data_product: None
    data_version: None
    data_level: None
    revision_date (list, 2 items)
       [numpy.datetime64('2018-10-31T00:00:00')
        numpy.datetime64('2018-03-20T00:00:00')]
    
    ts_type_src: hourly
    
    Data arrays
    .................
    dtime (array, 9794 items)
       [numpy.datetime64('1995-07-08T23:29:59.000000000')
        numpy.datetime64('1995-07-09T00:30:00.000000000')
        ...
        numpy.datetime64('2017-12-24T19:29:59.000000000')
        numpy.datetime64('2017-12-31T23:29:59.000000000')]
    
    Pandas Series
    .................
    scatc550aer (Series, 9794 items)


As you can see in the output, the merging comprises not only the data
arrays but also registers any differences in the assoicated metdadata
(cf. e.g., sampling wavelength 550 nm vs. 525 nm, instrument name, PI)

Now, have a look at the merged timeseries data.

.. code:: ipython3

    merged.plot_timeseries('scatc550aer');



.. image:: add04_stationdata_merging/add04_stationdata_merging_17_0.png


Looks okay. Let’s merge all 26 files and see if we get a nice long time
series.

Retrieve list of ``StationData`` objects:

.. code:: ipython3

    stats = data.to_station_data('Jungfraujoch', 'scatc550aer', merge_if_multi=False)
    print('Number of StationData objects retrieved: {}'.format(len(stats)))


.. parsed-literal::

    Number of StationData objects retrieved: 26


Now merge them into one long time series:

.. code:: ipython3

    merged = pya.helpers.merge_station_data(stats, var_name='scatc550aer')
    print(merged)


.. parsed-literal::

    
    Pyaerocom StationData
    ---------------------
    var_info (BrowseDict([('scatc550aer', {'name': 'aerosol_light_scattering_coefficient', 'unit': '1/Mm', 'wavelength': '550.0 nm;525.0 nm', 'statistics': 'arithmetic mean', 'matrix': 'aerosol', 'overlap': False, 'method_ref': 'CH02L_scat_coef', 'ts_type': 'hourly'})]))
       scatc550aer (<class 'dict'>)
        name: aerosol_light_scattering_coefficient
        unit: 1/Mm
        wavelength: 550.0 nm;525.0 nm
        statistics: arithmetic mean
        matrix: aerosol
        overlap: False
        method_ref: CH02L_scat_coef
        ts_type: hourly
    station_coords ({'latitude': 46.5475, 'longitude': 7.985, 'altitude': 3580.0})
       latitude: 46.5475
       longitude: 7.985
       altitude: 3580.0
    data_err (BrowseDict([('scatc550aer', array([nan, nan, nan, ..., nan, nan, nan]))]))
       scatc550aer (array, 8760 items)
       [nan
        nan
        ...
        nan
        nan]
    
    overlap (BrowseDict([('scatc550aer', 2015-01-01 00:30:00    0.068376
    2015-01-01 01:29:59    0.255198
    2015-01-01 02:29:59   -0.284809
    2015-01-01 03:30:00    0.123830
    2015-01-01 04:29:59    0.127599
    2015-01-01 05:29:59    0.052224
    2015-01-01 06:30:00   -0.011306
    2015-01-01 07:29:59    0.086143
    2015-01-01 08:29:59   -0.088835
    2015-01-01 09:30:00   -0.084528
    2015-01-01 10:29:59    0.082912
    2015-01-01 11:29:59    0.540007
    2015-01-01 12:30:00    0.062992
    2015-01-01 13:29:59    0.791436
    2015-01-01 14:29:59    0.220202
    2015-01-01 15:30:00   -0.008076
    2015-01-01 16:29:59    0.062992
    2015-01-01 17:29:59    0.386565
    2015-01-01 18:30:00    0.272965
    2015-01-01 19:29:59    0.078067
    2015-01-01 20:29:59    0.375259
    2015-01-01 21:30:00    0.059223
    2015-01-01 22:29:59    0.164209
    2015-01-01 23:29:59   -0.025843
    2015-01-02 00:30:00    0.074836
    2015-01-02 01:29:59    0.159902
    2015-01-02 02:29:59    0.003769
    2015-01-02 03:30:00    0.050070
    2015-01-02 04:29:59    0.156134
    2015-01-02 05:29:59   -0.015613
                             ...   
    2017-12-23 15:30:00    0.504355
    2017-12-23 16:29:59    0.395655
    2017-12-23 17:29:59    0.259811
    2017-12-23 18:30:00    0.258700
    2017-12-23 19:29:59    0.259792
    2017-12-23 20:29:59    0.211566
    2017-12-23 21:30:00    0.296822
    2017-12-23 22:29:59    0.158973
    2017-12-23 23:29:59    0.048703
    2017-12-24 00:30:00    0.103658
    2017-12-24 01:29:59    0.226225
    2017-12-24 02:29:59    0.145462
    2017-12-24 03:30:00    0.081840
    2017-12-24 04:29:59    0.186278
    2017-12-24 05:29:59    0.137102
    2017-12-24 06:30:00    0.192551
    2017-12-24 07:29:59    0.201115
    2017-12-24 08:29:59    0.364645
    2017-12-24 09:30:00    0.375183
    2017-12-24 10:29:59    0.947353
    2017-12-24 11:29:59    0.321736
    2017-12-24 12:30:00    0.601246
    2017-12-24 13:29:59    0.970577
    2017-12-24 14:29:59    0.172226
    2017-12-24 15:30:00    0.161048
    2017-12-24 16:29:59    0.138531
    2017-12-24 17:29:59    0.099212
    2017-12-24 18:30:00    0.186739
    2017-12-24 19:29:59    0.194889
    2017-12-31 23:29:59    0.750785
    Length: 17466, dtype: float64)]))
       scatc550aer: 2015-01-01 00:30:00    0.068376
    2015-01-01 01:29:59    0.255198
    2015-01-01 02:29:59   -0.284809
    2015-01-01 03:30:00    0.123830
    2015-01-01 04:29:59    0.127599
    2015-01-01 05:29:59    0.052224
    2015-01-01 06:30:00   -0.011306
    2015-01-01 07:29:59    0.086143
    2015-01-01 08:29:59   -0.088835
    2015-01-01 09:30:00   -0.084528
    2015-01-01 10:29:59    0.082912
    2015-01-01 11:29:59    0.540007
    2015-01-01 12:30:00    0.062992
    2015-01-01 13:29:59    0.791436
    2015-01-01 14:29:59    0.220202
    2015-01-01 15:30:00   -0.008076
    2015-01-01 16:29:59    0.062992
    2015-01-01 17:29:59    0.386565
    2015-01-01 18:30:00    0.272965
    2015-01-01 19:29:59    0.078067
    2015-01-01 20:29:59    0.375259
    2015-01-01 21:30:00    0.059223
    2015-01-01 22:29:59    0.164209
    2015-01-01 23:29:59   -0.025843
    2015-01-02 00:30:00    0.074836
    2015-01-02 01:29:59    0.159902
    2015-01-02 02:29:59    0.003769
    2015-01-02 03:30:00    0.050070
    2015-01-02 04:29:59    0.156134
    2015-01-02 05:29:59   -0.015613
                             ...   
    2017-12-23 15:30:00    0.504355
    2017-12-23 16:29:59    0.395655
    2017-12-23 17:29:59    0.259811
    2017-12-23 18:30:00    0.258700
    2017-12-23 19:29:59    0.259792
    2017-12-23 20:29:59    0.211566
    2017-12-23 21:30:00    0.296822
    2017-12-23 22:29:59    0.158973
    2017-12-23 23:29:59    0.048703
    2017-12-24 00:30:00    0.103658
    2017-12-24 01:29:59    0.226225
    2017-12-24 02:29:59    0.145462
    2017-12-24 03:30:00    0.081840
    2017-12-24 04:29:59    0.186278
    2017-12-24 05:29:59    0.137102
    2017-12-24 06:30:00    0.192551
    2017-12-24 07:29:59    0.201115
    2017-12-24 08:29:59    0.364645
    2017-12-24 09:30:00    0.375183
    2017-12-24 10:29:59    0.947353
    2017-12-24 11:29:59    0.321736
    2017-12-24 12:30:00    0.601246
    2017-12-24 13:29:59    0.970577
    2017-12-24 14:29:59    0.172226
    2017-12-24 15:30:00    0.161048
    2017-12-24 16:29:59    0.138531
    2017-12-24 17:29:59    0.099212
    2017-12-24 18:30:00    0.186739
    2017-12-24 19:29:59    0.194889
    2017-12-31 23:29:59    0.750785
    Length: 17466, dtype: float64
    filename: CH0001G.20010101000000.20180321102615.nephelometer..aerosol.1y.1h.CH02L_TSI_3563_JFJ_dry.CH02L_Neph_3563.lev2.nas;CH0001G.20100101000000.20180321102615.nephelometer..aerosol.1y.1h.CH02L_TSI_3563_JFJ_dry.CH02L_Neph_3563.lev2.nas;CH0001G.20060101000000.20180321102615.nephelometer..aerosol.1y.1h.CH02L_TSI_3563_JFJ_dry.CH02L_Neph_3563.lev2.nas;CH0001G.20040101000000.20180321102615.nephelometer..aerosol.1y.1h.CH02L_TSI_3563_JFJ_dry.CH02L_Neph_3563.lev2.nas;CH0001G.20080101000000.20180321102615.nephelometer..aerosol.1y.1h.CH02L_TSI_3563_JFJ_dry.CH02L_Neph_3563.lev2.nas;CH0001G.20050101000000.20180321102615.nephelometer..aerosol.1y.1h.CH02L_TSI_3563_JFJ_dry.CH02L_Neph_3563.lev2.nas;CH0001G.20070101000000.20180321102615.nephelometer..aerosol.1y.1h.CH02L_TSI_3563_JFJ_dry.CH02L_Neph_3563.lev2.nas;CH0001G.20110101000000.20180321102615.nephelometer..aerosol.1y.1h.CH02L_TSI_3563_JFJ_dry.CH02L_Neph_3563.lev2.nas;CH0001G.20030101000000.20180321102615.nephelometer..aerosol.1y.1h.CH02L_TSI_3563_JFJ_dry.CH02L_Neph_3563.lev2.nas;CH0001G.20150101000000.20180321103020.nephelometer..aerosol.1y.1h.CH02L_Ecotech_Aurora3000_JFJ_dry.CH02L_Neph_Aurora3000.lev2.nas;CH0001G.20170101000000.20180320151431.nephelometer..aerosol.1y.1h.CH02L_TSI_3563_JFJ_dry.CH02L_Neph_3563.lev2.nas;CH0001G.20160101000000.20180321102615.nephelometer..aerosol.1y.1h.CH02L_TSI_3563_JFJ_dry.CH02L_Neph_3563.lev2.nas;CH0001G.20000101000000.20181031145000.nephelometer..aerosol.1y.1h.CH02L_IN3563.CH02L_backscat_coef.lev2.nas;CH0001G.20140101000000.20180321102615.nephelometer..aerosol.1y.1h.CH02L_TSI_3563_JFJ_dry.CH02L_Neph_3563.lev2.nas;CH0001G.20020101000000.20180321102615.nephelometer..aerosol.1y.1h.CH02L_TSI_3563_JFJ_dry.CH02L_Neph_3563.lev2.nas;CH0001G.20090101000000.20180321102615.nephelometer..aerosol.1y.1h.CH02L_TSI_3563_JFJ_dry.CH02L_Neph_3563.lev2.nas;CH0001G.20120101000000.20180321102615.nephelometer..aerosol.1y.1h.CH02L_TSI_3563_JFJ_dry.CH02L_Neph_3563.lev2.nas;CH0001G.20130101000000.20180321102615.nephelometer..aerosol.1y.1h.CH02L_TSI_3563_JFJ_dry.CH02L_Neph_3563.lev2.nas;CH0001G.19980101000000.20181031145000.nephelometer..aerosol.1y.1h.CH02L_IN3563.CH02L_backscat_coef.lev2.nas;CH0001G.19960101000000.20181031145000.nephelometer..aerosol.1y.1h.CH02L_IN3563.CH02L_backscat_coef.lev2.nas;CH0001G.20170101000000.20180320151536.nephelometer..aerosol.1y.1h.CH02L_Ecotech_Aurora3000_JFJ_dry.CH02L_Neph_Aurora3000.lev2.nas;CH0001G.19990101000000.20181031145000.nephelometer..aerosol.1y.1h.CH02L_IN3563.CH02L_backscat_coef.lev2.nas;CH0001G.20150101000000.20180321102615.nephelometer..aerosol.1y.1h.CH02L_TSI_3563_JFJ_dry.CH02L_Neph_3563.lev2.nas;CH0001G.20160101000000.20180321103020.nephelometer..aerosol.1y.1h.CH02L_Ecotech_Aurora3000_JFJ_dry.CH02L_Neph_Aurora3000.lev2.nas;CH0001G.19970101000000.20181031145000.nephelometer..aerosol.1y.1h.CH02L_IN3563.CH02L_backscat_coef.lev2.nas;CH0001G.19950101000000.20181031145000.nephelometer..aerosol.1y.1h.CH02L_IN3563.CH02L_backscat_coef.lev2.nas
    station_id: None
    station_name: Jungfraujoch
    instrument_name: TSI_3563_JFJ_dry;Ecotech_Aurora3000_JFJ_dry;IN3563
    PI: Baltensperger, Urs; Weingartner, Ernest;Bukowiecki, Nicolas
    country: None
    ts_type: hourly
    latitude: 46.5475
    longitude: 7.985
    altitude: 3580.0
    data_id: EBASMC
    dataset_name: None
    data_product: None
    data_version: None
    data_level: None
    revision_date (list, 3 items)
       [numpy.datetime64('2018-03-21T00:00:00')
        numpy.datetime64('2018-03-20T00:00:00')    numpy.datetime64('2018-10-31T00:00:00')]
    
    ts_type_src: hourly
    
    Data arrays
    .................
    dtime (array, 197089 items)
       [numpy.datetime64('1995-07-08T23:00:00.000000000')
        numpy.datetime64('1995-07-09T00:00:00.000000000')
        ...
        numpy.datetime64('2017-12-31T22:00:00.000000000')
        numpy.datetime64('2017-12-31T23:00:00.000000000')]
    
    Pandas Series
    .................
    scatc550aer (Series, 197089 items)


And plot…

.. code:: ipython3

    ax = merged.plot_timeseries('scatc550aer')
    merged.plot_timeseries('scatc550aer', freq='daily', ax=ax)
    merged.plot_timeseries('scatc550aer', freq='monthly', lw=3, ax=ax)
    merged.plot_timeseries('scatc550aer', freq='yearly', ls='none', marker='o', ms=10, ax=ax);



.. image:: add04_stationdata_merging/add04_stationdata_merging_23_0.png


Comment for convenience….
^^^^^^^^^^^^^^^^^^^^^^^^^

Actually, in the default setup you do not really need to think about all
this. As you might have recognised, when creating the list of
``StationData`` objects from the ``UngriddedData`` object (using method
``to_station_data``) we parsed the argument ``merge_if_multi=False``.

The default here is ``True``, so you can just go ahead and do:

.. code:: ipython3

    data.to_station_data('Jungfraujoch', 'scatc550aer').plot_timeseries('scatc550aer')




.. parsed-literal::

    <matplotlib.axes._subplots.AxesSubplot at 0x7fec9a5bfcc0>




.. image:: add04_stationdata_merging/add04_stationdata_merging_25_1.png


What’s happening here is, that ``to_station_data`` internally creates a
list of ``StationData`` objects and uses the above illustrated method
``merge_station_data`` at the end if the input argument
``merge_if_multi=True``.

What about overlapping data ??
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In some situations, there may be overlapping conflicts when merging
multiple time series into one long time-series. In the following, we
illustrate how these overlaps are handled if they occur.

The method ``merge_station_data`` that is illustrated above has some
features to handle overlapping data and in any case, all overlaps that
were detected are stored in the ``overlap`` attribute of the merged
``StationData`` object. Let’s check first if there are any overlaps in
the Jungfraujoch data:

.. code:: ipython3

    merged.overlap




.. parsed-literal::

    BrowseDict([('scatc550aer', 2015-01-01 00:30:00    0.068376
                 2015-01-01 01:29:59    0.255198
                 2015-01-01 02:29:59   -0.284809
                 2015-01-01 03:30:00    0.123830
                 2015-01-01 04:29:59    0.127599
                 2015-01-01 05:29:59    0.052224
                 2015-01-01 06:30:00   -0.011306
                 2015-01-01 07:29:59    0.086143
                 2015-01-01 08:29:59   -0.088835
                 2015-01-01 09:30:00   -0.084528
                 2015-01-01 10:29:59    0.082912
                 2015-01-01 11:29:59    0.540007
                 2015-01-01 12:30:00    0.062992
                 2015-01-01 13:29:59    0.791436
                 2015-01-01 14:29:59    0.220202
                 2015-01-01 15:30:00   -0.008076
                 2015-01-01 16:29:59    0.062992
                 2015-01-01 17:29:59    0.386565
                 2015-01-01 18:30:00    0.272965
                 2015-01-01 19:29:59    0.078067
                 2015-01-01 20:29:59    0.375259
                 2015-01-01 21:30:00    0.059223
                 2015-01-01 22:29:59    0.164209
                 2015-01-01 23:29:59   -0.025843
                 2015-01-02 00:30:00    0.074836
                 2015-01-02 01:29:59    0.159902
                 2015-01-02 02:29:59    0.003769
                 2015-01-02 03:30:00    0.050070
                 2015-01-02 04:29:59    0.156134
                 2015-01-02 05:29:59   -0.015613
                                          ...   
                 2017-12-23 15:30:00    0.504355
                 2017-12-23 16:29:59    0.395655
                 2017-12-23 17:29:59    0.259811
                 2017-12-23 18:30:00    0.258700
                 2017-12-23 19:29:59    0.259792
                 2017-12-23 20:29:59    0.211566
                 2017-12-23 21:30:00    0.296822
                 2017-12-23 22:29:59    0.158973
                 2017-12-23 23:29:59    0.048703
                 2017-12-24 00:30:00    0.103658
                 2017-12-24 01:29:59    0.226225
                 2017-12-24 02:29:59    0.145462
                 2017-12-24 03:30:00    0.081840
                 2017-12-24 04:29:59    0.186278
                 2017-12-24 05:29:59    0.137102
                 2017-12-24 06:30:00    0.192551
                 2017-12-24 07:29:59    0.201115
                 2017-12-24 08:29:59    0.364645
                 2017-12-24 09:30:00    0.375183
                 2017-12-24 10:29:59    0.947353
                 2017-12-24 11:29:59    0.321736
                 2017-12-24 12:30:00    0.601246
                 2017-12-24 13:29:59    0.970577
                 2017-12-24 14:29:59    0.172226
                 2017-12-24 15:30:00    0.161048
                 2017-12-24 16:29:59    0.138531
                 2017-12-24 17:29:59    0.099212
                 2017-12-24 18:30:00    0.186739
                 2017-12-24 19:29:59    0.194889
                 2017-12-31 23:29:59    0.750785
                 Length: 17466, dtype: float64)])



Apparently, there is. You can check out these data (in comparison with
the retrieved time series) as follows:

.. code:: ipython3

    merged.plot_timeseries('scatc550aer', add_overlaps=True);



.. image:: add04_stationdata_merging/add04_stationdata_merging_30_0.png


How to prioritise certain stations from others, when deciding what goes into overlap and what into the final timeseries?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The method ``merge_station_data`` provides a bunch of options to handle
that. Things do not be written twice so please read the docstring of the
method:

.. code:: ipython3

    help(pya.helpers.merge_station_data)


.. parsed-literal::

    Help on function merge_station_data in module pyaerocom.helpers:
    
    merge_station_data(stats, var_name, pref_attr=None, sort_by_largest=True, fill_missing_nan=True, **add_meta_keys)
        Merge multiple StationData objects (from one station) into one instance
        
        Note
        ----
        - all input :class:`StationData` objects need to have same attributes       ``station_name``, ``latitude``, ``longitude`` and ``altitude``
        
        Parameters
        ----------
        stats : list
            list containing :class:`StationData` objects (note: all of these 
            objects must contain variable data for the specified input variable)
        var_name : str
            data variable name that is to be merged
        pref_attr 
            optional argument that may be used to specify a metadata attribute
            that is available in all input :class:`StationData` objects and that
            is used to order the input stations by relevance. The associated values
            of this attribute need to be sortable (e.g. revision_date). This is 
            only relevant in case overlaps occur. If unspecified the relevance of 
            the stations is sorted based on the length of the associated data 
            arrays.
        sort_by_largest : bool
            if True, the result from the sorting is inverted. E.g. if 
            ``pref_attr`` is unspecified, then the stations will be sorted based on
            the length of the data vectors, starting with the shortest, ending with
            the longest. This sorting result will then be inverted, if 
            ``sort_by_largest=True``, so that the longest time series get's highest
            importance. If, e.g. ``pref_attr='revision_date'``, then the stations 
            are sorted by the associated revision date value, starting with the 
            earliest, ending with the latest (which will also be inverted if 
            this argument is set to True)
        fill_missing_nan : bool
            if True, the resulting time series is filled with NaNs. NOTE: this 
            requires that information about the temporal resolution (ts_type) of
            the data is available in each of the StationData objects.
    


In particular, ``pref_attr`` and ``sort_by_largest`` are relevant here.

**NOTE**: if ``pref_attr`` is unspecified, then the stations are sorted
based on the number of valid measurement points for the input variable.
This was done in the merged time series that we retrieved above.

Now, in the following, let’s not use the number of available data points
(to sort the stations by relevance) but prefer stations that have a more
recent data revision date.

.. code:: ipython3

    try:
        merged_pref_awesomeness = pya.helpers.merge_station_data(stats, 'scatc550aer', pref_attr='awesomeness')
    except pya.exceptions.MetaDataError as e:
        print('Failed merging, error: {}'.format(repr(e)))


.. parsed-literal::

    Failed merging, error: MetaDataError('Cannot sort station relevance by attribute awesomeness. At least one of the input stations does not contain this attribute',)


Unfortunately, the ``StationData`` objects do not contain an attribute
``awesomeness`` by which we could sort. Let’s go with ``revision_date``
instead:

.. code:: ipython3

    # recompute stations, since we overwrote one above
    stats = data.to_station_data('Jungfraujoch', 'scatc550aer', merge_if_multi=False)
    merged_pref_recent_revision = pya.helpers.merge_station_data(stats, 'scatc550aer', pref_attr='revision_date')

.. code:: ipython3

    merged_pref_recent_revision.plot_timeseries('scatc550aer', add_overlaps=True)




.. parsed-literal::

    <matplotlib.axes._subplots.AxesSubplot at 0x7fec99f95438>




.. image:: add04_stationdata_merging/add04_stationdata_merging_37_1.png


Let’s see if there is any difference to the previous method (resample to
daily resolution):

.. code:: ipython3

    ax = merged.overlap['scatc550aer'].resample('D').mean().plot(style='x', label='Overlaps (prefer longer timeseries)',
                                                                 figsize=(20, 8))
    
    merged_pref_recent_revision.overlap['scatc550aer'].resample('D').mean().plot(style='o', 
                                                                                 label='Overlaps (prefer more recent)',
                                                                                 ax=ax, markerfacecolor='none')
    ax.legend();



.. image:: add04_stationdata_merging/add04_stationdata_merging_39_0.png


As you can see, the merging strategy can make an impact and it is
important to define a reasonable strategy. In this case, it is certainly
more reliable to use the data with the more recent revision date.

.. code:: ipython3

    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(16, 12))
    ax = plt.scatter(merged_pref_recent_revision.overlap['scatc550aer'], 
                     merged.overlap['scatc550aer'], marker='x')



.. image:: add04_stationdata_merging/add04_stationdata_merging_41_0.png

