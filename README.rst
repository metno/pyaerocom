About
=====

pyaerocom is written and tested for Python >= 3.6 and for unix based systems. pyaerocom provides tools for processing and plotting of data related to the AEROCOM-project.

This includes reading and processing of gridded data (e.g. model or satellite data, e.g. NetCDF files) and ungridded data (e.g. observational data from `AERONET <https://aeronet.gsfc.nasa.gov/>`__ or `EBAS <http://ebas.nilu.no/>`__ networks, e.g. ASCII files) as well as tools for colocation and cross evaluation of different datasets.

Main features
^^^^^^^^^^^^^

- Reading routines for many ground based observation databases, such as:

	- `AERONET <https://aeronet.gsfc.nasa.gov/>`_ Sun, SDA and Inversion products.
	- `EBAS database <http://ebas.nilu.no/>`__.
	- `EARLINET Lidar network <https://www.earlinet.org/index.php?id=earlinet_homepage>`__.
	- Coming soon: `AirBase <https://www.eea.europa.eu/data-and-maps/data/airbase-the-european-air-quality-database-7>`__ database.

- Reading routines for many space-based observations, such as:

	- `MODIS Aerosol Product <https://modis.gsfc.nasa.gov/data/dataprod/mod04.php>`__ (gridded).
	- `CALIPSO CALIOP <https://www-calipso.larc.nasa.gov/>`__ Lidar observations (gridded).
	- `ENVISAT AATSR <https://earth.esa.int/web/guest/missions/esa-operational-eo-missions/envisat/instruments/aatsr>`__.
	- Coming soon: Support for `Sentinel-5P <https://earth.esa.int/web/guest/missions/esa-eo-missions/sentinel-5p>`__ and `aeolus <https://www.esa.int/Our_Activities/Observing_the_Earth/Aeolus>`__ data.

- Access to the AeroCom model database.
- Data objects for analysis of gridded and ungridded (point-cloud) observations.
	- This includes interfaces for conversion of data to data types of related data analysis libraries such as `pandas <https://pandas.pydata.org/>`__, `numpy <http://www.numpy.org/>`__, `xarray <http://xarray.pydata.org/en/stable/>`__ or `iris <https://scitools.org.uk/iris/docs/latest/>`__. 
- Colocation tools for gridded and ungridded datasets.
- Harmonisation of variable and metadata conventions.
- Data visualisation tools and interfaces to common plotting libraries such as `matplotlib <https://matplotlib.org/>`__ or `cartopy <https://scitools.org.uk/cartopy/docs/latest/>`__.
- Tools for statistical analysis.

Usage examples
^^^^^^^^^^^^^^

- Processing and harmonisation of observations for `Aerosol Trends interface <https://aerocom-trends.met.no/>`__.

AeroCom
=======

