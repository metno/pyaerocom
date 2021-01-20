#!/bin/bash
set -x
#shell script to convert Aeolus data to netcdf
# for dir in `find /lustre/storeB/project/fou/kl/admaeolus/data.rev.2A10 -mindepth 3 -type d | sort`
version="2A09"
cmd="/home/jang/data/Python3/pyaerocom/pyaerocom/io/read_aeolus_l2a_data.py"
for dir in `cat ./${version}_dirs.txt`
do echo ${dir}
  outdir=`echo ${dir} | rev | cut '-d/' -f 4- | rev`
  outdate=`echo ${dir} | rev | cut '-d/' -f1-2 | rev | sed -e 's/\///g' -e 's/\-//g'`
  ncoutfile="${outdir}/netcdf/${outdate}_${version}.nc"
  logoutfile="${outdir}/netcdf/${outdate}_${version}.log"
  ${cmd} -O --variables ec355aer --outfile ${ncoutfile} --logfile ${logoutfile} --file ${dir}/*.TGZ
done