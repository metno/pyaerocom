Introduction
============

Pyaerocom is written and tested for Python >= 3.6. It provides tools for processing and plotting of data related to the AEROCOM-project.

The AEROCOM-project (http://aerocom.met.no/) is an open international initiative of scientists interested in the advancement of the understanding of the global aerosol and its impact on climate. A large number of observations (including MODIS, POLDER, MISR, AVHHR, SEAWIFS, TOMS, AATSR, AERONET and surface concentrations) and results from more than 14 global models have been assembled to document and compare state of the art modeling of the global aerosol. A common protocol has been established and models are asked to make use of the AEROCOM emission inventories for the year 2000 and preindustrial times. Results are documented via interactive websites which give access to 2D fields and standard comparisons to observations. Regular workshops are held to discuss findings and future directions.

This repository contains the aerocom python tools which are / will be used to produce the standard aerocom analyses shown at the aerocom phase 2 interface (http://aerocom.met.no/cgi-bin/AEROCOM/aerocom/surfobs_annualrs.pl)

At this point the tools are work in progress and will develop into a replacement for the IDL based aerocom-tools that cannot be made public because they use 3rd party libraries with a non GPL compatible license.

Documentation
=============

Documentation can be found here: http://aerocom.met.no/pyaerocom

Requirements
============

We recommend using `Anaconda <https://www.continuum.io/downloads>`_ as package manager. The following packages are required for the installation of pyaerocom.

- iris >= 2.0.0
- xarray >= 0.10.8
- pandas >= 0.22.0 (comes with iris)
- cartopy >= 0.16.0 (comes with iris)
- netcdf4 >= 1.4.0 (comes with iris)
- cf_units >= 2.0.1 (comes with iris)
- numpy >= 1.14 (comes with iris)
- matplotlib >= 2.1.2 and < 3.0.0 (**Note** `this issue <https://github.com/SciTools/cartopy/issues/1120>`__ with latest 3.0.0 update of matplotlib.)
- **Optional**:
	- seaborn >= 0.8.1
	- geonum (for SRTM access and basic atmospheric calculations, e.g. conversion of pressure to altitude)
	- geopy (for reading Aeolus data)

By installing iris, some of the further listed dependencies will be installed automatically (e.g. numpy, pandas, cf_units, netcdf4 and matplotlib).

Installing requirements using provided *environment.yml* file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you use Anaconda as a package manager, you can install all requirements using the *environment.yml* file in the source code. 

Installation
============

Make sure to have all requirements installed (see previous point). Download and extract the `latest release <https://github.com/metno/pyaerocom/releases>`__ and install from source tree folder (that contains a file *setup.py*) either using::

	python setup.py install

or in development mode using::

	python setup.py develop

You may also download and extract (or clone) the `GitHub repo <https://github.com/metno/pyaerocom>`__ to install the very latest (not yet released) version of pyaerocom.

More detailed installation instructions `can be found here <https://github.com/metno/pyaerocom/blob/master/notebooks/info00_install_detailed.ipynb>`__.

Finally, we recommend installing jupyter (if not already installed in your conda environment)::

   conda install jupyter

Getting started
===============

Please see `introduction notebook <https://github.com/metno/pyaerocom/blob/master/notebooks/tut00_get_started.ipynb>`__
