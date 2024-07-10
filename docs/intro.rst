About
============

pyaerocom is written and tested for python >= 3.9 and for-unix based systems. It provides tools for processing and plotting of data related to the the AeroTools project at the Norwegian Meteorological institute, which services projects such as the `Copernicus Atmosphere Monitoring Service <https://atmosphere.copernicus.eu/>`_, `EMEP <https://www.emep.int/>`_, `NorESM <https://www.noresm.org/>`_, and `AeroCom <https://aerocom.met.no/>`_.

The AeroTools project has the following mandate:
- Support for projects delivering model evaluation results
- User support for model-evaluation
- Database management of observation data
- Short and long-term development of evaluation tools, including web-pages showing evaluation results

The pyaerocom software is core part of the AeroTools project and therefore it's scope  includes support for reading and processing of modeldata (e.g. AeroCom, EMEP), satellite data (e.g. MODIS, AATSR) and ground based observation datasets (e.g. AERONET, EBAS, EARLINET).
In addition, pyaerocom provides tools for colocation and cross evaluation of different datasets using commonly used statistics such as several biases, gross-errors, or correlation coefficients.


Main features
^^^^^^^^^^^^^

- Reading routines for many ground based observation databases, such as:

	- `AERONET <https://aeronet.gsfc.nasa.gov/>`_ Sun, SDA and Inversion products.
	- `EBAS database <https://ebas.nilu.no/>`__.
	- `EEA Air Quality e-Reporting (AQ e-Reporting) <https://www.eea.europa.eu/data-and-maps/data/aqereporting-9>`__.
	- `AirNow <https://www.airnow.gov/about-the-data/>`__.
	- `China National Envrionmental Monitoring Service (CNEMC) <https://www.cnemc.cn/en/>`__.
	- `ICOS <https://www.icos-cp.eu/>`

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
- Processing of data to display on `AeroVal <https://aeroval.met.no/>`_
- Processing of data for the new AeroCom `Model Evaluation interface <https://aerocom-evaluation.met.no/>`__.
- Processing and harmonization of observations for `Aerosol Trends interface <https://aerocom-trends.met.no/>`__.
- pyaerocom was used for the model evaluation study by `Gliß et al., 2020 <https://acp.copernicus.org/preprints/acp-2019-1214/>`__.
- pyaerocom was used for the trends analysis by `Mortier et al., 2020 <https://acp.copernicus.org/articles/20/13355/2020/acp-20-13355-2020-discussion.html>`__.

.. figure:: biasmaps_fig5_glissetal2021.png

  Bias maps of the AeroCom ensemble median compared to several observation records (Figure 5 from `Gliß et al., 2021 <https://acp.copernicus.org/articles/21/87/2021/acp-21-87-2021.html>`__, processed with pyaerocom)


Access to AeroCom users database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The AeroCom users database contains model diagnostics from all AeroCom phases, ready for analysis.

If you wish to get access to the database, please follow the instructions provided in the following link:

https://wiki.met.no/aerocom/data_retrieval

**NOTE**: the users database does not contain any ground based observational data (such as EBAS, AERONET, etc.) but only the AeroCom model data available in the database as well as some gridded level 3 satellite data which may be used for model evaluation.
Once you have access to the user database you may mount the file-system locally (e.g. via `sshfs` and register the data-paths you need in pyaerocom, for details see tutorials, more info below).


Remark for Windows users
^^^^^^^^^^^^^^^^^^^^^^^^

pyaerocom is not tested on Windows systems and may only work in parts and thus some features may not work on Windows machines at the moment. Please let us know if you intend to use pyaerocom on a Windows machine so that we can consider adjusting our priorities, or also if you have any questions related to the usage.
