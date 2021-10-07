# pyaerocom version 0.12.0

This release comes with many new features, major improvements and a more 
stable API. Please see the individual points below for major changes.

The notes below summarise the major updates since the release of version [0.
10.0](https://github.com/metno/pyaerocom/releases/tag/v0.10.0). This 
includes the changes that were done in the recent release of version 
[0.11.0](https://github.com/metno/pyaerocom/releases/tag/v0.11.0)), which 
is the last version that officially supports

## Major updates

### **NEW** AeroVal tools

The web processing tools have seen major improvements and the backend has a 
new API, which can be found in the **aeroval** sub-package. Compared to the 
former AeroCom Evaluation tools (**web** sup-package in former releases), 
the new tools are a lot more flexible and support, for instance:

- Processing of time series of statistical parameters.
- Option to calculate seasonal statistics.
- Temporal and spatial correlation in heatmap display.
- Combination of different observation datasets into "superobservations".
- All this is packed into a new modular and intuitive API.

**Follow AeroVal on twitter**: https://twitter.com/AeroVal_MetNo

### **web** sub-package 

- The code under **web** is deprecated and relevant code has been shipped 
  and redesigned into the new **AeroVal** tools (**aeroval** subpackage).
- Processing tools for old trends interface are deprecated, instead trends 
  visualisation is included in the new **aeroval** interface and can be 
  done via the new tools in the **aeroval** subpackage.

### 
### UNSORTED

- EBAS evaluation of individual timestamps to resolve ts_type of NASA Ames 
  file.
- Processing of wet deposition and precipitation.

## Unit conversions

- Automatic detection and correction of implicit deposition units to 
  explicit units, both for model and obs, centralised in 
  [units_helpers.py](https://github.com/metno/pyaerocom/blob/master/pyaerocom/units_helpers.py) module. 
  E.g. if precip is reported mm and if the associated sampling duration is 
  known (e.g. daily), it is corrected to mm d-1. Same applies to wet 
  deposition.


