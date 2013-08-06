#!/bin/bash

#This shell script assumes that CTOOLS and GAMMALIB paths were previously
#exported via the command line
source $CTOOLS/bin/ctools-init.sh
source $GAMMALIB/bin/gammalib-init.sh

./monitor_pipeline.py -log=True --loop=True -pa=" -type=in_memory -nobs=50"
./plot_pipeline.py -log=True -o="pipeline_INMEMORY_50OBS_"
mkdir plots/INMEMORY_50_DATA
cp *.csv plots/INMEMORY_50_DATA
cp *.log plots/INMEMORY_50_DATA

./monitor_pipeline.py -log=True --loop=True -pa=" -type=save -nobs=50"
./plot_pipeline.py -log=True -o="pipeline_INMEMORY_50OBS_"
mkdir plots/SAVE_50_DATA
cp *.csv plots/SAVE_50_DATA
cp *.log plots/SAVE_50_DATA

rm -r *.fits *.csv *.log *.xml
