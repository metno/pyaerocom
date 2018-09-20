
AEROCOM default regions
~~~~~~~~~~~~~~~~~~~~~~~

This notebook introduces how pya handles information related to default
regions (e.g. Europe, Asia, …) as used in the `AEROCOM
interface <http://aerocom.met.no/cgi-bin/AEROCOM/aerocom/surfobs_annualrs.pl>`__.
All default regions are defined in the file
`regions.ini <http://aerocom.met.no/pya/config_files.html#default-regions>`__.

.. code:: ipython3

    import pyaerocom as pya
    
    print(pya.region.get_all_default_region_ids())


.. parsed-literal::

    2018-09-20 15:31:48,090:WARNING:
    basemap extension library is not installed (or cannot be imported. Some features will not be available


.. parsed-literal::

    Elapsed time init all variables: 0.036505937576293945 s


.. parsed-literal::

    2018-09-20 15:31:48,839:WARNING:
    geopy library is not available. Aeolus data read not enabled


.. parsed-literal::

    Elapsed time init pyaerocom: 1.0629911422729492 s
    ['WORLD', 'EUROPE', 'ASIA', 'AUSTRALIA', 'CHINA', 'INDIA', 'NAFRICA', 'SAFRICA', 'SAMERICA', 'NAMERICA']


Now load some default regions and print them.

.. code:: ipython3

    europe = pya.Region("EUROPE")
    asia = pya.Region("ASIA")
    
    print(europe)
    print()
    print(asia)


.. parsed-literal::

    pyaeorocom Region
    Name: EUROPE
    Longitude range: [-20, 70]
    Latitude range: [30, 80]
    Longitude range (plots): [-20, 70]
    Latitude range (plots): [30, 80]
    
    pyaeorocom Region
    Name: ASIA
    Longitude range: [40, 150]
    Latitude range: [0, 60]
    Longitude range (plots): [40, 150]
    Latitude range (plots): [0, 60]


Load example data and apply region specific crop
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the following cell, we create an instance of the ``GriddedData``
class (hich is introduced in more detail in a later tutorial), load some
test data (from the CAMS ECMWF OSUITE dataset), crop it and plot a map
of the results over Europe.

.. code:: ipython3

    data = pya.GriddedData()
    data._init_testdata_default()
    crop = data.crop(region="EUROPE")
    fig = crop.quickplot_map()


.. parsed-literal::

    /home/jonasg/anaconda3/lib/python3.6/site-packages/iris/fileformats/_pyke_rules/compiled_krb/fc_rules_cf_fc.py:1808: UserWarning: Ignoring netCDF variable 'od550dust' invalid units '~'
      warnings.warn(msg)
    /home/jonasg/anaconda3/lib/python3.6/site-packages/iris/fileformats/_pyke_rules/compiled_krb/fc_rules_cf_fc.py:1808: UserWarning: Ignoring netCDF variable 'od550bc' invalid units '~'
      warnings.warn(msg)
    /home/jonasg/anaconda3/lib/python3.6/site-packages/iris/fileformats/_pyke_rules/compiled_krb/fc_rules_cf_fc.py:1808: UserWarning: Ignoring netCDF variable 'od550oa' invalid units '~'
      warnings.warn(msg)
    /home/jonasg/anaconda3/lib/python3.6/site-packages/iris/fileformats/_pyke_rules/compiled_krb/fc_rules_cf_fc.py:1808: UserWarning: Ignoring netCDF variable 'od550so4' invalid units '~'
      warnings.warn(msg)
    /home/jonasg/anaconda3/lib/python3.6/site-packages/iris/fileformats/_pyke_rules/compiled_krb/fc_rules_cf_fc.py:1808: UserWarning: Ignoring netCDF variable 'od550aer' invalid units '~'
      warnings.warn(msg)
    2018-09-20 15:31:49,186:WARNING:
    File /lustre/storeA/project/aerocom/aerocom1/ECMWF_OSUITE_NRT_test/renamed/aerocom.ECMWF_OSUITE_NRT_test.daily.od550aer.2018.nc contains more than one data field: 0: Dust Aerosol Optical Depth at 550nm / (unknown) (time: 365; latitude: 451; longitude: 900)
    1: Black Carbon Aerosol Optical Depth at 550nm / (unknown) (time: 365; latitude: 451; longitude: 900)
    2: Organic Matter Aerosol Optical Depth at 550nm / (unknown) (time: 365; latitude: 451; longitude: 900)
    3: Sulphate Aerosol Optical Depth at 550nm / (unknown) (time: 365; latitude: 451; longitude: 900)
    4: Dust Aerosol Optical Depth at 550nm / (unknown) (time: 365; latitude: 451; longitude: 900)



.. image:: tut01_intro_regions/tut01_intro_regions_5_1.png

