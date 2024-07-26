Core API
========

Documentation of the core API of pyaerocom.

Logging
-------

``pyaerocom`` initializes logging automatically on import in the following way.

1. ``info``-messages or worse are logged to ``logs/pyaerocom.log.$PID`` or
   (dynamic feature) the file given in the environment variable ``PYAEROCOM_LOG_FILE``
   - (dynamic feature) these log-files will be deleted after 7 days.
2. ``warning``-messages or worse are also printed on stdout.
   (dynamic feature) Output to stdout is disabled if the script is called non-interactive.

Besides the default records as defined in https://docs.python.org/3/library/logging.html#logrecord-attributes
pyaerocom also adds a special `mem_usage` keyword to be able to detect memory-leaks of the
python process early.

Putting a file with the name ``logging.ini`` in the scripts current working directory will use that
configuration instead of above described default. An example ``logging.ini`` doing about the same as
described above, except for the dynamic features, and enable ``debug`` logging on one package (``pyaerocom.io.ungridded``), is
provided here:

.. code-block:: ini

   [loggers]
   keys=root,pyaerocom-ungridded

   [handlers]
   keys=console,file

   [formatters]
   keys=plain,detailed

   [formatter_plain]
   format=%(message)s

   [formatter_detailed]
   format=%(asctime)s:%(name)s:%(mem_usage)s:%(levelname)s:%(message)s
   datefmt=%F %T

   [handler_console]
   class=StreamHandler
   formatter=plain
   args=(sys.stdout,)
   level=WARN

   [handler_file]
   class=FileHandler
   formatter=detailed
   level=DEBUG
   file_name=logs/pyaerocom.log.%(pid)s
   args=('%(file_name)s', "w")


   [logger_root]
   handlers=file,console
   level=INFO

   [logger_pyaerocom-ungridded]
   handlers=file
   qualname=pyaerocom.io.readungriddedbase
   level=DEBUG
   propagate=0




Data classes
------------

Gridded data
^^^^^^^^^^^^

.. automodule:: pyaerocom.griddeddata
   :members:
   :undoc-members:

Ungridded data
^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.ungriddeddata
   :members:
   :undoc-members:

Co-located data
^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.colocation.colocated_data
   :members:
   :undoc-members:

Station data
^^^^^^^^^^^^

.. automodule:: pyaerocom.stationdata
   :members:
   :undoc-members:

Other data classes
^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.vertical_profile
   :members:
   :undoc-members:

Co-location routines
---------------------

High-level co-location engine
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.colocation.colocator
   :members:

.. automodule:: pyaerocom.colocation.colocation_setup
   :members:

Low-level co-location functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.colocation.colocation_utils
   :members:
   :undoc-members:

.. automodule:: pyaerocom.colocation.colocation_3d
   :members:
   :undoc-members:

Co-locating ungridded observations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.combine_vardata_ungridded
   :members:
   :undoc-members:

.. _reading:

Reading of gridded data
-----------------------

Gridded data specifies any dataset that can be represented and stored on a
regular grid within a certain domain (e.g. lat, lon time), for instance, model
output or level 3 satellite data, stored, for instance, as NetCDF files.
In pyaerocom, the underlying data object is :class:`GriddedData` and
pyaerocom supports reading of such data for different file naming conventions.

Gridded data using AeroCom conventions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.io.readgridded
   :members:
   :undoc-members:

Gridded data using EMEP conventions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.io.read_mscw_ctm
  :members:
  :undoc-members:

Reading of ungridded data
-------------------------

Other than gridded data, ungridded data represents data that is irregularly
sampled in space and time, for instance, observations at different locations
around the globe. Such data is represented in pyaerocom by
`UngriddedData` which is essentially a point-cloud dataset. Reading of
`UngriddedData` is typically specific for different observational
data records, as they typically come in various data formats using various
metadata conventions, which need to be harmonised, which is done during the
data import.

The following flowchart illustrates the architecture of ungridded reading in
pyaerocom. Below are information about the individual reading classes for each
dataset (blue in flowchart), the abstract template base classes the reading
classes are based on (dark green) and the factory class `ReadUngridded`
(orange) which has registered all individual reading classes. The data classes
that are returned by the reading class are indicated in light green.

.. image:: ../suppl/pyaerocom_ungridded_io_flowchart.png
  :width: 800px
  :align: center

ReadUngridded factory class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Factory class that has all reading class for the individual datasets registered.

