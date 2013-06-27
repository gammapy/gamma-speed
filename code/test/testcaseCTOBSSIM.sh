#!/bin/bash
# Location: same directory as ../.monitor.py ../.monitorPlot.py ../.run_multi_ctobssim.py
source $CTOOLS/bin/ctools-init.sh
mkdir plots

.././monitor.py ".././run_multi_ctobssim.py -nobs=4 -dur=1000"
.././monitorPlot.py

.././monitor.py ".././run_multi_ctobssim.py -nobs=4 -dur=10000"
.././monitorPlot.py

../.monitor.py "../.run_multi_ctobssim.py -nobs=4 -dur=100000"
../.monitorPlot.py

rm -r *.fits *.csv *.log *.xml

