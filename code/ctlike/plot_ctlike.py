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


def ctlike_mplot(my_plotter, ncsv):
    """
    add and modify a plot instance returned by monitor_plot.mplot
    """
    
    the_plot = my_plotter.mplot(outfile='', figtitle='ctlike measurements')

    # Customize plot size
    the_plot.subplot(411)
    [x1, x2, y1, y2] = the_plot.axis()
    the_plot.axis((x1, x2, y1, y2 * 3.1))
    
    the_plot.subplot(412)
    [x1, x2, y1, y2] = the_plot.axis()
    the_plot.axis((x1, x2, y1, y2 * 1.5))
    
    # TODO: Add vertical lines for
    #         simulation start/endpoints - for CPU usage
    #         write finished - disk IO lines
    # with ax1.fill_between(x=sim_loop, facecolor='red', interpolate=True)
    for i in xrange(ncsv):
        df = pd.read_csv(my_plotter.infile + "_CPUs=" + str(i + 1) + ".csv")
        sim_loop = select_lines('ctlike_CPUs=' + str(i + 1) + '.csv', df.at[0, 'TIME'], ['gammaspeed:libraries_loaded', 'gammaspeed:events_simulated'])
        write_loop = select_lines('ctlike_CPUs=' + str(i + 1) + '.csv', df.at[0, 'TIME'], ['write_FILE_start', 'write_FILE_done'])
        
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
    the_plot.savefig("plots/ctlike_mplot.png")

def ctlike_speed_up(my_plotter, ncsv):
    # first we want to plot the general speed up and efficiency
    plt.figure(1)
    my_plotter.speed_up(ncores = ncsv, out_pref='ctlike_general', figtitle = 'Overall speed up and efficiency for ctlike')
     
    # now, we will extract the duration of each simulation and plot the speed up for the parallel regions
    plt.figure(2)
    parallel_loop = np.array([])
    aux = np.array([])
    for i in xrange(ncsv):
        df = pd.read_csv(my_plotter.infile + "_CPUs=" + str(i + 1) + ".csv")
        aux = select_lines('ctlike_CPUs=' + str(i + 1) + '.csv', df.at[0, 'TIME'], ['gammaspeed:omp_region_start', 'gammaspeed:omp_region_end'])
        parallel_loop = np.append(parallel_loop, aux[1]-aux[0])
    
    my_plotter.speed_up(ncores = ncsv, out_pref='ctlike_parallel', figtitle = 'Parallel region speed up and efficiency for ctlike', speed_frame=parallel_loop)
    
    
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--infile', default='monitor',
                        help='Input file name - prefix')
    parser.add_argument('-n', '--nrcsv', default=multiprocessing.cpu_count(), type=int,
                        help='Number of csv files')
    parser.add_argument('-o', '--outpref', default='',
                        help='Outfile prefix')
    
    args = parser.parse_args()
    
    my_plotter = mtp.monitorplot(args.infile, args.nrcsv, "ctlike")
    ctlike_mplot(my_plotter, args.nrcsv)
    ctlike_speed_up(my_plotter, args.nrcsv)
    
if __name__ == '__main__':
    main()