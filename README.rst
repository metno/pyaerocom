About
=====

Pyaerocom is written and tested for Python >= 3.6 and for unix based systems (Windows users, please information below in Getting started section). Pyaerocom provides tools for processing and plotting of data related to the AEROCOM-project. 

This includes reading and processing of gridded data (e.g. model or satellite data, e.g. NetCDF files) and ungridded data (e.g. observational data from `AERONET <https://aeronet.gsfc.nasa.gov/>`__ or `EBAS <http://ebas.nilu.no/>`__ networks, e.g. ASCII files) as well as tools for colocation and cross evaluation of different datasets.

The AEROCOM-project (http://aerocom.met.no/) is an open international initiative of scientists interested in the advancement of the understanding of the global aerosol and its impact on climate. A large number of observations (including MODIS, POLDER, MISR, AVHHR, SEAWIFS, TOMS, AATSR, AERONET and surface concentrations) and results from more than 14 global models have been assembled to document and compare state of the art modeling of the global aerosol. A common protocol has been established and models are asked to make use of the AEROCOM emission inventories for the year 2000 and preindustrial times. Results are documented via interactive websites which give access to 2D fields and standard comparisons to observations. Regular workshops are held to discuss findings and future directions.

This repository contains the aerocom python tools which are / will be used to produce the standard aerocom analyses shown at the aerocom phase 2 interface (http://aerocom.met.no/cgi-bin/AEROCOM/aerocom/surfobs_annualrs.pl)

At this point the tools are work in progress and will develop into a replacement for the IDL based aerocom-tools that cannot be made public because they use 3rd party libraries with a non GPL compatible license.

Website and code documentation
==============================

The official website including code documentation is hosted here: 

http://aerocom.met.no/pyaerocom

if you are not already *here* anyways ;)

Installation
============

If you use `Anaconda <https://www.continuum.io/downloads>`_ as package manager, the easiest way to install pyaerocom (and all requirements, see below) via the *nordicesmhub* conda channel::

	conda install -c nordicesmhub -c conda-forge pyaerocom

This will install the latest release of pyaerocom. Alternatively, you may install from source as described in the following.

**PLEASE NOTE**: installation support via conda as described above is quite recent, so please let us know if you run into problems with the installation (best way to do this is by raising an issue `here <https://github.com/metno/pyaerocom/issues>`__).

You can skip the following lines and go straight to *Getting started* section if you have installed via conda as described above.

Requirements
============

The following Python packages are required for the installation of pyaerocom. To install the requirements, 
we recommend using `Anaconda <https://www.continuum.io/downloads>`_ as package manager. 

- iris >= 2.0.0
- xarray >= 0.10.8
- pandas >= 0.22.0 (comes with iris)
- cartopy >= 0.16.0 (comes with iris)
- netcdf4 >= 1.4.0 (comes with iris)
- cf_units >= 2.0.1 (comes with iris)
- numpy >= 1.14 (comes with iris)
- matplotlib >= 3.0.1 (**Note**: please avoid matplotlib v3.0.0 due to `this issue <https://github.com/SciTools/cartopy/issues/1120>`__)
- seaborn >= 0.8.1
- **Optional**:
	- geonum (for SRTM access and basic atmospheric calculations, e.g. conversion of pressure to altitude)
	- geopy (for reading Aeolus data)

By installing iris, some of the further listed dependencies will be installed automatically (e.g. numpy, pandas, cf_units, netcdf4 and matplotlib).

Installing requirements using provided *pyaerocom_env.yml* file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you use Anaconda as a package manager, you can install all requirements into a new environment using the provided *pyaerocom_env.yml* file::

	conda env create -f pyaerocom_env.yml

Make sure to `activate the newly created environment <https://conda.io/docs/user-guide/tasks/manage-environments.html#activating-an-environment>`__ before installing pyaerocom.
For more information about conda environments, `see here <https://conda.io/docs/user-guide/tasks/manage-environments.html>`__.
Make sure to have all requirements installed (see prev. section). You may install the requirements using the provided *pyaerocom_env.yml* file as described at the end of the previous section (note that this ONLY installs he requirements and not pyaerocom itself). 

To install pyaerocom, please download and extract the `latest release <https://github.com/metno/pyaerocom/releases>`__ (or clone this repository) and install from source tree folder (that contains a file *setup.py*) either using::

	python setup.py install

You may also download and extract (or clone) the `GitHub repo <https://github.com/metno/pyaerocom>`__ to install the very latest (not yet released) version of pyaerocom.

More detailed installation instructions `can be found here <https://github.com/metno/pyaerocom/blob/master/notebooks/info00_install_detailed.ipynb>`__.

Finally, we recommend installing jupyter (if not already installed in your conda environment)::

   conda install jupyter

Access to users database
========================

Please follow the instructions provided here, to retrieve access to the AEROCOM users database:

https://wiki.met.no/aerocom/data_retrieval

Getting started
===============

To get started, please see `introduction notebook <https://github.com/metno/pyaerocom/blob/master/notebooks/tut00_get_started.ipynb>`__.

Note for Windows users
^^^^^^^^^^^^^^^^^^^^^^^

pyaerocom has only been tested on macOS and other linux systems (Ubuntu). Many high-level features won't work on Windows machines at the moment, that is, features that rely on and are built upon access to the AEROCOM database servers and automatic database path navigation. In particular, this includes the automised reading of gridded and ungridded data using the either of the pre-defined path infrastuctures (e.g. check out `paths.ini <https://github.com/metno/pyaerocom/blob/master/pyaerocom/data/paths.ini>`__ or `paths_user_server.ini <https://github.com/metno/pyaerocom/blob/master/pyaerocom/data/paths_user_server.ini>`__). 
However, you may still define file locations in your Python script yourself yourself and use the more low-level features for reading the data. Windows support will be provided soon. Please let us know if you intend to use pyaerocom on a Windows machine so that we can consider adjusting our priorities, or also if you have any questions related to the usage.
