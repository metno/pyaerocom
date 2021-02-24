Getting started
===============

After installing pyaerocom, open your python executable and try to import pyaerocom::

	import pyaerocom as pya

To get started, please checkout the tutorials.

Tutorials (Jupyter notebooks)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A number of tutorial jupyter notebooks can be found in the `pyaerocom-tutorials repo <https://github.com/metno/pyaerocom-tutorials/tree/master>`__.

Access to AeroCom users database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The AeroCom users database contains model diagnostics from all AeroCom phases, ready for analysis.

If you wish to get access to the database, please follow the instructions provided in the following link:

https://wiki.met.no/aerocom/data_retrieval

**NOTE**: the users database does not contain any ground based observational data (such as EBAS, AERONET, etc.) but only the AeroCom model data available in the database as well as some gridded level 3 satellite data which may be used for model evaluation.
Once you have access to the user database you may mount the file-system locally (e.g. via `sshfs` and register the data-paths you need in pyaerocom, for details see tutorials, more info below).

Remark for Windows users
^^^^^^^^^^^^^^^^^^^^^^^^

pyaerocom is not tested on Windows systems and may only work in parts and thus some features may not work on Windows machines at the moment. In particular, features that rely on and are built upon access to the AeroCom database servers and automatic database path navigation. This includes the automised reading of gridded and ungridded data using either of the pre-defined path infrastuctures (e.g. check out `paths.ini <https://github.com/metno/pyaerocom/blob/master/pyaerocom/data/paths.ini>`__ or `paths_user_server.ini <https://github.com/metno/pyaerocom/blob/master/pyaerocom/data/paths_user_server.ini>`__).
However, you may still define file locations in your Python scripts yourself and use the more low-level features for reading the data. Windows support will be provided soon. Please let us know if you intend to use pyaerocom on a Windows machine so that we can consider adjusting our priorities, or also if you have any questions related to the usage.
