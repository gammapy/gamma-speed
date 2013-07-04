#!/bin/bash
source $GAMMALIB/bin/gammalib-init.sh
mkdir plots

.././monitor.py -mt=1 "../../scripts/./make_io.py  -iot=gamma_save -s=500"
.././monitor_plot.py -o makeio -fn gamma_save

.././monitor.py -mt=1 "../../scripts/./make_io.py  -iot=gamma_saveto -s=500"
.././monitor_plot.py -o makeio -fn gamma_saveto

.././monitor.py -mt=1 "../../scripts/./make_io.py  -iot=fits_gen -s=500"
.././monitor_plot.py -o makeio -fn fits

.././monitor.py -mt=1 "../../scripts/./make_io.py  -iot=fits_copy -s=250"
.././monitor_plot.py -o makeio -fn fits_copy

.././monitor.py -mt=1 "cp copy1.fits copz2.fits"
.././monitor_plot.py -o makeio -fn "cp"

rm -r *.fits *.csv *.log *.xml
