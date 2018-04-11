API
===

.. note::

	1. The code documentation is far from complete 
	2. For developers: please use the `NumPy docstring standard <http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html>`__. 
  
Data types and data representation
----------------------------------

Model data
^^^^^^^^^^

.. automodule:: pyaerocom.modeldata
   :members:
   :undoc-members:
   
Observation data 
^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.obsdata
   :members:
   :undoc-members:

Input / Output
--------------

The `:mod:pyaerocom.io` sub-package contains I/O routines of the module.
Most importantly, these include reading routines for different models and
observations.

Reading routines
^^^^^^^^^^^^^^^^^^^^

Reading of model data
"""""""""""""""""""""

.. automodule:: pyaerocom.io.readmodeldata
   :members:
   :undoc-members:
   
Reading of observation data
"""""""""""""""""""""""""""

.. automodule:: pyaerocom.io.readobsdata
   :members:
   :undoc-members:
  
     
I/O supplementary and helpers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.io.utils
   :members:
   :undoc-members:

Regions / Domains
-------------------------

.. automodule:: pyaerocom.region
   :members:
   :undoc-members:

  
Plotting / Visualisation
-------------------------

The :mod:`pyaerocom.plot` package contains algorithms related to data visualisation and plotting

.. automodule:: pyaerocom.plot.mapping
   :members:
   :undoc-members:

Mathematical helpers
--------------------

.. automodule:: pyaerocom.mathutils
   :members:
   :undoc-members:
