# pyaerocom version 0.12.0 (release summary)

This release comes with many new features, major improvements and a more 
stable API. Please see the individual points below for major changes.

The notes below summarise the major updates since the release of version [0.
10.0](https://github.com/metno/pyaerocom/releases/tag/v0.10.0). This 
includes the changes that were done in the recent release of version 
[0.11.0](https://github.com/metno/pyaerocom/releases/tag/v0.11.0), which 
is the last version that officially supports the former "Aerocom 
Evaluation" tools, e.g. used extensively in [CAMS61 project](https://aerocom-evaluation.met.no/main.php?project=cams61_p3&exp=BASE).


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
- All this is packed into a new modular and intuitive 
[API](https://pyaerocom.readthedocs.io/en/latest/api-aeroval.html).

**Visit AeroVal**: https://aeroval.met.no/  
**Follow AeroVal on twitter**: https://twitter.com/AeroVal_MetNo

#### NOTE: **web** sub-package is deprecated 

- All code under **pyaerocom/web** is deprecated and this sub-package 
  does not exist anymore in v0.12.0. Relevant code has been shipped 
  and redesigned into the code basis for the new **AeroVal** tools 
  (**pyaerocom/aeroval** subpackage).
- Processing tools for old trends interface are deprecated. Instead trends 
  visualisation is included in the new **AeroVal** interface and can be 
  processed via the new tools in the **aeroval** subpackage.
- Former CLIs for web tools (pyaeroeval, pyaerotrends) are deprecated.
  However, the simple pyaerocom (pya) CLI is still available.

## New observation networks

- Added support for reading of EEA air pollution data
- Added support for reading of AirNow air pollution data
- Added support for reading of MarcoPolo air pollution data

## Further updates and improvements

- Improvements in EBAS reader, e.g.
  - Evaluation of individual timestamps to resolve ts_type of NASA Ames file.
  - Improved logic for automatic column selection.
  - Automatic conversion of vmr to conc and vice versa (e.g. vmro3 to conco3)
- Evaluation of wet deposition and precipitation data.
- Revised, more powerful and intuitive co-location routines.
  - E.g. ["per-station" time co-location](https://github.com/metno/pyaerocom/issues/301)
- Improved and more robust unit conversions
  - E.g. Automatic detection and correction of implicit deposition units to 
    explicit units, both for model and obs, centralised in [units_helpers.
    py](https://github.com/metno/pyaerocom/blob/master/pyaerocom/units_helpers.py) module.
- Improved robustness and performance of EMEP reader.
- Support reading and co-location of AeroCom model climatology files (year 
9999 in filename). See [here](https://github.com/metno/pyaerocom/pull/354) 
  for details.
- New features in `TsType` class (e.g.[infer ts_type from total seconds](https://github.com/metno/pyaerocom/pull/357))
- Improved and more clearly defined API.
  - E.g. [Harmonisation of ungridded reading API](https://github.com/metno/pyaerocom/pull/389)
- Installation with all requirements via PyPi
- Many bug fixes
- [Improved test coverage](https://app.codecov.io/gh/metno/pyaerocom).