.. automodule:: pyaerocom.io.readungridded
   :members:
   :undoc-members:

ReadUngriddedBase template class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All ungridded reading routines are based on this template class.

.. automodule:: pyaerocom.io.readungriddedbase
   :members:
   :undoc-members:

AERONET
^^^^^^^^
`Aerosol Robotic Network (AERONET) <https://aeronet.gsfc.nasa.gov/>`_

AERONET base class
""""""""""""""""""

All AERONET reading classes are based on the template :class:`ReadAeronetBase`
class which, in turn inherits from :class:`ReadUngriddedBase`.

.. automodule:: pyaerocom.io.readaeronetbase
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

AERONET Sun (V3)
""""""""""""""""

.. automodule:: pyaerocom.io.read_aeronet_sunv3
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

AERONET SDA (V3)
""""""""""""""""
.. automodule:: pyaerocom.io.read_aeronet_sdav3
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

AERONET Inversion (V3)
""""""""""""""""""""""
.. automodule:: pyaerocom.io.read_aeronet_invv3
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

EARLINET
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
`European Aerosol Research Lidar Network (EARLINET) <https://www.earlinet.org/index.php?id=earlinet_homepage>`_

.. automodule:: pyaerocom.io.read_earlinet
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

EBAS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`EBAS <https://ebas.nilu.no/>`_ is a database with atmospheric measurement data hosted by the `Norwegian Institute for Air Research <https://www.nilu.no/>`_. Declaration of AEROCOM variables in EBAS and assocaited information such as acceptable minimum and maximum values occurs in ``pyaerocom/data/variables.ini`` .

.. automodule:: pyaerocom.io.read_ebas
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

EBAS (low level)
""""""""""""""""

.. automodule:: pyaerocom.io.ebas_nasa_ames
   :members:
   :undoc-members:

.. automodule:: pyaerocom.io.ebas_file_index
   :members:
   :undoc-members:

.. automodule:: pyaerocom.io.ebas_varinfo
   :members:
   :undoc-members:

EEA data
^^^^^^^^

EEA base reader
"""""""""""""""

Reader for European air pollution data from `EEA AqERep files <https://www.eea.europa.eu/data-and-maps/data/aqereporting-9>`_.

.. automodule:: pyaerocom.io.read_eea_aqerep_base
   :members:
   :undoc-members:

EEA E2a product (NRT)
"""""""""""""""""""""

Near realtime EEA data.

.. automodule:: pyaerocom.io.read_eea_aqerep
   :members:
   :undoc-members:

