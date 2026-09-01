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

The `--no-deps` option will ensure that only the pyaerocom package is installed, preserving the conda environment.

Alternatively, if you plan to apply local changes to the pyaerocom source code, you may install in
editable mode (i.e. setuptools "develop mode") including the test dependencies::

	pip install --no-deps -e .

You may also download and extract (or clone) the `GitHub repo <https://github.com/metno/pyaerocom>`__
to install the very latest (not yet released) version of pyaerocom. Note, if you install in develop
mode, make sure you do not have pyaerocom installed already in the site packages directory,
check e.g. ``conda list pyaerocom`` .


Install from source into a default environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want PyAerocom in your default installation of python, then you install the latest released version of pyaerocom and its dependencies:
::

	# install pyaerocom on machines with Proj8 or newer
	# e.g. Ubuntu 22.04 LTS (Jammy Jellyfish)
	python3 -m pip install pyaerocom

This type of installation is no longer allowed on newer OS-installations, i.e. Ubuntu 24.04. Use the
installation into a new virtual environment instead.

Use PyAerocom in an Apptainer container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following definition file will create a container with Python 3.12 and the latest pyaerocom installation::

    BootStrap: docker
    From: python:3.12

    %post
       apt -y update
       apt -y upgrade
       pip install pyaerocom
       pip install pyaro-readers

    %environment
       export LC_ALL=C

    %labels
        Author JanG

To create the container, run the command::

    apptainer build pyaerocom_python3.12.sif <name of definition file>

To add data, you need to mount data paths using apptainer's ``--bind`` option like ::

    apptainer shell --bind /lustre/storeB:/lustre/storeB pyaerocom_python3.12.sif

To check, if the container works as expected you can run the following command::

    apptainer exec --bind /lustre/storeB:/lustre/storeB pyaerocom_python3.12.sif pya --help

Which should return the following::

     Usage: pya [OPTIONS] COMMAND [ARGS]...

    🦄 Pyaerocom Command Line Interface

    ╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ --version             -V                                                                                                                                                                                        │
    │ --install-completion            Install completion for the current shell.                                                                                                                                       │
    │ --show-completion               Show completion for the current shell, to copy it or customize the installation.                                                                                                │
    │ --help                          Show this message and exit.                                                                                                                                                     │
    ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ browse          Browse database (e.g., browse <DATABASE>)                                                                                                                                                       │
    │ clearcache      Delete cached data objects                                                                                                                                                                      │
    │ listcache       List cached data objects                                                                                                                                                                        │
    │ ppiaccess       Check if MET Norway's PPI can be accessed                                                                                                                                                       │
    │ aeroval         Run an AeroVal experiment as described in a json config file                                                                                                                                    │
    │ getsampledata   Downloads a minimal sample dataset.                                                                                                                                                             │
    │ init            init ~/MyPyaerocom directory and copy the default paths.ini there                                                                                                                               │
    ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

To run the container based python interpreter that has pyaerocom installed just run::

    apptainer exec --bind /lustre/storeB:/lustre/storeB pyaerocom_python3.12.sif python

To run an aeroval analysis via the container please use (for python config files)::

    apptainer exec --bind /lustre/storeB:/lustre/storeB pyaerocom_python3.12.sif python <aeroval_config>.py

or (for json config files)::

    apptainer exec --bind /lustre/storeB:/lustre/storeB pyaerocom_python3.12.sif pya aeroval <aeroval_config>.json


Change the default paths
^^^^^^^^^^^^^^^^^^^^^^^^

pyaerocom searches in ``~/MyPyaerocom`` for a file named ``paths.ini`` and uses that instead of the default
one in ``data/`` in the pyaerocom installation directory (or at
<https://github.com/metno/pyaerocom/blob/main-dev/pyaerocom/data/paths.ini>).

To change paths, just run the command ``pya init`` and  change paths to your needs with your favorite editor.

For information: It happens that the pyaerocom developers add entries to the default ``paths.ini`` file. If that
happens. pyaerocom will add the additional lines to a user specific ``paths.ini``. Due to technical reasons, that means
that all keywords in the file are converted to lower case characters and that comments are removed. The lower case
keywords are the standard for Python written ini files.
