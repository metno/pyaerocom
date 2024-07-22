API of Aeroval tools
====================

Documentation of the pyaerocom AeroVal API, for high level web
processing tools.


Tools for AeroVal experiment setup
----------------------------------

High level analysis setup for AeroVal experiment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.aeroval.setupclasses
   :members:

Specification of observation datasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.aeroval.obsentry
   :members:

Specification of model datasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.aeroval.modelentry
   :members:

Containers for model and observation setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Collection classes to specify a number of model entries and a
number of observation entries for a given AeroVal experiment.

.. automodule:: pyaerocom.aeroval.collections
   :members:

Processing tools
----------------

Experiment processing engine
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: pyaerocom.aeroval.experiment_processor
   :members:

Model maps processing
^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.aeroval.modelmaps_engine
   :members:

Processing of super-observation entries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Super observations refer to merged observation datasets to
increase the number of stations.

.. automodule:: pyaerocom.aeroval.superobs_engine
   :members:

Low-level base classes for processing engines
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.aeroval._processing_base
   :members:

Helpers for processing of auxiliary variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.aeroval.aux_io_helpers
   :members:

Conversion of co-located data to json output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.aeroval.coldatatojson_engine
   :members:

Output management
-----------------

.. automodule:: pyaerocom.aeroval.experiment_output
   :members:

Global settings
----------------

Global defaults
^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.aeroval.glob_defaults
   :members:

Frontend variable naming conventions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.aeroval.varinfo_web
   :members:

High-level utility functions
----------------------------

.. automodule:: pyaerocom.aeroval.utils
   :members:

High-level functions for emep reporting
---------------------------------------

.. automodule:: pyaerocom.aeroval.config.emep.reporting_base
   :members:

Helper modules
--------------

General helper functions
^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.aeroval.helpers
   :members:

Helpers for coldat2json conversion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.aeroval.coldatatojson_helpers
   :members:

Model maps helper functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyaerocom.aeroval.modelmaps_helpers
   :members:
