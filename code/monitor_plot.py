#!/usr/bin/env python

"""
Parse and plot the output of monitor.py

Example: ./monitor_plot.py --nrcsv=3 --outfile=performance --function=cp
will interpret the output of 3 .csv files and will make a plot with the name
    performance_cp.png in the directory plots/
"""
import argparse
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FormatStrFormatter
import multiprocessing
import numpy as np
import platform
TIME_ZONE_SHIFT = 7200  # the ctobssim log messages correspond to 
                        # Greenwich Mean Time and python makes the 
                        # measurements for the current time zone - 
                        # in this case, CET -> 7200 s shift

class monitorplot:
    def __init__(self, infile, ncsv):
        self.infile = infile
        self.ncsv = ncsv
        
#     def select_lines(infile, start_time, search_string):
#         ctobs = pd.read_csv(infile)
#         result = np.array([])
#         ctobs['TIME'] = ctobs['TIME'] - start_time + TIME_ZONE_SHIFT
#         for i in range(len(search_string)):
#             result = np.append(result, ctobs[ctobs['EVENT'].str.contains(search_string[i])]['TIME'])    
#         return result
    
    def mplot(self, outfile, func, figtitle):
        # read the values into a csv file        
        fig = plt.figure(1, figsize=(15.0, 15.0))
        
        for i in xrange(self.ncsv):
            filename = self.infile + "_CPUs=" + str(i + 1) + ".csv"
            df = readcsv(filename)
            if i == 0:
                core_label = '1 core'
            else:
                core_label = str(i + 1) + ' cores'
     
    #          The monitor_plot was originally intended to measure ctobssim
    #          In order to adapt it to general purposes, the following ctobssim 
    #          specific code has been made optional
#             if func == 'ctobssim':
#                 sim_loop = select_lines('ctobssim_CPUs=' + str(i + 1) + '.csv', df.at[0, 'TIME'], ['gammaspeed:libraries_loaded', 'gammaspeed:events_simulated'])
#                 w_start = select_lines('ctobssim_CPUs=' + str(i + 1) + '.csv', df.at[0, 'TIME'], ['write_FILE_start'])
#                 w_stop = select_lines('ctobssim_CPUs=' + str(i + 1) + '.csv', df.at[0, 'TIME'], ['write_FILE_done'])
                       
             
             
            plt.subplot(411)
            df.plot(x='TIME', y='CPU_USAGE', label=core_label)
            plt.ylabel('CPU (%)')
            plt.title('CPU usage for ' + func)
            plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            plt.legend(loc=0, ncol=self.ncsv / 2)
            plt.xlabel('Time(s)')
            [x1, x2, y1, y2] = plt.axis()
            plt.axis((x1, x2, y1, y2 * 1.1))
#             if func == 'ctobssim':   
#                 plt.vlines(sim_loop, ymin=y1, ymax=y2, colors='m')
#                 plt.vlines(w_start, ymin=y1, ymax=y2, colors='r')
#                 plt.vlines(w_stop, ymin=y1, ymax=y2, colors='g')
              
            mem = plt.subplot(412)
            df.plot(x='TIME', y='MEM_USAGE', label=core_label)
            plt.ylabel('RAM usage (MB)')
            plt.title('Memory usage for ' + func)
            plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            plt.legend(loc=0, ncol=self.ncsv / 2)
            plt.xlabel('Time(s)')
            [x1, x2, y1, y2] = plt.axis()
            plt.axis((x1, x2, y1, y2 * 1.1))
#             if func == 'ctobssim':
#                 plt.vlines(w_start, ymin=y1, ymax=y2, colors='r')
#                 plt.vlines(w_stop, ymin=y1, ymax=y2, colors='g')
             
    #         plt.subplot(514)
    #         df['IO_READ_COUNTS'].plot()
    #         plt.ylabel('IO Read (counts)')
    #         plt.title('IO Read counts for ' + name)
    #   
    #         plt.subplot(515)
    #         df['IO_WRITE_COUNTS'].plot()
    #         plt.ylabel('IO Write (counts)')
    #         plt.title('IO write counts for ' + name)     
              
            plt.subplot(413)
            df['IO_WRITE_BYTES'] = df['IO_WRITE_BYTES'] / int(1e6)
            iow = df.plot(x='TIME', y='IO_WRITE_BYTES', label=core_label)
            plt.ylabel('IO Write (MB)')
            plt.title('Write sum for ' + func)
            plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            plt.legend(loc=0, ncol=self.ncsv / 2)
            plt.xlabel('Time(s)')
            [x1, x2, y1, y2] = plt.axis()
            plt.axis((x1, x2, y1, y2 * 1.1))
             
            df['IO_WRITE_BYTES'] = df['IO_WRITE_BYTES'].diff() / df['TIME'].diff()
            plt.subplot(414)
            iow = df.plot(x='TIME', y='IO_WRITE_BYTES', label=core_label)
            plt.ylabel('IO Write (MB/s)')
            plt.title('Write rate for ' + func)
            plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            plt.legend(loc=0, ncol=self.ncsv / 2)
            plt.xlabel('Time(s)')
            [x1, x2, y1, y2] = plt.axis()
            plt.axis((x1, x2, y1, y2 * 1.1))
#             if func == 'ctobssim':
#                 plt.vlines(w_start, ymin=y1, ymax=y2, colors='r')
#                 plt.vlines(w_stop, ymin=y1, ymax=y2, colors='g')
             
             
        fig.subplots_adjust(hspace=.5)
         
#         if func == 'ctobssim':    
#             s = pd.read_csv('temp.csv')
#             plt_name = 'plots/' + outpref + str(float(s['values'][3]) - float(s['values'][2])) + 'sec_' + s['values'][11] + 'obs_' + s['values'][12] + '.png'
#             fig.suptitle('Observation time:' + str(float(s['values'][3]) - float(s['values'][2])) + ' seconds; ' + s['values'][11] + ' runs; Machine: ' + s['values'][12])
#         else:
        fig.suptitle(figtitle)
         
        plt.savefig(outfile+)
    #     plt.show()
    
def readcsv(filename):
    df = pd.read_csv(filename)
    name = df.at[1, 'PROCESS_NAME']
    df['MEM_USAGE'] = df['MEM_USAGE'] / int(1e6)
    df['TIME'] = df['TIME'] - df.at[0, 'TIME']
    return df

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--infile', default='monitor',
                        help='Input file name - prefix')
    parser.add_argument('-n', '--nrcsv', default=multiprocessing.cpu_count(), type=int,
                        help='Number of csv files')
    parser.add_argument('-o', '--outpref', default='',
                        help='Outfile prefix')
    parser.add_argument('-fn', '--function', default='',
                        help='If a ctools function has been monitored, it should be mentioned here\\ Ex. -fn=ctobssim')
    
    args = parser.parse_args()
    my_mplot = monitorplot(args.infile, args.nrcsv)
    my_mplot.mplot(outfile='plots/' + args.outpref + '_' + args.function + '_' + platform.node() + '.png',
           func=args.function, figtitle='Machine: ' + platform.node())

if __name__ == '__main__':
    main()
