API
===

Documentation of the pyaerocom programming interface.

.. note::

	1. The code documentation is far from complete 
	2. For developers: please use the `NumPy docstring standard <http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html>`__. 

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

.. automodule:: pyaerocom.io.readaeronetbase
   :members:
   :undoc-members:
   
.. automodule:: pyaerocom.io.read_aeronet_invv2
   :members:
   :undoc-members:
   
.. automodule:: pyaerocom.io.read_aeronet_sunv2
   :members:
   :undoc-members:

.. automodule:: pyaerocom.io.read_aeronet_sdav3
   :members:
   :undoc-members:
   
Further networks
""""""""""""""""

Nothing to show yet
   
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

  
Data types and data representation
----------------------------------

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

.. _io: 

Further I/O features
--------------------
  
.. note::

	The	:mod:`pyaerocom.io` package also includes data import and reading routines. These are introduced
	above, in Section :ref:`reading`.

File naming conventions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.io.fileconventions
   :members:
   :undoc-members:
   
I/O helper methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.io.helpers
   :members:
   :undoc-members:

Test file access
^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.io.testfiles
   :members:
   :undoc-members:
   
Regions / Domains
-------------------------

.. automodule:: pyaerocom.region
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

Colors etc.
^^^^^^^^^^^

.. automodule:: pyaerocom.plot.config
   :members:
   :undoc-members:

Helpers
-------

General helper methods
^^^^^^^^^^^^^^^^^^^^^^ 

.. automodule:: pyaerocom.helpers
   :members:
   :undoc-members:
   
Mathematical helpers
^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.mathutils
   :members:
   :undoc-members:
