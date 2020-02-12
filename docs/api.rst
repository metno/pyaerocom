API
===

Documentation of the pyaerocom programming interface.


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
   
Colocated data
^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.colocateddata
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
   
Metadata and vocabulary standards
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.metastandards
   :members:
   :undoc-members:
   
Colocation routines
-------------------

Automatic colocation engine
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.colocation_auto
   :members:
   :undoc-members:
   
Low-level colocation methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.colocation
   :members:
   :undoc-members:
   
.. _reading: 

.. note::

	All reading routines are part of the :mod:`pyaerocom.io` sub-package (cf. :ref:`io`)
	
Reading of gridded data
-----------------------

.. automodule:: pyaerocom.io.readgridded
   :members:
   :undoc-members:
   
Reading of ungridded data
-------------------------

The following flowchart illustrates the architecture of ungridded reading in pyaerocom. Below are information about the individual reading classes for each dataset (blue in flowchart), the abstract template base classes the reading classes are based on (dark green) and the factory class :class:`ReadUngridded` (orange) which has registered all individual reading classes. The data classes that are returned by the reading class are indicated in light green. 

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All AERONET reading classes are based on the template :class:`ReadAeronetBase` class which, in turn inherits from :class:`ReadUngriddedBase`.

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
   
AERONET (older versions)
""""""""""""""""""""""""

.. automodule:: pyaerocom.io.read_aeronet_sunv2
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

.. automodule:: pyaerocom.io.read_aeronet_sdav2
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:
   
.. automodule:: pyaerocom.io.read_aeronet_invv2
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

EARLINET
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.io.read_earlinet
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

EBAS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
   
.. _io: 

Further I/O features
--------------------
  
.. note::

	The	:mod:`pyaerocom.io` package also includes all relevant data import and reading routines. These are introduced
	above, in Section Reading.
	
AeroCom database browser
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
   
Regions and  data filtering
----------------------------

Region defintions
^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.region
   :members:
   :undoc-members:

Filter class
^^^^^^^^^^^^

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
   
Conversion of vertical coordinates
----------------------------------

.. automodule:: pyaerocom.vert_coords
   :members:
   :undoc-members:
   
Trends computation
------------------

Trends engine
^^^^^^^^^^^^^

.. automodule:: pyaerocom.trends_engine
   :members:
   :undoc-members:
   
Helper methods
^^^^^^^^^^^^^^

.. automodule:: pyaerocom.trends_helpers
   :members:
   :undoc-members:
   

Plotting / Visualisation
-------------------------

The :mod:`pyaerocom.plot` package contains algorithms related to data visualisation and plotting.

Plotting maps
^^^^^^^^^^^^^

.. automodule:: pyaerocom.plot.mapping
   :members:
   :undoc-members:
   
Scatter plots
^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.plot.plotscatter
   :members:
   :undoc-members:

Time-series plots
^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.plot.plotseries
   :members:
   :undoc-members:   
   
Heatmap plots
^^^^^^^^^^^^^

.. automodule:: pyaerocom.plot.heatmaps
   :members:
   :undoc-members:

Colors etc.
^^^^^^^^^^^

.. automodule:: pyaerocom.plot.config
   :members:
   :undoc-members:

Utils
-----

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
   
Web processing (sub-package: web)
---------------------------------

This sub-package contains high level processing routines that can be used to process AeroCom data for individual web-interfaces, such as the `AeroCom Evaluation <https://aerocom-trends.met.no/evaluation/web/>`__ interface or the `Aerosol trends <https://aerocom-trends.met.no/>`__ interface.

Aerocom Evaluation interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.web.aerocom_evaluation
   :members:
   :undoc-members:

Aerosol Trends interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.web.aerosol_trends
   :members:
   :undoc-members:

Helpers of web-subpackage
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.web.helpers
   :members:
   :undoc-members:
