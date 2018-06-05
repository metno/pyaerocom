API
===

Documentation of the pyaerocom programming interface.

.. note::

	1. The code documentation is far from complete 
	2. For developers: please use the `NumPy docstring standard <http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html>`__. 

.. _reading: 

Data import (Reading routines)
------------------------------

.. note::

	All reading routines are part of the :mod:`pyaerocom.io` sub-package (cf. :ref:`io`)

Reading of gridded data
^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.io.readgridded
   :members:
   :undoc-members:
   
Reading of ungridded data
^^^^^^^^^^^^^^^^^^^^^^^^^

High-level
""""""""""

.. automodule:: pyaerocom.io.readungridded
   :members:
   :undoc-members:
  
Low-level
"""""""""

.. automodule:: pyaerocom.io.read_aeronet_sunv2
   :members:
   :undoc-members:
     
.. automodule:: pyaerocom.io.read_earlinet
   :members:
   :undoc-members:	
  
Data types and data representation
----------------------------------

Gridded data
^^^^^^^^^^^^

.. automodule:: pyaerocom.griddeddata
   :members:
   :undoc-members:
   
Ungridded data 
^^^^^^^^^^^^^^^^

So far, no class for ungridded data objects has been defined. Coming soon...

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
