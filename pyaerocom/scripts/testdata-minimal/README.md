# Scripts for test dataset creation of pyaerocom
This directory consists of scripts to create the minimal test dataset needed
for automatic testing and continuous integration of pyaerocom. The scripts need access to Met Norway's 
internal file storage and are therefore
of limited use to the general public. In order to not be forgotten during major updates of pyaerocom
they are included in the main pyaerocom gihub repository anyway.

The minimal test data created from these scripts will usually go to the subdirectory `~/MyPyaerocom/testdata-minimal`
Example model and observation data can be found in sub-directories `modeldata` and `obsdata`, respectively.

At this time only `create_subset_ebas.py` is running with the 
latest version of pyaerocom

## Data usage guidelines

Any data provided in this dataset is solely intended to be used for automatic testing of the pyaerocom software.
The data is generally NOT intended to be downloaded and used. If you download these data for your personal use, the
general data policy terms and restrictions of each provided dataset apply. These will be listed in the following.

### AERONET data
See: [https://aeronet.gsfc.nasa.gov/new_web/data_usage.html](https://aeronet.gsfc.nasa.gov/new_web/data_usage.html)

### EBAS data
See: [https://ebas.nilu.no/](https://ebas.nilu.no/)

Under "Data policy".

### Model data

- TM5 :Courtesy of Twan van Noije (KNMI)

### Satellite data

- MODIS: start with the [MODIS landing page](https://modis.gsfc.nasa.gov/data/)

## Updating testdata for CI
**Note:** The test data has to be updated by hand for CI to pickup the changes!

Howto for that:
```
cd ~/MyPyaerocom
mkdir -p ~/tmp
tar -cvzf ~/tmp/testdata-minimal.tar.gz testdata-minimal
```
The resulting file `~/tmp/testdata-minimal.tar.gz` then needs to be copied to the right place.
Please ask your fellow developers in case you do not know how to do that.


