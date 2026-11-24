# Apptainer definition file

This directory contains apptainer definition files to create apptainer containers to run pyaerocom
Please mount data paths and when you start a container like in the following examples.

Beware that the container by default inherits your home directory.

## building the container
```shell
apptainer build <path to sif file> suppl/apptainer/pyaerocom.def
```

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

### create cachefiles using the container

```shell
apptainer exec --bind /lustre/storeB:/lustre/storeB --bind ~/MyPyaerocom.apptainer:/home/${USER}/MyPyaerocom ~/tmp/apptainer/pyaerocom.sif pyaerocom_cachegen --vars vmro3 -o EBASMC
```


### check which cache files are available in the container

```shell
apptainer exec --bind /lustre/storeB:/lustre/storeB --bind ~/MyPyaerocom.apptainer:/home/${USER}/MyPyaerocom ~/tmp/apptainer/pyaerocom.sif pya listcache
```

## Running on nird
apptainer is only installed at the nird3 login node at the time of this writing (and on betzy)

The main difference here is that the home directory is not `/home` but `/cluster/home`.

For HYway the standard command line is this
```shell
apptainer exec --bind \ 
/nird/datapeak/NS11106K/HYway/modelling_repository/pyaerocom/MyPyaerocom.apptainer:/cluster/home/${USER}/MyPyaerocom \
--bind \
/nird/datapeak/NS11106K/HYway/modelling_repository/pyaerocom/pyaerocom_data:/lustre/storeB/project/aerocom/aerocom1 \
/nird/datapeak/NS11106K/HYway/modelling_repository/pyaerocom/bin/pyaerocom.sif \
pya listcache
```