EEA E1a product (QC)
"""""""""""""""""""""

Quality controlled EEA data.

.. automodule:: pyaerocom.io.read_eea_aqerep_v2
   :members:
   :undoc-members:

AirNow data
^^^^^^^^^^^

Reader for `air quality measurements from North America. <https://www.airnow.gov/about-the-data/>`_

.. automodule:: pyaerocom.io.read_airnow
   :members:
   :undoc-members:

MarcoPolo data
^^^^^^^^^^^^^^

Reader for air quality measurements for China from the `EU-FP7 project MarcoPolo <https://www.knmi.nl/kennis-en-datacentrum/project/marcopolo>`_.

.. automodule:: pyaerocom.io.read_marcopolo
   :members:
   :undoc-members:
GHOST
^^^^^
GHOST (Globally Harmonised Observational Surface Treatment) project developed at the Earth Sciences Department of the Barcelona Supercomputing Center (see e.g., `Petetin et al., 2020 <https://acp.copernicus.org/articles/20/11119/2020/acp-20-11119-2020.html>`_ for more information).

.. automodule:: pyaerocom.io.read_ghost
   :members:
   :undoc-members:

.. _io:

Further I/O features
--------------------

.. note::

    The	`pyaerocom.io` package also includes all relevant data import and
    reading routines. These are introduced above, in Section `reading`.

AeroCom database browser
^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.io.aerocom_browser
   :members:
   :undoc-members:

File naming conventions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.io.fileconventions
   :members:
   :undoc-members:

Iris helpers
^^^^^^^^^^^^^

.. automodule:: pyaerocom.io.iris_io
   :members:
   :undoc-members:

.. automodule:: pyaerocom.io.aux_read_cubes
   :members:
   :undoc-members:

Handling of cached ungridded data objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.io.cachehandler_ungridded
   :members:
   :undoc-members:

I/O utils
^^^^^^^^^

.. automodule:: pyaerocom.io.utils
   :members:
   :undoc-members:

I/O helpers
^^^^^^^^^^^^

.. automodule:: pyaerocom.io.helpers
   :members:
   :undoc-members:

Metadata and vocabulary standards
----------------------------------

.. automodule:: pyaerocom.metastandards
  :members:
  :undoc-members:

Variables
---------

Variable collection
^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.variable
  :members:
  :undoc-members:

Variable class
^^^^^^^^^^^^^^

.. automodule:: pyaerocom.variable
  :members:
  :undoc-members:

Variable helpers
^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.variable_helpers
  :members:
  :undoc-members:

Variable name info
^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.varnameinfo
  :members:
  :undoc-members:

Helpers for auxiliary variables
-------------------------------

.. automodule:: pyaerocom.aux_var_helpers
   :members:
   :undoc-members:

Variable categorisations
------------------------

.. automodule:: pyaerocom.var_groups
   :members:
   :undoc-members:

Regions and  data filtering
----------------------------

Region class and helper functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.region
   :members:
   :undoc-members:

Region definitions
^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.region_defs
   :members:
   :undoc-members:

Region filter
^^^^^^^^^^^^^^

.. automodule:: pyaerocom.filter
   :members:
   :undoc-members:

Land / Sea masks
^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.helpers_landsea_masks
   :members:
   :undoc-members:

Time and frequencies
--------------------

Handling of time frequencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.tstype
   :members:
   :undoc-members:

Temporal resampling
^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.time_resampler
   :members:
   :undoc-members:

Global constants
^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.time_config
   :members:
   :undoc-members:

Vertical coordinate support
----------------------------

.. note::

    BETA: most functionality of this module is currently not implemented in
    any of the pyaerocom standard API.

.. automodule:: pyaerocom.vert_coords
   :members:
   :undoc-members:

Trends computation
------------------

Trends engine
^^^^^^^^^^^^^

.. automodule:: pyaerocom.trends_engine
   :members:

Helper methods
^^^^^^^^^^^^^^

.. automodule:: pyaerocom.trends_helpers
   :members:
   :undoc-members:
   :private-members:

Utility functions
-----------------

.. automodule:: pyaerocom.utils
   :members:
   :undoc-members:

Helpers
-------

.. automodule:: pyaerocom.helpers
   :members:
   :undoc-members:

Mathematical helpers
--------------------

.. automodule:: pyaerocom.mathutils
   :members:
   :undoc-members:

Geodesic calculations and topography
------------------------------------

.. automodule:: pyaerocom.geodesy
   :members:
   :undoc-members:

Units and unit conversion
-------------------------

Units helpers in base package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.units_helpers
   :members:
   :undoc-members:

Units helpers in `io` sub-package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.io.helpers_units
  :members:
  :undoc-members:


Plotting / visualisation (sub package `plot`)
----------------------------------------------

The :mod:`pyaerocom.plot` package contains algorithms related to data
visualisation and plotting.

Plotting of maps
^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.plot.mapping
  :members:
  :undoc-members:

Plotting coordinates on maps
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.plot.plotcoordinates
  :members:
  :undoc-members:

Scatter plots
^^^^^^^^^^^^^^

.. automodule:: pyaerocom.plot.plotscatter
  :members:
  :undoc-members:

Heatmap plots
^^^^^^^^^^^^^

.. automodule:: pyaerocom.plot.heatmaps
  :members:
  :undoc-members:


Colors schemes
^^^^^^^^^^^^^^

.. automodule:: pyaerocom.plot.config
  :members:
  :undoc-members:

Plot helper functions
^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.plot.helpers
  :members:
  :undoc-members:

Configuration and global constants
----------------------------------

Basic configuration class
^^^^^^^^^^^^^^^^^^^^^^^^^

Will be initiated on input and is accessible via `pyaerocom.const`.

.. automodule:: pyaerocom.config
   :members:
   :undoc-members:

Config defaults related to gridded data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.grid_io
   :members:
   :undoc-members:

Config details related to observations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.obs_io
   :members:
   :undoc-members:

Molar masses and related helpers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.molmasses
   :members:
   :undoc-members:

Access to minimal test dataset
------------------------------

.. automodule:: pyaerocom.sample_data_access
   :members:
   :undoc-members:

Low-level helper classes and functions
--------------------------------------

.. automodule:: pyaerocom._lowlevel_helpers
   :members:
   :undoc-members:

Custom exceptions
------------------

.. automodule:: pyaerocom.exceptions
   :members:
   :undoc-members:
