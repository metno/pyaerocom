Installation
============

You have several options to install pyaerocom, the first one is the easiest, but may not refer to the most recent (non-released) version of pyaerocom. So please check first, which version you are interested in.

Via conda
^^^^^^^^^

**NOTE:** This will install the latest release of pyaerocom.

- It hence, may not include the most recent developments.
- Requirements are installed automatically.

If you use *conda* as a package manager, the easiest way to install pyaerocom (and all requirements, see previous section) is to use the build provided in the *nordicesmhub* conda channel::

	conda install -c conda-forge pyaerocom

This will install the latest release of pyaerocom including all requirements. Alternatively, you may install from source as described in the following.

**NOTE**: installation support via conda as described above is quite recent, so please let us know if you run into problems with the installation (best way to do this is by raising an issue `here <https://github.com/metno/pyaerocom/issues>`__).

Via PyPi
^^^^^^^^

**NOTE:** this will install the latest released version of pyaerocom, which is the same as distributed via *conda-forge* (see prev. point). However, installation via PyPi does **not** take care of any requirements (see below) but only installs pyaerocom::

	pip install pyaerocom


Installing from source
^^^^^^^^^^^^^^^^^^^^^^

If you use the *conda* package manager, please make sure to `activate the environment <https://conda.io/docs/user-guide/tasks/manage-environments.html#activating-an-environment>`__ you want to install pyaerocom into. For more information about conda environments, `see here <https://conda.io/docs/user-guide/tasks/manage-environments.html>`__.

Please make sure to install all requirements (see below) before installing pyaerocom from source. You can do that with the provided file pyaerocom_env.yml.

To install pyaerocom from source, please download and extract the `latest release <https://github.com/metno/pyaerocom/releases>`__ (or clone the `repo <https://github.com/metno/pyaerocom/>`__) and install from the top-level directory (that contains a file *setup.py*) using::

	python setup.py install

Alternatively, if you plan to apply local changes to the pyaerocom source code, you may install in development mode::

	python setup.py develop

You may also download and extract (or clone) the `GitHub repo <https://github.com/metno/pyaerocom>`__ to install the very latest (not yet released) version of pyaerocom.


Requirements
^^^^^^^^^^^^

A list of requirements is provided in file `pyaerocom_env.yml <https://github.com/metno/pyaerocom/blob/master/pyaerocom_env.yml>`__.

Normally, conda will install these requirements along with pyaerocom, however, if you install from source or using pip, you need to install the requirements yourself.

In order to do so, we recommend using the `Anaconda <https://www.anaconda.com/distribution/>`_ Python 3.7 distribution (or `Miniconda <https://conda.io/en/latest/miniconda.html>`__, if you want to save disk space) and to use the *conda* package manager to install the requirements.

With *conda* you can install all requirements (specified in previous section) into a new environment using the *pyaerocom_env.yml* file::

	conda env create -n pya -f pyaerocom_env.yml

This will create a new conda environment called *pya* which can be activated using::

	conda activate pya

Alternatively, you can include the requirements into an existing environment. First, activate the existing environment, and then install the dependencies using::

	conda env update -f=pyaerocom_env.yml
