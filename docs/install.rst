Installation
============

You can install PyAerocom via pip

If you want PyAerocom in your default installation of python, then you install the latest released version of pyaerocom and its depencencies:
::

	# install pyaerocom on machines with Proj8 or newer
	# e.g. Ubuntu 22.04 LTS (Jammy Jellyfish)
	python3 -m pip install pyaerocom

Or into a new virtual environment (recommended) named *.venv* via::

	# create and activate new virtual environment
	python3 -m venv --prompt pya .venv
	source .venv/bin/activate

	# update pip
	python3 -m pip install -U pip

	# install pyaerocom on machines with Proj8 or newer
	# e.g. Ubuntu 22.04 LTS (Jammy Jellyfish)
	pip install pyaerocom


