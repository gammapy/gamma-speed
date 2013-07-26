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

./monitor_ctobssim.py -log=True --loop=True -ca=" -dur=1800 -nobs=50"
./plot_ctobssim.py -log=True -o="ctobssim_50OBS_"
mkdir plots/50_OBS_DATA
cp *.csv plots/50_OBS_DATA
cp *.log plots/50_OBS_DATA

./monitor_ctobssim.py -log=True --loop=True -ca=" -dur=1800 -nobs=100"
./plot_ctobssim.py -log=True -o="ctobssim_100OBS_"
mkdir plots/100_OBS_DATA
cp *.csv plots/100_OBS_DATA
cp *.log plots/100_OBS_DATA

./monitor_ctobssim.py -log=True --loop=True -ca=" -dur=1800 -nobs=200"
./plot_ctobssim.py -log=True -o="ctobssim_200OBS_"
mkdir plots/200_OBS_DATA
cp *.csv plots/200_OBS_DATA
cp *.log plots/200_OBS_DATA

rm -r *.fits *.csv *.log *.xml
