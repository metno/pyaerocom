API
===

Documentation of the pyaerocom programming interface.

.. note::

	1. The code documentation is far from complete 
	2. For developers: please use the `NumPy docstring standard <http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html>`__. 

Data types and data representation
----------------------------------

.. todo::

	Introduce for main data classes :class:`UngriddedData`, :class:`GriddedData`, :class:`StationData` and :class:`ColocatedData`
	
Gridded data
^^^^^^^^^^^^

.. automodule:: pyaerocom.griddeddata
   :members:
   :undoc-members:

.. _ungriddeddata:

Ungridded data 
^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.ungriddeddata
   :members:
   :undoc-members:

Colocated data
^^^^^^^^^^^^^^^

.. note::

	This module is a beta version and currently more a draft for handling of merged and temorally regularised data objects. It may undergo significant changes in the near future.
	
.. automodule:: pyaerocom.colocateddata
   :members:
   :undoc-members:
   
Other data classes
^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.station
   :members:
   :undoc-members:
   
.. automodule:: pyaerocom.stationdata
   :members:
   :undoc-members:
   
.. automodule:: pyaerocom.vertical_profile
   :members:
   :undoc-members:

Colocation of data
-------------------

This module contains colocation methods (cf. :class:`ColocatedData`)

.. automodule:: pyaerocom.colocation
   :members:
   :undoc-members:
   
.. _reading: 

Data import (io module)
------------------------

.. note::

	All reading routines are part of the :mod:`pyaerocom.io` sub-package (cf. :ref:`io`)

Reading of gridded data
^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.io.readgridded
   :members:
   :undoc-members:
   
Reading of ungridded data
^^^^^^^^^^^^^^^^^^^^^^^^^

Factory class (high level)
""""""""""""""""""""""""""

.. automodule:: pyaerocom.io.readungridded
   :members:
   :undoc-members:

Aeronet
"""""""

.. note::

	The following includes only reading routines that were already shipped to the new API for ungridded data, that is, which are based on the abstract base class :class:`ReadUngriddedBase` (for details see :ref:`ungriddedbase`) and that use the new ungridded data class :class:`UngriddedData` (cf. :ref:`ungriddeddata`).

Aeronet (base template)
++++++++++++++++++++++++

.. automodule:: pyaerocom.io.readaeronetbase
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

Aeronet Version 2
++++++++++++++++++

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

Aeronet Version 3
++++++++++++++++++

.. automodule:: pyaerocom.io.read_aeronet_sunv3
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

.. automodule:: pyaerocom.io.read_aeronet_sdav3
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

.. automodule:: pyaerocom.io.read_aeronet_invv3
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:
   
Further networks
""""""""""""""""

.. automodule:: pyaerocom.io.read_earlinet
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:
   
.. automodule:: pyaerocom.io.read_ebas
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:
   
.. _ungriddedbase:

Low level
"""""""""

.. automodule:: pyaerocom.io.readungriddedbase
   :members:
   :undoc-members:
   
EBAS I/O (low level)
"""""""""""""""""""""

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
	above, in Section :ref:`reading`.
	
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
  
Conversion of vertical coordinates
----------------------------------

.. automodule:: pyaerocom.vert_coords
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
   
Site location plots
^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.plot.plotsitelocation
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
