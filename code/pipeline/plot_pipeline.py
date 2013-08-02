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

def pipeline_separate_plots(my_plotter, outpref, log_exists=False):
    """
    this function makes separate plots for CPU, memory and disk IO usage
    """
    cpu_plot = my_plotter.CPU_plot('plots/CPU' + outpref)
    mem_plot = my_plotter.MEM_plot('plots/mem' + outpref)
    io_cumul_plot = my_plotter.IO_cumulative_plot('plots/io_cumul' + outpref)
    io_speed_plot = my_plotter.IO_speed_plot('plots/io_speed' + outpref)
    io_read = my_plotter.IO_read('plots/io_read' + outpref)

def pipeline_mplot(my_plotter, ncsv, outpref, log_exists):
    """
    add and modify a plot instance returned by monitor_plot.mplot
    """
    
    the_plot = my_plotter.mplot(outfile='', figtitle='pipeline measurement')
    
    if not os.path.exists('plots'):
        os.makedirs('plots')
    the_plot.savefig("plots/pipeline_mplot.png")

def pipeline_speed_up(my_plotter, outpref, log_exists):
    # first we want to plot the general speed up and efficiency
    if log_exists:
        aux = np.array([])
        cores = [i + 1 for i in range(my_plotter.ncsv)]
        times = pd.Series(index=cores)
        amd = pd.Series(index=cores)
        parallel_loop = pd.Series(index=cores)
        for i in xrange(my_plotter.ncsv):
            df = pd.read_csv(my_plotter.infile + "_CPUs=" + str(i + 1) + ".csv")
            aux = select_lines('pipeline_CPUs=' + str(i + 1) + '.csv', df.at[0, 'TIME'], ['gammaspeed:'])
            parallel_loop[i+1] = aux[1] - aux[0] + aux[3] - aux[2]

        paralleltime = parallel_loop[1]
        
        for i in xrange(my_plotter.ncsv):
            df = my_plotter.read_monitor_log(i)
            # time spent for the whole process
            times[i + 1] = df['TIME'].iget(-1) - df['TIME'].iget(0)
            amd[i+1] = times[1] / (times[1] - paralleltime + paralleltime / (i+1))
            
        plt.figure(21)
        my_plotter.splot(figtitle = 'Overall speed up and efficiency for pipeline', outfile="plots/" +outpref+'_general', speed_frame = times, amdahl_frame = amd)
             
        plt.figure(20)
        my_plotter.splot(figtitle = 'Parallel speed up and efficiency for pipeline', outfile="plots/" +outpref+'_parallel', speed_frame = parallel_loop, amdahl_frame = pd.Series(data=cores, index=cores))
    
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--infile', default='monitor',
                        help='Input file name - prefix')
    parser.add_argument('-n', '--nrcsv', default=multiprocessing.cpu_count(), type=int,
                        help='Number of csv files')
    parser.add_argument('-o', '--outpref', default='pipeline',
                        help='Outfile prefix')
    parser.add_argument('-log', default=False, type=bool,
                        help='if gammaspeed logging statements have been added to'
                        + 'ctools and gammalib, this option should be set to True')
    
    args = parser.parse_args()
    
    my_plotter = mtp.monitorplot(args.infile, args.nrcsv, " pipeline")
    pipeline_mplot(my_plotter, args.nrcsv, args.outpref, args.log)
    pipeline_speed_up(my_plotter, args.outpref, args.log)
    pipeline_separate_plots(my_plotter, args.outpref, args.log)
    
if __name__ == '__main__':
    main()