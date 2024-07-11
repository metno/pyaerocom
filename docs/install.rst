Installation
============

You can install pyaerocom via ``pip``

Install from source into a new virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Installation into a new virtual environment (recommended for machines with newer python version and
binary libraries) named *.venv* via::

	# create and activate new virtual environment
	python3 -m venv --prompt pya .venv
	source .venv/bin/activate

	# update pip
	python3 -m pip install -U pip

	# install pyaerocom on machines with Proj8 or newer
	# e.g. Ubuntu 22.04 LTS (Jammy Jellyfish)
	pip install pyaerocom


Install from source into a conda environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you use the *conda* package manager, please make sure to
`activate the environment <https://conda.io/docs/user-guide/tasks/manage-environments.html#activating-an-environment>`__
you want to install pyaerocom into. For more information about conda environments,
`see here <https://conda.io/docs/user-guide/tasks/manage-environments.html>`__.

Please make sure to install all requirements (see below) before installing pyaerocom from source.
You can do that with the provided file pyaerocom_env.yml.

To install pyaerocom from source, please download and extract the
`latest release <https://github.com/metno/pyaerocom/releases>`__
(or clone the `repo <https://github.com/metno/pyaerocom/>`__) and install from the top-level
directory (that contains a file *pyproject.toml*) using::

	pip install --no-deps .

The `--no-deps` option will ensure that only the pyearocom package is installed, preserving the conda environment.

Alternatively, if you plan to apply local changes to the pyaerocom source code, you may install in
editable mode (i.e. setuptools "develop mode") including the test dependencies::

	pip install --no-deps -e .

You may also download and extract (or clone) the `GitHub repo <https://github.com/metno/pyaerocom>`__
to install the very latest (not yet released) version of pyaerocom. Note, if you install in develop
mode, make sure you do not have pyaerocom installed already in the site packages directory,
check e.g. `conda list pyaerocom`__ .


Install from source into a default environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want PyAerocom in your default installation of python, then you install the latest released version of pyaerocom and its depencencies:
::

	# install pyaerocom on machines with Proj8 or newer
	# e.g. Ubuntu 22.04 LTS (Jammy Jellyfish)
	python3 -m pip install pyaerocom

This type of installation is no longer allowed on newer OS-installations, i.e. Ubuntu 24.04. Use the
installation into a new virtual environment instead.
