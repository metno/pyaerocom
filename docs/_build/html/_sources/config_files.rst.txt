Configuration files
-------------------

Variables
^^^^^^^^^

.. literalinclude:: ../pyaerocom/data/variables.ini

.. code-block:: python

	>>> import pyaerocom
	>>> var = pyaerocom.Variable("od550aer")
	>>> print(var)
	pyaeorocom Variable
	Name: od550aer
	Unit: ''
	Value range: 0 - 1.0
	Levels colorbar: [0.0, 0.01, ..., 0.9, 1.0]
	Colorbar ticks: [0.0, 0.02, ..., 0.7, 0.9]
	
Default regions
^^^^^^^^^^^^^^^^

The following file contains all pyaerocom default regions. 
	
.. literalinclude:: ../pyaerocom/data/regions.ini

Each region defined here can easily be loaded as follows using its id. For instance:

.. code-block:: python
	
	>>> import pyaerocom
	>>> region = pyaerocom.Region("EUROPE")
	>>> print(region)
	pyaeorocom Region
	Name: EUROPE
	Longitude range: [-20.0, 70.0]
	Latitude range: [30.0, 80.0]

File conventions
^^^^^^^^^^^^^^^^

The following file contains file naming conventions for data import

.. literalinclude:: ../pyaerocom/data/file_conventions.ini

Each convention defined here can easily be loaded as follows using its id.
For instance:

.. code-block:: python
	
	>>> import pyaerocom
	>>> conf = pyaerocom.io.FileConventionRead(name="aerocom2")
	>>> print(conf)
	pyaeorocom FileConventionRead
	name: aerocom2
	file_sep: .
	year_pos: -2
	var_pos: -3
	ts_pos: -4

Test paths
^^^^^^^^^^

The following file contains paths to test files for different models 
and observations.

.. literalinclude:: ../pyaerocom/data/test_files.ini


Paths and directories
^^^^^^^^^^^^^^^^^^^^^

The following file contains relevant search paths for data import

.. literalinclude:: ../pyaerocom/data/paths.ini

