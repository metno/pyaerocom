|CI|

Introduction
============

pyaerocom is written and tested for python >= 3.6 and for unix based systems. pyaerocom provides tools for processing and plotting of data related to the AeroCom project.
This includes reading and processing of gridded data (e.g. model data or level 3 satellite data) and ungridded data (e.g. observational data from `AERONET <https://aeronet.gsfc.nasa.gov/>`__ or `EBAS <http://ebas.nilu.no/>`__ networks, e.g. ASCII files) as well as low and high-level tools for co-location and cross evaluation of different data-sets.

AeroCom
^^^^^^^^^

The AeroCom-project (http://aerocom.met.no/) is an open international initiative of scientists interested in the advancement of the understanding of the global aerosol and its impact on climate. A large number of observations (including MODIS, POLDER, MISR, AVHHR, SEAWIFS, TOMS, AATSR, AERONET and surface concentrations) and results from more than 14 global models have been assembled to document and compare state of the art modeling of the global aerosol. A common protocol has been established and models are asked to make use of the AeroCom emission inventories for the year 2000 and preindustrial times. Results are documented via interactive websites which give access to 2D fields and standard comparisons to observations. Regular workshops are held to discuss findings and future directions.

Citation
========

If you use pyaerocom for your research and find it useful, please consider citing pyaerocom. DOI's and citation entries are available via Zenodo for recent releases here:

https://zenodo.org/record/4159570#.X8dTdsJ7k5l

Installation
============

You have several options to install pyaerocom, the first one is the easiest, but may not refer to the most recent (non-released) version of pyaerocom. So please check first, which version you are interested in.

Via conda
^^^^^^^^^

**NOTE:** This will install the latest release of pyaerocom.

- It hence, may not include the most recent developments.
- Requirements are installed automatically.

If you use *conda* as a package manager, the easiest way to install pyaerocom (and all requirements, see previous section) is to use the build provided in the *nordicesmhub* conda channel::

	conda install -c conda-forge pyaerocom

This will install the latest release of pyaerocom including all requirements. Alternatively, you may install from source as described in the following.

**NOTE**: installation support via conda as described above is quite recent, so please let us know if you run into problems with the installation (best way to do this is by raising an issue `here <https://github.com/metno/pyaerocom/issues>`__).

Via PyPi
^^^^^^^^

**NOTE:** this will install the latest released version of pyaerocom, which is the same as distributed via *conda-forge* (see prev. point). However, installation via PyPi does **not** take care of any requirements but only installs pyaerocom::

	pip install pyaerocom


Installing from source
^^^^^^^^^^^^^^^^^^^^^^

If you use the *conda* packages manager, please make sure to `activate the environment <https://conda.io/docs/user-guide/tasks/manage-environments.html#activating-an-environment>`__ you want to install pyaerocom into. For more information about conda environments, `see here <https://conda.io/docs/user-guide/tasks/manage-environments.html>`__.

Please make sure to install all requirements before installing pyaerocom from source. You can do that with the provided file pyaerocom_env.yml.

To install pyaerocom from source, please download and extract the `latest release <https://github.com/metno/pyaerocom/releases>`__ (or clone the `repo <https://github.com/metno/pyaerocom/>`__) and install from the top-level directory (that contains a file *setup.py*) using::

	python setup.py install

Alternatively, if you plan to apply local changes to the pyaerocom source code, you may install in development mode::

	python setup.py develop

You may also download and extract (or clone) the `GitHub repo <https://github.com/metno/pyaerocom>`__ to install the very latest (not yet released) version of pyaerocom.


Access to users database
========================

Please follow the instructions provided here, to retrieve access to the AeroCom users database:

https://wiki.met.no/aerocom/data_retrieval

**NOTE**: the users database does not contain any ground based observational data (such as EBAS, AERONET, etc.) but only the AeroCom model data available in the database as well as some gridded level 3 satellite datasets which may be used for model evaluation.

Getting started
===============

After installing pyaerocom, open your python executable and try to import pyaerocom::

	import pyaerocom as pya

To get started, please check out the `tutorials <https://pyaerocom.met.no/pyaerocom-tutorials/index.html>`__. The tutorials can also be `run interactively <https://mybinder.org/v2/gh/metno/pyaerocom-tutorials/master>`__ online using Binder (note that the startup of the binder hub may take a while).

Remark for Windows users
^^^^^^^^^^^^^^^^^^^^^^^^

pyaerocom is not tested on Windows systems and may only work in parts and thus some features may not work on Windows machines at the moment. In particular, features that rely on and are built upon access to the AeroCom database servers and automatic database path navigation. This includes the automised reading of gridded and ungridded data using either of the pre-defined path infrastuctures (e.g. check out `paths.ini <https://github.com/metno/pyaerocom/blob/master/pyaerocom/data/paths.ini>`__ or `paths_user_server.ini <https://github.com/metno/pyaerocom/blob/master/pyaerocom/data/paths_user_server.ini>`__).
However, you may still define file locations in your Python scripts yourself and use the more low-level features for reading the data. Windows support will be provided soon. Please let us know if you intend to use pyaerocom on a Windows machine so that we can consider adjusting our priorities, or also if you have any questions related to the usage.

.. |CI| image:: https://github.com/metno/pyaerocom/workflows/CI/badge.svg
   :target: https://github.com/metno/pyaerocom/actions
