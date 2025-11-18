# Apptainer definition file

This directory contains apptainer definition files to create apptainer containers to run pyaerocom
Please mount data paths and when you start a container like in the following examples.

Beware that the container by default inherits your home directory.

## Examples for the Met infrastructure

### mount the `/lustre/storeB` file system into the container 
```shell
apptainer exec --bind /lustre/storeB:/lustre/storeB pyaerocom.sif pya ppiaccess
```
should return `True`

### mount seperate MyPyaerocom directory `~/MyPyaerocom.apptainer` into the container

```shell

apptainer exec --bind ~/MyPyaerocom.apptainer:/home/${USER}/MyPyaerocom pya --help

```
