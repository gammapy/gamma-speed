#!/bin/bash

#This shell script assumes that CTOOLS and GAMMALIB paths were previously
#exported via the command line
source $CTOOLS/bin/ctools-init.sh
source $GAMMALIB/bin/gammalib-init.sh

./monitor_ctobssim.py -log=True --loop=True -ca=" -dur=1800 -nobs=10"
./plot_ctobssim.py -log=True -o="ctobssim_10OBS_"
mkdir plots/10_OBS_DATA
cp *.csv plots/10_OBS_DATA
cp *.log plots/10_OBS_DATA

./monitor_ctobssim.py -log=True --loop=True -ca=" -dur=1800 -nobs=100"
./plot_ctobssim.py -log=True -o="ctobssim_100OBS_"
mkdir plots/100_OBS_DATA
cp *.csv plots/100_OBS_DATA
cp *.log plots/100_OBS_DATA

./monitor_ctobssim.py -log=True --loop=True -ca=" -dur=1800 -nobs=1000"
./plot_ctobssim.py -log=True -o="ctobssim_1000OBS_"
mkdir plots/1000_OBS_DATA
cp *.csv plots/1000_OBS_DATA
cp *.log plots/1000_OBS_DATA

rm -r *.fits *.csv *.log *.xml
