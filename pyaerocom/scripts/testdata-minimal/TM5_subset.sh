#!/bin/bash -x
# Extract a few lat/lon points to decrease filesize
LON=20,30
LAT=20,30

ncks -d lat,"$LAT" -d lon,"$LON" aerocom3_TM5-met2010_AP3-CTRL2019_abs550aer_Column_2010_daily.nc ./aerocom3_TM5-met2010_AP3-CTRL2019_abs550aer_Column_2010_daily.nc

ncks -d lat,"$LAT" -d lon,"$LON" aerocom3_TM5-met2010_AP3-CTRL2019_od550aer_Column_2010_daily.nc ./aerocom3_TM5-met2010_AP3-CTRL2019_od550aer_Column_2010_daily.nc
