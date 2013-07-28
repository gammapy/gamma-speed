#!/bin/bash
#This script will make different types of io with file size of the first argument
#passed when calling the script
source $GAMMALIB/bin/gammalib-init.sh
mkdir plots

../code/ctobssim/src/./monitor.py -mt=1 "./make_io.py  -iot=gamma_save -s=$1"
../code/ctobssim/src/./monitor_plot.py --nrcsv=1 -o makeio -fn gamma_save
mkdir plots/gamma_save
mv *.csv plots/gamma_save

../code/ctobssim/src/./monitor.py -mt=1 "./make_io.py  -iot=gamma_saveto -s=$1"
../code/ctobssim/src/./monitor_plot.py --nrcsv=1 -o makeio -fn gamma_saveto
mkdir plots/gamma_saveto
mv *.csv plots/gamma_saveto

../code/ctobssim/src/./monitor.py -mt=1 "./make_io.py  -iot=fits_gen -s=$1"
../code/ctobssim/src/./monitor_plot.py --nrcsv=1 -o makeio -fn fits
mkdir plots/fit_gen
mv *.csv plots/fits_gen

../code/ctobssim/src/./monitor.py -mt=1 "./make_io.py  -iot=fits_copy -s=$1"
../code/ctobssim/src/./monitor_plot.py --nrcsv=1 -o makeio -fn fits_copy
mkdir plots/fits_copy
mv *.csv plots/fits_copy

../code/ctobssim/src/./monitor.py -mt=1 "cp copy1.fits copz2.fits"
../code/ctobssim/src/./monitor_plot.py --nrcsv=1 -o makeio -fn "cp"
mkdir plots/copy
mv *.csv plots/copy

rm -r *.fits *.csv *.log *.xml
