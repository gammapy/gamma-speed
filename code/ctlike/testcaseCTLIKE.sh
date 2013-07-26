#!/bin/bash

# This shell script assumes that CTOOLS and GAMMALIB paths were previously
# exported via the command line and also that there is a subdirectory which contanins
# the three xml files referenced by the -infile argument
source $CTOOLS/bin/ctools-init.sh
source $GAMMALIB/bin/gammalib-init.sh

./monitor_ctlike.py -log=True --loop=True -ca=" -infile=data/sim_events10.xml"
./plot_ctlike.py -log=True -o="ctlike_10OBS_"
mkdir plots/10_OBS_DATA
cp *.csv plots/10_OBS_DATA
cp *.log plots/10_OBS_DATA

./monitor_ctlike.py -log=True --loop=True -ca=" -infile=data/sim_events50.xml"
./plot_ctlike.py -log=True -o="ctlike_50OBS_"
mkdir plots/50_OBS_DATA
cp *.csv plots/50_OBS_DATA
cp *.log plots/50_OBS_DATA

./monitor_ctlike.py -log=True --loop=True -ca=" -infile=data/sim_events100.xml"
./plot_ctlike.py -log=True -o="ctlike_100OBS_"
mkdir plots/100_OBS_DATA
cp *.csv plots/100_OBS_DATA
cp *.log plots/100_OBS_DATA

./monitor_ctlike.py -log=True --loop=True -ca=" -infile=data/sim_events200.xml"
./plot_ctlike.py -log=True -o="ctlike_200OBS_"
mkdir plots/200_OBS_DATA
cp *.csv plots/200_OBS_DATA
cp *.log plots/200_OBS_DATA

rm -r *.fits *.csv *.log *.xml
