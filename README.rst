Introduction
============

Pyaerocom is written and tested for Python3.6. It provides tools for processing and plotting of data related to the AEROCOM-project.

The AEROCOM-project (http://aerocom.met.no/) is an open international initiative of scientists interested in the advancement of the understanding of the global aerosol and its impact on climate. A large number of observations (including MODIS, POLDER, MISR, AVHHR, SEAWIFS, TOMS, AATSR, AERONET and surface concentrations) and results from more than 14 global models have been assembled to document and compare state of the art modeling of the global aerosol. A common protocol has been established and models are asked to make use of the AEROCOM emission inventories for the year 2000 and preindustrial times. Results are documented via interactive websites which give access to 2D fields and standard comparisons to observations. Regular workshops are held to discuss findings and future directions.

This repository contains the aerocom python tools which are / will be used to produce the standard aerocom analyses shown at the aerocom phase 2 interface (http://aerocom.met.no/cgi-bin/AEROCOM/aerocom/surfobs_annualrs.pl)

At this point the tools are work in progress and will develop into a replacement for the IDL based aerocom-tools that cannot be made public because they use 3rd party libraries with a non GPL compatible license.

Documentation
=============
Documentation can be found here: http://aerocom.met.no/pyaerocom

Requirements
============

We recommend using `Anaconda <https://www.continuum.io/downloads>`_ as package manager.

.. note:: This list may be incomplete

- iris >= 2.0.0	
- pandas >= 0.22.0
- cartopy >= 0.16.0
- numpy >= 1.14
- matplotlib >= 2.1.2

Installation
============

Download and extract (or clone) the `GitHub repo <https://github.com/metno/pyaerocom>`__ and install from source folder either using::

	python setup.py install
	
or in development mode using::

	python setup.py develop

