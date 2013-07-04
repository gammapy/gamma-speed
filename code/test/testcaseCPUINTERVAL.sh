#!/bin/bash
source $CTOOLS/bin/ctools-init.sh
mkdir plots

.././monitor.py -ti 0.001 ".././run_multi_ctobssim.py -nobs=4 -dur=10000"
.././monitor_plot.py -o "CPUINTERVAL=0.001_"

.././monitor.py -ti 0.01 ".././run_multi_ctobssim.py -nobs=4 -dur=10000"
.././monitor_plot.py -o "CPUINTERVAL=0.01_"

.././monitor.py -ti 0.1 ".././run_multi_ctobssim.py -nobs=4 -dur=10000"
.././monitor_plot.py -o "CPUINTERVAL=0.1_"

.././monitor.py -ti 1 ".././run_multi_ctobssim.py -nobs=4 -dur=10000"
.././monitor_plot.py -o "CPUINTERVAL=1.0_"

rm -r *.fits *.csv *.log *.xml

