Example configuration files for AeroVal
=======================================

This section provides some example setup files for AeroVal evaluations with
detailed explanations of the setup parameters. A configuration could be run as the following:: 
    
    python cfg_example1.py

The code blocks below are the Python configuruation files *cfg_examples_example1.py* and *sample_gridded_io_aux.py*.

Example 1: NorESM, CAMS reanalysis against AERONET
---------

NorESM2 and CAMS reanalysis vs AERONET and merged satellite AOD dataset.

.. literalinclude:: _static/aeroval/cfg_examples_example1.py

Example IO aux file for model reading
-------------------------------------

.. literalinclude:: _static/aeroval/sample_gridded_io_aux.py


Example for pm ratios compared to EMEP model data
---------------------

.. literalinclude:: _static/aeroval/sample_pm_ratios.py

