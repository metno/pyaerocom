|CI|

About
=====

pyaerocom is written and tested for Python >= 3.6 and for unix based systems. It provides tools for processing and plotting of data related to the AeroCom project.

This includes support for reading and processing of modeldata (e.g. AeroCom, EMEP), satellite data (e.g. MODIS, AATSR) and ground based observation datasets (e.g. AERONET, EBAS, EARLINET).
In addition, pyaerocom provides tools for colocation and cross evaluation of different datasets using commonly used statistical metrics such as several  biases, gross-errors, or correlation coefficients.


Main features
^^^^^^^^^^^^^

- Reading routines for many ground based observation databases, such as:

	- `AERONET <https://aeronet.gsfc.nasa.gov/>`_ Sun, SDA and Inversion products.
	- `EBAS database <http://ebas.nilu.no/>`__.
	- `GHOST` dataset (see e.g., `Petetin et al., 2020 <https://acp.copernicus.org/articles/20/11119/2020/acp-20-11119-2020.html>`_ for more information).
	- `EARLINET Lidar network <https://www.earlinet.org/index.php?id=earlinet_homepage>`__.

- Reading routines for level 3 gridded satellite observations, such as:

	- `MODIS Aerosol Product <https://modis.gsfc.nasa.gov/data/dataprod/mod04.php>`__.
	- `CALIPSO CALIOP <https://www-calipso.larc.nasa.gov/>`__ Lidar observations.
	- `ENVISAT AATSR <https://earth.esa.int/web/guest/missions/esa-operational-eo-missions/envisat/instruments/aatsr>`__.

- Data harmonization tools following the `CF conventions <https://cfconventions.org/>`__.
- Intuitive data objects for analysis of gridded data and ungridded (point-cloud) observations.
- Sophisticated colocation routines for model evaluation and intercomparison of observations.
- Interfaces for conversion of data to data types of related data analysis libraries such as `pandas <https://pandas.pydata.org/>`__, `numpy <http://www.numpy.org/>`__, `xarray <http://xarray.pydata.org/en/stable/>`__ or `iris <https://scitools.org.uk/iris/docs/latest/>`__.
- Data visualization tools and interfaces to common plotting libraries such as `matplotlib <https://matplotlib.org/>`__ or `cartopy <https://scitools.org.uk/cartopy/docs/latest/>`__.
- Tools for statistical analysis.
- Toolbox for analysis of trends in time-series.
- Tools to compute ensemble averages from multiple model outputs.
- High-level tools for automated analyses of multi-model and multi-obs inter-comparison studies.

Usage examples
^^^^^^^^^^^^^^

- Processing of data for the new AeroCom `Model Evaluation interface <https://aerocom-evaluation.met.no/>`__.
- Processing and harmonization of observations for `Aerosol Trends interface <https://aerocom-trends.met.no/>`__.
- pyaerocom was used for the model evaluation study by `Gliß et al., 2020 <https://acp.copernicus.org/preprints/acp-2019-1214/>`__.
- pyaerocom was used for the trends analysis by `Mortier et al., 2020 <https://acp.copernicus.org/articles/20/13355/2020/acp-20-13355-2020-discussion.html>`__.

AeroCom
=======

