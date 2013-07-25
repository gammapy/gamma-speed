#!/usr/bin/env python

import src.monitor_plot as mtp
import argparse
import multiprocessing
import pandas as pd
import numpy as np 
from matplotlib import pyplot as plt
import os

def select_lines(infile, start_time, search_string):
    ctobs = pd.read_csv(infile)
    result = np.array([])
    ctobs['TIME'] = ctobs['TIME'] - start_time
    for i in range(len(search_string)):
        result = np.append(result, ctobs[ctobs['EVENT'].str.contains(search_string[i])]['TIME'])    
    return result

def ctobssim_separate_plots(my_plotter, ncsv, log_exists=False):
    """
    this function makes separate plots for CPU, memory and disk IO usage
    """
    cpu_plot = my_plotter.CPU_plot('plots/CPU')
    mem_plot = my_plotter.MEM_plot('plots/mem')
    io_cumul_plot = my_plotter.IO_cumulative_plot('plots/io_cumul')
    io_speed_plot = my_plotter.IO_speed_plot('plots/io_speed')
    

def ctobssim_mplot(my_plotter, ncsv, log_exists=False):
    """
    add and modify a plot instance returned by monitor_plot.mplot
    """
    
    the_plot = my_plotter.mplot(outfile='', figtitle='ctobssim measurements')
    
    # TODO: Add vertical lines for
    #         simulation start/endpoints - for CPU usage
    #         write finished - disk IO lines
    # with ax1.fill_between(x=sim_loop, facecolor='red', interpolate=True)
    if log_exists:
        for i in xrange(ncsv):
            df = pd.read_csv(my_plotter.infile + "_CPUs=" + str(i + 1) + ".csv")
            sim_loop = select_lines('ctobssim_CPUs=' + str(i + 1) + '.csv', df.at[0, 'TIME'], ['gammaspeed:libraries_loaded', 'gammaspeed:events_simulated'])
            write_loop = select_lines('ctobssim_CPUs=' + str(i + 1) + '.csv', df.at[0, 'TIME'], ['write_FILE_start', 'write_FILE_done'])
            
            the_plot.subplot(411)
            [x1, x2, y1, y2] = the_plot.axis()
            the_plot.vlines(sim_loop, ymin=y1, ymax=y2, colors='m')
            
            the_plot.subplot(413)
            [x1, x2, y1, y2] = the_plot.axis()
            the_plot.vlines(write_loop, ymin=y1, ymax=y2, colors='m')
            
            the_plot.subplot(413)
            [x1, x2, y1, y2] = the_plot.axis()
            the_plot.vlines(write_loop, ymin=y1, ymax=y2, colors='m')
            
            the_plot.subplot(414)
            [x1, x2, y1, y2] = the_plot.axis()
            the_plot.vlines(write_loop, ymin=y1, ymax=y2, colors='m')
            
    if not os.path.exists('plots'):
        os.makedirs('plots')
        print 'Made directory plots/'
    
    the_plot.close()

def ctobssim_speed_up(my_plotter, ncsv, log_exists=False):
    # first we want to plot the general speed up and efficiency
    plt.figure(1)
    my_plotter.speed_up(ncores = ncsv, out_pref='ctobssim_general', figtitle = 'Overall speed up and efficiency for ctobssim')
     
    if log_exists:
        # now, we will extract the duration of each simulation and plot the speed up for the parallel regions
        plt.figure(2)
        parallel_loop = np.array([])
        aux = np.array([])
        for i in xrange(ncsv):
            df = pd.read_csv(my_plotter.infile + "_CPUs=" + str(i + 1) + ".csv")
            aux = select_lines('ctobssim_CPUs=' + str(i + 1) + '.csv', df.at[0, 'TIME'], ['gammaspeed:libraries_loaded', 'gammaspeed:events_simulated'])
            parallel_loop = np.append(parallel_loop, aux[1]-aux[0])
        
        my_plotter.speed_up(ncores = ncsv, out_pref='ctobssim_parallel', figtitle = 'Parallel region speed up and efficiency for ctobssim', speed_frame=parallel_loop)
    
    
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--infile', default='monitor',
                        help='Input file name - prefix')
    parser.add_argument('-n', '--nrcsv', default=multiprocessing.cpu_count(), type=int,
                        help='Number of csv files')
    parser.add_argument('-o', '--outpref', default='',
                        help='Outfile prefix')
    parser.add_argument('-log', default=False, type=bool,
                        help='if gammaspeed logging statements have been added to'
                        + 'ctools and gammalib, this option should be set to True')
    
    
    args = parser.parse_args()
    
    my_plotter = mtp.monitorplot(args.infile, args.nrcsv, "ctobssim")
    ctobssim_mplot(my_plotter, args.nrcsv, args.log)
    ctobssim_speed_up(my_plotter, args.nrcsv, args.log)
    ctobssim_separate_plots(my_plotter, args.nrcsv, args.log)
    
if __name__ == '__main__':
    main()