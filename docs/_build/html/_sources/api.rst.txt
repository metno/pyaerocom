API
===

Documentation of the pyaerocom programming interface.

.. note::

	1. The code documentation is far from complete 
	2. For developers: please use the `NumPy docstring standard <http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html>`__. 
  
Data types and data representation
----------------------------------

Gridded data
^^^^^^^^^^^^

.. automodule:: pyaerocom.griddata
   :members:
   :undoc-members:
   
Ungridded data 
^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.nogriddata
   :members:
   :undoc-members:

Input / Output
--------------

The `:mod:pyaerocom.io` sub-package contains I/O routines of the module.
Most importantly, these include reading routines for different models and
observations.

Reading routines
^^^^^^^^^^^^^^^^^^^^

Reading of gridded data
""""""""""""""""""""""""

.. automodule:: pyaerocom.io.readgrid
   :members:
   :undoc-members:
   
Reading of ungridded data
"""""""""""""""""""""""""

.. automodule:: pyaerocom.io.read_aeronet_sdav2
   :members:
   :undoc-members:
  
.. automodule:: pyaerocom.io.read_aeronet_sunv2
   :members:
   :undoc-members:
     
.. automodule:: pyaerocom.io.read_earlinet
   :members:
   :undoc-members:
   
File naming conventions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.io.fileconventions
   :members:
   :undoc-members:
   
I / O helper methods
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
