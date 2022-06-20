About
============

pyaerocom is written and tested for python >= 3.6 and for unix based systems. It provides tools for processing and plotting of data related to the AeroCom project.

This includes support for reading and processing of modeldata (e.g. AeroCom, EMEP), satellite data (e.g. MODIS, AATSR) and ground based observation datasets (e.g. AERONET, EBAS, EARLINET).
In addition, pyaerocom provides tools for colocation and cross evaluation of different datasets using commonly used statistical metrics such as several  biases, gross-errors, or correlation coefficients.

AeroCom
^^^^^^^

The AeroCom-project (http://aerocom.met.no/) is an open international initiative of scientists interested in the advancement of the understanding of the global aerosol and its impact on climate. A large number of observations (including MODIS, POLDER, MISR, AVHHR, SEAWIFS, TOMS, AATSR, AERONET and surface concentrations) and results from more than 14 global models have been assembled to document and compare state of the art modeling of the global aerosol. A common protocol has been established and models are asked to make use of the AeroCom emission inventories for the year 2000 and preindustrial times. Results are documented via interactive websites which give access to 2D fields and standard comparisons to observations. Regular workshops are held to discuss findings and future directions.

This repository contains the AeroCom python tools which are / will be used to produce the standard AeroCom analyses shown at the AeroCom phase 2 interface (http://aerocom.met.no/cgi-bin/AeroCom/aerocom/surfobs_annualrs.pl)

At this point the tools are co-operational together with the IDL based aerocom-tools that cannot be made public because they use 3rd party libraries with a non GPL compatible license.

Main features
^^^^^^^^^^^^^

- Reading routines for many ground based observation databases, such as:

	- `AERONET <https://aeronet.gsfc.nasa.gov/>`_ Sun, SDA and Inversion products.
	- `EBAS database </>`__.
	- `EEA Air Quality e-Reporting (AQ e-Reporting) <https://www.eea.europa.eu/data-and-maps/data/aqereporting-9>`__.
	- `AirNow <https://www.airnow.gov/about-the-data/>`__.
	- `MarcoPolo <https://www.knmi.nl/kennis-en-datacentrum/project/marcopolo>`__.
	- `GHOST` (Globally Harmonised Observational Surface Treatment) (see e.g., `Petetin et al., 2020 <https://acp.copernicus.org/articles/20/11119/2020/acp-20-11119-2020.html>`_ for more information).

- Reading routines for level 3 gridded satellite observations, such as:

	- `MODIS Aerosol Product <https://modis.gsfc.nasa.gov/data/dataprod/mod04.php>`__.
	- `CALIPSO CALIOP <https://www-calipso.larc.nasa.gov/>`__ Lidar observations.
	- `ENVISAT AATSR <https://earth.esa.int/web/guest/missions/esa-operational-eo-missions/envisat/instruments/aatsr>`__.

- Data harmonization tools following the `CF conventions <https://cfconventions.org/>`__.
- Intuitive data objects for analysis of gridded data and ungridded (point-cloud) observations.
- Sophisticated and flexible colocation routines for model evaluation and intercomparison of observations.
- Interfaces for conversion of data to data types of related data analysis libraries such as `pandas <https://pandas.pydata.org/>`__, `numpy <http://www.numpy.org/>`__, `xarray <http://xarray.pydata.org/en/stable/>`__ or `iris <https://scitools.org.uk/iris/docs/latest/>`__.
- Data visualization tools and interfaces to common plotting libraries such as `matplotlib <https://matplotlib.org/>`__ or `cartopy <https://scitools.org.uk/cartopy/docs/latest/>`__.
- Tools for statistical analysis of model performance.
- Toolbox for analysis of trends in time-series.
- Tools to compute ensemble averages from multiple model outputs.
- High-level tools for automated analyses of multi-model and multi-obs inter-comparison studies.

Usage examples
^^^^^^^^^^^^^^

- Processing of data for the new AeroCom `Model Evaluation interface <https://aerocom-evaluation.met.no/>`__.
- Processing and harmonization of observations for `Aerosol Trends interface <https://aerocom-trends.met.no/>`__.
- pyaerocom was used for the model evaluation study by `Gliß et al., 2020 <https://acp.copernicus.org/preprints/acp-2019-1214/>`__.
- pyaerocom was used for the trends analysis by `Mortier et al., 2020 <https://acp.copernicus.org/articles/20/13355/2020/acp-20-13355-2020-discussion.html>`__.

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