The AEROCOM-project (http://aerocom.met.no/) is an open international initiative of scientists interested in the advancement of the understanding of the global aerosol and its impact on climate. A large number of observations (including MODIS, POLDER, MISR, AVHHR, SEAWIFS, TOMS, AATSR, AERONET and surface concentrations) and results from more than 14 global models have been assembled to document and compare state of the art modeling of the global aerosol. A common protocol has been established and models are asked to make use of the AEROCOM emission inventories for the year 2000 and preindustrial times. Results are documented via interactive websites which give access to 2D fields and standard comparisons to observations. Regular workshops are held to discuss findings and future directions.

This repository contains the aerocom python tools which are / will be used to produce the standard aerocom analyses shown at the aerocom phase 2 interface (http://aerocom.met.no/cgi-bin/AEROCOM/aerocom/surfobs_annualrs.pl)

At this point the tools are work in progress and will develop into a replacement for the IDL based aerocom-tools that cannot be made public because they use 3rd party libraries with a non GPL compatible license.

Website and code documentation
==============================

The official website including code documentation is hosted here:

http://aerocom.met.no/pyaerocom

if you are not already *here* anyways ;)

Requirements
============

Please see file `pyaerocom_env.yml <https://github.com/metno/pyaerocom/blob/master/pyaerocom_env.yml>`__ in the toplevel directory for a list of all requirements.

Installing all requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We recommend using the `Anaconda <https://www.anaconda.com/distribution/>`_ Python 3.7 distribution (or `Miniconda <https://conda.io/en/latest/miniconda.html>`__, if you want to save disk space) and to use the *conda* package manager to install the requirements.

If you use Anaconda as a package manager, you can install all requirements (specified in previous section) into a new environment using the provided *pyaerocom_env.yml* file::

	conda env create -n pya -f pyaerocom_env.yml

This will create a new conda environment called *pya* which can be activated using::

	conda activate pya

Alternatively, you can include the requirements into an existing environment. First, activate the existing environment, and then install the dependencies using:

	conda env update -f=pyaerocom_env.yml

Installation of pyaerocom
=========================

**NOTE**: Use branch v080DEV for most recent changes. This branch is not yet released and cannot be installed using Option 1. Please install from source if you want the most recent version (Option 2).

You have several options to install pyaerocom, the first one is the easiest, but may not refer to the most recent (non-released) version of pyaerocom. So please check first, which version you are interested in.

Option 1: Installation using conda install
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**NOTE:** This will install the latest release of pyaerocom.

- It hence, may not include the most recent developments.
- Requirements are installed automatically.

If you use *conda* as a package manager, the easiest way to install pyaerocom (and all requirements, see previous section) is to use the build provided in the *nordicesmhub* conda channel::

	conda install -c nordicesmhub -c conda-forge pyaerocom

This will install the latest release of pyaerocom including all requirements. Alternatively, you may install from source as described in the following.

**NOTE**: installation support via conda as described above is quite recent, so please let us know if you run into problems with the installation (best way to do this is by raising an issue `here <https://github.com/metno/pyaerocom/issues>`__).

Option 2: Installing from source
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you use the *conda* packages manager, please make sure to `activate the environment <https://conda.io/docs/user-guide/tasks/manage-environments.html#activating-an-environment>`__ you want to install pyaerocom into. For more information about conda environments, `see here <https://conda.io/docs/user-guide/tasks/manage-environments.html>`__.

Please make sure to install all requirements (see above) before installing pyaerocom from source.

To install pyaerocom from source, please download and extract the `latest release <https://github.com/metno/pyaerocom/releases>`__ (or clone this repository) and install from the toplevel directory (that contains a file *setup.py*) using::

	python setup.py install

Alternatively, if you plan to apply local changes to the pyaerocom source code, you may install in `development mode <>`__::

	python setup.py develop

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

After installing pyaerocom, open your python executable and try to import pyaerocom::

	import pyaerocom as pya

To get started, please see `introduction notebook <https://github.com/metno/pyaerocom/blob/master/notebooks/tut00_get_started.ipynb>`__.

**NOTE:** pyaerocom requires access to the AeroCom database located on servers of the Norwegian Meteorological Institute.

The directory *notebooks* contains introduction tutorials for many features of pyaerocom. Note that, for now, you have to be connected to the METNO servers which
contain the example data used in the notebooks. This is `planned to be updated soon <https://github.com/metno/pyaerocom/issues/22>`__ so that the notebooks are based on a publicly available example dataset.

Remark for Windows users
^^^^^^^^^^^^^^^^^^^^^^^^

pyaerocom has only been tested on macOS and other linux systems (Ubuntu). Many high-level features won't work on Windows machines at the moment, that is, features that rely on and are built upon access to the AEROCOM database servers and automatic database path navigation. In particular, this includes the automised reading of gridded and ungridded data using the either of the pre-defined path infrastuctures (e.g. check out `paths.ini <https://github.com/metno/pyaerocom/blob/master/pyaerocom/data/paths.ini>`__ or `paths_user_server.ini <https://github.com/metno/pyaerocom/blob/master/pyaerocom/data/paths_user_server.ini>`__).
However, you may still define file locations in your Python script yourself yourself and use the more low-level features for reading the data. Windows support will be provided soon. Please let us know if you intend to use pyaerocom on a Windows machine so that we can consider adjusting our priorities, or also if you have any questions related to the usage.
