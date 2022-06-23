Installation
============

You can install pyaerocom via conda, pip or from source.

Via conda
^^^^^^^^^

The easiest way to install pyaerocom and all requirements using conda. You can install pyaerocom into a pre-existing conda environment via::

	conda install -c conda-forge pyaerocom

Or into a new conda environment (recommended) named *pya* via::

	conda create -c conda-forge --name pya pyaerocom

This will install the latest release of pyaerocom including all requirements. Alternatively, you may install via pip or from source as described in the following.


Via pip
^^^^^^^

This will install the latest released version of pyaerocom and its depencencies.
**NOTE** this same pacakge as distributed via *conda-forge* (see prev. point).::

	# install pyaerocom on machines with Proj8 or newer
	# e.g. Ubuntu 22.04 LTS (Jammy Jellyfish)
	python3 -m pip install --use-deprecated=legacy-resolver pyaerocom[proj8]

	# install pyaerocom on machiles with an older version of Proj
	# e.g. Ubuntu 20.04 LTS (Focal Fossa)
	python3 -m pip install --use-deprecated=legacy-resolver pyaerocom[proj-legacy]

Or into a new virtual environment (recommended) named *.venv* via::

	# create and activate new virtual environment
	python3 -m venv --prompt pya .venv
	source .venv/bin/activate

	# update pip
	python3 -m pip install -U pip

	# install pyaerocom on machines with Proj8 or newer
	# e.g. Ubuntu 22.04 LTS (Jammy Jellyfish)
	pip install --use-deprecated=legacy-resolver pyaerocom[proj8]

	# install pyaerocom on machiles with an older version of Proj
	# e.g. Ubuntu 20.04 LTS (Focal Fossa)
	pip install --use-deprecated=legacy-resolver pyaerocom[proj-legacy]


Install from source into a conda environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you use the *conda* package manager, please make sure to `activate the environment <https://conda.io/docs/user-guide/tasks/manage-environments.html#activating-an-environment>`__ you want to install pyaerocom into. For more information about conda environments, `see here <https://conda.io/docs/user-guide/tasks/manage-environments.html>`__.

Please make sure to install all requirements (see below) before installing pyaerocom from source. You can do that with the provided file pyaerocom_env.yml.

To install pyaerocom from source, please download and extract the `latest release <https://github.com/metno/pyaerocom/releases>`__ (or clone the `repo <https://github.com/metno/pyaerocom/>`__) and install from the top-level directory (that contains a file *setup.cfg*) using::

	pip install --no-deps .

The `--no-deps` option will ensure that only the pyearocom package is installed, preserving the conda environment.

Alternatively, if you plan to apply local changes to the pyaerocom source code, you may install in editable mode (i.e. setuptools "develop mode")
including the test rependencies::

	pip install --no-deps -e .

You may also download and extract (or clone) the `GitHub repo <https://github.com/metno/pyaerocom>`__ to install the very latest (not yet released) version of pyaerocom. Note, if you install in develop mode, make sure you do not have pyaerocom installed already in the site packages directory, check e.g. `conda list pyaerocom`.


Requirements for a conda environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A list of requirements is provided in file `pyaerocom_env.yml <https://github.com/metno/pyaerocom/blob/master/pyaerocom_env.yml>`__.

Normally, conda will install these requirements along with pyaerocom, however, if you install from source or using pip, you need to install the requirements yourself.

In order to do so, we recommend using the `Anaconda <https://www.anaconda.com/distribution/>`_ Python 3.8 distribution (or `Miniconda <https://conda.io/en/latest/miniconda.html>`__, if you want to save disk space) and to use the *conda* package manager to install the requirements.

With *conda* you can install all requirements (specified in previous section) into a new environment using the *pyaerocom_env.yml* file::

	conda env create -n pya -f pyaerocom_env.yml

This will create a new conda environment called *pya* which can be activated using::

	conda activate pya

Alternatively, you can include the requirements into an existing environment. First, activate the existing environment, and then install the dependencies using::

	conda env update -f=pyaerocom_env.yml