The AeroCom-project (http://aerocom.met.no/) is an open international initiative of scientists interested in the advancement of the understanding of the global aerosol and its impact on climate. A large number of observations (including MODIS, POLDER, MISR, AVHHR, SEAWIFS, TOMS, AATSR, AERONET and surface concentrations) and results from more than 14 global models have been assembled to document and compare state of the art modeling of the global aerosol. A common protocol has been established and models are asked to make use of the AeroCom emission inventories for the year 2000 and preindustrial times. Results are documented via interactive websites which give access to 2D fields and standard comparisons to observations. Regular workshops are held to discuss findings and future directions.

This repository contains the AeroCom python tools which are / will be used to produce the standard AeroCom analyses shown at the AeroCom phase 2 interface (http://aerocom.met.no/cgi-bin/AeroCom/aerocom/surfobs_annualrs.pl)

At this point the tools are co-operational together with the IDL based aerocom-tools that cannot be made public because they use 3rd party libraries with a non GPL compatible license.

Citation
========

If you use pyaerocom for your research and find it useful, please consider citing pyaerocom. DOI's and citation entries are available via Zenodo for recent releases here:

https://zenodo.org/record/4159570#.X8dTdsJ7k5l


Website and code documentation
==============================

The official website including code documentation is hosted here:

http://aerocom.met.no/pyaerocom

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

**NOTE:** this will install the latest released version of pyaerocom, which is the same as distributed via *conda-forge* (see prev. point). However, installation via PyPi does **not** take care of any requirements (see below) but only installs pyaerocom::

	pip install pyaerocom


Installing from source
^^^^^^^^^^^^^^^^^^^^^^

If you use the *conda* packages manager, please make sure to `activate the environment <https://conda.io/docs/user-guide/tasks/manage-environments.html#activating-an-environment>`__ you want to install pyaerocom into. For more information about conda environments, `see here <https://conda.io/docs/user-guide/tasks/manage-environments.html>`__.

Please make sure to install all requirements (see below) before installing pyaerocom from source. You can do that with the provided file pyaerocom_env.yml.

To install pyaerocom from source, please download and extract the `latest release <https://github.com/metno/pyaerocom/releases>`__ (or clone the `repo <https://github.com/metno/pyaerocom/>`__) and install from the top-level directory (that contains a file *setup.py*) using::

	python setup.py install

Alternatively, if you plan to apply local changes to the pyaerocom source code, you may install in development mode::

	python setup.py develop

You may also download and extract (or clone) the `GitHub repo <https://github.com/metno/pyaerocom>`__ to install the very latest (not yet released) version of pyaerocom.


Requirements
============

A list of all requirements is provided in file `pyaerocom_env.yml <https://github.com/metno/pyaerocom/blob/master/pyaerocom_env.yml>`__.

Installing all requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**NOTE:** You can skip this section if you install the latest *conda-forge* release (more infos below under *Installation*).

We recommend using the `Anaconda <https://www.anaconda.com/distribution/>`_ Python 3.7 distribution (or `Miniconda <https://conda.io/en/latest/miniconda.html>`__, if you want to save disk space) and to use the *conda* package manager to install the requirements.

If you use Anaconda as a package manager, you can install all requirements (specified in previous section) into a new environment using the provided *pyaerocom_env.yml* file::

	conda env create -n pya -f pyaerocom_env.yml

This will create a new conda environment called *pya* which can be activated using::

	conda activate pya

Alternatively, you can include the requirements into an existing environment. First, activate the existing environment, and then install the dependencies using::

	conda env update -f=pyaerocom_env.yml


Access to users database
========================

Please follow the instructions provided here, to retrieve access to the AeroCom users database:

https://wiki.met.no/aerocom/data_retrieval

**NOTE**: the users database does not contain any ground based observational data (such as EBAS, AERONET, etc.) but only the AeroCom model data available in the database as well as some gridded level 3 satellite datasets which may be used for model evaluation.
Once you have access to the user database you may mount the file-system locally (e.g. via `sshfs` and register the data-paths you need in pyaerocom, for details see tutorials, more info below).

Getting started
===============

After installing pyaerocom, open your python executable and try to import pyaerocom::

	import pyaerocom as pya

To get started, please checkout the tutorials.

Tutorials (Jupyter notebooks)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A number of tutorial jupyter notebooks can be found in the `pyaerocom-tutorials repo <https://github.com/metno/pyaerocom-tutorials/tree/master>`__.

Remark for Windows users
^^^^^^^^^^^^^^^^^^^^^^^^

pyaerocom is not tested on Windows systems and may only work in parts and thus some features may not work on Windows machines at the moment. In particular, features that rely on and are built upon access to the AeroCom database servers and automatic database path navigation. This includes the automised reading of gridded and ungridded data using either of the pre-defined path infrastuctures (e.g. check out `paths.ini <https://github.com/metno/pyaerocom/blob/master/pyaerocom/data/paths.ini>`__ or `paths_user_server.ini <https://github.com/metno/pyaerocom/blob/master/pyaerocom/data/paths_user_server.ini>`__).
However, you may still define file locations in your Python scripts yourself and use the more low-level features for reading the data. Windows support will be provided soon. Please let us know if you intend to use pyaerocom on a Windows machine so that we can consider adjusting our priorities, or also if you have any questions related to the usage.

.. |CI| image:: https://github.com/metno/pyaerocom/workflows/CI/badge.svg
   :target: https://github.com/metno/pyaerocom/actions
