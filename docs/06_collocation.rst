
Collocating gridded data with discrete observations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This notebook gives an introduction into collocation of gridded data
with observations. Here, AODs of the ECMWF CAMS reanalysis model are
compared with global daily observations from the AeroNet V2 for the
years of XXX-XXX.

.. code:: ipython3

    start=2000
    stop=2018
    
    ts_type = "daily"
    
    model_id = "ECMWF_CAMS_REAN"
    obs
