#!/usr/bin/env python

import monitor_plot as mtp
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
        result = np.append(
            result,
            ctobs[ctobs['EVENT'].str.contains(search_string[i])]['TIME'])
    return result


def ctobssim_separate_plots(my_plotter, ncsv, outpref, log_exists=False):
    """
    this function makes separate plots for CPU, memory and disk IO usage
    """
    my_plotter.CPU_plot('plots/' + outpref + 'CPU')
    my_plotter.MEM_plot('plots/' + outpref + 'mem')
    my_plotter.IO_cumulative_plot('plots/' + outpref + 'io_cumul')
    my_plotter.IO_speed_plot('plots/' + outpref + 'io_speed')
    my_plotter.IO_read('plots/' + outpref + 'io_read')


def ctobssim_mplot(my_plotter, ncsv, outpref, log_exists=False):
    """
    add and modify a plot instance returned by monitor_plot.mplot
    """

    the_plot = my_plotter.mplot(outfile='', figtitle='ctobssim measurements')

    # TODO: Add vertical lines for
    #         serial and parallel portions of the code
    #         write finished - disk IO lines
    # with ax1.fill_between(x=sim_loop, facecolor='red', interpolate=True)

    if not os.path.exists('plots'):
        os.makedirs('plots')
        print 'Made directory plots/'

    the_plot.savefig('plots/' + outpref + '_mplot.png')
    the_plot.close()


def ctobssim_speed_up(my_plotter, ncsv, outpref, log_exists=False):
    """
    plot both the overall and parallel speed up for ctlike
    and build Amdahl's Law prediction from log files
    """
    if log_exists:
        aux = np.array([])
        cores = [i + 1 for i in range(my_plotter.ncsv)]
        times = pd.Series(index=cores)
        amd = pd.Series(index=cores)
        parallel_loop = pd.Series(index=cores)
        for i in xrange(my_plotter.ncsv):
            df = pd.read_csv(
                my_plotter.infile + "_CPUs_" + str(i + 1) + ".csv")
            aux = select_lines(
                'ctobssim_CPUs_' + str(i + 1) + '.csv',
                df.at[0, 'TIME'],
                ['gammaspeed:parallel_region_start',
                 'gammaspeed:parallel_region_end'])
            parallel_loop[i + 1] = aux[1] - aux[0]

        paralleltime = parallel_loop[1]

        for i in xrange(my_plotter.ncsv):
            df = my_plotter.read_monitor_log(i)
            # time spent for the whole process
            times[i + 1] = df['TIME'].iget(-1) - df['TIME'].iget(0)
            amd[i + 1] = times[1] / \
                (times[1] - paralleltime + paralleltime / (i + 1))

        plt.figure(21)
        my_plotter.splot(
            figtitle='Overall speed up and efficiency for ctobssim',
            outfile="plots/" + outpref + '_general',
            speed_frame=times,
            amdahl_frame=amd)

        plt.figure(20)
        my_plotter.splot(
            figtitle='Parallel speed up and efficiency for ctobssim',
            outfile="plots/" + outpref + '_parallel',
            speed_frame=parallel_loop,
            amdahl_frame=pd.Series(data=cores,
                                   index=cores))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--infile', default='monitor',
                        help='Input file name - prefix')
    parser.add_argument('-n', '--nrcsv', 
                        default=multiprocessing.cpu_count(), type=int,
                        help='Number of csv files')
    parser.add_argument('-o', '--outpref', default='ctlike',
                        help='Outfile prefix')
    parser.add_argument('-log', default=False, type=bool,
                        help='if gammaspeed logging statements have been ' +
                        'added to ctools and gammalib, this option should' +
                        ' be set to True')

    args = parser.parse_args()

    my_plotter = mtp.MonitorPlot(args.infile, args.nrcsv, " ctobssim")
    ctobssim_mplot(my_plotter, args.nrcsv, args.outpref, args.log)
    ctobssim_separate_plots(my_plotter, args.nrcsv, args.outpref, args.log)
    ctobssim_speed_up(my_plotter, args.nrcsv, args.outpref, args.log)

if __name__ == '__main__':
    main()
