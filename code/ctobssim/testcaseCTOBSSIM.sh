#!/bin/bash
source $CTOOLS/bin/ctools-init.sh
mkdir plots

.././monitor.py ".././run_multi_ctobssim.py -nobs=4 -dur=1000"
.././monitor_plot.py
.././speedup_plot.py

.././monitor.py ".././run_multi_ctobssim.py -nobs=4 -dur=10000"
.././monitor_plot.py
.././speedup_plot.py

.././monitor.py ".././run_multi_ctobssim.py -nobs=4 -dur=100000"
.././monitor_plot.py
.././speedup_plot.py

rm -r *.fits *.csv *.log *.xml

