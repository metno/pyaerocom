
AEROCOM default regions
~~~~~~~~~~~~~~~~~~~~~~~

This notebook introduces how pyaerocom handles information related to
default regions (e.g. Europe, Asia, ...) as used in the `AEROCOM
interface <http://aerocom.met.no/cgi-bin/AEROCOM/aerocom/surfobs_annualrs.pl>`__.
All default regions are defined in the file
`regions.ini <http://aerocom.met.no/pyaerocom/config_files.html#default-regions>`__.

.. code:: ipython3

    import pyaerocom
    
    print(pyaerocom.region.get_all_default_region_ids())


.. parsed-literal::

    ['WORLD', 'EUROPE', 'ASIA', 'AUSTRALIA', 'CHINA', 'INDIA', 'NAFRICA', 'SAFRICA', 'SAMERICA', 'NAMERICA']


Now load some default regions and print them.

.. code:: ipython3

    europe = pyaerocom.Region("EUROPE")
    asia = pyaerocom.Region("ASIA")
    
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

In the following cell, we create an instance of the ``ModelData`` class
(hich is introduced in more detail in a later tutorial), load some test
data (from the CAMS ECMWF OSUITE dataset), crop it and plot a map of the
results over Europe.

.. code:: ipython3

    data = pyaerocom.ModelData()
    data._init_testdata_default()
    crop = data.crop(region="EUROPE")
    fig = crop.quickplot_map()


.. parsed-literal::

    Rolling longitudes to -180 -> 180 definition



.. image:: 01_intro_regions/01_intro_regions_5_1.png

