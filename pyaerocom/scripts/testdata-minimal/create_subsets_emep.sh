#!/bin/bash -x

INFILEPATH="/lustre/storeB/project/fou/kl/emep/ModelRuns/2019_REPORTING/EMEP01_L20EC_rv4_33.2017/Base_fullrun.nc"
VARIABLES="SURF_ug_O3,SURF_ppb_O3,SURF_ug_PM10_rh50,SURF_ug_PM25_rh50,SURF_ug_NO2"
TMPFILE="./tmp.nc"
LAT=50,52
LON=10,12

ncks -d lat,"$LAT" -d lon,"$LON" -v "$VARIABLES" "$INFILEPATH" "$TMPFILE"

# netcdf files with dimension set to unlimited takes up a lot of space.
# dump the file, change UNLIMITED to an integer and regenerate the file
OUTFILEPATH="./Base_fullrun.nc"
ncdump "$TMPFILE"| sed -e "s/UNLIMITED/1/" | ncgen -o "$OUTFILEPATH"
rm "$TMPFILE"


INFILEPATH="/lustre/storeB/project/fou/kl/emep/ModelRuns/2019_REPORTING/EMEP01_L20EC_rv4_33.2017/Base_month.nc"
ncks -d time,0,2 -d lat,"$LAT" -d lon,"$LON" -v "$VARIABLES" "$INFILEPATH" "$TMPFILE"
OUTFILEPATH="./Base_month.nc"
ncdump "$TMPFILE"| sed -e "s/UNLIMITED/3/" | ncgen -o "$OUTFILEPATH"
rm "$TMPFILE"

INFILEPATH="/lustre/storeB/project/fou/kl/emep/ModelRuns/2019_REPORTING/EMEP01_L20EC_rv4_33.2017/Base_day.nc"
ncks -d time,0,2 -d lat,"$LAT" -d lon,"$LON" -v "$VARIABLES" "$INFILEPATH" "$TMPFILE"
OUTFILEPATH="./Base_day.nc"
ncdump "$TMPFILE"| sed -e "s/UNLIMITED/3/" | ncgen -o "$OUTFILEPATH"
rm "$TMPFILE"
